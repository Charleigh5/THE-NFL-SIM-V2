import React, { useState } from "react";
import "./TradeAnalyzer.css";
import { FeedbackCollector } from "../draft/FeedbackCollector";

interface TradeAnalyzerProps {
  seasonId: number;
  teamId: number;
  targetTeamId?: number | null;
  offeredAssets: number[]; // Player IDs
  requestedAssets: number[]; // Player IDs
}

interface TradeEvaluation {
  decision: "ACCEPT" | "REJECT";
  score: number;
  reasoning: string;
}

export const TradeAnalyzer: React.FC<TradeAnalyzerProps> = ({
  seasonId,
  teamId,
  targetTeamId,
  offeredAssets,
  requestedAssets,
}) => {
  const [loading, setLoading] = useState(false);
  const [evaluation, setEvaluation] = useState<TradeEvaluation | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (offeredAssets.length === 0 && requestedAssets.length === 0) return;
    if (!targetTeamId) return;

    setLoading(true);
    setError(null);
    // Ensure the panel reflects the latest analysis.
    setEvaluation(null);
    try {
      const response = await fetch(`/api/trades/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target_team_id: targetTeamId,
          offered_player_ids: offeredAssets,
          requested_player_ids: requestedAssets,
          offered_picks: null,
          requested_picks: null,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to evaluate trade");
      }

      const data = await response.json();
      setEvaluation(data);
    } catch (err) {
      setError("Could not analyze trade. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="trade-analyzer" data-testid="trade-analyzer-widget">
      <div className="analyzer-header">
        <h4>AI Trade Analysis</h4>
      </div>

      <button
        className="analyze-btn"
        onClick={handleAnalyze}
        data-testid="analyze-btn"
        disabled={
          loading || !targetTeamId || (offeredAssets.length === 0 && requestedAssets.length === 0)
        }
      >
        {loading ? "Consulting GM..." : "Analyze Fairness"}
      </button>

      {loading && (
        <div className="analyzer-loading" data-testid="analyzer-loading">
          <div className="mini-spinner"></div>
          <span>Consulting GM...</span>
        </div>
      )}

      {error && <div className="analyzer-error">{error}</div>}

      {evaluation && (
        <div
          className={`evaluation-result ${evaluation.decision.toLowerCase()}`}
          data-testid="evaluation-result"
        >
          <div className="decision-badge" data-testid="decision-badge">
            {evaluation.decision}
          </div>
          <div className="fairness-score">
            <span className="label">Fairness Score:</span>
            <span
              className={`score ${evaluation.score >= 0 ? "positive" : "negative"}`}
              data-testid="fairness-score"
            >
              {evaluation.score > 0 ? "+" : ""}
              {evaluation.score}
            </span>
          </div>
          <div className="gm-reasoning" data-testid="gm-reasoning">
            <p>"{evaluation.reasoning}"</p>
          </div>

          <FeedbackCollector
            contextId={`trade-${seasonId}-${teamId}-${targetTeamId ?? "na"}-${Date.now()}`}
            contextType="trade"
          />

          <button
            className="re-analyze-btn"
            onClick={() => setEvaluation(null)}
            data-testid="re-analyze-btn"
          >
            Re-evaluate
          </button>
        </div>
      )}
    </div>
  );
};
