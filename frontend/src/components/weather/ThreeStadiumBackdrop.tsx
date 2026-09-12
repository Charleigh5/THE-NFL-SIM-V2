import React, { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float } from "@react-three/drei";
import * as THREE from "three";
import { useWeatherThemeStore } from "../../store/useWeatherThemeStore";

// 3D Procedural NFL Football Mesh with laces & leather shader
const NFLFootball: React.FC<{ position?: [number, number, number]; scale?: number }> = ({
  position = [0, 0, 0],
  scale = 1.0,
}) => {
  const meshRef = useRef<THREE.Group>(null);
  const { condition } = useWeatherThemeStore();

  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.45;
      meshRef.current.rotation.x = Math.sin(Date.now() * 0.001) * 0.15;
    }
  });

  const isRain = condition === "ARROWHEAD_DOWNPOUR";
  const isSnow = condition === "LAMBEAU_BLIZZARD";

  return (
    <group ref={meshRef} position={position} scale={scale}>
      {/* Football body: Prolate spheroid */}
      <mesh castShadow receiveShadow scale={[1.0, 1.65, 1.0]} rotation={[0, 0, Math.PI / 4]}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial
          color={isSnow ? "#6a402a" : "#7b3811"}
          roughness={isRain ? 0.2 : 0.65}
          metalness={isRain ? 0.35 : 0.05}
        />
      </mesh>

      {/* White Regulation Grip Stripes */}
      <mesh position={[0.42, 0.42, 0]} rotation={[0, 0, Math.PI / 4]}>
        <torusGeometry args={[0.78, 0.04, 16, 32]} />
        <meshStandardMaterial color="#f0f0f0" roughness={0.4} />
      </mesh>
      <mesh position={[-0.42, -0.42, 0]} rotation={[0, 0, Math.PI / 4]}>
        <torusGeometry args={[0.78, 0.04, 16, 32]} />
        <meshStandardMaterial color="#f0f0f0" roughness={0.4} />
      </mesh>

      {/* Center Laces Bar */}
      <mesh position={[0.05, 0.05, 0.88]} rotation={[0, 0, Math.PI / 4]}>
        <boxGeometry args={[0.06, 0.75, 0.04]} />
        <meshStandardMaterial color="#ffffff" roughness={0.2} />
      </mesh>

      {/* Cross Laces */}
      {[-0.24, -0.12, 0, 0.12, 0.24].map((offset, i) => (
        <mesh
          key={`lace-${i}`}
          position={[offset * 0.7 + 0.05, offset * 0.7 + 0.05, 0.89]}
          rotation={[0, 0, -Math.PI / 4]}
        >
          <boxGeometry args={[0.04, 0.24, 0.03]} />
          <meshStandardMaterial color="#ffffff" roughness={0.2} />
        </mesh>
      ))}
    </group>
  );
};

// 3D Procedural Lombardi Trophy Mesh with PBR Chrome Reflection
const LombardiTrophy: React.FC<{ position?: [number, number, number]; scale?: number }> = ({
  position = [0, 0, 0],
  scale = 1.0,
}) => {
  const trophyRef = useRef<THREE.Group>(null);
  const { lightningActive } = useWeatherThemeStore();

  useFrame((_, delta) => {
    if (trophyRef.current) {
      trophyRef.current.rotation.y += delta * 0.35;
    }
  });

  return (
    <group ref={trophyRef} position={position} scale={scale}>
      {/* Triangular Flared Base Pillar */}
      <mesh position={[0, -0.8, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[0.3, 0.65, 2.4, 3]} />
        <meshStandardMaterial
          color="#d0d8e2"
          metalness={0.96}
          roughness={lightningActive ? 0.05 : 0.18}
          envMapIntensity={2.0}
        />
      </mesh>

      {/* Regulation Silver Football atop Trophy at authentic 45-degree angle */}
      <group position={[0, 0.75, 0]} rotation={[Math.PI / 4, 0, Math.PI / 4]}>
        <mesh castShadow receiveShadow scale={[0.55, 0.95, 0.55]}>
          <sphereGeometry args={[1, 32, 32]} />
          <meshStandardMaterial
            color="#e8f0f8"
            metalness={0.98}
            roughness={lightningActive ? 0.02 : 0.12}
            envMapIntensity={2.5}
          />
        </mesh>
      </group>
    </group>
  );
};

// 3D Stadium Architecture & Dynamic PBR Field
const StadiumScene: React.FC = () => {
  const { preset, condition, lightningActive, lightningIntensity } = useWeatherThemeStore();

  const isRain = condition === "ARROWHEAD_DOWNPOUR";
  const isSnow = condition === "LAMBEAU_BLIZZARD";

  return (
    <>
      {/* Atmospheric Fog */}
      <fog
        attach="fog"
        args={[
          preset.ambientLightingHex,
          isSnow ? 25 : isRain ? 35 : 55,
          isSnow ? 90 : isRain ? 110 : 180,
        ]}
      />

      {/* Ambient Fill Light */}
      <ambientLight
        intensity={lightningActive ? 2.5 : isSnow ? 0.65 : 0.35}
        color={lightningActive ? "#e6f7ff" : preset.ambientLightingHex}
      />

      {/* Main Stadium Directional Floodlight */}
      <directionalLight
        position={[25, 45, 20]}
        intensity={lightningActive ? 4.5 * lightningIntensity : 1.8}
        color={lightningActive ? "#ffffff" : preset.stadiumLightHex}
        castShadow
        shadow-mapSize={[1024, 1024]}
      />

      {/* Rim Spotlight for high-contrast broadcast silhouette */}
      <spotLight
        position={[-30, 35, -20]}
        intensity={lightningActive ? 3.0 : 1.2}
        color={preset.stadiumLightHex}
        angle={0.6}
        penumbra={0.8}
      />

      {/* PBR Gridiron Turf Ground Plane */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -2.5, 0]} receiveShadow>
        <planeGeometry args={[160, 100]} />
        <meshStandardMaterial
          color={isSnow ? "#dce7ee" : preset.turfTint}
          roughness={isRain ? 0.18 : isSnow ? 0.85 : 0.6}
          metalness={isRain ? 0.45 : 0.05}
        />
      </mesh>

      {/* Yard Line Inlays */}
      {[-40, -20, 0, 20, 40].map((x, i) => (
        <mesh key={`yard-${i}`} rotation={[-Math.PI / 2, 0, 0]} position={[x, -2.48, 0]}>
          <planeGeometry args={[0.5, 75]} />
          <meshBasicMaterial color="#ffffff" transparent opacity={isSnow ? 0.35 : 0.65} />
        </mesh>
      ))}

      {/* Stadium Grandstand Rings (Curved Architectural Tier Tiers) */}
      <mesh position={[0, 4, -48]} rotation={[0, 0, 0]}>
        <cylinderGeometry args={[75, 85, 18, 32, 1, true, Math.PI * 0.8, Math.PI * 1.4]} />
        <meshStandardMaterial
          color="#12151c"
          roughness={0.7}
          metalness={0.4}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Stadium Floodlight Pylons with Luminous Glow Bulbs */}
      {[
        [-50, 22, -35],
        [50, 22, -35],
        [-50, 22, 35],
        [50, 22, 35],
      ].map((pos, i) => (
        <group key={`pylon-${i}`} position={pos as [number, number, number]}>
          {/* Steel Truss Tower */}
          <mesh position={[0, -11, 0]}>
            <cylinderGeometry args={[0.6, 1.2, 22, 8]} />
            <meshStandardMaterial color="#2a2e38" metalness={0.8} roughness={0.4} />
          </mesh>
          {/* Light Fixture Bank */}
          <mesh position={[0, 0, 0]}>
            <boxGeometry args={[5, 2.5, 1.2]} />
            <meshStandardMaterial color="#1e222b" />
          </mesh>
          {/* Emissive Bulb Array */}
          <mesh position={[0, 0, 0.6]}>
            <planeGeometry args={[4.6, 2.2]} />
            <meshBasicMaterial color={lightningActive ? "#ffffff" : preset.stadiumLightHex} />
          </mesh>
        </group>
      ))}

      {/* Floating Interactive 3D NFL Object Stage */}
      <Float speed={1.8} rotationIntensity={0.6} floatIntensity={0.8}>
        <NFLFootball position={[-7.5, 1.2, 0]} scale={1.35} />
        <LombardiTrophy position={[7.5, 1.2, 0]} scale={1.25} />
      </Float>
    </>
  );
};

export const ThreeStadiumBackdrop: React.FC = () => {
  const { show3DBackdrop } = useWeatherThemeStore();

  if (!show3DBackdrop) return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden opacity-85 transition-opacity duration-700">
      <Canvas
        shadows
        camera={{ position: [0, 6, 22], fov: 42 }}
        gl={{ antialias: true, alpha: true, powerPreference: "high-performance" }}
      >
        <StadiumScene />
      </Canvas>
    </div>
  );
};
