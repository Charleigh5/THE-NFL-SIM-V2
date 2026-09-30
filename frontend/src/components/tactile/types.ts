import type React from "react";
import type { MotionStyle, HTMLMotionProps } from "framer-motion";

export type TactileState =
  | "idle"
  | "hover"
  | "pressed"
  | "focused"
  | "dragging"
  | "drop-target"
  | "selected"
  | "disabled"
  | "loading"
  | "success"
  | "warning"
  | "error";

export interface TactileTiltOptions {
  /** Maximum tilt angle in degrees (default: 10) */
  maxTilt?: number;
  /** Enable Web Audio haptic clicks (default: true) */
  enableHaptics?: boolean;
  /** Angular threshold in degrees to trigger haptic detent tick (default: 4.5) */
  tiltThreshold?: number;
  /** Suppress 3D tilt interactions (default: false) */
  disabled?: boolean;
  /** Scale factor during active hover (default: 1) */
  scale?: number;
}

export interface TactileTiltResult {
  ref: React.RefObject<HTMLDivElement | null>;
  style: MotionStyle;
  handlers: {
    onPointerMove: (e: React.PointerEvent<HTMLDivElement>) => void;
    onPointerEnter: () => void;
    onPointerLeave: () => void;
    onPointerDown: () => void;
    onPointerUp: () => void;
  };
  isTilting: boolean;
}

export type TactileElevation = "flat" | "raised" | "floating";

export interface TactileCardProps extends Omit<HTMLMotionProps<"div">, "ref" | "children"> {
  state?: TactileState;
  maxTilt?: number;
  enableHaptics?: boolean;
  elevation?: TactileElevation;
  children?: React.ReactNode;
  testId?: string;
  onAction?: () => void;
  disabled?: boolean;
  selected?: boolean;
}

export interface TactileStateConfig {
  classes: string;
  border: string;
  shadow: string;
  ariaProps: {
    role?: string;
    "aria-pressed"?: boolean;
    "aria-selected"?: boolean;
    "aria-disabled"?: boolean;
    "aria-busy"?: boolean;
    "aria-invalid"?: boolean;
    "aria-dropeffect"?: "none" | "copy" | "execute" | "link" | "move" | "popup";
    "aria-grabbed"?: boolean;
    "aria-live"?: "off" | "assertive" | "polite";
  };
}
