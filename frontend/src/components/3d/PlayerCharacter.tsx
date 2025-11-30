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

export const PlayerCharacter = ({
  position,
  team,
  playerNumber = 0,
  isAnimating = false,
  targetPosition,
}: PlayerCharacterProps) => {
  const meshRef = useRef<THREE.Group>(null);

  // Use a ref for target position to avoid re-creating Vector3 every frame if possible,
  // but creating it is cheap.

  useFrame((state, delta) => {
    if (meshRef.current) {
      // Determine target: if animating and explicit target provided, use that.
      // Otherwise use the 'position' prop (which changes with LOS).
      const target =
        isAnimating && targetPosition
          ? new THREE.Vector3(...targetPosition)
          : new THREE.Vector3(...position);

      // Smooth interpolation (lerp)
      // Use a faster speed for responsiveness, but slow enough to be smooth
      meshRef.current.position.lerp(target, delta * 5);

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
