import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * HelmetIcon
 * Represents the modern NFL Riddell SpeedFlex franchise helmet:
 * Aerodynamic polycarbonate cranial shell, ear hole cutout,
 * chinstrap attachment, and multi-bar protective titanium facemask.
 */
export const HelmetIcon: React.FC<IconBaseProps> = ({
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
      {/* Helmet Shell Cranial Dome */}
      <path d="M 12 3 C 6.5 3, 3 7, 3 12.5 C 3 16, 4.5 18.5, 7.5 19.5 L 9.5 16.5" />
      {/* Ear Hole Cutout */}
      <circle cx="9.5" cy="13.5" r="1.5" />
      {/* Chin Cup Strap */}
      <path d="M 9.5 16.5 L 13 20" />
      {/* Facemask Outer Profile */}
      <path d="M 13 12 H 21 L 20 16.5 H 13.5" />
      {/* Facemask Vertical & Horizontal Grid Bars */}
      <path d="M 17 12 V 16.5" />
      <path d="M 13 14.25 H 20.5" />
      {/* Crown Ridge Curve */}
      <path d="M 12 3 C 14.5 3, 17 5, 18 8" />
    </svg>
  );
};

export default HelmetIcon;
