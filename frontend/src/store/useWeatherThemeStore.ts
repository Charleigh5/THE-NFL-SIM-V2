import { create } from "zustand";

export type WeatherCondition =
  | "CLEAR_NIGHT"
  | "VICE_HEATWAVE"
  | "LAMBEAU_BLIZZARD"
  | "ARROWHEAD_DOWNPOUR"
  | "FOXBOROUGH_AUTUMN";

export interface WeatherPreset {
  name: string;
  location: string;
  seasonLabel: string;
  temperature: number; // °F
  windSpeed: number; // mph
  windAngleRad: number; // angle in radians
  precipitationDensity: number; // 0 to 1
  particleType: "none" | "rain" | "snow" | "leaves" | "heat_shimmer";
  ambientLightingHex: string;
  stadiumLightHex: string;
  skyColorTop: string;
  skyColorBottom: string;
  turfTint: string;
  description: string;
}

export const WEATHER_PRESETS: Record<WeatherCondition, WeatherPreset> = {
  CLEAR_NIGHT: {
    name: "Clear Stadium Night",
    location: "SoFi Stadium, Los Angeles",
    seasonLabel: "Regular Season • Prime Time",
    temperature: 68,
    windSpeed: 4,
    windAngleRad: 0.1,
    precipitationDensity: 0.0,
    particleType: "none",
    ambientLightingHex: "#101420",
    stadiumLightHex: "#00f0ff",
    skyColorTop: "#050810",
    skyColorBottom: "#0b1122",
    turfTint: "#1f6e43",
    description: "Crisp stadium floodlights cutting through cool California night air.",
  },
  VICE_HEATWAVE: {
    name: "Vice Dusk Heatwave",
    location: "Hard Rock Stadium, Miami",
    seasonLabel: "Week 02 • Searing Humidity",
    temperature: 92,
    windSpeed: 12,
    windAngleRad: 0.35,
    precipitationDensity: 0.25,
    particleType: "heat_shimmer",
    ambientLightingHex: "#220818",
    stadiumLightHex: "#ff1493",
    skyColorTop: "#2a0426",
    skyColorBottom: "#7a1a54",
    turfTint: "#228045",
    description: "Sultry neon dusk, humid Biscayne Bay haze, and shimmering heat waves.",
  },
  LAMBEAU_BLIZZARD: {
    name: "Frozen Tundra Blizzard",
    location: "Lambeau Field, Green Bay",
    seasonLabel: "Divisional Playoff • Sub-Zero",
    temperature: -4,
    windSpeed: 24,
    windAngleRad: 0.75,
    precipitationDensity: 0.95,
    particleType: "snow",
    ambientLightingHex: "#121b28",
    stadiumLightHex: "#b8e2f2",
    skyColorTop: "#0f1624",
    skyColorBottom: "#1e2c40",
    turfTint: "#e2ecf0",
    description: "Driving snow squalls accumulating on players and sideline equipment.",
  },
  ARROWHEAD_DOWNPOUR: {
    name: "Torrential Thunderstorm",
    location: "Arrowhead Stadium, Kansas City",
    seasonLabel: "AFC Championship • Torrential Rain",
    temperature: 46,
    windSpeed: 18,
    windAngleRad: 0.55,
    precipitationDensity: 0.9,
    particleType: "rain",
    ambientLightingHex: "#0c151e",
    stadiumLightHex: "#00e5ff",
    skyColorTop: "#080e14",
    skyColorBottom: "#142230",
    turfTint: "#14482b",
    description: "Heavy rain sheeting across the turf with dramatic lightning illumination.",
  },
  FOXBOROUGH_AUTUMN: {
    name: "New England Autumn Chill",
    location: "Gillette Stadium, Foxborough",
    seasonLabel: "November Classic • Overcast",
    temperature: 44,
    windSpeed: 15,
    windAngleRad: 0.45,
    precipitationDensity: 0.35,
    particleType: "leaves",
    ambientLightingHex: "#17181c",
    stadiumLightHex: "#ffb800",
    skyColorTop: "#121418",
    skyColorBottom: "#282622",
    turfTint: "#3b6b3e",
    description: "Cold gusty autumn winds with swirling leaves and crisp stadium lighting.",
  },
};

interface WeatherThemeState {
  condition: WeatherCondition;
  preset: WeatherPreset;
  lightningActive: boolean;
  lightningIntensity: number;
  show3DBackdrop: boolean;
  snowAccumulationActive: boolean;
  audioEnabled: boolean;
  rainVolume: number;
  setCondition: (condition: WeatherCondition) => void;
  triggerLightning: (intensity?: number) => void;
  toggle3DBackdrop: () => void;
  toggleSnowAccumulation: () => void;
  toggleAudio: () => void;
  setRainVolume: (volume: number) => void;
}

export const useWeatherThemeStore = create<WeatherThemeState>((set, get) => ({
  condition: "ARROWHEAD_DOWNPOUR",
  preset: WEATHER_PRESETS.ARROWHEAD_DOWNPOUR,
  lightningActive: false,
  lightningIntensity: 0,
  show3DBackdrop: true,
  snowAccumulationActive: true,
  audioEnabled: false,
  rainVolume: 0.4,

  setCondition: (condition: WeatherCondition) => {
    set({
      condition,
      preset: WEATHER_PRESETS[condition],
    });
  },

  triggerLightning: (intensity = 1.0) => {
    if (get().lightningActive) return;
    set({ lightningActive: true, lightningIntensity: intensity });

    // Multi-stage lightning flicker simulation
    setTimeout(() => set({ lightningIntensity: 0.3 }), 40);
    setTimeout(() => set({ lightningIntensity: intensity * 1.2 }), 90);
    setTimeout(() => set({ lightningIntensity: 0.5 }), 160);
    setTimeout(() => {
      set({ lightningActive: false, lightningIntensity: 0 });
    }, 380);
  },

  toggle3DBackdrop: () => {
    set((state) => ({ show3DBackdrop: !state.show3DBackdrop }));
  },

  toggleSnowAccumulation: () => {
    set((state) => ({ snowAccumulationActive: !state.snowAccumulationActive }));
  },

  toggleAudio: () => {
    set((state) => ({ audioEnabled: !state.audioEnabled }));
  },

  setRainVolume: (volume: number) => {
    set({ rainVolume: Math.max(0, Math.min(1, volume)) });
  },
}));
