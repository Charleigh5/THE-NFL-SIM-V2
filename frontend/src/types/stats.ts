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
  passing_tds: PlayerLeader[];
  rushing_yards: PlayerLeader[];
  rushing_tds: PlayerLeader[];
  receiving_yards: PlayerLeader[];
  receiving_tds: PlayerLeader[];
}
