/**
 * TradeCenterPage
 * Main page for all trade-related functionality
 */
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useSettingsStore } from "../store/useSettingsStore";
import { seasonApi } from "../services/season";
import { api } from "../services/api";
import { tradeApi } from "../services/tradeApi"; // Import tradeApi
import type { Season } from "../types/season";
import type { Team } from "../services/api";
import type { TradeOffer } from "../types/trade"; // Import TradeOffer
import { TradeNegotiator } from "../components/trades/TradeNegotiator"; // Use TradeNegotiator
import { TradeBlock } from "../components/trades/TradeBlock";
import { PendingOffers } from "../components/trades/PendingOffers";
import { LoadingSpinner } from "../components/ui/LoadingSpinner";
import "./TradeCenterPage.css";

type TradeTab = "negotiate" | "offers" | "trade-block"; // Added offers tab

const TradeCenterPage: React.FC = () => {
  const [season, setSeason] = useState<Season | null>(null);
  const [team, setTeam] = useState<Team | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<TradeTab>("negotiate");
  const [pendingOffersCount, setPendingOffersCount] = useState(0); // State for badge
  const [counterOffer, setCounterOffer] = useState<TradeOffer | null>(null); // State for counter offer
  const [settingsAttempted, setSettingsAttempted] = useState(false);

  const { userTeamId, fetchSettings, isLoading: settingsLoading } = useSettingsStore();
  const navigate = useNavigate();

  // Fetch settings on mount
  useEffect(() => {
    (async () => {
      try {
        await fetchSettings();
      } finally {
        setSettingsAttempted(true);
      }
    })();
  }, [fetchSettings]);

  // Redirect if no team selected
  useEffect(() => {
    // Avoid redirecting on first paint before settings fetch flips loading.
    if (settingsAttempted && !settingsLoading && userTeamId === null) {
      navigate("/team-selection");
    }
  }, [settingsAttempted, settingsLoading, userTeamId, navigate]);

  const effectiveTeamId = Number(localStorage.getItem("selectedTeamId")) || userTeamId || 1;

  // Fetch season and team data
  useEffect(() => {
    const fetchData = async () => {
      if (!effectiveTeamId) return;

      setLoading(true);
      try {
        const [currentSeason, teamData] = await Promise.all([
          seasonApi.getCurrentSeason(),
          api.getTeam(effectiveTeamId),
        ]);
        setSeason(currentSeason);
        setTeam(teamData);
      } catch (err) {
        console.error("Failed to load trade center data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [effectiveTeamId]);

  // Fetch pending offers count for badge
  useEffect(() => {
    const fetchOffersCount = async () => {
      if (!effectiveTeamId) return;
      try {
        const { incoming } = await tradeApi.getPendingOffers(effectiveTeamId);
        setPendingOffersCount(incoming ? incoming.length : 0);
      } catch (err) {
        console.error("Failed to fetch pending offers count:", err);
      }
    };

    if (effectiveTeamId) {
      fetchOffersCount();
      // Poll every 30 seconds for updates
      const interval = setInterval(fetchOffersCount, 30000);
      return () => clearInterval(interval);
    }
  }, [effectiveTeamId]);

  // Handle counter offer action from PendingOffers
  const handleCounter = (offer: TradeOffer) => {
    setCounterOffer(offer);
    setActiveTab("negotiate");
  };

  if (loading || settingsLoading) {
    return (
      <div className="trade-center-page" data-testid="trade-center-page-loading">
        <div className="trade-center-loading">
          <LoadingSpinner text="Loading Trade Center..." size="large" />
        </div>
      </div>
    );
  }

  if (!season || !team) {
    return (
      <div className="trade-center-page" data-testid="trade-center-page-error">
        <div className="trade-center-error">
          <h2>Unable to Load Trade Center</h2>
          <p>Please ensure you have selected a team and an active season exists.</p>
          <button onClick={() => navigate("/team-selection")}>Select Team</button>
        </div>
      </div>
    );
  }

  const rawCap =
    typeof team.salary_cap_space === "number" && !isNaN(team.salary_cap_space)
      ? team.salary_cap_space
      : 25000000;
  const capSpaceM = (rawCap > 10000 ? rawCap / 1000000 : rawCap).toFixed(1);

  return (
    <div className="trade-center-page" data-testid="trade-center-page">
      {/* Page Header */}
      <header className="trade-page-header">
        <div className="header-content">
          <div className="header-title">
            <h1>Trade Center</h1>
            <p className="subtitle">
              {team.city} {team.name} • {season.year} Season
            </p>
          </div>
          <div className="header-stats">
            <div className="stat">
              <span className="stat-label">Cap Space</span>
              <span className="stat-value cap-space">${capSpaceM}M</span>
            </div>
            <div className="stat">
              <span className="stat-label">Record</span>
              <span className="stat-value">
                {team.wins}-{team.losses}
              </span>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        {/* Tab Navigation */}
        <nav className="trade-tabs" role="tablist" aria-label="Trade Center Tabs">
          <button
            className={`tab-btn ${activeTab === "negotiate" ? "active" : ""}`}
            onClick={() => setActiveTab("negotiate")}
            data-testid="tab-negotiate"
            role="tab"
            aria-selected={activeTab === "negotiate"}
            aria-controls="trade-tabpanel-negotiate"
          >
            <span className="tab-icon">🔄</span>
            <span className="tab-label">Negotiate</span>
          </button>

          <button
            className={`tab-btn ${activeTab === "offers" ? "active" : ""}`}
            onClick={() => setActiveTab("offers")}
            data-testid="tab-offers"
            role="tab"
            aria-selected={activeTab === "offers"}
            aria-controls="trade-tabpanel-offers"
          >
            <span className="tab-icon">📫</span>
            <span className="tab-label">Offers</span>
            {pendingOffersCount > 0 && (
              <span className="notification-badge">{pendingOffersCount}</span>
            )}
          </button>

          <button
            className={`tab-btn ${activeTab === "trade-block" ? "active" : ""}`}
            onClick={() => setActiveTab("trade-block")}
            data-testid="tab-trade-block"
            role="tab"
            aria-selected={activeTab === "trade-block"}
            aria-controls="trade-tabpanel-trade-block"
          >
            <span className="tab-icon">📋</span>
            <span className="tab-label">Trade Block</span>
          </button>
        </nav>
      </header>

      {/* Tab Content */}
      <main className="trade-content">
        {activeTab === "negotiate" && (
          <section id="trade-tabpanel-negotiate" role="tabpanel" aria-label="Negotiate">
            <TradeNegotiator
              seasonId={season.id}
              userTeamId={effectiveTeamId}
              initialOffer={counterOffer}
            />
          </section>
        )}
        {activeTab === "offers" && (
          <section id="trade-tabpanel-offers" role="tabpanel" aria-label="Offers">
            <PendingOffers teamId={effectiveTeamId} onCounter={handleCounter} />
          </section>
        )}
        {activeTab === "trade-block" && (
          <section id="trade-tabpanel-trade-block" role="tabpanel" aria-label="Trade Block">
            <TradeBlock seasonId={season.id} userTeamId={effectiveTeamId} />
          </section>
        )}
      </main>
    </div>
  );
};

export default TradeCenterPage;
