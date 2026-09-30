import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * PenaltyFlagIcon
 * Represents the official NFL weighted yellow penalty flag:
 * Compact weighted beanbag shot pouch base, cinch tie knot,
 * and dynamic billowing cloth tail fluttering diagonally upward.
 */
export const PenaltyFlagIcon: React.FC<IconBaseProps> = ({
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
      {/* Weighted Shot Pouch Base */}
      <circle cx="6" cy="18" r="3" />
      {/* Pouch Tie Knot */}
      <path d="M 6.5 15.5 L 9 15.5" />
      {/* Billowing Fluttering Cloth Streamer */}
      <path d="M 7.5 15.5 C 9 11, 12 12.5, 14 9.5 C 16 6.5, 18 8, 21.5 5 C 20 9.5, 17.5 11, 15 13.5 C 12.5 16, 10 16, 7.5 15.5 Z" />
      {/* Internal Cloth Crease Line */}
      <path d="M 12 11.5 C 13.5 10, 15 10.5, 17 8.5" />
    </svg>
  );
};

export default PenaltyFlagIcon;
