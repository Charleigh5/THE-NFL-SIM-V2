/**
 * Enhanced Player Profile Modal
 *
 * Rich player profile with career stats, personality traits, morale,
 * and development information. Task 8.3.2 implementation.
 */

import React, { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { api } from "../../services/api";
import {
  X,
  TrendingUp,
  TrendingDown,
  Star,
  Zap,
  Heart,
  Shield,
  Award,
  GraduationCap,
  DollarSign,
  Calendar,
  Activity,
  Target,
} from "lucide-react";
import { PlayerAvatar } from "./PlayerAvatar";
import { getTeamAbbr } from "../../utils/teamUtils";
import "./EnhancedPlayerProfile.css";

// ============================================================================
// TYPES
// ============================================================================

interface TraitInfo {
  name: string;
  description: string;
  tier: string;
}

interface PersonalityInfo {
  morale: number;
  morale_status: string;
  development_trait: string;
  archetype?: string;
}

interface EnhancedPlayerProfileData {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  jersey_number: number;
  overall_rating: number;
  age: number;
  experience: number;
  college?: string;
  height?: number;
  weight?: number;
  team_id?: number;
  team_abbreviation?: string;
  speed: number;
  acceleration: number;
  strength: number;
  agility: number;
  awareness: number;
  stamina: number;
  injury_resistance: number;
  position_attributes: Record<string, number>;
  personality: PersonalityInfo;
  traits: TraitInfo[];
  career_stats: Record<string, number>;
  season_history?: Array<Record<string, any>>;
  contract_years: number;
  contract_salary: number;
  is_rookie: boolean;
}

interface EnhancedPlayerProfileProps {
  playerId: number;
  onClose: () => void;
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

const formatHeight = (inches?: number): string => {
  if (!inches) return "-";
  return `${Math.floor(inches / 12)}'${inches % 12}"`;
};

const formatSalary = (salary: number): string => {
  if (salary >= 1000000) {
    return `$${(salary / 1000000).toFixed(1)}M`;
  }
  return `$${(salary / 1000).toFixed(0)}K`;
};

const getMoraleIcon = (status: string) => {
  switch (status) {
    case "Ecstatic":
      return <Heart size={16} className="morale-icon ecstatic" />;
    case "Happy":
      return <TrendingUp size={16} className="morale-icon happy" />;
    case "Content":
      return <Activity size={16} className="morale-icon content" />;
    case "Unhappy":
      return <TrendingDown size={16} className="morale-icon unhappy" />;
    case "Disgruntled":
      return <Zap size={16} className="morale-icon disgruntled" />;
    default:
      return <Activity size={16} className="morale-icon" />;
  }
};

const getDevTraitIcon = (trait: string) => {
  switch (trait) {
    case "XFACTOR":
      return <Star size={16} className="dev-icon xfactor" />;
    case "SUPERSTAR":
      return <Zap size={16} className="dev-icon superstar" />;
    case "STAR":
      return <Award size={16} className="dev-icon star" />;
    default:
      return <Target size={16} className="dev-icon normal" />;
  }
};

const getDevTraitLabel = (trait: string): string => {
  switch (trait) {
    case "XFACTOR":
      return "X-Factor";
    case "SUPERSTAR":
      return "Superstar";
    case "STAR":
      return "Star";
    default:
      return "Normal";
  }
};

const getAttributeClass = (value: number): string => {
  if (value >= 90) return "elite";
  if (value >= 80) return "great";
  if (value >= 70) return "good";
  if (value >= 60) return "average";
  return "poor";
};

const getMoraleClass = (status: string): string => {
  return status.toLowerCase();
};

// ============================================================================
// COMPONENT
// ============================================================================

export const EnhancedPlayerProfile: React.FC<EnhancedPlayerProfileProps> = ({
  playerId,
  onClose,
}) => {
  const [profile, setProfile] = useState<EnhancedPlayerProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"stats" | "history" | "attributes">("stats");

  useEffect(() => {
    let isCancelled = false;

    const fetchProfile = async () => {
      try {
        setLoading(true);
        setError(null);

        const data = await api.getPlayerProfile(playerId);
        if (!isCancelled) {
          setProfile(data as unknown as EnhancedPlayerProfileData);
        }
      } catch (err) {
        if (!isCancelled) {
          setError(err instanceof Error ? err.message : "Failed to load profile");
        }
      } finally {
        if (!isCancelled) {
          setLoading(false);
        }
      }
    };

    if (playerId) {
      fetchProfile();
    }

    return () => {
      isCancelled = true;
    };
  }, [playerId]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  if (!playerId) return null;

  return createPortal(
    <div className="epp-overlay" onClick={onClose}>
      <div className="epp-modal" data-testid="player-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="epp-header">
          <button
            className="epp-close"
            onClick={onClose}
            data-testid="close-modal-button"
            aria-label="Close player profile"
          >
            <X size={20} />
          </button>

          {loading ? (
            <div className="epp-header-loading">
              <div className="loading-pulse" />
            </div>
          ) : (
            profile && (
              <div className="epp-header-content">
                <PlayerAvatar
                  teamAbbr={profile.team_abbreviation || getTeamAbbr(profile.team_id)}
                  playerId={profile.id}
                  pose="hero_pose"
                  size="hero"
                  playerName={`${profile.first_name} ${profile.last_name}`}
                  position={profile.position}
                  jerseyNumber={profile.jersey_number}
                  className="w-24 h-28 mr-4 shrink-0 shadow-xl rounded-xl border border-white/20"
                />
                <div className="epp-player-identity">
                  <div className="epp-jersey">#{profile.jersey_number}</div>
                  <div className="epp-name">
                    <span className="first-name">{profile.first_name}</span>
                    <span className="last-name">{profile.last_name}</span>
                  </div>
                  <div className="epp-position-badge">{profile.position}</div>
                </div>

                <div className="epp-overall">
                  <span className="overall-value">{profile.overall_rating}</span>
                  <span className="overall-label">OVR</span>
                </div>
              </div>
            )
          )}
        </div>

        {loading ? (
          <div className="epp-loading">
            <div className="loading-spinner" />
            <span>Loading player profile...</span>
          </div>
        ) : error ? (
          <div className="epp-error">
            <span>{error}</span>
          </div>
        ) : (
          profile && (
            <div className="epp-body">
              {/* Quick Info Bar */}
              <div className="epp-quick-info">
                <div className="quick-item">
                  <Calendar size={14} />
                  <span>{profile.age} yrs</span>
                </div>
                <div className="quick-item">
                  <Award size={14} />
                  <span>
                    {profile.experience} yr{profile.experience !== 1 ? "s" : ""} exp
                  </span>
                </div>
                {profile.college && (
                  <div className="quick-item">
                    <GraduationCap size={14} />
                    <span>{profile.college}</span>
                  </div>
                )}
                <div className="quick-item">
                  <span>{formatHeight(profile.height)}</span>
                  <span className="separator">•</span>
                  <span>{profile.weight} lbs</span>
                </div>
              </div>

              {/* Personality & Development Section */}
              <div className="epp-personality-section">
                <div className="personality-card morale-card">
                  <div className="personality-header">
                    {getMoraleIcon(profile.personality.morale_status)}
                    <span>Morale</span>
                  </div>
                  <div className="personality-value">
                    <div
                      className={`morale-bar morale-${getMoraleClass(profile.personality.morale_status)}`}
                      data-morale={profile.personality.morale}
                    >
                      <div className="morale-fill" />
                    </div>
                    <span
                      className={`morale-status ${getMoraleClass(profile.personality.morale_status)}`}
                    >
                      {profile.personality.morale_status}
                    </span>
                  </div>
                </div>

                <div className="personality-card dev-card">
                  <div className="personality-header">
                    {getDevTraitIcon(profile.personality.development_trait)}
                    <span>Development</span>
                  </div>
                  <div className="personality-value">
                    <span
                      className={`dev-label ${profile.personality.development_trait.toLowerCase()}`}
                    >
                      {getDevTraitLabel(profile.personality.development_trait)}
                    </span>
                  </div>
                </div>

                <div className="personality-card contract-card">
                  <div className="personality-header">
                    <DollarSign size={16} />
                    <span>Contract</span>
                  </div>
                  <div className="personality-value">
                    <span className="contract-salary">{formatSalary(profile.contract_salary)}</span>
                    <span className="contract-years">
                      {profile.contract_years} yr{profile.contract_years !== 1 ? "s" : ""}
                    </span>
                  </div>
                </div>
              </div>

              {/* Active Traits Section */}
              {profile.traits.length > 0 && (
                <div className="epp-traits-section">
                  <h4>
                    <Shield size={16} />
                    Active Traits
                  </h4>
                  <div className="traits-list">
                    {profile.traits.map((trait, index) => (
                      <div
                        key={`${trait.name}-${index}`}
                        className={`trait-badge tier-${trait.tier.toLowerCase()}`}
                      >
                        <span className="trait-tier">{trait.tier}</span>
                        <span className="trait-name">{trait.name}</span>
                        <span className="trait-tooltip">{trait.description}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Tabs */}
              <div className="epp-tabs">
                <button
                  className={`tab-btn ${activeTab === "stats" ? "active" : ""}`}
                  onClick={() => setActiveTab("stats")}
                >
                  Career Stats
                </button>
                <button
                  className={`tab-btn ${activeTab === "history" ? "active" : ""}`}
                  onClick={() => setActiveTab("history")}
                >
                  Season History
                </button>
                <button
                  className={`tab-btn ${activeTab === "attributes" ? "active" : ""}`}
                  onClick={() => setActiveTab("attributes")}
                >
                  Attributes
                </button>
              </div>

              {/* Tab Content */}
              <div className="epp-tab-content">
                {activeTab === "stats" && (
                  <div className="stats-grid">
                    <div className="stat-item">
                      <span className="stat-label">Games Played</span>
                      <span className="stat-value">{profile.career_stats.games_played || 0}</span>
                    </div>
                    {(profile.career_stats.passing_yards > 0 || profile.position === "QB") && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">Pass Yards</span>
                          <span className="stat-value">
                            {(profile.career_stats.passing_yards || 0).toLocaleString()}
                          </span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Pass TDs</span>
                          <span className="stat-value">{profile.career_stats.passing_tds || 0}</span>
                        </div>
                      </>
                    )}
                    {(profile.career_stats.rushing_yards > 0 || ["RB", "FB", "QB"].includes(profile.position)) && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">Rush Yards</span>
                          <span className="stat-value">
                            {(profile.career_stats.rushing_yards || 0).toLocaleString()}
                          </span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Rush TDs</span>
                          <span className="stat-value">{profile.career_stats.rushing_tds || 0}</span>
                        </div>
                      </>
                    )}
                    {(profile.career_stats.receiving_yards > 0 || ["WR", "TE", "RB"].includes(profile.position)) && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">Rec Yards</span>
                          <span className="stat-value">
                            {(profile.career_stats.receiving_yards || 0).toLocaleString()}
                          </span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Rec TDs</span>
                          <span className="stat-value">{profile.career_stats.receiving_tds || 0}</span>
                        </div>
                      </>
                    )}
                    {((profile.career_stats.tackles || 0) > 0 ||
                      (profile.career_stats.sacks || 0) > 0 ||
                      ["DL", "DE", "DT", "LB", "MLB", "OLB", "CB", "S", "FS", "SS", "DB"].includes(profile.position)) && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">Total Tackles</span>
                          <span className="stat-value">
                            {profile.career_stats.tackles ||
                              (profile.career_stats.tackles_solo || 0) + (profile.career_stats.tackles_assist || 0)}
                          </span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Sacks</span>
                          <span className="stat-value">{Number(profile.career_stats.sacks || 0).toFixed(1)}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Interceptions</span>
                          <span className="stat-value">{profile.career_stats.interceptions || 0}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Pass Deflections</span>
                          <span className="stat-value">{profile.career_stats.pass_deflections || 0}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">TFL</span>
                          <span className="stat-value">{profile.career_stats.tackles_for_loss || 0}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">QB Pressures</span>
                          <span className="stat-value">{profile.career_stats.qb_pressures || 0}</span>
                        </div>
                      </>
                    )}
                    {(["K", "P", "LS"].includes(profile.position) ||
                      (profile.career_stats.fg_made || 0) > 0 ||
                      (profile.career_stats.punt_yards || 0) > 0) && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">FG Made / Att</span>
                          <span className="stat-value">
                            {profile.career_stats.fg_made || 0} / {profile.career_stats.fg_att || 0}
                          </span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Punt Yards</span>
                          <span className="stat-value">
                            {(profile.career_stats.punt_yards || 0).toLocaleString()}
                          </span>
                        </div>
                      </>
                    )}
                    {(["OL", "OT", "OG", "C", "LT", "RT", "LG", "RG"].includes(profile.position) ||
                      (profile.career_stats.pancakes || 0) > 0) && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">Pancakes</span>
                          <span className="stat-value">{profile.career_stats.pancakes || 0}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Sacks Allowed</span>
                          <span className="stat-value">{profile.career_stats.sacks_allowed || 0}</span>
                        </div>
                      </>
                    )}
                  </div>
                )}

                {activeTab === "history" && (
                  <div className="p-4">
                    {profile.season_history && profile.season_history.length > 0 ? (
                      <div className="overflow-x-auto rounded border border-white/10 bg-slate-900/60">
                        <table className="w-full text-xs text-left text-gray-200">
                          <thead className="bg-slate-950 text-cyan-400 font-mono uppercase text-[10px] border-b border-white/10">
                            <tr>
                              <th className="p-2.5">Season</th>
                              <th className="p-2.5">GP</th>
                              <th className="p-2.5">Pass Y/TD</th>
                              <th className="p-2.5">Rush Y/TD</th>
                              <th className="p-2.5">Rec Y/TD</th>
                              <th className="p-2.5">Tackles/Sack/INT</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-white/5 font-mono">
                            {profile.season_history.map((hist, idx) => (
                              <tr key={idx} className="hover:bg-white/5">
                                <td className="p-2.5 font-bold text-white">Season {hist.season_id ?? hist.year ?? idx + 1}</td>
                                <td className="p-2.5">{hist.games_played ?? "-"}</td>
                                <td className="p-2.5">{(hist.pass_yards ?? 0).toLocaleString()} / {hist.pass_tds ?? 0}</td>
                                <td className="p-2.5">{(hist.rush_yards ?? 0).toLocaleString()} / {hist.rush_tds ?? 0}</td>
                                <td className="p-2.5">{(hist.rec_yards ?? 0).toLocaleString()} / {hist.rec_tds ?? 0}</td>
                                <td className="p-2.5">
                                  {(hist.tackles_solo ?? 0) + (hist.tackles_assist ?? 0)} / {hist.sacks ?? 0} / {hist.interceptions ?? 0}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    ) : (
                      <div className="text-center py-8 text-gray-400 font-mono text-xs">
                        No archived prior seasons on file. Career archives are persisted upon season completion.
                      </div>
                    )}
                  </div>
                )}

                {activeTab === "attributes" && (
                  <div className="attributes-section">
                    <div className="attr-group">
                      <h5>Core</h5>
                      <div className="attr-grid">
                        <div className="attr-item" data-testid="player-speed">
                          <span className="attr-label">Speed</span>
                          <div className="attr-bar-container">
                            <div
                              className={`attr-bar ${getAttributeClass(profile.speed)}`}
                              data-width={profile.speed}
                            />
                          </div>
                          <span className={`attr-value ${getAttributeClass(profile.speed)}`}>
                            {profile.speed}
                          </span>
                        </div>
                        <div className="attr-item">
                          <span className="attr-label">Acceleration</span>
                          <div className="attr-bar-container">
                            <div
                              className={`attr-bar ${getAttributeClass(profile.acceleration)}`}
                              data-width={profile.acceleration}
                            />
                          </div>
                          <span className={`attr-value ${getAttributeClass(profile.acceleration)}`}>
                            {profile.acceleration}
                          </span>
                        </div>
                        <div className="attr-item" data-testid="player-strength">
                          <span className="attr-label">Strength</span>
                          <div className="attr-bar-container">
                            <div
                              className={`attr-bar ${getAttributeClass(profile.strength)}`}
                              data-width={profile.strength}
                            />
                          </div>
                          <span className={`attr-value ${getAttributeClass(profile.strength)}`}>
                            {profile.strength}
                          </span>
                        </div>
                        <div className="attr-item">
                          <span className="attr-label">Agility</span>
                          <div className="attr-bar-container">
                            <div
                              className={`attr-bar ${getAttributeClass(profile.agility)}`}
                              data-width={profile.agility}
                            />
                          </div>
                          <span className={`attr-value ${getAttributeClass(profile.agility)}`}>
                            {profile.agility}
                          </span>
                        </div>
                        <div className="attr-item">
                          <span className="attr-label">Awareness</span>
                          <div className="attr-bar-container">
                            <div
                              className={`attr-bar ${getAttributeClass(profile.awareness)}`}
                              data-width={profile.awareness}
                            />
                          </div>
                          <span className={`attr-value ${getAttributeClass(profile.awareness)}`}>
                            {profile.awareness}
                          </span>
                        </div>
                        <div className="attr-item">
                          <span className="attr-label">Stamina</span>
                          <div className="attr-bar-container">
                            <div
                              className={`attr-bar ${getAttributeClass(profile.stamina)}`}
                              data-width={profile.stamina}
                            />
                          </div>
                          <span className={`attr-value ${getAttributeClass(profile.stamina)}`}>
                            {profile.stamina}
                          </span>
                        </div>
                      </div>
                    </div>

                    {Object.keys(profile.position_attributes).length > 0 && (
                      <div className="attr-group">
                        <h5>Position Skills</h5>
                        <div className="attr-grid">
                          {Object.entries(profile.position_attributes).map(([key, value]) => (
                            <div key={key} className="attr-item">
                              <span className="attr-label">
                                {key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                              </span>
                              <div className="attr-bar-container">
                                <div
                                  className={`attr-bar ${getAttributeClass(value)}`}
                                  data-width={value}
                                />
                              </div>
                              <span className={`attr-value ${getAttributeClass(value)}`}>
                                {value}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Rookie Badge */}
              {profile.is_rookie && (
                <div className="rookie-badge">
                  <Star size={14} />
                  <span>ROOKIE</span>
                </div>
              )}
            </div>
          )
        )}
      </div>
    </div>,
    document.body
  );
};

export default EnhancedPlayerProfile;
