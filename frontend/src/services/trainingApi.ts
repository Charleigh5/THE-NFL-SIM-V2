import {
  Drill,
  DrillCategory,
  SeasonPhase,
  TrainingResult,
  WeeklySchedule,
  CoachingStyle,
  DrillListResponse,
} from "../types/training";
import axios from "axios";

// Base API URL
const API_URL = "http://localhost:8000/api/training";

class TrainingApiService {
  /**
   * Fetch available drills with optional filtering.
   */
  async getDrills(params?: {
    position?: string;
    season?: SeasonPhase;
    category?: DrillCategory;
  }): Promise<DrillListResponse> {
    const response = await axios.get(`${API_URL}/drills`, { params });
    return response.data;
  }

  /**
   * Execute a training session for a player.
   */
  async executeTraining(
    playerId: number,
    drillName: string,
    coachingStyle?: string,
    seasonPhase: string = "regular",
    playerAge: number = 25
  ): Promise<TrainingResult> {
    const response = await axios.post(`${API_URL}/execute`, {
      player_id: playerId,
      drill_name: drillName,
      coaching_style: coachingStyle,
      season_phase: seasonPhase,
      player_age: playerAge,
    });
    return response.data;
  }

  /**
   * Get a recommended weekly schedule.
   */
  async getSchedule(
    position: string,
    seasonPhase: string = "regular",
    coachingStyle: string = "smart"
  ): Promise<WeeklySchedule> {
    const response = await axios.get(`${API_URL}/schedule`, {
      params: {
        position,
        season_phase: seasonPhase,
        coaching_style: coachingStyle,
      },
    });
    return response.data;
  }

  /**
   * Fetch available coaching styles.
   */
  async getCoachingStyles(): Promise<CoachingStyle[]> {
    const response = await axios.get(`${API_URL}/styles`);
    return response.data;
  }
}

export const trainingApi = new TrainingApiService();
