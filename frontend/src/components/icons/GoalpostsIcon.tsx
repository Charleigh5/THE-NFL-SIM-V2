import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * GoalpostsIcon
 * Represents the official NFL slingshot goalpost:
 * Gooseneck central base stanchion, ground base plate,
 * horizontal crossbar, dual vertical uprights, and top streamer ribbons.
 */
export const GoalpostsIcon: React.FC<IconBaseProps> = ({
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
      {/* Ground Base Plate */}
      <path d="M 8.5 22 L 15.5 22" />
      {/* Gooseneck Stanchion */}
      <path d="M 12 22 L 12 14" />
      {/* Horizontal Crossbar */}
      <path d="M 5 14 L 19 14" />
      {/* Left Upright */}
      <path d="M 5 14 L 5 3" />
      {/* Right Upright */}
      <path d="M 19 14 L 19 3" />
      {/* Top Wind Streamers */}
      <path d="M 5 3 L 3 4.5" />
      <path d="M 19 3 L 21 4.5" />
    </svg>
  );
};

export default GoalpostsIcon;
