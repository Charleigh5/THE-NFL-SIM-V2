import { useState, useCallback, useRef, useEffect, useLayoutEffect } from "react";
import html2canvas from "html2canvas";
import "./RegionSelector.css";

interface RegionSelectorProps {
  isActive: boolean;
  onCapture: (imageData: string, rect: DOMRect) => void;
  onCancel: () => void;
}

interface SelectionRect {
  startX: number;
  startY: number;
  endX: number;
  endY: number;
}

/**
 * RegionSelector - A lasso/screenshot tool for capturing screen regions
 *
 * Usage:
 * 1. User clicks and drags to select a region
 * 2. On mouse up, the region is captured using html2canvas
 * 3. The captured image is returned as a base64 data URL
 */
const RegionSelector = ({ isActive, onCapture, onCancel }: RegionSelectorProps) => {
  const [selection, setSelection] = useState<SelectionRect | null>(null);
  const [isSelecting, setIsSelecting] = useState(false);
  const overlayRef = useRef<HTMLDivElement>(null);
  const boxRef = useRef<HTMLDivElement>(null);

  // Handle escape key to cancel
  useEffect(() => {
    if (!isActive) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setSelection(null);
        setIsSelecting(false);
        onCancel();
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isActive, onCancel]);

  // Update CSS custom properties for selection box position (avoids inline styles)
  useLayoutEffect(() => {
    if (boxRef.current && selection) {
      const left = Math.min(selection.startX, selection.endX);
      const top = Math.min(selection.startY, selection.endY);
      const width = Math.abs(selection.endX - selection.startX);
      const height = Math.abs(selection.endY - selection.startY);

      boxRef.current.style.setProperty("--box-left", `${left}px`);
      boxRef.current.style.setProperty("--box-top", `${top}px`);
      boxRef.current.style.setProperty("--box-width", `${width}px`);
      boxRef.current.style.setProperty("--box-height", `${height}px`);
    }
  }, [selection]);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    // Ignore clicks on the overlay itself (only start from content)
    if (e.target === overlayRef.current) {
      setIsSelecting(true);
      setSelection({
        startX: e.clientX,
        startY: e.clientY,
        endX: e.clientX,
        endY: e.clientY,
      });
    }
  }, []);

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      if (!isSelecting || !selection) return;

      setSelection((prev) =>
        prev
          ? {
              ...prev,
              endX: e.clientX,
              endY: e.clientY,
            }
          : null
      );
    },
    [isSelecting, selection]
  );

  const handleMouseUp = useCallback(async () => {
    if (!isSelecting || !selection) return;

    const rect = {
      x: Math.min(selection.startX, selection.endX),
      y: Math.min(selection.startY, selection.endY),
      width: Math.abs(selection.endX - selection.startX),
      height: Math.abs(selection.endY - selection.startY),
    };

    // Only capture if selection is meaningful (> 20px)
    if (rect.width > 20 && rect.height > 20) {
      try {
        // Hide overlay temporarily for clean capture
        if (overlayRef.current) {
          overlayRef.current.style.display = "none";
        }

        // Capture the full document body
        const canvas = await html2canvas(document.body, {
          x: rect.x + window.scrollX,
          y: rect.y + window.scrollY,
          width: rect.width,
          height: rect.height,
          useCORS: true,
          logging: false,
          backgroundColor: null,
        });

        // Restore overlay
        if (overlayRef.current) {
          overlayRef.current.style.display = "block";
        }

        const imageData = canvas.toDataURL("image/png");

        onCapture(imageData, new DOMRect(rect.x, rect.y, rect.width, rect.height));
      } catch (error) {
        console.error("Failed to capture screenshot:", error);
      }
    }

    setSelection(null);
    setIsSelecting(false);
  }, [isSelecting, selection, onCapture]);

  if (!isActive) return null;

  // Calculate if selection is visible
  const hasSelection =
    selection &&
    Math.abs(selection.endX - selection.startX) > 0 &&
    Math.abs(selection.endY - selection.startY) > 0;

  return (
    <div
      ref={overlayRef}
      className="region-selector-overlay"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
    >
      <div className="region-selector-instructions">
        <span>📸 Click and drag to select a region • Press ESC to cancel</span>
      </div>

      {hasSelection && (
        <div ref={boxRef} className="region-selector-box">
          <div className="region-selector-dimensions">
            {Math.round(Math.abs(selection.endX - selection.startX))} ×{" "}
            {Math.round(Math.abs(selection.endY - selection.startY))}
          </div>
        </div>
      )}
    </div>
  );
};

export default RegionSelector;
