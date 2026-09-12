import React, { useEffect, useRef } from "react";
import { useReducedMotion } from "framer-motion";
import clsx from "clsx";
import type { SpatialSceneManifest } from "./spatialSceneManifest";
import styles from "./SpatialSceneShell.module.css";

interface SpatialSceneShellProps {
  manifest: SpatialSceneManifest;
  className?: string;
  children: React.ReactNode;
}

/**
 * Shared shell for storyboard scenes.
 *
 * This proof slice deliberately stays DOM/CSS-first. It provides spatial depth,
 * atmosphere, and a stable interaction plane without adding another permanent
 * WebGL canvas on top of the app-wide Three.js/weather layers.
 */
export function SpatialSceneShell({ manifest, className, children }: SpatialSceneShellProps) {
  const rootRef = useRef<HTMLDivElement | null>(null);
  const frameRef = useRef<number | null>(null);
  const pendingRef = useRef({ x: 0, y: 0 });
  const shouldReduceMotion = useReducedMotion();

  const isAutomated =
    typeof navigator !== "undefined" && (navigator as unknown as { webdriver?: boolean }).webdriver;

  const motionDisabled = Boolean(shouldReduceMotion || isAutomated);

  useEffect(() => {
    return () => {
      if (frameRef.current !== null) {
        cancelAnimationFrame(frameRef.current);
      }
    };
  }, []);

  const flushPointer = () => {
    const root = rootRef.current;
    frameRef.current = null;
    if (!root) return;

    root.style.setProperty("--scene-x", `${pendingRef.current.x.toFixed(2)}px`);
    root.style.setProperty("--scene-y", `${pendingRef.current.y.toFixed(2)}px`);
  };

  const handlePointerMove = (event: React.PointerEvent<HTMLDivElement>) => {
    if (motionDisabled) return;

    const root = rootRef.current;
    if (!root) return;

    const rect = root.getBoundingClientRect();
    const nx = (event.clientX - rect.left) / Math.max(rect.width, 1) - 0.5;
    const ny = (event.clientY - rect.top) / Math.max(rect.height, 1) - 0.5;
    const intensity = manifest.motion.pointerParallaxPx;

    pendingRef.current = {
      x: nx * intensity * 2,
      y: ny * intensity * 2,
    };

    if (frameRef.current === null) {
      frameRef.current = requestAnimationFrame(flushPointer);
    }
  };

  const resetPointer = () => {
    pendingRef.current = { x: 0, y: 0 };
    const root = rootRef.current;
    if (!root) return;
    root.style.setProperty("--scene-x", "0px");
    root.style.setProperty("--scene-y", "0px");
  };

  return (
    <div
      ref={rootRef}
      className={clsx(styles.scene, className)}
      data-testid="depth-chart-scene"
      data-scene-id={manifest.id}
      data-render-mode={manifest.renderMode}
      data-asset-status={manifest.assetStatus}
      data-motion={motionDisabled ? "reduced" : "full"}
      onPointerMove={handlePointerMove}
      onPointerLeave={resetPointer}
    >
      <div className={styles.architecture} aria-hidden="true">
        <div className={styles.ceilingGlow} />
        <div className={styles.leftPillar} />
        <div className={styles.rightPillar} />
        <div className={styles.boardWall} />
        <div className={styles.fieldGrid} />
        <div className={styles.vignette} />
      </div>

      <div className={styles.content}>{children}</div>
    </div>
  );
}

export default SpatialSceneShell;
