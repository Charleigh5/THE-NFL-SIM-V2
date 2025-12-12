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
  const content = items.length
    ? items
    : ["League Update", "Night Game Atmosphere", "Franchise Mode"]; // safe fallback

  return (
    <div className={styles.wrap} data-testid={testId}>
      <motion.div
        className={styles.row}
        aria-hidden={reduceMotion ? undefined : true}
        animate={
          reduceMotion
            ? undefined
            : {
                x: [0, -50 * content.length],
              }
        }
        transition={
          reduceMotion
            ? undefined
            : {
                duration: speedSec,
                ease: "linear",
                repeat: Infinity,
              }
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
