import { useRef } from "react";
import clsx from "clsx";
import styles from "./ParallaxScene.module.css";

type ParallaxSceneProps = {
  className?: string;
  children: React.ReactNode;
  rain?: boolean;
};

/**
 * Lightweight page-scene wrapper.
 * - pointer-based parallax (no scroll listeners)
 * - layered atmospheric backgrounds (grain, rain, spotlights)
 */
export function ParallaxScene({ className, children, rain = false }: ParallaxSceneProps) {
  const ref = useRef<HTMLDivElement | null>(null);

  return (
    <div
      ref={ref}
      className={clsx(styles.scene, className)}
      onPointerMove={(e) => {
        const el = ref.current;
        if (!el) return;
        const rect = el.getBoundingClientRect();
        const px = (e.clientX - rect.left) / rect.width;
        const py = (e.clientY - rect.top) / rect.height;
        const dx = (px - 0.5) * 18;
        const dy = (py - 0.5) * 18;
        el.style.setProperty("--px", `${dx.toFixed(1)}px`);
        el.style.setProperty("--py", `${dy.toFixed(1)}px`);
      }}
    >
      <div className={styles.bg} />
      <div className={styles.grain} />
      {rain && <div className={styles.rain} />}
      <div className={styles.content}>{children}</div>
    </div>
  );
}
