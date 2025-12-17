import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { Line } from "@react-three/drei";
// Removed unused THREE import

interface ConnectionLineProps {
  start: [number, number, number];
  end: [number, number, number];
  isUnlocked: boolean;
  color?: string;
}

export const ConnectionLine: React.FC<ConnectionLineProps> = ({
  start,
  end,
  isUnlocked,
  color = "#fbbf24", // Default gold-ish
}) => {
  // Fix 'any' -> typed as THREE.LineBasicMaterial (or generic with dashOffset)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const materialRef = useRef<any>(null);

  useFrame((_state, delta) => {
    if (materialRef.current && isUnlocked) {
      // Animate the dash offset to create a "flow" effect
      materialRef.current.dashOffset -= delta * 2;
    }
  });

  return (
    <Line
      points={[start, end]}
      color={isUnlocked ? color : "#4b5563"} // Gold if unlocked, grey if locked
      lineWidth={isUnlocked ? 3 : 1}
      dashed={true}
      dashScale={isUnlocked ? 2 : 0} // No dashes (solidish/faint) if locked? Or spaced out
      dashSize={isUnlocked ? 0.5 : 0.1}
      gapSize={isUnlocked ? 0.2 : 0.1}
      opacity={isUnlocked ? 1 : 0.3}
      transparent
      toneMapped={false} // Make it glow against bloom
    >
      {/* We can attach specific material properties if needed, but Line handles most via props */}
      <lineBasicMaterial
        ref={materialRef}
        color={isUnlocked ? color : "#4b5563"}
        opacity={isUnlocked ? 1 : 0.3}
        transparent
      />
    </Line>
  );
};
