import React, { useState, useEffect, useCallback } from "react";
import {
  Flame,
  RefreshCw,
  MessageSquare,
  AlertTriangle,
  Network,
  Radio,
  Gauge,
} from "lucide-react";
import { LockerRoomTelemetry } from "../components/society/LockerRoomTelemetry";
import { ClosedDoorCouncilModal } from "../components/society/ClosedDoorCouncilModal";
import { LockerRoomGraphCanvas } from "../components/social/LockerRoomGraphCanvas";
import { MediaLeaksFeed } from "../components/social/MediaLeaksFeed";
import { HoldoutWarningBanner } from "../components/social/HoldoutWarningBanner";
import { societyApi } from "../services/societyApi";
import { socialGraphApi } from "../services/socialGraphApi";
import { api, type Player, type Team } from "../services/api";
import type {
  LockerRoomEventResponse,
  LockerRoomResolutionRequest,
  LockerRoomResolutionResponse,
} from "../types/society";
import type { LockerRoomSocialNetworkResponse, HoldoutAction } from "../types/socialGraph";

export const LockerRoom: React.FC = () => {
  const storedTeamId = localStorage.getItem("selectedTeamId");
  const teamId = storedTeamId ? parseInt(storedTeamId, 10) : 1;
  const currentWeek = 3;

  const [team, setTeam] = useState<Team | null>(null);
  const [roster, setRoster] = useState<Player[]>([]);
  const [teamTension, setTeamTension] = useState<number>(45.0);
  const [socialGraph, setSocialGraph] = useState<LockerRoomSocialNetworkResponse | null>(null);
  const [activeTab, setActiveTab] = useState<"graph" | "wire" | "telemetry">("graph");
  const [activeEvent, setActiveEvent] = useState<LockerRoomEventResponse | null>(null);
  const [isCouncilModalOpen, setIsCouncilModalOpen] = useState<boolean>(false);
  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);
  const [isResolvingHoldout, setIsResolvingHoldout] = useState<boolean>(false);
  const [evaluationFeedback, setEvaluationFeedback] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Load team roster, initial society status, and 2D social graph
  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [teamData, rosterData, graphData] = await Promise.all([
        api.getTeam(teamId),
        api.getTeamRoster(teamId),
        socialGraphApi.getSocialGraph(teamId).catch(() => null),
      ]);
      setTeam(teamData);
      setRoster(rosterData);
      if (graphData) {
        setSocialGraph(graphData);
      }

      // Compute average tension from roster if tension_score present
      if (rosterData.length > 0) {
        const scores = rosterData.map(
          (p) => (p as unknown as { tension_score?: number }).tension_score ?? 35.0
        );
        const avg = scores.reduce((sum, val) => sum + val, 0) / scores.length;
        setTeamTension(avg);
      }
    } catch (err: unknown) {
      console.error("Error loading locker room data:", err);
    } finally {
      setLoading(false);
    }
  }, [teamId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Run Tier 2 Gate Evaluation via Society Engine
  const handleRunEvaluation = async () => {
    setIsEvaluating(true);
    setEvaluationFeedback(null);
    try {
      const event = await societyApi.evaluateLockerRoom(teamId, currentWeek);

      if (event) {
        setActiveEvent(event);
        setIsCouncilModalOpen(true);
        setTeamTension((prev) => Math.max(76.0, prev + 15.0));
        setEvaluationFeedback(
          `Tier 2 Gate Triggered! Active tension exceeded 75.0: "${event.headline}"`
        );
      } else {
        setActiveEvent(null);
        setEvaluationFeedback(
          "Tier 2 Gate Bypass (0ms): All player tension values are below 75.0. Locker room is harmonious."
        );
      }

      // Refresh social graph after evaluation
      const refreshedGraph = await socialGraphApi.getSocialGraph(teamId).catch(() => null);
      if (refreshedGraph) setSocialGraph(refreshedGraph);
    } catch (err: unknown) {
      console.error("Evaluation error:", err);
      // Fallback synthetic demonstration event for testing
      const fallbackEvent: LockerRoomEventResponse = {
        team_id: teamId,
        week: currentWeek,
        active_actors: [roster[0]?.id || 1],
        captain_id: roster[1]?.id || 2,
        headline: "Locker Room Friction: Disgruntled Receiver Questions Target Share",
        dialogue: [
          {
            speaker_name: roster[0]
              ? `${roster[0].first_name} ${roster[0].last_name}`
              : "Star Player",
            speaker_role: "disgruntled_star",
            speaker_id: roster[0]?.id || 1,
            text: "Coach, I didn't work all offseason to run decoy clear-outs. I need the ball in my hands to win games, and two targets in the second half isn't going to cut it.",
          },
          {
            speaker_name: "Coach",
            speaker_role: "head_coach",
            speaker_id: null,
            text: "We called the plays that gave us the best look against their Cover-3. When you start freelancing routes, it breaks the entire progression for the quarterback.",
          },
          {
            speaker_name: roster[1]
              ? `${roster[1].first_name} ${roster[1].last_name}`
              : "Team Captain",
            speaker_role: "team_captain",
            speaker_id: roster[1]?.id || 2,
            text: "Look, we all want the rock, but film doesn't lie. When we execute the concept as installed, the offense moves. Let's keep the focus between these four walls.",
          },
          {
            speaker_name: roster[0]
              ? `${roster[0].first_name} ${roster[0].last_name}`
              : "Star Player",
            speaker_role: "disgruntled_star",
            speaker_id: roster[0]?.id || 1,
            text: "I respect you, Cap, but my playmaking speaks for itself. If we want to make the postseason, the ball has to come through me.",
          },
        ],
        consequences: {
          morale_deltas: { "1": -8 },
          trust_coach_deltas: { "1": -12 },
          trust_qb_deltas: { "1": -10 },
          trade_requested: false,
          team_chemistry_delta: -8.0,
          drama_headline: "Locker Room Friction Over Target Distribution",
        },
        action_options: [
          {
            id: "promise_usage",
            label: "Commit to Scripted Early Touches",
            description: "Direct offensive coordinator to script primary looks for star player.",
            projected_impact:
              "+12 Morale to star player, -5 Coach Authority, sets high target expectation.",
          },
          {
            id: "demand_accountability",
            label: "Enforce Coaching Authority & Discipline",
            description:
              "Back the head coach and demand conformity to offensive scheme or face benching.",
            projected_impact: "+10 Coach Authority, -10 Morale to star player, tests resilience.",
          },
          {
            id: "players_meeting",
            label: "Mandate Closed-Door Players-Only Meeting",
            description: "Empower team captains to lead a players-only alignment session.",
            projected_impact:
              "+5 Team Chemistry, -15 Tension for active roster, builds peer leadership.",
          },
          {
            id: "explore_trade",
            label: "Instruct Front Office to Field Trade Inquiries",
            description: "Quietly test league trade market before trade deadline.",
            projected_impact:
              "Removes internal tension, alerts league GMs, prepares draft capital return.",
          },
        ],
        summary:
          "Primary offensive weapon expressed serious frustration regarding scheme and target share.",
      };

      setActiveEvent(fallbackEvent);
      setIsCouncilModalOpen(true);
      setTeamTension(82.0);
    } finally {
      setIsEvaluating(false);
    }
  };

  // Resolution Callback for Closed Door Council
  const handleResolve = async (
    req: LockerRoomResolutionRequest
  ): Promise<LockerRoomResolutionResponse> => {
    try {
      const response = await societyApi.resolveLockerRoom(teamId, req);
      setTeamTension((prev) => Math.max(20, prev - 25));
      setEvaluationFeedback(`Resolved with: ${req.action_id}. ${response.message}`);

      // Refresh social graph to reflect new tension
      const refreshedGraph = await socialGraphApi.getSocialGraph(teamId).catch(() => null);
      if (refreshedGraph) setSocialGraph(refreshedGraph);

      return response;
    } catch {
      // Deterministic offline fallback resolution
      setTeamTension((prev) => Math.max(25, prev - 20));
      return {
        team_id: teamId,
        action_id: req.action_id,
        success: true,
        message: `Front office directive applied. Squad chemistry stabilized.`,
        updated_chemistry: 72.0,
      };
    }
  };

  // Resolve Active Athlete Holdout
  const handleResolveHoldout = async (playerId: number, action: HoldoutAction) => {
    setIsResolvingHoldout(true);
    try {
      const updatedGraph = await socialGraphApi.resolveHoldout(teamId, playerId, { action });
      setSocialGraph(updatedGraph);
      setTeamTension(Math.max(15, 100.0 - updatedGraph.team_morale_index));
      setEvaluationFeedback(
        `GM Decision Applied: ${action.replace("_", " ")} on athlete #${playerId}. Locker room dynamics recalculated.`
      );
    } catch (err: unknown) {
      console.error("Failed to resolve holdout:", err);
      setEvaluationFeedback("Failed to submit holdout resolution to server.");
    } finally {
      setIsResolvingHoldout(false);
    }
  };

  // Simulate Star Holdout for Testing
  const handleSeedHoldout = async () => {
    const candidate = roster[0] || (socialGraph?.nodes[0] ? { id: socialGraph.nodes[0].id } : null);
    if (!candidate) return;

    setIsResolvingHoldout(true);
    try {
      const updatedGraph = await socialGraphApi.seedHoldout(teamId, candidate.id);
      setSocialGraph(updatedGraph);
      setTeamTension(Math.max(78.0, 100.0 - updatedGraph.team_morale_index));
      setEvaluationFeedback(
        `Simulated Holdout Activated: Athlete #${candidate.id} has initiated contract boycott.`
      );
    } catch (err: unknown) {
      console.error("Failed to seed holdout:", err);
    } finally {
      setIsResolvingHoldout(false);
    }
  };

  const holdoutNodes = socialGraph?.nodes.filter((n) => n.is_holding_out) || [];

  if (loading) {
    return (
      <div className="text-white p-8 flex items-center justify-center min-h-[50vh]">
        <span className="font-header text-2xl uppercase tracking-wider text-gray-400 animate-pulse">
          Loading Locker Room Dynamics &amp; Social Network...
        </span>
      </div>
    );
  }

  return (
    <div className="space-y-6 font-body" data-testid="locker-room-page">
      {/* Top Header Banner */}
      <header className="relative rounded-2xl overflow-hidden broadcast-glass p-6 border border-white/15 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-xl bg-black/60 border-2 border-white/15 p-2 shadow-xl flex items-center justify-center shrink-0">
            <Flame className="text-red-400" size={32} />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-400 animate-pulse" />
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-red-400">
                Society Engine • Tier 1 Differential &amp; Tier 3 Council
              </span>
            </div>
            <h1 className="text-3xl md:text-5xl font-header uppercase tracking-tight text-white leading-none mt-0.5">
              Locker Room: {team?.city} {team?.name}
            </h1>
            <p className="text-gray-400 text-xs font-mono mt-1">
              Social Topology, Morale Chemistry, Holdout Mechanics &amp; Media Leaks
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleRunEvaluation}
            disabled={isEvaluating}
            className="px-4 py-2.5 bg-white/10 hover:bg-white/15 text-gray-200 hover:text-white font-header text-xs uppercase tracking-wider rounded-xl border border-white/10 transition-all flex items-center gap-2 active:scale-95 disabled:opacity-50"
          >
            <RefreshCw size={14} className={isEvaluating ? "animate-spin" : ""} />
            <span>Evaluate Atmosphere</span>
          </button>

          {activeEvent && (
            <button
              onClick={() => setIsCouncilModalOpen(true)}
              className="px-5 py-2.5 bg-gradient-to-r from-red-600 to-rose-700 hover:from-red-500 hover:to-rose-600 text-white font-header text-xs uppercase tracking-wider rounded-xl shadow-lg transition-all flex items-center gap-2 active:scale-95 animate-pulse"
            >
              <MessageSquare size={14} />
              <span>Convene Council</span>
            </button>
          )}
        </div>
      </header>

      {/* Critical Holdout Alert Banner (Gated on is_holding_out) */}
      <HoldoutWarningBanner
        holdoutNodes={holdoutNodes}
        onResolveHoldout={handleResolveHoldout}
        onSeedHoldout={handleSeedHoldout}
        isResolving={isResolvingHoldout}
      />

      {/* Evaluation Feedback Message Banner */}
      {evaluationFeedback && (
        <div className="p-3.5 rounded-xl bg-slate-900/90 border border-white/10 text-xs font-mono text-gray-300 flex items-center gap-2">
          <AlertTriangle size={15} className="text-yellow-400 shrink-0" />
          <span>{evaluationFeedback}</span>
        </div>
      )}

      {/* Navigation Sub-Tabs */}
      <div className="flex items-center gap-2 border-b border-white/10 pb-2">
        <button
          onClick={() => setActiveTab("graph")}
          className={`px-4 py-2 rounded-xl text-xs font-header uppercase tracking-wider transition-all flex items-center gap-2 ${
            activeTab === "graph"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-lg"
              : "text-gray-400 hover:text-white hover:bg-white/5"
          }`}
        >
          <Network size={15} />
          <span>Social Network Topology</span>
          {socialGraph && (
            <span className="px-1.5 py-0.5 rounded-full bg-black/40 text-[10px] font-mono text-cyan-400">
              {socialGraph.nodes.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab("wire")}
          className={`px-4 py-2 rounded-xl text-xs font-header uppercase tracking-wider transition-all flex items-center gap-2 ${
            activeTab === "wire"
              ? "bg-red-500/20 text-red-300 border border-red-500/40 shadow-lg"
              : "text-gray-400 hover:text-white hover:bg-white/5"
          }`}
        >
          <Radio
            size={15}
            className={socialGraph?.active_leaks?.length ? "text-red-400 animate-pulse" : ""}
          />
          <span>Media Leaks Wire</span>
          {socialGraph && socialGraph.active_leaks.length > 0 && (
            <span className="px-1.5 py-0.5 rounded-full bg-red-500 text-[10px] font-mono text-white font-bold">
              {socialGraph.active_leaks.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab("telemetry")}
          className={`px-4 py-2 rounded-xl text-xs font-header uppercase tracking-wider transition-all flex items-center gap-2 ${
            activeTab === "telemetry"
              ? "bg-purple-500/20 text-purple-300 border border-purple-500/40 shadow-lg"
              : "text-gray-400 hover:text-white hover:bg-white/5"
          }`}
        >
          <Gauge size={15} />
          <span>Atmosphere Telemetry &amp; Council</span>
        </button>
      </div>

      {/* Tab 1: 2D Social Network Graph Canvas */}
      {activeTab === "graph" && socialGraph && (
        <LockerRoomGraphCanvas
          nodes={socialGraph.nodes}
          edges={socialGraph.edges}
          cliques={socialGraph.cliques}
        />
      )}

      {/* Tab 2: Media Leaks Wire */}
      {activeTab === "wire" && socialGraph && <MediaLeaksFeed leaks={socialGraph.active_leaks} />}

      {/* Tab 3: Locker Room Telemetry Component */}
      {activeTab === "telemetry" && (
        <LockerRoomTelemetry
          teamTension={teamTension}
          roster={roster}
          activeEvent={activeEvent}
          onOpenCouncil={() => setIsCouncilModalOpen(true)}
          onRunEvaluation={handleRunEvaluation}
          isEvaluating={isEvaluating}
        />
      )}

      {/* Closed-Door Council Modal */}
      {isCouncilModalOpen && activeEvent && (
        <ClosedDoorCouncilModal
          event={activeEvent}
          teamId={teamId}
          onClose={() => setIsCouncilModalOpen(false)}
          onResolve={handleResolve}
        />
      )}
    </div>
  );
};

export default LockerRoom;
