import { motion, useReducedMotion } from "framer-motion";
import styles from "./RibbonTicker.module.css";

type RibbonTickerProps = {
  items: Array<string>;
  speedSec?: number;
  "data-testid"?: string;
};

/**
 * LED-ribbon style ticker.
 * Renders duplicated content to create a seamless marquee.
 */
export function RibbonTicker({ items, speedSec = 18, "data-testid": testId }: RibbonTickerProps) {
  const reduceMotion = useReducedMotion();
  const isAutomated =
    typeof navigator !== "undefined" && (navigator as unknown as { webdriver?: boolean }).webdriver;
  const shouldAnimate = !reduceMotion && !isAutomated;
  const content = items.length
    ? items
    : ["League Update", "Night Game Atmosphere", "Franchise Mode"]; // safe fallback

  return (
    <div className={styles.wrap} data-testid={testId}>
      <motion.div
        className={styles.row}
        aria-hidden={shouldAnimate ? true : undefined}
        animate={
          shouldAnimate
            ? {
                x: [0, -50 * content.length],
              }
            : undefined
        }
        transition={
          shouldAnimate
            ? {
                duration: speedSec,
                ease: "linear",
                repeat: Infinity,
              }
            : undefined
        }
      >
        {content.concat(content).map((t, i) => (
          <span className={styles.pill} key={`${t}-${i}`}>
            <span className={styles.dot} />
            {t}
          </span>
        ))}
      </motion.div>
    </div>
  );
}
