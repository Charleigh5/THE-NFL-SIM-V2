import React, { useCallback, useRef } from "react";
import { useTick } from "@pixi/react";
import type { Graphics as PixiGraphics } from "pixi.js";
import { Graphics } from "pixi.js";

// We assume 'extend' was called in the parent or app root.
// If needed, we can call it here too, but duplicate calls might be safe or warned.
// To be safe, we won't call it here but assume <pixiGraphics> handles it.

interface PlayerSpriteProps {
  /** Player ID - required for dynamic position updates via dataSource */
  id?: number;
  /** Static X position (used when dataSource not provided) */
  x: number;
  /** Static Y position (used when dataSource not provided) */
  y: number;
  /** Fill color for the player sprite */
  color: number;
  /** Whether player is on offense (affects direction indicator) */
  isOffense?: boolean;
  /** Dynamic position source - when provided with id, sprite updates position from this ref */
  dataSource?: React.MutableRefObject<Map<number, { x: number; y: number }>>;
}

export const PlayerSprite: React.FC<PlayerSpriteProps> = ({
  id,
  x,
  y,
  color,
  isOffense,
  dataSource,
}) => {
  const spriteRef = useRef<PixiGraphics>(null);

  // Dynamic position updates - only active when both id and dataSource are provided
  useTick(() => {
    if (id !== undefined && dataSource?.current && spriteRef.current) {
      const pos = dataSource.current.get(id);
      if (pos) {
        spriteRef.current.position.set(pos.x, pos.y);
      }
    }
  });

  const draw = useCallback(
    (g: Graphics) => {
      g.clear();

      // Shadow
      g.circle(0, 2, 8);
      g.fill({ color: 0x000000, alpha: 0.3 }); // checking pixi v8 docs: g.fill({ color, alpha }) is standard.

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

  return <pixiGraphics ref={spriteRef} draw={draw} x={x} y={y} />;
};
