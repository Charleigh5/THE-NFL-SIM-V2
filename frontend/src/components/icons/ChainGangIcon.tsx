import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * ChainGangIcon
 * Represents the official 10-yard sideline measurement chain crew markers:
 * Dual indicator poles with bullseye target discs, ground support plates,
 * taut 10-yard connecting chain, and center 5-yard clip marker.
 */
export const ChainGangIcon: React.FC<IconBaseProps> = ({
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
      {/* Left Indicator Disc Target */}
      <circle cx="5" cy="4" r="2.5" />
      <circle cx="5" cy="4" r="0.75" />
      {/* Left Vertical Rod & Footer */}
      <path d="M 5 6.5 L 5 21" />
      <path d="M 3.5 21 L 6.5 21" />
      {/* Right Indicator Disc Target */}
      <circle cx="19" cy="4" r="2.5" />
      <circle cx="19" cy="4" r="0.75" />
      {/* Right Vertical Rod & Footer */}
      <path d="M 19 6.5 L 19 21" />
      <path d="M 17.5 21 L 20.5 21" />
      {/* Connecting 10-Yard Ground Chain */}
      <path d="M 5 19 L 19 19" />
      {/* Center 5-Yard Clip Marker Diamond */}
      <path d="M 12 17 L 13.5 19 L 12 21 L 10.5 19 Z" />
    </svg>
  );
};

export default ChainGangIcon;
