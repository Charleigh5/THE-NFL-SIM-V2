import { useEffect, useState, useCallback } from "react";
import { traitService } from "../../services/traits";
import type { Trait, TraitAssignment } from "../../types/trait";
import { TraitSource } from "../../types/trait";
import styles from "./TraitManager.module.css";

interface TraitManagerProps {
  playerId: number;
  playerName?: string;
}

export const TraitManager: React.FC<TraitManagerProps> = ({ playerId, playerName }) => {
  const [availableTraits, setAvailableTraits] = useState<Trait[]>([]);
  const [assignedTraits, setAssignedTraits] = useState<Trait[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedTraitId, setSelectedTraitId] = useState<number | string>("");

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [all, assigned] = await Promise.all([
        traitService.getAllTraits(),
        traitService.getPlayerTraits(playerId),
      ]);
      setAvailableTraits(all);
      setAssignedTraits(assigned);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    } finally {
      setLoading(false);
    }
  }, [playerId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleAssign = async () => {
    if (!selectedTraitId) return;

    try {
      const assignment: TraitAssignment = {
        trait_id: Number(selectedTraitId),
        source: TraitSource.DEVELOPMENT, // Default for dev tool
      };
      await traitService.assignTrait(playerId, assignment);
      await loadData(); // Refresh
      setSelectedTraitId("");
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to assign trait");
      }
    }
  };

  // Filter out already assigned traits
  const unassignedTraits = availableTraits.filter(
    (t) => !assignedTraits.some((at) => at.id === t.id)
  );

  return (
    <div className={styles.container}>
      <h3>Trait Manager {playerName ? `- ${playerName}` : ""}</h3>

      {error && <div className={styles.errorMessage}>Error: {error}</div>}

      <div className={styles.columnsContainer}>
        <div className={styles.column}>
          <h4>Assigned Traits</h4>
          {loading ? (
            <p>Loading...</p>
          ) : assignedTraits.length === 0 ? (
            <p>No traits assigned.</p>
          ) : (
            <ul className={styles.traitList}>
              {assignedTraits.map((t) => (
                <li key={t.id} className={styles.traitItem}>
                  <strong>{t.name}</strong>
                  <div className={styles.traitDetails}>
                    {t.effect_type} ({t.effect_value})
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className={styles.column}>
          <h4 id="assign-trait-label">Assign New Trait</h4>
          <div className={styles.assignRow}>
            <select
              value={selectedTraitId}
              onChange={(e) => setSelectedTraitId(e.target.value)}
              className={styles.selectTrait}
              aria-labelledby="assign-trait-label"
            >
              <option value="">Select a trait...</option>
              {unassignedTraits.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name} ({t.effect_type})
                </option>
              ))}
            </select>
            <button
              onClick={handleAssign}
              disabled={!selectedTraitId || loading}
              className={styles.assignButton}
            >
              Assign
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
