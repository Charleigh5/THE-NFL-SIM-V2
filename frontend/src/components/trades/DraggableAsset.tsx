import React from "react";
import styled from "styled-components";
import { useDraggable } from "@dnd-kit/core";
import { CSS } from "@dnd-kit/utilities";
import type { TradePlayer } from "../../types/trade";

/**
 * Styled Components for standard-compliant dynamic styling.
 * Using .attrs() ensures that high-frequency updates (60fps)
 * are applied efficiently without generating new CSS classes.
 */
const AssetContainer = styled.div.attrs<{ $transform?: string; $isDragging?: boolean }>(
  (props) => ({
    style: {
      transform: props.$transform
        ? `${props.$transform} ${props.$isDragging ? "scale(1.05)" : ""}`
        : undefined,
    },
  })
)<{ $isDragging?: boolean; $disabled?: boolean }>`
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.2s ease;
  touch-action: none;
  opacity: ${(props) => (props.$isDragging ? 0.5 : props.$disabled ? 0.6 : 1)};
  cursor: ${(props) => (props.$disabled ? "not-allowed" : "grab")};
  z-index: ${(props) => (props.$isDragging ? 1000 : 1)};
  box-shadow: ${(props) => (props.$isDragging ? "0 8px 24px rgba(0, 0, 0, 0.4)" : "none")};

  &:hover:not(:disabled) {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
    border-color: rgba(255, 255, 255, 0.2);
    transform: ${(props) => (props.$isDragging ? "none" : "translateY(-2px)")};
    box-shadow: ${(props) =>
      props.$isDragging ? "0 8px 24px rgba(0, 0, 0, 0.4)" : "0 4px 12px rgba(0, 0, 0, 0.3)"};
  }

  &:active:not(:disabled) {
    cursor: grabbing;
  }

  .position-badge {
    background: rgba(59, 130, 246, 0.2);
    color: #60a5fa;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    min-width: 32px;
    text-align: center;
  }

  .player-info {
    flex: 1;
    min-width: 0;
  }

  .player-name {
    font-weight: 600;
    font-size: 14px;
    color: #fff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .player-details {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    margin-top: 2px;
  }

  .overall-badge {
    font-weight: 700;
    font-size: 16px;
    padding: 4px 8px;
    border-radius: 4px;
    min-width: 36px;
    text-align: center;

    &.elite {
      background: linear-gradient(135deg, #a855f7, #ec4899);
      color: #fff;
    }
    &.great {
      background: linear-gradient(135deg, #3b82f6, #06b6d4);
      color: #fff;
    }
    &.good {
      background: linear-gradient(135deg, #10b981, #14b8a6);
      color: #fff;
    }
    &.average {
      background: rgba(234, 179, 8, 0.2);
      color: #fbbf24;
    }
    &.below {
      background: rgba(239, 68, 68, 0.2);
      color: #f87171;
    }
  }

  .trade-value {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
  }

  .value-label {
    font-size: 10px;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .value-number {
    font-size: 14px;
    font-weight: 700;
    color: #60a5fa;
  }

  .remove-btn {
    position: absolute;
    top: 4px;
    right: 4px;
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
    z-index: 10;

    &:hover {
      background: rgba(239, 68, 68, 0.4);
      transform: scale(1.1);
    }
  }

  @media (max-width: 768px) {
    padding: 10px;
    gap: 8px;
    .player-name {
      font-size: 13px;
    }
    .overall-badge {
      font-size: 14px;
      min-width: 32px;
    }
  }
`;

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

  const dragTransform = CSS.Translate.toString(transform);

  const getOverallLevel = (overall: number): string => {
    if (overall >= 90) return "elite";
    if (overall >= 80) return "great";
    if (overall >= 70) return "good";
    if (overall >= 60) return "average";
    return "below";
  };

  return (
    <AssetContainer
      ref={setNodeRef}
      $transform={dragTransform}
      $isDragging={isDragging}
      $disabled={disabled}
      {...listeners}
      {...attributes}
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
      <span className={`overall-badge ${getOverallLevel(player.overall_rating)}`}>
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
    </AssetContainer>
  );
};
