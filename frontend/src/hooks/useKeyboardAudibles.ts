/**
 * In-Game Tactile Keyboard Audibles Hook
 * =======================================
 * Deterministic keyboard event controller providing zero-latency on-field controls:
 * - [Space]: Snap Ball / Confirm 4th-Down Recommended Decision (with scroll suppression)
 * - [1] - [4]: Select Concept Card by Index (0-3)
 * - [A]: Quick-cycle audible category (Run <-> Pass)
 * - [T]: Call team timeout (with sound and remaining timeout check)
 * - [Esc]: Close active overlays / pause
 *
 * Strict Focus Protection: Bypasses all keystrokes when typing inside inputs, textareas, or contenteditables.
 */

import { useEffect, useCallback } from "react";
import { soundEffects } from "../services/soundEffects";

export interface KeyboardAudiblesOptions {
  enabled?: boolean;
  onSnapOrConfirm?: () => void;
  onSelectConceptIndex?: (index: number) => void;
  onToggleAudible?: () => void;
  onCallTimeout?: () => void;
  onDismissOrPause?: () => void;
}

export function useKeyboardAudibles({
  enabled = true,
  onSnapOrConfirm,
  onSelectConceptIndex,
  onToggleAudible,
  onCallTimeout,
  onDismissOrPause,
}: KeyboardAudiblesOptions): void {
  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (!enabled) return;

      // 1. Focus Protection Gate: Ignore hotkeys if user is focused on a text input
      const activeElement = document.activeElement;
      if (
        activeElement &&
        (activeElement.tagName === "INPUT" ||
          activeElement.tagName === "TEXTAREA" ||
          (activeElement as HTMLElement).isContentEditable)
      ) {
        return;
      }

      const key = event.key;
      const code = event.code;

      // 2. Spacebar: Snap or Confirm Recommended Decision
      if (code === "Space" || key === " ") {
        event.preventDefault();
        soundEffects.playCadence("hut");
        onSnapOrConfirm?.();
        return;
      }

      // 3. Digits 1-4: Select Concept Cards
      if (code === "Digit1" || key === "1") {
        event.preventDefault();
        soundEffects.playCadence("set");
        onSelectConceptIndex?.(0);
        return;
      }
      if (code === "Digit2" || key === "2") {
        event.preventDefault();
        soundEffects.playCadence("set");
        onSelectConceptIndex?.(1);
        return;
      }
      if (code === "Digit3" || key === "3") {
        event.preventDefault();
        soundEffects.playCadence("set");
        onSelectConceptIndex?.(2);
        return;
      }
      if (code === "Digit4" || key === "4") {
        event.preventDefault();
        soundEffects.playCadence("set");
        onSelectConceptIndex?.(3);
        return;
      }

      // 4. 'A' or 'a': Quick Audible Toggle
      if (code === "KeyA" || key === "a" || key === "A") {
        event.preventDefault();
        soundEffects.playCadence("audible");
        onToggleAudible?.();
        return;
      }

      // 5. 'T' or 't': Call Timeout
      if (code === "KeyT" || key === "t" || key === "T") {
        event.preventDefault();
        soundEffects.playSpatialWhistle();
        onCallTimeout?.();
        return;
      }

      // 6. Escape: Close Overlays / Pause
      if (code === "Escape" || key === "Escape") {
        event.preventDefault();
        onDismissOrPause?.();
        return;
      }
    },
    [
      enabled,
      onSnapOrConfirm,
      onSelectConceptIndex,
      onToggleAudible,
      onCallTimeout,
      onDismissOrPause,
    ]
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [handleKeyDown]);
}
