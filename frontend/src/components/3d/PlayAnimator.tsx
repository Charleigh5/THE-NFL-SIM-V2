import { useCallback, useEffect, useState } from "react";
import { useSimulationStore } from "../../store/useSimulationStore";
import type { PlayResult } from "../../types/simulation";

interface PlayAnimatorProps {
  onAnimationComplete?: () => void;
}

/**
 * PlayAnimator component - manages play-by-play animation logic
 * Note: For a simpler hook-based approach, see hooks/usePlayAnimator.ts
 */
export const PlayAnimator = ({ onAnimationComplete }: PlayAnimatorProps) => {
  const { playLog, gameState } = useSimulationStore();
  const [isAnimating, setIsAnimating] = useState(false);

  const latestPlay = playLog[0]; // Most recent play

  const animatePassPlay = useCallback(async (startX: number, endX: number) => {
    // QB starts at line of scrimmage
    const qbPosition: [number, number, number] = [startX, 0, 0];

    // Receiver runs route
    const receiverEnd: [number, number, number] = [endX, 0, 5];

    // Update positions (simplified for MVP - just showing concept)
    // In a full implementation, this would update state frame-by-frame
    console.log("Animating pass from", qbPosition, "to", receiverEnd);

    // Wait for animation duration
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }, []);

  const animateRunPlay = useCallback(async (startX: number, endX: number) => {
    // Running back starts behind QB
    const rbStart: [number, number, number] = [startX - 3, 0, 0];
    const rbEnd: [number, number, number] = [endX, 0, 0];

    console.log("Animating run from", rbStart, "to", rbEnd);

    await new Promise((resolve) => setTimeout(resolve, 2000));
  }, []);

  const animateKickoff = useCallback(async (returnYards: number) => {
    console.log("Animating kickoff return for", returnYards, "yards");

    await new Promise((resolve) => setTimeout(resolve, 3000));
  }, []);

  const animatePlay = useCallback(
    async (play: PlayResult) => {
      setIsAnimating(true);

      // Convert yard line (0-100) to 3D position (-60 to +60)
      const yardTo3D = (yardLine: number) => {
        return (yardLine / 100) * 120 - 60;
      };

      const startX = yardTo3D(gameState.yardLine - play.yards_gained);
      const endX = yardTo3D(gameState.yardLine);

      // Simulate player movements based on play type
      if (play.description.includes("Pass")) {
        // Pass play animation
        await animatePassPlay(startX, endX);
      } else if (play.description.includes("Run")) {
        // Run play animation
        await animateRunPlay(startX, endX);
      } else if (play.description.includes("Kickoff")) {
        // Kickoff return animation
        await animateKickoff(play.yards_gained);
      }

      setIsAnimating(false);
      onAnimationComplete?.();
    },
    [
      gameState.yardLine,
      onAnimationComplete,
      animatePassPlay,
      animateRunPlay,
      animateKickoff,
    ]
  );

  useEffect(() => {
    if (!latestPlay) return;

    // Animate based on play type
    animatePlay(latestPlay);
  }, [latestPlay, animatePlay]);

  // Return animation state for rendering
  return { isAnimating };
};
