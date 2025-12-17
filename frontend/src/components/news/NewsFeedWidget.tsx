/**
 * NewsFeedWidget Component
 *
 * A sidebar widget that displays the Living World news feed.
 * Uses the useLivingNews custom hook for data fetching.
 */
import { useLivingNews } from "../../hooks/useLivingWorld";
import type { LivingNewsItem } from "../../hooks/useLivingWorld";
import "./NewsFeedWidget.css";

interface NewsFeedWidgetProps {
  seasonId: number;
  week?: number;
  maxItems?: number;
}

function NewsItemCard({ item }: { item: LivingNewsItem }) {
  const isBreaking = item.importance_score >= 0.7;

  return (
    <article className={`news-item-card ${isBreaking ? "breaking" : ""}`}>
      {isBreaking && <span className="breaking-badge">BREAKING</span>}
      <div className="category-indicator" data-category={item.category} />
      <div className="news-content">
        <h4 className="news-headline">{item.headline}</h4>
        <p className="news-preview">{item.content.slice(0, 120)}...</p>
        <div className="news-meta">
          <span className="news-category">{item.category}</span>
          <span className="news-time">{new Date(item.created_at).toLocaleDateString()}</span>
        </div>
      </div>
    </article>
  );
}

export function NewsFeedWidget({ seasonId, week, maxItems = 10 }: NewsFeedWidgetProps) {
  const { data, loading, error, refetch } = useLivingNews(seasonId, week, 1, maxItems);

  if (loading) {
    return (
      <div className="news-feed-widget loading">
        <div className="loading-spinner" />
        <p>Loading news...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="news-feed-widget error">
        <p>Failed to load news</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  if (!data || data.items.length === 0) {
    return (
      <div className="news-feed-widget empty">
        <p>No news available yet.</p>
        <p className="hint">Play some games to generate stories!</p>
      </div>
    );
  }

  return (
    <aside className="news-feed-widget">
      <header className="widget-header">
        <h3>📰 Living World News</h3>
        <span className="news-count">{data.total_count} stories</span>
      </header>

      <div className="news-feed-list">
        {data.items.map((item) => (
          <NewsItemCard key={item.id} item={item} />
        ))}
      </div>

      {data.has_more && <button className="load-more-btn">View All News →</button>}
    </aside>
  );
}

export default NewsFeedWidget;
