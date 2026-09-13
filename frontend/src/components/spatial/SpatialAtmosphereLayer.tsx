import React, { useState, useEffect, useMemo } from "react";

export type FacilityAtmosphereType =
  | "locker"
  | "office"
  | "weight_room"
  | "war_room"
  | "stadium"
  | "film_room";

export type WeatherType = "clear" | "rain" | "snow" | "dome";

export interface SpatialAtmosphereLayerProps {
  facilityType: FacilityAtmosphereType;
  weather?: WeatherType;
  className?: string;
  intensity?: "subtle" | "medium" | "cinematic";
}

interface ParticleConfig {
  id: number;
  left: string;
  top: string;
  size: number;
  duration: number;
  delay: number;
  opacity: number;
}

/**
 * Deterministic pseudo-random sequence for consistent particle positioning
 */
function createDeterministicParticles(count: number, seed: number): ParticleConfig[] {
  const particles: ParticleConfig[] = [];
  let s = seed;
  const pseudoRandom = () => {
    s = (s * 9301 + 49297) % 233280;
    return s / 233280;
  };

  for (let i = 0; i < count; i++) {
    particles.push({
      id: i,
      left: `${(pseudoRandom() * 96 + 2).toFixed(1)}%`,
      top: `${(pseudoRandom() * 90 + 5).toFixed(1)}%`,
      size: Number((pseudoRandom() * 2.5 + 1.2).toFixed(1)),
      duration: Number((pseudoRandom() * 8 + 6).toFixed(1)),
      delay: Number((pseudoRandom() * 5).toFixed(1)),
      opacity: Number((pseudoRandom() * 0.4 + 0.15).toFixed(2)),
    });
  }
  return particles;
}

/**
 * SpatialAtmosphereLayer
 * ======================
 * GPU-composited atmospheric FX layer positioned between the 2.5D background image
 * and the interactive UI planes.
 *
 * Adly Frontier UI Architect Principles:
 * - 100% pointer-events-none (never blocks user interaction)
 * - contain: layout paint (strict CSS layout containment)
 * - Pure hardware-accelerated transform3d / opacity keyframes
 * - Native prefers-reduced-motion fallback (static subtle overlays)
 */
export const SpatialAtmosphereLayer: React.FC<SpatialAtmosphereLayerProps> = ({
  facilityType,
  weather = "clear",
  className = "",
  intensity = "subtle",
}) => {
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReducedMotion(mediaQuery.matches);

    const handler = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, []);

  // Pre-generate deterministic particle sets
  const weightRoomChalkMotes = useMemo(() => createDeterministicParticles(18, 42), []);
  const filmRoomProjectorMotes = useMemo(() => createDeterministicParticles(24, 99), []);
  const officeDustMotes = useMemo(() => createDeterministicParticles(12, 137), []);
  const stadiumVaporMotes = useMemo(() => createDeterministicParticles(16, 211), []);

  const intensityMultiplier =
    intensity === "cinematic" ? 1.4 : intensity === "medium" ? 1.0 : 0.75;

  return (
    <div
      aria-hidden="true"
      data-testid={`spatial-atmosphere-${facilityType}`}
      className={`absolute inset-0 pointer-events-none overflow-hidden select-none z-0 spatial-atmosphere-layer ${className}`}
      style={{ contain: "layout paint" }}
    >
      <style>{`
        @keyframes warroom-flicker {
          0%, 100% { opacity: 0.98; }
          42% { opacity: 0.96; }
          43% { opacity: 1.0; }
          78% { opacity: 0.97; }
          80% { opacity: 0.99; }
        }

        @keyframes warroom-flare-pulse {
          0%, 100% {
            opacity: 0.35;
            transform: translate3d(0, 0, 0) scaleX(1);
          }
          50% {
            opacity: 0.65;
            transform: translate3d(0, 0, 0) scaleX(1.15);
          }
        }

        @keyframes locker-mist-drift {
          0% {
            transform: translate3d(-3%, 0, 0) scaleY(1);
            opacity: 0.35;
          }
          50% {
            transform: translate3d(3%, -8px, 0) scaleY(1.05);
            opacity: 0.55;
          }
          100% {
            transform: translate3d(-3%, 0, 0) scaleY(1);
            opacity: 0.35;
          }
        }

        @keyframes atmospheric-mote-float {
          0% {
            transform: translate3d(0, 0, 0);
          }
          50% {
            transform: translate3d(12px, -24px, 0);
          }
          100% {
            transform: translate3d(0, 0, 0);
          }
        }

        @keyframes chalk-drift {
          0% {
            transform: translate3d(-10px, 15px, 0);
            opacity: 0;
          }
          25% {
            opacity: 0.45;
          }
          75% {
            opacity: 0.45;
          }
          100% {
            transform: translate3d(25px, -45px, 0);
            opacity: 0;
          }
        }

        @keyframes rain-streak-fall {
          0% {
            transform: translate3d(0, -100%, 0);
          }
          100% {
            transform: translate3d(-20px, 100%, 0);
          }
        }

        @keyframes projector-shimmer {
          0%, 100% { opacity: 0.22; }
          50% { opacity: 0.38; }
        }

        @media (prefers-reduced-motion: reduce) {
          .spatial-animated-element {
            animation: none !important;
            transform: none !important;
          }
          .spatial-particle-mote {
            display: none !important;
          }
        }
      `}</style>

      {/* ========================================================================= */}
      {/* 1. WAR ROOM (Scene 07): CRT Scanlines, Ambient Monitor Glow, Screen Flicker & Optical Flare */}
      {/* ========================================================================= */}
      {facilityType === "war_room" && (
        <div
          className={`w-full h-full relative ${
            reducedMotion ? "" : "spatial-animated-element"
          }`}
          style={
            reducedMotion
              ? undefined
              : { animation: "warroom-flicker 8s ease-in-out infinite" }
          }
        >
          {/* Subtle CRT / Multi-Monitor Scanline Grid */}
          <div
            className="absolute inset-0 opacity-[0.14]"
            style={{
              backgroundImage:
                "repeating-linear-gradient(to bottom, transparent 0px, transparent 2px, rgba(0, 0, 0, 0.45) 2px, rgba(0, 0, 0, 0.45) 4px)",
              backgroundSize: "100% 4px",
            }}
          />

          {/* Multi-Screen Wall Ambient Cyan / Deep Blue Monitor Glows */}
          <div
            className="absolute top-1/4 left-1/5 w-[50vw] h-[35vh] rounded-full blur-[110px] pointer-events-none"
            style={{
              background: `radial-gradient(circle, rgba(0, 180, 255, ${
                0.15 * intensityMultiplier
              }) 0%, transparent 70%)`,
            }}
          />
          <div
            className="absolute bottom-1/4 right-1/6 w-[45vw] h-[40vh] rounded-full blur-[130px] pointer-events-none"
            style={{
              background: `radial-gradient(circle, rgba(37, 99, 235, ${
                0.14 * intensityMultiplier
              }) 0%, rgba(16, 185, 129, ${
                0.05 * intensityMultiplier
              }) 50%, transparent 75%)`,
            }}
          />

          {/* Central Blue Optical Flare Streak across Analytics Display Line */}
          <div
            className={`absolute top-[18%] left-0 right-0 h-[2px] pointer-events-none ${
              reducedMotion ? "" : "spatial-animated-element"
            }`}
            style={{
              background:
                "linear-gradient(90deg, transparent 0%, rgba(0, 118, 182, 0) 15%, rgba(0, 212, 255, 0.45) 50%, rgba(0, 118, 182, 0) 85%, transparent 100%)",
              filter: "blur(0.5px)",
              animation: reducedMotion
                ? undefined
                : "warroom-flare-pulse 6s ease-in-out infinite",
            }}
          />

          {/* Soft Optical Flare Core Starburst */}
          <div
            className="absolute top-[18%] left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-12 pointer-events-none opacity-40 blur-sm"
            style={{
              background:
                "radial-gradient(ellipse at center, rgba(56, 189, 248, 0.6) 0%, rgba(0, 118, 182, 0.15) 50%, transparent 80%)",
            }}
          />
        </div>
      )}

      {/* ========================================================================= */}
      {/* 2. LOCKER ROOM (Scene 01): Ventilation / Shower Mist Gradient & Fluorescent Hum */}
      {/* ========================================================================= */}
      {facilityType === "locker" && (
        <div className="w-full h-full relative">
          {/* Subtle Ventilation / Hydrotherapy Mist Rising Gradient */}
          <div
            className={`absolute inset-0 pointer-events-none ${
              reducedMotion ? "" : "spatial-animated-element"
            }`}
            style={{
              background:
                "linear-gradient(to top, rgba(0, 118, 182, 0.12) 0%, rgba(148, 163, 184, 0.06) 35%, transparent 70%)",
              animation: reducedMotion
                ? undefined
                : "locker-mist-drift 14s ease-in-out infinite alternate",
            }}
          />

          {/* Overhead Fluorescent Ceiling Tube Light Beam Sheet */}
          <div
            className="absolute top-0 left-0 right-0 h-48 pointer-events-none opacity-30"
            style={{
              background:
                "linear-gradient(to bottom, rgba(255, 255, 255, 0.12) 0%, rgba(0, 118, 182, 0.04) 50%, transparent 100%)",
            }}
          />

          {/* Subtle Floor Vapor Pools */}
          <div
            className="absolute -bottom-10 left-1/4 right-1/4 h-36 rounded-full blur-[80px] pointer-events-none"
            style={{
              background:
                "radial-gradient(circle, rgba(0, 118, 182, 0.2) 0%, rgba(203, 213, 225, 0.05) 50%, transparent 75%)",
            }}
          />
        </div>
      )}

      {/* ========================================================================= */}
      {/* 3. HEAD COACH OFFICE (Scene 04): Daylight Beams, Dust Motes & Optional Rain Streaks */}
      {/* ========================================================================= */}
      {facilityType === "office" && (
        <div className="w-full h-full relative">
          {/* Ambient Warm Daylight Window Light Beam */}
          <div
            className="absolute -top-20 -left-20 w-[80vw] h-[80vh] pointer-events-none opacity-40 blur-2xl"
            style={{
              background:
                "linear-gradient(135deg, rgba(254, 243, 199, 0.14) 0%, rgba(253, 230, 138, 0.04) 40%, transparent 70%)",
              transform: "rotate(-5deg)",
            }}
          />

          {/* Drifting Golden Office Dust Motes */}
          {!reducedMotion &&
            officeDustMotes.map((mote) => (
              <span
                key={mote.id}
                className="absolute rounded-full pointer-events-none spatial-particle-mote"
                style={{
                  left: mote.left,
                  top: mote.top,
                  width: `${mote.size}px`,
                  height: `${mote.size}px`,
                  backgroundColor: "rgba(254, 240, 138, 0.85)",
                  boxShadow: "0 0 6px rgba(250, 204, 21, 0.5)",
                  opacity: mote.opacity * intensityMultiplier,
                  animation: `atmospheric-mote-float ${mote.duration}s ease-in-out infinite`,
                  animationDelay: `${mote.delay}s`,
                }}
              />
            ))}

          {/* Window Rain Streaks (rendered if weather is rainy or default rain overlay) */}
          {weather === "rain" && (
            <div className="absolute inset-0 pointer-events-none opacity-30 overflow-hidden">
              <div
                className={`w-full h-[200%] ${
                  reducedMotion ? "" : "spatial-animated-element"
                }`}
                style={{
                  backgroundImage:
                    "repeating-linear-gradient(110deg, transparent 0px, transparent 38px, rgba(255, 255, 255, 0.35) 39px, transparent 41px)",
                  backgroundSize: "60px 100px",
                  animation: reducedMotion
                    ? undefined
                    : "rain-streak-fall 1.2s linear infinite",
                }}
              />
            </div>
          )}
        </div>
      )}

      {/* ========================================================================= */}
      {/* 4. WEIGHT ROOM: Chalk Dust Motes Drifting Across High-Bay Light Shafts */}
      {/* ========================================================================= */}
      {facilityType === "weight_room" && (
        <div className="w-full h-full relative">
          {/* High-Bay Gym Light Shafts */}
          <div
            className="absolute -top-10 left-1/3 w-[40vw] h-[100vh] pointer-events-none opacity-30 blur-xl"
            style={{
              background:
                "linear-gradient(155deg, rgba(255, 255, 255, 0.18) 0%, rgba(203, 213, 225, 0.05) 50%, transparent 80%)",
            }}
          />

          {/* Chalk Dust Motes Drifting */}
          {!reducedMotion &&
            weightRoomChalkMotes.map((mote) => (
              <span
                key={mote.id}
                className="absolute rounded-full pointer-events-none spatial-particle-mote"
                style={{
                  left: mote.left,
                  top: mote.top,
                  width: `${mote.size * 1.3}px`,
                  height: `${mote.size * 1.3}px`,
                  backgroundColor: "rgba(255, 255, 255, 0.9)",
                  boxShadow: "0 0 5px rgba(255, 255, 255, 0.6)",
                  animation: `chalk-drift ${mote.duration + 4}s linear infinite`,
                  animationDelay: `${mote.delay}s`,
                }}
              />
            ))}
        </div>
      )}

      {/* ========================================================================= */}
      {/* 5. FILM ROOM: Projector Beam Cone & Illuminated Dust Suspension */}
      {/* ========================================================================= */}
      {facilityType === "film_room" && (
        <div className="w-full h-full relative">
          {/* Projector Light Beam Cone */}
          <div
            className={`absolute top-1/4 right-0 w-[85vw] h-[55vh] pointer-events-none ${
              reducedMotion ? "" : "spatial-animated-element"
            }`}
            style={{
              background:
                "conic-gradient(from 260deg at 100% 40%, rgba(224, 242, 254, 0.25) 0deg, rgba(186, 230, 253, 0.08) 18deg, transparent 40deg)",
              filter: "blur(20px)",
              animation: reducedMotion
                ? undefined
                : "projector-shimmer 4s ease-in-out infinite",
            }}
          />

          {/* Beam Dust Particles */}
          {!reducedMotion &&
            filmRoomProjectorMotes.map((mote) => (
              <span
                key={mote.id}
                className="absolute rounded-full pointer-events-none spatial-particle-mote"
                style={{
                  left: mote.left,
                  top: mote.top,
                  width: `${mote.size}px`,
                  height: `${mote.size}px`,
                  backgroundColor: "rgba(224, 242, 254, 0.95)",
                  boxShadow: "0 0 6px rgba(186, 230, 253, 0.7)",
                  opacity: mote.opacity * intensityMultiplier,
                  animation: `atmospheric-mote-float ${mote.duration}s ease-in-out infinite`,
                  animationDelay: `${mote.delay}s`,
                }}
              />
            ))}
        </div>
      )}

      {/* ========================================================================= */}
      {/* 6. STADIUM: Floodlight Bloom & Night Turf Vapor */}
      {/* ========================================================================= */}
      {facilityType === "stadium" && (
        <div className="w-full h-full relative">
          {/* Left / Right Floodlight Flares */}
          <div
            className="absolute -top-10 left-5 w-[35vw] h-[40vh] rounded-full blur-[90px] pointer-events-none opacity-30"
            style={{
              background:
                "radial-gradient(circle, rgba(255, 255, 255, 0.25) 0%, rgba(56, 189, 248, 0.08) 45%, transparent 70%)",
            }}
          />
          <div
            className="absolute -top-10 right-5 w-[35vw] h-[40vh] rounded-full blur-[90px] pointer-events-none opacity-30"
            style={{
              background:
                "radial-gradient(circle, rgba(255, 255, 255, 0.25) 0%, rgba(56, 189, 248, 0.08) 45%, transparent 70%)",
            }}
          />

          {/* Cold Breath / Turf Vapor Particles */}
          {!reducedMotion &&
            stadiumVaporMotes.map((mote) => (
              <span
                key={mote.id}
                className="absolute rounded-full pointer-events-none spatial-particle-mote"
                style={{
                  left: mote.left,
                  top: `${parseFloat(mote.top) * 0.4 + 60}%`,
                  width: `${mote.size * 2}px`,
                  height: `${mote.size * 1.5}px`,
                  backgroundColor: "rgba(255, 255, 255, 0.35)",
                  filter: "blur(3px)",
                  animation: `atmospheric-mote-float ${mote.duration + 2}s ease-in-out infinite`,
                  animationDelay: `${mote.delay}s`,
                }}
              />
            ))}
        </div>
      )}
    </div>
  );
};

export default SpatialAtmosphereLayer;
