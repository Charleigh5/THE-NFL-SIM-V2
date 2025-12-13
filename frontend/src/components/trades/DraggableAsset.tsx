/**
 * DraggableAsset Component
 * Wraps player/pick cards to make them draggable using dnd-kit
 */
import React from "react";
import { useDraggable } from "@dnd-kit/core";
import { CSS } from "@dnd-kit/utilities";
import type { TradePlayer } from "../../types/trade";
import "./DraggableAsset.css";

interface DraggableAssetProps {
  id: string;
  player: TradePlayer;
  disabled?: boolean;
  onClick?: () => void;
  showRemoveButton?: boolean;
  onRemove?: () => void;
}

export const DraggableAsset: React.FC<DraggableAssetProps> = ({
  id,
  player,
  disabled = false,
  onClick,
  showRemoveButton = false,
  onRemove,
}) => {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id,
    disabled,
  });

  // Transform style is required for dnd-kit positioning during drag
  const dragTransform = CSS.Translate.toString(transform);

  const getOverallClass = (overall: number): string => {
    if (overall >= 90) return "elite";
    if (overall >= 80) return "great";
    if (overall >= 70) return "good";
    if (overall >= 60) return "average";
    return "below";
  };

  const classNames = ["draggable-asset", isDragging ? "dragging" : "", disabled ? "disabled" : ""]
    .filter(Boolean)
    .join(" ");

  return (
    // eslint-disable-next-line
    <div
      ref={setNodeRef}
      style={dragTransform ? { transform: dragTransform } : undefined}
      {...listeners}
      {...attributes}
      className={classNames}
      onClick={onClick}
      data-testid={`draggable-${id}`}
    >
      <div className="position-badge">{player.position}</div>
      <div className="player-info">
        <div className="player-name">
          {player.first_name} {player.last_name}
        </div>
        <div className="player-details">
          <span>Age {player.age}</span>
        </div>
      </div>
      <span className={`overall-badge ${getOverallClass(player.overall_rating)}`}>
        {player.overall_rating}
      </span>
      <div className="trade-value">
        <span className="value-label">Value</span>
        <span className="value-number">{player.trade_value}</span>
      </div>
      {showRemoveButton && onRemove && (
        <button
          className="remove-btn"
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          aria-label="Remove player"
        >
          ✕
        </button>
      )}
    </div>
  );
};
