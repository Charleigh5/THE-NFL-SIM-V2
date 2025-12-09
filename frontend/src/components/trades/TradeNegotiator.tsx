/**
 * TradeNegotiator Component
 * Enhanced trade interface with drag-and-drop support using dnd-kit
 */
import React, { useState, useEffect } from "react";
import {
  DndContext,
  DragOverlay,
  PointerSensor,
  KeyboardSensor,
  useSensor,
  useSensors,
  closestCenter,
} from "@dnd-kit/core";
import type { DragEndEvent, DragStartEvent } from "@dnd-kit/core";
import { sortableKeyboardCoordinates } from "@dnd-kit/sortable";
import type { Team } from "../../services/api";
import type { TradePlayer, TradeEvaluation } from "../../types/trade";
import { tradeApi } from "../../services/tradeApi";
import { DraggableAsset } from "./DraggableAsset";
import { DroppableZone } from "./DroppableZone";
import { FeedbackCollector } from "../draft/FeedbackCollector";
import "./TradeNegotiator.css";

interface TradeNegotiatorProps {
  seasonId: number;
  userTeamId: number;
}

export const TradeNegotiator: React.FC<TradeNegotiatorProps> = ({ seasonId, userTeamId }) => {
  // State for teams and players
  const [tradePartners, setTradePartners] = useState<Team[]>([]);
  const [selectedPartner, setSelectedPartner] = useState<Team | null>(null);
  const [userPlayers, setUserPlayers] = useState<TradePlayer[]>([]);
  const [partnerPlayers, setPartnerPlayers] = useState<TradePlayer[]>([]);

  // State for trade assets
  const [offeredPlayers, setOfferedPlayers] = useState<TradePlayer[]>([]);
  const [requestedPlayers, setRequestedPlayers] = useState<TradePlayer[]>([]);

  // State for drag and drop
  const [activeId, setActiveId] = useState<string | null>(null);
  const [activeDragPlayer, setActiveDragPlayer] = useState<TradePlayer | null>(null);

  // State for evaluation
  const [evaluation, setEvaluation] = useState<TradeEvaluation | null>(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Loading states
  const [loading, setLoading] = useState(true);
  const [loadingPartnerRoster, setLoadingPartnerRoster] = useState(false);

  // Configure drag sensors
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // 8px movement required before drag starts
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // Fetch initial data
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [partners, players] = await Promise.all([
          tradeApi.getTradePartners(userTeamId),
          tradeApi.getTradeablePlayers(userTeamId),
        ]);
        setTradePartners(partners);
        setUserPlayers(players);
      } catch (err) {
        console.error("Failed to load trade data:", err);
        setError("Failed to load trade data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [userTeamId]);

  // Fetch partner players when partner is selected
  useEffect(() => {
    if (selectedPartner) {
      const fetchPartnerPlayers = async () => {
        setLoadingPartnerRoster(true);
        try {
          const players = await tradeApi.getTradeablePlayers(selectedPartner.id);
          setPartnerPlayers(players);
        } catch (err) {
          console.error("Failed to load partner roster:", err);
        } finally {
          setLoadingPartnerRoster(false);
        }
      };
      fetchPartnerPlayers();
    } else {
      setPartnerPlayers([]);
    }
  }, [selectedPartner]);

  // Handle drag start
  const handleDragStart = (event: DragStartEvent) => {
    const { active } = event;
    setActiveId(active.id as string);

    // Find the player being dragged
    const playerId = parseInt((active.id as string).split("-").pop() || "0");
    const player =
      userPlayers.find((p) => p.id === playerId) ||
      partnerPlayers.find((p) => p.id === playerId) ||
      offeredPlayers.find((p) => p.id === playerId) ||
      requestedPlayers.find((p) => p.id === playerId);

    setActiveDragPlayer(player || null);
  };

  // Handle drag end
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveId(null);
    setActiveDragPlayer(null);

    if (!over) return;

    const activeId = active.id as string;
    const overId = over.id as string;

    // Extract player ID from the active draggable
    const playerId = parseInt(activeId.split("-").pop() || "0");

    // Find the player
    const player =
      userPlayers.find((p) => p.id === playerId) ||
      partnerPlayers.find((p) => p.id === playerId) ||
      offeredPlayers.find((p) => p.id === playerId) ||
      requestedPlayers.find((p) => p.id === playerId);

    if (!player) return;

    // Determine source and destination
    const isFromUserPool = userPlayers.some((p) => p.id === playerId);
    const isFromPartnerPool = partnerPlayers.some((p) => p.id === playerId);
    const isFromOffered = offeredPlayers.some((p) => p.id === playerId);
    const isFromRequested = requestedPlayers.some((p) => p.id === playerId);

    // Handle drop into offered zone
    if (overId === "offered-zone") {
      if (isFromUserPool && !offeredPlayers.find((p) => p.id === playerId)) {
        setOfferedPlayers([...offeredPlayers, player]);
        setEvaluation(null);
      } else if (isFromRequested) {
        // Move from requested to offered
        setRequestedPlayers(requestedPlayers.filter((p) => p.id !== playerId));
        if (!offeredPlayers.find((p) => p.id === playerId)) {
          setOfferedPlayers([...offeredPlayers, player]);
        }
        setEvaluation(null);
      }
    }

    // Handle drop into requested zone
    if (overId === "requested-zone") {
      if (isFromPartnerPool && !requestedPlayers.find((p) => p.id === playerId)) {
        setRequestedPlayers([...requestedPlayers, player]);
        setEvaluation(null);
      } else if (isFromOffered) {
        // Move from offered to requested
        setOfferedPlayers(offeredPlayers.filter((p) => p.id !== playerId));
        if (!requestedPlayers.find((p) => p.id === playerId)) {
          setRequestedPlayers([...requestedPlayers, player]);
        }
        setEvaluation(null);
      }
    }
  };

  // Remove player from offer
  const handleRemoveFromOffer = (playerId: number) => {
    setOfferedPlayers(offeredPlayers.filter((p) => p.id !== playerId));
    setEvaluation(null);
  };

  // Remove player from request
  const handleRemoveFromRequest = (playerId: number) => {
    setRequestedPlayers(requestedPlayers.filter((p) => p.id !== playerId));
    setEvaluation(null);
  };

  // Evaluate trade
  const handleEvaluateTrade = async () => {
    if (!selectedPartner) return;
    if (offeredPlayers.length === 0 && requestedPlayers.length === 0) return;

    setIsEvaluating(true);
    setError(null);

    try {
      const result = await tradeApi.evaluateTrade(
        selectedPartner.id,
        requestedPlayers.map((p) => p.id),
        offeredPlayers.map((p) => p.id)
      );
      setEvaluation(result);
    } catch (err) {
      console.error("Trade evaluation failed:", err);
      setError("Failed to evaluate trade. Please try again.");
    } finally {
      setIsEvaluating(false);
    }
  };

  // Clear trade
  const handleClearTrade = () => {
    setOfferedPlayers([]);
    setRequestedPlayers([]);
    setEvaluation(null);
  };

  // Calculate trade values
  const offeredValue = offeredPlayers.reduce((sum, p) => sum + p.trade_value, 0);
  const requestedValue = requestedPlayers.reduce((sum, p) => sum + p.trade_value, 0);
  const valueDifference = offeredValue - requestedValue;

  // Get available players (not in trade)
  const availableUserPlayers = userPlayers.filter(
    (p) => !offeredPlayers.find((op) => op.id === p.id)
  );
  const availablePartnerPlayers = partnerPlayers.filter(
    (p) => !requestedPlayers.find((rp) => rp.id === p.id)
  );

  if (loading) {
    return (
      <div className="trade-negotiator" data-testid="trade-negotiator-loading">
        <div className="trade-loading">
          <div className="spinner"></div>
          <p>Loading Trade Negotiator...</p>
        </div>
      </div>
    );
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <div className="trade-negotiator" data-testid="trade-negotiator">
        {/* Header */}
        <div className="trade-negotiator-header">
          <h2>Trade Negotiator</h2>
          <div className="drag-hint">💡 Drag players to propose trades</div>
        </div>

        {/* Team Selector */}
        <div className="team-selector-section">
          <label className="team-selector-label">Select Trade Partner</label>
          <select
            className="team-selector-dropdown"
            value={selectedPartner?.id || ""}
            onChange={(e) => {
              const partner = tradePartners.find((t) => t.id === Number(e.target.value));
              setSelectedPartner(partner || null);
              setRequestedPlayers([]);
              setEvaluation(null);
            }}
            data-testid="trade-partner-select"
            aria-label="Select trade partner team"
          >
            <option value="">Choose a team...</option>
            {tradePartners.map((team) => (
              <option key={team.id} value={team.id}>
                {team.city} {team.name} ({team.wins}-{team.losses})
              </option>
            ))}
          </select>
        </div>

        {/* Main Trade Area */}
        <div className="trade-grid">
          {/* User Assets Pool */}
          <div className="asset-pool">
            <h3>Your Roster</h3>
            <div className="player-list">
              {availableUserPlayers.map((player) => (
                <DraggableAsset key={player.id} id={`user-player-${player.id}`} player={player} />
              ))}
            </div>
          </div>

          {/* Offered Zone */}
          <DroppableZone
            id="offered-zone"
            title="You Offer"
            players={offeredPlayers}
            onRemove={handleRemoveFromOffer}
            emptyMessage="Drag your players here"
          />

          {/* Requested Zone */}
          <DroppableZone
            id="requested-zone"
            title="You Receive"
            players={requestedPlayers}
            onRemove={handleRemoveFromRequest}
            emptyMessage="Drag their players here"
          />

          {/* Partner Assets Pool */}
          <div className="asset-pool">
            <h3>{selectedPartner ? `${selectedPartner.name} Roster` : "Select Team"}</h3>
            {selectedPartner && (
              <div className="player-list">
                {loadingPartnerRoster ? (
                  <div className="loading-roster">Loading...</div>
                ) : (
                  availablePartnerPlayers.map((player) => (
                    <DraggableAsset
                      key={player.id}
                      id={`partner-player-${player.id}`}
                      player={player}
                    />
                  ))
                )}
              </div>
            )}
          </div>
        </div>

        {/* Trade Summary */}
        <div className="trade-summary">
          <div className="trade-value-comparison">
            <div className="value-side offering">
              <div className="label">You Offer</div>
              <div className="value">{offeredValue}</div>
            </div>
            <div
              className={`value-difference ${
                valueDifference > 0 ? "favor-offer" : valueDifference < 0 ? "favor-receive" : "even"
              }`}
            >
              <div className="arrow">⇄</div>
              <div className="diff">
                {valueDifference > 0 ? `+${valueDifference}` : valueDifference}
              </div>
            </div>
            <div className="value-side receiving">
              <div className="label">You Receive</div>
              <div className="value">{requestedValue}</div>
            </div>
          </div>

          <div className="trade-actions">
            <button
              className="trade-btn secondary"
              onClick={handleClearTrade}
              disabled={offeredPlayers.length === 0 && requestedPlayers.length === 0}
            >
              Clear Trade
            </button>
            <button
              className="trade-btn primary"
              onClick={handleEvaluateTrade}
              disabled={
                !selectedPartner ||
                (offeredPlayers.length === 0 && requestedPlayers.length === 0) ||
                isEvaluating
              }
              data-testid="evaluate-trade-btn"
            >
              {isEvaluating ? "Analyzing..." : "Get GM Response"}
            </button>
          </div>

          {error && <div className="trade-error">{error}</div>}

          {/* GM Response */}
          {evaluation && (
            <div
              className={`gm-response ${evaluation.decision.toLowerCase()}`}
              data-testid="gm-response"
            >
              <div className="gm-response-header">
                <div className="gm-avatar">👔</div>
                <div className="gm-info">
                  <h4>
                    {selectedPartner?.city} {selectedPartner?.name} GM
                  </h4>
                  <span className="gm-verdict">{evaluation.decision}</span>
                </div>
              </div>
              <p>"{evaluation.reasoning}"</p>

              <FeedbackCollector
                contextId={`trade-${seasonId}-${userTeamId}-${selectedPartner?.id}-${Date.now()}`}
                contextType="trade"
              />
            </div>
          )}
        </div>

        {/* Drag Overlay */}
        <DragOverlay>
          {activeId && activeDragPlayer ? (
            <DraggableAsset id={activeId} player={activeDragPlayer} disabled />
          ) : null}
        </DragOverlay>
      </div>
    </DndContext>
  );
};

export default TradeNegotiator;
