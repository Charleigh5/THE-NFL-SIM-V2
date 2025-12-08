/**
 * ElementInspector Component
 * ==========================
 * Overlay component for design mode that highlights elements on hover
 * and captures clicks for annotation.
 *
 * Context7 Best Practices:
 * - useCallback for memoized event handlers
 * - useEffect for event listener cleanup
 * - useLayoutEffect for DOM manipulation
 */

import { useState, useEffect, useLayoutEffect, useCallback, useRef } from "react";
import { generateCssSelector, getElementDescription } from "../../utils/cssSelector";
import type { ElementMetadata } from "../../hooks/useAnnotationList";
import "./ElementInspector.css";

// ============================================================================
// TYPES
// ============================================================================

interface ElementInspectorProps {
  isActive: boolean;
  onElementSelect: (metadata: ElementMetadata) => void;
  onDeactivate: () => void;
}

// ============================================================================
// COMPONENT
// ============================================================================

const ElementInspector = ({ isActive, onElementSelect, onDeactivate }: ElementInspectorProps) => {
  const [hoveredElement, setHoveredElement] = useState<HTMLElement | null>(null);
  const overlayRef = useRef<HTMLDivElement>(null);

  // Update CSS custom properties via ref (avoids inline styles)
  useLayoutEffect(() => {
    if (overlayRef.current && hoveredElement) {
      const rect = hoveredElement.getBoundingClientRect();
      const el = overlayRef.current;
      el.style.setProperty("--highlight-top", `${rect.top + window.scrollY}px`);
      el.style.setProperty("--highlight-left", `${rect.left + window.scrollX}px`);
      el.style.setProperty("--highlight-width", `${rect.width}px`);
      el.style.setProperty("--highlight-height", `${rect.height}px`);
    }
  }, [hoveredElement]);

  // Handle mouse movement to detect hovered element
  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      if (!isActive) return;

      // Ignore our own overlay elements
      const target = e.target as HTMLElement;
      if (target.closest(".element-inspector-overlay")) {
        return;
      }

      // Ignore feedback widget
      if (target.closest(".feedback-widget")) {
        return;
      }

      setHoveredElement(target);
    },
    [isActive]
  );

  // Handle click to select element
  const handleClick = useCallback(
    (e: MouseEvent) => {
      if (!isActive || !hoveredElement) return;

      // Ignore our own overlay
      const target = e.target as HTMLElement;
      if (target.closest(".element-inspector-overlay")) {
        return;
      }

      // Ignore feedback widget
      if (target.closest(".feedback-widget")) {
        return;
      }

      // Prevent default and stop propagation
      e.preventDefault();
      e.stopPropagation();

      // Generate metadata
      const metadata: ElementMetadata = {
        selector: generateCssSelector(hoveredElement),
        tagName: hoveredElement.tagName.toLowerCase(),
        textContent: getElementDescription(hoveredElement),
        className: hoveredElement.className || undefined,
      };

      onElementSelect(metadata);
    },
    [isActive, hoveredElement, onElementSelect]
  );

  // Handle escape key to deactivate
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === "Escape" && isActive) {
        onDeactivate();
      }
    },
    [isActive, onDeactivate]
  );

  // Setup event listeners
  useEffect(() => {
    if (isActive) {
      document.addEventListener("mousemove", handleMouseMove, true);
      document.addEventListener("click", handleClick, true);
      document.addEventListener("keydown", handleKeyDown);
      document.body.classList.add("design-mode-active");

      return () => {
        document.removeEventListener("mousemove", handleMouseMove, true);
        document.removeEventListener("click", handleClick, true);
        document.removeEventListener("keydown", handleKeyDown);
        document.body.classList.remove("design-mode-active");
        setHoveredElement(null);
      };
    }
  }, [isActive, handleMouseMove, handleClick, handleKeyDown]);

  if (!isActive) return null;

  return (
    <>
      {/* Design Mode Indicator */}
      <div className="element-inspector-overlay design-mode-toast">
        🎨 Design Mode Active — Click any element to annotate (ESC to exit)
      </div>

      {/* Element Highlight Overlay */}
      {hoveredElement && (
        <div ref={overlayRef} className="element-inspector-overlay element-highlight">
          <div className="element-label">
            {hoveredElement.tagName.toLowerCase()}
            {hoveredElement.id ? `#${hoveredElement.id}` : ""}
          </div>
        </div>
      )}
    </>
  );
};

export default ElementInspector;
