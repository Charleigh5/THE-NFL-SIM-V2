import { create } from "zustand";
import type { BatchTrainingResponse } from "../services/trainingApi";

export interface NotificationData {
  id: string;
  type: "TRAINING_SUMMARY" | "GENERIC";
  data: BatchTrainingResponse;
  duration?: number;
}

interface NotificationStore {
  notifications: NotificationData[];
  addNotification: (notification: Omit<NotificationData, "id">) => void;
  removeNotification: (id: string) => void;
}

export const useNotificationStore = create<NotificationStore>((set) => ({
  notifications: [],
  addNotification: (notification) =>
    set((state) => ({
      notifications: [
        ...state.notifications,
        { ...notification, id: Math.random().toString(36).substring(7) },
      ],
    })),
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
}));
