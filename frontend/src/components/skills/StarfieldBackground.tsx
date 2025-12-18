import { Sparkles, Stars, Cloud } from "@react-three/drei";
import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

export const StarfieldBackground = () => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      // Slow rotation for dynamism
      groupRef.current.rotation.y = state.clock.getElapsedTime() * 0.05;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Deep space / stadium night sky feel */}
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

      {/* Floating "Chalk Dust" or Magic Particles */}
      <Sparkles
        count={200}
        scale={20}
        size={4}
        speed={0.4}
        opacity={0.5}
        color="#fbbf24" // Gold tint
        noise={1} // Organic movement
      />

      <Sparkles
        count={100}
        scale={25}
        size={6}
        speed={0.2}
        opacity={0.3}
        color="#3b82f6" // Blue tint
        noise={2}
      />

      {/* Subtle Fog/Clouds for depth */}
      <Cloud opacity={0.15} speed={0.2} segments={20} color="#1f2937" />
    </group>
  );
};
