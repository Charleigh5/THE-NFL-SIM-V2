import React, { useState } from "react";
import "./TradeAnalyzer.css";
import { FeedbackCollector } from "../draft/FeedbackCollector";
import { AccessibleTooltip } from "../ui/AccessibleTooltip";
import { Handshake, Info } from "lucide-react";
import type { CounterOfferSuggestion, DraftPickInfo, TradeEvaluation } from "../../types/trade";
import { humanizeNarrativeNote } from "./tradeNarrative";

/**
 * Props for the TradeAnalyzer component.
 */
interface TradeAnalyzerProps {
  seasonId: number;
  teamId: number;
  targetTeamId?: number | null;
  offeredAssets: number[]; // Player IDs
  requestedAssets: number[]; // Player IDs
  offeredPicks?: DraftPickInfo[];
  requestedPicks?: DraftPickInfo[];
  onApplyCounterOffer?: (counter: CounterOfferSuggestion) => void;
}

/**
 * TradeAnalyzer Component
 * ======================
 * Renders live contextual trade evaluation telemetry with WAI-APG accessible tooltips,
 * humanized narrative feedback, and GM counter-offer proposal mechanics.
 */
export const TradeAnalyzer: React.FC<TradeAnalyzerProps> = ({
  seasonId,
  teamId,
  targetTeamId,
  offeredAssets,
  requestedAssets,
  offeredPicks,
  requestedPicks,
  onApplyCounterOffer,
}) => {
  const [loading, setLoading] = useState(false);
  const [evaluation, setEvaluation] = useState<TradeEvaluation | null>(null);
  const [error, setError] = useState<string | null>(null);

  const hasOffered = offeredAssets.length > 0 || (offeredPicks && offeredPicks.length > 0);
  const hasRequested = requestedAssets.length > 0 || (requestedPicks && requestedPicks.length > 0);

  const handleAnalyze = async () => {
    if (!hasOffered || !hasRequested) return;
    if (!targetTeamId) return;

    setLoading(true);
    setError(null);
    setEvaluation(null);
    try {
      const response = await fetch(`/api/trades/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          offering_team_id: teamId,
          target_team_id: targetTeamId,
          offered_player_ids: offeredAssets,
          requested_player_ids: requestedAssets,
          offered_picks: offeredPicks && offeredPicks.length > 0 ? offeredPicks : null,
          requested_picks: requestedPicks && requestedPicks.length > 0 ? requestedPicks : null,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to evaluate trade");
      }

      const data: TradeEvaluation = await response.json();
      setEvaluation(data);
    } catch (err) {
      setError("Could not analyze trade. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getGradeClass = (grade?: string) => {
    if (!grade) return "grade-neutral";
    if (grade.startsWith("A")) return "grade-a";
    if (grade.startsWith("B")) return "grade-b";
    if (grade.startsWith("C")) return "grade-c";
    return "grade-f";
  };

  return (
    <div className="trade-analyzer" data-testid="trade-analyzer-widget">
      <div className="analyzer-header">
        <h4>Contextual Trade Value Analysis</h4>
      </div>

      <button
        className="analyze-btn"
        onClick={handleAnalyze}
        data-testid="analyze-btn"
        disabled={loading || !targetTeamId || !hasOffered || !hasRequested}
      >
        {loading ? "Consulting GM & Analytics..." : "Analyze Fairness"}
      </button>

      {loading && (
        <div className="analyzer-loading" data-testid="analyzer-loading">
          <div className="mini-spinner"></div>
          <span>Calculating market surplus, cap impact & draft EV...</span>
        </div>
      )}

      {error && <div className="analyzer-error">{error}</div>}

      {evaluation && (
        <div
          className={`evaluation-result ${evaluation.decision.toLowerCase()}`}
          data-testid="evaluation-result"
        >
          <div className="decision-header-row">
            <div className="decision-badge" data-testid="decision-badge">
              {evaluation.decision}
            </div>

            {evaluation.user_side && evaluation.ai_side && (
              <div className="dual-grades" data-testid="dual-grades">
                <div className="grade-box">
                  <span className="grade-title">Your Grade</span>
                  <span className={`grade-pill ${getGradeClass(evaluation.user_side.grade)}`}>
                    {evaluation.user_side.grade}
                  </span>
                </div>
                <div className="grade-box">
                  <span className="grade-title">GM Grade</span>
                  <span className={`grade-pill ${getGradeClass(evaluation.ai_side.grade)}`}>
                    {evaluation.ai_side.grade}
                  </span>
                </div>
              </div>
            )}
          </div>

          <div className="fairness-score">
            <div className="flex items-center gap-1.5">
              <span className="label">Fairness Surplus:</span>
              <AccessibleTooltip content="Surplus percentage difference between offered and requested value. Positive values favor your franchise; negative values favor the trade partner.">
                <Info className="w-3.5 h-3.5 text-zinc-400 hover:text-cyan-400 cursor-help" />
              </AccessibleTooltip>
            </div>
            <span
              className={`score ${evaluation.score >= 0 ? "positive" : "negative"}`}
              data-testid="fairness-score"
            >
              {evaluation.score > 0 ? "+" : ""}
              {typeof evaluation.score === "number"
                ? evaluation.score.toFixed(1)
                : evaluation.score}
              %
            </span>
          </div>

          {evaluation.offered_value !== undefined && evaluation.requested_value !== undefined && (
            <div className="tvp-values-row">
              <div className="tvp-stat">
                <div className="flex items-center gap-1">
                  <span className="tvp-label">You Offer Capital</span>
                  <AccessibleTooltip content="Contextual Trade Value Points (TVP): Jimmy Johnson draft value combined with contract cap efficiency, age decay, and positional scarcity.">
                    <Info className="w-3 h-3 text-zinc-400 hover:text-cyan-400 cursor-help" />
                  </AccessibleTooltip>
                </div>
                <span className="tvp-val" data-testid="offered-capital-val">
                  {Math.round(evaluation.offered_value).toLocaleString()} Pts
                </span>
              </div>
              <div className="tvp-stat">
                <div className="flex items-center gap-1">
                  <span className="tvp-label">You Receive Capital</span>
                  <AccessibleTooltip content="Contextual Trade Value Points (TVP): Jimmy Johnson draft value combined with contract cap efficiency, age decay, and positional scarcity.">
                    <Info className="w-3 h-3 text-zinc-400 hover:text-cyan-400 cursor-help" />
                  </AccessibleTooltip>
                </div>
                <span className="tvp-val" data-testid="received-capital-val">
                  {Math.round(evaluation.requested_value).toLocaleString()} Pts
                </span>
              </div>
            </div>
          )}

          {evaluation.narrative_notes && evaluation.narrative_notes.length > 0 && (
            <div className="narrative-tags-container" data-testid="narrative-tags">
              {evaluation.narrative_notes.map((note, idx) => {
                const humanized = humanizeNarrativeNote(note);
                return (
                  <AccessibleTooltip key={idx} content={humanized.tooltip}>
                    <span className="narrative-tag" data-testid={`narrative-tag-${idx}`}>
                      {humanized.label}
                    </span>
                  </AccessibleTooltip>
                );
              })}
            </div>
          )}

          <div className="gm-reasoning" data-testid="gm-reasoning">
            <p>"{evaluation.reasoning}"</p>
          </div>

          {evaluation.counter_offer && (
            <div className="counter-offer-banner" data-testid="counter-offer-banner">
              <div className="counter-offer-header">
                <div className="counter-icon-box">
                  <Handshake className="w-5 h-5 text-amber-400" />
                </div>
                <strong>GM Counter-Offer Proposal</strong>
              </div>
              <p className="counter-offer-summary">
                {"summary" in evaluation.counter_offer && evaluation.counter_offer.summary
                  ? evaluation.counter_offer.summary
                  : "Consider adding future draft capital to bridge the value gap."}
              </p>
              {onApplyCounterOffer && "add_picks" in evaluation.counter_offer && (
                <button
                  type="button"
                  className="apply-counter-btn"
                  onClick={() =>
                    onApplyCounterOffer(evaluation.counter_offer as CounterOfferSuggestion)
                  }
                >
                  Apply Suggested Counter
                </button>
              )}
            </div>
          )}

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
