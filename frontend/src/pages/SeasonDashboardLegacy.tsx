import { useEffect, useState } from "react";
import { api } from "../services/api";
import { seasonApi } from "../services/season";

type LegacySeason = {
  id: number;
  year: number;
  current_week: number;
};

type LegacyStanding = {
  team_id: number;
  team_name: string;
  wins: number;
  losses: number;
  ties: number;
};

type LegacyScheduleGame = {
  id: number;
  week: number;
  home_team_id: number;
  away_team_id: number;
  home_score: number | null;
  away_score: number | null;
  status: "COMPLETED" | "SCHEDULED" | string;
  home_team_name: string;
  away_team_name: string;
};

/**
 * Back-compat Season Dashboard used by older Playwright suites.
 * Does not replace the main /season experience.
 */
const SeasonDashboardLegacy = () => {
  const [season, setSeason] = useState<LegacySeason | null>(null);
  const [standings, setStandings] = useState<LegacyStanding[]>([]);
  const [schedule, setSchedule] = useState<LegacyScheduleGame[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const run = async () => {
      try {
        const s = (await seasonApi.getCurrentSeason()) as unknown as LegacySeason;
        setSeason(s);

        const [standingsRes, scheduleRes] = await Promise.all([
          api.get("/api/standings"),
          api.get(`/api/schedule?week=${s.current_week}`),
        ]);
        setStandings((standingsRes.data ?? []) as LegacyStanding[]);
        setSchedule((scheduleRes.data ?? []) as LegacyScheduleGame[]);
      } catch (e) {
        console.error("Legacy season dashboard failed to load", e);
      } finally {
        setLoading(false);
      }
    };
    run();
  }, []);

  if (loading) return <div className="season-dashboard">Loading...</div>;

  const title = season ? `${season.year} Season - Week ${season.current_week}` : "Season Dashboard";

  return (
    <div className="season-dashboard" data-testid="season-dashboard-page">
      <header data-testid="season-dashboard-header">
        <h1>{title}</h1>
      </header>

      <section data-testid="standings-table">
        <h2>Standings</h2>
        <div>
          {standings.map((row) => (
            <div key={row.team_id} data-testid={`standings-table-row-${row.team_name}`}>
              <span>{row.team_name}</span>
              <span>
                {row.wins}-{row.losses}-{row.ties}
              </span>
            </div>
          ))}
        </div>
      </section>

      <section data-testid="schedule-section">
        <h2>Schedule</h2>
        <div>
          {schedule.map((g) => {
            const matchup = `${g.home_team_name} vs ${g.away_team_name}`;
            const statusText =
              g.status === "COMPLETED"
                ? `Final: ${g.home_score ?? 0} - ${g.away_score ?? 0}`
                : "Upcoming";
            return (
              <div key={g.id} data-testid={`schedule-game-${g.id}`}>
                <div>{matchup}</div>
                <div>{statusText}</div>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
};

export default SeasonDashboardLegacy;
