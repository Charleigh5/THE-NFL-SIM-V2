import { useState, useEffect, useCallback, useRef } from "react";
import type { ReactNode } from "react";
import { Howl } from "howler";
import { STORAGE_KEY, AudioContext } from "./AudioTypes";
import type { AudioPreferences } from "./AudioTypes";

const getStoredPreferences = (): AudioPreferences => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch {
    // Ignore localStorage errors
  }
  return { volume: 0.5, isMuted: false };
};

const savePreferences = (prefs: AudioPreferences): void => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
  } catch {
    // Ignore localStorage errors
  }
};

export const AudioProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const prefs = getStoredPreferences();
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolumeState] = useState(prefs.volume);
  const [isMuted, setIsMuted] = useState(prefs.isMuted);
  const soundRef = useRef<Howl | null>(null);

  // Initialize Howl instance
  useEffect(() => {
    soundRef.current = new Howl({
      src: ["/audio/main-theme.mp3"],
      loop: true,
      volume: isMuted ? 0 : volume,
      html5: true, // Better for large files, enables streaming
      preload: true,
      onplay: () => setIsPlaying(true),
      onpause: () => setIsPlaying(false),
      onstop: () => setIsPlaying(false),
      onend: () => setIsPlaying(false),
    });

    return () => {
      soundRef.current?.unload();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Update volume when changed
  useEffect(() => {
    if (soundRef.current) {
      soundRef.current.volume(isMuted ? 0 : volume);
    }
    savePreferences({ volume, isMuted });
  }, [volume, isMuted]);

  const play = useCallback(() => {
    if (soundRef.current && !soundRef.current.playing()) {
      soundRef.current.play();
    }
  }, []);

  const pause = useCallback(() => {
    if (soundRef.current) {
      soundRef.current.pause();
    }
  }, []);

  const toggle = useCallback(() => {
    if (soundRef.current) {
      if (soundRef.current.playing()) {
        soundRef.current.pause();
      } else {
        soundRef.current.play();
      }
    }
  }, []);

  const setVolume = useCallback(
    (newVolume: number) => {
      const clampedVolume = Math.max(0, Math.min(1, newVolume));
      setVolumeState(clampedVolume);
      if (clampedVolume > 0 && isMuted) {
        setIsMuted(false);
      }
    },
    [isMuted]
  );

  const toggleMute = useCallback(() => {
    setIsMuted((prev) => !prev);
  }, []);

  return (
    <AudioContext.Provider
      value={{
        isPlaying,
        volume,
        isMuted,
        play,
        pause,
        toggle,
        setVolume,
        toggleMute,
      }}
    >
      {children}
    </AudioContext.Provider>
  );
};
