import React from "react";
import type { Trait } from "../../types/trait";
import styles from "./TraitTooltip.module.css";

interface TraitTooltipProps {
  trait: Trait;
}

const TraitTooltip: React.FC<TraitTooltipProps> = ({ trait }) => {
  const tier = trait.tier || "COMMON";

  return (
    <div className={styles.tooltip}>
      <div className={styles.header}>
        <span className={styles.title}>{trait.name}</span>
        <span className={`${styles.tier} ${styles[tier]}`}>{tier}</span>
      </div>

      <div className={styles.description}>{trait.description || "No description available."}</div>

      {(trait.effect_value !== 0 || trait.effect_type) && (
        <div className={styles.effects}>
          <div className={styles.effectRow}>
            <span className={styles.label}>Type:</span>
            <span className={styles.value}>{trait.effect_type}</span>
          </div>
          {trait.effect_value !== 0 && (
            <div className={styles.effectRow}>
              <span className={styles.label}>Effect:</span>
              <span className={styles.value}>
                {trait.effect_value > 0 ? "+" : ""}
                {trait.effect_value}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TraitTooltip;
