import React, { useState, useEffect, useMemo } from "react";
import {
  Users,
  DollarSign,
  Filter,
  Search,
  CheckCircle2,
  XCircle,
  TrendingUp,
  Award,
  ShieldAlert,
  X,
  Send,
  Sparkles,
} from "lucide-react";
import { VirtualizedTable, type VirtualizedTableColumn } from "../common/VirtualizedTable";
import type {
  FreeAgentMarketPlayer,
  FreeAgentBidRequest,
  FreeAgentBidResponse,
} from "../../types/offseason";
import { api } from "../../services/api";
import { VoidYearsSlider } from "../capology/VoidYearsSlider";
import { MultiYearCapHeatmap } from "../capology/MultiYearCapHeatmap";
import { CompPickWarningBadge } from "../capology/CompPickWarningBadge";
import { capologyApi } from "../../services/capologyApi";
import type {
  MultiYearContractProposal,
  MultiYearCapProjectionResponse,
} from "../../types/capology";

import {
  useFreeAgencyStore,
  useFilteredFreeAgents,
  useFreeAgencyMarketStatus,
  useFreeAgencyFilterState,
  type PositionFilter,
  type TierFilter,
} from "../../store/useFreeAgencyStore";

interface FreeAgencyMarketProps {
  seasonId?: number;
  teamId?: number;
}

export const FreeAgencyMarket: React.FC<FreeAgencyMarketProps> = ({ seasonId = 1, teamId = 1 }) => {
  const filteredPlayers = useFilteredFreeAgents();
  const { isLoading: loading, error, capSpace, team, totalCount } = useFreeAgencyMarketStatus();
  const { positionFilter, tierFilter, searchQuery } = useFreeAgencyFilterState();
  const {
    loadMarketData,
    setPositionFilter,
    setTierFilter,
    setSearchQuery,
    removePlayer,
    updateCapSpace,
  } = useFreeAgencyStore();

  // Bidding Modal states
  const [selectedPlayer, setSelectedPlayer] = useState<FreeAgentMarketPlayer | null>(null);
  const [bidYears, setBidYears] = useState<number>(3);
  const [bidTotalAmount, setBidTotalAmount] = useState<number>(30000000); // in dollars
  const [bidSigningBonus, setBidSigningBonus] = useState<number>(9000000); // in dollars
  const [bidGuaranteed, setBidGuaranteed] = useState<number>(18000000); // in dollars
  const [submittingBid, setSubmittingBid] = useState<boolean>(false);
  const [bidResponse, setBidResponse] = useState<FreeAgentBidResponse | null>(null);

  // Capology & Void Years Enhancement states (TASK-014)
  const [voidYears, setVoidYears] = useState<number>(0);
  const [postJune1, setPostJune1] = useState<boolean>(false);
  const [multiYearProjection, setMultiYearProjection] =
    useState<MultiYearCapProjectionResponse | null>(null);
  const [isSimulatingCap, setIsSimulatingCap] = useState<boolean>(false);

  useEffect(() => {
    loadMarketData(seasonId, teamId);
  }, [loadMarketData, seasonId, teamId]);

  // When a player is selected for bidding, initialize offer from their projected values
  const handleOpenBidModal = (player: FreeAgentMarketPlayer) => {
    setSelectedPlayer(player);
    setBidResponse(null);
    setVoidYears(0);
    setPostJune1(false);
    setMultiYearProjection(null);

    const projYears = Math.max(1, Math.min(5, player.projected_years || 3));
    const projAAV = player.projected_aav || 5000000;
    const total = projAAV * projYears;
    const bonus = Math.round(total * 0.3);
    const guaranteed = Math.round(total * 0.55);

    setBidYears(projYears);
    setBidTotalAmount(total);
    setBidSigningBonus(bonus);
    setBidGuaranteed(guaranteed);
  };

  // Synchronize 5-Year Capology & Void Calculations (TASK-014)
  useEffect(() => {
    if (!selectedPlayer) {
      setMultiYearProjection(null);
      return;
    }

    let isCancelled = false;
    setIsSimulatingCap(true);

    const baseSalaryTotal = Math.max(0, bidTotalAmount - bidSigningBonus);
    const annualBase = Math.max(950_000, Math.round(baseSalaryTotal / Math.max(1, bidYears)));

    const proposal: MultiYearContractProposal = {
      player_id: selectedPlayer.player_id,
      team_id: teamId,
      real_years: Math.min(5, Math.max(1, bidYears)),
      void_years: voidYears,
      annual_base_salary: annualBase,
      signing_bonus_total: bidSigningBonus,
      guaranteed_total: bidGuaranteed,
      post_june_1_designation: postJune1,
    };

    const timer = setTimeout(() => {
      capologyApi
        .simulateProposal(proposal)
        .then((res) => {
          if (!isCancelled) {
            setMultiYearProjection(res);
            setIsSimulatingCap(false);
          }
        })
        .catch((err) => {
          if (!isCancelled) {
            console.error("Capology simulation error:", err);
            setIsSimulatingCap(false);
          }
        });
    }, 150);

    return () => {
      isCancelled = true;
      clearTimeout(timer);
    };
  }, [
    selectedPlayer,
    teamId,
    bidYears,
    voidYears,
    bidTotalAmount,
    bidSigningBonus,
    bidGuaranteed,
    postJune1,
  ]);

  // Live Capology Proration Calculations (NFL CBA Compliant)
  const capologyPreview = useMemo(() => {
    const years = Math.max(1, bidYears);
    const prorationYears = Math.min(years, 5); // NFL 5-year maximum proration ceiling
    const annualSigningBonusProration =
      prorationYears > 0 ? Math.round(bidSigningBonus / prorationYears) : 0;
    const baseSalaryTotal = Math.max(0, bidTotalAmount - bidSigningBonus);
    const annualBaseSalary = Math.round(baseSalaryTotal / years);
    const year1CapHit = annualBaseSalary + annualSigningBonusProration;
    const remainingCap = capSpace - year1CapHit;
    const aav = Math.round(bidTotalAmount / years);
    const guaranteedPercentage =
      bidTotalAmount > 0 ? Math.min(100, Math.round((bidGuaranteed / bidTotalAmount) * 100)) : 0;

    return {
      prorationYears,
      annualSigningBonusProration,
      annualBaseSalary,
      year1CapHit,
      remainingCap,
      aav,
      guaranteedPercentage,
      isCapCompliant: remainingCap >= 0,
    };
  }, [bidYears, bidTotalAmount, bidSigningBonus, bidGuaranteed, capSpace]);

  // Handle Bid Submission
  const handleSubmitBid = async () => {
    if (!selectedPlayer) return;

    setSubmittingBid(true);
    setBidResponse(null);

    const payload: FreeAgentBidRequest = {
      player_id: selectedPlayer.player_id,
      team_id: teamId,
      years: bidYears,
      total_amount: bidTotalAmount,
      signing_bonus: bidSigningBonus,
      guaranteed_amount: bidGuaranteed,
    };

    try {
      const res = await api.post<FreeAgentBidResponse>(
        `/api/seasons/${seasonId}/free-agency/bid`,
        payload
      );

      setBidResponse(res.data);

      if (res.data.accepted) {
        updateCapSpace(res.data.updated_cap_space);
        removePlayer(selectedPlayer.player_id);
      }
    } catch (err: unknown) {
      console.error("Bid submission failed:", err);
      setBidResponse({
        status: "ERROR",
        accepted: false,
        message:
          err instanceof Error ? err.message : "Network error while submitting contract bid.",
        updated_cap_space: capSpace,
      });
    } finally {
      setSubmittingBid(false);
    }
  };

  // Virtualized Table Columns
  const columns: VirtualizedTableColumn<FreeAgentMarketPlayer>[] = useMemo(
    () => [
      {
        id: "tier",
        header: "Tier",
        width: 90,
        align: "center",
        sortable: true,
        sortKey: (p) => p.tier || "Tier 4",
        cell: (p) => {
          const tier = p.tier || "Tier 4";
          const isTier1 = tier.includes("1");
          const isTier2 = tier.includes("2");
          const isTier3 = tier.includes("3");

          const badgeColor = isTier1
            ? "bg-amber-500/20 text-amber-300 border-amber-500/40"
            : isTier2
              ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
              : isTier3
                ? "bg-blue-500/20 text-blue-300 border-blue-500/40"
                : "bg-gray-500/20 text-gray-300 border-gray-500/40";

          return (
            <span
              className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider border ${badgeColor}`}
            >
              {tier}
            </span>
          );
        },
      },
      {
        id: "name",
        header: "Athlete",
        minWidth: 160,
        sortable: true,
        sortKey: (p) => p.player_name || p.name || "",
        cell: (p) => (
          <div className="flex flex-col">
            <span className="font-header text-sm text-white uppercase tracking-tight">
              {p.player_name || p.name || `Player #${p.player_id}`}
            </span>
            <span className="text-[10px] font-mono text-gray-400">
              {p.position} • Age {p.age}
            </span>
          </div>
        ),
      },
      {
        id: "position",
        header: "Pos",
        width: 70,
        align: "center",
        sortable: true,
        sortKey: (p) => p.position,
        cell: (p) => (
          <span className="px-2 py-0.5 rounded bg-white/5 border border-white/10 text-white font-mono text-xs font-bold">
            {p.position}
          </span>
        ),
      },
      {
        id: "overall",
        header: "OVR",
        width: 75,
        align: "center",
        sortable: true,
        sortKey: (p) => p.overall_rating,
        cell: (p) => {
          const ovr = p.overall_rating;
          const ratingColor =
            ovr >= 90
              ? "text-yellow-400 font-bold"
              : ovr >= 82
                ? "text-emerald-400 font-semibold"
                : ovr >= 75
                  ? "text-cyan-400"
                  : "text-gray-300";
          return <span className={`text-base font-header ${ratingColor}`}>{ovr}</span>;
        },
      },
      {
        id: "age",
        header: "Age",
        width: 65,
        align: "center",
        sortable: true,
        sortKey: (p) => p.age,
        cell: (p) => <span className="text-gray-300 font-mono text-xs">{p.age}</span>,
      },
      {
        id: "aav",
        header: "Projected AAV",
        width: 130,
        align: "right",
        sortable: true,
        sortKey: (p) => p.projected_aav,
        cell: (p) => (
          <span className="text-emerald-400 font-mono text-xs font-semibold">
            ${(p.projected_aav / 1000000).toFixed(2)}M / yr
          </span>
        ),
      },
      {
        id: "years",
        header: "Exp. Term",
        width: 90,
        align: "center",
        sortable: true,
        sortKey: (p) => p.projected_years,
        cell: (p) => (
          <span className="text-gray-300 font-mono text-xs">{p.projected_years} yrs</span>
        ),
      },
      {
        id: "suitors",
        header: "Interested Teams",
        minWidth: 150,
        cell: (p) => {
          const teams = p.top_interested_teams || [];
          if (teams.length === 0) {
            return <span className="text-[10px] text-gray-500 font-mono">Market Open</span>;
          }
          return (
            <div className="flex flex-wrap gap-1">
              {teams.slice(0, 3).map((teamAbbr) => (
                <span
                  key={teamAbbr}
                  className="px-1.5 py-0.5 rounded bg-white/5 border border-white/10 text-[10px] font-mono text-gray-300"
                >
                  {teamAbbr}
                </span>
              ))}
              {teams.length > 3 && (
                <span className="text-[9px] text-gray-400 self-center">+{teams.length - 3}</span>
              )}
            </div>
          );
        },
      },
      {
        id: "actions",
        header: "Action",
        width: 110,
        align: "center",
        cell: (p) => (
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleOpenBidModal(p);
            }}
            className="px-3 py-1 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-header text-xs uppercase tracking-wider rounded-lg shadow-md transition-all active:scale-95"
          >
            Submit Bid
          </button>
        ),
      },
    ],
    []
  );

  return (
    <div className="space-y-6 font-body" data-testid="free-agency-market">
      {/* Vitally Important Cap & Market Header Banner */}
      <div className="relative rounded-2xl overflow-hidden broadcast-glass p-6 border border-white/15 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-xl bg-black/60 border-2 border-white/15 p-2 shadow-xl flex items-center justify-center shrink-0">
            <DollarSign className="text-emerald-400" size={32} />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-emerald-400">
                NFL CBA Top-51 Offseason Market {team ? `• ${team.city} ${team.name}` : ""}
              </span>
            </div>
            <h1 className="text-3xl md:text-5xl font-header uppercase tracking-tight text-white leading-none mt-0.5">
              Free Agency Market
            </h1>
            <p className="text-gray-400 text-xs font-mono mt-1">
              Active Negotiations & Multi-Year Contract Capology Bidding Hub
            </p>
          </div>
        </div>

        {/* Salary Cap Status Box */}
        <div className="flex items-center gap-4 bg-black/40 backdrop-blur-md px-5 py-3.5 rounded-xl border border-white/10">
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-400 uppercase tracking-widest flex items-center gap-1">
              <DollarSign size={12} className="text-emerald-400" /> Available Cap Space
            </span>
            <span
              className={`font-header text-2xl leading-none mt-0.5 ${
                capSpace >= 0 ? "text-emerald-400" : "text-red-400"
              }`}
            >
              ${(capSpace / 1000000).toFixed(2)}M
            </span>
            <span className="text-[9px] font-mono text-gray-500 mt-0.5">
              Top-51 Offseason Rule Active
            </span>
          </div>

          <div className="h-8 w-[1px] bg-white/15" />

          <div className="flex flex-col">
            <span className="text-[10px] text-gray-400 uppercase tracking-widest flex items-center gap-1">
              <Users size={12} className="text-cyan-400" /> Free Agents
            </span>
            <span className="font-header text-2xl text-white leading-none mt-0.5">
              {totalCount}
            </span>
            <span className="text-[9px] font-mono text-gray-500 mt-0.5">
              Filtered: {filteredPlayers.length}
            </span>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-broadcast-dark/80 backdrop-blur-md p-3.5 rounded-xl border border-white/10 shadow-lg">
        {/* Unit & Position Filter Tabs */}
        <div className="flex flex-wrap items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
          <span className="text-xs font-mono text-gray-400 mr-1 flex items-center gap-1">
            <Filter size={12} /> Unit:
          </span>
          {(
            [
              "ALL",
              "OFF",
              "DEF",
              "QB",
              "RB",
              "WR",
              "TE",
              "OL",
              "DL",
              "LB",
              "DB",
              "K/P",
            ] as PositionFilter[]
          ).map((pos) => (
            <button
              key={pos}
              onClick={() => setPositionFilter(pos)}
              className={`px-3 py-1 rounded-md text-xs font-header uppercase tracking-wider transition-all ${
                positionFilter === pos
                  ? "bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-md shadow-emerald-600/30"
                  : "bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white"
              }`}
            >
              {pos}
            </button>
          ))}
        </div>

        {/* Tier Filter & Search Input */}
        <div className="flex items-center gap-3 w-full md:w-auto">
          {/* Tier Selector */}
          <div className="flex items-center gap-1 text-xs font-mono">
            <span className="text-gray-400 mr-1 flex items-center gap-1">
              <Award size={12} /> Tier:
            </span>
            {(["ALL", "Tier 1", "Tier 2", "Tier 3", "Tier 4"] as TierFilter[]).map((t) => (
              <button
                key={t}
                onClick={() => setTierFilter(t)}
                className={`px-2 py-0.5 rounded text-[11px] font-mono transition-colors ${
                  tierFilter === t
                    ? "bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold"
                    : "text-gray-400 hover:text-white hover:bg-white/5"
                }`}
              >
                {t}
              </button>
            ))}
          </div>

          {/* Search Box */}
          <div className="relative flex-1 md:w-56">
            <Search
              size={13}
              className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400"
            />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search athlete..."
              className="w-full pl-8 pr-3 py-1 bg-black/40 border border-white/10 rounded-lg text-xs font-mono text-white placeholder-gray-500 focus:outline-none focus:border-emerald-500 transition-colors"
            />
          </div>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs font-mono flex items-center gap-2">
          <ShieldAlert size={16} className="text-red-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Virtualized Free Agency Table */}
      <div className="broadcast-glass p-4 rounded-2xl border border-white/15 shadow-2xl">
        <VirtualizedTable
          data={filteredPlayers}
          columns={columns}
          height={560}
          estimateRowHeight={50}
          overscan={15}
          isLoading={loading}
          emptyMessage="No free agents match your current position and tier filters."
          getRowId={(player) => player.player_id}
          onRowClick={(player) => handleOpenBidModal(player)}
          testId="free-agency-table"
        />
      </div>

      {/* Interactive Contract Bidding Modal */}
      {selectedPlayer && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4"
          data-testid="bidding-modal"
          onClick={() => setSelectedPlayer(null)}
        >
          <div
            className="broadcast-glass rounded-2xl border border-white/20 p-6 max-w-xl w-full relative shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar"
            data-testid="bidding-modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close Button */}
            <button
              onClick={() => setSelectedPlayer(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white p-1.5 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
              aria-label="Close bidding modal"
            >
              <X size={18} />
            </button>

            {/* Modal Header */}
            <div className="flex items-center gap-4 mb-5 pb-4 border-b border-white/10">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-emerald-600/30 to-teal-600/30 border border-emerald-500/40 flex items-center justify-center shadow-lg">
                <span className="font-header text-2xl text-emerald-400">
                  {selectedPlayer.overall_rating}
                </span>
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded bg-white/10 text-[10px] font-mono font-bold text-gray-300">
                    {selectedPlayer.position}
                  </span>
                  <span className="text-xs font-mono text-gray-400">
                    Age {selectedPlayer.age} • {selectedPlayer.tier || "Tier 3"}
                  </span>
                </div>
                <h2 className="font-header text-2xl text-white uppercase leading-tight mt-0.5">
                  {selectedPlayer.player_name || selectedPlayer.name}
                </h2>
                <p className="text-[11px] font-mono text-gray-400">
                  Expected Market AAV: ${(selectedPlayer.projected_aav / 1000000).toFixed(2)}M •{" "}
                  {selectedPlayer.projected_years} yrs
                </p>
              </div>
            </div>

            {/* Bidding Response Alert */}
            {bidResponse && (
              <div
                className={`mb-5 p-4 rounded-xl border flex items-start gap-3 ${
                  bidResponse.accepted
                    ? "bg-emerald-500/15 border-emerald-500/40 text-emerald-200"
                    : "bg-red-500/15 border-red-500/40 text-red-200"
                }`}
              >
                {bidResponse.accepted ? (
                  <CheckCircle2 size={20} className="text-emerald-400 shrink-0 mt-0.5" />
                ) : (
                  <XCircle size={20} className="text-red-400 shrink-0 mt-0.5" />
                )}
                <div className="text-xs font-mono">
                  <strong className="font-bold uppercase tracking-wider block mb-0.5">
                    {bidResponse.accepted ? "Offer Accepted!" : "Offer Rejected"}
                  </strong>
                  <p>{bidResponse.message}</p>
                  {bidResponse.accepted && (
                    <p className="mt-1 text-[11px] text-emerald-300">
                      New Available Cap: ${(bidResponse.updated_cap_space / 1000000).toFixed(2)}M
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* Contract Negotiation Sliders / Form Controls */}
            {!bidResponse?.accepted && (
              <div className="space-y-4">
                {/* CBA Void Years & Proration Slider (TASK-014) */}
                <VoidYearsSlider
                  realYears={bidYears}
                  setRealYears={setBidYears}
                  voidYears={voidYears}
                  setVoidYears={setVoidYears}
                  postJune1={postJune1}
                  setPostJune1={setPostJune1}
                  signingBonus={bidSigningBonus}
                />

                {/* Total Value */}
                <div>
                  <div className="flex justify-between items-center text-xs font-mono mb-1.5">
                    <span className="text-gray-300 flex items-center gap-1.5">
                      <DollarSign size={12} className="text-emerald-400" /> Total Contract Value:
                    </span>
                    <span className="text-emerald-400 font-bold">
                      ${(bidTotalAmount / 1000000).toFixed(2)}M
                    </span>
                  </div>
                  <input
                    type="range"
                    min={1000000}
                    max={250000000}
                    step={500000}
                    value={bidTotalAmount}
                    onChange={(e) => {
                      const val = parseInt(e.target.value);
                      setBidTotalAmount(val);
                      if (bidSigningBonus > val) setBidSigningBonus(Math.round(val * 0.4));
                      if (bidGuaranteed > val) setBidGuaranteed(Math.round(val * 0.6));
                    }}
                    className="w-full accent-emerald-500 cursor-pointer h-1.5 bg-white/10 rounded-lg"
                  />
                </div>

                {/* Signing Bonus */}
                <div>
                  <div className="flex justify-between items-center text-xs font-mono mb-1.5">
                    <span className="text-gray-300 flex items-center gap-1.5">
                      <Sparkles size={12} className="text-cyan-400" /> Signing Bonus (Prorated):
                    </span>
                    <span className="text-cyan-400 font-bold">
                      ${(bidSigningBonus / 1000000).toFixed(2)}M
                    </span>
                  </div>
                  <input
                    type="range"
                    min={0}
                    max={bidTotalAmount}
                    step={250000}
                    value={bidSigningBonus}
                    onChange={(e) => {
                      const val = parseInt(e.target.value);
                      setBidSigningBonus(val);
                      if (bidGuaranteed < val) setBidGuaranteed(val);
                    }}
                    className="w-full accent-cyan-500 cursor-pointer h-1.5 bg-white/10 rounded-lg"
                  />
                </div>

                {/* Guaranteed Money */}
                <div>
                  <div className="flex justify-between items-center text-xs font-mono mb-1.5">
                    <span className="text-gray-300 flex items-center gap-1.5">
                      <ShieldAlert size={12} className="text-amber-400" /> Total Guaranteed Money:
                    </span>
                    <span className="text-amber-400 font-bold">
                      ${(bidGuaranteed / 1000000).toFixed(2)}M (
                      {capologyPreview.guaranteedPercentage}%)
                    </span>
                  </div>
                  <input
                    type="range"
                    min={bidSigningBonus}
                    max={bidTotalAmount}
                    step={500000}
                    value={bidGuaranteed}
                    onChange={(e) => setBidGuaranteed(parseInt(e.target.value))}
                    className="w-full accent-amber-500 cursor-pointer h-1.5 bg-white/10 rounded-lg"
                  />
                </div>

                {/* Live Capology Proration Preview Panel */}
                <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 space-y-2 mt-4">
                  <div className="flex items-center justify-between pb-2 border-b border-white/10">
                    <span className="text-xs font-header uppercase tracking-wider text-gray-300 flex items-center gap-1">
                      <TrendingUp size={13} className="text-emerald-400" /> Capology Proration
                      Breakdown
                    </span>
                    <span className="text-[10px] font-mono text-gray-400">
                      CBA Max Proration: {capologyPreview.prorationYears} yrs
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                    <div className="bg-black/40 p-2 rounded-lg">
                      <span className="text-[10px] text-gray-400 block">Annual Base Salary</span>
                      <span className="text-white font-bold">
                        ${(capologyPreview.annualBaseSalary / 1000000).toFixed(2)}M
                      </span>
                    </div>

                    <div className="bg-black/40 p-2 rounded-lg">
                      <span className="text-[10px] text-gray-400 block">Bonus Proration / Yr</span>
                      <span className="text-cyan-300 font-bold">
                        ${(capologyPreview.annualSigningBonusProration / 1000000).toFixed(2)}M
                      </span>
                    </div>

                    <div className="bg-black/40 p-2 rounded-lg border border-emerald-500/20">
                      <span className="text-[10px] text-emerald-400 block">Year 1 Cap Hit</span>
                      <span className="text-emerald-400 font-bold text-sm">
                        ${(capologyPreview.year1CapHit / 1000000).toFixed(2)}M
                      </span>
                    </div>

                    <div
                      className={`p-2 rounded-lg border ${
                        capologyPreview.isCapCompliant
                          ? "bg-black/40 border-white/5"
                          : "bg-red-500/20 border-red-500/40"
                      }`}
                    >
                      <span className="text-[10px] text-gray-400 block">Remaining Cap Space</span>
                      <span
                        className={`font-bold text-sm ${
                          capologyPreview.isCapCompliant ? "text-white" : "text-red-400"
                        }`}
                      >
                        ${(capologyPreview.remainingCap / 1000000).toFixed(2)}M
                      </span>
                    </div>
                  </div>

                  {!capologyPreview.isCapCompliant && (
                    <div className="p-2 bg-red-500/20 rounded-lg text-[11px] font-mono text-red-300 flex items-center gap-1.5">
                      <ShieldAlert size={13} className="shrink-0" />
                      <span>Year 1 cap hit exceeds team available cap room!</span>
                    </div>
                  )}
                </div>

                {/* Compensatory Pick Warning Badge (TASK-014) */}
                <CompPickWarningBadge impact={multiYearProjection?.comp_pick_impact ?? null} />

                {/* 5-Year Capology Heatmap (TASK-014) */}
                <MultiYearCapHeatmap
                  schedule={multiYearProjection?.yearly_schedule ?? []}
                  loading={isSimulatingCap}
                />

                {/* Action Buttons */}
                <div className="flex gap-3 pt-2">
                  <button
                    onClick={() => setSelectedPlayer(null)}
                    className="flex-1 py-2.5 bg-white/10 hover:bg-white/15 text-gray-300 font-header text-xs uppercase tracking-wider rounded-xl transition-all"
                  >
                    Cancel
                  </button>

                  <button
                    onClick={handleSubmitBid}
                    disabled={submittingBid || !capologyPreview.isCapCompliant}
                    className={`flex-1 py-2.5 font-header text-xs uppercase tracking-wider rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 ${
                      submittingBid || !capologyPreview.isCapCompliant
                        ? "bg-gray-600/50 text-gray-400 cursor-not-allowed"
                        : "bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white active:scale-95"
                    }`}
                  >
                    {submittingBid ? (
                      <span className="animate-pulse">Evaluating Offer...</span>
                    ) : (
                      <>
                        <Send size={13} />
                        <span>Transmit Formal Offer</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}

            {bidResponse?.accepted && (
              <div className="pt-3 flex justify-end">
                <button
                  onClick={() => setSelectedPlayer(null)}
                  className="px-6 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-header text-xs uppercase tracking-wider rounded-xl shadow-lg"
                >
                  Close & Return to Market
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default FreeAgencyMarket;
