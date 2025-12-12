import React from "react";
import clsx from "clsx";
import { motion } from "framer-motion";
import styles from "./BroadcastPanel.module.css";

type BroadcastPanelProps = {
  title: string;
  isLive?: boolean;
  className?: string;
  children: React.ReactNode;
  "data-testid"?: string;
};

export function BroadcastPanel({
  title,
  isLive = false,
  className,
  children,
  "data-testid": testId,
}: BroadcastPanelProps) {
  return (
    <motion.div
      className={clsx(styles.panel, className)}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      data-testid={testId}
    >
      <div className={styles.header}>
        <div className={styles.title}>
          {isLive && <span className={styles.liveIndicator} aria-hidden="true" />}
          {title}
        </div>
        {/* Future slot for window controls or action icons */}
      </div>
      <div className={styles.content}>{children}</div>
    </motion.div>
  );
}
