import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * FootballLacesIcon
 * Represents regulation NFL Wilson "The Duke" pro game ball:
 * 45-degree angled prolate spheroid silhouette, central longitudinal seam,
 * perpendicular cross-stitch laces, knot caps, and twin stripe arcs.
 */
export const FootballLacesIcon: React.FC<IconBaseProps> = ({
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
      {/* Prolate Spheroid Outer Silhouette */}
      <path d="M 3.2 20.8 C 1.8 13.5, 10.5 1.8, 20.8 3.2 C 22.2 10.5, 13.5 22.2, 3.2 20.8 Z" />
      {/* Center Longitudinal Seam */}
      <path d="M 7.5 16.5 L 16.5 7.5" />
      {/* Perpendicular Cross-Stitch Laces */}
      <path d="M 8.5 12.5 L 11.5 15.5" />
      <path d="M 10.5 10.5 L 13.5 13.5" />
      <path d="M 12.5 8.5 L 15.5 11.5" />
      {/* Terminating Knot Caps */}
      <path d="M 7 16 L 8 17" />
      <path d="M 16 7 L 17 8" />
      {/* White Tip Stripes */}
      <path d="M 4.5 16.5 C 6 16, 7 17, 7.5 19.5" />
      <path d="M 16.5 4.5 C 17 6, 18 7, 19.5 7.5" />
    </svg>
  );
};

export default FootballLacesIcon;
