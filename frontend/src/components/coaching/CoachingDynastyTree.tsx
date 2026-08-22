import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Award, Zap, Shield, BookOpen, Lock, CheckCircle2 } from 'lucide-react';
import type { CoachDynastyProfile, CoachingSkillNode, StaffSynergyBreakdown } from '../../types/deepDive';

interface CoachingDynastyTreeProps {
  initialProfile?: CoachDynastyProfile;
  initialSynergy?: StaffSynergyBreakdown;
  onSkillUnlock?: (nodeId: string) => void;
}

const DEFAULT_PROFILE: CoachDynastyProfile = {
  coach_id: 'HC-CAMPBELL',
  name: 'Dan Campbell',
  role: 'Head Coach',
  level: 14,
  current_sp: 4,
  total_sp_earned: 28,
  archetype: 'Tactical Mastermind',
  tree_nodes: {
    SCHEME_DISGUISE_I: {
      id: 'SCHEME_DISGUISE_I',
      name: 'Pre-Snap Disguise',
      branch: 'SCHEME_TACTICS',
      tier: 1,
      unlocked: true,
      sp_cost: 1,
      bonus_description: '+5% pre-snap coverage misdirection against opposing QBs',
      prerequisites: [],
      stat_multiplier: 1.05,
    },
    SCHEME_MATCHUP_NIGHTMARE: {
      id: 'SCHEME_MATCHUP_NIGHTMARE',
      name: 'Iso-Mismatches',
      branch: 'SCHEME_TACTICS',
      tier: 2,
      unlocked: false,
      sp_cost: 2,
      bonus_description: '+8% route win rate for slot receivers and tight ends',
      prerequisites: ['SCHEME_DISGUISE_I'],
      stat_multiplier: 1.08,
    },
    SCHEME_FOURTH_DOWN_ALGO: {
      id: 'SCHEME_FOURTH_DOWN_ALGO',
      name: 'Analytics 4th-Down Edge',
      branch: 'SCHEME_TACTICS',
      tier: 3,
      unlocked: false,
      sp_cost: 3,
      bonus_description: '+12% conversion probability on 4th & 2 or less',
      prerequisites: ['SCHEME_MATCHUP_NIGHTMARE'],
      stat_multiplier: 1.12,
    },
    DEV_ROOKIE_ONBOARDING: {
      id: 'DEV_ROOKIE_ONBOARDING',
      name: 'Rookie Fast-Track',
      branch: 'DEVELOPMENT',
      tier: 1,
      unlocked: true,
      sp_cost: 1,
      bonus_description: '+15% XP gain for Year 1 rookies during training camp',
      prerequisites: [],
      stat_multiplier: 1.15,
    },
    DEV_TRENCH_DEVELOPER: {
      id: 'DEV_TRENCH_DEVELOPER',
      name: 'Trench Whisperer',
      branch: 'DEVELOPMENT',
      tier: 2,
      unlocked: false,
      sp_cost: 2,
      bonus_description: '+10% pass-rush & run-block progression for OL/DL',
      prerequisites: ['DEV_ROOKIE_ONBOARDING'],
      stat_multiplier: 1.10,
    },
    DEV_STAR_MAKER: {
      id: 'DEV_STAR_MAKER',
      name: 'X-Factor Catalyst',
      branch: 'DEVELOPMENT',
      tier: 3,
      unlocked: false,
      sp_cost: 3,
      bonus_description: '+20% higher chance for Star dev traits to elevate to Superstar',
      prerequisites: ['DEV_TRENCH_DEVELOPER'],
      stat_multiplier: 1.20,
    },
    CULTURE_LOCKER_ROOM_UNITY: {
      id: 'CULTURE_LOCKER_ROOM_UNITY',
      name: 'Brotherhood Culture',
      branch: 'PROGRAM_CULTURE',
      tier: 1,
      unlocked: true,
      sp_cost: 1,
      bonus_description: '-50% morale penalty after tough divisional losses',
      prerequisites: [],
      stat_multiplier: 1.05,
    },
    CULTURE_CAP_DISCIPLINE: {
      id: 'CULTURE_CAP_DISCIPLINE',
      name: 'Hometown Loyalty Discount',
      branch: 'PROGRAM_CULTURE',
      tier: 2,
      unlocked: false,
      sp_cost: 2,
      bonus_description: 'Re-signing players grant a 5% hometown contract discount',
      prerequisites: ['CULTURE_LOCKER_ROOM_UNITY'],
      stat_multiplier: 1.05,
    },
    CULTURE_PRIME_TIME_SWAGGER: {
      id: 'CULTURE_PRIME_TIME_SWAGGER',
      name: 'Big Game Mentality',
      branch: 'PROGRAM_CULTURE',
      tier: 3,
      unlocked: false,
      sp_cost: 3,
      bonus_description: '+3 OVR boost to all starters in playoff and primetime night games',
      prerequisites: ['CULTURE_CAP_DISCIPLINE'],
      stat_multiplier: 1.10,
    },
  },
};

const DEFAULT_SYNERGY: StaffSynergyBreakdown = {
  head_coach_id: 'HC-CAMPBELL',
  offensive_coord_id: 'OC-BEN-JOHNSON',
  defensive_coord_id: 'DC-AARON-GLENN',
  offensive_synergy_score: 96,
  defensive_synergy_score: 92,
  overall_chemistry_score: 94,
  active_synergy_perks: [
    'Apex Staff Synergy (+5% team OVR in 4th Quarter)',
    'Play-Caller Telepathy (Redzone TD% +8%)',
  ],
  scheme_alignment_notes: [
    'Perfect Scheme Lock (WEST_COAST): +10% play-call execution speed',
    'Defensive Autonomy (COVER_3_ZONE): DC has complete tactical control',
  ],
};

export const CoachingDynastyTree: React.FC<CoachingDynastyTreeProps> = ({
  initialProfile = DEFAULT_PROFILE,
  initialSynergy = DEFAULT_SYNERGY,
  onSkillUnlock,
}) => {
  const [profile, setProfile] = useState<CoachDynastyProfile>(initialProfile);
  const [synergy] = useState<StaffSynergyBreakdown>(initialSynergy);
  const [activeBranch, setActiveBranch] = useState<'ALL' | 'SCHEME_TACTICS' | 'DEVELOPMENT' | 'PROGRAM_CULTURE'>('ALL');
  const [selectedNode, setSelectedNode] = useState<CoachingSkillNode | null>(null);

  const handleUnlock = (node: CoachingSkillNode) => {
    if (node.unlocked || profile.current_sp < node.sp_cost) return;

    // Check prerequisites
    for (const prereqId of node.prerequisites) {
      if (!profile.tree_nodes[prereqId]?.unlocked) return;
    }

    const updatedNodes = {
      ...profile.tree_nodes,
      [node.id]: { ...node, unlocked: true },
    };

    setProfile({
      ...profile,
      current_sp: profile.current_sp - node.sp_cost,
      tree_nodes: updatedNodes,
    });

    if (selectedNode?.id === node.id) {
      setSelectedNode({ ...node, unlocked: true });
    }

    onSkillUnlock?.(node.id);
  };

  const branches = [
    { key: 'SCHEME_TACTICS', label: 'Tactical Playbook', icon: BookOpen, color: '#00f0ff' },
    { key: 'DEVELOPMENT', label: 'Player Development', icon: Zap, color: '#10b981' },
    { key: 'PROGRAM_CULTURE', label: 'Culture & Dynasty', icon: Shield, color: '#f59e0b' },
  ];

  return (
    <div className="w-full bg-slate-950/90 border border-slate-800 rounded-3xl p-6 shadow-2xl backdrop-blur-2xl font-sans">
      {/* Header Banner: Coach Details & Available SP */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-800">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-600/30 border border-cyan-500/40 flex items-center justify-center text-cyan-400 font-extrabold text-2xl font-mono shadow-lg shadow-cyan-500/10">
            {profile.name.charAt(0)}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xl font-bold text-white tracking-wide">{profile.name}</h3>
              <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px] font-mono uppercase font-bold">
                LVL {profile.level}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              {profile.role} • <strong className="text-cyan-400">{profile.archetype}</strong>
            </p>
          </div>
        </div>

        {/* Staff Synergy Meter & SP Counter */}
        <div className="flex items-center gap-4">
          <div className="p-3 bg-slate-900/90 border border-slate-800 rounded-2xl flex items-center gap-3">
            <Award className="w-5 h-5 text-amber-400" />
            <div>
              <div className="text-[10px] font-mono text-slate-400 uppercase">Staff Synergy</div>
              <div className="text-base font-extrabold text-amber-400 font-mono">
                {synergy.overall_chemistry_score}%
              </div>
            </div>
          </div>

          <div className="p-3 bg-cyan-950/60 border border-cyan-500/40 rounded-2xl flex items-center gap-3 shadow-lg shadow-cyan-500/10">
            <Zap className="w-5 h-5 text-cyan-400 animate-pulse" />
            <div>
              <div className="text-[10px] font-mono text-cyan-300 uppercase">Available Points</div>
              <div className="text-base font-extrabold text-white font-mono">
                {profile.current_sp} <span className="text-xs text-cyan-400">SP</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Branch Tabs */}
      <div className="flex items-center gap-2 mt-6 overflow-x-auto pb-2">
        <button
          onClick={() => setActiveBranch('ALL')}
          className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all ${
            activeBranch === 'ALL'
              ? 'bg-slate-800 text-white border border-slate-600'
              : 'text-slate-400 hover:text-slate-200 bg-slate-900/60 border border-slate-800'
          }`}
        >
          FULL DYNASTY TREE
        </button>
        {branches.map((b) => {
          const Icon = b.icon;
          const isActive = activeBranch === b.key;
          return (
            <button
              key={b.key}
              onClick={() => setActiveBranch(b.key as any)}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all ${
                isActive
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/60 shadow-[0_0_12px_rgba(0,240,255,0.2)]'
                  : 'text-slate-400 hover:text-slate-200 bg-slate-900/60 border border-slate-800'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{b.label}</span>
            </button>
          );
        })}
      </div>

      {/* 3-Branch Tree Visualization */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        {branches.map((branch) => {
          if (activeBranch !== 'ALL' && activeBranch !== branch.key) return null;

          const branchNodes = Object.values(profile.tree_nodes)
            .filter((n) => n.branch === branch.key)
            .sort((a, b) => a.tier - b.tier);

          const BranchIcon = branch.icon;

          return (
            <div
              key={branch.key}
              className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800/80 flex flex-col gap-4 relative overflow-hidden"
            >
              <div className="flex items-center gap-2 pb-3 border-b border-slate-800/60">
                <BranchIcon className="w-4 h-4 text-cyan-400" />
                <h4 className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider">
                  {branch.label}
                </h4>
              </div>

              {/* Connected Tier Nodes */}
              <div className="flex flex-col gap-3">
                {branchNodes.map((node) => {
                  const prereqsMet = node.prerequisites.every(
                    (p) => profile.tree_nodes[p]?.unlocked
                  );
                  const canUnlock = !node.unlocked && prereqsMet && profile.current_sp >= node.sp_cost;

                  return (
                    <motion.div
                      key={node.id}
                      onClick={() => setSelectedNode(node)}
                      whileHover={{ scale: 1.02 }}
                      className={`p-3.5 rounded-xl border cursor-pointer transition-all flex items-start justify-between gap-3 ${
                        node.unlocked
                          ? 'bg-emerald-950/40 border-emerald-500/50 text-slate-100 shadow-[0_0_12px_rgba(16,185,129,0.15)]'
                          : canUnlock
                          ? 'bg-cyan-950/40 border-cyan-500/40 text-slate-200 hover:border-cyan-400'
                          : 'bg-slate-950/60 border-slate-800 text-slate-500 opacity-60'
                      }`}
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-bold">
                            T{node.tier}
                          </span>
                          <span className="text-xs font-bold font-mono text-white">
                            {node.name}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-400 mt-1 leading-snug">
                          {node.bonus_description}
                        </p>
                      </div>

                      {/* Status Icon / Cost Button */}
                      <div className="flex flex-col items-end gap-1">
                        {node.unlocked ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        ) : canUnlock ? (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleUnlock(node);
                            }}
                            className="px-2 py-1 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black text-[10px] font-mono font-bold uppercase transition-transform active:scale-95"
                          >
                            {node.sp_cost} SP
                          </button>
                        ) : (
                          <div className="flex items-center gap-1 text-[10px] font-mono text-slate-500">
                            <Lock className="w-3 h-3" />
                            <span>{node.sp_cost} SP</span>
                          </div>
                        )}
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
