import React, { useRef, useState, useEffect } from "react";
import type { ThreeEvent } from "@react-three/fiber";
import { Text, Html, RoundedBox } from "@react-three/drei";
import { useSpring, animated } from "@react-spring/three";
import { useNotificationStore } from "../../store/useNotificationStore";
import type { NotificationData } from "../../store/useNotificationStore";
import * as THREE from "three";

interface ImmersiveNotificationProps {
  data: NotificationData;
  index: number;
}

const ImmersiveNotification: React.FC<ImmersiveNotificationProps> = ({ data }) => {
  const meshRef = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);
  const removeNotification = useNotificationStore((state) => state.removeNotification);

  // Auto-dismiss logic
  useEffect(() => {
    if (hovered) return; // Pause if hovered

    const duration = data.duration || 3000;
    const timer = setTimeout(() => {
      removeNotification(data.id);
    }, duration);

    return () => clearTimeout(timer);
  }, [hovered, data.id, data.duration, removeNotification]);

  // Animation spring
  const { scale, position } = useSpring({
    scale: hovered ? 1.1 : 1,
    position: [0, 0, 0] as [number, number, number],
    config: { tension: 300, friction: 20 },
  });

  const trainingData = data.data; // BatchTrainingResponse

  return (
    <animated.group
      ref={meshRef}
      scale={scale}
      position={position as any}
      onPointerOver={(e: ThreeEvent<PointerEvent>) => {
        e.stopPropagation();
        setHovered(true);
      }}
      onPointerOut={() => setHovered(false)}
    >
      {/* Background Panel - Futuristic Glass Look */}
      <RoundedBox args={[6, 4, 0.2]} radius={0.1} smoothness={4}>
        <meshPhysicalMaterial
          color="#1a1a2e"
          roughness={0.2}
          metalness={0.8}
          transparent
          opacity={0.9}
          clearcoat={1}
        />
      </RoundedBox>

      {/* Border Glow */}
      <RoundedBox args={[6.1, 4.1, 0.1]} radius={0.1} smoothness={4}>
        <meshBasicMaterial color="#00d4ff" transparent opacity={0.3} wireframe />
      </RoundedBox>

      {/* Content */}
      <group position={[0, 0, 0.15]}>
        {/* Title */}
        <Text
          position={[0, 1.5, 0]}
          fontSize={0.4}
          color="#ffffff"
          anchorX="center"
          anchorY="middle"
        >
          TRAINING REPORT
        </Text>

        {/* Stats Grid */}
        <group position={[-1.5, 0.5, 0]}>
          <Text fontSize={0.25} color="#4ade80" anchorX="center">
            XP Gained
          </Text>
          <Text position={[0, -0.4, 0]} fontSize={0.5} color="#ffffff" anchorX="center">
            +{trainingData.total_xp_gained?.toFixed(0) || 0}
          </Text>
           {/* XP Bar Visualization */}
           <group position={[0, -0.9, 0]}>
             {/* Background Bar */}
             <RoundedBox args={[2, 0.15, 0.05]} radius={0.07} smoothness={4}>
               <meshBasicMaterial color="#334155" />
             </RoundedBox>
             {/* Fill Bar (Simulated 60% fill for visual flair) */}
             <group position={[-1, 0, 0.01]}>
               <RoundedBox args={[1.2, 0.15, 0.05]} radius={0.07} smoothness={4} position={[0.6, 0, 0]}>
                 <meshBasicMaterial color="#4ade80" />
               </RoundedBox>
             </group>
           </group>
        </group>

        <group position={[1.5, 0.5, 0]}>
          <Text
            fontSize={0.25}
            color={trainingData.injuries_occurred > 0 ? "#ef4444" : "#94a3b8"}
            anchorX="center"
          >
            Injuries
          </Text>
          <Text position={[0, -0.4, 0]} fontSize={0.5} color="#ffffff" anchorX="center">
            {trainingData.injuries_occurred || 0}
          </Text>
        </group>

        {/* Top Performers Preview */}
        <group position={[0, -1.0, 0]}>
          <Text fontSize={0.2} color="#cbd5e1" anchorX="center">
            Top Performer
          </Text>
          <Text position={[0, -0.3, 0]} fontSize={0.25} color="#ffd700" anchorX="center">
            {trainingData.top_performers?.[0]
              ? `Player #${trainingData.top_performers[0].player_id}`
              : "N/A"}
          </Text>
        </group>

        {/* Dismiss Button (HTML for better interaction) */}
        <Html position={[2.5, 1.5, 0]} transform>
          <button
            onClick={() => removeNotification(data.id)}
            style={{
              background: "rgba(255, 0, 0, 0.7)",
              border: "none",
              borderRadius: "50%",
              color: "white",
              width: "24px",
              height: "24px",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            X
          </button>
        </Html>
      </group>
    </animated.group>
  );
};

export default ImmersiveNotification;
