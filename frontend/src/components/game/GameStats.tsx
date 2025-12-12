import { useMemo } from "react";
import { useSimulationStore } from "../../store/useSimulationStore";
import type { PlayResult } from "../../types/simulation";

interface TeamStats {
  passYards: number;
  rushYards: number;
  totalYards: number;
  plays: number;
  passPlays: number;
  rushPlays: number;
  sacks: number;
  turnovers: number;
  touchdowns: number;
}

export const GameStats = () => {
  const { playLog } = useSimulationStore();

  const stats = useMemo(() => {
    // Initialize stats
    // Note: In a real implementation, we would need to know WHICH team performed the action.
    // The current PlayResult doesn't explicitly state "offenseTeamId".
    // However, we can infer possession from gameState, but playLog is historical.
    // For MVP, since we don't have team_id on PlayResult, we might have to aggregate TOTALS
    // or assume the current simplistic "Empire vs Genesis" single-game simulation flow
    // where we might not distinguish teams perfectly in the log without more data.
    //
    // WAIT: PlayResult has passer_id, rusher_id. We need to know which team those players belong to.
    // We don't have that map here easily.
    //
    // ALTERNATIVE: Just show "Game Totals" or try to split if possible.
    // actually, let's checking if we can infer it.
    // For now, let's display Aggregate Stats (Game Flow) or maybe just "Last Drive"?
    //
    // Actually, looking at the user's `playLog` in `useSimulationStore`, it is just a list.
    // If we can't split by team, maybe we just show "Offensive Production" (since it's a sim, maybe we assume 1 active game).
    // But there are two teams.
    //
    // Let's assume for this MVP task we will calculate TOTALS and display them.
    // OR better, we iterate and if the description contains "Empire" or "Genesis" we assign it?
    // That's brittle.
    //
    // Let's check `PlayResult` again... `passer_id`, `receiver_id`.
    // Maybe `engineData.homeTeam.roster` has IDs?
    // That's too complex for this frontend task without fetching roster.
    //
    // Simplification: display "Simulated Stats" as a single block for now,
    // or just break it down by Play Type (Pass vs Run) regardless of team.
    // This is still useful "Pass Yards: X, Run Yards: Y".

    // Actually, let's look at `gameState.possession`.
    // But `playLog` stores history. We don't know who had possession at index i.
    //
    // Let's build a "Game Summary" that shows total Passing/Rushing for the game.

    const acc: TeamStats = {
      passYards: 0,
      rushYards: 0,
      totalYards: 0,
      plays: 0,
      passPlays: 0,
      rushPlays: 0,
      sacks: 0,
      turnovers: 0,
      touchdowns: 0,
    };

    playLog.forEach((play: PlayResult) => {
      acc.plays += 1;

      const yards = play.yards_gained;

      if (play.passer_id !== undefined) {
        // Passing Play
        acc.passPlays += 1;
        if (!play.is_sack) {
          acc.passYards += yards;
        }
      } else if (play.rusher_id !== undefined) {
        // Rushing Play
        acc.rushPlays += 1;
        acc.rushYards += yards;
      }

      if (play.is_sack) acc.sacks += 1;
      if (play.is_turnover) acc.turnovers += 1;
      if (play.is_touchdown) acc.touchdowns += 1;
    });

    acc.totalYards = acc.passYards + acc.rushYards;

    return acc;
  }, [playLog]);

  return (
    <div className="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-6 h-full overflow-y-auto">
      <h2 className="text-xl font-bold text-white mb-6 border-b border-white/10 pb-2">
        Game Statistics
      </h2>

      <div className="grid grid-cols-2 gap-8">
        {/* Offensive Stats */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-cyan-400 uppercase tracking-wider">Offense</h3>

          <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
            <span className="text-gray-300">Total Yards</span>
            <span className="text-2xl font-bold text-white">{stats.totalYards}</span>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 bg-white/5 rounded-lg">
              <div className="text-xs text-gray-400 mb-1">Passing</div>
              <div className="text-xl font-bold text-white">{stats.passYards}</div>
              <div className="text-xs text-gray-500">{stats.passPlays} plays</div>
            </div>
            <div className="p-3 bg-white/5 rounded-lg">
              <div className="text-xs text-gray-400 mb-1">Rushing</div>
              <div className="text-xl font-bold text-white">{stats.rushYards}</div>
              <div className="text-xs text-gray-500">{stats.rushPlays} plays</div>
            </div>
          </div>

          <div className="flex justify-between items-center text-sm text-gray-400 px-2">
            <span>Avg / Play</span>
            <span className="text-white font-mono">
              {stats.plays > 0 ? (stats.totalYards / stats.plays).toFixed(1) : "0.0"}
            </span>
          </div>
        </div>

        {/* Events / Misc */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-cyan-400 uppercase tracking-wider">Events</h3>

          <div className="space-y-2">
            <StatRow label="Touchdowns" value={stats.touchdowns} />
            <StatRow label="Turnovers" value={stats.turnovers} />
            <StatRow label="Sacks" value={stats.sacks} />
            <StatRow label="First Downs" value="--" /> {/* Placeholder */}
          </div>
        </div>
      </div>

      <div className="mt-8 text-xs text-gray-500 text-center italic">
        * Stats reflect total game production (combined teams for MVP)
      </div>
    </div>
  );
};

const StatRow = ({ label, value }: { label: string; value: string | number }) => (
  <div className="flex justify-between items-center py-2 border-b border-white/5 last:border-0">
    <span className="text-gray-300">{label}</span>
    <span className="font-mono font-bold text-white">{value}</span>
  </div>
);
