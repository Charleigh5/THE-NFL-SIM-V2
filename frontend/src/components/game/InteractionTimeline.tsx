import React from "react";
import type { InteractionResult } from "../../types/interaction";
import { InteractionOutcome } from "../../types/interaction";
import InteractionBadge from "./InteractionBadge";
import "./InteractionTimeline.css";

interface InteractionTimelineProps {
  interactions: InteractionResult[];
}

const InteractionTimeline: React.FC<InteractionTimelineProps> = ({ interactions }) => {
  if (!interactions || interactions.length === 0) {
    return null;
  }

  const isWin = (outcome: InteractionOutcome): boolean => {
    const winOutcomes: InteractionOutcome[] = [
      InteractionOutcome.DOMINANT_WIN,
      InteractionOutcome.WIN,
      InteractionOutcome.SLIGHT_WIN,
    ];
    return winOutcomes.includes(outcome);
  };

  const isLoss = (outcome: InteractionOutcome): boolean => {
    const lossOutcomes: InteractionOutcome[] = [
      InteractionOutcome.DOMINANT_LOSS,
      InteractionOutcome.LOSS,
      InteractionOutcome.SLIGHT_LOSS,
    ];
    return lossOutcomes.includes(outcome);
  };

  const getBorderClass = (outcome: InteractionOutcome) => {
    if (isWin(outcome)) return "win-border";
    if (isLoss(outcome)) return "loss-border";
    return "";
  };

  const formatName = (name: string) => {
    return name
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  return (
    <div className="interaction-timeline">
      {interactions.map((interaction, index) => (
        <div key={index} className={`interaction-item ${getBorderClass(interaction.outcome)}`}>
          <div className="interaction-details">
            <span className="interaction-name">{formatName(interaction.interaction_name)}</span>
            <div className="interaction-matchup">
              {interaction.attacker_name} vs {interaction.defender_name}
            </div>
            <div className="interaction-narrative">"{interaction.narrative}"</div>
          </div>

          <div className="interaction-outcome-container">
            <InteractionBadge outcome={interaction.outcome} />
            {interaction.winner_boost > 0 && (
              <span className="interaction-boost">+{interaction.winner_boost.toFixed(1)}%</span>
            )}
            {interaction.loser_penalty > 0 && (
              <span className="interaction-penalty">-{interaction.loser_penalty.toFixed(1)}%</span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default InteractionTimeline;
