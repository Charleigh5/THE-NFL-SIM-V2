import React, { useState } from "react";
import type { Trait } from "../../types/trait";
import TraitBadge from "../common/TraitBadge";
import styles from "./CoachingUnlockPanel.module.css";

interface CoachingUnlockPanelProps {
  playerId: number;
  availableTraits: Trait[];
  onUnlockComplete: () => void;
}

const CoachingUnlockPanel: React.FC<CoachingUnlockPanelProps> = ({
  playerId,
  availableTraits,
  onUnlockComplete,
}) => {
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUnlock = async (trait: Trait) => {
    setLoading(trait.name);
    setError(null);
    try {
      const response = await fetch(`/api/traits/players/${playerId}/unlock`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ trait_name: trait.name }),
      });

      if (!response.ok) {
        throw new Error("Failed to unlock trait");
      }

      onUnlockComplete();
    } catch (err) {
      setError("Unlock failed. Please try again.");
      console.error(err);
    } finally {
      setLoading(null);
    }
  };

  if (availableTraits.length === 0) {
    return <div className={styles.empty}>No coaching traits available to unlock.</div>;
  }

  return (
    <div className={styles.panel}>
      <h3 className={styles.header}>Coaching Unlocks</h3>
      {error && <div className={styles.error}>{error}</div>}
      <div className={styles.grid}>
        {availableTraits.map((trait) => (
          <div key={trait.id} className={styles.card}>
            <div className={styles.traitInfo}>
              <TraitBadge trait={trait} showTooltip={true} />
              <p className={styles.description}>{trait.description}</p>
            </div>
            <button
              className={styles.unlockButton}
              onClick={() => handleUnlock(trait)}
              disabled={loading === trait.name}
            >
              {loading === trait.name ? "Unlocking..." : "Unlock"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CoachingUnlockPanel;
