import { useRef, useEffect } from "react";
import { useStorylines } from "../../hooks/useLivingWorld";
import type { Storyline } from "../../hooks/useLivingWorld";
import "./StorylineTracker.css";

interface StorylineTrackerProps {
  teamId?: number;
}

// Storyline type configurations
const STORYLINE_CONFIG: Record<string, { icon: string; color: string; label: string }> = {
  HOT_STREAK: { icon: "🔥", color: "#e74c3c", label: "Hot Streak" },
  COLD_STREAK: { icon: "❄️", color: "#3498db", label: "Cold Streak" },
  BREAKOUT_PLAYER: { icon: "⭐", color: "#f1c40f", label: "Breakout Star" },
  QB_CONTROVERSY: { icon: "🏈", color: "#9b59b6", label: "QB Controversy" },
  RIVALRY: { icon: "⚔️", color: "#e67e22", label: "Rivalry Renewed" },
  REDEMPTION_ARC: { icon: "🦅", color: "#2ecc71", label: "Redemption Arc" },
  DECLINE: { icon: "📉", color: "#7f8c8d", label: "Declining Star" },
  TRADE_AFTERMATH: { icon: "🔄", color: "#1abc9c", label: "Trade Aftermath" },
};

function StorylineCard({ storyline }: { storyline: Storyline }) {
  const intensityRef = useRef<HTMLDivElement>(null);

  const config = STORYLINE_CONFIG[storyline.type] || {
    icon: "📖",
    color: "#95a5a6",
    label: storyline.type.replace(/_/g, " "),
  };

  // Intensity bar (1-5)
  const intensityPct = (storyline.intensity / 5) * 100;

  useEffect(() => {
    if (intensityRef.current) {
      intensityRef.current.style.setProperty("--intensity-pct", `${intensityPct}%`);
    }
  }, [intensityPct]);

  return (
    <div
      className={`storyline-card storyline-${storyline.type.toLowerCase()}`}
      data-storyline-type={storyline.type}
    >
      <div className="storyline-header">
        <span className="storyline-icon">{config.icon}</span>
        <span className="storyline-label">{config.label}</span>
      </div>

      <div className="storyline-details">
        <span className="detail-item">Started Week {storyline.start_week}</span>
        <span className="detail-item">{storyline.event_count} events</span>
      </div>

      <div ref={intensityRef} className="intensity-bar-container">
        <div className="intensity-label">
          <span>Intensity</span>
          <span>{storyline.intensity}/5</span>
        </div>
        <div className="intensity-bar">
          <div className="intensity-fill" />
        </div>
      </div>
    </div>
  );
}

export function StorylineTracker({ teamId }: StorylineTrackerProps) {
  const { data, loading, error, refetch } = useStorylines(teamId);

  if (loading) {
    return (
      <div className="storyline-tracker loading">
        <div className="loading-spinner" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="storyline-tracker error">
        <p>Failed to load storylines</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="storyline-tracker empty">
        <span className="empty-icon">📚</span>
        <p>No active storylines</p>
        <p className="hint">Storylines develop over multiple weeks of play.</p>
      </div>
    );
  }

  return (
    <section className="storyline-tracker">
      <header className="tracker-header">
        <h3>📖 Active Storylines</h3>
        <span className="storyline-count">{data.length} active</span>
      </header>

      <div className="storyline-list">
        {data.map((storyline, index) => (
          <StorylineCard key={`${storyline.type}-${index}`} storyline={storyline} />
        ))}
      </div>
    </section>
  );
}

export default StorylineTracker;
