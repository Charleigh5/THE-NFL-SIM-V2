import React, { useState, useEffect, useMemo } from "react";
import { seasonApi } from "../services/season";
import { api } from "../services/api";
import type { Season, Game, TeamStanding, SeasonAwards } from "../types/season";
import type { Team } from "../services/api";
import type { PlayoffMatchup } from "../types/playoff";
import { StandingsTable } from "../components/season/StandingsTable";
import { ScheduleView } from "../components/season/ScheduleView";
import { PlayoffBracket } from "../components/season/PlayoffBracket";
import { LoadingSpinner } from "../components/ui/LoadingSpinner";
import { LeagueLeaders } from "../components/season/LeagueLeaders";
import { SeasonSummaryCard } from "../components/season/SeasonSummaryCard";
import { NewsFeed } from "../components/season/NewsFeed";
import type { LeagueLeaders as LeagueLeadersType } from "../types/stats";
import "./SeasonDashboard.css";

const SeasonDashboard: React.FC = () => {
  const [season, setSeason] = useState<Season | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [standings, setStandings] = useState<TeamStanding[]>([]);
  const [games, setGames] = useState<Game[]>([]);
  const [playoffBracket, setPlayoffBracket] = useState<PlayoffMatchup[]>([]);
  const [leaders, setLeaders] = useState<LeagueLeadersType | null>(null);
  const [seasonProgress, setSeasonProgress] = useState<number>(0);
  const [awards, setAwards] = useState<SeasonAwards | null>(null);
  const [activeTab, setActiveTab] = useState<
    "overview" | "standings" | "schedule" | "playoffs" | "leaders"
  >("overview");
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

        // Try to get current season summary
        try {
          const summary = await seasonApi.getSeasonSummary();
          setSeason(summary.season);
          setSeasonProgress(summary.completion_percentage);

          // Fetch standings, schedule, leaders, and awards for current season
          const [standingsData, scheduleData, leadersData, awardsData] = await Promise.all([
            seasonApi.getStandings(summary.season.id),
            seasonApi.getSchedule(summary.season.id, summary.season.current_week),
            seasonApi.getLeagueLeaders(summary.season.id),
            seasonApi.getProjectedAwards(summary.season.id),
          ]);

          setStandings(standingsData);
          setGames(scheduleData);
          setLeaders(leadersData);
          setAwards(awardsData);

          // If in playoffs or off-season, fetch bracket
          if (summary.season.status === "POST_SEASON" || summary.season.status === "OFF_SEASON") {
            const bracket = await seasonApi.getPlayoffBracket(summary.season.id);
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
      const [standingsData, scheduleData, leadersData, awardsData] = await Promise.all([
        seasonApi.getStandings(newSeason.id),
        seasonApi.getSchedule(newSeason.id, 1),
        seasonApi.getLeagueLeaders(newSeason.id),
        seasonApi.getProjectedAwards(newSeason.id),
      ]);

      setStandings(standingsData);
      setGames(scheduleData);
      setLeaders(leadersData);
      setAwards(awardsData);
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
        if (updatedSeason.status === "POST_SEASON" && season.status === "REGULAR_SEASON") {
          // Generate Playoffs
          const bracket = await seasonApi.generatePlayoffs(season.id);
          setPlayoffBracket(bracket);
          setActiveTab("playoffs");
        }

        // Refresh data
        const [standingsData, scheduleData, leadersData, awardsData] = await Promise.all([
          seasonApi.getStandings(season.id),
          seasonApi.getSchedule(season.id, updatedSeason.current_week),
          seasonApi.getLeagueLeaders(season.id),
          seasonApi.getProjectedAwards(season.id),
        ]);

        setStandings(standingsData);
        setGames(scheduleData);
        setLeaders(leadersData);
        setAwards(awardsData);
      }
    } catch (err) {
      setError("Failed to simulate week");
      console.error(err);
    } finally {
      setSimulating(false);
    }
  };

  const handleSimulateToPlayoffs = async () => {
    if (!season) return;
    try {
      setSimulating(true);
      const result = await seasonApi.simulateToPlayoffs(season.id);
      setSeason(result.season);

      if (result.season.status === "POST_SEASON") {
        const bracket = await seasonApi.getPlayoffBracket(season.id);
        setPlayoffBracket(bracket);
        setActiveTab("playoffs");
      }

      // Refresh data
      const [standingsData, scheduleData, leadersData, awardsData] = await Promise.all([
        seasonApi.getStandings(season.id),
        seasonApi.getSchedule(season.id, result.season.current_week),
        seasonApi.getLeagueLeaders(season.id),
        seasonApi.getProjectedAwards(season.id),
      ]);

      setStandings(standingsData);
      setGames(scheduleData);
      setLeaders(leadersData);
      setAwards(awardsData);
    } catch (err) {
      setError("Failed to simulate to playoffs");
      console.error(err);
    } finally {
      setSimulating(false);
    }
  };

  // Calculate champion name using useMemo (must be before any early returns)
  const championName = useMemo(() => {
    if (season?.status === "OFF_SEASON" && playoffBracket.length > 0) {
      const superBowl = playoffBracket.find((m) => m.round === "SUPER_BOWL");
      return superBowl?.winner?.name;
    }
    return undefined;
  }, [season, playoffBracket]);

  const handleSimulateGame = async (gameId: number) => {
    if (!season) return;
    try {
      setSimulating(true);
      await seasonApi.simulateGame(gameId);

      // Refresh schedule (use current view week if possible, but for now refresh current week or just refresh games)
      // Note: ScheduleView manages its own selectedWeek, but we update 'games' state.
      // Ideally we should know which week is being viewed.
      // But 'games' state is what ScheduleView renders.
      // So we just need to re-fetch the games that are currently in 'games' state.
      // Wait, 'games' state might be for a different week if user navigated.
      // We should probably track 'viewingWeek' in SeasonDashboard if we want to be precise.
      // For now, let's assume we refresh the week that the game belongs to.
      // But we don't know the week easily without looking at the game object.
      // Let's just re-fetch the schedule for the week of the game.
      // Actually, 'games' state holds the games for the currently viewed week.
      // So we can just re-fetch for that week.
      // But we don't have 'viewingWeek' state here, only 'season.current_week' and 'games'.
      // However, ScheduleView calls 'handleWeekChange' which updates 'games'.
      // So 'games' corresponds to the week the user is looking at.
      // We can get the week from the first game in 'games'.
      const viewingWeek = games.length > 0 ? games[0].week : season.current_week;

      const scheduleData = await seasonApi.getSchedule(season.id, viewingWeek);
      setGames(scheduleData);

      // Refresh standings and leaders
      const [standingsData, leadersData, awardsData] = await Promise.all([
        seasonApi.getStandings(season.id),
        seasonApi.getLeagueLeaders(season.id),
        seasonApi.getProjectedAwards(season.id),
      ]);
      setStandings(standingsData);
      setLeaders(leadersData);
      setAwards(awardsData);
    } catch (err) {
      setError("Failed to simulate game");
      console.error(err);
    } finally {
      setSimulating(false);
    }
  };

  if (loading && !season) {
    return (
      <div className="season-dashboard" data-testid="loading-season-data">
        <LoadingSpinner text="Loading season data..." size="large" />
      </div>
    );
  }

  if (!season) {
    return (
      <div className="season-dashboard" data-testid="season-dashboard-page">
        <div className="no-season-state" data-testid="no-season-state">
          <h2>No Active Season</h2>
          <p>Start a new franchise mode season to begin your journey to the Super Bowl.</p>
          <button
            className="action-button"
            onClick={handleInitializeSeason}
            data-testid="initialize-season-button"
          >
            Initialize New Season
          </button>
        </div>
      </div>
    );
  }

  const actions = [
    {
      id: "simulate",
      label: simulating ? "Simulating..." : "Simulate Week",
      icon: "⚡",
      onClick: handleSimulateWeek,
      disabled: simulating || season.status === "OFF_SEASON",
      tooltip: "Simulate all games for the current week",
    },
    {
      id: "sim-playoffs",
      label: "Sim to Playoffs",
      icon: "⏩",
      onClick: handleSimulateToPlayoffs,
      disabled: simulating || season.status !== "REGULAR_SEASON",
      tooltip: "Simulate remaining regular season games",
    },
    {
      id: "playoffs",
      label: "View Playoffs",
      icon: "🏆",
      onClick: () => setActiveTab("playoffs"),
      disabled: season.status !== "POST_SEASON" && season.status !== "OFF_SEASON",
      tooltip: "View playoff bracket",
    },
  ];

  return (
    <div className="season-dashboard" data-testid="season-dashboard-page">
      {simulating && (
        <div className="loading-overlay">
          <LoadingSpinner text={`Simulating...`} size="large" color="white" />
        </div>
      )}

      <div className="dashboard-header" data-testid="dashboard-header">
        <SeasonSummaryCard
          season={season}
          progress={seasonProgress}
          actions={actions}
          champion={championName}
        />
        <LeagueLeaders leaders={leaders} loading={loading} teams={teams} />
      </div>

      <div className="dashboard-tabs" data-testid="dashboard-tabs">
        <button
          className={`tab-button ${activeTab === "overview" ? "active" : ""}`}
          onClick={() => setActiveTab("overview")}
          title="Season Overview"
          data-testid="tab-overview"
        >
          Overview
        </button>
        <button
          className={`tab-button ${activeTab === "standings" ? "active" : ""}`}
          onClick={() => setActiveTab("standings")}
          title="View current season standings"
          data-testid="tab-standings"
        >
          Standings
        </button>
        <button
          className={`tab-button ${activeTab === "schedule" ? "active" : ""}`}
          onClick={() => setActiveTab("schedule")}
          title="View season schedule and results"
          data-testid="tab-schedule"
        >
          Schedule
        </button>
        {(season.status === "POST_SEASON" || season.status === "OFF_SEASON") && (
          <button
            className={`tab-button ${activeTab === "playoffs" ? "active" : ""}`}
            onClick={() => setActiveTab("playoffs")}
            title="View playoff bracket"
            data-testid="tab-playoffs"
          >
            Playoffs
          </button>
        )}
        <button
          className={`tab-button ${activeTab === "leaders" ? "active" : ""}`}
          onClick={() => setActiveTab("leaders")}
          title="View league statistical leaders"
          data-testid="tab-leaders"
        >
          Leaders
        </button>
      </div>

      <div className="dashboard-content" data-testid="dashboard-content">
        {error && <div className="error-message">{error}</div>}

        {activeTab === "overview" && (
          <div className="overview-grid" data-testid="overview-grid">
            <div className="overview-section" data-testid="upcoming-games-section">
              <h3>Upcoming Games (Week {season.current_week})</h3>
              <div className="games-list-compact">
                {games
                  .filter((g) => !g.is_played)
                  .slice(0, 5)
                  .map((game) => (
                    <div
                      key={game.id}
                      className="game-card-compact"
                      data-testid={`upcoming-game-${game.id}`}
                    >
                      <div className="game-info-row">
                        <div className="team-row">
                          <span className="team-name">{game.away_team?.name}</span>
                          <span className="team-record">vs</span>
                          <span className="team-name">{game.home_team?.name}</span>
                        </div>
                        <div className="game-date">
                          {new Date(game.scheduled_date).toLocaleDateString()}
                        </div>
                      </div>
                      {game.weather_info && (
                        <div className="game-weather-compact">
                          <span
                            title={`${game.weather_info.temperature}°F, ${game.weather_info.precipitation_type || "Clear"}`}
                          >
                            {Math.round(game.weather_info.temperature)}°{" "}
                            {game.weather_info.precipitation_type?.includes("Rain")
                              ? "🌧️"
                              : game.weather_info.precipitation_type?.includes("Snow")
                                ? "❄️"
                                : game.weather_info.precipitation_type?.includes("Cloud")
                                  ? "☁️"
                                  : "☀️"}
                          </span>
                        </div>
                      )}
                    </div>
                  ))}
                {games.filter((g) => !g.is_played).length === 0 && (
                  <p>No upcoming games this week.</p>
                )}
              </div>
            </div>

            <div className="overview-section" data-testid="recent-results-section">
              <h3>Recent Results</h3>
              <div className="games-list-compact">
                {games
                  .filter((g) => g.is_played)
                  .slice(0, 5)
                  .map((game) => (
                    <div
                      key={game.id}
                      className="game-card-compact"
                      data-testid={`recent-game-${game.id}`}
                    >
                      <div className="game-info-row">
                        <div className="team-row">
                          <span className="team-name">{game.away_team?.name}</span>
                          <span className="score">{game.away_score}</span>
                        </div>
                        <span className="vs">@</span>
                        <div className="team-row">
                          <span className="score">{game.home_score}</span>
                          <span className="team-name">{game.home_team?.name}</span>
                        </div>
                      </div>
                      {game.weather_info && (
                        <div className="game-weather-compact">
                          <span
                            title={`${game.weather_info.temperature}°F, ${game.weather_info.precipitation_type || "Clear"}`}
                          >
                            {Math.round(game.weather_info.temperature)}°{" "}
                            {game.weather_info.precipitation_type?.includes("Rain")
                              ? "🌧️"
                              : game.weather_info.precipitation_type?.includes("Snow")
                                ? "❄️"
                                : game.weather_info.precipitation_type?.includes("Cloud")
                                  ? "☁️"
                                  : "☀️"}
                          </span>
                        </div>
                      )}
                    </div>
                  ))}
                {games.filter((g) => g.is_played).length === 0 && (
                  <p>No games played this week yet.</p>
                )}
              </div>
            </div>

            <div className="overview-section" data-testid="standings-overview-section">
              <h3>Standings Overview</h3>
              <StandingsTable standings={standings} compact={true} />
            </div>

            <div className="overview-section" data-testid="awards-race-section">
              <h3>Season Awards Race</h3>
              {awards ? (
                <div className="awards-race">
                  <div className="award-item">
                    <h4>MVP</h4>
                    {awards.mvp[0] ? (
                      <div className="award-leader">
                        <p className="leader-name">{awards.mvp[0].name}</p>
                        <p className="leader-team">
                          {awards.mvp[0].team} • {awards.mvp[0].position}
                        </p>
                        <p className="leader-stats">Score: {awards.mvp[0].score.toFixed(1)}</p>
                      </div>
                    ) : (
                      <p>No candidates</p>
                    )}
                  </div>
                  <div className="award-item">
                    <h4>OPOY</h4>
                    {awards.opoy[0] ? (
                      <div className="award-leader">
                        <p className="leader-name">{awards.opoy[0].name}</p>
                        <p className="leader-team">
                          {awards.opoy[0].team} • {awards.opoy[0].position}
                        </p>
                      </div>
                    ) : (
                      <p>No candidates</p>
                    )}
                  </div>
                  <div className="award-item">
                    <h4>DPOY</h4>
                    {awards.dpoy[0] ? (
                      <div className="award-leader">
                        <p className="leader-name">{awards.dpoy[0].name}</p>
                        <p className="leader-team">
                          {awards.dpoy[0].team} • {awards.dpoy[0].position}
                        </p>
                      </div>
                    ) : (
                      <p>No candidates</p>
                    )}
                  </div>
                </div>
              ) : (
                <LoadingSpinner />
              )}
            </div>

            <div className="overview-section" data-testid="news-feed-section">
              <h3>League News</h3>
              <NewsFeed maxItems={5} compact={false} refreshInterval={60} />
            </div>
          </div>
        )}

        {activeTab === "standings" && <StandingsTable standings={standings} />}

        {activeTab === "schedule" && (
          <ScheduleView
            games={games}
            teams={teams}
            currentWeek={season.current_week}
            totalWeeks={season.total_weeks + 4} // Approx playoff weeks
            onWeekChange={handleWeekChange}
            onSimulateGame={handleSimulateGame}
          />
        )}

        {activeTab === "playoffs" && <PlayoffBracket matchups={playoffBracket} />}

        {activeTab === "leaders" && (
          <LeagueLeaders leaders={leaders} loading={loading} teams={teams} />
        )}
      </div>
    </div>
  );
};

export default SeasonDashboard;
