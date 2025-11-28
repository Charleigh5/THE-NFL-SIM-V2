import { Canvas } from "@react-three/fiber";
import { Environment, OrbitControls, Stars } from "@react-three/drei";
import { Suspense } from "react";
import { useLocation } from "react-router-dom";
import { FieldVisualizer } from "./FieldVisualizer";

export const SceneContainer = () => {
  const location = useLocation();

  return (
    <div className="canvas-container">
      <Canvas
        camera={{ position: [0, 5, 10], fov: 45 }}
        gl={{ antialias: true, alpha: true }}
      >
        <Suspense fallback={null}>
          {/* Global Environment */}
          <color attach="background" args={["#050510"]} />
          <fog attach="fog" args={["#050510", 10, 50]} />

          <Stars
            radius={100}
            depth={50}
            count={5000}
            factor={4}
            saturation={0}
            fade
            speed={1}
          />
          <Environment preset="city" />

          {/* Ambient Light */}
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} intensity={1} />

          <OrbitControls
            enableZoom={false}
            enablePan={false}
            autoRotate={location.pathname === "/"}
            autoRotateSpeed={0.5}
            maxPolarAngle={Math.PI / 2}
          />

          {location.pathname === "/live-sim" ? (
            <FieldVisualizer />
          ) : (
            /* Placeholder Content (The "Hive" Core) - Only show on Dashboard/others */
            <mesh position={[0, 0, 0]} rotation={[0, Math.PI / 4, 0]}>
              <boxGeometry args={[2, 2, 2]} />
              <meshStandardMaterial
                color="#00f0ff"
                roughness={0.1}
                metalness={0.8}
                wireframe
              />
            </mesh>
          )}
        </Suspense>
      </Canvas>
    </div>
  );
};
