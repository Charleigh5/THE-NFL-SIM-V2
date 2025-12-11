import React, { useEffect, useState, useCallback } from "react";
import styles from "./TraitNotification.module.css";

export interface TraitNotificationProps {
  traitName: string;
  playerName: string;
  type?: "UNLOCK" | "UPGRADE" | "LOST";
  duration?: number;
  onDismiss?: () => void;
}

const TraitNotification: React.FC<TraitNotificationProps> = ({
  traitName,
  playerName,
  type = "UNLOCK",
  duration = 5000,
  onDismiss,
}) => {
  const [visible, setVisible] = useState(true);
  const [isExiting, setIsExiting] = useState(false);

  const handleDismiss = useCallback(() => {
    setIsExiting(true);
    setTimeout(() => {
      setVisible(false);
      if (onDismiss) onDismiss();
    }, 300); // Wait for exit animation
  }, [onDismiss]);

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        handleDismiss();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, handleDismiss]);

  if (!visible) return null;

  const getTitle = () => {
    switch (type) {
      case "UNLOCK":
        return "Trait Unlocked";
      case "UPGRADE":
        return "Trait Upgraded";
      case "LOST":
        return "Trait Lost";
      default:
        return "Trait Update";
    }
  };

  const getIcon = () => {
    switch (type) {
      case "UNLOCK":
        return "🌟";
      case "UPGRADE":
        return "⚡";
      case "LOST":
        return "📉";
      default:
        return "ℹ️";
    }
  };

  return (
    <div className={`${styles.notificationContainer} ${isExiting ? styles.exit : ""}`}>
      <div className={styles.iconWrapper}>{getIcon()}</div>
      <div className={styles.content}>
        <div className={styles.title}>{getTitle()}</div>
        <div className={styles.message}>
          <span className={styles.whiteHighlight}>{playerName}</span> has acquired the{" "}
          <span className={styles.traitName}>{traitName}</span> trait!
        </div>
      </div>
      <button className={styles.dismissButton} onClick={handleDismiss}>
        ✕
      </button>
    </div>
  );
};

export default TraitNotification;
