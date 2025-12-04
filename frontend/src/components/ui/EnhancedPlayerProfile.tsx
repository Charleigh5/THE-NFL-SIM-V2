/**
 * Enhanced Player Profile Modal
 *
 * Rich player profile with career stats, personality traits, morale,
 * and development information. Task 8.3.2 implementation.
 */

import React, { useEffect, useState } from "react";
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
  const [activeTab, setActiveTab] = useState<"stats" | "attributes" | "traits">("stats");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`http://localhost:8000/api/players/${playerId}/profile`);

        if (!response.ok) {
          throw new Error("Failed to fetch player profile");
        }

        const data = await response.json();
        setProfile(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load profile");
      } finally {
        setLoading(false);
      }
    };

    if (playerId) {
      fetchProfile();
    }
  }, [playerId]);

  if (!playerId) return null;

  return (
    <div className="epp-overlay" onClick={onClose}>
      <div className="epp-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="epp-header">
          <button className="epp-close" onClick={onClose} aria-label="Close player profile">
            <X size={20} />
          </button>

          {loading ? (
            <div className="epp-header-loading">
              <div className="loading-pulse" />
            </div>
          ) : (
            profile && (
              <div className="epp-header-content">
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
                      <span className="stat-value">{profile.career_stats.games_played}</span>
                    </div>
                    {profile.career_stats.passing_yards > 0 && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">Pass Yards</span>
                          <span className="stat-value">
                            {profile.career_stats.passing_yards.toLocaleString()}
                          </span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Pass TDs</span>
                          <span className="stat-value">{profile.career_stats.passing_tds}</span>
                        </div>
                      </>
                    )}
                    {profile.career_stats.rushing_yards > 0 && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">Rush Yards</span>
                          <span className="stat-value">
                            {profile.career_stats.rushing_yards.toLocaleString()}
                          </span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Rush TDs</span>
                          <span className="stat-value">{profile.career_stats.rushing_tds}</span>
                        </div>
                      </>
                    )}
                    {profile.career_stats.receiving_yards > 0 && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">Rec Yards</span>
                          <span className="stat-value">
                            {profile.career_stats.receiving_yards.toLocaleString()}
                          </span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Rec TDs</span>
                          <span className="stat-value">{profile.career_stats.receiving_tds}</span>
                        </div>
                      </>
                    )}
                    {profile.career_stats.games_played === 0 && (
                      <div className="no-stats">
                        <span>No career stats recorded yet</span>
                      </div>
                    )}
                  </div>
                )}

                {activeTab === "attributes" && (
                  <div className="attributes-section">
                    <div className="attr-group">
                      <h5>Core</h5>
                      <div className="attr-grid">
                        <div className="attr-item">
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
                        <div className="attr-item">
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
    </div>
  );
};

export default EnhancedPlayerProfile;
