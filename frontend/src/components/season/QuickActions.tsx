import React from "react";
import "./QuickActions.css";

interface Action {
  id: string;
  label: string;
  icon: string;
  onClick: () => void;
  disabled?: boolean;
  tooltip?: string;
}

interface QuickActionsProps {
  actions: Action[];
}

export const QuickActions: React.FC<QuickActionsProps> = ({ actions }) => {
  return (
    <div className="quick-actions-container">
      {actions.map((action) => (
        <button
          key={action.id}
          className="action-button"
          onClick={action.onClick}
          disabled={action.disabled}
          title={action.tooltip}
        >
          <span className="action-icon">{action.icon}</span>
          <span className="action-label">{action.label}</span>
        </button>
      ))}
    </div>
  );
};
