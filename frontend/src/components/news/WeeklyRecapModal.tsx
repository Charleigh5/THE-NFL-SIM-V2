/**
 * WeeklyRecapModal Component
 *
 * A modal that displays the "SportsCenter" style weekly recap.
 * Features:
 * - Markdown rendering for summary text
 * - MVP player highlight
 * - Play of the week showcase
 * - Generate button if recap doesn't exist
 */
import { useState } from "react";
import { useWeeklyRecap } from "../../hooks/useLivingWorld";
import type { WeeklyRecap } from "../../hooks/useLivingWorld";
import "./WeeklyRecapModal.css";

interface WeeklyRecapModalProps {
  seasonId: number;
  week: number;
  isOpen: boolean;
  onClose: () => void;
}

function RecapContent({ recap }: { recap: WeeklyRecap }) {
  return (
    <div className="recap-content">
      {/* Summary Section */}
      <section className="recap-section summary-section">
        <div
          className="summary-text"
          dangerouslySetInnerHTML={{
            __html: recap.summary_text
              .replace(/\n/g, "<br/>")
              .replace(/^# /gm, "<h1>")
              .replace(/^## /gm, "<h2>"),
          }}
        />
      </section>

      {/* Highlights Row */}
      <div className="highlights-row">
        {recap.mvp_player_id && (
          <div className="highlight-card mvp-card">
            <span className="highlight-icon">🏆</span>
            <span className="highlight-label">Week MVP</span>
            <span className="highlight-value">Player #{recap.mvp_player_id}</span>
          </div>
        )}

        {recap.play_of_the_week_id && (
          <div className="highlight-card play-card">
            <span className="highlight-icon">🎬</span>
            <span className="highlight-label">Play of the Week</span>
            <span className="highlight-value">{recap.play_of_the_week_id}</span>
          </div>
        )}
      </div>

      {/* Surprising Result */}
      {recap.surprising_result && (
        <section className="recap-section surprise-section">
          <h3>😲 Surprise of the Week</h3>
          <p>{recap.surprising_result}</p>
        </section>
      )}
    </div>
  );
}

export function WeeklyRecapModal({ seasonId, week, isOpen, onClose }: WeeklyRecapModalProps) {
  const { data, loading, error, generateRecap } = useWeeklyRecap(seasonId, week);
  const [generating, setGenerating] = useState(false);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      await generateRecap();
    } catch {
      // Error is handled by the hook
    } finally {
      setGenerating(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="weekly-recap-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <header className="modal-header">
          <div className="header-content">
            <span className="week-badge">WEEK {week}</span>
            <h2>Weekly Wrap-Up</h2>
            <p className="subtitle">Season {seasonId}</p>
          </div>
          <button className="close-btn" onClick={onClose}>
            ×
          </button>
        </header>

        {/* Body */}
        <div className="modal-body">
          {loading ? (
            <div className="loading-state">
              <div className="loading-spinner large" />
              <p>Loading recap...</p>
            </div>
          ) : error ? (
            <div className="error-state">
              <p>Failed to load recap</p>
              <button onClick={handleGenerate}>Try Again</button>
            </div>
          ) : data ? (
            <RecapContent recap={data} />
          ) : (
            <div className="empty-state">
              <span className="empty-icon">📺</span>
              <h3>No Recap Available</h3>
              <p>The weekly recap hasn't been generated yet.</p>
              <button className="generate-btn" onClick={handleGenerate} disabled={generating}>
                {generating ? "Generating..." : "🎬 Generate Recap"}
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="modal-footer">
          <span className="generated-time">
            {data?.created_at && `Generated: ${new Date(data.created_at).toLocaleString()}`}
          </span>
        </footer>
      </div>
    </div>
  );
}

export default WeeklyRecapModal;
