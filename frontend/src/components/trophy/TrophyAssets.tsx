import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { Text } from "@react-three/drei";
import * as THREE from "three";

// --- Materials ---
const GoldMaterial = () => (
  <meshStandardMaterial color="#FFD700" metalness={1} roughness={0.15} envMapIntensity={1.5} />
);

const SilverMaterial = () => (
  <meshStandardMaterial color="#C0C0C0" metalness={1} roughness={0.2} envMapIntensity={1.2} />
);

const CrystalMaterial = () => (
  <meshPhysicalMaterial
    color="#d1e8ff"
    transmission={0.9} // Glass-like
    opacity={1}
    metalness={0.1}
    roughness={0.05}
    thickness={1}
    ior={1.5}
  />
);

// --- Trophies ---

export const LombardiTrophy = (props: any) => {
  const group = useRef<THREE.Group>(null);

  // Slow rotation
  useFrame((state) => {
    if (group.current) {
      group.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.2) * 0.1;
    }
  });

  return (
    <group ref={group} {...props}>
      {/* Base (Pyramid-ish) */}
      <mesh position={[0, 1.5, 0]} castShadow>
        <cylinderGeometry args={[0.2, 0.4, 3, 4]} />
        <SilverMaterial />
      </mesh>

      {/* The Football */}
      <mesh position={[0, 3.2, 0.2]} rotation={[0.4, 0, 0.2]} castShadow>
        <sphereGeometry args={[0.5, 32, 16]} />
        <SilverMaterial />
        {/* Seams logic would be complex, keeping simple silver sphere for "Abstract" vibe */}
      </mesh>

      {/* Plaque text */}
      <Text
        position={[0, 0.5, 0.35]}
        fontSize={0.15}
        color="black"
        anchorX="center"
        anchorY="middle"
      >
        WORLD CHAMPS
      </Text>
    </group>
  );
};

export const MvpTrophy = (props: any) => {
  const mesh = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (mesh.current) {
      mesh.current.rotation.y += 0.01;
      mesh.current.position.y = Math.sin(state.clock.elapsedTime) * 0.1 + 1;
    }
  });

  return (
    <group {...props}>
      <mesh ref={mesh} position={[0, 1, 0]} castShadow>
        <icosahedronGeometry args={[0.6, 0]} />
        <GoldMaterial />
      </mesh>
      <mesh position={[0, 0.2, 0]} receiveShadow>
        <boxGeometry args={[1, 0.4, 1]} />
        <meshStandardMaterial color="#333" />
      </mesh>
    </group>
  );
};

export const DivisionTitleTrophy = (props: any) => {
  return (
    <group {...props}>
      <mesh position={[0, 1.2, 0]} castShadow>
        <octahedronGeometry args={[0.5]} />
        <CrystalMaterial />
      </mesh>
      <mesh position={[0, 0.5, 0]}>
        <cylinderGeometry args={[0.1, 0.1, 1, 8]} />
        <SilverMaterial />
      </mesh>
      <mesh position={[0, 0, 0]}>
        <cylinderGeometry args={[0.4, 0.4, 0.1, 16]} />
        <SilverMaterial />
      </mesh>
    </group>
  );
};
