import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * YardHashesIcon
 * Represents the 100-yard gridiron field turf markings:
 * Parallel sideline boundaries, 5-yard transversal lines,
 * and inbound hash tick marks on integer/half-integer coordinates.
 */
export const YardHashesIcon: React.FC<IconBaseProps> = ({
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
      {/* Left & Right Sideline Boundaries */}
      <path d="M 3 3 L 3 21" />
      <path d="M 21 3 L 21 21" />
      {/* Horizontal Transversal Yard Lines */}
      <path d="M 3 6 L 21 6" />
      <path d="M 3 12 L 21 12" />
      <path d="M 3 18 L 21 18" />
      {/* Left Inbound Hashes */}
      <path d="M 9.5 8.5 L 9.5 9.5" />
      <path d="M 9.5 14.5 L 9.5 15.5" />
      {/* Right Inbound Hashes */}
      <path d="M 14.5 8.5 L 14.5 9.5" />
      <path d="M 14.5 14.5 L 14.5 15.5" />
    </svg>
  );
};

export default YardHashesIcon;
