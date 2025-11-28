import React from "react";

export interface DraggableHandlers {
  onPointerDown: (e: React.PointerEvent) => void;
  onPointerMove: (e: React.PointerEvent) => void;
  onPointerUp: (e: React.PointerEvent) => void;
}

export interface PressHoldHandlers {
  onPointerDown: () => void;
  onPointerUp: () => void;
  onPointerLeave: () => void;
}

export const createDraggableHandlers = (): DraggableHandlers => {
  return {
    onPointerDown: (e: React.PointerEvent) => e.stopPropagation(),
    onPointerMove: (e: React.PointerEvent) => e.stopPropagation(),
    onPointerUp: (e: React.PointerEvent) => e.stopPropagation(),
  };
};

export const createPressHoldHandlers = (
  onPressEnd?: () => void,
  duration: number = 500
): PressHoldHandlers => {
  let pressTimer: number | null = null;

  const handlePressStart = () => {
    pressTimer = setTimeout(() => {
      onPressEnd?.();
    }, duration);
  };

  const handlePressEnd = () => {
    if (pressTimer) {
      clearTimeout(pressTimer);
      pressTimer = null;
    }
    onPressEnd?.();
  };

  return {
    onPointerDown: handlePressStart,
    onPointerUp: handlePressEnd,
    onPointerLeave: handlePressEnd,
  };
};
