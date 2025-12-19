import { useState, useCallback } from "react";
import axios from "axios";
import ElementInspector from "./ElementInspector";
import AnnotationPopover from "./AnnotationPopover";
import RegionSelector from "./RegionSelector";
import TaskListPanel from "./TaskListPanel";
import ScreenshotEditor from "./ScreenshotEditor";
import {
  useAnnotationList,
  type ElementMetadata,
  type Annotation,
} from "../../hooks/useAnnotationList";
import "./FeedbackWidget.css";

interface FeedbackWidgetProps {
  currentPage?: string;
}

interface BatchSubmitResult {
  artifact_path: string;
  issues_logged: number;
}

const FeedbackWidget = ({ currentPage = "Unknown" }: FeedbackWidgetProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isDesignMode, setIsDesignMode] = useState(false);
  const [isScreenshotMode, setIsScreenshotMode] = useState(false);
  const [isTaskListOpen, setIsTaskListOpen] = useState(false);
  const [selectedElement, setSelectedElement] = useState<ElementMetadata | null>(null);
  const [capturedScreenshot, setCapturedScreenshot] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGeneratingPlan, setIsGeneratingPlan] = useState(false);
  const [editingAnnotation, setEditingAnnotation] = useState<Annotation | null>(null);
  const [lastBatchResult, setLastBatchResult] = useState<BatchSubmitResult | null>(null);

  const { annotations, addAnnotation, updateAnnotation, removeAnnotation, clearAll } =
    useAnnotationList();

  const handleToggle = useCallback(() => {
    setIsOpen((prev) => !prev);
    if (isOpen) {
      setIsDesignMode(false);
      setIsScreenshotMode(false);
      setIsTaskListOpen(false);
    }
  }, [isOpen]);

  const handleDesignModeToggle = () => {
    setIsDesignMode(!isDesignMode);
    setIsScreenshotMode(false);
    setIsOpen(false);
  };

  const handleScreenshotModeToggle = () => {
    setIsScreenshotMode(!isScreenshotMode);
    setIsDesignMode(false);
    setIsOpen(false);
  };

  const handleTaskListToggle = () => {
    setIsTaskListOpen(!isTaskListOpen);
    setIsOpen(false);
  };

  const handleElementSelect = useCallback((metadata: ElementMetadata) => {
    setSelectedElement(metadata);
  }, []);

  const handleScreenshotCapture = useCallback((imageData: string, rect: DOMRect) => {
    setCapturedScreenshot(imageData);
    const screenshotMetadata = {
      selector: `screenshot-${Date.now()}`,
      tagName: "SCREENSHOT",
      description: `📸 Screen Region (${Math.round(rect.width)}×${Math.round(rect.height)})`,
      boundingRect: {
        top: rect.y,
        left: rect.x,
        width: rect.width,
        height: rect.height,
      },
    } as ElementMetadata;
    setSelectedElement(screenshotMetadata);
    setIsScreenshotMode(false);
  }, []);

  const handleSaveAnnotation = useCallback(
    async (note: string, researchRequested: boolean) => {
      if (selectedElement) {
        addAnnotation(note, selectedElement, capturedScreenshot ?? undefined);

        if (researchRequested) {
          axios
            .post("/api/feedback/research", { task: note })
            .then((res) => {
              console.log("Research complete:", res.data);
            })
            .catch((err) => console.error("Research failed:", err));
        }

        setSelectedElement(null);
        setCapturedScreenshot(null);
      }
    },
    [selectedElement, addAnnotation, capturedScreenshot]
  );

  const handleEditAnnotation = (annotation: Annotation) => {
    setEditingAnnotation(annotation);
    setIsTaskListOpen(false);
  };

  const handleSaveEdit = (updatedAnnotation: Annotation) => {
    updateAnnotation(updatedAnnotation.id, updatedAnnotation);
    setEditingAnnotation(null);
  };

  const handleRemoveAnnotation = (id: string) => {
    removeAnnotation(id);
  };

  const handleBatchSubmit = async () => {
    if (annotations.length === 0) return;
    setIsSubmitting(true);
    setLastBatchResult(null);

    try {
      // Use the new export endpoint to save to docs/updates_and_enhancements
      const response = await axios.post("/api/feedback/export", { annotations });
      const result: BatchSubmitResult = response.data;
      setLastBatchResult(result);
      clearAll();
      // Don't close panel - show success with "Generate Plan" option
    } catch (error) {
      console.error("Export failed:", error);
      alert("❌ Failed to export tasks. Check console for details.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGeneratePlan = async () => {
    if (!lastBatchResult) return;
    setIsGeneratingPlan(true);

    try {
      // Convert the batch result info into task items for the agent
      const tasks = [
        {
          id: Date.now().toString(),
          note: `Task list from ${lastBatchResult.artifact_path}`,
          element_type: "BATCH",
          has_research: false,
        },
      ];

      const response = await axios.post("/api/agent/generate-plan", {
        tasks,
        project_context: `Generated from Mission Control batch with ${lastBatchResult.issues_logged} issues`,
      });

      alert(
        `✅ Implementation plan generated!\n\nArtifact: ${response.data.artifact_path}\nTasks: ${response.data.task_count}\n\n${response.data.summary}`
      );
      setLastBatchResult(null);
      setIsOpen(false);
    } catch (error) {
      console.error("Plan generation failed:", error);
      alert("❌ Failed to generate plan. Check console for details.");
    } finally {
      setIsGeneratingPlan(false);
    }
  };

  const handleDismissSuccess = () => {
    setLastBatchResult(null);
  };

  return (
    <>
      <ElementInspector
        isActive={isDesignMode}
        onElementSelect={handleElementSelect}
        onDeactivate={() => setIsDesignMode(false)}
      />

      <RegionSelector
        isActive={isScreenshotMode}
        onCapture={handleScreenshotCapture}
        onCancel={() => setIsScreenshotMode(false)}
      />

      <AnnotationPopover
        element={selectedElement}
        screenshot={capturedScreenshot}
        onSave={handleSaveAnnotation}
        onCancel={() => {
          setSelectedElement(null);
          setCapturedScreenshot(null);
        }}
      />

      {isTaskListOpen && (
        <TaskListPanel
          annotations={annotations}
          onEdit={handleEditAnnotation}
          onRemove={handleRemoveAnnotation}
          onClose={() => setIsTaskListOpen(false)}
        />
      )}

      {editingAnnotation && (
        <ScreenshotEditor
          annotation={editingAnnotation}
          onSave={handleSaveEdit}
          onClose={() => setEditingAnnotation(null)}
        />
      )}

      <div className="feedback-widget">
        <button
          className={`feedback-fab ${isOpen ? "active" : ""} ${isDesignMode ? "design-active" : ""} ${isScreenshotMode ? "screenshot-active" : ""}`}
          onClick={handleToggle}
          aria-label="Mission Control"
        >
          {isOpen ? "×" : isDesignMode ? "🎨" : isScreenshotMode ? "📸" : "⚡"}
        </button>

        {isOpen && (
          <div className="feedback-panel">
            <div className="feedback-header">
              <h3>Mission Control</h3>
              <span className="feedback-page">{currentPage}</span>
            </div>

            {/* Success State - Show after batch submit */}
            {lastBatchResult && (
              <div className="success-panel">
                <div className="success-icon">✅</div>
                <h4>Tasks Exported!</h4>
                <p className="success-details">{lastBatchResult.issues_logged} issues logged</p>
                <div className="success-actions">
                  <button
                    className="generate-plan-btn"
                    onClick={handleGeneratePlan}
                    disabled={isGeneratingPlan}
                  >
                    {isGeneratingPlan ? "🔄 Generating..." : "🚀 Generate Plan"}
                  </button>
                  <button className="dismiss-btn" onClick={handleDismissSuccess}>
                    Done
                  </button>
                </div>
              </div>
            )}

            {/* Normal State - Annotations and actions */}
            {!lastBatchResult && (
              <>
                <div className="feedback-stats">
                  <button
                    className="stat-item clickable"
                    onClick={handleTaskListToggle}
                    type="button"
                  >
                    <span className="stat-value">{annotations.length}</span>
                    <span className="stat-label">Pending Tasks</span>
                  </button>
                </div>

                <div className="feedback-actions-grid">
                  <button className="action-card" onClick={handleDesignModeToggle}>
                    <span className="icon">🎨</span>
                    <span className="label">Enter Design Mode</span>
                  </button>

                  <button className="action-card" onClick={handleScreenshotModeToggle}>
                    <span className="icon">📸</span>
                    <span className="label">Screenshot Region</span>
                  </button>

                  <button className="action-card" onClick={handleTaskListToggle}>
                    <span className="icon">📋</span>
                    <span className="label">View Tasks</span>
                  </button>

                  <button
                    className="action-card"
                    onClick={() => window.open("/ISSUES.md", "_blank")}
                  >
                    <span className="icon">🐛</span>
                    <span className="label">View Issues</span>
                  </button>
                </div>

                {annotations.length > 0 && (
                  <div className="batch-actions">
                    <button
                      className="feedback-submit batch-btn"
                      onClick={handleBatchSubmit}
                      disabled={isSubmitting}
                    >
                      {isSubmitting
                        ? "Exporting..."
                        : `Export Updates to Docs (${annotations.length})`}
                    </button>
                    <button className="clear-link" onClick={clearAll}>
                      Clear List
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </>
  );
};

export default FeedbackWidget;
