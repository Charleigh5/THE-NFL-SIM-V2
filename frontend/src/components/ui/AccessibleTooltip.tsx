import React, { useState, useEffect, useId, useRef } from "react";
import "./AccessibleTooltip.css";

/**
 * Props for the AccessibleTooltip component.
 */
export interface AccessibleTooltipProps {
  /** The tooltip content (text or React node) displayed in the floating bubble. */
  content: React.ReactNode;
  /** The trigger element that receives hover and focus events. */
  children: React.ReactNode;
  /** Optional custom HTML ID for the tooltip bubble. Auto-generated if omitted. */
  id?: string;
  /** Positioning orientation relative to the trigger. Defaults to "top". */
  position?: "top" | "bottom" | "left" | "right";
  /** Optional custom CSS class name for styling the trigger wrapper. */
  className?: string;
}

/**
 * AccessibleTooltip Component
 * ===========================
 * W3C WAI-APG compliant tooltip implementation.
 * - Enforces role="tooltip" and dynamic aria-describedby binding.
 * - Supports mouse hover (onMouseEnter/onMouseLeave) and keyboard focus (onFocus/onBlur).
 * - Implements keyboard dismissal on "Escape" key.
 * - Dark theme styling with WCAG 2.1 AA high contrast (>4.5:1 ratio).
 */
export const AccessibleTooltip: React.FC<AccessibleTooltipProps> = ({
  content,
  children,
  id,
  position = "top",
  className = "",
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const reactGeneratedId = useId();
  const tooltipId = id || `tooltip-${reactGeneratedId.replace(/[^a-zA-Z0-9_-]/g, "")}`;
  const triggerRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (!isVisible) return;
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setIsVisible(false);
      }
    };
    window.addEventListener("keydown", handleGlobalKeyDown);
    return () => window.removeEventListener("keydown", handleGlobalKeyDown);
  }, [isVisible]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape" && isVisible) {
      e.stopPropagation();
      setIsVisible(false);
    }
  };

  return (
    <span
      ref={triggerRef}
      className={`accessible-tooltip-trigger ${className}`.trim()}
      aria-describedby={isVisible ? tooltipId : undefined}
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      {children}
      {isVisible && (
        <div
          id={tooltipId}
          role="tooltip"
          aria-live="polite"
          className={`accessible-tooltip-bubble position-${position}`}
          data-testid="accessible-tooltip-bubble"
        >
          {content}
        </div>
      )}
    </span>
  );
};
