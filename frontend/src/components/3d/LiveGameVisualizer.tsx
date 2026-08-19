import React, { useState, useEffect, useRef, useCallback } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, PerspectiveCamera, Environment, ContactShadows } from "@react-three/drei";
import * as THREE from "three";
import EnhancedPlayerCharacter from "./EnhancedPlayerCharacter";
import EnhancedFieldVisualizer from "./EnhancedFieldVisualizer";

interface PlayerVisualData {
  id: number;
  name: string;
  number: number;
  position: string;
  position_group: "offense" | "defense" | "special_teams";
  height: number;
  weight: number;
  team_id: number;
  visuals: {
    body_type: "large" | "medium" | "lean" | "athletic" | "pocket" | "muscular";
    jersey_color_primary: string;
    jersey_color_secondary: string;
    helmet_design: {
      base: string;
      stripe: string;
      logo_side: boolean;
      facemask: string;
    };
    face_mask_color: string;
    cleat_color: string;
    accessories: string[];
  };
}

interface TeamVisualData {
  id: number;
  name: string;
  abbreviation: string;
  primary_color: string;
  secondary_color: string;
  logo_url: string;
  players: PlayerVisualData[];
}

interface GameRosterData {
  game_id: number;
  home_team: TeamVisualData;
  away_team: TeamVisualData;
}

interface FormationData {
  play_id: number;
  formation: {
    offense: {
      name: string;
      players: Array<{ position: string; x: number; y: number; z: number }>;
    };
    defense: {
      name: string;
      players: Array<{ position: string; x: number; y: number; z: number }>;
    };
  };
}

interface LiveGameVisualizerProps {
  gameId: number;
  apiUrl?: string;
  autoConnect?: boolean;
  showControls?: boolean;
  detailLevel?: "low" | "medium" | "high";
}

export const LiveGameVisualizer = ({
  gameId,
  apiUrl = "http://localhost:8000/api/live",
  autoConnect = true,
  showControls = true,
  detailLevel = "medium",
}: LiveGameVisualizerProps) => {
  const [rosterData, setRosterData] = useState<GameRosterData | null>(null);
  const [formationData, setFormationData] = useState<FormationData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [wsConnected, setWsConnected] = useState(false);
  const [currentPlay, setCurrentPlay] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  
  const wsRef = useRef<WebSocket | null>(null);
  const animationFrameRef = useRef<number>();

  // Fetch roster data
  const fetchRosterData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiUrl}/game/${gameId}/roster`);
      if (!response.ok) {
        throw new Error(`Failed to fetch roster: ${response.statusText}`);
      }
      const data = await response.json();
      setRosterData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [gameId, apiUrl]);

  // Fetch formation data
  const fetchFormationData = useCallback(async (playId: number) => {
    try {
      const response = await fetch(`${apiUrl}/game/${gameId}/formation/${playId}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch formation: ${response.statusText}`);
      }
      const data = await response.json();
      setFormationData(data);
    } catch (err) {
      console.error("Formation fetch error:", err);
    }
  }, [gameId, apiUrl]);

  // WebSocket connection for live updates
  useEffect(() => {
    if (!autoConnect) return;

    const wsUrl = `ws://localhost:8000/api/live/ws/game/${gameId}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      setWsConnected(true);
      console.log("WebSocket connected");
      // Send ping to keep connection alive
      const pingInterval = setInterval(() => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send("ping");
        }
      }, 30000);
      return () => clearInterval(pingInterval);
    };

    wsRef.current.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        // Handle different message types
        switch (message.type) {
          case "play_start":
            setIsAnimating(true);
            break;
          case "play_end":
            setIsAnimating(false);
            break;
          case "player_update":
            // Update player positions in real-time
            break;
          case "pong":
            // Heartbeat response
            break;
          default:
            console.log("WS Message:", message);
        }
      } catch (err) {
        console.error("WS message parse error:", err);
      }
    };

    wsRef.current.onclose = () => {
      setWsConnected(false);
      console.log("WebSocket disconnected");
    };

    wsRef.current.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [gameId, autoConnect]);

  // Initial data fetch
  useEffect(() => {
    fetchRosterData();
    fetchFormationData(1);
  }, [fetchRosterData, fetchFormationData]);

  // Map players to formation positions
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

    // Map offense (home team)
    offenseFormation.forEach((formPlayer, index) => {
      if (homePlayers[index]) {
        positionedPlayers.push({
          player: homePlayers[index],
          position: [formPlayer.x, formPlayer.y, formPlayer.z],
          team: "home",
        });
      }
    });

    // Map defense (away team)
    defenseFormation.forEach((formPlayer, index) => {
      if (awayPlayers[index]) {
        positionedPlayers.push({
          player: awayPlayers[index],
          position: [formPlayer.x + 10, formPlayer.y, formPlayer.z], // Offset defense
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
      <div className="flex items-center justify-center h-96 bg-gray-900 text-white">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p>Loading game visualization...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-900 text-white">
        <div className="text-center">
          <p className="text-red-500 mb-4">Error: {error}</p>
          <button
            onClick={fetchRosterData}
            className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const playerPositions = getPlayerPositions();

  return (
    <div className="w-full h-[600px] bg-gradient-to-b from-sky-400 to-sky-200 rounded-lg overflow-hidden relative">
      {/* HUD Overlay */}
      <div className="absolute top-4 left-4 z-10 bg-black/70 text-white px-4 py-2 rounded-lg">
        <div className="flex items-center gap-4">
          {rosterData && (
            <>
              <div className="text-lg font-bold">
                {rosterData.home_team.abbreviation} vs {rosterData.away_team.abbreviation}
              </div>
              <div className={`px-2 py-1 rounded ${wsConnected ? "bg-green-600" : "bg-red-600"}`}>
                {wsConnected ? "LIVE" : "OFFLINE"}
              </div>
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
            className="px-4 py-2 bg-white/90 rounded-lg shadow hover:bg-white disabled:opacity-50"
          >
            ← Previous Play
          </button>
          <button
            onClick={handleNextPlay}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700"
          >
            Next Play →
          </button>
          <button
            onClick={() => fetchFormationData(currentPlay)}
            className="px-4 py-2 bg-white/90 rounded-lg shadow hover:bg-white"
          >
            ↻ Reset
          </button>
        </div>
      )}

      {/* Play Info */}
      {formationData && (
        <div className="absolute top-4 right-4 z-10 bg-black/70 text-white px-4 py-2 rounded-lg">
          <div className="text-sm">
            <div>Play #{currentPlay}</div>
            <div className="text-xs text-gray-300">
              OFF: {formationData.formation.offense.name}
            </div>
            <div className="text-xs text-gray-300">
              DEF: {formationData.formation.defense.name}
            </div>
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
          maxDistance={50}
        />
        
        {/* Lighting */}
        <ambientLight intensity={0.6} />
        <directionalLight
          position={[50, 50, 25]}
          intensity={1.5}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        
        {/* Environment */}
        <Environment preset="clear" />

        {/* Field */}
        <EnhancedFieldVisualizer
          homeColor={rosterData?.home_team.primary_color || "#003366"}
          awayColor={rosterData?.away_team.primary_color || "#CC0000"}
          showYardLines={true}
          showNumbers={true}
        />

        {/* Players */}
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

        {/* Shadows */}
        <ContactShadows
          position={[0, 0.1, 0]}
          opacity={0.4}
          scale={100}
          blur={2}
          far={10}
        />
      </Canvas>

      {/* Team Legends */}
      {rosterData && (
        <div className="absolute bottom-4 left-4 z-10 flex gap-4">
          <div
            className="px-3 py-1 rounded text-white text-sm font-bold"
            style={{ backgroundColor: rosterData.home_team.primary_color }}
          >
            {rosterData.home_team.name}
          </div>
          <div
            className="px-3 py-1 rounded text-white text-sm font-bold"
            style={{ backgroundColor: rosterData.away_team.primary_color }}
          >
            {rosterData.away_team.name}
          </div>
        </div>
      )}
    </div>
  );
};

export default LiveGameVisualizer;
