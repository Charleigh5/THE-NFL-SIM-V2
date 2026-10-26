import React, { useEffect, useState } from "react";
import { X } from "lucide-react";
import { api } from "../../services/api";
import type { Player, PlayerStats } from "../../services/api";
import { PlayerAvatar } from "./PlayerAvatar";
import { getTeamAbbr } from "../../utils/teamUtils";
import { ModalShell } from "./ModalShell";
import { calculateSchemeFit, getPrimaryTraits, getSecondaryTraits } from "../../utils/schemeFit";
import "./PlayerModal.css";

interface PlayerModalProps {
  playerId: number;
  onClose: () => void;
}

export const PlayerModal: React.FC<PlayerModalProps> = ({ playerId, onClose }) => {
  const [player, setPlayer] = useState<Player | null>(null);
  const [stats, setStats] = useState<PlayerStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    const fetchData = async () => {
      try {
        const [playerData, statsData] = await Promise.all([
          api.getPlayer(playerId),
          api.getPlayerStats(playerId),
        ]);
        if (isMounted) {
          setPlayer(playerData);
          setStats(statsData);
        }
      } catch (error) {
        console.error("Failed to load player details", error);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };
    if (playerId) {
      fetchData();
    }
    return () => {
      isMounted = false;
    };
  }, [playerId]);

  if (!playerId) return null;

  const schemeFit = player ? calculateSchemeFit(player) : null;
  const primaryTraits = getPrimaryTraits(player?.position);
  const secondaryTraits = getSecondaryTraits(player?.position);

  const isDefense = ["DL", "DE", "DT", "LB", "MLB", "OLB", "CB", "S", "FS", "SS", "DB"].includes(
    player?.position?.toUpperCase() || ""
  );

  const isOL = ["OL", "OT", "OG", "C", "LT", "RT", "LG", "RG"].includes(
    player?.position?.toUpperCase() || ""
  );

  const isSpecial = ["K", "P", "LS"].includes(player?.position?.toUpperCase() || "");

  return (
    <ModalShell
      id={`player-modal-${playerId}`}
      isOpen={Boolean(playerId)}
      onClose={onClose}
      title={`${player?.first_name || ""} ${player?.last_name || ""} Dossier`}
      overlayClassName="player-modal-overlay"
      testId="player-modal-shell"
    >
      <div
        className="player-modal-content"
        data-testid="player-modal"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="player-modal-header flex items-center justify-between">
          <div className="flex items-center gap-4">
            <PlayerAvatar
              teamAbbr={player?.team_abbreviation || getTeamAbbr(player?.team_id)}
              playerId={player?.id || playerId}
              playerName={`${player?.first_name || "NFL"} ${player?.last_name || "Athlete"}`}
              position={player?.position || "ATH"}
              jerseyNumber={player?.jersey_number || 0}
              size="lg"
              className="w-16 h-16 rounded-[2px] border border-white/20"
            />
            <div className="player-info">
              {loading ? (
                <h2>Loading...</h2>
              ) : (
                <>
                  <h2>
                    {player?.first_name} {player?.last_name}
                  </h2>
                  <div className="player-meta">
                    <span>#{player?.jersey_number}</span>
                    <span>{player?.position}</span>
                    {player?.college && <span>&bull; {player.college}</span>}
                  </div>
                  {schemeFit && (
                    <div
                      className={`scheme-fit-badge ${schemeFit.badgeClass}`}
                      data-testid="scheme-fit-badge"
                    >
                      <span className="scheme-fit-label">Scheme Fit:</span>
                      <span className="scheme-fit-val">{schemeFit.tagLabel}</span>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
          <button
            className="close-button"
            data-testid="close-modal-button"
            onClick={onClose}
            aria-label="Close modal"
          >
            <X size={24} />
          </button>
        </div>

        <div className="player-modal-body">
          {loading ? (
            <div className="p-10 text-center text-gray-400 font-mono">
              Loading player dossier...
            </div>
          ) : (
            <>
              {/* Core Biometrics Bar */}
              <div className="attributes-grid biometrics-bar">
                <div className="attribute-item">
                  <span className="attribute-label">Overall</span>
                  <span className="attribute-value text-cyan-400">{player?.overall_rating}</span>
                </div>
                <div className="attribute-item">
                  <span className="attribute-label">Age</span>
                  <span className="attribute-value">{player?.age}</span>
                </div>
                <div className="attribute-item">
                  <span className="attribute-label">Exp</span>
                  <span className="attribute-value">{player?.experience}y</span>
                </div>
                <div className="attribute-item">
                  <span className="attribute-label">Height</span>
                  <span className="attribute-value">
                    {player?.height
                      ? `${Math.floor(player.height / 12)}'${player.height % 12}"`
                      : "-"}
                  </span>
                </div>
                <div className="attribute-item">
                  <span className="attribute-label">Weight</span>
                  <span className="attribute-value">{player?.weight} lbs</span>
                </div>
                <div className="attribute-item" data-testid="player-speed">
                  <span className="attribute-label">Speed</span>
                  <span className="attribute-value">{player?.speed ?? 80}</span>
                </div>
                <div className="attribute-item" data-testid="player-strength">
                  <span className="attribute-label">Strength</span>
                  <span className="attribute-value">{player?.strength ?? 80}</span>
                </div>
              </div>

              {/* Tier 1: Key Positional Attributes */}
              <div className="primary-attributes-section mb-6">
                <h4 className="text-xs font-mono uppercase tracking-wider text-cyan-400 mb-2">
                  Key Positional Attributes
                </h4>
                <div className="primary-attributes-grid" data-testid="primary-attributes-grid">
                  {primaryTraits.map((trait) => (
                    <div
                      key={trait.key}
                      className="primary-attribute-card"
                      data-testid={`primary-trait-${trait.key}`}
                    >
                      <span className="text-2xl font-black font-heading text-cyan-300">
                        {player?.[trait.key] ?? 75}
                      </span>
                      <span className="primary-trait-label">{trait.label}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Tier 2: Full Athletic & Technical Profile (Progressive Disclosure) */}
              <details className="full-traits-disclosure mb-6" data-testid="full-traits-disclosure">
                <summary className="traits-summary traits-summary-btn flex items-center justify-between cursor-pointer">
                  <span>
                    View Full Athletic & Technical Profile ({secondaryTraits.length} traits)
                  </span>
                  <span className="text-xs text-cyan-400 font-mono">Expand</span>
                </summary>
                <div className="secondary-traits-grid">
                  {secondaryTraits.map((trait) => (
                    <div
                      key={trait.key}
                      className="secondary-trait-item"
                      data-testid={`secondary-trait-${trait.key}`}
                    >
                      <span className="secondary-trait-label">{trait.label}</span>
                      <span className="secondary-trait-val">{player?.[trait.key] ?? 70}</span>
                    </div>
                  ))}
                </div>
              </details>

              <div className="career-stats-section">
                <h3>Career Performance</h3>
                {stats ? (
                  <div className="overflow-x-auto">
                    <table className="career-stats-table w-full text-center">
                      <thead>
                        <tr>
                          <th>Games</th>
                          {isDefense ? (
                            <>
                              <th>Tackles</th>
                              <th>Sacks</th>
                              <th>INTs</th>
                              <th>PD</th>
                              <th>TFL</th>
                              <th>Pressures</th>
                            </>
                          ) : isOL ? (
                            <>
                              <th>Pancakes</th>
                              <th>Sacks Allowed</th>
                            </>
                          ) : isSpecial ? (
                            <>
                              <th>FG Made</th>
                              <th>FG Att</th>
                              <th>Punt Yds</th>
                            </>
                          ) : (
                            <>
                              <th>Pass Yds</th>
                              <th>Pass TDs</th>
                              <th>Rush Yds</th>
                              <th>Rush TDs</th>
                              <th>Rec Yds</th>
                              <th>Rec TDs</th>
                            </>
                          )}
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>{stats.games_played}</td>
                          {isDefense ? (
                            <>
                              <td>
                                {stats.tackles ??
                                  (stats.tackles_solo || 0) + (stats.tackles_assist || 0)}
                              </td>
                              <td>{Number(stats.sacks || 0).toFixed(1)}</td>
                              <td>{stats.interceptions || 0}</td>
                              <td>{stats.pass_deflections || 0}</td>
                              <td>{stats.tackles_for_loss || 0}</td>
                              <td>{stats.qb_pressures || 0}</td>
                            </>
                          ) : isOL ? (
                            <>
                              <td>{stats.pancakes || 0}</td>
                              <td>{stats.sacks_allowed || 0}</td>
                            </>
                          ) : isSpecial ? (
                            <>
                              <td>{stats.fg_made || 0}</td>
                              <td>{stats.fg_att || 0}</td>
                              <td>{stats.punt_yards || 0}</td>
                            </>
                          ) : (
                            <>
                              <td>{stats.passing_yards}</td>
                              <td>{stats.passing_tds}</td>
                              <td>{stats.rushing_yards}</td>
                              <td>{stats.rushing_tds}</td>
                              <td>{stats.receiving_yards}</td>
                              <td>{stats.receiving_tds}</td>
                            </>
                          )}
                        </tr>
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="text-gray-400 font-mono text-xs">No career stats on file.</p>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </ModalShell>
  );
};

export default PlayerModal;
