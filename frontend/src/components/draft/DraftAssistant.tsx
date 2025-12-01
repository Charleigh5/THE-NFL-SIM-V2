import React, { useState } from "react";
import "./DraftAssistant.css";

interface DraftAssistantProps {
  seasonId: number;
  teamId: number;
  onPlayerSelect?: (playerId: number) => void;
}

interface Suggestion {
  player_id: number | null;
  reasoning: string;
  alternatives: Record<string, unknown>[];
  external_data?: Record<string, unknown>;
}

export const DraftAssistant: React.FC<DraftAssistantProps> = ({
  seasonId,
  teamId,
  onPlayerSelect,
}) => {
  const [loading, setLoading] = useState(false);
  const [suggestion, setSuggestion] = useState<Suggestion | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGetRecommendation = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`/api/season/${seasonId}/draft/suggest-pick?team_id=${teamId}`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Failed to fetch recommendation");
      }

      const data = await response.json();
      setSuggestion(data);
    } catch (err) {
      setError("Could not get recommendation. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="draft-assistant">
      <div className="assistant-header">
        <h3>AI Draft Assistant</h3>
        <span className="beta-tag">BETA</span>
      </div>

      <div className="assistant-content">
        {!suggestion && !loading && (
          <div className="assistant-intro">
            <p>
              Need help making a pick? Our AI analyzes team needs, historical data, and player value
              to suggest the best fit.
            </p>
            <button className="recommend-btn" onClick={handleGetRecommendation}>
              Get Recommendation
            </button>
          </div>
        )}

        {loading && (
          <div className="assistant-loading">
            <div className="spinner"></div>
            <p>Analyzing roster gaps and prospect value...</p>
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
            <h4>Recommended Pick</h4>
            <div className="suggestion-details">
              {suggestion.player_id ? (
                <div className="suggested-player">
                  <span className="player-id-ref">Player #{suggestion.player_id}</span>
                  {/* In a real app we'd look up the player name from a context or prop */}
                  {onPlayerSelect && (
                    <button
                      className="select-player-btn"
                      onClick={() => onPlayerSelect(suggestion.player_id!)}
                    >
                      Draft Player
                    </button>
                  )}
                </div>
              ) : (
                <p>No suitable player found.</p>
              )}

              <div className="reasoning">
                <h5>Analysis</h5>
                <p>{suggestion.reasoning}</p>
              </div>

              {suggestion.external_data && (
                <div className="external-data">
                  <h5>League Context</h5>
                  <pre>{JSON.stringify(suggestion.external_data, null, 2)}</pre>
                </div>
              )}
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
