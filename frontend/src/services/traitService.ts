import type { Trait, PlayerTrait, TraitAssignment } from "../types/trait";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

class TraitService {
  async getAllTraits(): Promise<Trait[]> {
    const response = await fetch(`${API_BASE_URL}/api/traits/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch traits: ${response.statusText}`);
    }
    return response.json();
  }

  async getPlayerTraits(playerId: number): Promise<Trait[]> {
    // Endpoint returns List[Trait] currently (based on backend fix)
    // If it returns PlayerTrait in future, type needs adjustment
    const response = await fetch(`${API_BASE_URL}/api/traits/players/${playerId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch player traits: ${response.statusText}`);
    }
    return response.json();
  }

  async assignTrait(playerId: number, assignment: TraitAssignment): Promise<PlayerTrait> {
    const response = await fetch(`${API_BASE_URL}/api/traits/players/${playerId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(assignment),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Failed to assign trait: ${response.statusText}`);
    }
    return response.json();
  }
}

export const traitService = new TraitService();
