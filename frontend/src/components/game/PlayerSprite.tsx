import React, { useCallback } from "react";
// We assume 'extend' was called in the parent or app root.
// If needed, we can call it here too, but duplicate calls might be safe or warned.
// To be safe, we won't call it here but assume <pixiGraphics> handles it.

interface PlayerSpriteProps {
  x: number;
  y: number;
  color: number;
  isOffense?: boolean;
}

export const PlayerSprite: React.FC<PlayerSpriteProps> = ({ x, y, color, isOffense }) => {
  const draw = useCallback(
    (g: any) => {
      g.clear();

      // Shadow
      g.circle(0, 2, 8);
      g.fill({ color: 0x000000, alpha: 0.3 }); // v8 syntax uses object for alpha sometimes? Or standard g.fill(color, alpha) might be deprecated.
      // checking pixi v8 docs: g.fill({ color, alpha }) is standard.

      // Body
      g.circle(0, 0, 8);
      g.fill(color);
      g.stroke({ width: 2, color: 0xffffff });

      // Direction Indicator
      g.beginPath();
      if (isOffense) {
        g.moveTo(6, -4);
        g.lineTo(10, 0);
        g.lineTo(6, 4);
      } else {
        g.moveTo(-6, -4);
        g.lineTo(-10, 0);
        g.lineTo(-6, 4);
      }
      g.stroke({ width: 2, color: 0xffffff });
    },
    [color, isOffense]
  );

  // @ts-ignore
  return <pixiGraphics draw={draw} x={x} y={y} />;
};
