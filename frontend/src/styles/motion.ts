import type { Transition, Variants } from "framer-motion";

/**
 * Centralized motion tokens.
 *
 * Goals:
 * - consistent timing/easing across the app
 * - easy reduced-motion overrides
 * - avoid one-off transitions sprinkled everywhere
 */

export const ease = {
  out: [0.22, 1, 0.36, 1] as const,
  inOut: [0.65, 0, 0.35, 1] as const,
  smooth: [0.25, 0.46, 0.45, 0.94] as const,
};

export const t = {
  fast: { duration: 0.16, ease: ease.out } satisfies Transition,
  med: { duration: 0.32, ease: ease.out } satisfies Transition,
  slow: { duration: 0.9, ease: ease.out } satisfies Transition,
  springTactile: {
    type: "spring",
    stiffness: 420,
    damping: 32,
    mass: 0.8,
  } satisfies Transition,
};

// Default route transition (fade + blur + slight Y movement)
export const routeVariants: Variants = {
  initial: { opacity: 0, y: 18, filter: "blur(8px)" },
  animate: { opacity: 1, y: 0, filter: "blur(0px)", transition: t.med },
  exit: { opacity: 0, y: -12, filter: "blur(6px)", transition: t.fast },
};

// Simple fade up animation
export const fadeUp: Variants = {
  initial: { opacity: 0, y: 14 },
  animate: { opacity: 1, y: 0, transition: t.med },
};

// Slide from right (for drill-down navigation)
export const slideFromRight: Variants = {
  initial: { opacity: 0, x: 60 },
  animate: { opacity: 1, x: 0, transition: { duration: 0.4, ease: ease.smooth } },
  exit: { opacity: 0, x: -40, transition: t.fast },
};

// Slide from left (for back navigation)
export const slideFromLeft: Variants = {
  initial: { opacity: 0, x: -60 },
  animate: { opacity: 1, x: 0, transition: { duration: 0.4, ease: ease.smooth } },
  exit: { opacity: 0, x: 40, transition: t.fast },
};

// Scale transition (for modal-like pages)
export const scaleTransition: Variants = {
  initial: { opacity: 0, scale: 0.95 },
  animate: { opacity: 1, scale: 1, transition: { duration: 0.35, ease: ease.out } },
  exit: { opacity: 0, scale: 0.98, transition: t.fast },
};

// Stagger container for pages with many children
export const staggerContainer: Variants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
      when: "beforeChildren",
    },
  },
  exit: { opacity: 0 },
};

// Stagger child item
export const staggerItem: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: ease.smooth },
  },
};

// Card hover/tap effects
export const cardHover: Variants = {
  initial: { scale: 1 },
  hover: { scale: 1.02, transition: t.fast },
  tap: { scale: 0.98, transition: t.fast },
};

// List item animations
export const listItem: Variants = {
  initial: { opacity: 0, x: -10 },
  animate: { opacity: 1, x: 0, transition: t.med },
  exit: { opacity: 0, x: 10, transition: t.fast },
};
