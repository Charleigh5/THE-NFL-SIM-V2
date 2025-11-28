import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { Text } from "@react-three/drei";
import * as THREE from "three";
import { PlayerCharacter } from "./PlayerCharacter";
import { useSimulationStore } from "../../store/useSimulationStore";
import { usePlayAnimator } from "../../hooks/usePlayAnimator";

export const FieldVisualizer = () => {
  const fieldRef = useRef<THREE.Group>(null);
  const { gameState } = useSimulationStore();
  const { isAnimating } = usePlayAnimator();

  // Simple animation loop (e.g., grass swaying or lights pulsing)
  useFrame(() => {
    if (fieldRef.current) {
      // fieldRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.1) * 0.05;
    }
  });

  // Convert yard line (0-100) to 3D X position
  const yardTo3D = (yardLine: number) => {
    return (yardLine / 100) * 120 - 60;
  };

  const losX = yardTo3D(gameState.yardLine); // Line of scrimmage

  // Generate offensive player positions (spread formation)
  const offensePlayers: Array<{ id: number; pos: [number, number, number] }> = [
    { id: 1, pos: [losX - 5, 0, 0] }, // QB
    { id: 2, pos: [losX - 7, 0, 0] }, // RB
    { id: 3, pos: [losX, 0, -10] }, // WR Left
    { id: 4, pos: [losX, 0, 10] }, // WR Right
    { id: 5, pos: [losX, 0, -5] }, // TE
    { id: 6, pos: [losX, 0, -2] }, // OL
    { id: 7, pos: [losX, 0, -1] }, // OL
    { id: 8, pos: [losX, 0, 0] }, // Center
    { id: 9, pos: [losX, 0, 1] }, // OL
    { id: 10, pos: [losX, 0, 2] }, // OL
    { id: 11, pos: [losX, 0, 5] }, // Slot WR
  ];

  // Generate defensive player positions (4-3 formation)
  const defensePlayers: Array<{ id: number; pos: [number, number, number] }> = [
    { id: 12, pos: [losX + 2, 0, -12] }, // CB Left
    { id: 13, pos: [losX + 2, 0, 12] }, // CB Right
    { id: 14, pos: [losX + 8, 0, -8] }, // Safety Left
    { id: 15, pos: [losX + 8, 0, 8] }, // Safety Right
    { id: 16, pos: [losX + 1, 0, -5] }, // DE
    { id: 17, pos: [losX + 1, 0, 5] }, // DE
    { id: 18, pos: [losX + 1, 0, -2] }, // DT
    { id: 19, pos: [losX + 1, 0, 2] }, // DT
    { id: 20, pos: [losX + 4, 0, -3] }, // LB
    { id: 21, pos: [losX + 4, 0, 0] }, // MLB
    { id: 22, pos: [losX + 4, 0, 3] }, // LB
  ];

  return (
    <group ref={fieldRef} position={[0, -2, 0]}>
      {/* Turf */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[120, 53.3]} />
        <meshStandardMaterial color="#2e8b57" roughness={0.8} />
      </mesh>

      {/* Yard Lines */}
      {Array.from({ length: 21 }).map((_, i) => {
        const x = (i - 10) * 6; // Every 5 yards
        return (
          <group key={i} position={[x, 0.01, 0]}>
            {/* Line */}
            <mesh rotation={[-Math.PI / 2, 0, 0]}>
              <planeGeometry args={[0.2, 53.3]} />
              <meshBasicMaterial color="white" opacity={0.5} transparent />
            </mesh>
            {/* Numbers */}
            {i % 2 === 0 && i !== 0 && i !== 20 && (
              <>
                <Text
                  position={[0, 0.1, 20]}
                  rotation={[-Math.PI / 2, 0, 0]}
                  fontSize={2}
                  color="white"
                >
                  {50 - Math.abs(x / 6) * 5}
                </Text>
                <Text
                  position={[0, 0.1, -20]}
                  rotation={[-Math.PI / 2, 0, Math.PI]}
                  fontSize={2}
                  color="white"
                >
                  {50 - Math.abs(x / 6) * 5}
                </Text>
              </>
            )}
          </group>
        );
      })}

      {/* Endzones */}
      <mesh position={[-60, 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[10, 53.3]} />
        <meshBasicMaterial color="#002244" opacity={0.8} transparent />{" "}
        {/* Empire Navy */}
      </mesh>
      <mesh position={[60, 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[10, 53.3]} />
        <meshBasicMaterial color="#880000" opacity={0.8} transparent />{" "}
        {/* Genesis Red */}
      </mesh>

      {/* PLAYERS - Offensive Team (Blue) */}
      {offensePlayers.map((player) => (
        <PlayerCharacter
          key={player.id}
          position={player.pos}
          team="offense"
          playerNumber={player.id}
          isAnimating={isAnimating}
        />
      ))}

      {/* PLAYERS - Defensive Team (Red) */}
      {defensePlayers.map((player) => (
        <PlayerCharacter
          key={player.id}
          position={player.pos}
          team="defense"
          playerNumber={player.id}
          isAnimating={isAnimating}
        />
      ))}

      {/* Ball Position Marker */}
      <mesh position={[losX, 0.3, 0]} castShadow>
        <sphereGeometry args={[0.2, 16, 16]} />
        <meshStandardMaterial color="#8b4513" roughness={0.6} />
      </mesh>
    </group>
  );
};
