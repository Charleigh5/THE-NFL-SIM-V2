/**
 * Generic Normalized Entity State & Slice Interfaces
 * Standards: Production-grade strict typing (0 any types), O(1) dictionary lookups.
 */

export type EntityKey = string | number;

export interface EntityState<T, K extends EntityKey = string | number> {
  byId: Record<K, T>;
  allIds: K[];
  selectedId: K | null;
  filterIds: K[];
  isLoading: boolean;
  error: string | null;
}

export interface EntitySliceActions<T, K extends EntityKey = string | number> {
  setAll: (entities: T[], getId: (entity: T) => K) => void;
  upsertOne: (entity: T, getId: (entity: T) => K) => void;
  updateOne: (id: K, updates: Partial<T>) => void;
  removeOne: (id: K) => void;
  setSelectedId: (id: K | null) => void;
  setFilterIds: (ids: K[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

export type EntitySlice<T, K extends EntityKey = string | number> = EntityState<T, K> &
  EntitySliceActions<T, K>;
