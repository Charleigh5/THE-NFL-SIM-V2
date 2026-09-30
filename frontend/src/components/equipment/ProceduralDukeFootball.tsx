import React, { useMemo, useRef } from "react";
import * as THREE from "three";
import { useFrame } from "@react-three/fiber";
import { createDukeFootballTextures } from "./proceduralTextures";

export interface ProceduralDukeFootballProps {
  position?: [number, number, number];
  scale?: number;
  rotation?: [number, number, number];
  autoRotate?: boolean;
}

/**
 * "The Duke" Regulation NFL Game Football (100% Procedural & Offline)
 * - Parametric Prolate Spheroid with cusped tips: R(u) = a * cos(u) * (1 - 0.14 * sin^2(u))
 * - 4-meridian cosine seam troughs: S(v) = 1 - 0.038 * cos^16(4v)
 * - In-memory Horween pebble leather grain bump map, dual white tip stripes, gold foil branding
 * - 3D capsule laces (8 cross-laces, longitudinal spine ridge, and 16 grommet eyelets)
 */
export const ProceduralDukeFootball: React.FC<ProceduralDukeFootballProps> = ({
  position = [0, 0, 0],
  scale = 1.0,
  rotation = [0.2, 0.4, 0.1],
  autoRotate = false,
}) => {
  const groupRef = useRef<THREE.Group>(null);

  // Generate procedural geometry for prolate spheroid with cusps and 4-panel seam troughs
  const ballGeometry = useMemo(() => {
    const Nu = 48; // polar segments
    const Nv = 64; // azimuthal segments
    const c = 1.0; // half length
    const a = 0.6; // equatorial radius

    const positions: number[] = [];
    const uvs: number[] = [];
    const indices: number[] = [];

    for (let i = 0; i <= Nu; i++) {
      const u = -Math.PI / 2 + (i / Nu) * Math.PI;
      const sinU = Math.sin(u);
      const cosU = Math.cos(u);
      const z = c * sinU;
      const R = a * cosU * (1.0 - 0.14 * sinU * sinU);

      for (let j = 0; j <= Nv; j++) {
        const v = (j / Nv) * Math.PI * 2;
        const cos4v = Math.cos(4 * v);
        const cos4vPow16 = Math.pow(cos4v, 16);
        const S = 1.0 - 0.038 * cos4vPow16;

        const x = R * Math.cos(v) * S;
        const y = R * Math.sin(v) * S;

        positions.push(x, y, z);
        uvs.push(j / Nv, i / Nu);
      }
    }

    for (let i = 0; i < Nu; i++) {
      for (let j = 0; j < Nv; j++) {
        const row1 = i * (Nv + 1);
        const row2 = (i + 1) * (Nv + 1);

        const aIdx = row1 + j;
        const bIdx = row2 + j;
        const cIdx = row2 + (j + 1);
        const dIdx = row1 + (j + 1);

        indices.push(aIdx, bIdx, dIdx);
        indices.push(bIdx, cIdx, dIdx);
      }
    }

    const geom = new THREE.BufferGeometry();
    geom.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
    geom.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
    geom.setIndex(indices);
    geom.computeVertexNormals();
    return geom;
  }, []);

  // In-memory procedural Horween leather bump and color textures
  const { colorMap, bumpMap } = useMemo(() => createDukeFootballTextures(), []);

  // 8 Transverse Cross-Laces & Eyelets coordinates along v = 0
  const lacePoints = useMemo(() => {
    const c = 1.0;
    const a = 0.6;
    const items: Array<{
      z: number;
      x: number;
      u: number;
    }> = [];

    for (let i = 0; i < 8; i++) {
      const z = -0.35 + (i / 7) * 0.7;
      const u = Math.asin(z / c);
      const cosU = Math.cos(u);
      const sinU = Math.sin(u);
      const R = a * cosU * (1.0 - 0.14 * sinU * sinU) * (1.0 - 0.038);
      items.push({ z, x: R + 0.012, u });
    }
    return items;
  }, []);

  useFrame((_, delta) => {
    if (autoRotate && groupRef.current) {
      groupRef.current.rotation.y += delta * 0.4;
    }
  });

  return (
    <group ref={groupRef} position={position} scale={scale} rotation={rotation}>
      {/* 1. Procedural Football Body Mesh */}
      <mesh geometry={ballGeometry} castShadow receiveShadow>
        <meshStandardMaterial
          map={colorMap}
          bumpMap={bumpMap}
          bumpScale={0.018}
          roughness={0.62}
          metalness={0.08}
        />
      </mesh>

      {/* 2. Longitudinal Center Seam Spine Stitch */}
      <mesh position={[0.6 * (1.0 - 0.038) + 0.008, 0, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <capsuleGeometry args={[0.011, 0.72, 8, 12]} />
        <meshStandardMaterial color="#F4F2EB" roughness={0.45} metalness={0.05} />
      </mesh>

      {/* 3. 8 3D Capsule Cross-Laces */}
      {lacePoints.map((pt, idx) => (
        <group key={`lace-${idx}`} position={[pt.x, 0, pt.z]}>
          {/* Main Transverse Cross-Lace Capsule */}
          <mesh castShadow receiveShadow>
            <capsuleGeometry args={[0.014, 0.125, 8, 12]} />
            <meshStandardMaterial color="#F7F6F2" roughness={0.4} metalness={0.06} />
          </mesh>

          {/* Left Eyelet Grommet */}
          <mesh position={[-0.006, 0.072, 0]} rotation={[0, Math.PI / 2, 0]}>
            <torusGeometry args={[0.013, 0.004, 8, 16]} />
            <meshStandardMaterial color="#2B1A0F" roughness={0.3} metalness={0.8} />
          </mesh>

          {/* Right Eyelet Grommet */}
          <mesh position={[-0.006, -0.072, 0]} rotation={[0, Math.PI / 2, 0]}>
            <torusGeometry args={[0.013, 0.004, 8, 16]} />
            <meshStandardMaterial color="#2B1A0F" roughness={0.3} metalness={0.8} />
          </mesh>
        </group>
      ))}
    </group>
  );
};
