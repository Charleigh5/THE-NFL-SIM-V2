import React from "react";
import { Application, extend } from "@pixi/react";
import { Container, Graphics, Text } from "pixi.js";

// Register components
extend({ Container, Graphics, Text });

// Constants
const YARDS_TO_PIXELS = 10;
const FIELD_LENGTH_YARDS = 120; // 100 + 2 endzones
const FIELD_WIDTH_YARDS = 53.3;
const FIELD_WIDTH_PX = FIELD_WIDTH_YARDS * YARDS_TO_PIXELS;
const FIELD_HEIGHT_PX = FIELD_LENGTH_YARDS * YARDS_TO_PIXELS;

// Colors
const COLOR_GRASS = 0x2e8b57;
const COLOR_LINES = 0xffffff;
const COLOR_ENDZONE_HOME = 0x00008b;
const COLOR_ENDZONE_AWAY = 0x8b0000;

interface GameCanvasProps {
  width?: number;
  height?: number;
  children?: React.ReactNode;
}

const FieldGraphics = () => {
  const drawField = (g: any) => {
    g.clear();
    // Draw Grass
    g.rect(0, 0, FIELD_WIDTH_PX, FIELD_HEIGHT_PX);
    g.fill(COLOR_GRASS);

    const SCALE = YARDS_TO_PIXELS;
    const W = FIELD_LENGTH_YARDS * SCALE;
    const H = FIELD_WIDTH_YARDS * SCALE;

    // Grass
    g.rect(0, 0, W, H);
    g.fill(COLOR_GRASS);

    // Endzones
    g.rect(0, 0, 10 * SCALE, H);
    g.fill(COLOR_ENDZONE_HOME);

    g.rect(110 * SCALE, 0, 10 * SCALE, H);
    g.fill(COLOR_ENDZONE_AWAY);

    // Yard Lines
    g.stroke({ width: 2, color: COLOR_LINES });
    for (let i = 10; i <= 110; i += 5) {
      const x = i * SCALE;
      g.moveTo(x, 0);
      g.lineTo(x, H);
      if (i % 10 === 0) {
        g.stroke({ width: 4, color: COLOR_LINES });
      } else {
        g.stroke({ width: 2, color: COLOR_LINES, alpha: 0.5 });
      }
    }
  };

  // @ts-ignore - Dynamic JSX type for Pixi
  return <pixiGraphics draw={drawField} />;
};

export const GameCanvas: React.FC<GameCanvasProps> = ({ width = 1200, height = 533, children }) => {
  return (
    <div
      style={{
        width: "100%",
        overflow: "hidden",
        border: "4px solid #444",
        borderRadius: "8px",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <Application width={width} height={height} backgroundColor={0x1a1a1a}>
        {/* @ts-ignore - Dynamic JSX type for Pixi */}
        <pixiContainer x={0} y={0}>
          <FieldGraphics />
          {children}
        </pixiContainer>
      </Application>
    </div>
  );
};
