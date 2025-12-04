import React from "react";
import { InteractionOutcome } from "../../types/interaction";
import "./InteractionBadge.css";

interface InteractionBadgeProps {
  outcome: InteractionOutcome;
  showLabel?: boolean;
}

const InteractionBadge: React.FC<InteractionBadgeProps> = ({ outcome, showLabel = true }) => {
  const getClassName = (outcome: InteractionOutcome): string => {
    switch (outcome) {
      case InteractionOutcome.DOMINANT_WIN:
        return "dominant-win";
      case InteractionOutcome.WIN:
        return "win";
      case InteractionOutcome.SLIGHT_WIN:
        return "slight-win";
      case InteractionOutcome.NEUTRAL:
        return "neutral";
      case InteractionOutcome.SLIGHT_LOSS:
        return "slight-loss";
      case InteractionOutcome.LOSS:
        return "loss";
      case InteractionOutcome.DOMINANT_LOSS:
        return "dominant-loss";
      default:
        return "neutral";
    }
  };

  const getLabel = (outcome: InteractionOutcome): string => {
    return outcome.replace("_", " ");
  };

  return (
    <span className={`interaction-badge ${getClassName(outcome)}`}>
      {showLabel ? getLabel(outcome) : ""}
    </span>
  );
};

export default InteractionBadge;
