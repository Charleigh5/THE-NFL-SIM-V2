import React from "react";
import { type IconBaseProps, resolveIconSize } from "./types";

/**
 * PlayClockIcon
 * Represents the stadium digital 40-second play clock:
 * Beveled scoreboard housing with mounting rivets, and crisp
 * digital 7-segment/stencil numerals "40".
 */
export const PlayClockIcon: React.FC<IconBaseProps> = ({
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
      {/* Outer Scoreboard Bezel */}
      <rect x="2.5" y="4" width="19" height="16" rx="2.5" />
      {/* Corner Fastener Rivets */}
      <path d="M 4.5 6.5 H 4.51" />
      <path d="M 19.5 6.5 H 19.51" />
      {/* Stencil Digit "4" */}
      <path d="M 7.5 8 L 7.5 12.5 H 10.5 M 10.5 8 V 16" />
      {/* Stencil Digit "0" */}
      <rect x="13" y="8" width="4.5" height="8" rx="1.5" />
    </svg>
  );
};

export default PlayClockIcon;
