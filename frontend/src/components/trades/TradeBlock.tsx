/**
 * TradeBlock Component
 * Allows users to manage their trade block and view incoming offers
 */
import React, { useState, useEffect } from "react";
import type { TradeBlockPlayer, IncomingTradeOffer, TradePlayer } from "../../types/trade";
import { tradeApi } from "../../services/tradeApi";
import "./TradeBlock.css";

interface TradeBlockProps {
  seasonId: number;
  userTeamId: number;
}

export const TradeBlock: React.FC<TradeBlockProps> = ({ userTeamId }) => {
  // State
  const [tradeBlockPlayers, setTradeBlockPlayers] = useState<TradeBlockPlayer[]>([]);
  const [incomingOffers, setIncomingOffers] = useState<IncomingTradeOffer[]>([]);
  const [rosterPlayers, setRosterPlayers] = useState<TradePlayer[]>([]);
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(null);
  const [askingPrice, setAskingPrice] = useState<"high" | "medium" | "low">("medium");
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [processingOffer, setProcessingOffer] = useState<number | null>(null);

  // Fetch data
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [block, offers, roster] = await Promise.all([
          tradeApi.getTradeBlock(userTeamId),
          tradeApi.getIncomingOffers(userTeamId),
          tradeApi.getTradeablePlayers(userTeamId),
        ]);
        setTradeBlockPlayers(block);
        setIncomingOffers(offers);
        setRosterPlayers(roster);
      } catch (err) {
        console.error("Failed to load trade block data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [userTeamId]);

  // Add player to trade block
  const handleAddToBlock = async () => {
    if (!selectedPlayerId) return;

    try {
      const player = rosterPlayers.find((p) => p.id === selectedPlayerId);
      if (!player) return;

      const newBlockPlayer = await tradeApi.addToTradeBlock(selectedPlayerId, askingPrice);

      // Update local state with enriched data
      setTradeBlockPlayers([
        ...tradeBlockPlayers,
        {
          ...newBlockPlayer,
          player_name: `${player.first_name} ${player.last_name}`,
          position: player.position,
          overall: player.overall_rating,
          trade_value: player.trade_value,
        },
      ]);

      setShowAddModal(false);
      setSelectedPlayerId(null);
    } catch (err) {
      console.error("Failed to add player to trade block:", err);
    }
  };

  // Remove player from trade block
  const handleRemoveFromBlock = async (playerId: number) => {
    try {
      await tradeApi.removeFromTradeBlock(playerId);
      setTradeBlockPlayers(tradeBlockPlayers.filter((p) => p.player_id !== playerId));
    } catch (err) {
      console.error("Failed to remove player from trade block:", err);
    }
  };

  // Respond to offer
  const handleOfferResponse = async (
    offerId: number,
    response: "accept" | "reject" | "counter"
  ) => {
    setProcessingOffer(offerId);
    try {
      const result = await tradeApi.respondToOffer(offerId, response);

      if (result.success) {
        // Remove offer from list (in a real app, we'd update the status)
        setIncomingOffers(incomingOffers.filter((o) => o.id !== offerId));

        // If accepted, refresh the trade block as roster may have changed
        if (response === "accept") {
          const roster = await tradeApi.getTradeablePlayers(userTeamId);
          setRosterPlayers(roster);

          // Remove any traded players from the trade block
          const block = await tradeApi.getTradeBlock(userTeamId);
          setTradeBlockPlayers(block);
        }
      }
    } catch (err) {
      console.error("Failed to respond to offer:", err);
    } finally {
      setProcessingOffer(null);
    }
  };

  // Get asking price color
  const getAskingPriceClass = (price: "high" | "medium" | "low"): string => {
    switch (price) {
      case "high":
        return "price-high";
      case "medium":
        return "price-medium";
      case "low":
        return "price-low";
      default:
        return "";
    }
  };

  // Get overall rating class
  const getOverallClass = (overall: number): string => {
    if (overall >= 90) return "elite";
    if (overall >= 80) return "great";
    if (overall >= 70) return "good";
    if (overall >= 60) return "average";
    return "below";
  };

  // Get players not already on trade block
  const availableForBlock = rosterPlayers.filter(
    (p) => !tradeBlockPlayers.some((tb) => tb.player_id === p.id)
  );

  if (loading) {
    return (
      <div className="trade-block-container" data-testid="trade-block-loading">
        <div className="trade-loading">
          <div className="spinner"></div>
          <p>Loading Trade Block...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="trade-block-container" data-testid="trade-block-container">
      {/* Trade Block Section */}
      <section className="trade-block-section" data-testid="trade-block-section">
        <div className="section-header">
          <h3>
            <span className="icon">📋</span>
            Your Trade Block
          </h3>
          <button
            className="add-to-block-btn"
            onClick={() => setShowAddModal(true)}
            data-testid="add-to-block-btn"
          >
            + Add Player
          </button>
        </div>

        {tradeBlockPlayers.length === 0 ? (
          <div className="trade-block-empty">
            <span className="empty-icon">🏈</span>
            <p>No players on the trade block</p>
            <p className="hint">Add players to attract trade offers from other teams</p>
          </div>
        ) : (
          <div className="trade-block-grid">
            {tradeBlockPlayers.map((player) => (
              <div
                key={player.player_id}
                className="trade-block-card"
                data-testid={`trade-block-player-${player.player_id}`}
              >
                <div className="block-card-header">
                  <span className="position-badge">{player.position}</span>
                  <span className={`overall-badge ${getOverallClass(player.overall)}`}>
                    {player.overall}
                  </span>
                </div>
                <div className="block-card-body">
                  <h4>{player.player_name}</h4>
                  <div className="block-stats">
                    <div className="stat">
                      <span className="label">Trade Value</span>
                      <span className="value">{player.trade_value}</span>
                    </div>
                    <div className="stat">
                      <span className="label">Interest</span>
                      <span className="value">
                        {player.interest_level > 0 ? `${player.interest_level}%` : "Low"}
                      </span>
                    </div>
                  </div>
                  <div className={`asking-price ${getAskingPriceClass(player.asking_price)}`}>
                    Asking: {player.asking_price.toUpperCase()}
                  </div>
                </div>
                <div className="block-card-actions">
                  <button
                    className="block-action-btn remove"
                    onClick={() => handleRemoveFromBlock(player.player_id)}
                    aria-label="Remove from trade block"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Incoming Offers Section */}
      <section className="incoming-offers-section" data-testid="incoming-offers-section">
        <div className="section-header">
          <h3>
            <span className="icon">📨</span>
            Incoming Trade Offers
            {incomingOffers.length > 0 && (
              <span className="offer-count">{incomingOffers.length}</span>
            )}
          </h3>
        </div>

        {incomingOffers.length === 0 ? (
          <div className="offers-empty">
            <span className="empty-icon">📭</span>
            <p>No pending trade offers</p>
            <p className="hint">Adding players to your trade block may attract interest</p>
          </div>
        ) : (
          <div className="offers-list">
            {incomingOffers.map((offer) => (
              <div key={offer.id} className="offer-card" data-testid={`offer-${offer.id}`}>
                <div className="offer-header">
                  <div className="offer-from">
                    <span className="team-logo">🏈</span>
                    <span className="team-name">{offer.from_team_name}</span>
                  </div>
                  <span className={`urgency-badge ${offer.urgency}`}>
                    {offer.urgency === "high"
                      ? "⚡ Urgent"
                      : offer.urgency === "medium"
                        ? "📌 Standard"
                        : "🕐 Open"}
                  </span>
                </div>

                <div className="offer-details">
                  <div className="offer-column giving">
                    <h5>They Offer</h5>
                    <div className="offer-assets-list">
                      {offer.offered_assets.map((asset) => (
                        <div key={`${asset.type}-${asset.id}`} className="offer-asset-item">
                          {asset.type === "player" ? (
                            <>
                              <span className="pos">{asset.position}</span>
                              <span className="name">{asset.name}</span>
                              <span className={`ovr ${getOverallClass(asset.overall || 0)}`}>
                                {asset.overall}
                              </span>
                            </>
                          ) : (
                            <>
                              <span className="pick-icon">📜</span>
                              <span className="name">
                                Round {asset.round} Pick ({asset.year})
                              </span>
                            </>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="offer-arrow">⇄</div>

                  <div className="offer-column receiving">
                    <h5>They Want</h5>
                    <div className="offer-assets-list">
                      {offer.requested_assets.map((asset) => (
                        <div key={`${asset.type}-${asset.id}`} className="offer-asset-item">
                          {asset.type === "player" ? (
                            <>
                              <span className="pos">{asset.position}</span>
                              <span className="name">{asset.name}</span>
                              <span className={`ovr ${getOverallClass(asset.overall || 0)}`}>
                                {asset.overall}
                              </span>
                            </>
                          ) : (
                            <>
                              <span className="pick-icon">📜</span>
                              <span className="name">
                                Round {asset.round} Pick ({asset.year})
                              </span>
                            </>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {offer.gm_message && (
                  <div className="gm-message">
                    <span className="quote-icon">💬</span>
                    <p>"{offer.gm_message}"</p>
                  </div>
                )}

                <div className="offer-actions">
                  <button
                    className="offer-action-btn reject"
                    onClick={() => handleOfferResponse(offer.id, "reject")}
                    disabled={processingOffer === offer.id}
                  >
                    Decline
                  </button>
                  <button
                    className="offer-action-btn counter"
                    onClick={() => handleOfferResponse(offer.id, "counter")}
                    disabled={processingOffer === offer.id}
                  >
                    Counter
                  </button>
                  <button
                    className="offer-action-btn accept"
                    onClick={() => handleOfferResponse(offer.id, "accept")}
                    disabled={processingOffer === offer.id}
                  >
                    {processingOffer === offer.id ? "Processing..." : "Accept"}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Add to Trade Block Modal */}
      {showAddModal && (
        <div className="modal-overlay" data-testid="add-to-block-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Add Player to Trade Block</h3>
              <button
                className="modal-close"
                onClick={() => setShowAddModal(false)}
                aria-label="Close modal"
              >
                ✕
              </button>
            </div>

            <div className="modal-body">
              <div className="form-group">
                <label>Select Player</label>
                <select
                  value={selectedPlayerId || ""}
                  onChange={(e) => setSelectedPlayerId(Number(e.target.value) || null)}
                  data-testid="select-player-for-block"
                  aria-label="Select player to add to trade block"
                >
                  <option value="">Choose a player...</option>
                  {availableForBlock.map((player) => (
                    <option key={player.id} value={player.id}>
                      {player.position} - {player.first_name} {player.last_name} (
                      {player.overall_rating} OVR)
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Asking Price</label>
                <div className="price-options">
                  {(["high", "medium", "low"] as const).map((price) => (
                    <button
                      key={price}
                      className={`price-option ${askingPrice === price ? "selected" : ""} ${price}`}
                      onClick={() => setAskingPrice(price)}
                    >
                      {price.charAt(0).toUpperCase() + price.slice(1)}
                    </button>
                  ))}
                </div>
                <p className="price-hint">
                  {askingPrice === "high" && "Premium price - may limit interest"}
                  {askingPrice === "medium" && "Fair market value - balanced interest"}
                  {askingPrice === "low" && "Discount price - attracts more offers"}
                </p>
              </div>
            </div>

            <div className="modal-footer">
              <button className="modal-btn cancel" onClick={() => setShowAddModal(false)}>
                Cancel
              </button>
              <button
                className="modal-btn confirm"
                onClick={handleAddToBlock}
                disabled={!selectedPlayerId}
                data-testid="confirm-add-to-block"
              >
                Add to Trade Block
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TradeBlock;
