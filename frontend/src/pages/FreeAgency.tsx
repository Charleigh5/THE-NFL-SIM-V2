import React, { useState } from "react";
import { FreeAgencyMarket } from "../components/offseason/FreeAgencyMarket";
import { CapLedgerAuditModal } from "../components/capology/CapLedgerAuditModal";
import { Scale, ShieldCheck } from "lucide-react";

export const FreeAgency: React.FC = () => {
  // Retrieve user team from localStorage if present, default to team 1
  const storedTeamId = localStorage.getItem("selectedTeamId");
  const teamId = storedTeamId ? parseInt(storedTeamId, 10) : 1;

  // Default to season 1 if not otherwise configured
  const seasonId = 1;
  const [isLedgerOpen, setIsLedgerOpen] = useState(false);

  return (
    <div className="space-y-6" data-testid="free-agency-page">
      {/* Institutional Double-Entry Capology Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 bg-slate-900/80 border border-emerald-500/20 rounded-2xl shadow-xl backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl">
            <Scale className="w-5 h-5 text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-header uppercase tracking-wider text-white">
                Double-Entry Capology Ledger
              </h2>
              <span className="flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                <ShieldCheck className="w-3 h-3" />
                Zero-Sum Active
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono">
              Immutable journaled debits/credits • CBA Article 13 & Appendix V
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsLedgerOpen(true)}
          className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-mono text-xs font-bold uppercase tracking-wider rounded-xl shadow-lg shadow-emerald-500/20 transition-all active:scale-95 cursor-pointer"
          data-testid="open-cap-ledger-audit-btn"
        >
          <Scale className="w-4 h-4" />
          Audit Ledger & Statement
        </button>
      </div>

      <FreeAgencyMarket seasonId={seasonId} teamId={teamId} />

      <CapLedgerAuditModal
        isOpen={isLedgerOpen}
        onClose={() => setIsLedgerOpen(false)}
        teamId={teamId}
      />
    </div>
  );
};

export default FreeAgency;
