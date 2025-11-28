import { useEffect, useRef, useCallback } from "react";
import { useSimulationStore } from "../store/useSimulationStore";
import { simulationService } from "../services/simulation";

export const useWebSocket = (url: string) => {
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectDelay = 30000; // 30 seconds
  const { updateGameState, addPlay, updateEngineData } = useSimulationStore();

  const syncState = useCallback(async () => {
    try {
      const status = await simulationService.getSimulationStatus();
      updateGameState({
        homeScore: status.homeScore,
        awayScore: status.awayScore,
        quarter: status.currentQuarter,
        timeLeft: status.timeLeft,
        possession: status.possession,
        down: status.down,
        distance: status.distance,
        yardLine: status.yardLine,
      });
      console.log("Game state synchronized");
    } catch (error) {
      console.error("Failed to sync game state:", error);
    }
  }, [updateGameState]);

  useEffect(() => {
    let reconnectTimeout: number;
    let isMounted = true;

    const connect = () => {
      if (socketRef.current?.readyState === WebSocket.OPEN) return;

      const socket = new WebSocket(url);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log("WebSocket connected");
        reconnectAttempts.current = 0;
        syncState();
      };

      socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);

          switch (message.type) {
            case "GAME_UPDATE":
              updateGameState(message.payload);
              break;
            case "PLAY_RESULT":
              addPlay(message.payload);
              break;
            case "ENGINE_UPDATE":
              updateEngineData(message.engine, message.payload);
              break;
            case "PONG":
              // Handle pong if needed
              break;
            default:
              console.warn("Unknown message type:", message.type);
          }
        } catch (error) {
          console.error("Failed to parse WebSocket message:", error);
        }
      };

      socket.onclose = () => {
        if (!isMounted) return;

        const delay = Math.min(
          1000 * Math.pow(2, reconnectAttempts.current),
          maxReconnectDelay
        );
        console.log(`WebSocket disconnected. Reconnecting in ${delay}ms...`);

        reconnectAttempts.current += 1;
        reconnectTimeout = window.setTimeout(connect, delay);
      };

      socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        socket.close();
      };
    };

    connect();

    return () => {
      isMounted = false;
      if (socketRef.current) {
        socketRef.current.close();
      }
      clearTimeout(reconnectTimeout);
    };
  }, [url, updateGameState, addPlay, updateEngineData, syncState]);

  const sendMessage = (type: string, payload: unknown) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type, payload }));
    } else {
      console.warn("WebSocket is not connected");
    }
  };

  return { sendMessage };
};
