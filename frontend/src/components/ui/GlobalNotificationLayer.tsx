import React from "react";
import { Canvas } from "@react-three/fiber";
import { useNotificationStore } from "../../store/useNotificationStore";
import ImmersiveNotification from "./ImmersiveNotification";

const GlobalNotificationLayer: React.FC = () => {
  const notifications = useNotificationStore((state) => state.notifications);

  if (notifications.length === 0) return null;

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        pointerEvents: "none", // Let clicks pass through to app
        zIndex: 9999,
      }}
    >
      <Canvas
        camera={{ position: [0, 0, 10], fov: 50 }}
        gl={{ alpha: true, antialias: true }}
        style={{ pointerEvents: "auto" }} // But capture events on canvas objects? No, we want canvas transparent but objects interactive.
        // Actually, for R3F, pointerEvents: "none" on container and "auto" on Canvas usually works if we want to interact with 3D objects.
        // But here the Canvas covers the whole screen. We need `eventSource` or similar to handle partial interaction.
        // For simplicity, let's keep pointerEvents auto on the container ONLY if there is a notification, but that blocks the app.
        // Solution: Use R3F's event system.
      >
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        {notifications.map((notif, index) => (
          <ImmersiveNotification key={notif.id} data={notif} index={index} />
        ))}
      </Canvas>
    </div>
  );
};

export default GlobalNotificationLayer;
