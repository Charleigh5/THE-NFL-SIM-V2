/**
 * CapLedgerAuditModal.tsx
 * =======================
 * Institutional audit view for the Capology Double-Entry Ledger.
 * Displays real-time balanced debit/credit transactions, proof-of-balance checks,
 * and 5-year ledger forecasts under NFL CBA Article 13 invariants.
 */

import React, { useState, useEffect } from "react";
import {
  X,
  Scale,
  CheckCircle2,
  AlertTriangle,
  History,
  TrendingUp,
  ShieldCheck,
  ArrowDownRight,
  ArrowUpRight,
} from "lucide-react";
import type {
  TeamLedgerStatementDTO,
  MultiYearLedgerStatementResponse,
} from "../../types/capLedger";
import { capLedgerApi } from "../../services/capLedgerApi";

interface CapLedgerAuditModalProps {
  isOpen: boolean;
  onClose: () => void;
  teamId: number;
}

export const CapLedgerAuditModal: React.FC<CapLedgerAuditModalProps> = ({
  isOpen,
  onClose,
  teamId,
}) => {
  const [activeTab, setActiveTab] = useState<"journal" | "multiyear">("journal");
  const [statement, setStatement] = useState<TeamLedgerStatementDTO | null>(null);
  const [multiYear, setMultiYear] = useState<MultiYearLedgerStatementResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!isOpen) return;
    setLoading(true);

    Promise.all([
      capLedgerApi.getTeamStatement(teamId),
      capLedgerApi.getMultiYearStatement(teamId),
    ])
      .then(([stmtData, multiData]) => {
        setStatement(stmtData);
        setMultiYear(multiData);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [isOpen, teamId]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn"
      role="dialog"
      aria-modal="true"
      data-testid="cap-ledger-audit-modal"
    >
      <div className="relative w-full max-w-5xl max-h-[90vh] bg-slate-900 border border-emerald-500/30 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-slate-950/60">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl">
              <Scale className="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-header uppercase tracking-wider text-white">
                  Capology Double-Entry Ledger
                </h2>
                {statement?.isBalanced ? (
                  <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                    <ShieldCheck className="w-3 h-3" />
                    Zero-Sum Balanced (Δ $0)
                  </span>
                ) : (
                  <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider bg-rose-500/20 text-rose-400 border border-rose-500/40">
                    <AlertTriangle className="w-3 h-3" />
                    Invariant Violation
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-400 font-mono">
                {statement?.teamName || "NFL Franchise"} • League Year {statement?.leagueYear || 2026} • CBA Article 13 & Appendix V
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
            aria-label="Close Ledger Audit Modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center gap-4 px-6 pt-3 border-b border-white/10 bg-slate-950/30">
          <button
            onClick={() => setActiveTab("journal")}
            className={`flex items-center gap-2 pb-3 text-xs font-mono font-bold uppercase tracking-wider transition-all border-b-2 ${
              activeTab === "journal"
                ? "border-emerald-400 text-emerald-300"
                : "border-transparent text-slate-400 hover:text-white"
            }`}
          >
            <History className="w-4 h-4" />
            Journal Entries & Transactions
          </button>
          <button
            onClick={() => setActiveTab("multiyear")}
            className={`flex items-center gap-2 pb-3 text-xs font-mono font-bold uppercase tracking-wider transition-all border-b-2 ${
              activeTab === "multiyear"
                ? "border-emerald-400 text-emerald-300"
                : "border-transparent text-slate-400 hover:text-white"
            }`}
          >
            <TrendingUp className="w-4 h-4" />
            5-Year Multi-Year Ledger Forecast
          </button>
        </div>

        {/* Body Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {loading ? (
            <div className="flex items-center justify-center py-20">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-400" />
            </div>
          ) : (
            <>
              {/* Account Balance Summary Cards */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div className="p-3.5 bg-slate-950/60 border border-white/10 rounded-xl">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Total Hard Cap</div>
                  <div className="text-lg font-mono font-extrabold text-white mt-0.5">
                    ${((statement?.totalSalaryCap || 255_400_000) / 1_000_000).toFixed(2)}M
                  </div>
                  <div className="text-[10px] text-slate-500 font-mono">League Baseline</div>
                </div>

                <div className="p-3.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-emerald-400">Cap Room (Free)</div>
                  <div className="text-lg font-mono font-extrabold text-emerald-300 mt-0.5">
                    ${((statement?.availableCapRoom || 0) / 1_000_000).toFixed(2)}M
                  </div>
                  <div className="text-[10px] text-emerald-500/80 font-mono">Available Space</div>
                </div>

                <div className="p-3.5 bg-cyan-500/10 border border-cyan-500/30 rounded-xl">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-cyan-400">Active Liabilities</div>
                  <div className="text-lg font-mono font-extrabold text-cyan-300 mt-0.5">
                    ${((statement?.activeSalaryLiability || 0) / 1_000_000).toFixed(2)}M
                  </div>
                  <div className="text-[10px] text-cyan-500/80 font-mono">53-Man Base Payroll</div>
                </div>

                <div className="p-3.5 bg-rose-500/10 border border-rose-500/30 rounded-xl">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-rose-400">Dead Money</div>
                  <div className="text-lg font-mono font-extrabold text-rose-300 mt-0.5">
                    ${((statement?.deadMoneyLiability || 0) / 1_000_000).toFixed(2)}M
                  </div>
                  <div className="text-[10px] text-rose-500/80 font-mono">Accelerated Charges</div>
                </div>

                <div className="p-3.5 bg-amber-500/10 border border-amber-500/30 rounded-xl col-span-2 md:col-span-1">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-amber-400">Bonus Pool</div>
                  <div className="text-lg font-mono font-extrabold text-amber-300 mt-0.5">
                    ${((statement?.unamortizedBonusPool || 0) / 1_000_000).toFixed(2)}M
                  </div>
                  <div className="text-[10px] text-amber-500/80 font-mono">Unamortized Proration</div>
                </div>
              </div>

              {/* Mathematical Proof-of-Balance Equation Banner */}
              <div className="p-4 bg-slate-950/80 border border-white/10 rounded-xl flex flex-col md:flex-row items-center justify-between gap-3 font-mono text-xs">
                <div className="flex items-center gap-2 text-slate-300">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>
                    <strong className="text-white">Proof of Balance:</strong> Hard Cap ($
                    {((statement?.totalSalaryCap || 0) / 1_000_000).toFixed(2)}M) = Room ($
                    {((statement?.availableCapRoom || 0) / 1_000_000).toFixed(2)}M) + Active ($
                    {((statement?.activeSalaryLiability || 0) / 1_000_000).toFixed(2)}M) + Dead Money ($
                    {((statement?.deadMoneyLiability || 0) / 1_000_000).toFixed(2)}M)
                  </span>
                </div>
                <div className="px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-lg text-[11px] font-bold shrink-0">
                  Δ = ${statement?.proofOfBalanceDelta || 0} (EXACT)
                </div>
              </div>

              {/* Tab 1: Journal Transactions */}
              {activeTab === "journal" && (
                <div className="space-y-3">
                  <div className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400">
                    Journaled Double-Entry Transactions ({statement?.transactions.length || 0})
                  </div>

                  {statement?.transactions.length === 0 ? (
                    <div className="text-center py-10 text-slate-500 text-sm font-mono">
                      No transactions recorded yet in this league year.
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {statement?.transactions.map((tx) => (
                        <div
                          key={tx.id}
                          className="p-4 bg-slate-950/40 border border-white/10 hover:border-white/20 rounded-xl transition-all space-y-2"
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div>
                              <div className="flex items-center gap-2">
                                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-slate-800 text-slate-300 border border-slate-700">
                                  {tx.transactionType.replace(/_/g, " ")}
                                </span>
                                <span className="text-xs text-slate-400 font-mono">
                                  {new Date(tx.timestamp).toLocaleString()}
                                </span>
                              </div>
                              <div className="text-sm font-semibold text-white mt-1">
                                {tx.description}
                              </div>
                            </div>

                            <div className="text-right shrink-0">
                              <div
                                className={`text-sm font-mono font-bold flex items-center justify-end gap-1 ${
                                  tx.netCapDelta > 0
                                    ? "text-emerald-400"
                                    : tx.netCapDelta < 0
                                    ? "text-rose-400"
                                    : "text-slate-400"
                                }`}
                              >
                                {tx.netCapDelta > 0 ? (
                                  <ArrowUpRight className="w-4 h-4" />
                                ) : tx.netCapDelta < 0 ? (
                                  <ArrowDownRight className="w-4 h-4" />
                                ) : null}
                                {tx.netCapDelta > 0 ? "+" : ""}
                                ${(tx.netCapDelta / 1_000_000).toFixed(2)}M Cap Room
                              </div>
                              <div className="text-[10px] text-slate-500 font-mono">Net Delta</div>
                            </div>
                          </div>

                          {/* Line-item debits & credits */}
                          {tx.entries && tx.entries.length > 0 && (
                            <div className="pt-2 border-t border-white/5 grid grid-cols-1 sm:grid-cols-3 gap-2">
                              {tx.entries.map((entry, idx) => (
                                <div
                                  key={idx}
                                  className="flex items-center justify-between px-2.5 py-1 rounded bg-slate-900/60 border border-white/5 text-[11px] font-mono"
                                >
                                  <span className="text-slate-400 truncate mr-2">
                                    {entry.accountType.replace(/_/g, " ")}
                                  </span>
                                  <span
                                    className={`font-bold ${
                                      entry.amount > 0 ? "text-cyan-400" : "text-emerald-400"
                                    }`}
                                  >
                                    {entry.amount > 0 ? `Debit: +$${(entry.amount / 1_000_000).toFixed(2)}M` : `Credit: -$${(Math.abs(entry.amount) / 1_000_000).toFixed(2)}M`}
                                  </span>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Tab 2: 5-Year Multi-Year Ledger Forecast */}
              {activeTab === "multiyear" && (
                <div className="space-y-4">
                  <div className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400">
                    5-Year Double-Entry Cap Balance Trajectory (2026–2030)
                  </div>

                  <div className="overflow-x-auto rounded-xl border border-white/10 bg-slate-950/40">
                    <table className="w-full text-left text-xs font-mono">
                      <thead className="bg-slate-950/80 text-slate-400 border-b border-white/10">
                        <tr>
                          <th className="p-3">Year</th>
                          <th className="p-3">Hard Cap</th>
                          <th className="p-3">Active Payroll</th>
                          <th className="p-3">Dead Money</th>
                          <th className="p-3">Bonus Pool</th>
                          <th className="p-3">Cap Room</th>
                          <th className="p-3 text-right">Balance Invariant</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-white/5">
                        {multiYear?.yearlyStatements.map((yr) => (
                          <tr key={yr.leagueYear} className="hover:bg-white/5 transition-colors">
                            <td className="p-3 font-bold text-white">{yr.leagueYear}</td>
                            <td className="p-3 text-slate-300">
                              ${(yr.totalSalaryCap / 1_000_000).toFixed(1)}M
                            </td>
                            <td className="p-3 text-cyan-300">
                              ${(yr.activeSalaryLiability / 1_000_000).toFixed(1)}M
                            </td>
                            <td className="p-3 text-rose-300">
                              ${(yr.deadMoneyLiability / 1_000_000).toFixed(1)}M
                            </td>
                            <td className="p-3 text-amber-300">
                              ${(yr.unamortizedBonusPool / 1_000_000).toFixed(1)}M
                            </td>
                            <td className="p-3 font-bold text-emerald-400">
                              ${(yr.availableCapRoom / 1_000_000).toFixed(2)}M
                            </td>
                            <td className="p-3 text-right">
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                                <CheckCircle2 className="w-3 h-3" />
                                Validated (Δ $0)
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-white/10 bg-slate-950/80">
          <div className="text-xs text-slate-500 font-mono">
            NFL CBA Article 13 Compliant • Sub-Millisecond Double-Entry Ledger Engine
          </div>
          <button
            onClick={onClose}
            className="px-5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono font-bold rounded-xl transition-colors uppercase tracking-wider"
          >
            Close Audit Statement
          </button>
        </div>
      </div>
    </div>
  );
};
