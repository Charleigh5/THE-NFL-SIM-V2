import React, { useRef, useEffect, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import type { PlayerVisualData } from "../../types/broadcast";

interface EnhancedPlayerCharacterProps {
  playerData: PlayerVisualData;
  position: [number, number, number];
  isAnimating?: boolean;
  targetPosition?: [number, number, number];
  showNumber?: boolean;
  detailLevel?: "low" | "medium" | "high";
}

export const EnhancedPlayerCharacter: React.FC<EnhancedPlayerCharacterProps> = ({
  playerData,
  position,
  isAnimating = false,
  targetPosition,
  showNumber = true,
  detailLevel = "medium",
}) => {
  const groupRef = useRef<THREE.Group>(null);
  const bodyRef = useRef<THREE.Mesh>(null);
  const helmetRef = useRef<THREE.Mesh>(null);

  const { visuals, height, position: playerPosition, number: playerNumber } = playerData;
  const { body_type } = visuals;
  const effectiveHeight = height || 72;

  // Calculate body proportions based on position and attributes
  const bodyDimensions = useMemo(() => {
    const baseHeight = (effectiveHeight / 72) * 1.8;

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
  }, [body_type, effectiveHeight]);

  // Position-based stance offset
  const stanceOffset = useMemo(() => {
    if (["OT", "OG", "C", "DT", "DE"].includes(playerPosition)) {
      return -0.15;
    } else if (playerPosition === "QB") {
      return 0.05;
    }
    return 0;
  }, [playerPosition]);

  useFrame((state, delta) => {
    if (groupRef.current) {
      const target =
        isAnimating && targetPosition
          ? new THREE.Vector3(...targetPosition)
          : new THREE.Vector3(...position);

      groupRef.current.position.lerp(target, delta * 5);

      const breathSpeed = playerPosition === "QB" ? 2 : 3;
      const breathAmount = body_type === "lean" ? 0.03 : 0.02;
      const breath =
        1 + Math.sin(state.clock.elapsedTime * breathSpeed + playerNumber) * breathAmount;

      if (bodyRef.current) {
        bodyRef.current.scale.y = breath;
      }
    }
  });

  useEffect(() => {
    if (groupRef.current && groupRef.current.position.lengthSq() === 0) {
      groupRef.current.position.set(...position);
    }
  }, [position]);

  return (
    <group ref={groupRef} position={position}>
      {/* Body */}
      <mesh ref={bodyRef} position={[0, 0.5 + stanceOffset, 0]} castShadow receiveShadow>
        <cylinderGeometry
          args={[
            bodyDimensions.radiusTop,
            bodyDimensions.radiusBottom,
            bodyDimensions.height,
            detailLevel === "high" ? 16 : 8,
          ]}
        />
        <meshStandardMaterial
          color={visuals.jersey_color_primary}
          roughness={0.6}
          metalness={0.1}
        />
      </mesh>

      {/* Shoulder pads */}
      {detailLevel !== "low" && (
        <mesh position={[0, 0.9 + stanceOffset, 0]} castShadow>
          <torusGeometry
            args={[bodyDimensions.radiusBottom + 0.05, 0.08, 8, detailLevel === "high" ? 24 : 16]}
          />
          <meshStandardMaterial color={visuals.jersey_color_secondary} roughness={0.7} />
        </mesh>
      )}

      {/* Helmet */}
      <group position={[0, 1.2 + stanceOffset, 0]}>
        <mesh ref={helmetRef} castShadow receiveShadow>
          <sphereGeometry
            args={[0.25, detailLevel === "high" ? 24 : 16, detailLevel === "high" ? 24 : 16]}
          />
          <meshStandardMaterial
            color={visuals.helmet_design.base}
            roughness={0.3}
            metalness={0.4}
          />
        </mesh>

        {visuals.helmet_design.stripe && visuals.helmet_design.stripe !== "none" && (
          <mesh position={[0, 0.02, 0]} rotation={[0, 0, Math.PI / 2]}>
            <cylinderGeometry args={[0.02, 0.02, 0.5, 8]} />
            <meshStandardMaterial color={visuals.helmet_design.stripe} />
          </mesh>
        )}

        <mesh position={[0, -0.05, 0.2]} castShadow>
          <boxGeometry args={[0.35, 0.25, 0.05]} />
          <meshStandardMaterial color={visuals.face_mask_color} roughness={0.5} metalness={0.8} />
        </mesh>
      </group>

      {/* Arms */}
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

      {/* Legs */}
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
          <sprite scale={[0.3, 0.3, 1]}>
            <spriteMaterial attach="material" color="white" opacity={0.9} transparent />
          </sprite>
        </group>
      )}

      {/* Contact Shadow */}
      <mesh position={[0, 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <circleGeometry args={[0.4, 16]} />
        <meshBasicMaterial color="black" opacity={0.3} transparent />
      </mesh>
    </group>
  );
};

export default EnhancedPlayerCharacter;
