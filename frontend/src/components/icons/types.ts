import type React from "react";

export type GridironIconName =
  | "football_laces"
  | "yard_hashes"
  | "goalposts"
  | "chain_gang"
  | "referee_whistle"
  | "penalty_flag"
  | "blitz_bolt"
  | "play_clock"
  | "lombardi_trophy"
  | "chalkboard_route"
  | "helmet"
  | "down_marker";

export type IconSizePreset = "xs" | "sm" | "md" | "lg" | "xl";

export type IconSize = number | IconSizePreset | string;

export interface IconBaseProps extends React.SVGProps<SVGSVGElement> {
  size?: IconSize;
  strokeWidth?: number;
  className?: string;
  title?: string;
  color?: string;
}

export interface GridironIconProps extends IconBaseProps {
  name: GridironIconName;
}

/**
 * Resolves numeric pixel dimensions from preset strings or numbers.
 */
export const resolveIconSize = (size?: IconSize): number | string => {
  if (typeof size === "number") return size;
  if (typeof size === "string") {
    switch (size) {
      case "xs":
        return 12;
      case "sm":
        return 16;
      case "md":
        return 20;
      case "lg":
        return 24;
      case "xl":
        return 32;
      default:
        return size;
    }
  }
  return 24;
};
