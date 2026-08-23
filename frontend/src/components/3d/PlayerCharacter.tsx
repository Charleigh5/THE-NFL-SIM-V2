import { useRef, useEffect } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface PlayerCharacterProps {
  position: [number, number, number];
  team: "offense" | "defense";
  playerNumber?: number;
  isAnimating?: boolean;
  targetPosition?: [number, number, number];
}

const _tempTarget = new THREE.Vector3();

export const PlayerCharacter = ({
  position,
  team,
  playerNumber = 0,
  isAnimating = false,
  targetPosition,
}: PlayerCharacterProps) => {
  const meshRef = useRef<THREE.Group>(null);

  useFrame((state, delta) => {
    if (meshRef.current) {
      // Determine target without allocating a new Vector3 every frame
      if (isAnimating && targetPosition) {
        _tempTarget.set(targetPosition[0], targetPosition[1], targetPosition[2]);
      } else {
        _tempTarget.set(position[0], position[1], position[2]);
      }

      // Smooth interpolation (lerp)
      meshRef.current.position.lerp(_tempTarget, delta * 5);

      // Breathing animation (bobbing/scaling)
      // Only breathe if not moving fast? Or always.
      // Let's scale slightly on Y
      const breath = 1 + Math.sin(state.clock.elapsedTime * 3 + playerNumber) * 0.02;
      meshRef.current.scale.set(1, breath, 1);
    }
  });

  // Initial placement (optional, to prevent flying in from 0,0,0)
  useEffect(() => {
    if (meshRef.current) {
      // Only set if very far away (initial load)
      if (meshRef.current.position.lengthSq() === 0) {
        meshRef.current.position.set(...position);
      }
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Color based on team
  const bodyColor = team === "offense" ? "#3b82f6" : "#ef4444"; // Blue for offense, Red for defense
  const helmetColor = team === "offense" ? "#1e40af" : "#991b1b";

  return (
    <group ref={meshRef}>
      {/* Body (cylinder) */}
      <mesh position={[0, 0.5, 0]} castShadow>
        <cylinderGeometry args={[0.3, 0.4, 1, 8]} />
        <meshStandardMaterial color={bodyColor} roughness={0.7} />
      </mesh>

      {/* Helmet (sphere) */}
      <mesh position={[0, 1.2, 0]} castShadow>
        <sphereGeometry args={[0.25, 16, 16]} />
        <meshStandardMaterial color={helmetColor} roughness={0.3} metalness={0.5} />
      </mesh>

      {/* Jersey Number (text sprite - optional, simplified for MVP) */}
      {playerNumber > 0 && (
        <sprite position={[0, 0.5, 0.4]} scale={[0.5, 0.5, 0.5]}>
          <spriteMaterial attach="material" color="white" />
        </sprite>
      )}

      {/* Shadow indicator (circle on ground) */}
      <mesh position={[0, 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[0.4, 16]} />
        <meshBasicMaterial color="black" opacity={0.3} transparent />
      </mesh>
    </group>
  );
};
