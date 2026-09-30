import React, { useState, useEffect } from "react";
import {
  RefreshCw,
  ShieldCheck,
  Zap,
  CheckCircle2,
  AlertTriangle,
  ArrowRightLeft,
  Activity,
  Layers,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { rosterSyncApi } from "../../services/rosterSyncApi";
import type {
  ProviderStatus,
  ProvidersListResponse,
  SyncResult,
} from "../../services/rosterSyncApi";

export const LiveRosterSyncCard: React.FC = () => {
  const [status, setStatus] = useState<ProviderStatus | null>(null);
  const [providersInfo, setProvidersInfo] = useState<ProvidersListResponse | null>(null);
  const [selectedProvider, setSelectedProvider] = useState<string>("auto");
  const [loading, setLoading] = useState<boolean>(false);
  const [syncing, setSyncing] = useState<boolean>(false);
  const [lastResult, setLastResult] = useState<SyncResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<"transfers" | "depth" | "injuries">("transfers");

  const loadProviderStatus = async (provider?: string) => {
    try {
      setLoading(true);
      setError(null);
      const [statusRes, providersRes] = await Promise.all([
        rosterSyncApi.getStatus(provider === "auto" ? undefined : provider),
        rosterSyncApi.getProviders(),
      ]);
      setStatus(statusRes);
      setProvidersInfo(providersRes);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to query roster sync status.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProviderStatus();
  }, []);

  const handleSync = async (dryRun: boolean) => {
    try {
      setSyncing(true);
      setError(null);
      const result = await rosterSyncApi.executeSync(
        dryRun,
        selectedProvider === "auto" ? undefined : selectedProvider
      );
      setLastResult(result);
      setExpanded(true);
      // Reload provider status to update timestamp
      const updatedStatus = await rosterSyncApi.getStatus(
        selectedProvider === "auto" ? undefined : selectedProvider
      );
      setStatus(updatedStatus);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Roster synchronization failed.");
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl backdrop-blur-md text-slate-100">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-lg font-bold tracking-wide text-white">
                Live Roster Intelligence Sync
              </h3>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                <ShieldCheck className="w-3 h-3" />
                Differential Engine
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Pull authentic NFL trades, cuts, signings, depth orders, and injuries in real-time.
            </p>
          </div>
        </div>

        {/* Provider Selector & Refresh */}
        <div className="flex items-center gap-2">
          <select
            value={selectedProvider}
            onChange={(e) => {
              setSelectedProvider(e.target.value);
              loadProviderStatus(e.target.value);
            }}
            className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            disabled={loading || syncing}
          >
            <option value="auto">Auto-Select Provider</option>
            {providersInfo?.providers.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} {p.configured ? "✓" : "(Not Configured)"}
              </option>
            ))}
          </select>

          <button
            onClick={() => loadProviderStatus(selectedProvider)}
            disabled={loading || syncing}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors border border-slate-700"
            title="Refresh Provider Telemetry"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin text-emerald-400" : ""}`} />
          </button>
        </div>
      </div>

      {/* Provider Details Bar */}
      {status && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 my-4 bg-slate-950/60 p-3.5 rounded-lg border border-slate-800/80">
          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Active Provider
            </span>
            <span className="text-sm font-medium text-slate-200 mt-0.5 block truncate">
              {status.provider_name}
            </span>
          </div>

          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Authentication Key
            </span>
            <span className="text-sm font-mono text-emerald-400 mt-0.5 block">
              {status.masked_key || "None (Public Unauthenticated)"}
            </span>
          </div>

          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Last Sync Timestamp
            </span>
            <span className="text-sm text-slate-300 mt-0.5 block">
              {status.last_sync_timestamp
                ? new Date(status.last_sync_timestamp).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                  })
                : "Not Synced in Session"}
            </span>
          </div>
        </div>
      )}

      {/* Feature Badges */}
      {status && status.available_features && (
        <div className="flex flex-wrap gap-1.5 mb-4">
          {status.available_features.map((feat, i) => (
            <span
              key={i}
              className="text-[11px] px-2 py-0.5 rounded bg-slate-800/80 text-slate-400 border border-slate-700/60"
            >
              • {feat}
            </span>
          ))}
        </div>
      )}

      {/* Error Banner */}
      {error && (
        <div className="mb-4 p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Action Controls */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
        <div className="text-xs text-slate-400">
          Sync modifies team assignments and depth charts without resetting progression history.
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => handleSync(true)}
            disabled={syncing || loading}
            className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition flex items-center gap-1.5 disabled:opacity-50"
          >
            <Layers className="w-3.5 h-3.5 text-sky-400" />
            Preview Diffs (Dry Run)
          </button>

          <button
            onClick={() => handleSync(false)}
            disabled={syncing || loading}
            className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-lg shadow-emerald-900/30 transition flex items-center gap-1.5 disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${syncing ? "animate-spin" : ""}`} />
            {syncing ? "Syncing Gridiron Data..." : "Execute Live Sync"}
          </button>
        </div>
      </div>

      {/* Results Collapsible Panel */}
      {lastResult && (
        <div className="mt-4 pt-4 border-t border-slate-800">
          <button
            onClick={() => setExpanded(!expanded)}
            className="w-full flex items-center justify-between text-xs font-semibold text-slate-300 hover:text-white transition"
          >
            <span className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Sync Outcome: {lastResult.dry_run ? "[Preview Mode]" : "[Live Applied]"} (
              {lastResult.transfers_count} Transfers, {lastResult.depth_updates_count} Depth,{" "}
              {lastResult.injuries_count} Injuries)
            </span>
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {expanded && (
            <div className="mt-3 bg-slate-950/70 rounded-lg p-3 border border-slate-800">
              {/* Tabs */}
              <div className="flex gap-2 border-b border-slate-800 pb-2 mb-3">
                <button
                  onClick={() => setActiveTab("transfers")}
                  className={`text-xs px-2.5 py-1 rounded font-medium transition ${
                    activeTab === "transfers"
                      ? "bg-slate-800 text-emerald-400 font-semibold"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <ArrowRightLeft className="w-3 h-3 inline mr-1" />
                  Trades & Transfers ({lastResult.transfers_count})
                </button>
                <button
                  onClick={() => setActiveTab("depth")}
                  className={`text-xs px-2.5 py-1 rounded font-medium transition ${
                    activeTab === "depth"
                      ? "bg-slate-800 text-sky-400 font-semibold"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <Layers className="w-3 h-3 inline mr-1" />
                  Depth Changes ({lastResult.depth_updates_count})
                </button>
                <button
                  onClick={() => setActiveTab("injuries")}
                  className={`text-xs px-2.5 py-1 rounded font-medium transition ${
                    activeTab === "injuries"
                      ? "bg-slate-800 text-rose-400 font-semibold"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <Activity className="w-3 h-3 inline mr-1" />
                  Injuries ({lastResult.injuries_count})
                </button>
              </div>

              {/* Tab Contents */}
              {activeTab === "transfers" && (
                <div className="max-h-48 overflow-y-auto space-y-1.5 text-xs">
                  {lastResult.transfers.length === 0 ? (
                    <div className="text-slate-500 py-3 text-center">
                      No team movements detected. Rosters are fully synchronized with real NFL data.
                    </div>
                  ) : (
                    lastResult.transfers.map((t, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between p-2 rounded bg-slate-900/60 border border-slate-800"
                      >
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-slate-200">{t.player_name}</span>
                          <span className="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300">
                            {t.position}
                          </span>
                        </div>
                        <div className="flex items-center gap-1.5 text-slate-400 font-mono text-[11px]">
                          <span className="text-slate-400">{t.from_team}</span>
                          <ArrowRightLeft className="w-3 h-3 text-emerald-400" />
                          <span className="text-emerald-400 font-bold">{t.to_team}</span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {activeTab === "depth" && (
                <div className="max-h-48 overflow-y-auto space-y-1.5 text-xs">
                  {lastResult.depth_updates.length === 0 ? (
                    <div className="text-slate-500 py-3 text-center">
                      No depth chart movements detected.
                    </div>
                  ) : (
                    lastResult.depth_updates.map((d, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between p-2 rounded bg-slate-900/60 border border-slate-800"
                      >
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-slate-200">{d.player_name}</span>
                          <span className="text-slate-400 font-mono text-[11px]">
                            {d.team} • {d.position}
                          </span>
                        </div>
                        <div className="text-slate-300 text-[11px]">
                          Rank {d.old_rank} →{" "}
                          <span className="text-sky-400 font-bold">Rank {d.new_rank}</span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {activeTab === "injuries" && (
                <div className="max-h-48 overflow-y-auto space-y-1.5 text-xs">
                  {lastResult.injuries.length === 0 ? (
                    <div className="text-slate-500 py-3 text-center">
                      No active injury reports in feed.
                    </div>
                  ) : (
                    lastResult.injuries.map((inj, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between p-2 rounded bg-slate-900/60 border border-slate-800"
                      >
                        <span className="font-semibold text-slate-200">{inj.player_name}</span>
                        <div className="flex items-center gap-2">
                          <span className="text-slate-400">{inj.injury_type || "Injury"}</span>
                          <span className="px-1.5 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-300 font-bold border border-rose-500/30">
                            {inj.status}
                          </span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
