import React, { useState, useCallback } from "react";
import { motion } from "framer-motion";
import clsx from "clsx";
import { useTactileTilt } from "./useTactileTilt";
import type { TactileCardProps, TactileState } from "./types";

const STATE_STYLES: Record<TactileState, string> = {
  idle: "border border-white/15 bg-slate-950 text-white shadow-[2px_2px_0px_#000000]",
  hover:
    "border border-[#00A8FF]/80 bg-slate-900/95 text-white shadow-[4px_4px_0px_rgba(0,168,255,0.4)] -translate-y-0.5",
  pressed:
    "border-2 border-[#00A8FF] bg-slate-900 text-white shadow-[1px_1px_0px_#000000] translate-x-[2px] translate-y-[2px]",
  focused:
    "border border-[#00A8FF] bg-slate-900 text-white ring-2 ring-[#00A8FF] ring-offset-2 ring-offset-black shadow-[3px_3px_0px_#00A8FF] outline-none",
  dragging:
    "border-2 border-cyan-400 bg-slate-900/90 text-white scale-[1.03] z-50 shadow-[4px_4px_0px_#000000] opacity-90 cursor-grabbing",
  "drop-target":
    "border-2 border-dashed border-cyan-400 bg-cyan-950/40 text-white shadow-[3px_3px_0px_#000000] animate-pulse",
  selected:
    "border-2 border-cyan-400 bg-gradient-to-b from-[#0a1628] to-[#040810] text-white shadow-[3px_3px_0px_var(--theme-primary,#0076B6)]",
  disabled:
    "border border-white/5 bg-slate-950/60 text-zinc-400 opacity-40 grayscale cursor-not-allowed shadow-none",
  loading:
    "border border-white/10 bg-slate-900/80 text-white cursor-wait shadow-[2px_2px_0px_#000000]",
  success: "border border-emerald-500 bg-emerald-950/30 text-white shadow-[3px_3px_0px_#10B981]",
  warning: "border border-amber-500/80 bg-amber-950/30 text-white shadow-[3px_3px_0px_#F59E0B]",
  error: "border-2 border-red-500 bg-red-950/30 text-white shadow-[3px_3px_0px_#F43F5E]",
};

/**
 * 12-State Interactive Tactile Matrix Card Container
 * Enforces strict 0-4px corner radius (`rounded-[2px]`), directional zero-blur hard shadows,
 * 3D pointer perspective tilt, specular sheen reflection, and synthesized Web Audio haptics.
 */
export const TactileCard: React.FC<TactileCardProps> = ({
  state = "idle",
  maxTilt = 10,
  enableHaptics = true,
  elevation = "raised",
  children,
  className,
  onClick,
  onAction,
  testId = "tactile-card",
  disabled = false,
  selected = false,
  onPointerDown,
  onPointerUp,
  onFocus,
  onBlur,
  onKeyDown,
  ...props
}) => {
  const [isPressed, setIsPressed] = useState<boolean>(false);
  const [isFocused, setIsFocused] = useState<boolean>(false);
  const [isHovered, setIsHovered] = useState<boolean>(false);

  const isCardDisabled = disabled || state === "disabled" || state === "loading";
  const isCardSelected = selected || state === "selected";

  const { ref, style, handlers } = useTactileTilt({
    maxTilt,
    enableHaptics: enableHaptics && !isCardDisabled,
    disabled: isCardDisabled,
  });

  // Determine computed active state from interaction matrix
  let computedState: TactileState = state;
  if (isCardDisabled) {
    computedState = state === "loading" ? "loading" : "disabled";
  } else if (state === "dragging") {
    computedState = "dragging";
  } else if (state === "drop-target") {
    computedState = "drop-target";
  } else if (isPressed) {
    computedState = "pressed";
  } else if (isFocused) {
    computedState = "focused";
  } else if (isCardSelected) {
    computedState = "selected";
  } else if (isHovered && state === "idle") {
    computedState = "hover";
  }

  const handlePointerDown = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      if (isCardDisabled) return;
      setIsPressed(true);
      handlers.onPointerDown();
      onPointerDown?.(e);
    },
    [isCardDisabled, handlers, onPointerDown]
  );

  const handlePointerUp = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      if (isCardDisabled) return;
      setIsPressed(false);
      handlers.onPointerUp();
      onPointerUp?.(e);
    },
    [isCardDisabled, handlers, onPointerUp]
  );

  const handlePointerEnter = useCallback(() => {
    if (isCardDisabled) return;
    setIsHovered(true);
    handlers.onPointerEnter();
  }, [isCardDisabled, handlers]);

  const handlePointerLeave = useCallback(() => {
    setIsHovered(false);
    setIsPressed(false);
    handlers.onPointerLeave();
  }, [handlers]);

  const handleFocus = useCallback(
    (e: React.FocusEvent<HTMLDivElement>) => {
      if (isCardDisabled) return;
      setIsFocused(true);
      onFocus?.(e);
    },
    [isCardDisabled, onFocus]
  );

  const handleBlur = useCallback(
    (e: React.FocusEvent<HTMLDivElement>) => {
      setIsFocused(false);
      onBlur?.(e);
    },
    [onBlur]
  );

  const handleClick = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (isCardDisabled) {
        e.preventDefault();
        return;
      }
      onAction?.();
      onClick?.(e);
    },
    [isCardDisabled, onAction, onClick]
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLDivElement>) => {
      if (isCardDisabled) return;
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        onAction?.();
        onClick?.(e as unknown as React.MouseEvent<HTMLDivElement>);
      }
      onKeyDown?.(e);
    },
    [isCardDisabled, onAction, onClick, onKeyDown]
  );

  // Elevation modifier classes
  const elevationClass =
    elevation === "floating" ? "shadow-hard-lg" : elevation === "flat" ? "shadow-hard-xs" : "";

  return (
    <motion.div
      ref={ref}
      data-testid={testId}
      data-tactile-state={computedState}
      tabIndex={isCardDisabled ? -1 : 0}
      role={props.role || "button"}
      aria-disabled={isCardDisabled}
      aria-selected={isCardSelected}
      aria-busy={state === "loading"}
      aria-pressed={isPressed}
      aria-invalid={state === "error"}
      aria-live={state === "warning" || state === "error" ? "assertive" : "off"}
      style={style}
      className={clsx(
        "group relative rounded-[2px] transition-colors duration-150 select-none overflow-hidden",
        STATE_STYLES[computedState],
        elevationClass,
        className
      )}
      onPointerMove={handlers.onPointerMove}
      onPointerEnter={handlePointerEnter}
      onPointerLeave={handlePointerLeave}
      onPointerDown={handlePointerDown}
      onPointerUp={handlePointerUp}
      onFocus={handleFocus}
      onBlur={handleBlur}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      {...props}
    >
      {/* Specular Sheen Light Reflection Overlay */}
      <div
        className="absolute inset-0 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-150 z-20"
        style={{
          background:
            "radial-gradient(420px circle at var(--mx, 50%) var(--my, 50%), rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.04) 35%, transparent 65%)",
          mixBlendMode: "overlay",
        }}
      />

      {/* Machined Top Edge Inset Highlight */}
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/25 to-transparent pointer-events-none z-20" />

      {/* Loading Radar Sweep Line */}
      {computedState === "loading" && (
        <div
          className="absolute inset-0 pointer-events-none z-20 bg-gradient-to-b from-transparent via-cyan-400/20 to-transparent animate-pulse"
          style={{ animationDuration: "1.2s" }}
        />
      )}

      {/* Elevated 3D Children Content Plane */}
      <div
        className="relative z-10 w-full h-full"
        style={{ transform: "translateZ(8px)", transformStyle: "preserve-3d" }}
      >
        {children}
      </div>
    </motion.div>
  );
};
