import React, { useEffect, useRef, useCallback } from "react";
import { useWeatherThemeStore } from "../../store/useWeatherThemeStore";
import { weatherAudio } from "../../services/weatherAudioService";

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  alpha: number;
  rotation: number;
  vRot: number;
  stuck: boolean;
  elementId?: string;
  type: "snow" | "rain" | "leaf" | "shimmer" | "splash" | "powder";
  life: number;
  maxLife: number;
}

interface SurfaceRect {
  id: string;
  left: number;
  right: number;
  top: number;
  bottom: number;
  snowHeights: number[]; // segmented accumulation across width
  maxSnowCap: number;
  drips: Array<{ x: number; currentY: number; vy: number; active: boolean }>;
}

const MAX_PARTICLES = 650;
const SNOW_SEGMENTS = 20;

export const DynamicWeatherFXOverlay: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const {
    condition,
    preset,
    lightningActive,
    lightningIntensity,
    snowAccumulationActive,
    audioEnabled,
    triggerLightning,
  } = useWeatherThemeStore();

  const surfacesRef = useRef<Map<string, SurfaceRect>>(new Map());
  const particlesRef = useRef<Particle[]>([]);
  const animationFrameRef = useRef<number | null>(null);
  const lastLightningCheckRef = useRef<number>(0);

  // Update registered DOM surfaces periodically or on scroll
  const updateSurfaces = useCallback(() => {
    if (typeof document === "undefined") return;

    // Scan interactive buttons, cards, and explicitly marked weather surfaces
    const elements = document.querySelectorAll<HTMLElement>(
      'button, [role="button"], [data-weather-surface="true"], .weather-card, a'
    );

    const nextSurfaces = new Map<string, SurfaceRect>();

    elements.forEach((el, index) => {
      const rect = el.getBoundingClientRect();
      // Skip off-screen or tiny elements
      if (rect.width < 20 || rect.height < 15) return;
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;
      if (rect.right < 0 || rect.left > window.innerWidth) return;

      const id =
        el.id || el.getAttribute("data-weather-id") || `surf-${index}-${Math.round(rect.top)}`;
      const existing = surfacesRef.current.get(id);

      nextSurfaces.set(id, {
        id,
        left: rect.left,
        right: rect.right,
        top: rect.top,
        bottom: rect.bottom,
        snowHeights: existing ? existing.snowHeights : new Array(SNOW_SEGMENTS).fill(0),
        maxSnowCap: Math.min(14, rect.height * 0.35),
        drips: existing ? existing.drips : [],
      });
    });

    surfacesRef.current = nextSurfaces;
  }, []);

  // Listen to DOM events to displace snow when user interacts with buttons
  useEffect(() => {
    const handleDisplace = (e: MouseEvent) => {
      // Check which surface was clicked/hovered
      surfacesRef.current.forEach((surf) => {
        if (
          e.clientX >= surf.left - 5 &&
          e.clientX <= surf.right + 5 &&
          e.clientY >= surf.top - 10 &&
          e.clientY <= surf.bottom + 5
        ) {
          // Dislodge accumulated snow into a flurry of airborne powder
          const hasSnow = surf.snowHeights.some((h) => h > 1);
          if (hasSnow) {
            for (let i = 0; i < SNOW_SEGMENTS; i++) {
              const segX = surf.left + (i / SNOW_SEGMENTS) * (surf.right - surf.left);
              const height = surf.snowHeights[i];
              if (height > 0.5) {
                // Spawn 2-3 powder particles per segment
                for (let k = 0; k < 3; k++) {
                  particlesRef.current.push({
                    x: segX + (Math.random() * 8 - 4),
                    y: surf.top - height * 0.5,
                    vx: (Math.random() - 0.5) * 3 + (preset.windSpeed > 0 ? 1 : -1),
                    vy: -(Math.random() * 2.5 + 1.2), // burst upwards and outwards
                    size: Math.random() * 2.5 + 1.5,
                    alpha: 0.95,
                    rotation: Math.random() * Math.PI,
                    vRot: (Math.random() - 0.5) * 0.2,
                    stuck: false,
                    type: "powder",
                    life: 0,
                    maxLife: 45 + Math.random() * 30,
                  });
                }
              }
            }
            // Reset snow
            surf.snowHeights.fill(0);
          }
        }
      });
    };

    window.addEventListener("scroll", updateSurfaces, { passive: true });
    window.addEventListener("resize", updateSurfaces, { passive: true });
    window.addEventListener("click", handleDisplace);
    window.addEventListener("mousemove", handleDisplace, { passive: true });

    const interval = setInterval(updateSurfaces, 1200);

    return () => {
      window.removeEventListener("scroll", updateSurfaces);
      window.removeEventListener("resize", updateSurfaces);
      window.removeEventListener("click", handleDisplace);
      window.removeEventListener("mousemove", handleDisplace);
      clearInterval(interval);
    };
  }, [updateSurfaces, preset.windSpeed]);

  // Manage Audio state
  useEffect(() => {
    if (!audioEnabled) {
      weatherAudio.stopAll();
      return;
    }

    if (condition === "ARROWHEAD_DOWNPOUR") {
      weatherAudio.startRain(preset.precipitationDensity);
    } else {
      weatherAudio.stopRain();
    }

    if (condition === "LAMBEAU_BLIZZARD") {
      weatherAudio.startWind(preset.windSpeed);
    } else {
      weatherAudio.stopWind();
    }

    return () => {
      weatherAudio.stopAll();
    };
  }, [audioEnabled, condition, preset.precipitationDensity, preset.windSpeed]);

  // Spawn and initialize particles
  useEffect(() => {
    const pType = preset.particleType;
    if (pType === "none") {
      particlesRef.current = [];
      return;
    }

    const count = Math.round(MAX_PARTICLES * preset.precipitationDensity);
    const particles: Particle[] = [];

    const width = window.innerWidth;
    const height = window.innerHeight;

    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * (width + 200) - 100,
        y: Math.random() * height,
        vx: (Math.cos(preset.windAngleRad) * preset.windSpeed) / 5,
        vy: pType === "rain" ? Math.random() * 14 + 18 : Math.random() * 2 + 1.5,
        size: pType === "rain" ? Math.random() * 1.5 + 1 : Math.random() * 3 + 1.5,
        alpha: Math.random() * 0.6 + 0.35,
        rotation: Math.random() * Math.PI * 2,
        vRot: (Math.random() - 0.5) * 0.08,
        stuck: false,
        type:
          pType === "snow"
            ? "snow"
            : pType === "rain"
              ? "rain"
              : pType === "leaves"
                ? "leaf"
                : "shimmer",
        life: 0,
        maxLife: 300,
      });
    }

    particlesRef.current = particles;
  }, [preset]);

  // Main 60 FPS Render Loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d", { alpha: true });
    if (!ctx) return;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      updateSurfaces();
    };

    window.addEventListener("resize", handleResize);

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // 1. Check for random thunderstorm lightning strikes
      if (condition === "ARROWHEAD_DOWNPOUR") {
        const now = Date.now();
        if (now - lastLightningCheckRef.current > 7000 && Math.random() < 0.008) {
          triggerLightning(0.9 + Math.random() * 0.3);
          if (audioEnabled) {
            weatherAudio.playThunderStrike(0.8 + Math.random() * 0.4);
          }
          lastLightningCheckRef.current = now;
        }
      }

      // 2. Draw Ambient Lightning Flash wash if active
      if (lightningActive && lightningIntensity > 0) {
        ctx.fillStyle = `rgba(220, 245, 255, ${Math.min(0.75, lightningIntensity * 0.55)})`;
        ctx.fillRect(0, 0, width, height);

        // Draw dynamic branching lightning bolt in the distance
        ctx.save();
        ctx.strokeStyle = `rgba(255, 255, 255, ${lightningIntensity * 0.9})`;
        ctx.lineWidth = 3;
        ctx.shadowColor = "#00f0ff";
        ctx.shadowBlur = 18;

        const startX = width * (0.3 + Math.random() * 0.4);
        let currX = startX;
        let currY = 0;

        ctx.beginPath();
        ctx.moveTo(currX, currY);
        while (currY < height * 0.75) {
          currX += (Math.random() - 0.5) * 45;
          currY += Math.random() * 35 + 15;
          ctx.lineTo(currX, currY);

          // Sub-branch
          if (Math.random() < 0.25) {
            ctx.moveTo(currX, currY);
            ctx.lineTo(currX + (Math.random() - 0.5) * 60, currY + Math.random() * 40 + 20);
            ctx.moveTo(currX, currY);
          }
        }
        ctx.stroke();
        ctx.restore();
      }

      // 3. Draw Snow Accumulation Caps on Surfaces (Blizzard Mode)
      if (snowAccumulationActive && condition === "LAMBEAU_BLIZZARD") {
        surfacesRef.current.forEach((surf) => {
          const w = surf.right - surf.left;
          const segWidth = w / SNOW_SEGMENTS;

          ctx.save();
          ctx.fillStyle = "rgba(245, 250, 255, 0.96)";
          ctx.shadowColor = "rgba(180, 220, 245, 0.6)";
          ctx.shadowBlur = 4;

          ctx.beginPath();
          ctx.moveTo(surf.left, surf.top);

          // Build smooth crest over button/card top
          for (let i = 0; i < SNOW_SEGMENTS; i++) {
            const sx = surf.left + i * segWidth;
            const h = surf.snowHeights[i];
            const nextH = surf.snowHeights[Math.min(SNOW_SEGMENTS - 1, i + 1)];
            const midX = sx + segWidth * 0.5;
            const midY = surf.top - (h + nextH) * 0.5;

            ctx.quadraticCurveTo(sx, surf.top - h, midX, midY);
          }

          ctx.lineTo(surf.right, surf.top);
          ctx.closePath();
          ctx.fill();

          // Highlight rim on snow cap
          ctx.strokeStyle = "rgba(255, 255, 255, 0.9)";
          ctx.lineWidth = 1;
          ctx.stroke();

          ctx.restore();
        });
      }

      // 4. Draw Rain Dripping & Rivulets off Bottom of Components (Downpour Mode)
      if (condition === "ARROWHEAD_DOWNPOUR") {
        surfacesRef.current.forEach((surf) => {
          // Manage existing drips
          if (surf.drips.length < 3 && Math.random() < 0.04) {
            // Form a new droplet on bottom border
            surf.drips.push({
              x: surf.left + Math.random() * (surf.right - surf.left),
              currentY: surf.bottom,
              vy: 0.2,
              active: true,
            });
          }

          surf.drips.forEach((drip) => {
            if (!drip.active) return;

            // Accelerate downward with gravity
            drip.vy += 0.35;
            drip.currentY += drip.vy;

            // Draw droplet with refraction highlight
            ctx.save();
            ctx.fillStyle = "rgba(180, 230, 255, 0.75)";
            ctx.beginPath();
            ctx.arc(drip.x, drip.currentY, 2.2, 0, Math.PI * 2);
            ctx.fill();

            // Water trail tail
            ctx.strokeStyle = "rgba(180, 230, 255, 0.3)";
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(drip.x, drip.currentY - Math.min(10, drip.vy * 1.5));
            ctx.lineTo(drip.x, drip.currentY);
            ctx.stroke();
            ctx.restore();

            // Deactivate when out of screen or falls past 200px
            if (drip.currentY > surf.bottom + 220 || drip.currentY > height) {
              drip.active = false;
            }
          });

          // Clean dead drips
          surf.drips = surf.drips.filter((d) => d.active);
        });
      }

      // 5. Update and Draw Moving Weather Particles
      const particles = particlesRef.current;
      const windVx = (Math.cos(preset.windAngleRad) * preset.windSpeed) / 4;

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        if (p.type === "powder") {
          // Powder particle from disrupted button snow
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.12; // gravity
          p.vx *= 0.97;
          p.life++;
          p.alpha = Math.max(0, 1 - p.life / p.maxLife);

          ctx.fillStyle = `rgba(240, 248, 255, ${p.alpha})`;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fill();

          if (p.life >= p.maxLife) {
            // Remove powder
            particles.splice(i, 1);
            i--;
          }
          continue;
        }

        // Standard environmental precipitation
        p.x += p.vx + windVx;
        p.y += p.vy;
        p.rotation += p.vRot;

        // Collision detection with surfaces for snow accumulation
        if (snowAccumulationActive && condition === "LAMBEAU_BLIZZARD" && p.type === "snow") {
          surfacesRef.current.forEach((surf) => {
            if (
              p.x >= surf.left &&
              p.x <= surf.right &&
              p.y >= surf.top - 4 &&
              p.y <= surf.top + 6 &&
              p.vy > 0
            ) {
              // Particle lands on surface top
              const relX = (p.x - surf.left) / (surf.right - surf.left);
              const segIdx = Math.min(
                SNOW_SEGMENTS - 1,
                Math.max(0, Math.floor(relX * SNOW_SEGMENTS))
              );
              if (surf.snowHeights[segIdx] < surf.maxSnowCap) {
                surf.snowHeights[segIdx] += 0.45;
                // Distribute slightly to adjacent segments for organic mound
                if (segIdx > 0) surf.snowHeights[segIdx - 1] += 0.2;
                if (segIdx < SNOW_SEGMENTS - 1) surf.snowHeights[segIdx + 1] += 0.2;
              }

              // Recycle particle to top
              p.y = -10;
              p.x = Math.random() * (width + 200) - 100;
            }
          });
        }

        // Draw particle based on type
        if (p.type === "snow") {
          ctx.save();
          ctx.fillStyle = `rgba(240, 248, 255, ${p.alpha})`;
          ctx.shadowColor = "rgba(180, 220, 255, 0.4)";
          ctx.shadowBlur = 3;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        } else if (p.type === "rain") {
          ctx.save();
          ctx.strokeStyle = `rgba(160, 225, 255, ${p.alpha})`;
          ctx.lineWidth = p.size * 0.8;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          // Angle streaks with wind
          ctx.lineTo(p.x + windVx * 2.2, p.y + p.vy * 0.9);
          ctx.stroke();
          ctx.restore();
        } else if (p.type === "leaf") {
          // Autumn swirling leaf
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate(p.rotation);
          ctx.fillStyle = p.size > 2.5 ? "rgba(225, 110, 40, 0.75)" : "rgba(200, 160, 40, 0.75)";
          ctx.beginPath();
          ctx.ellipse(0, 0, p.size * 2, p.size, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        } else if (p.type === "shimmer") {
          // Miami heat distortion / humidity particle
          ctx.save();
          ctx.fillStyle = `rgba(255, 80, 180, ${p.alpha * 0.45})`;
          ctx.beginPath();
          ctx.arc(p.x + Math.sin(p.y * 0.05) * 4, p.y, p.size, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        }

        // Screen wrap
        if (p.y > height + 20) {
          p.y = -10;
          p.x = Math.random() * (width + 200) - 100;
        }
        if (p.x > width + 100) p.x = -50;
        if (p.x < -100) p.x = width + 50;
      }

      animationFrameRef.current = requestAnimationFrame(render);
    };

    animationFrameRef.current = requestAnimationFrame(render);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      window.removeEventListener("resize", handleResize);
    };
  }, [
    condition,
    preset,
    lightningActive,
    lightningIntensity,
    snowAccumulationActive,
    audioEnabled,
    triggerLightning,
    updateSurfaces,
  ]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-50 w-full h-full"
      style={{
        mixBlendMode: condition === "VICE_HEATWAVE" ? "screen" : "normal",
      }}
    />
  );
};
