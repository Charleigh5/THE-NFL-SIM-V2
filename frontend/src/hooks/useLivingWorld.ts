/**
 * Custom hook for fetching Living World news data.
 *
 * Following React best practices:
 * - Encapsulates fetch logic in reusable hook
 * - Uses useCallback for stable function references
 * - Handles loading, error, and data states
 */
import { useState, useEffect, useCallback } from "react";

const API_BASE = "/api/news";

// Types
export interface LivingNewsItem {
  id: number;
  season_id: number;
  week: number;
  team_id?: number;
  player_id?: number;
  category: string;
  headline: string;
  content: string;
  image_url?: string;
  importance_score: number;
  created_at: string;
}

export interface LivingNewsFeedResponse {
  items: LivingNewsItem[];
  total_count: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

export interface WeeklyRecap {
  id: number;
  season_id: number;
  week: number;
  summary_text: string;
  mvp_player_id?: number;
  play_of_the_week_id?: string;
  surprising_result?: string;
  media_assets?: string[];
  created_at: string;
}

export interface Storyline {
  type: string;
  team_id?: number;
  player_id?: number;
  start_week: number;
  intensity: number;
  event_count: number;
}

// Hook for fetching Living World news
export function useLivingNews(seasonId: number, week?: number, page = 1, pageSize = 20) {
  const [data, setData] = useState<LivingNewsFeedResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchNews = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        season_id: seasonId.toString(),
        page: page.toString(),
        page_size: pageSize.toString(),
      });

      if (week) {
        params.append("week", week.toString());
      }

      const response = await fetch(`${API_BASE}/living/feed?${params}`);

      if (!response.ok) {
        throw new Error(`Failed to fetch news: ${response.statusText}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [seasonId, week, page, pageSize]);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  return { data, loading, error, refetch: fetchNews };
}

// Hook for fetching weekly recap
export function useWeeklyRecap(seasonId: number, week: number) {
  const [data, setData] = useState<WeeklyRecap | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRecap = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/living/recap/${seasonId}/${week}`);

      if (response.status === 404) {
        setData(null);
        return;
      }

      if (!response.ok) {
        throw new Error(`Failed to fetch recap: ${response.statusText}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [seasonId, week]);

  const generateRecap = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/living/recap/${seasonId}/${week}/generate`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error(`Failed to generate recap: ${response.statusText}`);
      }

      const result = await response.json();
      setData(result);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      throw err;
    } finally {
      setLoading(false);
    }
  }, [seasonId, week]);

  useEffect(() => {
    fetchRecap();
  }, [fetchRecap]);

  return { data, loading, error, refetch: fetchRecap, generateRecap };
}

// Hook for fetching storylines
export function useStorylines(teamId?: number) {
  const [data, setData] = useState<Storyline[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStorylines = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params = teamId ? `?team_id=${teamId}` : "";
      const response = await fetch(`${API_BASE}/living/storylines${params}`);

      if (!response.ok) {
        throw new Error(`Failed to fetch storylines: ${response.statusText}`);
      }

      const result = await response.json();
      setData(result.storylines || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [teamId]);

  useEffect(() => {
    fetchStorylines();
  }, [fetchStorylines]);

  return { data, loading, error, refetch: fetchStorylines };
}
