import React, { useState, useEffect, useCallback } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, PerspectiveCamera, Environment, ContactShadows } from "@react-three/drei";
import EnhancedPlayerCharacter from "./EnhancedPlayerCharacter";
import EnhancedFieldVisualizer from "./EnhancedFieldVisualizer";
import { useBroadcastStore } from "../../store/useBroadcastStore";
import { getCutsceneDirector } from "../../broadcast/CutsceneDirector";
import {
  BroadcastPhase,
  type BroadcastPlayResult,
  type GameRosterData,
  type FormationData,
  type PlayerVisualData,
} from "../../types/broadcast";

interface LiveGameVisualizerProps {
  gameId: number;
  apiUrl?: string;
  autoConnect?: boolean;
  enableBroadcast?: boolean;
  showControls?: boolean;
  detailLevel?: "low" | "medium" | "high";
}

export const LiveGameVisualizer: React.FC<LiveGameVisualizerProps> = ({
  gameId,
  apiUrl = "/api/live",
  autoConnect = true,
  enableBroadcast = false,
  showControls = true,
  detailLevel = "medium",
}) => {
  const [rosterData, setRosterData] = useState<GameRosterData | null>(null);
  const [formationData, setFormationData] = useState<FormationData | null>(null);
  const [currentPlay, setCurrentPlay] = useState<number>(1);
  const [isAnimating] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [wsConnected, setWsConnected] = useState<boolean>(false);

  const activeClip = useBroadcastStore((s) => s.activeClip);
  const dispatchBroadcast = useBroadcastStore((s) => s.dispatch);
  const setActiveClip = useBroadcastStore((s) => s.setActiveClip);

  const fetchRosterData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`${apiUrl}/game/${gameId}/roster`);
      if (!response.ok) throw new Error("Failed to fetch roster data");
      const data: GameRosterData = await response.json();
      setRosterData(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  }, [apiUrl, gameId]);

  const fetchFormationData = useCallback(
    async (playId: number) => {
      try {
        const response = await fetch(`${apiUrl}/game/${gameId}/formation/${playId}`);
        if (!response.ok) throw new Error("Failed to fetch formation data");
        const data: FormationData = await response.json();
        setFormationData(data);
      } catch (err) {
        console.error("Error fetching formation:", err);
      }
    },
    [apiUrl, gameId]
  );

  useEffect(() => {
    fetchRosterData();
    fetchFormationData(currentPlay);
  }, [fetchRosterData, fetchFormationData, currentPlay]);

  useEffect(() => {
    if (!autoConnect) return;

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}${apiUrl}/ws/game/${gameId}`;
    let ws: WebSocket | null = null;

    try {
      ws = new WebSocket(wsUrl);
      ws.onopen = () => setWsConnected(true);
      ws.onclose = () => setWsConnected(false);
      ws.onerror = () => setWsConnected(false);
    } catch (err) {
      console.warn("WebSocket connection skipped or unavailable:", err);
    }

    return () => {
      if (ws) ws.close();
    };
  }, [autoConnect, apiUrl, gameId]);

  // Broadcast cutscene director state machine loop
  useEffect(() => {
    if (!enableBroadcast) return;

    const director = getCutsceneDirector();
    const mockPlayResult: BroadcastPlayResult = {
      playId: currentPlay,
      playType: "pass",
      outcome: "complete",
      yardsGained: 25,
      passerId: rosterData?.home_team.players.find((p) => p.position === "QB")?.id || 1,
      receiverId: rosterData?.home_team.players.find((p) => p.position === "WR")?.id || 2,
      tacklerIds: [rosterData?.away_team.players[0]?.id || 3],
      startTime: Date.now() / 1000,
      endTime: Date.now() / 1000 + 8,
      isHighlightWorthy: true,
    };

    dispatchBroadcast({ type: "PLAY_CALLED", playResult: mockPlayResult });

    const clips = director.generateClipSequence(mockPlayResult, BroadcastPhase.PRE_PLAY);
    if (clips.length > 0) {
      setActiveClip(clips[0]);
    }

    const phaseTimeout = setTimeout(() => {
      dispatchBroadcast({ type: "SNAP" });

      setTimeout(() => {
        dispatchBroadcast({ type: "WHISTLE", playResult: mockPlayResult });

        const nextPhase = director.determineNextPhase(BroadcastPhase.POST_PLAY, mockPlayResult);

        if (nextPhase === BroadcastPhase.REPLAY) {
          dispatchBroadcast({ type: "REPLAY_REQUESTED" });
        } else {
          dispatchBroadcast({ type: "REPLAY_COMPLETE" });
        }
      }, 5500);
    }, 4500);

    return () => clearTimeout(phaseTimeout);
  }, [enableBroadcast, currentPlay, rosterData, dispatchBroadcast, setActiveClip]);

  const getPlayerPositions = useCallback(() => {
    if (!rosterData || !formationData) return [];

    const homePlayers = rosterData.home_team.players;
    const awayPlayers = rosterData.away_team.players;
    const offenseFormation = formationData.formation.offense.players;
    const defenseFormation = formationData.formation.defense.players;

    const positionedPlayers: Array<{
      player: PlayerVisualData;
      position: [number, number, number];
      team: "home" | "away";
    }> = [];

    offenseFormation.forEach((formPlayer, index) => {
      if (homePlayers[index]) {
        positionedPlayers.push({
          player: homePlayers[index],
          position: [formPlayer.x, formPlayer.y, formPlayer.z],
          team: "home",
        });
      }
    });

    defenseFormation.forEach((formPlayer, index) => {
      if (awayPlayers[index]) {
        positionedPlayers.push({
          player: awayPlayers[index],
          position: [formPlayer.x + 10, formPlayer.y, formPlayer.z],
          team: "away",
        });
      }
    });

    return positionedPlayers;
  }, [rosterData, formationData]);

  const handleNextPlay = () => {
    setCurrentPlay((prev) => prev + 1);
    fetchFormationData(currentPlay + 1);
  };

  const handlePrevPlay = () => {
    if (currentPlay > 1) {
      setCurrentPlay((prev) => prev - 1);
      fetchFormationData(currentPlay - 1);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-900 text-white rounded-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p>Loading 3D game visualization...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-900 text-white rounded-lg">
        <div className="text-center">
          <p className="text-red-500 mb-4">Error: {error}</p>
          <button
            onClick={fetchRosterData}
            className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 font-semibold"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const playerPositions = getPlayerPositions();

  return (
    <div className="w-full h-[600px] bg-gradient-to-b from-sky-900 to-slate-950 rounded-lg overflow-hidden relative border border-white/10 shadow-2xl">
      {/* HUD Overlay */}
      <div className="absolute top-4 left-4 z-10 bg-black/80 backdrop-blur-md text-white px-4 py-2 rounded-lg border border-white/10">
        <div className="flex items-center gap-4">
          {rosterData && (
            <>
              <div className="text-lg font-black tracking-wider uppercase">
                {rosterData.home_team.abbreviation} vs {rosterData.away_team.abbreviation}
              </div>
              <div
                className={`px-2 py-0.5 rounded text-xs font-bold ${
                  wsConnected ? "bg-emerald-600 text-white" : "bg-zinc-700 text-zinc-300"
                }`}
              >
                {wsConnected ? "LIVE 3D" : "READY"}
              </div>
              {activeClip && (
                <div className="px-2 py-0.5 rounded text-xs font-semibold bg-amber-600/80 text-white">
                  CLIP: {activeClip.clipType}
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Controls */}
      {showControls && (
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-10 flex gap-2">
          <button
            onClick={handlePrevPlay}
            disabled={currentPlay <= 1}
            className="px-4 py-2 bg-black/70 backdrop-blur-md text-white text-xs font-bold rounded-lg shadow border border-white/10 hover:bg-black/90 disabled:opacity-40"
          >
            &larr; Previous Play
          </button>
          <button
            onClick={handleNextPlay}
            className="px-4 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg shadow hover:bg-blue-500"
          >
            Next Play &rarr;
          </button>
          <button
            onClick={() => fetchFormationData(currentPlay)}
            className="px-4 py-2 bg-black/70 backdrop-blur-md text-white text-xs font-bold rounded-lg shadow border border-white/10 hover:bg-black/90"
          >
            &#8635; Reset
          </button>
        </div>
      )}

      {/* Play Info */}
      {formationData && (
        <div className="absolute top-4 right-4 z-10 bg-black/80 backdrop-blur-md text-white px-4 py-2 rounded-lg border border-white/10">
          <div className="text-xs">
            <div className="font-bold text-amber-400">Play #{currentPlay}</div>
            <div className="text-zinc-300">OFF: {formationData.formation.offense.name}</div>
            <div className="text-zinc-300">DEF: {formationData.formation.defense.name}</div>
          </div>
        </div>
      )}

      {/* 3D Scene */}
      <Canvas shadows>
        <PerspectiveCamera makeDefault position={[0, 15, 30]} fov={50} />
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          maxPolarAngle={Math.PI / 2.2}
          minDistance={10}
          maxDistance={60}
        />

        <ambientLight intensity={0.6} />
        <directionalLight
          position={[50, 50, 25]}
          intensity={1.5}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />

        <Environment preset="night" />

        <EnhancedFieldVisualizer
          homeColor={rosterData?.home_team.primary_color || "#003366"}
          awayColor={rosterData?.away_team.primary_color || "#CC0000"}
          showYardLines={true}
          showNumbers={true}
        />

        {playerPositions.map(({ player, position, team }) => (
          <EnhancedPlayerCharacter
            key={`${team}-${player.id}`}
            playerData={player}
            position={position}
            isAnimating={isAnimating}
            detailLevel={detailLevel}
            showNumber={true}
          />
        ))}

        <ContactShadows position={[0, 0.1, 0]} opacity={0.4} scale={100} blur={2} far={10} />
      </Canvas>

      {/* Team Legends */}
      {rosterData && (
        <div className="absolute bottom-4 left-4 z-10 flex gap-2">
          <div
            className="px-3 py-1 rounded text-white text-xs font-black shadow"
            style={{ backgroundColor: rosterData.home_team.primary_color || "#003366" }}
          >
            {rosterData.home_team.name}
          </div>
          <div
            className="px-3 py-1 rounded text-white text-xs font-black shadow"
            style={{ backgroundColor: rosterData.away_team.primary_color || "#CC0000" }}
          >
            {rosterData.away_team.name}
          </div>
        </div>
      )}
    </div>
  );
};

export default LiveGameVisualizer;
