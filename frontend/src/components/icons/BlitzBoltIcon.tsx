import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * BlitzBoltIcon (also exported as DefensiveBlitzBoltIcon)
 * Represents the tactical playbook blitz symbol:
 * Dynamic multi-vertex defensive blitz penetration lightning bolt
 * terminating in a sharp penetration arrowhead.
 */
export const BlitzBoltIcon: React.FC<IconBaseProps> = ({
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
      {/* Dynamic Blitz Bolt Geometry */}
      <path d="M 13 2 L 5.5 12 L 11.5 12 L 8 22 L 19 9.5 L 13 9.5 Z" />
    </svg>
  );
};

export const DefensiveBlitzBoltIcon = BlitzBoltIcon;
export default BlitzBoltIcon;
