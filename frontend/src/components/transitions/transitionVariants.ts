import type { Variants } from "framer-motion";

/**
 * Child item variants for use with StaggeredTransition
 */
export const staggerChildVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
};

// Page transition variants
export const pageVariants: Variants = {
  initial: {
    opacity: 0,
    y: 20,
    scale: 0.98,
  },
  enter: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      duration: 0.4,
      ease: [0.25, 0.46, 0.45, 0.94], // Custom easing
      when: "beforeChildren",
      staggerChildren: 0.1,
    },
  },
  exit: {
    opacity: 0,
    y: -20,
    scale: 0.98,
    transition: {
      duration: 0.3,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
};

// Slide from right variant
export const slideVariants: Variants = {
  initial: {
    opacity: 0,
    x: 60,
  },
  enter: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.5,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
  exit: {
    opacity: 0,
    x: -60,
    transition: {
      duration: 0.3,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
};

// Fade with blur variant
export const fadeBlurVariants: Variants = {
  initial: {
    opacity: 0,
    filter: "blur(10px)",
  },
  enter: {
    opacity: 1,
    filter: "blur(0px)",
    transition: {
      duration: 0.5,
      ease: "easeOut",
    },
  },
  exit: {
    opacity: 0,
    filter: "blur(10px)",
    transition: {
      duration: 0.3,
      ease: "easeIn",
    },
  },
};

// Export all variants for custom usage
export const transitionVariants = {
  page: pageVariants,
  slide: slideVariants,
  fadeBlur: fadeBlurVariants,
};
