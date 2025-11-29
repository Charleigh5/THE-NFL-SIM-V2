import React from "react";
import "./OffseasonTimeline.css";

interface OffseasonTimelineProps {
  currentPhase: string; // 'contract_expirations' | 'draft' | 'free_agency' | 'complete'
}

export const OffseasonTimeline: React.FC<OffseasonTimelineProps> = ({
  currentPhase,
}) => {
  const steps = [
    { id: "contract_expirations", label: "Contracts" },
    { id: "player_progression", label: "Progression" },
    { id: "draft", label: "NFL Draft" },
    { id: "free_agency", label: "Free Agency" },
    { id: "complete", label: "Season Ready" },
  ];

  const getStepStatus = (stepId: string) => {
    // Map backend status or phase to these steps
    // Assuming currentPhase matches one of the IDs or we map it
    const phases = [
      "contract_expirations",
      "player_progression",
      "draft",
      "free_agency",
      "complete",
    ];

    // Simple mapping if needed, but for now assume direct match
    let phaseIndex = phases.indexOf(currentPhase);
    if (phaseIndex === -1) phaseIndex = 0; // Default to start

    const stepIndex = phases.indexOf(stepId);

    if (stepIndex < phaseIndex) return "completed";
    if (stepIndex === phaseIndex) return "active";
    return "pending";
  };

  return (
    <div className="offseason-timeline">
      {steps.map((step, index) => {
        const status = getStepStatus(step.id);
        return (
          <div key={step.id} className={`timeline-step ${status}`}>
            <div className="step-indicator">
              {status === "completed" ? "✓" : index + 1}
            </div>
            <div className="step-label">{step.label}</div>
            {index < steps.length - 1 && <div className="step-connector"></div>}
          </div>
        );
      })}
    </div>
  );
};
