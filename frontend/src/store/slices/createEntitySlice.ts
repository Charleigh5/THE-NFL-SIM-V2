import type { EntityKey, EntityState, EntitySliceActions } from "../../types/entityState";

/**
 * Creates a clean, empty initial entity state
 */
export function createInitialEntityState<T, K extends EntityKey = string | number>(): EntityState<
  T,
  K
> {
  return {
    byId: {} as Record<K, T>,
    allIds: [],
    selectedId: null,
    filterIds: [],
    isLoading: false,
    error: null,
  };
}

/**
 * Creates standardized O(1) dictionary mutations for normalized entity slices
 */
export function createEntitySliceActions<T, K extends EntityKey = string | number>(
  set: (updater: (state: EntityState<T, K>) => Partial<EntityState<T, K>>) => void
): EntitySliceActions<T, K> {
  return {
    setAll: (entities: T[], getId: (entity: T) => K) => {
      const byId = {} as Record<K, T>;
      const allIds: K[] = [];
      const seen = new Set<K>();

      for (let i = 0; i < entities.length; i++) {
        const entity = entities[i];
        const id = getId(entity);
        if (!seen.has(id)) {
          seen.add(id);
          allIds.push(id);
        }
        byId[id] = entity;
      }

      set((state) => ({
        ...state,
        byId,
        allIds,
        filterIds: allIds,
        isLoading: false,
        error: null,
      }));
    },

    upsertOne: (entity: T, getId: (entity: T) => K) => {
      const id = getId(entity);
      set((state) => {
        const exists = id in state.byId;
        return {
          ...state,
          byId: { ...state.byId, [id]: entity },
          allIds: exists ? state.allIds : [...state.allIds, id],
          filterIds: exists
            ? state.filterIds
            : state.filterIds.includes(id)
              ? state.filterIds
              : [...state.filterIds, id],
        };
      });
    },

    updateOne: (id: K, updates: Partial<T>) => {
      set((state) => {
        const existing = state.byId[id];
        if (!existing) return state;
        return {
          ...state,
          byId: {
            ...state.byId,
            [id]: { ...existing, ...updates },
          },
        };
      });
    },

    removeOne: (id: K) => {
      set((state) => {
        if (!(id in state.byId)) return state;
        const newById = { ...state.byId };
        delete newById[id];
        return {
          ...state,
          byId: newById,
          allIds: state.allIds.filter((item) => item !== id),
          filterIds: state.filterIds.filter((item) => item !== id),
          selectedId: state.selectedId === id ? null : state.selectedId,
        };
      });
    },

    setSelectedId: (id: K | null) => {
      set((state) => ({
        ...state,
        selectedId: id,
      }));
    },

    setFilterIds: (ids: K[]) => {
      set((state) => ({
        ...state,
        filterIds: ids,
      }));
    },

    setLoading: (loading: boolean) => {
      set((state) => ({
        ...state,
        isLoading: loading,
      }));
    },

    setError: (error: string | null) => {
      set((state) => ({
        ...state,
        error,
        isLoading: false,
      }));
    },

    reset: () => {
      set(() => createInitialEntityState<T, K>());
    },
  };
}
