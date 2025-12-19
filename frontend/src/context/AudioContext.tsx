import { createContext, useContext, useState, useEffect, useCallback, useRef } from "react";
import type { ReactNode } from "react";
import { Howl } from "howler";

interface AudioContextType {
  isPlaying: boolean;
  volume: number;
  isMuted: boolean;
  play: () => void;
  pause: () => void;
  toggle: () => void;
  setVolume: (volume: number) => void;
  toggleMute: () => void;
}

const STORAGE_KEY = "nfl-sim-audio-prefs";

interface AudioPreferences {
  volume: number;
  isMuted: boolean;
}

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

const AudioContext = createContext<AudioContextType | undefined>(undefined);

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

export const useAudio = (): AudioContextType => {
  const context = useContext(AudioContext);
  if (context === undefined) {
    throw new Error("useAudio must be used within an AudioProvider");
  }
  return context;
};
