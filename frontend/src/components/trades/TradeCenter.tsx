/**
 * TradeCenter Component
 * Main trade negotiation interface with drag-and-drop support
 */
import React, { useState, useEffect, useCallback } from "react";
import type { Team } from "../../services/api";
import type { TradePlayer, TradeEvaluation } from "../../types/trade";
import { tradeApi } from "../../services/tradeApi";
import { FeedbackCollector } from "../draft/FeedbackCollector";
import "./TradeCenter.css";

interface TradeCenterProps {
  seasonId: number;
  userTeamId: number;
  userTeam: Team;
}

export const TradeCenter: React.FC<TradeCenterProps> = ({ seasonId, userTeamId, userTeam }) => {
  // State for teams and players
  const [tradePartners, setTradePartners] = useState<Team[]>([]);
  const [selectedPartner, setSelectedPartner] = useState<Team | null>(null);
  const [userPlayers, setUserPlayers] = useState<TradePlayer[]>([]);
  const [partnerPlayers, setPartnerPlayers] = useState<TradePlayer[]>([]);

  // State for trade assets
  const [offeredPlayers, setOfferedPlayers] = useState<TradePlayer[]>([]);
  const [requestedPlayers, setRequestedPlayers] = useState<TradePlayer[]>([]);

  // State for filters
  const [userSearchTerm, setUserSearchTerm] = useState("");
  const [partnerSearchTerm, setPartnerSearchTerm] = useState("");
  const [userPositionFilter, setUserPositionFilter] = useState<string>("ALL");
  const [partnerPositionFilter, setPartnerPositionFilter] = useState<string>("ALL");

  // State for evaluation
  const [evaluation, setEvaluation] = useState<TradeEvaluation | null>(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Loading states
  const [loading, setLoading] = useState(true);
  const [loadingPartnerRoster, setLoadingPartnerRoster] = useState(false);

  // Position groups for filtering
  const positions = ["ALL", "QB", "RB", "WR", "TE", "OL", "DL", "LB", "CB", "S"];

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

  // Calculate trade values
  const offeredValue = offeredPlayers.reduce((sum, p) => sum + p.trade_value, 0);
  const requestedValue = requestedPlayers.reduce((sum, p) => sum + p.trade_value, 0);
  const valueDifference = offeredValue - requestedValue;

  // Filter players
  const filterPlayers = useCallback(
    (
      players: TradePlayer[],
      searchTerm: string,
      positionFilter: string,
      excludeIds: number[]
    ): TradePlayer[] => {
      return players.filter((p) => {
        if (excludeIds.includes(p.id)) return false;
        if (positionFilter !== "ALL") {
          const posGroup = getPositionGroup(p.position);
          if (posGroup !== positionFilter && p.position !== positionFilter) return false;
        }
        if (searchTerm) {
          const fullName = `${p.first_name} ${p.last_name}`.toLowerCase();
          if (!fullName.includes(searchTerm.toLowerCase())) return false;
        }
        return true;
      });
    },
    []
  );

  // Get position group for filtering
  const getPositionGroup = (position: string): string => {
    if (["LT", "LG", "C", "RG", "RT", "OT", "OG"].includes(position)) return "OL";
    if (["DE", "DT", "NT"].includes(position)) return "DL";
    if (["MLB", "OLB", "ILB"].includes(position)) return "LB";
    if (["FS", "SS"].includes(position)) return "S";
    return position;
  };

  // Add player to offer
  const handleAddToOffer = (player: TradePlayer) => {
    if (!offeredPlayers.find((p) => p.id === player.id)) {
      setOfferedPlayers([...offeredPlayers, player]);
      setEvaluation(null); // Reset evaluation when trade changes
    }
  };

  // Remove player from offer
  const handleRemoveFromOffer = (playerId: number) => {
    setOfferedPlayers(offeredPlayers.filter((p) => p.id !== playerId));
    setEvaluation(null);
  };

  // Add player to request
  const handleAddToRequest = (player: TradePlayer) => {
    if (!requestedPlayers.find((p) => p.id === player.id)) {
      setRequestedPlayers([...requestedPlayers, player]);
      setEvaluation(null);
    }
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
        seasonId,
        selectedPartner.id, // Evaluate from partner's perspective
        requestedPlayers.map((p) => p.id), // What they're giving up
        offeredPlayers.map((p) => p.id) // What they're receiving
      );
      setEvaluation(result);
    } catch (err) {
      console.error("Trade evaluation failed:", err);
      setError("Failed to evaluate trade. Please try again.");
    } finally {
      setIsEvaluating(false);
    }
  };

  // Execute trade
  const handleExecuteTrade = async () => {
    if (!selectedPartner || !evaluation || evaluation.decision !== "ACCEPT") return;

    try {
      const result = await tradeApi.executeTrade({
        offering_team_id: userTeamId,
        receiving_team_id: selectedPartner.id,
        offered_players: offeredPlayers.map((p) => p.id),
        offered_picks: [],
        requested_players: requestedPlayers.map((p) => p.id),
        requested_picks: [],
        status: "accepted",
      });

      if (result.success) {
        // Reset trade
        setOfferedPlayers([]);
        setRequestedPlayers([]);
        setEvaluation(null);
        setSelectedPartner(null);

        // Refresh user's roster
        const players = await tradeApi.getTradeablePlayers(userTeamId);
        setUserPlayers(players);
      }
    } catch (err) {
      console.error("Trade execution failed:", err);
      setError("Failed to execute trade.");
    }
  };

  // Clear trade
  const handleClearTrade = () => {
    setOfferedPlayers([]);
    setRequestedPlayers([]);
    setEvaluation(null);
  };

  // Get overall rating class
  const getOverallClass = (overall: number): string => {
    if (overall >= 90) return "elite";
    if (overall >= 80) return "great";
    if (overall >= 70) return "good";
    if (overall >= 60) return "average";
    return "below";
  };

  // Filter available players (excluding those already in trade)
  const availableUserPlayers = filterPlayers(
    userPlayers,
    userSearchTerm,
    userPositionFilter,
    offeredPlayers.map((p) => p.id)
  );

  const availablePartnerPlayers = filterPlayers(
    partnerPlayers,
    partnerSearchTerm,
    partnerPositionFilter,
    requestedPlayers.map((p) => p.id)
  );

  if (loading) {
    return (
      <div className="trade-center" data-testid="trade-center-loading">
        <div className="trade-loading">
          <div className="spinner"></div>
          <p>Loading Trade Center...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="trade-center" data-testid="trade-center">
      {/* Header */}
      <div className="trade-center-header">
        <h2>Trade Center</h2>
        <div className="trade-phase-indicator">
          <span className="phase-badge active">Negotiate</span>
          <span className="phase-badge inactive">Evaluate</span>
          <span className="phase-badge inactive">Execute</span>
        </div>
      </div>

      {/* User Team Panel (Offering) */}
      <div className="trade-panel" data-testid="user-trade-panel">
        <div className="trade-panel-header">
          <h3>Your Assets</h3>
          <div className="team-badge">
            {userTeam.abbreviation} • {userTeam.city} {userTeam.name}
          </div>
        </div>
        <div className="trade-panel-content">
          {/* Offered Players Drop Zone */}
          <div className="trade-drop-zone" data-testid="offered-drop-zone">
            {offeredPlayers.length === 0 ? (
              <div className="trade-drop-zone-placeholder">
                <span className="icon">➕</span>
                <p>Click players below to add them to the trade</p>
              </div>
            ) : (
              offeredPlayers.map((player) => (
                <div
                  key={player.id}
                  className="trade-player-card selected"
                  data-testid={`offered-player-${player.id}`}
                >
                  <div className="position-badge">{player.position}</div>
                  <div className="player-info">
                    <div className="player-name">
                      {player.first_name} {player.last_name}
                    </div>
                    <div className="player-details">
                      <span>Age {player.age}</span>
                    </div>
                  </div>
                  <span className={`overall-badge ${getOverallClass(player.overall_rating)}`}>
                    {player.overall_rating}
                  </span>
                  <div className="trade-value">
                    <span className="value-label">Value</span>
                    <span className="value-number">{player.trade_value}</span>
                  </div>
                  <button
                    className="remove-btn"
                    onClick={() => handleRemoveFromOffer(player.id)}
                    aria-label="Remove player"
                  >
                    ✕
                  </button>
                </div>
              ))
            )}
          </div>

          {/* Search and Filter */}
          <div className="player-search">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Search players..."
              value={userSearchTerm}
              onChange={(e) => setUserSearchTerm(e.target.value)}
              data-testid="user-player-search"
            />
          </div>

          <div className="position-filters">
            {positions.map((pos) => (
              <button
                key={pos}
                className={`position-filter-btn ${userPositionFilter === pos ? "active" : ""}`}
                onClick={() => setUserPositionFilter(pos)}
              >
                {pos}
              </button>
            ))}
          </div>

          {/* Available Players */}
          <div className="available-players" data-testid="user-available-players">
            {availableUserPlayers.slice(0, 10).map((player) => (
              <div
                key={player.id}
                className="trade-player-card"
                onClick={() => handleAddToOffer(player)}
                data-testid={`user-player-${player.id}`}
              >
                <div className="position-badge">{player.position}</div>
                <div className="player-info">
                  <div className="player-name">
                    {player.first_name} {player.last_name}
                  </div>
                  <div className="player-details">
                    <span>Age {player.age}</span>
                  </div>
                </div>
                <span className={`overall-badge ${getOverallClass(player.overall_rating)}`}>
                  {player.overall_rating}
                </span>
                <div className="trade-value">
                  <span className="value-label">Value</span>
                  <span className="value-number">{player.trade_value}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Trade Partner Panel (Requesting) */}
      <div className="trade-panel" data-testid="partner-trade-panel">
        <div className="trade-panel-header">
          <h3>Their Assets</h3>
          {selectedPartner && (
            <div className="team-badge">
              {selectedPartner.abbreviation} • {selectedPartner.city} {selectedPartner.name}
            </div>
          )}
        </div>
        <div className="trade-panel-content">
          {/* Team Selector */}
          <div className="team-selector">
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

          {selectedPartner && (
            <>
              {/* Requested Players Drop Zone */}
              <div className="trade-drop-zone" data-testid="requested-drop-zone">
                {requestedPlayers.length === 0 ? (
                  <div className="trade-drop-zone-placeholder">
                    <span className="icon">➕</span>
                    <p>Click players below to request them</p>
                  </div>
                ) : (
                  requestedPlayers.map((player) => (
                    <div
                      key={player.id}
                      className="trade-player-card selected"
                      data-testid={`requested-player-${player.id}`}
                    >
                      <div className="position-badge">{player.position}</div>
                      <div className="player-info">
                        <div className="player-name">
                          {player.first_name} {player.last_name}
                        </div>
                        <div className="player-details">
                          <span>Age {player.age}</span>
                        </div>
                      </div>
                      <span className={`overall-badge ${getOverallClass(player.overall_rating)}`}>
                        {player.overall_rating}
                      </span>
                      <div className="trade-value">
                        <span className="value-label">Value</span>
                        <span className="value-number">{player.trade_value}</span>
                      </div>
                      <button
                        className="remove-btn"
                        onClick={() => handleRemoveFromRequest(player.id)}
                        aria-label="Remove player"
                      >
                        ✕
                      </button>
                    </div>
                  ))
                )}
              </div>

              {/* Search and Filter */}
              <div className="player-search">
                <span className="search-icon">🔍</span>
                <input
                  type="text"
                  placeholder="Search players..."
                  value={partnerSearchTerm}
                  onChange={(e) => setPartnerSearchTerm(e.target.value)}
                  data-testid="partner-player-search"
                />
              </div>

              <div className="position-filters">
                {positions.map((pos) => (
                  <button
                    key={pos}
                    className={`position-filter-btn ${partnerPositionFilter === pos ? "active" : ""}`}
                    onClick={() => setPartnerPositionFilter(pos)}
                  >
                    {pos}
                  </button>
                ))}
              </div>

              {/* Partner's Available Players */}
              {loadingPartnerRoster ? (
                <div className="trade-loading">
                  <div className="spinner"></div>
                  <p>Loading roster...</p>
                </div>
              ) : (
                <div className="available-players" data-testid="partner-available-players">
                  {availablePartnerPlayers.slice(0, 10).map((player) => (
                    <div
                      key={player.id}
                      className="trade-player-card"
                      onClick={() => handleAddToRequest(player)}
                      data-testid={`partner-player-${player.id}`}
                    >
                      <div className="position-badge">{player.position}</div>
                      <div className="player-info">
                        <div className="player-name">
                          {player.first_name} {player.last_name}
                        </div>
                        <div className="player-details">
                          <span>Age {player.age}</span>
                        </div>
                      </div>
                      <span className={`overall-badge ${getOverallClass(player.overall_rating)}`}>
                        {player.overall_rating}
                      </span>
                      <div className="trade-value">
                        <span className="value-label">Value</span>
                        <span className="value-number">{player.trade_value}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}

          {!selectedPartner && (
            <div className="trade-drop-zone-placeholder">
              <span className="icon">🏈</span>
              <p>Select a team above to view their roster</p>
            </div>
          )}
        </div>
      </div>

      {/* Trade Summary */}
      <div className="trade-summary" data-testid="trade-summary">
        <div className="trade-summary-header">
          <h3>Trade Summary</h3>
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
          {evaluation && evaluation.decision === "ACCEPT" && (
            <button
              className="trade-btn primary"
              onClick={handleExecuteTrade}
              data-testid="execute-trade-btn"
            >
              Execute Trade
            </button>
          )}
        </div>

        {error && <div className="analyzer-error trade-error-centered">{error}</div>}

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
    </div>
  );
};

export default TradeCenter;
