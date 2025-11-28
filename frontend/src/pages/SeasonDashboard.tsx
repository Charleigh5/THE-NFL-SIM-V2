import React, { useState, useEffect } from "react";
import { seasonApi } from "../services/season";
import { api } from "../services/api";
import type { Season, Game, TeamStanding } from "../types/season";
import type { Team } from "../services/api";
import type { PlayoffMatchup } from "../types/playoff";
import { StandingsTable } from "../components/season/StandingsTable";
import { ScheduleView } from "../components/season/ScheduleView";
import { PlayoffBracket } from "../components/season/PlayoffBracket";
import "./SeasonDashboard.css";

const SeasonDashboard: React.FC = () => {
  const [season, setSeason] = useState<Season | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [standings, setStandings] = useState<TeamStanding[]>([]);
  const [games, setGames] = useState<Game[]>([]);
  const [playoffBracket, setPlayoffBracket] = useState<PlayoffMatchup[]>([]);
  const [activeTab, setActiveTab] = useState<
    "standings" | "schedule" | "playoffs"
  >("standings");
  const [loading, setLoading] = useState<boolean>(true);
  const [simulating, setSimulating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Initial data fetch
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Fetch teams first as they are needed for other components
        const teamsData = await api.getTeams();
        setTeams(teamsData);

        // Try to get current season
        try {
          const currentSeason = await seasonApi.getCurrentSeason();
          setSeason(currentSeason);

          // Fetch standings and schedule for current season
          const [standingsData, scheduleData] = await Promise.all([
            seasonApi.getStandings(currentSeason.id),
            seasonApi.getSchedule(currentSeason.id, currentSeason.current_week),
          ]);

          setStandings(standingsData);
          setGames(scheduleData);

          // If in playoffs, fetch bracket
          if (currentSeason.status === "POST_SEASON") {
            const bracket = await seasonApi.getPlayoffBracket(currentSeason.id);
            setPlayoffBracket(bracket);
            setActiveTab("playoffs");
          }
        } catch {
          // No active season found, which is a valid state
          console.log("No active season found");
        }
      } catch (err) {
        setError("Failed to load season data");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Fetch schedule when week changes in ScheduleView
  const handleWeekChange = async (week: number) => {
    if (!season) return;
    try {
      const scheduleData = await seasonApi.getSchedule(season.id, week);
      setGames(scheduleData);
    } catch (err) {
      console.error("Failed to load schedule", err);
    }
  };

  const handleInitializeSeason = async () => {
    try {
      setLoading(true);
      const newSeason = await seasonApi.initSeason(new Date().getFullYear());
      setSeason(newSeason);

      // Refresh data
      const [standingsData, scheduleData] = await Promise.all([
        seasonApi.getStandings(newSeason.id),
        seasonApi.getSchedule(newSeason.id, 1),
      ]);

      setStandings(standingsData);
      setGames(scheduleData);
    } catch (err) {
      setError("Failed to initialize season");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateWeek = async () => {
    if (!season) return;

    try {
      setSimulating(true);

      if (season.status === "POST_SEASON") {
        // Simulate Playoff Round
        await seasonApi.simulateWeek(season.id, season.current_week);
        await seasonApi.advancePlayoffRound(season.id);

        // Refresh Bracket and Season (for week update)
        const updatedSeason = await seasonApi.getSeason(season.id);
        const bracket = await seasonApi.getPlayoffBracket(season.id);

        setSeason(updatedSeason);
        setPlayoffBracket(bracket);
      } else {
        // Regular Season Simulation
        await seasonApi.simulateWeek(season.id, season.current_week);

        // Advance to next week
        const updatedSeason = await seasonApi.advanceWeek(season.id);
        setSeason(updatedSeason);

        // Check if we just entered Playoffs
        if (
          updatedSeason.status === "POST_SEASON" &&
          season.status === "REGULAR_SEASON"
        ) {
          // Generate Playoffs
          const bracket = await seasonApi.generatePlayoffs(season.id);
          setPlayoffBracket(bracket);
          setActiveTab("playoffs");
        }

        // Refresh data
        const [standingsData, scheduleData] = await Promise.all([
          seasonApi.getStandings(season.id),
          seasonApi.getSchedule(season.id, updatedSeason.current_week),
        ]);

        setStandings(standingsData);
        setGames(scheduleData);
      }
    } catch (err) {
      setError("Failed to simulate week");
      console.error(err);
    } finally {
      setSimulating(false);
    }
  };

  if (loading && !season) {
    return (
      <div className="season-dashboard">
        <div className="loading-spinner">Loading season data...</div>
      </div>
    );
  }

  if (!season) {
    return (
      <div className="season-dashboard">
        <div className="no-season-state">
          <h2>No Active Season</h2>
          <p>
            Start a new franchise mode season to begin your journey to the Super
            Bowl.
          </p>
          <button className="action-button" onClick={handleInitializeSeason}>
            Initialize New Season
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="season-dashboard">
      {simulating && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <div className="loading-text">
            Simulating Week {season.current_week}...
          </div>
        </div>
      )}

      <div className="season-header">
        <div className="season-info">
          <h1>{season.year} Season</h1>
          <div className="season-status">
            <span className="status-badge">
              {season.status.replace("_", " ")}
            </span>
            <span>
              Week {season.current_week}{" "}
              {season.status === "REGULAR_SEASON"
                ? `of ${season.total_weeks}`
                : ""}
            </span>
          </div>
        </div>

        <div className="season-actions">
          <button
            className="action-button"
            onClick={handleSimulateWeek}
            disabled={simulating || season.status === "OFF_SEASON"}
          >
            {simulating ? "Simulating..." : "Simulate Week"}
          </button>
        </div>
      </div>

      <div className="dashboard-tabs">
        <button
          className={`tab-button ${activeTab === "standings" ? "active" : ""}`}
          onClick={() => setActiveTab("standings")}
        >
          Standings
        </button>
        <button
          className={`tab-button ${activeTab === "schedule" ? "active" : ""}`}
          onClick={() => setActiveTab("schedule")}
        >
          Schedule
        </button>
        {(season.status === "POST_SEASON" ||
          season.status === "OFF_SEASON") && (
          <button
            className={`tab-button ${activeTab === "playoffs" ? "active" : ""}`}
            onClick={() => setActiveTab("playoffs")}
          >
            Playoffs
          </button>
        )}
      </div>

      <div className="dashboard-content">
        {error && <div className="error-message">{error}</div>}

        {activeTab === "standings" && <StandingsTable standings={standings} />}

        {activeTab === "schedule" && (
          <ScheduleView
            games={games}
            teams={teams}
            currentWeek={season.current_week}
            totalWeeks={season.total_weeks + 4} // Approx playoff weeks
            onWeekChange={handleWeekChange}
          />
        )}

        {activeTab === "playoffs" && (
          <PlayoffBracket matchups={playoffBracket} />
        )}
      </div>
    </div>
  );
};

export default SeasonDashboard;
