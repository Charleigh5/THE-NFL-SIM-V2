import React, { useMemo, useRef } from "react";
import * as THREE from "three";
import { useFrame } from "@react-three/fiber";
import { createStudioEnvironmentMap } from "./proceduralTextures";

export interface ProceduralLombardiTrophyProps {
  position?: [number, number, number];
  scale?: number;
  rotation?: [number, number, number];
  autoRotate?: boolean;
}

/**
 * The Vince Lombardi Trophy (100% Procedural & Offline)
 * - Authentic Tiffany & Co. Concave Trihedral Column Pedestal Base:
 *     Taper: R(y) = Rbase + (Rtop - Rbase) * (y / H)^0.94
 *     Face Concavity: Pface(lambda, y) = Pchord - 4*lambda*(1-lambda) * DeltaConcave * n_chord
 * - 45°-Tilted Regulation Silver Football atop collar cradle
 * - High-specular sterling silver chrome PBR (roughness: 0.04, metalness: 0.98)
 * - 100% In-memory procedural studio softbox reflection map attached to scene.environment
 */
export const ProceduralLombardiTrophy: React.FC<ProceduralLombardiTrophyProps> = ({
  position = [0, -1.2, 0],
  scale = 0.95,
  rotation = [0, 0, 0],
  autoRotate = false,
}) => {
  const groupRef = useRef<THREE.Group>(null);

  // In-memory procedural studio softbox reflection map
  const studioEnvMap = useMemo(() => createStudioEnvironmentMap(), []);

  // 1. Procedural Concave Trihedral Pedestal Geometry
  const pedestalGeometry = useMemo(() => {
    const H = 2.4;
    const Rbase = 0.65;
    const Rtop = 0.28;
    const Ny = 36; // Height slices
    const Nlambda = 16; // Slices per triangular face

    const positions: number[] = [];
    const uvs: number[] = [];
    const indices: number[] = [];

    // Angles for the 3 apex corners of the trihedron (pointing forward/sides)
    const phiCorners = [
      Math.PI / 2, // Front-top corner
      Math.PI / 2 + (Math.PI * 2) / 3, // Rear left
      Math.PI / 2 + (Math.PI * 4) / 3, // Rear right
    ];

    const totalCols = 3 * Nlambda;

    for (let i = 0; i <= Ny; i++) {
      const yNorm = i / Ny;
      const y = yNorm * H;
      // Authentic power-law taper
      const R = Rbase + (Rtop - Rbase) * Math.pow(yNorm, 0.94);
      const deltaConcave = 0.09 * R;

      // Calculate the 3 corner positions at this height
      const corners: THREE.Vector3[] = phiCorners.map(
        (phi) => new THREE.Vector3(R * Math.cos(phi), y, R * Math.sin(phi))
      );

      for (let face = 0; face < 3; face++) {
        const cA = corners[face];
        const cB = corners[(face + 1) % 3];

        const phiA = phiCorners[face];
        let phiB = phiCorners[(face + 1) % 3];
        if (phiB < phiA) phiB += Math.PI * 2;
        const phiMid = (phiA + phiB) / 2;
        const nChord = new THREE.Vector3(Math.cos(phiMid), 0, Math.sin(phiMid));

        for (let j = 0; j < Nlambda; j++) {
          const lambda = j / Nlambda;
          const chordX = (1 - lambda) * cA.x + lambda * cB.x;
          const chordZ = (1 - lambda) * cA.z + lambda * cB.z;

          // Concave inward deflection
          const scoop = deltaConcave * 4 * lambda * (1 - lambda);
          const px = chordX - scoop * nChord.x;
          const pz = chordZ - scoop * nChord.z;

          positions.push(px, y, pz);
          uvs.push((face * Nlambda + j) / totalCols, yNorm);
        }
      }
      // Wrap-around duplicate vertex for smooth UV interpolation
      const cA = corners[0];
      positions.push(cA.x, y, cA.z);
      uvs.push(1.0, yNorm);
    }

    const rowStride = totalCols + 1;
    for (let i = 0; i < Ny; i++) {
      for (let j = 0; j < totalCols; j++) {
        const a = i * rowStride + j;
        const b = (i + 1) * rowStride + j;
        const c = (i + 1) * rowStride + (j + 1);
        const d = i * rowStride + (j + 1);

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

  // 2. Regulation Silver Football Geometry (45-degree tilted atop pedestal)
  const silverBallGeometry = useMemo(() => {
    const Nu = 36;
    const Nv = 48;
    const c = 0.58;
    const a = 0.35;

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
        const S = 1.0 - 0.038 * Math.pow(Math.cos(4 * v), 16);
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

  useFrame((_, delta) => {
    if (autoRotate && groupRef.current) {
      groupRef.current.rotation.y += delta * 0.3;
    }
  });

  return (
    <group ref={groupRef} position={position} scale={scale} rotation={rotation}>
      {/* Declarative studio reflection map attached to scene environment */}
      <primitive object={studioEnvMap} attach="environment" />

      {/* 1. Base Beveled Plinth Plate */}
      <mesh position={[0, -0.04, 0]}>
        <cylinderGeometry args={[0.68, 0.72, 0.08, 32]} />
        <meshStandardMaterial color="#0B0E14" roughness={0.3} metalness={0.8} />
      </mesh>

      {/* 2. Main Concave Trihedral Column Pedestal */}
      <mesh geometry={pedestalGeometry} castShadow receiveShadow>
        <meshStandardMaterial
          color="#F2F5F8"
          roughness={0.04}
          metalness={0.98}
          envMap={studioEnvMap}
          envMapIntensity={2.8}
        />
      </mesh>

      {/* 3. Collar Mount Collar at y = 2.4 */}
      <mesh position={[0, 2.4, 0]}>
        <cylinderGeometry args={[0.29, 0.28, 0.05, 32]} />
        <meshStandardMaterial
          color="#F2F5F8"
          roughness={0.05}
          metalness={0.98}
          envMap={studioEnvMap}
          envMapIntensity={2.5}
        />
      </mesh>

      {/* 4. Cradle Mount Prongs */}
      <group position={[0, 2.46, 0]}>
        <mesh position={[0, 0.04, 0]}>
          <cylinderGeometry args={[0.16, 0.25, 0.08, 24]} />
          <meshStandardMaterial
            color="#EAEFF4"
            roughness={0.06}
            metalness={0.96}
            envMap={studioEnvMap}
          />
        </mesh>
      </group>

      {/* 5. 45°-Tilted Regulation Silver Football atop Collar */}
      <group position={[0, 2.86, 0]} rotation={[Math.PI / 4, Math.PI / 4, Math.PI / 12]}>
        <mesh geometry={silverBallGeometry} castShadow receiveShadow>
          <meshStandardMaterial
            color="#F2F5F8"
            roughness={0.04}
            metalness={0.98}
            envMap={studioEnvMap}
            envMapIntensity={3.0}
          />
        </mesh>

        {/* 6. Silver Raised Seams & Laces */}
        <mesh position={[0.35 * (1.0 - 0.038) + 0.007, 0, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <capsuleGeometry args={[0.009, 0.44, 8, 12]} />
          <meshStandardMaterial
            color="#FFFFFF"
            roughness={0.08}
            metalness={0.95}
            envMap={studioEnvMap}
          />
        </mesh>

        {[-0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15].map((z, idx) => (
          <mesh key={`silver-lace-${idx}`} position={[0.35 * (1.0 - 0.038) + 0.01, 0, z]}>
            <capsuleGeometry args={[0.01, 0.08, 6, 8]} />
            <meshStandardMaterial
              color="#FFFFFF"
              roughness={0.06}
              metalness={0.96}
              envMap={studioEnvMap}
            />
          </mesh>
        ))}
      </group>

      {/* 7. Front Engraving Inscription Plate Badge */}
      <group position={[0, 1.15, 0.46]} rotation={[-0.08, 0, 0]}>
        <mesh>
          <planeGeometry args={[0.32, 0.42]} />
          <meshStandardMaterial color="#141C28" roughness={0.4} metalness={0.7} />
        </mesh>
        {/* Embossed NFL Shield Outline */}
        <mesh position={[0, 0.12, 0.005]}>
          <boxGeometry args={[0.09, 0.11, 0.004]} />
          <meshStandardMaterial color="#F4D03F" roughness={0.2} metalness={0.9} />
        </mesh>
      </group>
    </group>
  );
};
