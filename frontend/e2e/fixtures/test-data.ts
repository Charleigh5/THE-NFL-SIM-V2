export const mockTeam = {
  id: 1,
  name: 'Cardinals',
  city: 'Arizona',
  abbreviation: 'ARI',
  conference: 'NFC',
  division: 'West',
  wins: 0,
  losses: 0,
  ties: 0,
};

export const mockPlayers = [
  { 
    id: 1, 
    first_name: 'Kyler', 
    last_name: 'Murray', 
    position: 'QB', 
    overall_rating: 85,
    age: 26,
    jersey_number: 1,
    speed: 90,
    strength: 70
  },
  { 
    id: 2, 
    first_name: 'James', 
    last_name: 'Conner', 
    position: 'RB', 
    overall_rating: 82,
    age: 28,
    jersey_number: 6,
    speed: 88,
    strength: 85
  },
];

export const mockSeason = {
  id: 1,
  year: 2024,
  currentWeek: 1,
  isPlayoffs: false,
};
