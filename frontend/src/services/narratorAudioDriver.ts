import type { NarrationResponse } from "../types/narrator";
import { narratorApi } from "./narrator";

// Module-scoped reference to prevent Chromium GC from collecting active utterances mid-speech
let activeUtterance: SpeechSynthesisUtterance | null = null;
let sharedAudioElement: HTMLAudioElement | null = null;
let activePlaybackToken = 0;

export function getActiveUtterance(): SpeechSynthesisUtterance | null {
  return activeUtterance;
}

const MAX_CHUNK_CHARS = 180;

export function splitScriptIntoChunks(
  script: string,
  maxChars: number = MAX_CHUNK_CHARS
): string[] {
  const cleaned = script.replace(/\s+/g, " ").trim();
  if (!cleaned) {
    return [];
  }
  const rawSentences = cleaned.split(/(?<=[.!?])\s+/);
  const chunks: string[] = [];
  let current = "";

  for (const sentence of rawSentences) {
    if (!sentence) continue;
    if (sentence.length > maxChars) {
      if (current) {
        chunks.push(current.trim());
        current = "";
      }
      const words = sentence.split(" ");
      let wordChunk = "";
      for (const word of words) {
        if ((wordChunk + " " + word).trim().length <= maxChars) {
          wordChunk = (wordChunk + " " + word).trim();
        } else {
          if (wordChunk) chunks.push(wordChunk);
          wordChunk = word.slice(0, maxChars);
        }
      }
      if (wordChunk) chunks.push(wordChunk);
      continue;
    }

    const candidate = current ? `${current} ${sentence}` : sentence;
    if (candidate.length <= maxChars) {
      current = candidate;
    } else {
      if (current) chunks.push(current.trim());
      current = sentence;
    }
  }

  if (current) {
    chunks.push(current.trim());
  }
  return chunks;
}

function getSharedAudio(): HTMLAudioElement | null {
  if (typeof window === "undefined" || typeof Audio === "undefined") {
    return null;
  }
  if (!sharedAudioElement) {
    sharedAudioElement = new Audio();
    sharedAudioElement.preload = "auto";
  }
  return sharedAudioElement;
}

async function ensureVoicesLoaded(): Promise<SpeechSynthesisVoice[]> {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) {
    return [];
  }
  const existing = window.speechSynthesis.getVoices();
  if (existing.length > 0) {
    return existing;
  }
  return new Promise<SpeechSynthesisVoice[]>((resolve) => {
    let settled = false;
    const finish = () => {
      if (settled) return;
      settled = true;
      window.speechSynthesis.removeEventListener("voiceschanged", onVoicesChanged);
      resolve(window.speechSynthesis.getVoices());
    };
    const onVoicesChanged = () => finish();
    window.speechSynthesis.addEventListener("voiceschanged", onVoicesChanged);
    window.setTimeout(finish, 350);
  });
}

export interface PlayNarrationCallbacks {
  isMuted: boolean;
  onStart?: () => void;
  onEnd?: () => void;
  onNeedsUserGesture?: () => void;
}

export function stopNarrationPlayback(): void {
  activePlaybackToken += 1;
  if (sharedAudioElement) {
    try {
      sharedAudioElement.pause();
      sharedAudioElement.removeAttribute("src");
      sharedAudioElement.load();
    } catch {
      // Ignore audio element reset errors
    }
  }
  if (typeof window !== "undefined" && "speechSynthesis" in window) {
    try {
      window.speechSynthesis.cancel();
    } catch {
      // Ignore speechSynthesis cancel errors
    }
  }
  activeUtterance = null;
}

export async function playNarrationResponse(
  narration: NarrationResponse,
  callbacks: PlayNarrationCallbacks
): Promise<void> {
  stopNarrationPlayback();
  const token = activePlaybackToken;

  if (callbacks.isMuted) {
    callbacks.onEnd?.();
    return;
  }

  if (narration.voice_source === "voicestudio" && narration.audio_url) {
    const playedMp3 = await playMp3Url(
      narratorApi.getAudioUrl(narration.audio_url),
      token,
      callbacks
    );
    if (playedMp3 || token !== activePlaybackToken) {
      return;
    }
  }

  await playBrowserSpeech(narration.script, token, callbacks);
}

async function playMp3Url(
  url: string,
  token: number,
  callbacks: PlayNarrationCallbacks
): Promise<boolean> {
  const audio = getSharedAudio();
  if (!audio) {
    return false;
  }

  return new Promise<boolean>((resolve) => {
    const cleanup = () => {
      audio.onended = null;
      audio.onerror = null;
    };

    audio.onended = () => {
      cleanup();
      if (token === activePlaybackToken) {
        callbacks.onEnd?.();
      }
      resolve(true);
    };

    audio.onerror = () => {
      cleanup();
      resolve(false);
    };

    audio.src = url;
    callbacks.onStart?.();
    const playPromise = audio.play();
    if (playPromise !== undefined) {
      playPromise.catch((err: unknown) => {
        cleanup();
        const errName = err instanceof DOMException ? err.name : (err as { name?: string })?.name;
        if (errName === "AbortError") {
          callbacks.onEnd?.();
          resolve(true);
          return;
        }
        if (errName === "NotAllowedError") {
          callbacks.onNeedsUserGesture?.();
          callbacks.onEnd?.();
          resolve(true);
          return;
        }
        resolve(false);
      });
    }
  });
}

async function playBrowserSpeech(
  script: string,
  token: number,
  callbacks: PlayNarrationCallbacks
): Promise<void> {
  if (
    typeof window === "undefined" ||
    !("speechSynthesis" in window) ||
    typeof SpeechSynthesisUtterance === "undefined"
  ) {
    callbacks.onEnd?.();
    return;
  }

  const chunks = splitScriptIntoChunks(script, MAX_CHUNK_CHARS);
  if (chunks.length === 0) {
    callbacks.onEnd?.();
    return;
  }

  try {
    window.speechSynthesis.cancel();
  } catch {
    // Ignore cancel errors
  }

  const voices = await ensureVoicesLoaded();
  if (token !== activePlaybackToken) {
    callbacks.onEnd?.();
    return;
  }

  const preferredVoice =
    voices.find((v) => v.lang.toLowerCase().startsWith("en-us")) ??
    voices.find((v) => v.lang.toLowerCase().startsWith("en")) ??
    null;

  callbacks.onStart?.();

  for (const chunk of chunks) {
    if (token !== activePlaybackToken) {
      break;
    }
    await new Promise<void>((resolve) => {
      const utterance = new SpeechSynthesisUtterance(chunk);
      activeUtterance = utterance;
      if (preferredVoice) {
        utterance.voice = preferredVoice;
      }
      utterance.rate = 1.03;
      utterance.pitch = 0.98;

      const timeoutId = window.setTimeout(() => {
        resolve();
      }, 14000);

      utterance.onend = () => {
        window.clearTimeout(timeoutId);
        resolve();
      };
      utterance.onerror = () => {
        window.clearTimeout(timeoutId);
        resolve();
      };

      try {
        window.speechSynthesis.speak(utterance);
      } catch {
        window.clearTimeout(timeoutId);
        resolve();
      }
    });
  }

  activeUtterance = null;
  if (token === activePlaybackToken) {
    callbacks.onEnd?.();
  }
}
