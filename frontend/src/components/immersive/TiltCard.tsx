import { useMemo } from "react";
import { motion, useMotionValue, useReducedMotion, useSpring } from "framer-motion";
import clsx from "clsx";
import styles from "./TiltCard.module.css";

type TiltCardProps = {
  className?: string;
  children: React.ReactNode;
  intensity?: number; // degrees
  glow?: boolean;
  onClick?: React.MouseEventHandler<HTMLDivElement>;
  "data-testid"?: string;
};

export function TiltCard({
  className,
  children,
  intensity = 10,
  glow = true,
  onClick,
  "data-testid": testId,
}: TiltCardProps) {
  const isAutomated =
    typeof navigator !== "undefined" &&
    (navigator as unknown as { webdriver?: boolean }).webdriver;
  const reduceMotion = useReducedMotion() || isAutomated;

  const rotateX = useMotionValue(0);
  const rotateY = useMotionValue(0);
  const rx = useSpring(rotateX, { stiffness: 240, damping: 24, mass: 0.7 });
  const ry = useSpring(rotateY, { stiffness: 240, damping: 24, mass: 0.7 });

  const style = useMemo(
    () =>
      ({
        rotateX: reduceMotion ? 0 : rx,
        rotateY: reduceMotion ? 0 : ry,
        transformPerspective: 1000,
      }) as const,
    [reduceMotion, rx, ry]
  );

  return (
    <motion.div
      className={clsx(styles.root, className)}
      style={style}
      onPointerMove={(e) => {
        if (reduceMotion) return;
        const rect = (e.currentTarget as HTMLDivElement).getBoundingClientRect();
        const px = (e.clientX - rect.left) / rect.width;
        const py = (e.clientY - rect.top) / rect.height;
        const dx = px - 0.5;
        const dy = py - 0.5;

        rotateX.set((-dy * intensity) as number);
        rotateY.set((dx * intensity) as number);

        // CSS variables for spotlight
        e.currentTarget.style.setProperty("--mx", `${Math.round(px * 100)}%`);
        e.currentTarget.style.setProperty("--my", `${Math.round(py * 100)}%`);
      }}
      onPointerLeave={() => {
        rotateX.set(0);
        rotateY.set(0);
      }}
      onClick={onClick}
      data-testid={testId}
    >
      {glow && <div className={styles.edgeGlow} />}
      <div className={styles.content}>{children}</div>
    </motion.div>
  );
}
