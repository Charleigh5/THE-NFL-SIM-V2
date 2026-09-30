import * as THREE from "three";

let cachedStudioEnvMap: THREE.CanvasTexture | null = null;
let cachedFootballTextures: {
  colorMap: THREE.CanvasTexture;
  bumpMap: THREE.CanvasTexture;
} | null = null;

/**
 * Creates an in-memory 512x256 equirectangular studio softbox reflection map.
 * 100% Offline: Generates pure studio floodlights, lateral strip diffusers,
 * and ground ambient falloff with zero external network or CDN calls.
 */
export function createStudioEnvironmentMap(): THREE.CanvasTexture {
  if (cachedStudioEnvMap) {
    return cachedStudioEnvMap;
  }

  const width = 512;
  const height = 256;
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");

  if (!ctx) {
    const fallback = new THREE.CanvasTexture(canvas);
    fallback.mapping = THREE.EquirectangularReflectionMapping;
    return fallback;
  }

  // 1. Dark horizon studio base
  const bgGrad = ctx.createLinearGradient(0, 0, 0, height);
  bgGrad.addColorStop(0, "#080C14");
  bgGrad.addColorStop(0.5, "#0F172A");
  bgGrad.addColorStop(0.52, "#05080E");
  bgGrad.addColorStop(1, "#020408");
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, width, height);

  // 2. Zenith Key Softbox (Top-down Gaussian floodlight)
  const zenithGrad = ctx.createRadialGradient(
    width / 2,
    height * 0.15,
    5,
    width / 2,
    height * 0.15,
    width * 0.35
  );
  zenithGrad.addColorStop(0, "rgba(255, 255, 255, 1.0)");
  zenithGrad.addColorStop(0.3, "rgba(240, 245, 255, 0.85)");
  zenithGrad.addColorStop(0.7, "rgba(180, 210, 255, 0.25)");
  zenithGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = zenithGrad;
  ctx.fillRect(0, 0, width, height * 0.5);

  // 3. Left Lateral Strip Softbox (Azimuth ~ 60 deg)
  const leftX = width * 0.22;
  const stripW = width * 0.08;
  const leftStrip = ctx.createLinearGradient(leftX - stripW, 0, leftX + stripW, 0);
  leftStrip.addColorStop(0, "rgba(0, 0, 0, 0)");
  leftStrip.addColorStop(0.3, "rgba(255, 255, 255, 0.7)");
  leftStrip.addColorStop(0.5, "rgba(255, 255, 255, 0.95)");
  leftStrip.addColorStop(0.7, "rgba(255, 255, 255, 0.7)");
  leftStrip.addColorStop(1, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = leftStrip;
  ctx.fillRect(leftX - stripW, height * 0.1, stripW * 2, height * 0.55);

  // 4. Right Lateral Strip Softbox (Azimuth ~ 300 deg)
  const rightX = width * 0.78;
  const rightStrip = ctx.createLinearGradient(rightX - stripW, 0, rightX + stripW, 0);
  rightStrip.addColorStop(0, "rgba(0, 0, 0, 0)");
  rightStrip.addColorStop(0.3, "rgba(245, 250, 255, 0.65)");
  rightStrip.addColorStop(0.5, "rgba(255, 255, 255, 0.92)");
  rightStrip.addColorStop(0.7, "rgba(245, 250, 255, 0.65)");
  rightStrip.addColorStop(1, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = rightStrip;
  ctx.fillRect(rightX - stripW, height * 0.1, stripW * 2, height * 0.55);

  // 5. Rim Accent Fill (Warm golden horizon kicker)
  const rimGrad = ctx.createRadialGradient(
    width * 0.5,
    height * 0.48,
    10,
    width * 0.5,
    height * 0.48,
    width * 0.45
  );
  rimGrad.addColorStop(0, "rgba(255, 215, 160, 0.22)");
  rimGrad.addColorStop(0.6, "rgba(100, 150, 255, 0.08)");
  rimGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = rimGrad;
  ctx.fillRect(0, height * 0.25, width, height * 0.35);

  const texture = new THREE.CanvasTexture(canvas);
  texture.mapping = THREE.EquirectangularReflectionMapping;
  texture.needsUpdate = true;

  cachedStudioEnvMap = texture;
  return texture;
}

/**
 * Creates in-memory procedural color and bump maps for "The Duke" regulation game ball.
 * Generates Voronoi pebble leather grain, dual regulation tip stripes,
 * and hot-stamped gold foil branding ("★ THE DUKE ★").
 */
export function createDukeFootballTextures(): {
  colorMap: THREE.CanvasTexture;
  bumpMap: THREE.CanvasTexture;
} {
  if (cachedFootballTextures) {
    return cachedFootballTextures;
  }

  const width = 1024;
  const height = 512;

  // --- 1. Color Map Canvas ---
  const colorCanvas = document.createElement("canvas");
  colorCanvas.width = width;
  colorCanvas.height = height;
  const colorCtx = colorCanvas.getContext("2d");

  // --- 2. Bump Map Canvas ---
  const bumpCanvas = document.createElement("canvas");
  bumpCanvas.width = width;
  bumpCanvas.height = height;
  const bumpCtx = bumpCanvas.getContext("2d");

  if (!colorCtx || !bumpCtx) {
    const fallbackColor = new THREE.CanvasTexture(colorCanvas);
    const fallbackBump = new THREE.CanvasTexture(bumpCanvas);
    return { colorMap: fallbackColor, bumpMap: fallbackBump };
  }

  // A. Base Horween Leather Gradient (Equator rich cognac to pole espresso)
  const leatherGrad = colorCtx.createLinearGradient(0, 0, width, 0);
  leatherGrad.addColorStop(0, "#481E08");
  leatherGrad.addColorStop(0.2, "#6E2D0C");
  leatherGrad.addColorStop(0.5, "#7A3510");
  leatherGrad.addColorStop(0.8, "#6E2D0C");
  leatherGrad.addColorStop(1, "#481E08");
  colorCtx.fillStyle = leatherGrad;
  colorCtx.fillRect(0, 0, width, height);

  // Neutral grey bump base (128)
  bumpCtx.fillStyle = "#808080";
  bumpCtx.fillRect(0, 0, width, height);

  // B. Voronoi Pebble Grain Generation
  // Uses a deterministic jittered cellular lattice for realistic pebble stippling
  const cellW = 8;
  const cellH = 8;
  const cols = Math.floor(width / cellW);
  const rows = Math.floor(height / cellH);

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      // Deterministic pseudo-random jitter based on cell coordinates
      const seed = (r * 131 + c * 359) % 1000;
      const jx = (seed % 5) - 2;
      const jy = ((seed * 7) % 5) - 2;
      const cx = c * cellW + cellW / 2 + jx;
      const cy = r * cellH + cellH / 2 + jy;
      const radius = 2.4 + (seed % 3) * 0.5;

      // Color pebble (dark crevice rim + warm raised center)
      colorCtx.beginPath();
      colorCtx.arc(cx, cy, radius + 0.8, 0, Math.PI * 2);
      colorCtx.fillStyle = "rgba(35, 12, 4, 0.42)";
      colorCtx.fill();

      colorCtx.beginPath();
      colorCtx.arc(cx - 0.5, cy - 0.5, radius * 0.75, 0, Math.PI * 2);
      colorCtx.fillStyle = "rgba(195, 95, 35, 0.28)";
      colorCtx.fill();

      // Bump pebble (crevice valley ~60, peak ~220)
      bumpCtx.beginPath();
      bumpCtx.arc(cx, cy, radius + 0.9, 0, Math.PI * 2);
      bumpCtx.fillStyle = "#3C3C3C";
      bumpCtx.fill();

      bumpCtx.beginPath();
      bumpCtx.arc(cx - 0.6, cy - 0.6, radius * 0.7, 0, Math.PI * 2);
      bumpCtx.fillStyle = "#E0E0E0";
      bumpCtx.fill();
    }
  }

  // C. Dual Regulation White Tip Stripes
  // Tip 1: x in [width * 0.12, width * 0.17]
  // Tip 2: x in [width * 0.83, width * 0.88]
  const renderStripe = (xStart: number, stripeWidth: number) => {
    // Semi-transparent base white band
    colorCtx.fillStyle = "rgba(242, 244, 248, 0.92)";
    colorCtx.fillRect(xStart, 0, stripeWidth, height);

    // Weathered stripe edges
    for (let y = 0; y < height; y += 4) {
      const edgeNoise = ((y * 37) % 7) - 3;
      colorCtx.fillStyle = "rgba(110, 45, 12, 0.35)";
      colorCtx.fillRect(xStart + edgeNoise, y, 2, 4);
      colorCtx.fillRect(xStart + stripeWidth - 2 + edgeNoise, y, 2, 4);
    }

    // Slightly raised bump map for painted stripe
    bumpCtx.fillStyle = "#A8A8A8";
    bumpCtx.fillRect(xStart, 0, stripeWidth, height);
  };

  const stripeW = width * 0.045;
  renderStripe(width * 0.13, stripeW);
  renderStripe(width * 0.825, stripeW);

  // D. Hot-Stamped Gold Foil Branding ("★ THE DUKE ★")
  // Center panel on the upper quadrant (away from laces seam)
  const stampX = width * 0.5;
  const stampY = height * 0.28;

  colorCtx.save();
  colorCtx.textAlign = "center";
  colorCtx.textBaseline = "middle";

  // Gold drop shadow
  colorCtx.fillStyle = "rgba(40, 20, 5, 0.7)";
  colorCtx.font = "bold 26px Georgia, serif";
  colorCtx.fillText("★  THE DUKE  ★", stampX + 1, stampY + 2);

  // Metallic gold fill
  colorCtx.fillStyle = "#E8C258";
  colorCtx.fillText("★  THE DUKE  ★", stampX, stampY);

  colorCtx.font = "bold 13px 'Courier New', monospace";
  colorCtx.fillStyle = "rgba(40, 20, 5, 0.7)";
  colorCtx.fillText("OFFICIAL NATIONAL FOOTBALL LEAGUE", stampX + 1, stampY + 26);
  colorCtx.fillStyle = "#D4AF37";
  colorCtx.fillText("OFFICIAL NATIONAL FOOTBALL LEAGUE", stampX, stampY + 24);

  colorCtx.restore();

  // Emboss gold text into bump map
  bumpCtx.save();
  bumpCtx.textAlign = "center";
  bumpCtx.textBaseline = "middle";
  bumpCtx.font = "bold 26px Georgia, serif";
  bumpCtx.fillStyle = "#FAFAFA";
  bumpCtx.fillText("★  THE DUKE  ★", stampX, stampY);
  bumpCtx.font = "bold 13px 'Courier New', monospace";
  bumpCtx.fillStyle = "#EAEAEA";
  bumpCtx.fillText("OFFICIAL NATIONAL FOOTBALL LEAGUE", stampX, stampY + 24);
  bumpCtx.restore();

  // Create Three.js textures
  const colorMap = new THREE.CanvasTexture(colorCanvas);
  colorMap.wrapS = THREE.RepeatWrapping;
  colorMap.wrapT = THREE.ClampToEdgeWrapping;
  colorMap.colorSpace = THREE.SRGBColorSpace;
  colorMap.needsUpdate = true;

  const bumpMap = new THREE.CanvasTexture(bumpCanvas);
  bumpMap.wrapS = THREE.RepeatWrapping;
  bumpMap.wrapT = THREE.ClampToEdgeWrapping;
  bumpMap.needsUpdate = true;

  cachedFootballTextures = { colorMap, bumpMap };
  return cachedFootballTextures;
}
