/**
 * TradeCenter Component
 * Main trade negotiation interface with drag-and-drop support
 */
import React, { useState, useEffect, useCallback } from "react";
import type { Team } from "../../services/api";
import type { TradePlayer, TradeEvaluation } from "../../types/trade";
import { tradeApi } from "../../services/tradeApi";
import { FeedbackCollector } from "../draft/FeedbackCollector";
import { PendingOffers } from "./PendingOffers";
import { motion, AnimatePresence } from "framer-motion";
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
      // Use the new /api/trades/evaluate endpoint
      // From the target team's perspective: they give up requestedPlayers and receive offeredPlayers
      const result = await tradeApi.evaluateTrade(
        selectedPartner.id, // target team evaluates the trade
        requestedPlayers.map((p) => p.id), // what they're giving up (offered TO them from their POV)
        offeredPlayers.map((p) => p.id) // what they're receiving (requested FROM them from their POV)
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

  // Tab state
  const [activeTab, setActiveTab] = useState<"negotiate" | "offers">("negotiate");

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
    <motion.div
      className="trade-center"
      data-testid="trade-center"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="trade-center-header">
        <h2>Trade Center</h2>
        <div className="trade-phase-indicator">
          <button
            className={`phase-badge ${activeTab === "negotiate" ? "active" : "inactive"}`}
            onClick={() => setActiveTab("negotiate")}
          >
            Negotiate
          </button>
          <button
            className={`phase-badge ${activeTab === "offers" ? "active" : "inactive"}`}
            onClick={() => setActiveTab("offers")}
          >
            Offers
          </button>
        </div>
      </div>

      <AnimatePresence mode="wait">
        {activeTab === "offers" ? (
          <motion.div
            key="offers"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            <PendingOffers teamId={userTeamId} />
          </motion.div>
        ) : (
          <motion.div
            key="negotiate"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.3 }}
          >
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
                  <AnimatePresence>
                    {offeredPlayers.length === 0 ? (
                      <motion.div
                        className="trade-drop-zone-placeholder"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                      >
                        <span className="icon">➕</span>
                        <p>Click players below to add them to the trade</p>
                      </motion.div>
                    ) : (
                      offeredPlayers.map((player) => (
                        <motion.div
                          key={player.id}
                          layoutId={`player-${player.id}`}
                          className="trade-player-card selected"
                          data-testid={`offered-player-${player.id}`}
                          initial={{ scale: 0.8, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          exit={{ scale: 0.8, opacity: 0 }}
                          transition={{ type: "spring", stiffness: 300, damping: 25 }}
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
                          <span
                            className={`overall-badge ${getOverallClass(player.overall_rating)}`}
                          >
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
                        </motion.div>
                      ))
                    )}
                  </AnimatePresence>
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
                  <AnimatePresence mode="popLayout">
                    {availableUserPlayers.slice(0, 10).map((player) => (
                      <motion.div
                        key={player.id}
                        layoutId={`player-${player.id}`}
                        className="trade-player-card"
                        onClick={() => handleAddToOffer(player)}
                        data-testid={`user-player-${player.id}`}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9 }}
                        whileHover={{ scale: 1.02, backgroundColor: "rgba(255, 255, 255, 0.05)" }}
                        whileTap={{ scale: 0.98 }}
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
                      </motion.div>
                    ))}
                  </AnimatePresence>
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
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.3 }}
                  >
                    {/* Requested Players Drop Zone */}
                    <div className="trade-drop-zone" data-testid="requested-drop-zone">
                      <AnimatePresence>
                        {requestedPlayers.length === 0 ? (
                          <motion.div
                            className="trade-drop-zone-placeholder"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                          >
                            <span className="icon">➕</span>
                            <p>Click players below to request them</p>
                          </motion.div>
                        ) : (
                          requestedPlayers.map((player) => (
                            <motion.div
                              key={player.id}
                              layoutId={`player-${player.id}`}
                              className="trade-player-card selected"
                              data-testid={`requested-player-${player.id}`}
                              initial={{ scale: 0.8, opacity: 0 }}
                              animate={{ scale: 1, opacity: 1 }}
                              exit={{ scale: 0.8, opacity: 0 }}
                              transition={{ type: "spring", stiffness: 300, damping: 25 }}
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
                              <span
                                className={`overall-badge ${getOverallClass(player.overall_rating)}`}
                              >
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
                            </motion.div>
                          ))
                        )}
                      </AnimatePresence>
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
                        <AnimatePresence mode="popLayout">
                          {availablePartnerPlayers.slice(0, 10).map((player) => (
                            <motion.div
                              key={player.id}
                              layoutId={`player-${player.id}`}
                              className="trade-player-card"
                              onClick={() => handleAddToRequest(player)}
                              data-testid={`partner-player-${player.id}`}
                              initial={{ opacity: 0, y: 10 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, scale: 0.9 }}
                              whileHover={{
                                scale: 1.02,
                                backgroundColor: "rgba(255, 255, 255, 0.05)",
                              }}
                              whileTap={{ scale: 0.98 }}
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
                              <span
                                className={`overall-badge ${getOverallClass(player.overall_rating)}`}
                              >
                                {player.overall_rating}
                              </span>
                              <div className="trade-value">
                                <span className="value-label">Value</span>
                                <span className="value-number">{player.trade_value}</span>
                              </div>
                            </motion.div>
                          ))}
                        </AnimatePresence>
                      </div>
                    )}
                  </motion.div>
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
                    <motion.div
                      key={offeredValue}
                      initial={{ scale: 1.2, color: "#fff" }}
                      animate={{ scale: 1, color: "rgba(255,255,255,0.7)" }}
                      className="value"
                    >
                      {offeredValue}
                    </motion.div>
                  </div>
                  <div
                    className={`value-difference ${
                      valueDifference > 0
                        ? "favor-offer"
                        : valueDifference < 0
                          ? "favor-receive"
                          : "even"
                    }`}
                  >
                    <div className="arrow">⇄</div>
                    <motion.div
                      key={valueDifference}
                      initial={{ opacity: 0, y: 5 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="diff"
                    >
                      {valueDifference > 0 ? `+${valueDifference}` : valueDifference}
                    </motion.div>
                  </div>
                  <div className="value-side receiving">
                    <div className="label">You Receive</div>
                    <motion.div
                      key={requestedValue}
                      initial={{ scale: 1.2, color: "#fff" }}
                      animate={{ scale: 1, color: "rgba(255,255,255,0.7)" }}
                      className="value"
                    >
                      {requestedValue}
                    </motion.div>
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
                  <motion.button
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="trade-btn primary"
                    onClick={handleExecuteTrade}
                    data-testid="execute-trade-btn"
                  >
                    Execute Trade
                  </motion.button>
                )}
              </div>

              {error && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="analyzer-error trade-error-centered"
                >
                  {error}
                </motion.div>
              )}

              {/* GM Response */}
              <AnimatePresence>
                {evaluation && (
                  <motion.div
                    key="evaluation"
                    initial={{ opacity: 0, y: 20, height: 0 }}
                    animate={{ opacity: 1, y: 0, height: "auto" }}
                    exit={{ opacity: 0, y: 20, height: 0 }}
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
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default TradeCenter;
