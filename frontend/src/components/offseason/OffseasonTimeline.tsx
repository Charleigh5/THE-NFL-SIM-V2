import React from "react";
import "./OffseasonTimeline.css";

interface PhaseStat {
  percentage: number;
  description: string;
  actionAvailable: boolean;
}

interface OffseasonTimelineProps {
  currentPhase: string;
  phaseStats?: {
    [key: string]: PhaseStat;
  };
  onPhaseAction?: (phaseId: string) => void;
}

export const OffseasonTimeline: React.FC<OffseasonTimelineProps> = ({
  currentPhase,
  phaseStats = {},
  onPhaseAction,
}) => {
  const steps = [
    { id: "contract_expirations", label: "Contracts" },
    { id: "player_progression", label: "Progression" },
    { id: "draft", label: "NFL Draft" },
    { id: "free_agency", label: "Free Agency" },
    { id: "complete", label: "Season Ready" },
  ];

  const getStepStatus = (stepId: string) => {
    const phases = [
      "contract_expirations",
      "player_progression",
      "draft",
      "free_agency",
      "complete",
    ];

    let phaseIndex = phases.indexOf(currentPhase);
    if (phaseIndex === -1) phaseIndex = 0;

    const stepIndex = phases.indexOf(stepId);

    if (stepIndex < phaseIndex) return "completed";
    if (stepIndex === phaseIndex) return "active";
    return "pending";
  };

  return (
    <div className="offseason-timeline" data-testid="offseason-timeline">
      {steps.map((step, index) => {
        const status = getStepStatus(step.id);
        const stats = phaseStats[step.id];
        const isActive = status === "active";

        return (
          <div key={step.id} className={`timeline-step ${status}`} data-testid={`timeline-step-${step.id}`}>
            <div className="step-indicator-container">
              <div className="step-indicator">{status === "completed" ? "✓" : index + 1}</div>
              {index < steps.length - 1 && <div className="step-connector"></div>}
            </div>

            <div className="step-content">
              <div className="step-label">{step.label}</div>

              {isActive && stats && (
                <div className="step-details">
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${stats.percentage}%` }}></div>
                  </div>
                  <div className="step-desc">{stats.description}</div>
                  {stats.actionAvailable && (
                    <button className="step-action-btn" onClick={() => onPhaseAction?.(step.id)} data-testid={`timeline-action-button-${step.id}`}>
                      Continue
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
