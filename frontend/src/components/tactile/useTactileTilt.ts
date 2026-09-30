import { useRef, useCallback, useState, useEffect } from "react";
import { useMotionValue, useSpring, useReducedMotion } from "framer-motion";
import { soundEffects } from "../../services/soundEffects";
import type { TactileTiltOptions, TactileTiltResult } from "./types";

/**
 * 3D Pointer Perspective Tilt Hook
 * Computes normalized cursor coordinates to drive 3D rotation, elevation,
 * dynamic specular sheen, and synthesized Web Audio detent haptics.
 *
 * Automatically bypasses 3D tilt in reduced-motion environments or headless automated test runs.
 */
export function useTactileTilt({
  maxTilt = 10,
  enableHaptics = true,
  tiltThreshold = 4.5,
  disabled = false,
}: TactileTiltOptions = {}): TactileTiltResult {
  const isAutomated =
    typeof navigator !== "undefined" &&
    Boolean((navigator as Navigator & { webdriver?: boolean }).webdriver);
  const prefersReduced = useReducedMotion();
  const shouldBypass = Boolean(prefersReduced || isAutomated || disabled);

  const ref = useRef<HTMLDivElement | null>(null);
  const [rawIsTilting, setRawIsTilting] = useState<boolean>(false);
  const isTilting = shouldBypass ? false : rawIsTilting;

  const rawRotateX = useMotionValue(0);
  const rawRotateY = useMotionValue(0);
  const rawTranslateZ = useMotionValue(0);

  // Physics-based spring dampening to eliminate jitter and bounce
  const rotateX = useSpring(rawRotateX, { stiffness: 280, damping: 24, mass: 0.6 });
  const rotateY = useSpring(rawRotateY, { stiffness: 280, damping: 24, mass: 0.6 });
  const translateZ = useSpring(rawTranslateZ, { stiffness: 320, damping: 26, mass: 0.5 });

  const hasFiredThreshold = useRef<boolean>(false);
  const lastDetentTime = useRef<number>(0);

  // Reset values when disabled or motion is reduced
  useEffect(() => {
    if (shouldBypass) {
      rawRotateX.set(0);
      rawRotateY.set(0);
      rawTranslateZ.set(0);
    }
  }, [shouldBypass, rawRotateX, rawRotateY, rawTranslateZ]);

  const handlePointerMove = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      if (shouldBypass || !ref.current) return;
      const rect = ref.current.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 0) return;

      const rawPx = (e.clientX - rect.left) / rect.width;
      const rawPy = (e.clientY - rect.top) / rect.height;

      const px = Math.max(0, Math.min(1, rawPx));
      const py = Math.max(0, Math.min(1, rawPy));

      const nx = (px - 0.5) * 2;
      const ny = (py - 0.5) * 2;

      const targetRotX = -ny * maxTilt;
      const targetRotY = nx * maxTilt;

      rawRotateX.set(targetRotX);
      rawRotateY.set(targetRotY);

      // Specular sheen coordinate reflection
      ref.current.style.setProperty("--mx", `${(px * 100).toFixed(1)}%`);
      ref.current.style.setProperty("--my", `${(py * 100).toFixed(1)}%`);

      // Angular threshold detent micro-chirp haptic detection with hysteresis
      if (enableHaptics) {
        const magnitude = Math.sqrt(targetRotX * targetRotX + targetRotY * targetRotY);
        const now = performance.now();
        if (
          magnitude > tiltThreshold &&
          !hasFiredThreshold.current &&
          now - lastDetentTime.current > 70
        ) {
          hasFiredThreshold.current = true;
          lastDetentTime.current = now;
          soundEffects.playTiltDetent();
        } else if (magnitude < Math.max(0, tiltThreshold - 1.5)) {
          hasFiredThreshold.current = false;
        }
      }
    },
    [maxTilt, enableHaptics, tiltThreshold, shouldBypass, rawRotateX, rawRotateY]
  );

  const handlePointerEnter = useCallback(() => {
    if (shouldBypass) return;
    setRawIsTilting(true);
    rawTranslateZ.set(14);
  }, [shouldBypass, rawTranslateZ]);

  const handlePointerLeave = useCallback(() => {
    rawRotateX.set(0);
    rawRotateY.set(0);
    rawTranslateZ.set(0);
    hasFiredThreshold.current = false;
    setRawIsTilting(false);
    if (ref.current) {
      ref.current.style.setProperty("--mx", "50%");
      ref.current.style.setProperty("--my", "50%");
    }
  }, [rawRotateX, rawRotateY, rawTranslateZ]);

  const handlePointerDown = useCallback(() => {
    if (shouldBypass) return;
    rawTranslateZ.set(2);
    if (enableHaptics) {
      soundEffects.playCardPress();
    }
  }, [shouldBypass, rawTranslateZ, enableHaptics]);

  const handlePointerUp = useCallback(() => {
    if (shouldBypass) return;
    rawTranslateZ.set(14);
    if (enableHaptics) {
      soundEffects.playCardRelease();
    }
  }, [shouldBypass, rawTranslateZ, enableHaptics]);

  return {
    ref,
    style: {
      rotateX: shouldBypass ? 0 : rotateX,
      rotateY: shouldBypass ? 0 : rotateY,
      translateZ: shouldBypass ? 0 : translateZ,
      transformPerspective: 1000,
      transformStyle: "preserve-3d",
    },
    handlers: {
      onPointerMove: handlePointerMove,
      onPointerEnter: handlePointerEnter,
      onPointerLeave: handlePointerLeave,
      onPointerDown: handlePointerDown,
      onPointerUp: handlePointerUp,
    },
    isTilting,
  };
}
