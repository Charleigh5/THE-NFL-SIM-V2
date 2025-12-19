import { createContext } from "react";

export const STORAGE_KEY = "nfl-sim-audio-prefs";

export interface AudioPreferences {
  volume: number;
  isMuted: boolean;
}

export interface AudioContextType {
  isPlaying: boolean;
  volume: number;
  isMuted: boolean;
  play: () => void;
  pause: () => void;
  toggle: () => void;
  setVolume: (volume: number) => void;
  toggleMute: () => void;
}

export const AudioContext = createContext<AudioContextType | undefined>(undefined);
