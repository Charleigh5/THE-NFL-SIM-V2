/**
 * Debug Store
 *
 * Sliced store for engine/debug data.
 * Provides typed access to kernel states for debugging.
 */

import { create } from "zustand";
import type {
  TypedEngineData,
  GenesisState,
  EmpireState,
  HiveState,
  SocietyState,
  RPGState,
} from "../types/engine-state";
import {
  DEFAULT_GENESIS_STATE,
  DEFAULT_EMPIRE_STATE,
  DEFAULT_HIVE_STATE,
  DEFAULT_SOCIETY_STATE,
  DEFAULT_RPG_STATE,
} from "../types/engine-state";

interface DebugStore {
  // State
  engineData: TypedEngineData;
  isDebugMode: boolean;
  lastUpdateTimestamp: number;

  // Actions
  updateGenesisState: (state: Partial<GenesisState>) => void;
  updateEmpireState: (state: Partial<EmpireState>) => void;
  updateHiveState: (state: Partial<HiveState>) => void;
  updateSocietyState: (state: Partial<SocietyState>) => void;
  updateRPGState: (state: Partial<RPGState>) => void;
  updateEngineData: (engine: keyof TypedEngineData, data: unknown) => void;
  setDebugMode: (enabled: boolean) => void;
  resetEngineData: () => void;
}

export const useDebugStore = create<DebugStore>((set) => ({
  engineData: {
    genesis: DEFAULT_GENESIS_STATE,
    empire: DEFAULT_EMPIRE_STATE,
    hive: DEFAULT_HIVE_STATE,
    society: DEFAULT_SOCIETY_STATE,
    rpg: DEFAULT_RPG_STATE,
  },
  isDebugMode: false,
  lastUpdateTimestamp: Date.now(),

  updateGenesisState: (state) =>
    set((prev) => ({
      engineData: {
        ...prev.engineData,
        genesis: { ...prev.engineData.genesis, ...state },
      },
      lastUpdateTimestamp: Date.now(),
    })),

  updateEmpireState: (state) =>
    set((prev) => ({
      engineData: {
        ...prev.engineData,
        empire: { ...prev.engineData.empire, ...state },
      },
      lastUpdateTimestamp: Date.now(),
    })),

  updateHiveState: (state) =>
    set((prev) => ({
      engineData: {
        ...prev.engineData,
        hive: { ...prev.engineData.hive, ...state },
      },
      lastUpdateTimestamp: Date.now(),
    })),

  updateSocietyState: (state) =>
    set((prev) => ({
      engineData: {
        ...prev.engineData,
        society: { ...prev.engineData.society, ...state },
      },
      lastUpdateTimestamp: Date.now(),
    })),

  updateRPGState: (state) =>
    set((prev) => ({
      engineData: {
        ...prev.engineData,
        rpg: { ...prev.engineData.rpg, ...state },
      },
      lastUpdateTimestamp: Date.now(),
    })),

  // Generic update for backward compatibility
  updateEngineData: (engine, data) =>
    set((prev) => ({
      engineData: {
        ...prev.engineData,
        [engine]: { ...prev.engineData[engine], ...(data as object) },
      },
      lastUpdateTimestamp: Date.now(),
    })),

  setDebugMode: (enabled) => set({ isDebugMode: enabled }),

  resetEngineData: () =>
    set({
      engineData: {
        genesis: DEFAULT_GENESIS_STATE,
        empire: DEFAULT_EMPIRE_STATE,
        hive: DEFAULT_HIVE_STATE,
        society: DEFAULT_SOCIETY_STATE,
        rpg: DEFAULT_RPG_STATE,
      },
      lastUpdateTimestamp: Date.now(),
    }),
}));
