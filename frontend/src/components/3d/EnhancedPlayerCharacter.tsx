import React, { useRef, useEffect, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface PlayerVisualData {
  id: number;
  name: string;
  number: number;
  position: string;
  position_group: "offense" | "defense" | "special_teams";
  height: number;
  weight: number;
  visuals: {
    body_type: "large" | "medium" | "lean" | "athletic" | "pocket" | "muscular";
    jersey_color_primary: string;
    jersey_color_secondary: string;
    helmet_design: {
      base: string;
      stripe: string;
      logo_side: boolean;
      facemask: string;
    };
    face_mask_color: string;
    cleat_color: string;
    accessories: string[];
  };
}

interface EnhancedPlayerCharacterProps {
  playerData: PlayerVisualData;
  position: [number, number, number];
  isAnimating?: boolean;
  targetPosition?: [number, number, number];
  showNumber?: boolean;
  detailLevel?: "low" | "medium" | "high";
}

export const EnhancedPlayerCharacter = ({
  playerData,
  position,
  isAnimating = false,
  targetPosition,
  showNumber = true,
  detailLevel = "medium",
}: EnhancedPlayerCharacterProps) => {
  const groupRef = useRef<THREE.Group>(null);
  const bodyRef = useRef<THREE.Mesh>(null);
  const helmetRef = useRef<THREE.Mesh>(null);
  
  // Calculate body proportions based on position and attributes
  const bodyDimensions = useMemo(() => {
    const { body_type, height, weight } = playerData.visuals;
    const baseHeight = (height / 72) * 1.8; // Scale to meters
    
    switch (body_type) {
      case "large":
        return { radiusTop: 0.35, radiusBottom: 0.45, height: baseHeight * 0.55 };
      case "muscular":
        return { radiusTop: 0.32, radiusBottom: 0.42, height: baseHeight * 0.58 };
      case "athletic":
        return { radiusTop: 0.28, radiusBottom: 0.38, height: baseHeight * 0.6 };
      case "lean":
        return { radiusTop: 0.24, radiusBottom: 0.32, height: baseHeight * 0.62 };
      case "pocket":
        return { radiusTop: 0.3, radiusBottom: 0.4, height: baseHeight * 0.57 };
      default:
        return { radiusTop: 0.3, radiusBottom: 0.4, height: baseHeight * 0.58 };
    }
  }, [playerData.visuals.body_type, playerData.height]);

  // Position-based animations
  const stanceOffset = useMemo(() => {
    const { position } = playerData;
    if (["OT", "OG", "C", "DT", "DE"].includes(position)) {
      return -0.15; // Linemen crouch lower
    } else if (position === "QB") {
      return 0.05; // QB stands slightly taller
    }
    return 0;
  }, [playerData.position]);

  useFrame((state, delta) => {
    if (groupRef.current) {
      const target =
        isAnimating && targetPosition
          ? new THREE.Vector3(...targetPosition)
          : new THREE.Vector3(...position);

      // Smooth interpolation
      groupRef.current.position.lerp(target, delta * 5);

      // Breathing animation
      const breathSpeed = playerData.position === "QB" ? 2 : 3;
      const breathAmount = playerData.visuals.body_type === "lean" ? 0.03 : 0.02;
      const breath = 1 + Math.sin(state.clock.elapsedTime * breathSpeed + playerData.number) * breathAmount;
      
      if (bodyRef.current) {
        bodyRef.current.scale.y = breath;
      }
    }
  });

  // Initial placement
  useEffect(() => {
    if (groupRef.current && groupRef.current.position.lengthSq() === 0) {
      groupRef.current.position.set(...position);
    }
  }, []);

  const { visuals } = playerData;

  return (
    <group ref={groupRef} position={position}>
      {/* Body */}
      <mesh ref={bodyRef} position={[0, 0.5 + stanceOffset, 0]} castShadow receiveShadow>
        <cylinderGeometry 
          args={[bodyDimensions.radiusTop, bodyDimensions.radiusBottom, bodyDimensions.height, detailLevel === "high" ? 16 : 8]} 
        />
        <meshStandardMaterial 
          color={visuals.jersey_color_primary} 
          roughness={0.6} 
          metalness={0.1}
        />
      </mesh>

      {/* Shoulder pads bulge */}
      {detailLevel !== "low" && (
        <mesh position={[0, 0.9 + stanceOffset, 0]} castShadow>
          <torusGeometry args={[bodyDimensions.radiusBottom + 0.05, 0.08, 8, detailLevel === "high" ? 24 : 16]} />
          <meshStandardMaterial color={visuals.jersey_color_secondary} roughness={0.7} />
        </mesh>
      )}

      {/* Helmet */}
      <group position={[0, 1.2 + stanceOffset, 0]}>
        <mesh ref={helmetRef} castShadow receiveShadow>
          <sphereGeometry args={[0.25, detailLevel === "high" ? 24 : 16, detailLevel === "high" ? 24 : 16]} />
          <meshStandardMaterial 
            color={visuals.helmet_design.base} 
            roughness={0.3} 
            metalness={0.4} 
          />
        </mesh>
        
        {/* Helmet stripe */}
        {visuals.helmet_design.stripe && visuals.helmet_design.stripe !== "none" && (
          <mesh position={[0, 0.02, 0]} rotation={[0, 0, Math.PI / 2]}>
            <cylinderGeometry args={[0.02, 0.02, 0.5, 8]} />
            <meshStandardMaterial color={visuals.helmet_design.stripe} />
          </mesh>
        )}
        
        {/* Face mask */}
        <mesh position={[0, -0.05, 0.2]} castShadow>
          <boxGeometry args={[0.35, 0.25, 0.05]} />
          <meshStandardMaterial 
            color={visuals.face_mask_color} 
            roughness={0.5} 
            metalness={0.8} 
          />
        </mesh>
      </group>

      {/* Arms (simplified) */}
      {detailLevel === "high" && (
        <>
          <mesh position={[-0.35, 0.7 + stanceOffset, 0]} rotation={[0, 0, -0.3]} castShadow>
            <capsuleGeometry args={[0.08, 0.5, 4, 8]} />
            <meshStandardMaterial color={visuals.jersey_color_primary} />
          </mesh>
          <mesh position={[0.35, 0.7 + stanceOffset, 0]} rotation={[0, 0, 0.3]} castShadow>
            <capsuleGeometry args={[0.08, 0.5, 4, 8]} />
            <meshStandardMaterial color={visuals.jersey_color_primary} />
          </mesh>
        </>
      )}

      {/* Legs (simplified) */}
      {detailLevel === "high" && (
        <>
          <mesh position={[-0.15, 0.15 + stanceOffset, 0]} castShadow>
            <capsuleGeometry args={[0.1, 0.6, 4, 8]} />
            <meshStandardMaterial color={visuals.jersey_color_secondary} />
          </mesh>
          <mesh position={[0.15, 0.15 + stanceOffset, 0]} castShadow>
            <capsuleGeometry args={[0.1, 0.6, 4, 8]} />
            <meshStandardMaterial color={visuals.jersey_color_secondary} />
          </mesh>
        </>
      )}

      {/* Cleats */}
      {detailLevel !== "low" && (
        <>
          <mesh position={[-0.15, 0.02 + stanceOffset, 0]} castShadow>
            <boxGeometry args={[0.12, 0.05, 0.25]} />
            <meshStandardMaterial color={visuals.cleat_color} roughness={0.4} />
          </mesh>
          <mesh position={[0.15, 0.02 + stanceOffset, 0]} castShadow>
            <boxGeometry args={[0.12, 0.05, 0.25]} />
            <meshStandardMaterial color={visuals.cleat_color} roughness={0.4} />
          </mesh>
        </>
      )}

      {/* Accessories */}
      {visuals.accessories.includes("gloves") && detailLevel === "high" && (
        <>
          <mesh position={[-0.4, 0.45 + stanceOffset, 0.1]} castShadow>
            <sphereGeometry args={[0.09, 8, 8]} />
            <meshStandardMaterial color="white" roughness={0.6} />
          </mesh>
          <mesh position={[0.4, 0.45 + stanceOffset, 0.1]} castShadow>
            <sphereGeometry args={[0.09, 8, 8]} />
            <meshStandardMaterial color="white" roughness={0.6} />
          </mesh>
        </>
      )}

      {/* Jersey Number */}
      {showNumber && playerData.number > 0 && (
        <group position={[0, 0.6 + stanceOffset, bodyDimensions.radiusBottom + 0.02]}>
          {/* This would use @react-three/drei Text in production */}
          <sprite scale={[0.3, 0.3, 1]}>
            <spriteMaterial attach="material" color="white" opacity={0.9} transparent />
          </sprite>
        </group>
      )}

      {/* Shadow */}
      <mesh position={[0, 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <circleGeometry args={[0.4, 16]} />
        <meshBasicMaterial color="black" opacity={0.3} transparent />
      </mesh>
    </group>
  );
};

export default EnhancedPlayerCharacter;
