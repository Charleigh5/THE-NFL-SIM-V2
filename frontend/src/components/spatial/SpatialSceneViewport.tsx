import React, { useState, useEffect, useRef, useMemo } from "react";
import type { ParallaxBounds } from "../../types/spatial";
import {
  SpatialAtmosphereLayer,
  type FacilityAtmosphereType,
  type WeatherType,
} from "./SpatialAtmosphereLayer";

interface SpatialSceneViewportProps {
  backgroundSrc: string;
  overscan?: number;
  parallaxBounds?: ParallaxBounds;
  disabled?: boolean;
  className?: string;
  children?: React.ReactNode;
  atmosphereType?: FacilityAtmosphereType;
  weather?: WeatherType;
}

const DEFAULT_PARALLAX: ParallaxBounds = {
  maxOffsetX: 16,
  maxOffsetY: 10,
  maxRotateX: 2.2,
  maxRotateY: 3.2,
};

export const SpatialSceneViewport: React.FC<SpatialSceneViewportProps> = ({
  backgroundSrc,
  overscan = 1.06,
  parallaxBounds = DEFAULT_PARALLAX,
  disabled = false,
  className = "",
  children,
  atmosphereType,
  weather = "clear",
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const backgroundLayerRef = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number | null>(null);

  // Target coordinates normalized [-1, 1]
  const targetPos = useRef({ x: 0, y: 0 });
  // Current lerped coordinates [-1, 1]
  const currentPos = useRef({ x: 0, y: 0 });
  // Running flag to avoid infinite loops when settled
  const isRunning = useRef(false);
  // Viewport intersection state
  const isIntersecting = useRef(true);

  const [reducedMotion, setReducedMotion] = useState(() => {
    if (typeof window !== "undefined") {
      return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    }
    return false;
  });

  // Derive webpSrc if backgroundSrc is a .jpg or .png format
  const webpSrc = useMemo(() => {
    if (!backgroundSrc) return null;
    if (backgroundSrc.endsWith(".webp")) return backgroundSrc;
    if (/\.(jpe?g|png)($|\?)/i.test(backgroundSrc)) {
      return backgroundSrc.replace(/\.(jpe?g|png)($|\?)/i, ".webp$2");
    }
    return null;
  }, [backgroundSrc]);

  // Check system prefers-reduced-motion
  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

    const handler = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, []);

  // Power-efficient idling: visibilitychange & IntersectionObserver
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        if (rafRef.current) {
          cancelAnimationFrame(rafRef.current);
          rafRef.current = null;
        }
        isRunning.current = false;
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);

    let observer: IntersectionObserver | null = null;
    if (typeof IntersectionObserver !== "undefined" && containerRef.current) {
      observer = new IntersectionObserver(
        ([entry]) => {
          const intersecting = entry ? entry.isIntersecting : true;
          isIntersecting.current = intersecting;
          if (!intersecting) {
            if (rafRef.current) {
              cancelAnimationFrame(rafRef.current);
              rafRef.current = null;
            }
            isRunning.current = false;
          }
        },
        { threshold: 0 }
      );
      observer.observe(containerRef.current);
    }

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      if (observer) {
        observer.disconnect();
      }
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
        isRunning.current = false;
      }
    };
  }, []);

  // Butter-smooth direct DOM transform update (Zero React re-renders)
  const startAnimationLoop = () => {
    if (
      isRunning.current ||
      disabled ||
      reducedMotion ||
      (typeof document !== "undefined" && document.hidden) ||
      !isIntersecting.current
    ) {
      return;
    }
    isRunning.current = true;

    const LERP_FACTOR = 0.08;

    const tick = () => {
      if ((typeof document !== "undefined" && document.hidden) || !isIntersecting.current) {
        isRunning.current = false;
        rafRef.current = null;
        return;
      }

      const dx = targetPos.current.x - currentPos.current.x;
      const dy = targetPos.current.y - currentPos.current.y;

      currentPos.current.x += dx * LERP_FACTOR;
      currentPos.current.y += dy * LERP_FACTOR;

      const offsetX = currentPos.current.x * parallaxBounds.maxOffsetX;
      const offsetY = currentPos.current.y * parallaxBounds.maxOffsetY;
      const rotX = -currentPos.current.y * parallaxBounds.maxRotateX;
      const rotY = currentPos.current.x * parallaxBounds.maxRotateY;

      if (backgroundLayerRef.current) {
        backgroundLayerRef.current.style.transform = `scale(${overscan}) translate3d(${-offsetX.toFixed(
          2
        )}px, ${-offsetY.toFixed(2)}px, 0px) rotateX(${rotX.toFixed(
          2
        )}deg) rotateY(${rotY.toFixed(2)}deg)`;
      }

      // Continue while motion is noticeable
      if (Math.abs(dx) > 0.0005 || Math.abs(dy) > 0.0005) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        isRunning.current = false;
        rafRef.current = null;
      }
    };

    rafRef.current = requestAnimationFrame(tick);
  };

  useEffect(() => {
    if (disabled || reducedMotion) {
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
        isRunning.current = false;
      }
      if (backgroundLayerRef.current) {
        backgroundLayerRef.current.style.transform =
          "scale(1) translate3d(0px, 0px, 0px) rotateX(0deg) rotateY(0deg)";
      }
    } else {
      if (backgroundLayerRef.current) {
        backgroundLayerRef.current.style.transform = `scale(${overscan}) translate3d(0px, 0px, 0px) rotateX(0deg) rotateY(0deg)`;
      }
    }

    return () => {
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
        isRunning.current = false;
      }
    };
  }, [disabled, reducedMotion, overscan]);

  // Pointer Move Handler triggers LERP loop
  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (
      disabled ||
      reducedMotion ||
      (typeof document !== "undefined" && document.hidden) ||
      !isIntersecting.current
    ) {
      return;
    }
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;

    const xRel = (e.clientX - rect.left) / rect.width;
    const yRel = (e.clientY - rect.top) / rect.height;

    // Clamp to [-1, 1] range
    targetPos.current.x = Math.max(-1, Math.min(1, (xRel - 0.5) * 2));
    targetPos.current.y = Math.max(-1, Math.min(1, (yRel - 0.5) * 2));

    startAnimationLoop();
  };

  const handlePointerLeave = () => {
    targetPos.current.x = 0;
    targetPos.current.y = 0;
    startAnimationLoop();
  };

  return (
    <div
      ref={containerRef}
      onPointerMove={handlePointerMove}
      onPointerLeave={handlePointerLeave}
      className={`relative w-full overflow-hidden ${className}`}
    >
      {/* Dynamic 2.5D Background Layer with Direct Hardware Transform */}
      <div
        className="absolute inset-0 w-full h-full pointer-events-none overflow-hidden"
        style={{
          perspective: "1200px",
          perspectiveOrigin: "50% 45%",
          contain: "layout paint",
        }}
      >
        <div
          ref={backgroundLayerRef}
          className="absolute inset-0 w-full h-full pointer-events-none origin-center"
          style={{
            transform: `scale(${overscan}) translate3d(0px, 0px, 0px) rotateX(0deg) rotateY(0deg)`,
            willChange: "transform",
            contain: "layout paint",
          }}
        >
          <picture className="block w-full h-full">
            {webpSrc && <source type="image/webp" srcSet={webpSrc} />}
            <img
              src={backgroundSrc}
              alt="War Room Spatial Background"
              className="w-full h-full object-cover object-center filter brightness-95 contrast-[1.03]"
              loading="eager"
            />
          </picture>
          {/* Ambient Subtle Vignette & Gridiron Carbon Tint */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-black/60 pointer-events-none" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_40%_40%,rgba(0,118,182,0.12),transparent_65%)] pointer-events-none" />
        </div>
      </div>

      {/* Atmospheric Particle & Lighting FX Layer (GPU-composited between background and foreground) */}
      {atmosphereType && <SpatialAtmosphereLayer facilityType={atmosphereType} weather={weather} />}

      {/* Foreground Interactive Content Layer: Standard Unskewed 2D Projection */}
      <div className="relative z-10 w-full h-full">{children}</div>
    </div>
  );
};
