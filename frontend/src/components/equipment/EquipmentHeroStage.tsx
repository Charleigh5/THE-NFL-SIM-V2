import React, { useState, useRef, useEffect, useCallback, useMemo } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";
import { ProceduralDukeFootball } from "./ProceduralDukeFootball";
import { ProceduralFranchiseHelmet } from "./ProceduralFranchiseHelmet";
import { ProceduralLombardiTrophy } from "./ProceduralLombardiTrophy";
import { disposeThreeScene } from "./disposeThreeScene";
import { useTheme } from "../../context/useTheme";
import {
  type EquipmentModelType,
  type HelmetFinishType,
  type LightingPresetType,
  type TeamColorway,
} from "./types";
import {
  RotateCcw,
  ZoomIn,
  ZoomOut,
  Sparkles,
  Shield,
  Award,
  Sun,
  Palette,
  Play,
  Pause,
  Maximize2,
} from "lucide-react";

export type { EquipmentModelType, HelmetFinishType, LightingPresetType, TeamColorway };

export interface EquipmentHeroStageProps {
  activeModel?: EquipmentModelType;
  onModelChange?: (model: EquipmentModelType) => void;
  teamColors?: TeamColorway;
  className?: string;
  compact?: boolean;
  showControls?: boolean;
}

/**
 * Scene component running inside R3F Canvas:
 * Handles pointer-tracking spotlighting, drag rotation with inertia, zoom damping,
 * and WebGL context disposal upon unmount.
 */
interface StageSceneProps {
  model: EquipmentModelType;
  finish: HelmetFinishType;
  lightingPreset: LightingPresetType;
  teamColors: TeamColorway;
  autoRotate: boolean;
  zoom: number;
  onFpsUpdate?: (fps: number) => void;
}

const StageScene: React.FC<StageSceneProps> = ({
  model,
  finish,
  lightingPreset,
  teamColors,
  autoRotate,
  zoom,
  onFpsUpdate,
}) => {
  const { scene, gl, camera } = useThree();
  const modelGroupRef = useRef<THREE.Group>(null);
  const spotLightRef = useRef<THREE.SpotLight>(null);
  const keyLightRef = useRef<THREE.DirectionalLight>(null);

  // Rotation state with momentum & inertia damping
  const rotationRef = useRef({
    currentYaw: 0,
    currentPitch: 0,
    targetYaw: 0,
    targetPitch: 0,
    velocityYaw: 0,
    velocityPitch: 0,
    isDragging: false,
    lastPointerX: 0,
    lastPointerY: 0,
  });

  // FPS calculation
  const frameCountRef = useRef(0);
  const lastTimeRef = useRef(0);

  // Strict cleanup of geometries, textures, and WebGL context upon unmount
  useEffect(() => {
    return () => {
      disposeThreeScene(scene, gl);
    };
  }, [scene, gl]);

  // Adjust camera distance based on zoom level
  useEffect(() => {
    const baseDistance = model === "lombardi" ? 4.2 : 3.2;
    const targetZ = baseDistance / zoom;
    camera.position.set(0, model === "lombardi" ? 0.2 : 0, targetZ);
    camera.lookAt(0, model === "lombardi" ? 0.1 : 0, 0);
  }, [camera, zoom, model]);

  // Handle pointer interactions on the canvas
  useEffect(() => {
    const domElement = gl.domElement;

    const handlePointerDown = (e: PointerEvent) => {
      domElement.setPointerCapture(e.pointerId);
      rotationRef.current.isDragging = true;
      rotationRef.current.lastPointerX = e.clientX;
      rotationRef.current.lastPointerY = e.clientY;
      rotationRef.current.velocityYaw = 0;
      rotationRef.current.velocityPitch = 0;
    };

    const handlePointerMove = (e: PointerEvent) => {
      if (!rotationRef.current.isDragging) return;
      const dx = e.clientX - rotationRef.current.lastPointerX;
      const dy = e.clientY - rotationRef.current.lastPointerY;
      rotationRef.current.lastPointerX = e.clientX;
      rotationRef.current.lastPointerY = e.clientY;

      const deltaYaw = dx * 0.007;
      const deltaPitch = dy * 0.007;

      rotationRef.current.targetYaw += deltaYaw;
      rotationRef.current.targetPitch += deltaPitch;
      rotationRef.current.velocityYaw = deltaYaw;
      rotationRef.current.velocityPitch = deltaPitch;
    };

    const handlePointerUp = (e: PointerEvent) => {
      try {
        domElement.releasePointerCapture(e.pointerId);
      } catch {
        // Ignored
      }
      rotationRef.current.isDragging = false;
    };

    domElement.addEventListener("pointerdown", handlePointerDown);
    domElement.addEventListener("pointermove", handlePointerMove);
    domElement.addEventListener("pointerup", handlePointerUp);
    domElement.addEventListener("pointercancel", handlePointerUp);

    return () => {
      domElement.removeEventListener("pointerdown", handlePointerDown);
      domElement.removeEventListener("pointermove", handlePointerMove);
      domElement.removeEventListener("pointerup", handlePointerUp);
      domElement.removeEventListener("pointercancel", handlePointerUp);
    };
  }, [gl]);

  // Frame Loop (60 FPS): Pointer-tracking lights & angular damping
  useFrame((state, delta) => {
    // 1. FPS Telemetry (Throttled update ~2Hz)
    frameCountRef.current++;
    const now = performance.now();
    if (lastTimeRef.current === 0) {
      lastTimeRef.current = now;
    } else if (now - lastTimeRef.current >= 500) {
      const currentFps = Math.round((frameCountRef.current * 1000) / (now - lastTimeRef.current));
      onFpsUpdate?.(currentFps);
      frameCountRef.current = 0;
      lastTimeRef.current = now;
    }

    // 2. Interactive Spotlight Tracking Cursor Pointer Coordinates
    const px = state.pointer.x; // [-1, 1]
    const py = state.pointer.y; // [-1, 1]

    if (spotLightRef.current) {
      const targetX = 3.5 + px * 3.5;
      const targetY = 4.5 + py * 2.5;
      const targetZ = 5.0 + Math.sqrt(Math.max(0, 1 - px * px - py * py)) * 2.0;

      spotLightRef.current.position.lerp(new THREE.Vector3(targetX, targetY, targetZ), 0.08);
    }

    // 3. Angular Velocity Inertia and Damping
    const r = rotationRef.current;
    if (!r.isDragging) {
      r.velocityYaw *= 0.92;
      r.velocityPitch *= 0.92;

      if (autoRotate && Math.abs(r.velocityYaw) < 0.0005) {
        r.targetYaw += delta * 0.35;
      } else {
        r.targetYaw += r.velocityYaw;
        r.targetPitch += r.velocityPitch;
      }
    }

    // Clamp pitch to prevent disorienting inversion
    r.targetPitch = Math.max(-Math.PI * 0.32, Math.min(Math.PI * 0.32, r.targetPitch));

    // Smooth exponential lerp
    r.currentYaw += (r.targetYaw - r.currentYaw) * 0.12;
    r.currentPitch += (r.targetPitch - r.currentPitch) * 0.12;

    if (modelGroupRef.current) {
      modelGroupRef.current.rotation.y = r.currentYaw;
      modelGroupRef.current.rotation.x = r.currentPitch;
    }
  });

  // Lighting Preset Colors & Intensities
  const lightingConfig = useMemo(() => {
    switch (lightingPreset) {
      case "stadium_floodlights":
        return {
          ambientIntensity: 0.65,
          ambientColor: "#E0E8F5",
          keyColor: "#FFFFFF",
          keyIntensity: 2.2,
          spotColor: "#D0E5FF",
          spotIntensity: 3.5,
          fillColor: "#0076B6",
          fillIntensity: 0.8,
        };
      case "war_room_studio":
        return {
          ambientIntensity: 0.45,
          ambientColor: "#FFEAD0",
          keyColor: "#FFF2E2",
          keyIntensity: 2.0,
          spotColor: "#FFE0B2",
          spotIntensity: 3.0,
          fillColor: teamColors.primary,
          fillIntensity: 1.2,
        };
      case "primetime_neon":
        return {
          ambientIntensity: 0.25,
          ambientColor: "#0F172A",
          keyColor: "#38BDF8",
          keyIntensity: 2.6,
          spotColor: teamColors.primary,
          spotIntensity: 4.2,
          fillColor: teamColors.secondary,
          fillIntensity: 2.0,
        };
    }
  }, [lightingPreset, teamColors]);

  return (
    <>
      {/* Dynamic Lighting Rig */}
      <ambientLight
        color={lightingConfig.ambientColor}
        intensity={lightingConfig.ambientIntensity}
      />

      {/* Primary Key Directional Light */}
      <directionalLight
        ref={keyLightRef}
        position={[4, 6, 5]}
        color={lightingConfig.keyColor}
        intensity={lightingConfig.keyIntensity}
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
      />

      {/* Interactive Pointer-Tracking Key Spotlight */}
      <spotLight
        ref={spotLightRef}
        position={[3.5, 4.5, 5]}
        color={lightingConfig.spotColor}
        intensity={lightingConfig.spotIntensity}
        angle={Math.PI / 4}
        penumbra={0.6}
        distance={20}
        castShadow
      />

      {/* Back Rim / Kicker Light in Team Color */}
      <directionalLight
        position={[-5, 2, -4]}
        color={lightingConfig.fillColor}
        intensity={lightingConfig.fillIntensity}
      />

      {/* Ground Pedestal Shadow Floor */}
      <mesh
        position={[0, model === "lombardi" ? -1.3 : -1.0, 0]}
        rotation={[-Math.PI / 2, 0, 0]}
        receiveShadow
      >
        <circleGeometry args={[2.5, 32]} />
        <meshBasicMaterial color="#030712" transparent opacity={0.6} />
      </mesh>

      {/* Switchable 3D Procedural Model Group */}
      <group ref={modelGroupRef}>
        {model === "duke" && (
          <ProceduralDukeFootball position={[0, 0, 0]} scale={1.25} rotation={[0.2, 0.4, 0.1]} />
        )}

        {model === "helmet" && (
          <ProceduralFranchiseHelmet
            position={[0, -0.05, 0]}
            scale={1.15}
            rotation={[0.1, -0.4, 0]}
            primaryColor={teamColors.primary}
            secondaryColor={teamColors.secondary}
            accentColor={teamColors.accent}
            finish={finish}
          />
        )}

        {model === "lombardi" && (
          <ProceduralLombardiTrophy position={[0, -1.15, 0]} scale={0.88} rotation={[0, -0.2, 0]} />
        )}
      </group>
    </>
  );
};

/**
 * EquipmentHeroStage: High-Performance Procedural 3D WebGL Inspection Stage
 * - 100% Offline: Procedural geometry, textures, and studio reflections (0 CDN calls)
 * - Switcher controls: "The Duke", Franchise Team Helmet, Lombardi Trophy
 * - PBR Finish Selector: Gloss, Matte, Metallic
 * - Interactive pointer-tracking lighting & inertial drag rotation
 * - Zero WebGL context leaks: automatic recursive scene cleanup on unmount
 */
export const EquipmentHeroStage: React.FC<EquipmentHeroStageProps> = ({
  activeModel: controlledModel,
  onModelChange,
  teamColors: propTeamColors,
  className = "",
  compact = false,
  showControls = true,
}) => {
  const { activeTeam } = useTheme();

  // Selected Model State
  const [internalModel, setInternalModel] = useState<EquipmentModelType>("duke");
  const activeModel = controlledModel ?? internalModel;

  const handleSelectModel = useCallback(
    (model: EquipmentModelType) => {
      setInternalModel(model);
      onModelChange?.(model);
    },
    [onModelChange]
  );

  // Helmet Finish State
  const [finish, setFinish] = useState<HelmetFinishType>("gloss");

  // Lighting Preset State
  const [lightingPreset, setLightingPreset] = useState<LightingPresetType>("stadium_floodlights");

  // Interaction State
  const [autoRotate, setAutoRotate] = useState(true);
  const [zoom, setZoom] = useState(1.0);
  const [fps, setFps] = useState(60);

  // Resolve Team Colors with Fallbacks
  const teamColors: TeamColorway = useMemo(() => {
    if (propTeamColors) return propTeamColors;
    if (activeTeam?.colors) {
      return {
        primary: activeTeam.colors.primary || "#0076B6",
        secondary: activeTeam.colors.secondary || "#B0B7BC",
        accent: activeTeam.colors.accent || "#FFFFFF",
      };
    }
    return {
      primary: "#0076B6", // Default Detroit Lions Honolulu Blue
      secondary: "#B0B7BC",
      accent: "#FFFFFF",
    };
  }, [propTeamColors, activeTeam]);

  const handleZoomIn = () => setZoom((z) => Math.min(2.0, z + 0.2));
  const handleZoomOut = () => setZoom((z) => Math.max(0.6, z - 0.2));
  const handleReset = () => {
    setZoom(1.0);
    setAutoRotate(true);
  };

  return (
    <div
      className={`relative rounded-2xl broadcast-glass border border-white/15 overflow-hidden shadow-[0_20px_50px_rgba(0,0,0,0.8)] backdrop-blur-xl transition-all duration-300 ${
        compact ? "p-3" : "p-5 md:p-6"
      } ${className}`}
      data-testid="equipment-hero-stage"
    >
      {/* Dynamic Franchise Ambient Glow Mesh */}
      <div
        className="absolute -top-32 -left-32 w-80 h-80 rounded-full opacity-20 blur-3xl pointer-events-none"
        style={{ backgroundColor: teamColors.primary }}
      />
      <div
        className="absolute -bottom-32 -right-32 w-80 h-80 rounded-full opacity-15 blur-3xl pointer-events-none"
        style={{ backgroundColor: teamColors.secondary }}
      />

      <div className={`grid grid-cols-1 ${compact ? "" : "lg:grid-cols-12"} gap-5 items-center`}>
        {/* ========================================================================= */}
        {/* LEFT / CENTER: Interactive 3D WebGL Canvas Viewport */}
        {/* ========================================================================= */}
        <div
          className={`relative w-full ${
            compact ? "h-[260px]" : "lg:col-span-8 h-[380px] md:h-[440px]"
          } rounded-xl bg-slate-950/70 border border-white/10 overflow-hidden select-none touch-none`}
        >
          {/* Top Status & Telemetry HUD Overlay */}
          <div className="absolute top-3 left-3 right-3 z-10 flex items-center justify-between pointer-events-none">
            <div className="flex items-center gap-2">
              <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-black/60 border border-white/15 text-[10px] font-mono text-emerald-400 font-bold backdrop-blur-md">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                {fps} FPS • 60Hz WEBGL
              </span>
              <span className="hidden sm:inline-flex px-2 py-1 rounded bg-black/50 border border-white/10 text-[10px] font-mono text-gray-300 backdrop-blur-md">
                {activeModel === "duke" && "THE DUKE • HORWEEN"}
                {activeModel === "helmet" &&
                  `${activeTeam?.name?.toUpperCase() || "FRANCHISE"} SHELL`}
                {activeModel === "lombardi" && "STERLING SILVER CHROME"}
              </span>
            </div>

            {/* In-Canvas Quick Stage Action Controls */}
            <div className="flex items-center gap-1.5 pointer-events-auto">
              <button
                onClick={() => setAutoRotate((r) => !r)}
                title={autoRotate ? "Pause Orbit" : "Resume Orbit"}
                className={`p-1.5 rounded-lg border backdrop-blur-md transition-colors ${
                  autoRotate
                    ? "bg-cyan-500/20 border-cyan-500/40 text-cyan-300"
                    : "bg-black/60 border-white/15 text-gray-400 hover:text-white"
                }`}
              >
                {autoRotate ? <Pause size={14} /> : <Play size={14} />}
              </button>
              <button
                onClick={handleZoomIn}
                title="Zoom In"
                className="p-1.5 rounded-lg bg-black/60 border border-white/15 text-gray-300 hover:text-white hover:bg-black/80 backdrop-blur-md transition-colors"
              >
                <ZoomIn size={14} />
              </button>
              <button
                onClick={handleZoomOut}
                title="Zoom Out"
                className="p-1.5 rounded-lg bg-black/60 border border-white/15 text-gray-300 hover:text-white hover:bg-black/80 backdrop-blur-md transition-colors"
              >
                <ZoomOut size={14} />
              </button>
              <button
                onClick={handleReset}
                title="Reset Camera & Rotation"
                className="p-1.5 rounded-lg bg-black/60 border border-white/15 text-gray-300 hover:text-white hover:bg-black/80 backdrop-blur-md transition-colors"
              >
                <RotateCcw size={14} />
              </button>
            </div>
          </div>

          {/* Drag Instruction Cue Overlay */}
          <div className="absolute bottom-3 left-3 z-10 pointer-events-none">
            <span className="text-[10px] font-mono text-gray-400/80 bg-black/40 px-2 py-1 rounded backdrop-blur-sm border border-white/5 flex items-center gap-1">
              <Maximize2 size={10} /> Drag to inspect • Cursor tracks lighting
            </span>
          </div>

          {/* R3F WebGL Canvas Container */}
          <Canvas
            shadows
            dpr={[1, 2]}
            camera={{ position: [0, 0, 3.2], fov: 45 }}
            gl={{
              antialias: true,
              alpha: true,
              powerPreference: "high-performance",
            }}
            className="w-full h-full cursor-grab active:cursor-grabbing"
          >
            <StageScene
              model={activeModel}
              finish={finish}
              lightingPreset={lightingPreset}
              teamColors={teamColors}
              autoRotate={autoRotate}
              zoom={zoom}
              onFpsUpdate={setFps}
            />
          </Canvas>
        </div>

        {/* ========================================================================= */}
        {/* RIGHT: Equipment Control Rail & Spec Sheet */}
        {/* ========================================================================= */}
        {showControls && (
          <div className={`space-y-4 ${compact ? "mt-3" : "lg:col-span-4"}`}>
            {/* Header / Subtitle */}
            <div className="border-b border-white/10 pb-3">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono uppercase tracking-widest text-cyan-400 font-bold flex items-center gap-1.5">
                  <Sparkles size={12} />
                  3D Holographic Locker
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-white font-bold border border-white/15">
                  100% OFFLINE
                </span>
              </div>
              <h3 className="font-header text-xl md:text-2xl uppercase tracking-tight text-white mt-1 leading-none">
                Gameday Equipment Bay
              </h3>
              <p className="text-xs text-gray-400 font-mono mt-1">
                Precision procedural inspection with physical lighting & custom team styling.
              </p>
            </div>

            {/* Model Switcher Buttons */}
            <div>
              <label className="text-[11px] font-mono uppercase text-gray-400 tracking-wider block mb-2 font-bold">
                Select Equipment Artifact
              </label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  data-testid="equipment-switcher-duke"
                  onClick={() => handleSelectModel("duke")}
                  className={`p-2.5 rounded-xl border flex flex-col items-center justify-center gap-1 text-center transition-all cursor-pointer ${
                    activeModel === "duke"
                      ? "bg-amber-500/20 border-amber-400/60 text-amber-300 shadow-lg shadow-amber-500/10 font-bold"
                      : "bg-slate-900/50 border-white/10 text-gray-400 hover:text-white hover:bg-slate-800/60"
                  }`}
                >
                  <span className="text-base">🏈</span>
                  <span className="text-xs font-header uppercase tracking-wider">The Duke</span>
                  <span className="text-[9px] font-mono text-gray-400">Game Ball</span>
                </button>

                <button
                  type="button"
                  data-testid="equipment-switcher-helmet"
                  onClick={() => handleSelectModel("helmet")}
                  className={`p-2.5 rounded-xl border flex flex-col items-center justify-center gap-1 text-center transition-all cursor-pointer ${
                    activeModel === "helmet"
                      ? "bg-cyan-500/20 border-cyan-400/60 text-cyan-300 shadow-lg shadow-cyan-500/10 font-bold"
                      : "bg-slate-900/50 border-white/10 text-gray-400 hover:text-white hover:bg-slate-800/60"
                  }`}
                >
                  <Shield size={16} className={activeModel === "helmet" ? "text-cyan-400" : ""} />
                  <span className="text-xs font-header uppercase tracking-wider">Franchise</span>
                  <span className="text-[9px] font-mono text-gray-400">Team Helmet</span>
                </button>

                <button
                  type="button"
                  data-testid="equipment-switcher-lombardi"
                  onClick={() => handleSelectModel("lombardi")}
                  className={`p-2.5 rounded-xl border flex flex-col items-center justify-center gap-1 text-center transition-all cursor-pointer ${
                    activeModel === "lombardi"
                      ? "bg-yellow-500/20 border-yellow-400/60 text-yellow-300 shadow-lg shadow-yellow-500/10 font-bold"
                      : "bg-slate-900/50 border-white/10 text-gray-400 hover:text-white hover:bg-slate-800/60"
                  }`}
                >
                  <Award
                    size={16}
                    className={activeModel === "lombardi" ? "text-yellow-400" : ""}
                  />
                  <span className="text-xs font-header uppercase tracking-wider">Lombardi</span>
                  <span className="text-[9px] font-mono text-gray-400">Championship</span>
                </button>
              </div>
            </div>

            {/* Helmet PBR Finish Selector (Visible when helmet is active) */}
            {activeModel === "helmet" && (
              <div className="p-3 rounded-xl bg-slate-900/60 border border-white/10 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-mono uppercase text-gray-300 font-bold flex items-center gap-1.5">
                    <Palette size={12} className="text-cyan-400" />
                    Shell Surface Finish
                  </span>
                  <span className="text-[10px] font-mono text-cyan-400 uppercase font-bold">
                    {finish}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-2">
                  {(["gloss", "matte", "metallic"] as HelmetFinishType[]).map((f) => (
                    <button
                      key={f}
                      type="button"
                      onClick={() => setFinish(f)}
                      className={`py-1.5 px-2 rounded-lg text-xs font-header uppercase tracking-wider border transition-all cursor-pointer ${
                        finish === f
                          ? "bg-white/20 border-cyan-400 text-white font-bold"
                          : "bg-black/40 border-white/10 text-gray-400 hover:text-gray-200"
                      }`}
                    >
                      {f}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Stage Lighting Preset Selector */}
            <div className="p-3 rounded-xl bg-slate-900/60 border border-white/10 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono uppercase text-gray-300 font-bold flex items-center gap-1.5">
                  <Sun size={12} className="text-yellow-400" />
                  Lighting Rig
                </span>
              </div>
              <div className="grid grid-cols-3 gap-1.5 text-[10px] font-mono">
                <button
                  type="button"
                  onClick={() => setLightingPreset("stadium_floodlights")}
                  className={`py-1 px-1.5 rounded border text-center truncate transition-colors ${
                    lightingPreset === "stadium_floodlights"
                      ? "bg-cyan-500/25 border-cyan-400 text-cyan-300 font-bold"
                      : "bg-black/40 border-white/10 text-gray-400 hover:text-gray-200"
                  }`}
                >
                  Stadium
                </button>
                <button
                  type="button"
                  onClick={() => setLightingPreset("war_room_studio")}
                  className={`py-1 px-1.5 rounded border text-center truncate transition-colors ${
                    lightingPreset === "war_room_studio"
                      ? "bg-amber-500/25 border-amber-400 text-amber-300 font-bold"
                      : "bg-black/40 border-white/10 text-gray-400 hover:text-gray-200"
                  }`}
                >
                  Studio
                </button>
                <button
                  type="button"
                  onClick={() => setLightingPreset("primetime_neon")}
                  className={`py-1 px-1.5 rounded border text-center truncate transition-colors ${
                    lightingPreset === "primetime_neon"
                      ? "bg-purple-500/25 border-purple-400 text-purple-300 font-bold"
                      : "bg-black/40 border-white/10 text-gray-400 hover:text-gray-200"
                  }`}
                >
                  Primetime
                </button>
              </div>
            </div>

            {/* Franchise Colorway Swatches */}
            <div className="flex items-center justify-between px-3 py-2 rounded-xl bg-black/40 border border-white/10 text-xs font-mono">
              <span className="text-gray-400">Franchise Palette:</span>
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1">
                  <span
                    className="w-3.5 h-3.5 rounded-full border border-white/30 shadow-sm"
                    style={{ backgroundColor: teamColors.primary }}
                    title={`Primary: ${teamColors.primary}`}
                  />
                  <span className="text-[10px] text-gray-300 uppercase">PRI</span>
                </div>
                <div className="flex items-center gap-1">
                  <span
                    className="w-3.5 h-3.5 rounded-full border border-white/30 shadow-sm"
                    style={{ backgroundColor: teamColors.secondary }}
                    title={`Secondary: ${teamColors.secondary}`}
                  />
                  <span className="text-[10px] text-gray-300 uppercase">SEC</span>
                </div>
                <div className="flex items-center gap-1">
                  <span
                    className="w-3.5 h-3.5 rounded-full border border-white/30 shadow-sm"
                    style={{ backgroundColor: teamColors.accent }}
                    title={`Accent: ${teamColors.accent}`}
                  />
                  <span className="text-[10px] text-gray-300 uppercase">ACC</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
