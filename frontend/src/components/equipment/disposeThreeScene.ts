import * as THREE from "three";

/**
 * Type guard for Three.js Texture instances without using `any`.
 */
function isTexture(value: unknown): value is THREE.Texture {
  return (
    value !== null &&
    typeof value === "object" &&
    "isTexture" in value &&
    Boolean((value as { isTexture?: boolean }).isTexture)
  );
}

/**
 * Disposes a material and all associated textures attached to standard PBR slots.
 */
export function disposeMaterial(material: THREE.Material): void {
  const record = material as unknown as Record<string, unknown>;
  for (const key of Object.keys(record)) {
    const prop = record[key];
    if (isTexture(prop)) {
      prop.dispose();
    }
  }
  material.dispose();
}

/**
 * Recursively disposes all geometries, materials, textures, and renderers within a Three.js scene graph.
 * Forces GPU context release on unmount via WEBGL_lose_context to prevent browser context exhaustion.
 */
export function disposeThreeScene(
  scene: THREE.Scene | THREE.Object3D,
  renderer?: THREE.WebGLRenderer | null
): void {
  if (!scene) return;

  scene.traverse((object: THREE.Object3D) => {
    if ("geometry" in object) {
      const mesh = object as THREE.Mesh;
      if (mesh.geometry) {
        mesh.geometry.dispose();
      }
    }

    if ("material" in object) {
      const mesh = object as THREE.Mesh;
      if (mesh.material) {
        if (Array.isArray(mesh.material)) {
          for (const mat of mesh.material) {
            disposeMaterial(mat);
          }
        } else {
          disposeMaterial(mesh.material);
        }
      }
    }
  });

  if (renderer) {
    try {
      renderer.dispose();
      const gl = renderer.getContext();
      if (gl) {
        const loseContext = gl.getExtension("WEBGL_lose_context");
        loseContext?.loseContext();
      }
    } catch {
      // Graceful fallback if context already severed
    }
  }
}
