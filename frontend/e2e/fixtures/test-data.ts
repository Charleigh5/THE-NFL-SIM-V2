import { Team, Player } from '../../src/services/api';
import { Season } from '../../src/types/season';

export const mockTeam: Team = {
  id: 1,
  city: 'Arizona',
  name: 'Cardinals',
  abbreviation: 'ARI',
  conference: 'NFC',
  division: 'West',
  wins: 0,
  losses: 0,
  salary_cap_space: 12400000,
  logo_url: '/assets/teams/ari.png',
  primary_color: '#97233F',
  secondary_color: '#000000'
};

export const mockPlayers: Player[] = [
  {
    id: 1,
    first_name: 'Kyler',
    last_name: 'Murray',
    position: 'QB',
    jersey_number: 1,
    overall_rating: 85,
    age: 26,
    experience: 5,
    team_id: 1,
    height: 70,
    weight: 207,
    speed: 91,
    strength: 60,
    agility: 92,
    acceleration: 93,
    awareness: 85
  },
  {
    id: 2,
    first_name: 'James',
    last_name: 'Conner',
    position: 'RB',
    jersey_number: 6,
    overall_rating: 82,
    age: 28,
    experience: 7,
    team_id: 1,
    height: 73,
    weight: 233,
    speed: 86,
    strength: 84,
    agility: 82,
    acceleration: 85,
    awareness: 88
  }
];

export const mockSeason: Season = {
  id: 1,
  year: 2024,
  current_week: 1,
  is_active: true,
  status: "REGULAR_SEASON",
  total_weeks: 18,
  playoff_weeks: 4,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString()
};
