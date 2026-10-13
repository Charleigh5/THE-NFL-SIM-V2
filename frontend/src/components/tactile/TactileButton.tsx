import React, { useState, useCallback, useMemo } from "react";
import clsx from "clsx";
import { soundEffects } from "../../services/soundEffects";
import type {
  TactileButtonProps,
  TactileButtonVariant,
  TactileButtonSize,
  TactileState,
} from "./types";

const VARIANT_BASE_STYLES: Record<TactileButtonVariant, string> = {
  primary:
    "bg-gradient-to-b from-[#005187] to-[#0076B6] text-white border border-cyan-400/40 shadow-hard-sm hover:border-cyan-300 hover:shadow-hard-primary",
  secondary:
    "bg-slate-900 text-slate-100 border border-white/15 shadow-hard-sm hover:border-slate-400 hover:bg-slate-800 hover:shadow-hard-md",
  tactical:
    "bg-gradient-to-b from-[#06101c] via-[#040912] to-[#020509] text-cyan-300 border border-cyan-500/40 shadow-hard-sm hover:border-cyan-400 hover:text-white hover:shadow-hard-primary",
  danger:
    "bg-gradient-to-b from-rose-900/80 to-rose-950 text-rose-200 border border-rose-500/50 shadow-hard-sm hover:border-rose-400 hover:shadow-hard-rose",
  warning:
    "bg-gradient-to-b from-amber-900/80 to-amber-950 text-amber-200 border border-amber-500/50 shadow-hard-sm hover:border-amber-400 hover:shadow-hard-amber",
  success:
    "bg-gradient-to-b from-emerald-900/80 to-emerald-950 text-emerald-200 border border-emerald-500/50 shadow-hard-sm hover:border-emerald-400 hover:shadow-hard-emerald",
  ghost:
    "bg-transparent text-gray-300 border border-transparent shadow-none hover:border-white/20 hover:bg-white/5 hover:text-white hover:shadow-hard-xs",
};

const SIZE_STYLES: Record<TactileButtonSize, string> = {
  xs: "h-6 px-2 text-[10px] gap-1 font-mono tracking-wider",
  sm: "h-8 px-2.5 text-xs gap-1.5 font-mono tracking-wider",
  md: "h-9 px-3.5 text-sm gap-2 font-mono tracking-wider",
  lg: "h-11 px-5 text-base gap-2.5 font-mono tracking-wider",
};

const STATE_STYLES: Record<TactileState, string> = {
  idle: "",
  hover: "-translate-y-0.5 shadow-hard-md",
  pressed: "translate-x-[1px] translate-y-[1px] shadow-hard-pressed",
  focused: "ring-2 ring-cyan-400 ring-offset-2 ring-offset-black outline-none shadow-hard-primary",
  dragging: "scale-[1.04] opacity-90 cursor-grabbing z-50 shadow-hard-lg border-2 border-cyan-400",
  "drop-target":
    "border-2 border-dashed border-cyan-400 bg-cyan-950/60 text-cyan-300 shadow-hard-sm animate-pulse",
  selected:
    "border-2 border-cyan-400 bg-gradient-to-b from-[#0a1b30] to-[#040810] text-cyan-200 shadow-hard-primary",
  disabled:
    "opacity-40 grayscale cursor-not-allowed pointer-events-none shadow-none border-white/5 bg-slate-950/60 text-zinc-500",
  loading:
    "cursor-wait opacity-90 pointer-events-none border border-cyan-400/50 bg-slate-900/90 text-cyan-300 shadow-hard-sm",
  success: "border border-emerald-500 bg-emerald-950/40 text-emerald-300 shadow-hard-emerald",
  warning: "border border-amber-500 bg-amber-950/40 text-amber-300 shadow-hard-amber",
  error: "border-2 border-rose-500 bg-rose-950/40 text-rose-300 shadow-hard-rose",
};

/**
 * 12-State Interactive Matrix Tactile Button Component
 * Strictly adheres to the Anti-Template Firewall:
 * - Corner radius 0-4px ceiling (`rounded-[2px]`)
 * - Directional zero-blur hard shadows (`--shadow-hard-md: 3px 3px 0px #000000`, pressed: `1px 1px 0px #000000`)
 * - Machined top edge highlight
 * - Complete 12-state interactive coverage:
 *   idle, hover, pressed, focused, dragging, drop-target, selected, disabled, loading, success, warning, error
 * - Web Audio dual-tone mechanical actuation snap haptics
 */
export const TactileButton: React.FC<TactileButtonProps> = ({
  variant = "primary",
  size = "md",
  state,
  disabled = false,
  selected = false,
  loading = false,
  icon,
  iconRight,
  badge,
  testId = "tactile-button",
  enableHaptics = true,
  fullWidth = false,
  children,
  className,
  onClick,
  onPointerDown,
  onPointerUp,
  onPointerEnter,
  onPointerLeave,
  onFocus,
  onBlur,
  type = "button",
  ...props
}) => {
  const [isPressed, setIsPressed] = useState<boolean>(false);
  const [isFocused, setIsFocused] = useState<boolean>(false);
  const [isHovered, setIsHovered] = useState<boolean>(false);

  const isButtonDisabled = disabled || state === "disabled";
  const isButtonLoading = loading || state === "loading";
  const isButtonSelected = selected || state === "selected";
  const isLockedOut = isButtonDisabled || isButtonLoading;

  // Resolve computed active state across the 12-state interactive matrix
  const computedState: TactileState = useMemo(() => {
    if (isButtonDisabled) return "disabled";
    if (isButtonLoading) return "loading";
    if (state === "dragging") return "dragging";
    if (state === "drop-target") return "drop-target";
    if (state === "success") return "success";
    if (state === "warning") return "warning";
    if (state === "error") return "error";
    if (isPressed || state === "pressed") return "pressed";
    if (isFocused || state === "focused") return "focused";
    if (isButtonSelected) return "selected";
    if (isHovered || state === "hover") return "hover";
    return state || "idle";
  }, [isButtonDisabled, isButtonLoading, isPressed, isFocused, isButtonSelected, isHovered, state]);

  const handlePointerDown = useCallback(
    (e: React.PointerEvent<HTMLButtonElement>) => {
      if (isLockedOut) return;
      setIsPressed(true);
      if (enableHaptics) {
        soundEffects.playCardPress();
      }
      onPointerDown?.(e);
    },
    [isLockedOut, enableHaptics, onPointerDown]
  );

  const handlePointerUp = useCallback(
    (e: React.PointerEvent<HTMLButtonElement>) => {
      if (isLockedOut) return;
      setIsPressed(false);
      if (enableHaptics) {
        soundEffects.playCardRelease();
      }
      onPointerUp?.(e);
    },
    [isLockedOut, enableHaptics, onPointerUp]
  );

  const handlePointerEnter = useCallback(
    (e: React.PointerEvent<HTMLButtonElement>) => {
      if (isLockedOut) return;
      setIsHovered(true);
      onPointerEnter?.(e);
    },
    [isLockedOut, onPointerEnter]
  );

  const handlePointerLeave = useCallback(
    (e: React.PointerEvent<HTMLButtonElement>) => {
      setIsHovered(false);
      setIsPressed(false);
      onPointerLeave?.(e);
    },
    [onPointerLeave]
  );

  const handleFocus = useCallback(
    (e: React.FocusEvent<HTMLButtonElement>) => {
      if (isLockedOut) return;
      setIsFocused(true);
      onFocus?.(e);
    },
    [isLockedOut, onFocus]
  );

  const handleBlur = useCallback(
    (e: React.FocusEvent<HTMLButtonElement>) => {
      setIsFocused(false);
      onBlur?.(e);
    },
    [onBlur]
  );

  const handleClick = useCallback(
    (e: React.MouseEvent<HTMLButtonElement>) => {
      if (isLockedOut) {
        e.preventDefault();
        return;
      }
      onClick?.(e);
    },
    [isLockedOut, onClick]
  );

  return (
    <button
      type={type}
      data-testid={testId}
      data-tactile-state={computedState}
      disabled={isButtonDisabled}
      aria-disabled={isButtonDisabled}
      aria-busy={isButtonLoading}
      aria-pressed={isPressed || state === "pressed"}
      aria-selected={isButtonSelected}
      aria-invalid={computedState === "error"}
      aria-grabbed={computedState === "dragging" ? true : undefined}
      aria-dropeffect={computedState === "drop-target" ? "move" : props["aria-dropeffect"]}
      aria-live={
        computedState === "warning" || computedState === "error"
          ? "assertive"
          : computedState === "success"
            ? "polite"
            : "off"
      }
      className={clsx(
        "group relative inline-flex items-center justify-center rounded-[2px] transition-all duration-100 uppercase select-none font-semibold cursor-pointer overflow-hidden",
        VARIANT_BASE_STYLES[variant],
        SIZE_STYLES[size],
        STATE_STYLES[computedState],
        fullWidth && "w-full",
        className
      )}
      onClick={handleClick}
      onPointerDown={handlePointerDown}
      onPointerUp={handlePointerUp}
      onPointerEnter={handlePointerEnter}
      onPointerLeave={handlePointerLeave}
      onFocus={handleFocus}
      onBlur={handleBlur}
      {...props}
    >
      {/* Machined Top Edge Inset Highlight */}
      <span className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none z-10" />

      {/* Specular Sheen Shimmer on Hover */}
      {computedState === "hover" && (
        <span
          className="absolute inset-0 pointer-events-none opacity-40 z-10"
          style={{
            background: "linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 60%)",
          }}
        />
      )}

      {/* Selected Indicator Light */}
      {computedState === "selected" && (
        <span className="w-1.5 h-1.5 rounded-[1px] bg-cyan-400 shadow-hard-xs animate-pulse mr-1" />
      )}

      {/* Loading Radar Sweep Indicator */}
      {computedState === "loading" && (
        <span
          className="relative w-3.5 h-3.5 flex-shrink-0 inline-flex items-center justify-center mr-1"
          aria-hidden="true"
        >
          <span className="absolute inset-0 rounded-full animate-spin border border-cyan-400/30 border-t-cyan-300" />
          <span className="w-1 h-1 rounded-[1px] bg-cyan-400 animate-pulse" />
        </span>
      )}

      {/* Left Icon */}
      {icon && computedState !== "loading" && (
        <span className="inline-flex shrink-0 items-center justify-center z-10">{icon}</span>
      )}

      {/* Main Content */}
      <span className="relative z-10 inline-flex items-center truncate">{children}</span>

      {/* Right Icon */}
      {iconRight && (
        <span className="inline-flex shrink-0 items-center justify-center z-10">{iconRight}</span>
      )}

      {/* Tactical Badge / Numerical Count */}
      {badge !== undefined && (
        <span className="ml-1.5 px-1 py-0.2 rounded-[2px] bg-black/60 border border-white/20 text-[10px] font-mono font-bold tracking-tight text-white shadow-hard-xs z-10">
          {badge}
        </span>
      )}
    </button>
  );
};
