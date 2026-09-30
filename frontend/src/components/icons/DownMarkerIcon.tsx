import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * DownMarkerIcon
 * Represents the official sideline chain crew down box indicator:
 * Rectangular down box head displaying bold stencil numeral "4",
 * vertical padded support pole, and ground stabilization footplate.
 */
export const DownMarkerIcon: React.FC<IconBaseProps> = ({
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
      {/* Down Box Scoreboard Head */}
      <rect x="4.5" y="3" width="15" height="12" rx="2" />
      {/* Stencil Numeral "4" (4th Down Marker) */}
      <path d="M 10.5 5.5 L 8 9.5 H 13.5 M 12.5 5.5 V 12.5" />
      {/* Padded Sideline Ground Pole */}
      <path d="M 12 15 V 21" />
      {/* Ground Footplate */}
      <path d="M 9 21 H 15" />
    </svg>
  );
};

export default DownMarkerIcon;
