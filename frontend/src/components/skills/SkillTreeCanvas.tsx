import { Canvas } from "@react-three/fiber";
import { OrbitControls, PerspectiveCamera, Environment, ContactShadows } from "@react-three/drei";
import type { SkillTreeLayout } from "../../config/SkillTreeConfig";
import { SkillNode3D } from "./SkillNode3D";
import { ConnectionLine } from "./ConnectionLine";
import { StarfieldBackground } from "./StarfieldBackground";
import { Suspense, useMemo } from "react";
import "./SkillTree.css";

interface SkillTreeCanvasProps {
  layout: SkillTreeLayout;
  unlockedTraits: string[]; // List of trait IDs
  equippedTraits: string[]; // List of trait IDs
  onNodeClick: (traitId: string) => void;
}

export const SkillTreeCanvas: React.FC<SkillTreeCanvasProps> = ({
  layout,
  unlockedTraits,
  equippedTraits,
  onNodeClick,
}) => {
  // Memoize connections to avoid recalc on every render
  const connections = useMemo(() => {
    const lines: Array<{
      start: [number, number, number];
      end: [number, number, number];
      isUnlocked: boolean;
      key: string;
    }> = [];

    Object.values(layout).forEach((node) => {
      node.parents.forEach((parentId) => {
        const parentNode = layout[parentId];
        if (parentNode) {
          // Line is unlocked if BOTH nodes are unlocked? Or just parent?
          // Usually path is open if parent is unlocked.
          const isUnlocked = unlockedTraits.includes(parentId);

          lines.push({
            start: parentNode.position,
            end: node.position,
            isUnlocked,
            key: `${parentId}-${node.traitId}`,
          });
        }
      });
    });
    return lines;
  }, [layout, unlockedTraits]);

  return (
    <div className="skill-tree-canvas-container">
      <Canvas>
        <Suspense fallback={null}>
          <PerspectiveCamera makeDefault position={[0, 0, 10]} fov={50} />

          {/* IMMERSIVE BACKGROUND */}
          <StarfieldBackground />

          {/* LIGHTING */}
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} intensity={1} color="#fbbf24" />
          <pointLight position={[-10, -10, -5]} intensity={0.5} color="#3b82f6" />
          <Environment preset="city" />

          {/* CONTROLS */}
          <OrbitControls
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            minDistance={5}
            maxDistance={20}
            maxPolarAngle={Math.PI / 1.5} // Don't allow going too far below
            minPolarAngle={Math.PI / 4}
          />

          {/* NODES */}
          <group>
            {Object.values(layout).map((node) => (
              <SkillNode3D
                key={node.traitId}
                id={node.traitId}
                position={node.position}
                iconType={node.iconType}
                // It is unlocked if it's in the list
                isUnlocked={unlockedTraits.includes(node.traitId)}
                isEquipped={equippedTraits.includes(node.traitId)}
                tier="GOLD" // TODO: Read from actual trait data if available, defaulting for visual demo
                label={node.traitId}
                onClick={onNodeClick}
              />
            ))}
          </group>

          {/* CONNECTIONS */}
          <group>
            {connections.map((conn) => (
              <ConnectionLine
                key={conn.key}
                start={conn.start}
                end={conn.end}
                isUnlocked={conn.isUnlocked}
              />
            ))}
          </group>

          {/* SHADOWS */}
          <ContactShadows position={[0, -4, 0]} opacity={0.4} scale={20} blur={2.5} far={4} />
        </Suspense>
      </Canvas>
    </div>
  );
};
