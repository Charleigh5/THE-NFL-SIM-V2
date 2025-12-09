/**
 * DroppableZone Component
 * Creates a droppable area for trade assets using dnd-kit
 */
import React from "react";
import { useDroppable } from "@dnd-kit/core";
import type { TradePlayer } from "../../types/trade";
import { DraggableAsset } from "./DraggableAsset";
import "./DroppableZone.css";

interface DroppableZoneProps {
  id: string;
  title: string;
  players: TradePlayer[];
  onRemove: (playerId: number) => void;
  emptyMessage?: string;
}

export const DroppableZone: React.FC<DroppableZoneProps> = ({
  id,
  title,
  players,
  onRemove,
  emptyMessage = "Drag players here",
}) => {
  const { setNodeRef, isOver } = useDroppable({
    id,
  });

  return (
    <div ref={setNodeRef} className={`droppable-zone ${isOver ? "is-over" : ""}`} data-testid={id}>
      <div className="droppable-zone-header">
        <h4>{title}</h4>
        <span className="player-count">{players.length}</span>
      </div>

      <div className="droppable-zone-content">
        {players.length === 0 ? (
          <div className="droppable-zone-empty">
            <span className="empty-icon">➕</span>
            <p>{emptyMessage}</p>
          </div>
        ) : (
          <div className="droppable-zone-items">
            {players.map((player) => (
              <DraggableAsset
                key={player.id}
                id={`${id}-player-${player.id}`}
                player={player}
                showRemoveButton
                onRemove={() => onRemove(player.id)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
