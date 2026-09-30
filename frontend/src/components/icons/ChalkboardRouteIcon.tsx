import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * ChalkboardRouteIcon
 * Represents tactical playbook route design and coach telestrator diagrams:
 * Pre-snap receiver alignment circle, vertical route stem, sharp 90-degree break cut,
 * directional arrowhead terminal, and opposing defensive coverage "X".
 */
export const ChalkboardRouteIcon: React.FC<IconBaseProps> = ({
  size = 24,
  strokeWidth = 2,
  className,
  title,
  color,
  style,
  ...props
}) => {
  const pixelSize = resolveIconSize(size);

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      width={pixelSize}
      height={pixelSize}
      fill="none"
      stroke={color || "currentColor"}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      vectorEffect="non-scaling-stroke"
      className={className}
      aria-hidden={!title}
      role={title ? "img" : undefined}
      style={style}
      {...props}
    >
      {title && <title>{title}</title>}
      {/* Pre-Snap Receiver Alignment Circle */}
      <circle cx="5" cy="18" r="2" />
      {/* Vertical Route Stem & 90-Degree Break Cut */}
      <path d="M 5 16 V 8 H 15" />
      {/* Directional Route Arrowhead */}
      <path d="M 12 5 L 16 8 L 12 11" />
      {/* Opposing Defensive Coverage "X" */}
      <path d="M 17 15 L 21 19" />
      <path d="M 21 15 L 17 19" />
    </svg>
  );
};

export default ChalkboardRouteIcon;
