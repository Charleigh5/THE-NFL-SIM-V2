import { useState } from "react";
import { useLoaderData, useParams, useRevalidator } from "react-router-dom";
import { SkillTreeCanvas } from "../components/skills/SkillTreeCanvas";
import { SkillsOverlay } from "../components/skills/SkillsOverlay";
import { SKILL_TREE_LAYOUTS } from "../config/SkillTreeConfig";
import type { Trait as TraitType } from "../types/trait"; // Use shared type
import { traitsApi } from "../services/traits";
import type { Player } from "../services/api";

interface LoaderData {
  player: Player;
  traits: TraitType[];
}

export const SkillsPage = () => {
  const data = useLoaderData() as LoaderData | null;
  const { playerId } = useParams();
  const revalidator = useRevalidator();

  const [selectedTraitId, setSelectedTraitId] = useState<string | null>(null);

  // Optimistic UI updates
  const [optimisticUnlocks, setOptimisticUnlocks] = useState<string[]>([]);

  // Derived state
  const backendUnlocked = data?.traits.map((t) => t.name) || [];
  const unlockedTraits = Array.from(new Set([...backendUnlocked, ...optimisticUnlocks]));

  // Equipped logic: Currently just matches unlocked, but allow local toggle
  // Since we don't have backend persistence for "equipped" vs "unlocked",
  // we just assume all unlocked are equipped, or manage a local exclusion list.
  // For simplicity: All unlocked are equipped.
  const equippedTraits = unlockedTraits;

  // If no data (e.g. separate route or error), we might want to redirect or show empty
  // For dev, if no playerId, maybe show nothing?
  // if (!data) return <div className="text-white">Loading or No Player Selected</div>;

  const handleNodeClick = (traitId: string) => {
    setSelectedTraitId(traitId);
  };

  const handleUnlockOrEquip = async (traitId: string) => {
    if (!playerId) return;

    // Check if locked
    if (!unlockedTraits.includes(traitId)) {
      // Optimistic Update
      setOptimisticUnlocks((prev) => [...prev, traitId]);

      // API Call to Unlock
      try {
        const success = await traitsApi.unlockTrait(parseInt(playerId), traitId);
        if (success) {
          // Revalidate to get official state
          revalidator.revalidate();
          // Clear optimistic unlocks for this trait once confirmed by backend
          setOptimisticUnlocks((prev) => prev.filter((id) => id !== traitId));
        }
      } catch (e) {
        console.error("Failed to unlock trait", e);
        // Rollback optimistic update if needed, or just let revalidate handle it
        setOptimisticUnlocks((prev) => prev.filter((id) => id !== traitId)); // Rollback on error
      }
    } else {
      // Toggle Equip (Local only)
      // Since equippedTraits === unlockedTraits in this simplified version, we can't really toggle "off"
      // without extra state.
      // TODO: Implement "Equipped" slot logic when backend supports it.
      // For now, doing nothing or maybe logging.
      console.log("Toggle equip not fully supported yet");
    }
  };

  // Helper to find trait details from Config or Data
  // We need description/effects.
  // The Loader Trait has description/effect_type/value
  // The Config just has position/icon.
  // We should merge them.
  // But SKILL_TREE_LAYOUTS doesn't have description.
  // So we rely on backend data.
  // BUT: What if the user clicks a LOCKED node? usage data might not have it.
  // We need a catalog of ALL traits to show details for locked ones.
  // The current API `getAllTraits` exists. We might need to load that too?
  // Or just use the Mock data for descriptions if backend doesn't provide "All Traits".
  // `traitsApi.getAllTraits()` exists.

  // For now, I'll use a placeholder description if not found in user's traits.
  // Or fetch all traits in loader?

  const playerTrait = data?.traits.find((t) => t.name === selectedTraitId);

  // Construct details, merging backend data with defaults if locked
  const selectedTraitDetails: TraitType | null = selectedTraitId
    ? playerTrait ||
      ({
        id: 0,
        name: selectedTraitId,
        description: "Unlock this trait to see details.",
        effect_type: "PASSIVE" as const, // Cast literal to enum/string
        effect_value: 0,
        tier: "COMMON",
        extra_stats: {},
      } as unknown as TraitType)
    : null;
  // Note: Cast as unknown as TraitType because the fallback object assumes TraitType shape.
  // effect_type "PASSIVE" matches type.

  // Determine Layout based on Player Position (e.g. QB, WR)
  // Default to QB if not map
  const position = data?.player?.position || "QB";
  // Check if layout exists, else default key
  const layoutKey = SKILL_TREE_LAYOUTS[position] ? position : "QB";
  const layout = SKILL_TREE_LAYOUTS[layoutKey];

  return (
    <div className="w-full h-screen relative bg-black overflow-hidden">
      <SkillTreeCanvas
        layout={layout}
        unlockedTraits={unlockedTraits}
        equippedTraits={equippedTraits}
        onNodeClick={handleNodeClick}
      />

      <SkillsOverlay
        selectedTraitId={selectedTraitId}
        selectedTraitDetails={selectedTraitDetails}
        playerPoints={3} // TODO: Fetch available points
        onCloseDetail={() => setSelectedTraitId(null)}
        onEquip={handleUnlockOrEquip}
      />
    </div>
  );
};
