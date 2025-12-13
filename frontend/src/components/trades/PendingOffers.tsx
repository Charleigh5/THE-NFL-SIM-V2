import React, { useState, useEffect } from "react";
import { tradeApi } from "../../services/tradeApi";
import type { TradeOffer } from "../../types/trade";
import "./PendingOffers.css";

interface PendingOffersProps {
  teamId: number;
  onCounter?: (offer: TradeOffer) => void;
}

export const PendingOffers: React.FC<PendingOffersProps> = ({ teamId, onCounter }) => {
  const [incomingOffers, setIncomingOffers] = useState<TradeOffer[]>([]);
  const [outgoingOffers, setOutgoingOffers] = useState<TradeOffer[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"incoming" | "outgoing">("incoming");

  useEffect(() => {
    const fetchOffers = async () => {
      setLoading(true);
      try {
        const { incoming, outgoing } = await tradeApi.getPendingOffers(teamId);
        setIncomingOffers(incoming);
        setOutgoingOffers(outgoing);
      } catch {
        // Silent error for now, mock data fallback handles it
      } finally {
        setLoading(false);
      }
    };

    fetchOffers();
  }, [teamId]);

  const handleAction = async (offerId: number, action: "accept" | "reject") => {
    try {
      await tradeApi.respondToOffer(offerId, action);
      // Remove from list
      setIncomingOffers((prev) => prev.filter((o) => o.id !== offerId));
    } catch {
      alert("Failed to process offer");
    }
  };

  const handleCounterOffer = (offer: TradeOffer) => {
    if (onCounter) {
      onCounter(offer);
    } else {
      console.warn("Counter action not handled");
    }
  };

  const OfferCard: React.FC<{ offer: TradeOffer; type: "incoming" | "outgoing" }> = ({
    offer,
    type,
  }) => (
    <div className="offer-card" data-testid={`offer-${offer.id}`}>
      <div className="offer-header">
        <span className="offer-id">Offer #{offer.id}</span>
        <span className={`offer-status ${offer.status.toLowerCase()}`}>{offer.status}</span>
        <span className="offer-date">{new Date(offer.created_at).toLocaleDateString()}</span>
      </div>

      <div className="offer-content">
        <div className="offer-side giving">
          <h4>{type === "incoming" ? "They Offer" : "You Offer"}</h4>
          {offer.offered_assets.map((asset) => (
            <div key={asset.id} className="asset-item">
              {asset.name}
            </div>
          ))}
        </div>
        <div className="offer-divider">⇄</div>
        <div className="offer-side receiving">
          <h4>{type === "incoming" ? "They Want" : "You Get"}</h4>
          {offer.requested_assets.map((asset) => (
            <div key={asset.id} className="asset-item">
              {asset.name}
            </div>
          ))}
        </div>
      </div>

      {offer.gm_response && <div className="gm-message">"{offer.gm_response}"</div>}

      <div className="offer-actions">
        {type === "incoming" && offer.status === "PENDING" && (
          <>
            <button className="btn-reject" onClick={() => handleAction(offer.id, "reject")}>
              Reject
            </button>
            <button className="btn-counter" onClick={() => handleCounterOffer(offer)}>
              Counter
            </button>
            <button className="btn-accept" onClick={() => handleAction(offer.id, "accept")}>
              Accept
            </button>
          </>
        )}
        {type === "outgoing" && offer.status === "PENDING" && (
          <button className="btn-withdraw">Withdraw</button>
        )}
      </div>
    </div>
  );

  return (
    <div className="pending-offers">
      <div className="offers-tabs">
        <button
          className={`tab ${activeTab === "incoming" ? "active" : ""}`}
          onClick={() => setActiveTab("incoming")}
        >
          Incoming Offers ({incomingOffers.length})
        </button>
        <button
          className={`tab ${activeTab === "outgoing" ? "active" : ""}`}
          onClick={() => setActiveTab("outgoing")}
        >
          Outgoing Offers ({outgoingOffers.length})
        </button>
      </div>

      <div className="offers-list">
        {loading ? (
          <div className="loading">Loading offers...</div>
        ) : activeTab === "incoming" ? (
          incomingOffers.length > 0 ? (
            incomingOffers.map((offer) => (
              <OfferCard key={offer.id} offer={offer} type="incoming" />
            ))
          ) : (
            <div className="empty-state">No incoming trade offers.</div>
          )
        ) : outgoingOffers.length > 0 ? (
          outgoingOffers.map((offer) => <OfferCard key={offer.id} offer={offer} type="outgoing" />)
        ) : (
          <div className="empty-state">No active outgoing offers.</div>
        )}
      </div>
    </div>
  );
};
