/**
 * TaskListPanel Component
 * =======================
 * Displays pending annotations with thumbnails, allowing edit and remove actions.
 */

import React from "react";
import type { Annotation } from "../../hooks/useAnnotationList";
import "./TaskListPanel.css";

interface TaskListPanelProps {
  annotations: Annotation[];
  onEdit: (annotation: Annotation) => void;
  onRemove: (id: string) => void;
  onClose: () => void;
}

const TaskListPanel: React.FC<TaskListPanelProps> = ({
  annotations,
  onEdit,
  onRemove,
  onClose,
}) => {
  if (annotations.length === 0) {
    return (
      <div className="task-list-panel">
        <div className="panel-header">
          <h4>📋 Pending Tasks</h4>
          <button className="close-btn" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="empty-state">
          <span className="empty-icon">📭</span>
          <p>No tasks yet</p>
          <p className="empty-hint">Use Design Mode or Screenshot to add tasks</p>
        </div>
      </div>
    );
  }

  return (
    <div className="task-list-panel">
      <div className="panel-header">
        <h4>📋 Pending Tasks ({annotations.length})</h4>
        <button className="close-btn" onClick={onClose}>
          ×
        </button>
      </div>

      <div className="task-list">
        {annotations.map((ann, index) => (
          <div key={ann.id} className="task-item">
            <div className="task-number">{index + 1}</div>

            {ann.screenshot && (
              <div className="task-thumbnail">
                <img src={ann.screenshot} alt="Screenshot" />
              </div>
            )}

            <div className="task-content">
              <div className="task-note">{ann.note}</div>
              <div className="task-meta">
                <span className="task-element">&lt;{ann.element.tagName}&gt;</span>
                {ann.aiResearch && <span className="task-research">🔬 Researched</span>}
              </div>
            </div>

            <div className="task-actions">
              <button className="edit-btn" onClick={() => onEdit(ann)} title="Edit annotation">
                ✏️
              </button>
              <button className="remove-btn" onClick={() => onRemove(ann.id)} title="Remove">
                🗑️
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskListPanel;
