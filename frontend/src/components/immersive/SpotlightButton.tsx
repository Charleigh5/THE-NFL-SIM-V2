import { motion, useReducedMotion } from "framer-motion";
import type { HTMLMotionProps } from "framer-motion";
import clsx from "clsx";
import styles from "./SpotlightButton.module.css";
import { t } from "../../styles/motion";

export type SpotlightButtonProps = Omit<HTMLMotionProps<"button">, "ref"> & {
  variant?: "default" | "primary";
};

export function SpotlightButton({
  className,
  variant = "default",
  onPointerMove,
  ...props
}: SpotlightButtonProps) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.button
      {...props}
      className={clsx(styles.btn, variant === "primary" && styles.primary, className)}
      whileTap={reduceMotion ? undefined : { scale: 0.985 }}
      transition={t.fast}
      onPointerMove={(e) => {
        const rect = (e.currentTarget as HTMLButtonElement).getBoundingClientRect();
        const px = (e.clientX - rect.left) / rect.width;
        const py = (e.clientY - rect.top) / rect.height;
        e.currentTarget.style.setProperty("--mx", `${Math.round(px * 100)}%`);
        e.currentTarget.style.setProperty("--my", `${Math.round(py * 100)}%`);
        onPointerMove?.(e);
      }}
    />
  );
}
