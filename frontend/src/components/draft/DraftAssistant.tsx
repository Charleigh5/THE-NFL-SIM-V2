import React, { useState } from "react";
import { draftService, type DraftSuggestionResponse } from "../../services/draft";
import { FeedbackCollector } from "./FeedbackCollector";
import type { Prospect } from "../../types/offseason";
import "./DraftAssistant.css";

interface DraftAssistantProps {
  seasonId: number;
  teamId: number;
  pickNumber: number;
  availablePlayers: number[];
  onPlayerSelect?: (prospect: Prospect) => void;
}

export const DraftAssistant: React.FC<DraftAssistantProps> = ({
  seasonId,
  teamId,
  pickNumber,
  availablePlayers,
  onPlayerSelect,
}) => {
  const [loading, setLoading] = useState(false);
  const [suggestion, setSuggestion] = useState<DraftSuggestionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGetRecommendation = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await draftService.getDraftSuggestion({
        team_id: teamId,
        pick_number: pickNumber,
        available_players: availablePlayers,
        include_historical_data: true,
      });
      setSuggestion(result);
    } catch (err) {
      setError("Could not get recommendation. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Helper to construct a minimal Prospect object for the callback
  const handleSelect = (id: number, name: string, position: string, rating: number) => {
    if (onPlayerSelect) {
      // We construct a partial prospect here. In a real app, we might want to find the full prospect object
      // from the availablePlayers list if possible, but for now this suffices for the callback
      onPlayerSelect({
        id,
        name,
        position,
        overall_rating: rating,
        // Default values for required fields that might be missing in suggestion
        first_name: name.split(" ")[0],
        last_name: name.split(" ").slice(1).join(" "),
        height: 0,
        weight: 0,
        age: 0,
        speed: 0,
        acceleration: 0,
        strength: 0,
        agility: 0,
      });
    }
  };

  return (
    <div className="draft-assistant">
      <div className="assistant-header">
        <h3>War Room</h3>
        <span className="beta-tag">AI POWERED</span>
      </div>

      <div className="assistant-content">
        {!suggestion && !loading && (
          <div className="assistant-intro">
            <p>
              Analyze the board and get a recommendation based on team needs, value, and historical
              data.
            </p>
            <button className="recommend-btn" onClick={handleGetRecommendation}>
              Analyze Pick #{pickNumber}
            </button>
          </div>
        )}

        {loading && (
          <div className="assistant-loading">
            <div className="spinner"></div>
            <p>Crunching numbers...</p>
            <span className="loading-detail">Analyzing roster gaps...</span>
            <span className="loading-detail">Comparing historical data...</span>
          </div>
        )}

        {error && (
          <div className="assistant-error">
            <p>{error}</p>
            <button className="retry-btn" onClick={handleGetRecommendation}>
              Retry
            </button>
          </div>
        )}

        {suggestion && (
          <div className="suggestion-card">
            <div className="recommendation-header">
              <span className="label">RECOMMENDED PICK</span>
              <div className="confidence-meter">
                <div className="confidence-fill" data-confidence={suggestion.confidence_score} />
                <span>{Math.round(suggestion.confidence_score * 100)}% Confidence</span>
              </div>
            </div>

            <div className="suggested-player-card">
              <div className="player-info">
                <div className="player-main">
                  <span className="pos-badge">{suggestion.position}</span>
                  <span className="player-name">{suggestion.player_name}</span>
                </div>
                <span className="player-rating">{suggestion.overall_rating} OVR</span>
              </div>

              <button
                className="select-player-btn"
                onClick={() =>
                  handleSelect(
                    suggestion.recommended_player_id,
                    suggestion.player_name,
                    suggestion.position,
                    suggestion.overall_rating
                  )
                }
              >
                Draft Player
              </button>
            </div>

            <div className="analysis-section">
              <h5>Analysis</h5>
              <p className="reasoning-text">{suggestion.reasoning}</p>
            </div>

            {suggestion.historical_comparison && (
              <div className="historical-comp">
                <h5>Historical Comparison</h5>
                <div className="comp-card">
                  <div className="comp-header">
                    <span className="comp-name">
                      {suggestion.historical_comparison.comparable_player_name}
                    </span>
                    <span className="comp-years">
                      {suggestion.historical_comparison.seasons_active}
                    </span>
                  </div>
                  <p className="comp-highlights">
                    {suggestion.historical_comparison.career_highlights}
                  </p>
                  <div className="similarity-bar">
                    <span>Similarity</span>
                    <progress value={suggestion.historical_comparison.similarity_score} max={1} />
                  </div>
                </div>
              </div>
            )}

            {suggestion.roster_gap_analysis && suggestion.roster_gap_analysis.length > 0 && (
              <div className="gap-analysis">
                <h5>Roster Impact</h5>
                {suggestion.roster_gap_analysis.map((gap, idx) => (
                  <div key={idx} className="gap-item">
                    <div className="gap-header">
                      <span>{gap.position}</span>
                      <span className={`priority ${gap.priority_level.toLowerCase()}`}>
                        {gap.priority_level}
                      </span>
                    </div>
                    <div className="gap-stats">
                      <span>Current: {gap.current_count}</span>
                      <span>Target: {gap.target_count}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {suggestion.alternative_picks.length > 0 && (
              <div className="alternatives-section">
                <h5>Alternatives</h5>
                <div className="alternatives-list">
                  {suggestion.alternative_picks.map((alt) => (
                    <div
                      key={alt.player_id}
                      className="alt-item"
                      onClick={() =>
                        handleSelect(
                          alt.player_id,
                          alt.player_name,
                          alt.position,
                          alt.overall_rating
                        )
                      }
                    >
                      <div className="alt-info">
                        <span className="alt-pos">{alt.position}</span>
                        <span className="alt-name">{alt.player_name}</span>
                      </div>
                      <span className="alt-rating">{alt.overall_rating}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="feedback-section">
              <FeedbackCollector
                contextId={`draft-${seasonId}-${teamId}-${suggestion.recommended_player_id}`}
                contextType="draft"
              />
            </div>

            <button className="reset-btn" onClick={() => setSuggestion(null)}>
              New Analysis
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
