import React from "react";
import type { Trait } from "../../types/trait";
import styles from "./TraitBadge.module.css";
import TraitTooltip from "./TraitTooltip";

interface TraitBadgeProps {
  trait: Trait;
  showTooltip?: boolean;
}

const TraitBadge: React.FC<TraitBadgeProps> = ({ trait, showTooltip = true }) => {
  const tierClass = styles[trait.tier?.toLowerCase() || "common"];

  // Icons based on effect type or name keywords could go here
  const getIcon = () => {
    switch (trait.effect_type) {
      case "BOOST":
        return "⚡";
      case "SITUATIONAL":
        return "🎯";
      case "XFACTOR":
        return "🌟";
      case "PASSIVE":
        return "🛡️";
      default:
        return "🔹";
    }
  };

  return (
    <div className={`${styles.badge} ${tierClass}`}>
      <span className={styles.icon}>{getIcon()}</span>
      <span>{trait.name}</span>

      {showTooltip && (
        <div className={styles.tooltipContainer}>
          <TraitTooltip trait={trait} />
        </div>
      )}
    </div>
  );
};

export default TraitBadge;
