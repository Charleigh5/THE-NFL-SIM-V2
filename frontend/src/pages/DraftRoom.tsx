import React, { useState, useEffect, useCallback } from "react";
import { useLoaderData } from "react-router-dom";
import { seasonApi } from "../services/season";
import { draftService } from "../services/draft";
import { DraftBoard } from "../components/offseason/DraftBoard";
// import { DraftTicker } from "../components/offseason/DraftTicker";
import { TradeModal } from "../components/offseason/TradeModal";
import { DraftAssistant } from "../components/draft/DraftAssistant";
import { WarRoomTicker } from "../components/draft/WarRoomTicker";
import { TradePhone } from "../components/draft/TradePhone";
import type { Prospect, DraftPickDetail, DraftPickSummary, TeamNeed } from "../types/offseason";
import type { Team } from "../services/api";
import type { Season } from "../types/season";
// import "./DraftRoom.css";
import { ParallaxScene } from "../components/immersive/ParallaxScene";
// import { RibbonTicker } from "../components/immersive/RibbonTicker";
import { BroadcastPanel } from "../components/immersive/BroadcastPanel";
import styles from "./DraftRoom.module.css";

// Loader data type
interface DraftRoomLoaderData {
  teams: Team[];
  season: Season | null;
  currentPick: DraftPickDetail | null;
  noSeason: boolean;
}

export const DraftRoom: React.FC = () => {
  // Get loader data
  const loaderData = useLoaderData() as DraftRoomLoaderData | undefined;

  const [seasonId, setSeasonId] = useState<number | null>(loaderData?.season?.id ?? null);
  const [currentPick, setCurrentPick] = useState<DraftPickDetail | null>(null);
  const [prospects, setProspects] = useState<Prospect[]>([]);
  // TODO: Display recentPicks in a ticker or sidebar component
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [recentPicks, setRecentPicks] = useState<DraftPickSummary[]>([]);
  const [teamNeeds, setTeamNeeds] = useState<TeamNeed[]>([]);

  const [simulating, setSimulating] = useState(false);
  const [showTradeModal, setShowTradeModal] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchDraftState = useCallback(async (sid: number) => {
    try {
      const [pick, topProspects] = await Promise.all([
        seasonApi.getCurrentPick(sid),
        draftService.getDraftBoard(),
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
    if (loaderData?.noSeason) return;

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
  }, [fetchDraftState, loaderData?.noSeason]);

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

  // Handle no season state from loader
  if (loaderData?.noSeason) {
    return (
      <div className="draft-room" data-testid="no-season-state">
        <div className="empty-state">
          <div className="empty-state-icon">🏈</div>
          <h1>No Active Season</h1>
          <p>Start a new season from the Season Dashboard to access the Draft Room.</p>
          <a href="/season" className="action-button">
            Go to Season Dashboard
          </a>
        </div>
      </div>
    );
  }

  if (loading) return <div className="loading">Loading Draft Room...</div>;

  return (
    <ParallaxScene>
      <div className={`draft-room ${styles.container}`} data-testid="draft-room-page">
        {loading && <div className="loading-overlay">Loading...</div>}

        <div className={styles.headerBar}>
          <div>
            <h1 className={styles.headerTitle}>Draft Room</h1>
            <div className={styles.headerSubtitle}>Draft Theater • Live War Room Broadcast</div>
          </div>
          {currentPick && (
            <div className={styles.onTheClock}>
              <span className={styles.clockLabel}>On The Clock</span>
              <span className={styles.clockTeam}>Team {currentPick.team_id}</span>
              <span className={styles.clockRound}>
                Round {currentPick.round} • Pick {currentPick.pick_number}
              </span>
            </div>
          )}
        </div>

        <WarRoomTicker />

        <TradePhone
          hasOffer={showTradeModal} // Simulate offer when modal is open for now, or add specific state
          onAnswer={() => setShowTradeModal(true)}
        />

        <div className={styles.draftContent}>
          <div className={styles.mainBoard}>
            <BroadcastPanel title="Big Board - Live Feed" isLive={true}>
              <DraftBoard
                prospects={prospects}
                teamNeeds={teamNeeds}
                onProspectSelect={handlePick}
              />
            </BroadcastPanel>
          </div>

          <div className={styles.sidebar}>
            {seasonId && currentPick && (
              <BroadcastPanel title="AI Analyst">
                <DraftAssistant
                  seasonId={seasonId}
                  teamId={currentPick.team_id}
                  pickNumber={currentPick.pick_number}
                  availablePlayers={prospects.map((p) => p.id)}
                  onPlayerSelect={handlePick}
                />
              </BroadcastPanel>
            )}

            <BroadcastPanel title="Team Needs">
              <div className={styles.needsList}>
                {teamNeeds.map((need) => (
                  <div key={need.position} className={styles.needItem}>
                    <div className={styles.needInfo}>
                      <span className={styles.needPos}>{need.position}</span>
                      <progress className={styles.needProgress} value={need.need_score} max={5} />
                    </div>
                    <span className={styles.needScore}>{need.need_score.toFixed(1)}</span>
                  </div>
                ))}
              </div>
            </BroadcastPanel>

            <BroadcastPanel title="War Room Controls">
              <div className={styles.controlsContainer}>
                <button
                  className={styles.actionButton}
                  onClick={handleSimulateDraft}
                  disabled={simulating || !currentPick}
                >
                  {simulating ? "Simulating..." : "Auto-Sim Draft"}
                </button>

                <button
                  className={styles.actionButton}
                  onClick={() => setShowTradeModal(true)}
                  disabled={!currentPick}
                >
                  Propose Trade
                </button>
              </div>
            </BroadcastPanel>
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
    </ParallaxScene>
  );
};
