import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * LombardiTrophyIcon
 * Represents the Tiffany & Co. Vince Lombardi Super Bowl Trophy:
 * Three-sided concave tapered base pylon with central facet ridge,
 * solid baseplate, and a regulation football perched atop at a 45-degree angle.
 */
export const LombardiTrophyIcon: React.FC<IconBaseProps> = ({
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
      {/* Heavy Base Plate */}
      <path d="M 5.5 22 L 18.5 22" />
      {/* Concave Trihedral Silver Pylon */}
      <path d="M 6.5 22 C 8 18, 9.5 14, 11 11 L 13 11 C 14.5 14, 16 18, 17.5 22 Z" />
      {/* Center Pylon Ridge */}
      <path d="M 12 11 L 12 22" />
      {/* Regulation Football Atop Pedestal (45-degree tilt) */}
      <path d="M 9 7.5 C 7.5 4, 11 2, 15 3.5 C 16.5 5, 17.5 8.5, 15 10.5 C 13 11.5, 10.5 10.5, 9 7.5 Z" />
      {/* Football Seam and Cross Lace */}
      <path d="M 11 5.5 L 13.5 8" />
      <path d="M 11.5 7.5 L 13 6" />
    </svg>
  );
};

export default LombardiTrophyIcon;
