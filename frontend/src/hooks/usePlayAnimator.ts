import { useEffect, useState } from "react";
import { useSimulationStore } from "../store/useSimulationStore";

/**
 * Hook to track animation state based on play log updates
 * Returns isAnimating state that becomes true when new plays are added
 */
export const usePlayAnimator = () => {
  const { playLog } = useSimulationStore();
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (playLog.length === 0) {
      return;
    }

    // Start animation asynchronously to avoid cascading renders
    const startTimer = setTimeout(() => setIsAnimating(true), 0);

    // Animation completes after a delay
    const endTimer = setTimeout(() => setIsAnimating(false), 3000);

    return () => {
      clearTimeout(startTimer);
      clearTimeout(endTimer);
    };
  }, [playLog.length]);

  return { isAnimating };
};
