import React, { useState, useEffect, useCallback } from "react";
import { seasonApi } from "../services/season";
import { DraftBoard } from "../components/offseason/DraftBoard";
import { DraftTicker } from "../components/offseason/DraftTicker";
import { TradeModal } from "../components/offseason/TradeModal";
import type { Prospect, DraftPickDetail, DraftPickSummary, TeamNeed } from "../types/offseason";
import "./DraftRoom.css";

export const DraftRoom: React.FC = () => {
  const [seasonId, setSeasonId] = useState<number | null>(null);
  const [currentPick, setCurrentPick] = useState<DraftPickDetail | null>(null);
  const [prospects, setProspects] = useState<Prospect[]>([]);
  const [recentPicks, setRecentPicks] = useState<DraftPickSummary[]>([]);
  const [teamNeeds, setTeamNeeds] = useState<TeamNeed[]>([]);

  const [simulating, setSimulating] = useState(false);
  const [showTradeModal, setShowTradeModal] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchDraftState = useCallback(async (sid: number) => {
    try {
      const [pick, topProspects] = await Promise.all([
        seasonApi.getCurrentPick(sid),
        seasonApi.getTopProspects(sid, 100),
      ]);
      setCurrentPick(pick);
      setProspects(topProspects);

      if (pick) {
        const needs = await seasonApi.getTeamNeeds(sid, pick.team_id);
        setTeamNeeds(needs);
      }
    } catch (err) {
      console.error("Error fetching draft state:", err);
    }
  }, []);

  useEffect(() => {
    const init = async () => {
      try {
        const season = await seasonApi.getCurrentSeason();
        setSeasonId(season.id);
        await fetchDraftState(season.id);
      } catch (err) {
        console.error("Error initializing draft room:", err);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [fetchDraftState]);

  const handlePick = async (prospect: Prospect) => {
    if (!seasonId || !currentPick) return;

    // Only allow pick if it's user's turn (assuming userTeamId matches)
    // For now, allow picking for any team for testing

    try {
      const result = await seasonApi.makePick(seasonId, prospect.id);

      // Add to recent picks
      const summary: DraftPickSummary = {
        round: result.round,
        pick_number: result.pick_number,
        team_id: result.team_id,
        player_name: prospect.name,
        player_position: prospect.position,
        player_overall: prospect.overall_rating,
      };
      setRecentPicks((prev) => [summary, ...prev].slice(0, 10));

      // Refresh state
      await fetchDraftState(seasonId);
    } catch (err) {
      console.error("Error making pick:", err);
    }
  };

  const handleSimulateDraft = async () => {
    if (!seasonId) return;
    setSimulating(true);
    try {
      const results = await seasonApi.simulateDraft(seasonId);
      setRecentPicks((prev) => [...results.reverse(), ...prev].slice(0, 20));
      await fetchDraftState(seasonId);
    } catch (err) {
      console.error("Error simulating draft:", err);
    } finally {
      setSimulating(false);
    }
  };

  const handleTrade = async (targetTeamId: number) => {
    if (!seasonId) return;
    try {
      await seasonApi.tradeCurrentPick(seasonId, targetTeamId);
      setShowTradeModal(false);
      await fetchDraftState(seasonId);
    } catch (err) {
      console.error("Error trading pick:", err);
    }
  };

  if (loading) return <div className="loading">Loading Draft Room...</div>;

  return (
    <div className="draft-room">
      <div className="draft-header-bar">
        <h1>NFL Draft Room</h1>
        {currentPick && (
          <div className="current-pick-info">
            <span className="pick-label">ON THE CLOCK:</span>
            <span className="pick-team">Team {currentPick.team_id}</span>
            <span className="pick-round">
              Round {currentPick.round} • Pick {currentPick.pick_number}
            </span>
          </div>
        )}
      </div>

      <DraftTicker recentPicks={recentPicks} />

      <div className="draft-content">
        <div className="draft-main">
          <DraftBoard prospects={prospects} teamNeeds={teamNeeds} onProspectSelect={handlePick} />
        </div>

        <div className="draft-sidebar">
          <div className="team-needs-panel">
            <h3>Team Needs</h3>
            <div className="needs-list">
              {teamNeeds.map((need) => (
                <div key={need.position} className="need-item">
                  <div className="need-info">
                    <span className="need-pos">{need.position}</span>
                    <div
                      className="need-bar"
                      style={{ width: `${Math.min(100, need.need_score * 20)}%` }}
                    ></div>
                  </div>
                  <span className="need-score">{need.need_score.toFixed(1)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Mock Draft Simulator Placeholder */}
          <div className="mock-sim-panel">
            <h3>Draft Simulator</h3>
            <p>Simulate the remainder of the draft automatically.</p>
            <button
              className="mock-btn"
              onClick={handleSimulateDraft}
              disabled={simulating || !currentPick}
            >
              Simulate Rest of Draft
            </button>
          </div>

          <div className="trade-panel">
            <h3>Trade Options</h3>
            <button
              className="trade-btn"
              onClick={() => setShowTradeModal(true)}
              disabled={!currentPick}
            >
              Trade Current Pick
            </button>
          </div>
        </div>
      </div>

      {showTradeModal && currentPick && seasonId && (
        <TradeModal
          seasonId={seasonId}
          currentTeamId={currentPick.team_id}
          onClose={() => setShowTradeModal(false)}
          onTrade={handleTrade}
        />
      )}
    </div>
  );
};
