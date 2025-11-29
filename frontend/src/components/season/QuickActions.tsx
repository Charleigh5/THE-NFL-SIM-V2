import React from "react";
import "./QuickActions.css";

interface QuickAction {
  id: string;
  label: string;
  icon?: string;
  onClick: () => void;
  disabled?: boolean;
  tooltip?: string;
}

interface QuickActionsProps {
  actions: QuickAction[];
}

export const QuickActions: React.FC<QuickActionsProps> = ({ actions }) => {
  return (
    <div className="quick-actions-container">
      <h2 className="section-title">Quick Actions</h2>
      <div className="actions-grid">
        {actions.map((action) => (
          <button
            key={action.id}
            className="quick-action-btn"
            onClick={action.onClick}
            disabled={action.disabled}
            title={action.tooltip}
          >
            {action.icon && <span className="action-icon">{action.icon}</span>}
            <span className="action-label">{action.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
