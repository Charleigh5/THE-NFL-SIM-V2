import React, { useState } from "react";
import {
  X,
  AlertOctagon,
  Shield,
  User,
  CheckCircle2,
  Send,
  Sparkles,
  Flame,
  Scale,
  Users2,
  ArrowRightLeft,
  ChevronRight,
} from "lucide-react";
import type {
  LockerRoomEventResponse,
  LockerRoomResolutionRequest,
  LockerRoomResolutionResponse,
  LockerRoomActionOption,
} from "../../types/society";

interface ClosedDoorCouncilModalProps {
  event: LockerRoomEventResponse;
  teamId: number;
  onClose: () => void;
  onResolve: (req: LockerRoomResolutionRequest) => Promise<LockerRoomResolutionResponse>;
}

export const ClosedDoorCouncilModal: React.FC<ClosedDoorCouncilModalProps> = ({
  event,
  teamId,
  onClose,
  onResolve,
}) => {
  const [selectedActionId, setSelectedActionId] = useState<string>("promise_usage");
  const [isResolving, setIsResolving] = useState<boolean>(false);
  const [resolutionResult, setResolutionResult] = useState<LockerRoomResolutionResponse | null>(
    null
  );

  // Fallback default action options if backend options empty
  const defaultActions: LockerRoomActionOption[] = [
    {
      id: "promise_usage",
      label: "Commit to Scripted Early Touches",
      description:
        "Direct offensive coordinator to script primary looks for aggrieved star in upcoming game.",
      projected_impact:
        "+12 Morale to star player, -5 Coach Authority, sets high target expectation.",
    },
    {
      id: "demand_accountability",
      label: "Enforce Coaching Authority & Discipline",
      description:
        "Back the head coach and demand conformity to offensive scheme or face reduction in snaps.",
      projected_impact: "+10 Coach Authority, -10 Morale to star player, tests mental resilience.",
    },
    {
      id: "players_meeting",
      label: "Mandate Closed-Door Players-Only Meeting",
      description:
        "Empower team captains to lead a players-only locker room alignment and air grievances.",
      projected_impact:
        "+5 Team Chemistry, -15 Tension for active roster, builds peer leadership cohesion.",
    },
    {
      id: "explore_trade",
      label: "Instruct Front Office to Field Trade Inquiries",
      description:
        "Quietly test league trade market before trade deadline to maximize asset return.",
      projected_impact:
        "Removes internal tension, alerts league GMs, prepares draft capital return.",
    },
  ];

  const actions = event.action_options?.length > 0 ? event.action_options : defaultActions;

  const handleApplyResolution = async () => {
    setIsResolving(true);
    try {
      const request: LockerRoomResolutionRequest = {
        team_id: teamId,
        action_id: selectedActionId,
        week: event.week,
        active_actor_ids: event.active_actors,
      };

      const result = await onResolve(request);
      setResolutionResult(result);
    } catch (err: unknown) {
      console.error("Failed to resolve locker room action:", err);
      setResolutionResult({
        team_id: teamId,
        action_id: selectedActionId,
        success: false,
        message:
          err instanceof Error
            ? err.message
            : "Failed to apply council resolution due to network error.",
        updated_chemistry: 50.0,
      });
    } finally {
      setIsResolving(false);
    }
  };

  const getRoleBadge = (role: string) => {
    switch (role) {
      case "disgruntled_star":
        return {
          label: "Aggrieved Athlete",
          color: "bg-red-500/20 text-red-300 border-red-500/40",
          icon: <Flame size={12} className="text-red-400" />,
        };
      case "team_captain":
        return {
          label: "Team Captain",
          color: "bg-amber-500/20 text-amber-300 border-amber-500/40",
          icon: <Shield size={12} className="text-amber-400" />,
        };
      case "head_coach":
      default:
        return {
          label: "Head Coach",
          color: "bg-blue-500/20 text-blue-300 border-blue-500/40",
          icon: <User size={12} className="text-blue-400" />,
        };
    }
  };

  const getActionIcon = (actionId: string) => {
    switch (actionId) {
      case "promise_usage":
        return <Sparkles size={16} className="text-emerald-400" />;
      case "demand_accountability":
        return <Scale size={16} className="text-amber-400" />;
      case "players_meeting":
        return <Users2 size={16} className="text-cyan-400" />;
      case "explore_trade":
        return <ArrowRightLeft size={16} className="text-red-400" />;
      default:
        return <ChevronRight size={16} className="text-white" />;
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4"
      data-testid="closed-door-council-modal"
      onClick={onClose}
    >
      <div
        className="broadcast-glass rounded-2xl border border-red-500/30 p-6 max-w-2xl w-full relative shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar"
        data-testid="council-modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white p-1.5 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          aria-label="Close council modal"
        >
          <X size={18} />
        </button>

        {/* Cinematic Header */}
        <div className="flex items-center gap-4 mb-6 pb-4 border-b border-white/10">
          <div className="w-14 h-14 rounded-xl bg-red-600/30 border border-red-500/50 flex items-center justify-center shadow-lg shrink-0">
            <AlertOctagon size={30} className="text-red-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-400 animate-pulse" />
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-red-400">
                Tier 3 Agentic Confrontation Council (Week {event.week})
              </span>
            </div>
            <h2 className="font-header text-2xl md:text-3xl text-white uppercase leading-tight mt-0.5">
              {event.headline}
            </h2>
            <p className="text-gray-400 text-xs font-mono mt-0.5">
              Closed-door multi-agent summit between Disgruntled Star, Captain & Head Coach
            </p>
          </div>
        </div>

        {/* Resolution Feedback Alert */}
        {resolutionResult && (
          <div
            className={`mb-6 p-4 rounded-xl border flex items-start gap-3 ${
              resolutionResult.success
                ? "bg-emerald-500/15 border-emerald-500/40 text-emerald-200"
                : "bg-red-500/15 border-red-500/40 text-red-200"
            }`}
          >
            <CheckCircle2 size={20} className="text-emerald-400 shrink-0 mt-0.5" />
            <div className="text-xs font-mono">
              <strong className="font-bold uppercase tracking-wider block mb-1">
                Directive Transmitted Successfully
              </strong>
              <p>{resolutionResult.message}</p>
              <div className="mt-2 text-[11px] text-emerald-300 font-bold">
                Updated Squad Chemistry: {resolutionResult.updated_chemistry.toFixed(1)} / 100
              </div>
            </div>
          </div>
        )}

        {/* Dramatic 3-Way Dialogue Transcript */}
        <div className="space-y-4 mb-6">
          <div className="flex items-center justify-between pb-1 border-b border-white/5 text-[11px] font-mono text-gray-400 uppercase tracking-wider">
            <span>Confrontation Transcript</span>
            <span>Hard Knocks Audio Feed</span>
          </div>

          <div className="space-y-3 max-h-72 overflow-y-auto pr-1 custom-scrollbar">
            {event.dialogue.map((turn, idx) => {
              const roleInfo = getRoleBadge(turn.speaker_role);
              const isStar = turn.speaker_role === "disgruntled_star";
              const isCoach = turn.speaker_role === "head_coach";

              return (
                <div
                  key={idx}
                  className={`p-3.5 rounded-xl border transition-all ${
                    isStar
                      ? "bg-red-950/40 border-red-500/20 mr-4"
                      : isCoach
                        ? "bg-blue-950/40 border-blue-500/20 ml-4"
                        : "bg-amber-950/40 border-amber-500/20 mx-2"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <div className="flex items-center gap-2">
                      <span className="font-header text-sm text-white uppercase tracking-tight">
                        {turn.speaker_name}
                      </span>
                      <span
                        className={`px-2 py-0.2 rounded text-[9px] font-mono uppercase tracking-wider border flex items-center gap-1 ${roleInfo.color}`}
                      >
                        {roleInfo.icon}
                        {roleInfo.label}
                      </span>
                    </div>
                  </div>
                  <p className="text-xs font-body text-gray-200 leading-relaxed italic">
                    "{turn.text}"
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* GM / Head Coach 4-Action Resolution Matrix */}
        {!resolutionResult && (
          <div className="space-y-4 pt-2 border-t border-white/10">
            <div className="flex justify-between items-center text-xs font-mono">
              <span className="text-gray-300 font-bold uppercase tracking-wider">
                Select Front Office Resolution Choice:
              </span>
              <span className="text-gray-400">4 Executive Pathways</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {actions.map((action) => {
                const isSelected = selectedActionId === action.id;
                const icon = getActionIcon(action.id);

                return (
                  <div
                    key={action.id}
                    onClick={() => setSelectedActionId(action.id)}
                    className={`p-3.5 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
                      isSelected
                        ? "bg-red-600/25 border-red-500/60 shadow-lg shadow-red-900/30 ring-1 ring-red-500/40"
                        : "bg-black/40 border-white/10 hover:border-white/20 hover:bg-white/5"
                    }`}
                  >
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        {icon}
                        <h4 className="font-header text-xs uppercase tracking-wider text-white">
                          {action.label}
                        </h4>
                      </div>
                      <p className="text-[11px] font-mono text-gray-300 leading-tight">
                        {action.description}
                      </p>
                    </div>

                    <div className="mt-2.5 pt-2 border-t border-white/10 text-[10px] font-mono text-amber-300">
                      <strong>Impact:</strong> {action.projected_impact}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-3">
              <button
                onClick={onClose}
                className="flex-1 py-2.5 bg-white/10 hover:bg-white/15 text-gray-300 font-header text-xs uppercase tracking-wider rounded-xl transition-all"
              >
                Table Discussion
              </button>

              <button
                onClick={handleApplyResolution}
                disabled={isResolving}
                className="flex-1 py-2.5 bg-gradient-to-r from-red-600 to-rose-700 hover:from-red-500 hover:to-rose-600 text-white font-header text-xs uppercase tracking-wider rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isResolving ? (
                  <span className="animate-pulse">Executing Directive...</span>
                ) : (
                  <>
                    <Send size={13} />
                    <span>Enforce Resolution</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Close Button once resolved */}
        {resolutionResult && (
          <div className="pt-4 flex justify-end">
            <button
              onClick={onClose}
              className="px-6 py-2.5 bg-gradient-to-r from-red-600 to-rose-700 text-white font-header text-xs uppercase tracking-wider rounded-xl shadow-lg"
            >
              Close Council Chamber
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClosedDoorCouncilModal;
