/**
 * TradeCenterPage
 * Main page for all trade-related functionality
 */
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useSettingsStore } from "../store/useSettingsStore";
import { seasonApi } from "../services/season";
import { api } from "../services/api";
import type { Season } from "../types/season";
import type { Team } from "../services/api";
import { TradeCenter } from "../components/trades/TradeCenter";
import { TradeBlock } from "../components/trades/TradeBlock";
import { LoadingSpinner } from "../components/ui/LoadingSpinner";
import "./TradeCenterPage.css";

type TradeTab = "negotiate" | "trade-block";

const TradeCenterPage: React.FC = () => {
  const [season, setSeason] = useState<Season | null>(null);
  const [team, setTeam] = useState<Team | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<TradeTab>("negotiate");

  const { userTeamId, fetchSettings, isLoading: settingsLoading } = useSettingsStore();
  const navigate = useNavigate();

  // Fetch settings on mount
  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  // Redirect if no team selected
  useEffect(() => {
    if (!settingsLoading && userTeamId === null) {
      navigate("/team-selection");
    }
  }, [settingsLoading, userTeamId, navigate]);

  // Fetch season and team data
  useEffect(() => {
    const fetchData = async () => {
      if (!userTeamId) return;

      setLoading(true);
      try {
        const [currentSeason, teamData] = await Promise.all([
          seasonApi.getCurrentSeason(),
          api.getTeam(userTeamId),
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
  }, [userTeamId]);

  if (loading || settingsLoading) {
    return (
      <div className="trade-center-page" data-testid="trade-center-page-loading">
        <div className="trade-center-loading">
          <LoadingSpinner text="Loading Trade Center..." size="large" />
        </div>
      </div>
    );
  }

  if (!season || !team || !userTeamId) {
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
              <span className="stat-value cap-space">
                ${(team.salary_cap_space / 1000000).toFixed(1)}M
              </span>
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
        <nav className="trade-tabs">
          <button
            className={`tab-btn ${activeTab === "negotiate" ? "active" : ""}`}
            onClick={() => setActiveTab("negotiate")}
            data-testid="tab-negotiate"
          >
            <span className="tab-icon">🔄</span>
            <span className="tab-label">Negotiate Trade</span>
          </button>
          <button
            className={`tab-btn ${activeTab === "trade-block" ? "active" : ""}`}
            onClick={() => setActiveTab("trade-block")}
            data-testid="tab-trade-block"
          >
            <span className="tab-icon">📋</span>
            <span className="tab-label">Trade Block & Offers</span>
          </button>
        </nav>
      </header>

      {/* Tab Content */}
      <main className="trade-content">
        {activeTab === "negotiate" && (
          <TradeCenter seasonId={season.id} userTeamId={userTeamId} userTeam={team} />
        )}
        {activeTab === "trade-block" && <TradeBlock seasonId={season.id} userTeamId={userTeamId} />}
      </main>
    </div>
  );
};

export default TradeCenterPage;
