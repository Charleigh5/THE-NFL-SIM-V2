import React, { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface EnhancedFieldVisualizerProps {
  gameId?: number;
  showPlayers?: boolean;
  detailLevel?: "low" | "medium" | "high";
  homeColor?: string;
  awayColor?: string;
  showYardLines?: boolean;
  showNumbers?: boolean;
}

export const EnhancedFieldVisualizer: React.FC<EnhancedFieldVisualizerProps> = ({
  detailLevel = "medium",
  homeColor = "#002244",
  awayColor = "#880000",
}) => {
  const fieldRef = useRef<THREE.Group>(null);

  // Occasional subtle stadium light flicker
  useFrame(() => {
    if (fieldRef.current && Math.random() > 0.995) {
      fieldRef.current.children.forEach((child) => {
        if ((child as THREE.Mesh).material) {
          const mat = (child as THREE.Mesh).material as THREE.MeshStandardMaterial;
          if (mat.emissive) {
            mat.emissiveIntensity = 0.8 + Math.random() * 0.4;
          }
        }
      });
    }
  });

  return (
    <group ref={fieldRef}>
      {/* Main Field */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[120, 53.3]} />
        <meshStandardMaterial color="#2e8b57" roughness={0.8} metalness={0.1} />
      </mesh>

      {/* Grass texture pattern (stripes) */}
      {Array.from({ length: 12 }).map((_, i) => (
        <mesh
          key={`stripe-${i}`}
          position={[(i - 6) * 10, 0.02, 0]}
          rotation={[-Math.PI / 2, 0, 0]}
        >
          <planeGeometry args={[10, 53.3]} />
          <meshStandardMaterial
            color={i % 2 === 0 ? "#3cb371" : "#2e8b57"}
            roughness={0.8}
            transparent
            opacity={0.3}
          />
        </mesh>
      ))}

      {/* Yard Lines */}
      {Array.from({ length: 21 }).map((_, i) => {
        const x = (i - 10) * 6;

        return (
          <group key={`yardline-${i}`} position={[x, 0.03, 0]}>
            <mesh rotation={[-Math.PI / 2, 0, 0]}>
              <planeGeometry args={[0.3, 53.3]} />
              <meshBasicMaterial color="white" opacity={0.8} transparent />
            </mesh>

            {i % 2 === 0 && i !== 0 && i !== 20 && (
              <>
                <mesh position={[0, 0.05, 22]} rotation={[-Math.PI / 2, 0, 0]}>
                  <planeGeometry args={[3, 4]} />
                  <meshBasicMaterial color="white" />
                </mesh>
                <mesh position={[0, 0.05, -22]} rotation={[-Math.PI / 2, 0, Math.PI]}>
                  <planeGeometry args={[3, 4]} />
                  <meshBasicMaterial color="white" />
                </mesh>
              </>
            )}
          </group>
        );
      })}

      {/* Hash Marks */}
      {Array.from({ length: 19 }).map((_, i) => {
        const x = (i - 9) * 6 - 3;
        return (
          <group key={`hash-${i}`}>
            <mesh position={[x, 0.03, -8]} rotation={[-Math.PI / 2, 0, 0]}>
              <planeGeometry args={[0.3, 1]} />
              <meshBasicMaterial color="white" />
            </mesh>
            <mesh position={[x, 0.03, 8]} rotation={[-Math.PI / 2, 0, 0]}>
              <planeGeometry args={[0.3, 1]} />
              <meshBasicMaterial color="white" />
            </mesh>
          </group>
        );
      })}

      {/* Endzones */}
      <mesh position={[-65, 0.03, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[10, 53.3]} />
        <meshStandardMaterial
          color={homeColor}
          roughness={0.7}
          metalness={0.2}
          opacity={0.9}
          transparent
        />
      </mesh>

      <mesh position={[65, 0.03, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[10, 53.3]} />
        <meshStandardMaterial
          color={awayColor}
          roughness={0.7}
          metalness={0.2}
          opacity={0.9}
          transparent
        />
      </mesh>

      {/* Goal Posts */}
      <group position={[-70, 0, 0]}>
        <mesh position={[0, 5, 0]} castShadow>
          <cylinderGeometry args={[0.15, 0.15, 10, 8]} />
          <meshStandardMaterial color="yellow" roughness={0.5} metalness={0.6} />
        </mesh>
        <mesh position={[0, 10, 0]} rotation={[0, 0, Math.PI / 2]} castShadow>
          <cylinderGeometry args={[0.15, 0.15, 18.5, 8]} />
          <meshStandardMaterial color="yellow" roughness={0.5} metalness={0.6} />
        </mesh>
        <mesh position={[-0.5, 10, 0]} castShadow>
          <cylinderGeometry args={[0.1, 0.1, 10, 8]} />
          <meshStandardMaterial color="yellow" roughness={0.5} metalness={0.6} />
        </mesh>
      </group>

      <group position={[70, 0, 0]}>
        <mesh position={[0, 5, 0]} castShadow>
          <cylinderGeometry args={[0.15, 0.15, 10, 8]} />
          <meshStandardMaterial color="yellow" roughness={0.5} metalness={0.6} />
        </mesh>
        <mesh position={[0, 10, 0]} rotation={[0, 0, Math.PI / 2]} castShadow>
          <cylinderGeometry args={[0.15, 0.15, 18.5, 8]} />
          <meshStandardMaterial color="yellow" roughness={0.5} metalness={0.6} />
        </mesh>
        <mesh position={[0.5, 10, 0]} castShadow>
          <cylinderGeometry args={[0.1, 0.1, 10, 8]} />
          <meshStandardMaterial color="yellow" roughness={0.5} metalness={0.6} />
        </mesh>
      </group>

      {/* Sidelines */}
      <mesh position={[0, 0.04, -27]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[120, 1]} />
        <meshBasicMaterial color="white" />
      </mesh>

      <mesh position={[0, 0.04, 27]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[120, 1]} />
        <meshBasicMaterial color="white" />
      </mesh>

      {/* Ball marker placeholder */}
      <mesh position={[0, 0.3, 0]} castShadow>
        <sphereGeometry args={[0.2, 16, 16]} />
        <meshStandardMaterial color="#8b4513" roughness={0.6} metalness={0.2} />
      </mesh>

      {/* Stadium seating */}
      {detailLevel === "high" && (
        <>
          <mesh position={[0, 10, -40]} rotation={[-0.3, 0, 0]}>
            <boxGeometry args={[120, 15, 10]} />
            <meshStandardMaterial color="#333333" roughness={0.9} />
          </mesh>
          <mesh position={[0, 10, 40]} rotation={[0.3, 0, 0]}>
            <boxGeometry args={[120, 15, 10]} />
            <meshStandardMaterial color="#333333" roughness={0.9} />
          </mesh>
        </>
      )}

      {/* Lighting rigs */}
      {detailLevel !== "low" && (
        <>
          <pointLight
            position={[0, 30, 0]}
            intensity={1.2}
            color="#fff5e6"
            castShadow
            distance={150}
          />
          <pointLight position={[-30, 25, -20]} intensity={0.8} color="#fff5e6" />
          <pointLight position={[30, 25, 20]} intensity={0.8} color="#fff5e6" />
        </>
      )}
    </group>
  );
};

export default EnhancedFieldVisualizer;
