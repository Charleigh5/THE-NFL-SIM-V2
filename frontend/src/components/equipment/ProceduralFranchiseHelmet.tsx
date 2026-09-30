import React, { useMemo, useRef } from "react";
import * as THREE from "three";
import { useFrame } from "@react-three/fiber";
import { type HelmetFinishType, HELMET_FINISH_PRESETS } from "./types";

export type { HelmetFinishType };

export interface ProceduralFranchiseHelmetProps {
  position?: [number, number, number];
  scale?: number;
  rotation?: [number, number, number];
  primaryColor?: string;
  secondaryColor?: string;
  accentColor?: string;
  finish?: HelmetFinishType;
  autoRotate?: boolean;
}

/**
 * Procedural Franchise NFL Helmet (100% Procedural & Offline)
 * - Anatomical cranial dome shell with occipital flare: z' = z * (1 + 0.14 * cos^2(theta) * max(0, -z / rz))
 * - Circular ear cutouts at (+-0.72, -0.12, -0.04) with rubber grommet surrounds
 * - 3D Catmull-Rom tubular steel wireframe facemask (brow, nose, mouth, chin, and vertical nasal/outer struts)
 * - Impact-resistant polycarbonate eye shield (visor) with subtle tint
 * - Dynamic franchise colors (primary shell, secondary facemask/stripe, accent decals)
 * - Switchable PBR finishes: Gloss, Matte, and Metallic
 */
export const ProceduralFranchiseHelmet: React.FC<ProceduralFranchiseHelmetProps> = ({
  position = [0, 0, 0],
  scale = 1.0,
  rotation = [0.1, -0.4, 0],
  primaryColor = "#0076B6",
  secondaryColor = "#B0B7BC",
  accentColor = "#FFFFFF",
  finish = "gloss",
  autoRotate = false,
}) => {
  const groupRef = useRef<THREE.Group>(null);
  const finishConfig = HELMET_FINISH_PRESETS[finish] || HELMET_FINISH_PRESETS.gloss;

  // 1. Procedural Cranial Dome Shell with Occipital Flare & Face Cutout
  const shellGeometry = useMemo(() => {
    const rx = 0.86;
    const ry = 1.0;
    const rz = 1.04;

    const latSegments = 40;
    const lonSegments = 48;

    const positions: number[] = [];
    const uvs: number[] = [];
    const indices: number[] = [];

    // Latitude u in [0, PI] (0 = top crown, PI = bottom rim)
    // Longitude v in [-PI, PI] (0 = front, PI/-PI = rear occiput)
    for (let i = 0; i <= latSegments; i++) {
      const u = (i / latSegments) * Math.PI;
      const sinU = Math.sin(u);
      const cosU = Math.cos(u);

      for (let j = 0; j <= lonSegments; j++) {
        const v = -Math.PI + (j / lonSegments) * (Math.PI * 2);
        const cosV = Math.cos(v);
        const sinV = Math.sin(v);

        let x0 = sinU * sinV * rx;
        let y0 = cosU * ry;
        let z0 = sinU * cosV * rz;

        // Mathematical Occipital Flare for z0 < 0
        if (z0 < 0) {
          const theta = Math.atan2(y0, x0);
          const flareFactor = 1.0 + 0.14 * Math.pow(Math.cos(theta), 2) * Math.min(1.0, -z0 / rz);
          z0 *= flareFactor;
          // Flare downward at the back neck
          y0 -= 0.08 * Math.pow(Math.min(1.0, -z0 / rz), 2);
        }

        // Face opening indentation / boundary shaping:
        // Front region (z0 > 0.15 and y0 < 0.25):
        // Pull vertices backward or shape the brow and cheek flaps
        const isFaceZone = z0 > 0.1 && y0 < 0.25 && y0 > -0.45;
        if (isFaceZone) {
          const faceFactor = Math.max(0, 1.0 - Math.abs(x0) / 0.55);
          if (faceFactor > 0) {
            // Cut inward for face opening
            z0 -= 0.42 * faceFactor;
            x0 *= 1.0 - 0.25 * faceFactor;
          }
        }

        positions.push(x0, y0, z0);
        uvs.push(j / lonSegments, i / latSegments);
      }
    }

    for (let i = 0; i < latSegments; i++) {
      for (let j = 0; j < lonSegments; j++) {
        const row1 = i * (lonSegments + 1);
        const row2 = (i + 1) * (lonSegments + 1);

        const a = row1 + j;
        const b = row2 + j;
        const c = row2 + (j + 1);
        const d = row1 + (j + 1);

        indices.push(a, b, d);
        indices.push(b, c, d);
      }
    }

    const geom = new THREE.BufferGeometry();
    geom.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
    geom.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
    geom.setIndex(indices);
    geom.computeVertexNormals();
    return geom;
  }, []);

  // 2. 3D Catmull-Rom Spline Facemask Tubes
  const facemaskTubes = useMemo(() => {
    // A. Brow Bar
    const browCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-0.52, 0.14, 0.35),
      new THREE.Vector3(-0.35, 0.2, 0.62),
      new THREE.Vector3(0, 0.22, 0.72),
      new THREE.Vector3(0.35, 0.2, 0.62),
      new THREE.Vector3(0.52, 0.14, 0.35),
    ]);

    // B. Nose Bar
    const noseCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-0.48, 0.03, 0.42),
      new THREE.Vector3(-0.32, 0.04, 0.74),
      new THREE.Vector3(0, 0.05, 0.82),
      new THREE.Vector3(0.32, 0.04, 0.74),
      new THREE.Vector3(0.48, 0.03, 0.42),
    ]);

    // C. Mouth Bar
    const mouthCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-0.46, -0.1, 0.4),
      new THREE.Vector3(-0.3, -0.09, 0.72),
      new THREE.Vector3(0, -0.08, 0.79),
      new THREE.Vector3(0.3, -0.09, 0.72),
      new THREE.Vector3(0.46, -0.1, 0.4),
    ]);

    // D. Chin Guard Bar
    const chinCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-0.42, -0.22, 0.36),
      new THREE.Vector3(-0.25, -0.21, 0.66),
      new THREE.Vector3(0, -0.2, 0.73),
      new THREE.Vector3(0.25, -0.21, 0.66),
      new THREE.Vector3(0.42, -0.22, 0.36),
    ]);

    // E. Left & Right Nasal Bridge Struts
    const leftNasalCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-0.075, 0.22, 0.71),
      new THREE.Vector3(-0.075, 0.05, 0.81),
      new THREE.Vector3(-0.075, -0.08, 0.78),
      new THREE.Vector3(-0.075, -0.2, 0.72),
    ]);

    const rightNasalCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0.075, 0.22, 0.71),
      new THREE.Vector3(0.075, 0.05, 0.81),
      new THREE.Vector3(0.075, -0.08, 0.78),
      new THREE.Vector3(0.075, -0.2, 0.72),
    ]);

    // F. Outer Cage Struts
    const leftOuterCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-0.26, 0.18, 0.64),
      new THREE.Vector3(-0.26, 0.04, 0.74),
      new THREE.Vector3(-0.26, -0.09, 0.72),
      new THREE.Vector3(-0.24, -0.21, 0.66),
    ]);

    const rightOuterCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0.26, 0.18, 0.64),
      new THREE.Vector3(0.26, 0.04, 0.74),
      new THREE.Vector3(0.26, -0.09, 0.72),
      new THREE.Vector3(0.24, -0.21, 0.66),
    ]);

    const tubeRadius = 0.015;
    const radialSegs = 8;
    const tubularSegs = 28;

    return [
      new THREE.TubeGeometry(browCurve, tubularSegs, tubeRadius, radialSegs, false),
      new THREE.TubeGeometry(noseCurve, tubularSegs, tubeRadius, radialSegs, false),
      new THREE.TubeGeometry(mouthCurve, tubularSegs, tubeRadius, radialSegs, false),
      new THREE.TubeGeometry(chinCurve, tubularSegs, tubeRadius, radialSegs, false),
      new THREE.TubeGeometry(leftNasalCurve, 20, tubeRadius, radialSegs, false),
      new THREE.TubeGeometry(rightNasalCurve, 20, tubeRadius, radialSegs, false),
      new THREE.TubeGeometry(leftOuterCurve, 20, tubeRadius, radialSegs, false),
      new THREE.TubeGeometry(rightOuterCurve, 20, tubeRadius, radialSegs, false),
    ];
  }, []);

  useFrame((_, delta) => {
    if (autoRotate && groupRef.current) {
      groupRef.current.rotation.y += delta * 0.35;
    }
  });

  return (
    <group ref={groupRef} position={position} scale={scale} rotation={rotation}>
      {/* 1. Main Cranial Dome Shell */}
      <mesh geometry={shellGeometry} castShadow receiveShadow>
        <meshPhysicalMaterial
          color={primaryColor}
          roughness={finishConfig.roughness}
          metalness={finishConfig.metalness}
          clearcoat={finishConfig.clearcoat}
          clearcoatRoughness={finishConfig.clearcoatRoughness}
        />
      </mesh>

      {/* 2. Inner Shock-Absorbing Foam Padding Liner */}
      <mesh scale={[0.93, 0.93, 0.93]}>
        <sphereGeometry args={[0.92, 32, 24]} />
        <meshStandardMaterial color="#141414" roughness={0.88} metalness={0.05} />
      </mesh>

      {/* 3. Circular Ear Cutout Rings at (+-0.72, -0.12, -0.04) */}
      <group position={[-0.72, -0.12, -0.04]} rotation={[0, Math.PI / 2, 0]}>
        <mesh>
          <torusGeometry args={[0.075, 0.016, 8, 24]} />
          <meshStandardMaterial color="#1C1C1C" roughness={0.7} metalness={0.2} />
        </mesh>
        <mesh position={[0, 0, -0.01]}>
          <cylinderGeometry args={[0.07, 0.07, 0.02, 24]} />
          <meshStandardMaterial color="#0A0A0A" roughness={0.9} metalness={0.1} />
        </mesh>
      </group>

      <group position={[0.72, -0.12, -0.04]} rotation={[0, -Math.PI / 2, 0]}>
        <mesh>
          <torusGeometry args={[0.075, 0.016, 8, 24]} />
          <meshStandardMaterial color="#1C1C1C" roughness={0.7} metalness={0.2} />
        </mesh>
        <mesh position={[0, 0, -0.01]}>
          <cylinderGeometry args={[0.07, 0.07, 0.02, 24]} />
          <meshStandardMaterial color="#0A0A0A" roughness={0.9} metalness={0.1} />
        </mesh>
      </group>

      {/* 4. Center Ridge Ribbon Stripes (Primary - Secondary - Accent) */}
      <group position={[0, 0.01, 0]}>
        {/* Main Secondary Center Stripe */}
        <mesh position={[0, 0.48, 0.05]} rotation={[-Math.PI / 16, 0, 0]}>
          <boxGeometry args={[0.07, 0.85, 1.7]} />
          <meshStandardMaterial color={secondaryColor} roughness={0.25} metalness={0.2} />
        </mesh>
        {/* Accent Flank Stripes */}
        <mesh position={[-0.055, 0.48, 0.05]} rotation={[-Math.PI / 16, 0, 0]}>
          <boxGeometry args={[0.015, 0.84, 1.68]} />
          <meshStandardMaterial color={accentColor} roughness={0.25} metalness={0.2} />
        </mesh>
        <mesh position={[0.055, 0.48, 0.05]} rotation={[-Math.PI / 16, 0, 0]}>
          <boxGeometry args={[0.015, 0.84, 1.68]} />
          <meshStandardMaterial color={accentColor} roughness={0.25} metalness={0.2} />
        </mesh>
      </group>

      {/* 5. Catmull-Rom Tubular Facemask Cage */}
      <group>
        {facemaskTubes.map((geom, i) => (
          <mesh key={`tube-${i}`} geometry={geom} castShadow receiveShadow>
            <meshStandardMaterial color={secondaryColor} roughness={0.32} metalness={0.7} />
          </mesh>
        ))}
      </group>

      {/* 6. Polycarbonate Eye Shield (Visor) */}
      <mesh position={[0, 0.06, 0.48]} rotation={[0, 0, 0]}>
        <cylinderGeometry args={[0.49, 0.49, 0.22, 32, 1, true, -Math.PI * 0.32, Math.PI * 0.64]} />
        <meshPhysicalMaterial
          color="#0F172A"
          transmission={0.72}
          roughness={0.06}
          ior={1.52}
          transparent
          opacity={0.85}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* 7. Visor Mount Clips / Hardware */}
      <mesh position={[-0.32, 0.14, 0.58]}>
        <boxGeometry args={[0.03, 0.05, 0.04]} />
        <meshStandardMaterial color={accentColor} roughness={0.3} metalness={0.8} />
      </mesh>
      <mesh position={[0.32, 0.14, 0.58]}>
        <boxGeometry args={[0.03, 0.05, 0.04]} />
        <meshStandardMaterial color={accentColor} roughness={0.3} metalness={0.8} />
      </mesh>
    </group>
  );
};
