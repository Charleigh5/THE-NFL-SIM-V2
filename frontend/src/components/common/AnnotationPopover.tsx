/**
 * AnnotationPopover Component
 * ===========================
 * Floating popover for adding notes to a selected element.
 *
 * Features:
 * - Positioned near selected element
 * - AI Research toggle
 * - Add/Cancel actions
 */

import { useState, useRef, useEffect } from "react";
import type { ElementMetadata } from "../../hooks/useAnnotationList";
import "./AnnotationPopover.css";

interface AnnotationPopoverProps {
  element: ElementMetadata | null;
  screenshot?: string | null;
  onSave: (note: string, researchRequested: boolean) => void;
  onCancel: () => void;
}

const AnnotationPopover = ({ element, screenshot, onSave, onCancel }: AnnotationPopoverProps) => {
  const [note, setNote] = useState("");
  const [researchRequested, setResearchRequested] = useState(true);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-focus input on mount
  useEffect(() => {
    if (element && inputRef.current) {
      inputRef.current.focus();
    }
  }, [element]);

  if (!element) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (note.trim()) {
      onSave(note, researchRequested);
      setNote("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && e.ctrlKey) {
      handleSubmit(e);
    } else if (e.key === "Escape") {
      onCancel();
    }
  };

  return (
    <div className="annotation-popover">
      <div className="popover-header">
        <span className="element-tag">{element.tagName}</span>
        <span className="element-id">{element.description || element.selector}</span>
      </div>

      {screenshot && (
        <div className="screenshot-preview">
          <img src={screenshot} alt="Captured region" />
          <span className="screenshot-label">📸 Screenshot attached</span>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <textarea
          ref={inputRef}
          value={note}
          onChange={(e) => setNote(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe the change or issue..."
          rows={3}
        />

        <div className="popover-options">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={researchRequested}
              onChange={(e) => setResearchRequested(e.target.checked)}
            />
            <span>AI Research (Best Practices)</span>
          </label>
        </div>

        <div className="popover-actions">
          <button type="button" onClick={onCancel} className="btn-cancel">
            Cancel
          </button>
          <button type="submit" className="btn-save" disabled={!note.trim()}>
            Add to List ⏎
          </button>
        </div>
      </form>
    </div>
  );
};

export default AnnotationPopover;
