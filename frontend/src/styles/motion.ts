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

export const routeVariants: Variants = {
  initial: { opacity: 0, y: 18, filter: "blur(8px)" },
  animate: { opacity: 1, y: 0, filter: "blur(0px)", transition: t.med },
  exit: { opacity: 0, y: -12, filter: "blur(6px)", transition: t.fast },
};

export const fadeUp: Variants = {
  initial: { opacity: 0, y: 14 },
  animate: { opacity: 1, y: 0, transition: t.med },
};
