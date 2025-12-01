import React, { useState } from "react";
import "./TradeAnalyzer.css";

interface TradeAnalyzerProps {
  seasonId: number;
  teamId: number;
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
  offeredAssets,
  requestedAssets,
}) => {
  const [loading, setLoading] = useState(false);
  const [evaluation, setEvaluation] = useState<TradeEvaluation | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (offeredAssets.length === 0 && requestedAssets.length === 0) return;

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`/api/season/${seasonId}/gm/evaluate-trade`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          team_id: teamId,
          offered_ids: offeredAssets,
          requested_ids: requestedAssets,
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
    <div className="trade-analyzer">
      <div className="analyzer-header">
        <h4>AI Trade Analysis</h4>
      </div>

      {!evaluation && !loading && (
        <button
          className="analyze-btn"
          onClick={handleAnalyze}
          disabled={offeredAssets.length === 0 && requestedAssets.length === 0}
        >
          Analyze Fairness
        </button>
      )}

      {loading && (
        <div className="analyzer-loading">
          <div className="mini-spinner"></div>
          <span>Consulting GM...</span>
        </div>
      )}

      {error && <div className="analyzer-error">{error}</div>}

      {evaluation && (
        <div className={`evaluation-result ${evaluation.decision.toLowerCase()}`}>
          <div className="decision-badge">{evaluation.decision}</div>
          <div className="fairness-score">
            <span className="label">Fairness Score:</span>
            <span className={`score ${evaluation.score >= 0 ? "positive" : "negative"}`}>
              {evaluation.score > 0 ? "+" : ""}
              {evaluation.score}
            </span>
          </div>
          <div className="gm-reasoning">
            <p>"{evaluation.reasoning}"</p>
          </div>
          <button className="re-analyze-btn" onClick={handleAnalyze}>
            Re-evaluate
          </button>
        </div>
      )}
    </div>
  );
};
