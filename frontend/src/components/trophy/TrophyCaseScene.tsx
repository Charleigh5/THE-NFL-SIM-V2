import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Environment, ContactShadows, Stars } from "@react-three/drei";
import { LombardiTrophy, MvpTrophy, DivisionTitleTrophy } from "./TrophyAssets";
import { useTheme } from "../../context/ThemeContext";

export const TrophyCaseScene = () => {
  const { activeTeam } = useTheme();

  return (
    <Canvas shadows camera={{ position: [0, 2, 8], fov: 50 }}>
      {/* Atmosphere */}
      <color attach="background" args={["#050510"]} />
      <fog attach="fog" args={["#050510", 5, 20]} />
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <spotLight
        position={[10, 10, 10]}
        angle={0.15}
        penumbra={1}
        shadow-mapSize={2048}
        castShadow
        intensity={50}
        color={activeTeam?.colors.secondary || "#ffffff"}
      />
      <pointLight
        position={[-10, -10, -10]}
        intensity={1.5}
        color={activeTeam?.colors.primary || "#ffffff"}
      />

      {/* Environment */}
      <Suspense fallback={null}>
        <Environment preset="city" />
      </Suspense>

      {/* Trophies Arrangement */}
      <group position={[0, -1, 0]}>
        {/* Centerpiece: Super Bowl Trophy */}
        <LombardiTrophy position={[0, 0, 0]} />

        {/* Flanking: MVPs */}
        <MvpTrophy position={[-3, 0, 1]} rotation={[0, 0.5, 0]} />
        <MvpTrophy position={[3, 0, 1]} rotation={[0, -0.5, 0]} />

        {/* Back Row: Division Titles */}
        <DivisionTitleTrophy position={[-1.5, 1, -2]} />
        <DivisionTitleTrophy position={[1.5, 1, -2]} />

        {/* Floor Reflections */}
        <ContactShadows
          resolution={1024}
          scale={50}
          blur={2.5}
          opacity={0.5}
          far={10}
          color={activeTeam?.colors.primary || "#000000"}
        />
      </group>

      {/* Controls */}
      <OrbitControls
        enablePan={false}
        minPolarAngle={Math.PI / 4}
        maxPolarAngle={Math.PI / 1.8}
        minDistance={4}
        maxDistance={12}
        autoRotate
        autoRotateSpeed={0.5}
      />
    </Canvas>
  );
};
