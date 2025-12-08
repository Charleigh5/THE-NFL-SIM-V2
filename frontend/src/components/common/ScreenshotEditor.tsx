/**
 * ScreenshotEditor Component
 * ==========================
 * Modal for editing screenshots with drawing and text annotation tools.
 */

import React, { useRef, useState, useEffect, useCallback } from "react";
import type { Annotation } from "../../hooks/useAnnotationList";
import "./ScreenshotEditor.css";

interface ScreenshotEditorProps {
  annotation: Annotation;
  onSave: (updatedAnnotation: Annotation) => void;
  onClose: () => void;
}

interface DrawPoint {
  x: number;
  y: number;
}

const ScreenshotEditor: React.FC<ScreenshotEditorProps> = ({ annotation, onSave, onClose }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [brushColor, setBrushColor] = useState("#ff4444");
  const [brushSize, setBrushSize] = useState(3);
  const [note, setNote] = useState(annotation.note);
  const [history, setHistory] = useState<ImageData[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);

  // Load image onto canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !annotation.screenshot) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const img = new Image();
    img.onload = () => {
      // Set canvas size to image size (max 800x600)
      const maxWidth = 800;
      const maxHeight = 600;
      let width = img.width;
      let height = img.height;

      if (width > maxWidth) {
        height = (height * maxWidth) / width;
        width = maxWidth;
      }
      if (height > maxHeight) {
        width = (width * maxHeight) / height;
        height = maxHeight;
      }

      canvas.width = width;
      canvas.height = height;
      ctx.drawImage(img, 0, 0, width, height);

      // Save initial state to history
      const imageData = ctx.getImageData(0, 0, width, height);
      setHistory([imageData]);
      setHistoryIndex(0);
    };
    img.src = annotation.screenshot;
  }, [annotation.screenshot]);

  // Save to history
  const saveToHistory = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const newHistory = history.slice(0, historyIndex + 1);
    newHistory.push(imageData);
    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
  }, [history, historyIndex]);

  // Undo
  const handleUndo = useCallback(() => {
    if (historyIndex <= 0) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const newIndex = historyIndex - 1;
    ctx.putImageData(history[newIndex], 0, 0);
    setHistoryIndex(newIndex);
  }, [history, historyIndex]);

  // Redo
  const handleRedo = useCallback(() => {
    if (historyIndex >= history.length - 1) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const newIndex = historyIndex + 1;
    ctx.putImageData(history[newIndex], 0, 0);
    setHistoryIndex(newIndex);
  }, [history, historyIndex]);

  // Get mouse position relative to canvas
  const getMousePos = (e: React.MouseEvent<HTMLCanvasElement>): DrawPoint => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };

    const rect = canvas.getBoundingClientRect();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    };
  };

  // Drawing handlers
  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const pos = getMousePos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    ctx.strokeStyle = brushColor;
    ctx.lineWidth = brushSize;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    setIsDrawing(true);
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const pos = getMousePos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
  };

  const stopDrawing = () => {
    if (isDrawing) {
      saveToHistory();
      setIsDrawing(false);
    }
  };

  // Save edited screenshot
  const handleSave = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const newScreenshot = canvas.toDataURL("image/png");
    const updatedAnnotation: Annotation = {
      ...annotation,
      note,
      screenshot: newScreenshot,
    };
    onSave(updatedAnnotation);
  };

  const colors = ["#ff4444", "#44ff44", "#4444ff", "#ffff44", "#ff44ff", "#ffffff", "#000000"];

  return (
    <div className="screenshot-editor-overlay" onClick={onClose}>
      <div className="screenshot-editor-modal" onClick={(e) => e.stopPropagation()}>
        <div className="editor-header">
          <h3>✏️ Edit Screenshot</h3>
          <button className="close-btn" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="editor-toolbar">
          <div className="tool-group">
            <label>Color:</label>
            <div className="color-picker">
              {colors.map((color) => (
                <button
                  key={color}
                  className={`color-btn ${brushColor === color ? "active" : ""}`}
                  data-color={color}
                  onClick={() => setBrushColor(color)}
                  title={`Select ${color} color`}
                  aria-label={`Select ${color} color`}
                />
              ))}
            </div>
          </div>

          <div className="tool-group">
            <label>Size:</label>
            <input
              type="range"
              min="1"
              max="20"
              value={brushSize}
              onChange={(e) => setBrushSize(Number(e.target.value))}
              title="Brush size"
              aria-label="Brush size"
            />
            <span>{brushSize}px</span>
          </div>

          <div className="tool-group">
            <button
              className="tool-btn"
              onClick={handleUndo}
              disabled={historyIndex <= 0}
              title="Undo"
            >
              ↩️ Undo
            </button>
            <button
              className="tool-btn"
              onClick={handleRedo}
              disabled={historyIndex >= history.length - 1}
              title="Redo"
            >
              ↪️ Redo
            </button>
          </div>
        </div>

        <div className="canvas-container">
          <canvas
            ref={canvasRef}
            onMouseDown={startDrawing}
            onMouseMove={draw}
            onMouseUp={stopDrawing}
            onMouseLeave={stopDrawing}
          />
        </div>

        <div className="note-editor">
          <label>Note:</label>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Add notes about this screenshot..."
            rows={3}
          />
        </div>

        <div className="editor-footer">
          <button className="cancel-btn" onClick={onClose}>
            Cancel
          </button>
          <button className="save-btn" onClick={handleSave}>
            💾 Save Changes
          </button>
        </div>
      </div>
    </div>
  );
};

export default ScreenshotEditor;
