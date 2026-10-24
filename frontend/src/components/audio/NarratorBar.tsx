import { useEffect, useState, useCallback, useRef } from "react";
import { useLocation, useParams } from "react-router-dom";
import { Radio, Volume2, VolumeX, Sparkles, ChevronDown, ChevronUp, Square } from "lucide-react";
import { useShallow } from "zustand/react/shallow";
import { useAudio } from "../../context/useAudio";
import { useNarratorStore } from "../../store/useNarratorStore";
import { playNarrationResponse, stopNarrationPlayback } from "../../services/narratorAudioDriver";
import type { BroadcastStyle, PageRouteKey } from "../../types/narrator";

const ROUTE_TO_PAGE_KEY: Record<string, PageRouteKey> = {
  "": "dashboard",
  dashboard: "dashboard",
  season: "season",
  "season-dashboard": "season",
  offseason: "offseason",
  "offseason-dashboard": "offseason",
  "free-agency": "free-agency",
  draft: "draft",
  "front-office": "front-office",
  roster: "front-office",
  "depth-chart": "depth-chart",
  "trade-center": "trade-center",
  trades: "trade-center",
  "trophy-room": "trophy-room",
  "live-sim": "live-sim",
  "medical-center": "medical-center",
  medical: "medical-center",
  "locker-room": "locker-room",
  playbook: "playbook",
  training: "training",
  skills: "skills",
};

function resolvePageRouteKey(pathname: string): PageRouteKey {
  const segments = pathname.split("/").filter(Boolean);
  for (let i = segments.length - 1; i >= 0; i -= 1) {
    const match = ROUTE_TO_PAGE_KEY[segments[i]];
    if (match) {
      return match;
    }
  }
  return "dashboard";
}

function resolveCurrentTeamId(): number {
  if (typeof window === "undefined") return 1;
  const raw = window.localStorage.getItem("selectedTeamId");
  const parsed = raw ? parseInt(raw, 10) : NaN;
  return Number.isFinite(parsed) && parsed >= 1 ? parsed : 1;
}

const BROADCAST_STYLES: { id: BroadcastStyle; label: string }[] = [
  { id: "ESPN", label: "ESPN" },
  { id: "CBS", label: "CBS" },
  { id: "FOX", label: "FOX" },
  { id: "NFL_NETWORK", label: "NFL Network" },
];

export const NarratorBar: React.FC = () => {
  const location = useLocation();
  const params = useParams<{ playerId?: string }>();
  const { duckVolume, restoreVolume } = useAudio();

  const {
    enabled,
    autoNarrate,
    isMuted,
    style,
    isLoading,
    isSpeaking,
    currentNarration,
    voiceSource,
    needsUserGesture,
    setAutoNarrate,
    toggleMute,
    setStyle,
    setSpeaking,
    setNeedsUserGesture,
    cancelActiveRequest,
    requestNarration,
  } = useNarratorStore(
    useShallow((state) => ({
      enabled: state.enabled,
      autoNarrate: state.autoNarrate,
      isMuted: state.isMuted,
      style: state.style,
      isLoading: state.isLoading,
      isSpeaking: state.isSpeaking,
      currentNarration: state.currentNarration,
      voiceSource: state.voiceSource,
      needsUserGesture: state.needsUserGesture,
      setAutoNarrate: state.setAutoNarrate,
      toggleMute: state.toggleMute,
      setStyle: state.setStyle,
      setSpeaking: state.setSpeaking,
      setNeedsUserGesture: state.setNeedsUserGesture,
      cancelActiveRequest: state.cancelActiveRequest,
      requestNarration: state.requestNarration,
    }))
  );

  const [captionExpanded, setCaptionExpanded] = useState(true);
  const autoDebounceRef = useRef<number | null>(null);

  const triggerScreenNarration = useCallback(async () => {
    if (!enabled) return;
    stopNarrationPlayback();
    restoreVolume();

    const pageKey = resolvePageRouteKey(location.pathname);
    const teamId = resolveCurrentTeamId();
    const parsedPlayerId = params.playerId ? parseInt(params.playerId, 10) : NaN;
    const playerId = Number.isFinite(parsedPlayerId) && parsedPlayerId >= 1 ? parsedPlayerId : null;

    const response = await requestNarration({
      page: pageKey,
      team_id: teamId,
      player_id: playerId,
      style,
    });

    if (!response) {
      return;
    }

    setCaptionExpanded(true);
    await playNarrationResponse(response, {
      isMuted: useNarratorStore.getState().isMuted,
      onStart: () => {
        setNeedsUserGesture(false);
        setSpeaking(true);
        duckVolume(0.2);
      },
      onEnd: () => {
        setSpeaking(false);
        restoreVolume();
      },
      onNeedsUserGesture: () => {
        setNeedsUserGesture(true);
      },
    });
  }, [
    duckVolume,
    enabled,
    location.pathname,
    params.playerId,
    requestNarration,
    restoreVolume,
    setNeedsUserGesture,
    setSpeaking,
    style,
  ]);

  // Cancel stale audio/requests on route navigation & trigger 800ms debounced Auto-Narrate if enabled
  useEffect(() => {
    if (autoDebounceRef.current !== null) {
      window.clearTimeout(autoDebounceRef.current);
      autoDebounceRef.current = null;
    }

    cancelActiveRequest();
    stopNarrationPlayback();
    restoreVolume();

    if (enabled && autoNarrate) {
      autoDebounceRef.current = window.setTimeout(() => {
        void triggerScreenNarration();
      }, 800);
    }

    return () => {
      if (autoDebounceRef.current !== null) {
        window.clearTimeout(autoDebounceRef.current);
      }
    };
  }, [
    location.pathname,
    enabled,
    autoNarrate,
    cancelActiveRequest,
    restoreVolume,
    triggerScreenNarration,
  ]);

  const handleStop = () => {
    cancelActiveRequest();
    stopNarrationPlayback();
    restoreVolume();
  };

  return (
    <aside
      data-testid="narrator-bar"
      aria-label="Broadcast Desk Narrator"
      className="fixed bottom-4 left-24 md:left-[17rem] z-40 w-fit max-w-[calc(100vw-18rem)] rounded-[2px] border border-white/15 bg-slate-950/95 backdrop-blur-md shadow-2xl text-white px-3 py-2 transition-all"
    >
      <div className="flex items-center gap-2 whitespace-nowrap">
        <div className="flex items-center gap-1.5 pr-1">
          <Radio
            size={15}
            className={isSpeaking ? "text-red-500 animate-pulse" : "text-amber-400"}
          />
          <span className="text-[11px] font-bold tracking-wider uppercase text-slate-200">
            Broadcast Desk
          </span>
        </div>

        <button
          type="button"
          data-testid="narrator-trigger-btn"
          onClick={() => void triggerScreenNarration()}
          disabled={isLoading}
          className="inline-flex items-center gap-1.5 rounded-[2px] bg-amber-500 hover:bg-amber-400 disabled:opacity-60 text-slate-950 font-bold text-xs px-2.5 py-1 transition-colors cursor-pointer"
        >
          <Sparkles size={12} />
          {isLoading ? "On Air..." : "Narrate Screen"}
        </button>

        {isSpeaking && (
          <button
            type="button"
            data-testid="narrator-stop-btn"
            onClick={handleStop}
            aria-label="Stop narration"
            className="inline-flex items-center gap-1 rounded-[2px] bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 text-red-200 text-xs px-2 py-1 cursor-pointer"
          >
            <Square size={10} />
            Stop
          </button>
        )}

        <label
          htmlFor="narrator-auto-toggle"
          className="inline-flex items-center gap-1.5 text-xs text-slate-300 select-none cursor-pointer"
        >
          <input
            id="narrator-auto-toggle"
            name="narratorAutoNarrate"
            type="checkbox"
            data-testid="narrator-auto-toggle"
            checked={autoNarrate}
            onChange={(e) => setAutoNarrate(e.target.checked)}
            className="rounded border-slate-600 bg-slate-800 text-amber-500 focus:ring-amber-500"
          />
          Auto-Narrate
        </label>

        <select
          id="narrator-style-select"
          name="narratorBroadcastStyle"
          data-testid="narrator-style-select"
          aria-label="Broadcast Network Style"
          value={style}
          onChange={(e) => setStyle(e.target.value as BroadcastStyle)}
          className="rounded-[2px] border border-white/15 bg-slate-900 text-xs font-semibold text-slate-100 px-2 py-1 focus:outline-none focus:border-amber-400"
        >
          {BROADCAST_STYLES.map((opt) => (
            <option key={opt.id} value={opt.id}>
              {opt.label}
            </option>
          ))}
        </select>

        <span
          data-testid="narrator-voice-badge"
          className={`inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-semibold border ${
            voiceSource === "voicestudio"
              ? "bg-emerald-500/15 text-emerald-300 border-emerald-500/30"
              : "bg-sky-500/15 text-sky-300 border-sky-500/30"
          }`}
        >
          {voiceSource === "voicestudio" ? "Studio AI" : "Browser Voice"}
        </span>

        <button
          type="button"
          data-testid="narrator-mute-btn"
          onClick={toggleMute}
          aria-label={isMuted ? "Unmute narrator" : "Mute narrator"}
          className="p-1 rounded-[2px] hover:bg-white/10 text-slate-300 cursor-pointer inline-flex items-center justify-center"
        >
          {isMuted ? <VolumeX size={14} /> : <Volume2 size={14} />}
        </button>

        {currentNarration && (
          <button
            type="button"
            data-testid="narrator-caption-toggle"
            onClick={() => setCaptionExpanded((prev) => !prev)}
            aria-label={captionExpanded ? "Hide script caption" : "Show script caption"}
            className="p-1 rounded-[2px] hover:bg-white/10 text-slate-400 cursor-pointer ml-auto inline-flex items-center justify-center"
          >
            {captionExpanded ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
          </button>
        )}
      </div>

      {needsUserGesture && (
        <div
          data-testid="narrator-gesture-notice"
          className="mt-1.5 text-[11px] text-amber-300 font-medium"
        >
          Click &ldquo;Narrate Screen&rdquo; to enable browser audio playback.
        </div>
      )}

      {currentNarration && captionExpanded && (
        <div
          data-testid="narrator-caption-panel"
          className="mt-2 pt-2 border-t border-white/10 space-y-1 max-w-xl"
        >
          <div
            data-testid="narrator-headline-banner"
            className="text-[11px] font-bold tracking-wider uppercase text-amber-400"
          >
            {currentNarration.headline_banner}
          </div>
          <p data-testid="narrator-script-text" className="text-xs leading-relaxed text-slate-200">
            {currentNarration.script}
          </p>
        </div>
      )}
    </aside>
  );
};

export default NarratorBar;
