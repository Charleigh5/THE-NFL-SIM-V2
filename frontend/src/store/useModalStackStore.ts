import { create } from "zustand";

export interface ModalInstance {
  id: string;
  depth: number;
  triggerElement: HTMLElement | null;
  onDismiss: () => void;
}

export interface ModalStackState {
  stack: ModalInstance[];
  pushModal: (id: string, onDismiss: () => void, triggerElement?: HTMLElement | null) => void;
  popModal: (id?: string) => void;
  isTopModal: (id: string) => boolean;
  getTopModal: () => ModalInstance | null;
  clearStack: () => void;
}

export const useModalStackStore = create<ModalStackState>((set, get) => ({
  stack: [],
  pushModal: (id, onDismiss, triggerElement = null) => {
    set((state) => {
      // Deduplicate: filter out existing with same id if already present and re-index
      const filtered = state.stack
        .filter((m) => m.id !== id)
        .map((m, idx) => ({ ...m, depth: idx }));
      const newInstance: ModalInstance = {
        id,
        depth: filtered.length,
        triggerElement,
        onDismiss,
      };
      return { stack: [...filtered, newInstance] };
    });
  },
  popModal: (id) => {
    const { stack } = get();
    if (stack.length === 0) return;

    if (id) {
      const target = stack.find((m) => m.id === id);
      if (target) {
        const remaining = stack.filter((m) => m.id !== id).map((m, idx) => ({ ...m, depth: idx }));
        set({ stack: remaining });
        target.onDismiss();
      }
    } else {
      const top = stack[stack.length - 1];
      const remaining = stack.slice(0, -1).map((m, idx) => ({ ...m, depth: idx }));
      set({ stack: remaining });
      top.onDismiss();
    }
  },
  isTopModal: (id) => {
    const { stack } = get();
    return stack.length > 0 && stack[stack.length - 1].id === id;
  },
  getTopModal: () => {
    const { stack } = get();
    return stack.length > 0 ? stack[stack.length - 1] : null;
  },
  clearStack: () => {
    set({ stack: [] });
  },
}));
