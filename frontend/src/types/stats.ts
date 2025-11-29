export interface PlayerLeader {
  player_id: number;
  name: string;
  team: string;
  position: string;
  value: number;
  stat_type: string;
}

export interface LeagueLeaders {
  passing_yards: PlayerLeader[];
  rushing_yards: PlayerLeader[];
  receiving_yards: PlayerLeader[];
}
