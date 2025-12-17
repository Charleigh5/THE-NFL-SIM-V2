import React, { useRef, useState, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { Text, Html, Float, MeshDistortMaterial } from "@react-three/drei";
import * as THREE from "three";
import {
  Brain,
  BicepsFlexed,
  Rocket,
  Footprints,
  Zap,
  Swords,
  Snowflake,
  Sprout,
  Shield,
  Crosshair,
  Hand,
} from "lucide-react";
import { ICON_KEYS } from "../../config/SkillTreeConfig";
import "./SkillTree.css";

// Map keys to Lucide Components
const ICON_MAP = {
  [ICON_KEYS.BRAIN]: Brain,
  [ICON_KEYS.ARM]: BicepsFlexed,
  [ICON_KEYS.ROCKET]: Rocket,
  [ICON_KEYS.BOOT]: Footprints,
  [ICON_KEYS.LIGHTNING]: Zap,
  [ICON_KEYS.CHESS]: Swords,
  [ICON_KEYS.ICE]: Snowflake,
  [ICON_KEYS.GROWTH]: Sprout,
  [ICON_KEYS.SHIELD]: Shield,
  [ICON_KEYS.TARGET]: Crosshair,
  [ICON_KEYS.HANDS]: Hand,
};

interface SkillNode3DProps {
  id: string;
  position: [number, number, number];
  iconType: string;
  isUnlocked: boolean;
  isEquipped: boolean;
  tier: string;
  label: string;
  onClick: (id: string) => void;
}

export const SkillNode3D: React.FC<SkillNode3DProps> = ({
  id,
  position,
  iconType,
  isUnlocked,
  isEquipped,
  tier,
  label,
  onClick,
}) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHover] = useState(false);

  // Determine Colors based on state
  const baseColor = isEquipped
    ? "#fbbf24" // Gold
    : isUnlocked
      ? "#3b82f6" // Blue
      : "#1f2937"; // Gray

  const glowColor = isEquipped ? "#f59e0b" : isUnlocked ? "#60a5fa" : "#374151";

  // Icon Component
  const IconComponent = ICON_MAP[iconType as keyof typeof ICON_MAP] || Brain; // Default to brain

  useFrame((state, delta) => {
    if (meshRef.current) {
      // Hover Scale Animation
      const targetScale = hovered ? 1.2 : 1.0;
      meshRef.current.scale.lerp(
        new THREE.Vector3(targetScale, targetScale, targetScale),
        delta * 10
      );

      // Pulse Animation if unlocked
      if (isUnlocked) {
        // meshRef.current.rotation.y += delta * 0.5;
      }
    }
  });

  return (
    <group position={position}>
      {/* HTML Overlay for Icon (Easier to render crisp SVG icons) */}
      {/* We use a billboarded HTML element for the icon so it always faces camera and is crisp */}
      <Html
        transform
        occlude="blending"
        position={[0, 0, 0.51]} // Slightly in front of sphere
        style={{
          pointerEvents: "none",
          color: isUnlocked ? "white" : "rgba(255,255,255,0.2)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div className="skill-node-icon-container">
          <IconComponent size={24} strokeWidth={2.5} />
        </div>
      </Html>

      {/* The Core Sphere */}
      <Float speed={2} rotationIntensity={0.2} floatIntensity={0.2}>
        <mesh
          ref={meshRef}
          onClick={(e) => {
            e.stopPropagation();
            onClick(id);
          }}
          onPointerOver={() => {
            document.body.style.cursor = "pointer";
            setHover(true);
          }}
          onPointerOut={() => {
            document.body.style.cursor = "auto";
            setHover(false);
          }}
        >
          {/* Hexagon or Sphere? Sphere is classic orb. Icosahedron is techy. */}
          <icosahedronGeometry args={[0.5, 2]} />

          <MeshDistortMaterial
            color={baseColor}
            emissive={glowColor}
            emissiveIntensity={isUnlocked ? (hovered ? 2 : 1) : 0}
            roughness={isUnlocked ? 0.2 : 0.8}
            metalness={isUnlocked ? 0.8 : 0.2}
            distort={hovered ? 0.4 : 0} // Glitch effect on hover
            speed={5}
            toneMapped={false}
          />
        </mesh>
      </Float>

      {/* Text Label */}
      <Text
        position={[0, -0.8, 0]}
        fontSize={0.2}
        color={isUnlocked ? "white" : "gray"}
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#000000"
      >
        {label}
      </Text>

      {/* Selection/Focus Rings (Optional) */}
      {isEquipped && (
        <mesh rotation={[Math.PI / 2, 0, 0]}>
          <ringGeometry args={[0.6, 0.65, 32]} />
          <meshBasicMaterial color="#fbbf24" toneMapped={false} />
        </mesh>
      )}
    </group>
  );
};
