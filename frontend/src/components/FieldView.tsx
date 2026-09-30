// FieldView: Static formation diagram for Phase 1 (I-Form vs 4-3)
// import { useSimulationStore } from "../store/useSimulationStore"; // Unused in static view
import { GameCanvas } from "./game/GameCanvas";
import { PlayerSprite } from "./game/PlayerSprite";

export const FieldView = () => {
  // For Phase 1, we just render static placeholders.
  // In Phase 2, we will use gameState.playContext to position them.

  // Example Formation: I-Form vs 4-3
  // 1 yard = 10 px.
  // X = 20 yards (200px) for LOS.
  // Y = Middle (53.3 / 2 approx 26 yards -> 266px)

  const losX = 200;
  const centerY = 266;

  return (
    <div className="w-full overflow-x-auto">
      <GameCanvas width={1200} height={533}>
        {/* OFFENSE (Red) - Moving Right */}
        {/* C */}
        <PlayerSprite x={losX} y={centerY} color={0xff0000} isOffense />
        {/* QB */}
        <PlayerSprite x={losX - 20} y={centerY} color={0xff0000} isOffense />
        {/* HB */}
        <PlayerSprite x={losX - 50} y={centerY} color={0xff0000} isOffense />
        {/* FB */}
        <PlayerSprite x={losX - 35} y={centerY} color={0xff0000} isOffense />
        {/* LT */}
        <PlayerSprite x={losX} y={centerY - 20} color={0xff0000} isOffense />
        {/* LG */}
        <PlayerSprite x={losX} y={centerY - 10} color={0xff0000} isOffense />
        {/* RG */}
        <PlayerSprite x={losX} y={centerY + 10} color={0xff0000} isOffense />
        {/* RT */}
        <PlayerSprite x={losX} y={centerY + 20} color={0xff0000} isOffense />
        {/* TE */}
        <PlayerSprite x={losX} y={centerY + 30} color={0xff0000} isOffense />
        {/* WR1 (Top) */}
        <PlayerSprite x={losX} y={centerY - 150} color={0xff0000} isOffense />
        {/* WR2 (Bottom) */}
        <PlayerSprite x={losX} y={centerY + 150} color={0xff0000} isOffense />

        {/* DEFENSE (Blue) - Moving Left */}
        {/* DT1 */}
        <PlayerSprite x={losX + 15} y={centerY - 5} color={0x0000ff} />
        {/* DT2 */}
        <PlayerSprite x={losX + 15} y={centerY + 5} color={0x0000ff} />
        {/* DE1 */}
        <PlayerSprite x={losX + 15} y={centerY - 25} color={0x0000ff} />
        {/* DE2 */}
        <PlayerSprite x={losX + 15} y={centerY + 25} color={0x0000ff} />
        {/* MLB */}
        <PlayerSprite x={losX + 50} y={centerY} color={0x0000ff} />
        {/* OLB1 */}
        <PlayerSprite x={losX + 50} y={centerY - 40} color={0x0000ff} />
        {/* OLB2 */}
        <PlayerSprite x={losX + 50} y={centerY + 40} color={0x0000ff} />
        {/* CB1 */}
        <PlayerSprite x={losX + 50} y={centerY - 150} color={0x0000ff} />
        {/* CB2 */}
        <PlayerSprite x={losX + 50} y={centerY + 150} color={0x0000ff} />
        {/* FS */}
        <PlayerSprite x={losX + 120} y={centerY - 20} color={0x0000ff} />
        {/* SS */}
        <PlayerSprite x={losX + 120} y={centerY + 20} color={0x0000ff} />
      </GameCanvas>
    </div>
  );
};
