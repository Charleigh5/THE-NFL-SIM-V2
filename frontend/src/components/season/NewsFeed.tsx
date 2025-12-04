/**
 * News Feed Widget Component
 *
 * Dashboard widget displaying league news, team news, and injury reports.
 * Integrates with the sports_news MCP server via the backend API.
 */

import React, { useState, useEffect } from "react";
import {
  Newspaper,
  AlertTriangle,
  TrendingUp,
  Users,
  Shield,
  RefreshCw,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import "./NewsFeed.css";

// ============================================================================
// TYPES
// ============================================================================

export interface NewsItem {
  headline: string;
  source: string;
  date: string;
  category: string;
  team_id?: number;
  player_id?: number;
  is_breaking: boolean;
}

export interface NewsResponse {
  items: NewsItem[];
  total: number;
  last_updated: string;
}

interface NewsFeedProps {
  /** Filter news by team name */
  teamFilter?: string;
  /** Maximum items to display */
  maxItems?: number;
  /** Enable compact mode for sidebar */
  compact?: boolean;
  /** Auto-refresh interval in seconds (0 to disable) */
  refreshInterval?: number;
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

const getCategoryIcon = (category: string) => {
  switch (category) {
    case "injuries":
      return <AlertTriangle size={14} className="news-icon injury" />;
    case "trades":
      return <Users size={14} className="news-icon trade" />;
    case "rankings":
      return <TrendingUp size={14} className="news-icon ranking" />;
    case "team":
      return <Shield size={14} className="news-icon team" />;
    default:
      return <Newspaper size={14} className="news-icon general" />;
  }
};

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return "Today";
  if (diffDays === 1) return "Yesterday";
  if (diffDays < 7) return `${diffDays}d ago`;

  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
};

// ============================================================================
// COMPONENT
// ============================================================================

export const NewsFeed: React.FC<NewsFeedProps> = ({
  teamFilter,
  maxItems = 5,
  compact = false,
  refreshInterval = 0,
}) => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState(!compact);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const fetchNews = async () => {
    try {
      setLoading(true);
      setError(null);

      const endpoint = teamFilter
        ? `/api/news/team/${encodeURIComponent(teamFilter)}?limit=${maxItems}`
        : `/api/news/league?limit=${maxItems}`;

      const response = await fetch(`http://localhost:8000${endpoint}`);

      if (!response.ok) {
        throw new Error("Failed to fetch news");
      }

      const data: NewsResponse = await response.json();
      setNews(data.items);
      setLastUpdated(data.last_updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load news");
      console.error("News fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNews();

    if (refreshInterval > 0) {
      const interval = setInterval(fetchNews, refreshInterval * 1000);
      return () => clearInterval(interval);
    }
  }, [teamFilter, maxItems, refreshInterval]);

  const handleRefresh = () => {
    fetchNews();
  };

  if (loading && news.length === 0) {
    return (
      <div className="news-feed-widget loading">
        <div className="news-header">
          <Newspaper size={18} className="header-icon" />
          <h3>League News</h3>
        </div>
        <div className="news-loading">
          <div className="loading-spinner" />
          <span>Loading news...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="news-feed-widget error">
        <div className="news-header">
          <Newspaper size={18} className="header-icon" />
          <h3>League News</h3>
        </div>
        <div className="news-error">
          <AlertTriangle size={24} />
          <span>{error}</span>
          <button onClick={handleRefresh} className="retry-button">
            <RefreshCw size={14} />
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`news-feed-widget ${compact ? "compact" : ""}`}>
      <div className="news-header" onClick={() => compact && setExpanded(!expanded)}>
        <div className="header-left">
          <Newspaper size={18} className="header-icon" />
          <h3>{teamFilter ? `${teamFilter} News` : "League News"}</h3>
          {compact && <span className="news-count">{news.length}</span>}
        </div>
        <div className="header-right">
          {!compact && (
            <button
              onClick={handleRefresh}
              className="refresh-button"
              title="Refresh news"
              disabled={loading}
            >
              <RefreshCw size={14} className={loading ? "spinning" : ""} />
            </button>
          )}
          {compact && (expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />)}
        </div>
      </div>

      {(!compact || expanded) && (
        <div className="news-list">
          {news.map((item, index) => (
            <div
              key={`${item.headline}-${index}`}
              className={`news-item ${item.is_breaking ? "breaking" : ""}`}
            >
              {item.is_breaking && <div className="breaking-badge">BREAKING</div>}
              <div className="news-content">
                <div className="news-category">
                  {getCategoryIcon(item.category)}
                  <span className="category-label">{item.category}</span>
                </div>
                <h4 className="news-headline">{item.headline}</h4>
                <div className="news-meta">
                  <span className="news-source">{item.source}</span>
                  <span className="news-separator">•</span>
                  <span className="news-date">{formatDate(item.date)}</span>
                </div>
              </div>
            </div>
          ))}

          {news.length === 0 && (
            <div className="no-news">
              <Newspaper size={32} className="empty-icon" />
              <span>No news available</span>
            </div>
          )}
        </div>
      )}

      {lastUpdated && !compact && (
        <div className="news-footer">
          <span className="last-updated">
            Updated: {new Date(lastUpdated).toLocaleTimeString()}
          </span>
        </div>
      )}
    </div>
  );
};

export default NewsFeed;
