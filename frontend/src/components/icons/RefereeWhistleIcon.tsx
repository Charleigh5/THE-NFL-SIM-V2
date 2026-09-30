import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * RefereeWhistleIcon
 * Represents the Fox 40 referee pea-whistle:
 * Cylindrical pea chamber, top lanyard ring eyelet,
 * air exhaust vent port, and horizontal mouthpiece barrel.
 */
export const RefereeWhistleIcon: React.FC<IconBaseProps> = ({
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
      {/* Lanyard Eyelet Loop */}
      <circle cx="5" cy="8.5" r="2" />
      {/* Pea Chamber Resonant Body */}
      <path d="M 9 9 C 5.5 9, 3 11.5, 3 15 C 3 18.5, 5.5 21, 9 21 C 12 21, 14.5 19, 15 16" />
      {/* Mouthpiece Barrel & Taper */}
      <path d="M 14 16 L 21 16 L 21 12 L 12 12" />
      {/* Exhaust Sound Vent Port */}
      <path d="M 12 12 L 12 9.5 L 14 9.5 L 14 12" />
    </svg>
  );
};

export default RefereeWhistleIcon;
