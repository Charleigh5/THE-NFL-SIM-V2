import { useState, useEffect, useCallback } from "react";
import styles from "./NewsFeed.module.css";

interface NewsItem {
  headline: string;
  source: string;
  date: string;
  category: string;
  team_id?: number;
  player_id?: number;
  is_breaking: boolean;
}

interface NewsResponse {
  items: NewsItem[];
  total: number;
  last_updated: string;
}

interface NewsFeedProps {
  limit?: number;
  showRefresh?: boolean;
  compact?: boolean;
}

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function NewsFeed({
  limit = 5,
  showRefresh = true,
  compact = false,
}: NewsFeedProps) {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>("");

  const fetchNews = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/api/news/league?limit=${limit}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch news: ${response.statusText}`);
      }
      const data: NewsResponse = await response.json();
      setNews(data.items);
      setLastUpdated(data.last_updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load news");
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchNews();
    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchNews, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, [fetchNews]);

  const getCategoryIcon = (category: string): string => {
    switch (category.toLowerCase()) {
      case "injury":
        return "🏥";
      case "trade":
        return "🔄";
      case "draft":
        return "📋";
      case "contract":
        return "💰";
      case "performance":
        return "📈";
      default:
        return "📰";
    }
  };

  const formatDate = (dateStr: string): string => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));

    if (diffHours < 1) return "Just now";
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffHours < 48) return "Yesterday";
    return date.toLocaleDateString();
  };

  if (loading && news.length === 0) {
    return (
      <div className={`${styles.container} ${compact ? styles.compact : ""}`}>
        <div className={styles.header}>
          <h3 className={styles.title}>📰 League News</h3>
        </div>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <span>Loading news...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`${styles.container} ${compact ? styles.compact : ""}`}>
        <div className={styles.header}>
          <h3 className={styles.title}>📰 League News</h3>
        </div>
        <div className={styles.error}>
          <span>⚠️ {error}</span>
          <button onClick={fetchNews} className={styles.retryButton}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`${styles.container} ${compact ? styles.compact : ""}`}>
      <div className={styles.header}>
        <h3 className={styles.title}>📰 League News</h3>
        {showRefresh && (
          <button
            onClick={fetchNews}
            className={styles.refreshButton}
            disabled={loading}
            title="Refresh news"
          >
            {loading ? "⏳" : "🔄"}
          </button>
        )}
      </div>

      <div className={styles.newsList}>
        {news.map((item, index) => (
          <article
            key={`${item.headline}-${index}`}
            className={`${styles.newsItem} ${item.is_breaking ? styles.breaking : ""}`}
          >
            {item.is_breaking && <span className={styles.breakingBadge}>🔴 BREAKING</span>}
            <div className={styles.newsContent}>
              <span className={styles.categoryIcon}>{getCategoryIcon(item.category)}</span>
              <div className={styles.newsText}>
                <p className={styles.headline}>{item.headline}</p>
                <div className={styles.meta}>
                  <span className={styles.source}>{item.source}</span>
                  <span className={styles.separator}>•</span>
                  <span className={styles.date}>{formatDate(item.date)}</span>
                </div>
              </div>
            </div>
          </article>
        ))}
      </div>

      {lastUpdated && (
        <div className={styles.footer}>
          <span className={styles.lastUpdated}>Last updated: {formatDate(lastUpdated)}</span>
        </div>
      )}
    </div>
  );
}
