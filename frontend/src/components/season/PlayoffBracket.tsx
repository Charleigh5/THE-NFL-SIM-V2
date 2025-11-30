import React from "react";
import { type PlayoffMatchup, PlayoffRound, PlayoffConference } from "../../types/playoff";
import "./PlayoffBracket.css";

/**
 * Props for the PlayoffBracket component.
 */
interface PlayoffBracketProps {
  /** List of all playoff matchups to display in the bracket. */
  matchups: PlayoffMatchup[];
}

/**
 * Component to display the NFL Playoff Bracket.
 *
 * Renders the bracket structure for AFC and NFC conferences, including:
 * - Wild Card Round
 * - Divisional Round
 * - Conference Championship
 * - Super Bowl
 *
 * Visualizes matchups, seeds, team names, and highlights winners/losers.
 */
export const PlayoffBracket: React.FC<PlayoffBracketProps> = ({ matchups }) => {
  /**
   * Filters matchups by conference and round.
   */
  const getMatchups = (conf: PlayoffConference, round: PlayoffRound) => {
    return matchups.filter((m) => m.conference === conf && m.round === round);
  };

  /**
   * Renders a single matchup card.
   * Highlights the winner if determined.
   */
  const renderMatchup = (m: PlayoffMatchup) => {
    const homeWinner = m.winner_id && m.winner_id === m.home_team_id;
    const awayWinner = m.winner_id && m.winner_id === m.away_team_id;

    return (
      <div key={m.id} className={`matchup-card ${m.winner_id ? "winner-decided" : ""}`}>
        <div className={`matchup-team ${homeWinner ? "winner" : ""} ${awayWinner ? "loser" : ""}`}>
          <span className="seed">{m.home_team_seed || "-"}</span>
          <span className="team-name">
            {m.home_team ? `${m.home_team.city} ${m.home_team.name}` : "TBD"}
          </span>
        </div>
        <div className={`matchup-team ${awayWinner ? "winner" : ""} ${homeWinner ? "loser" : ""}`}>
          <span className="seed">{m.away_team_seed || "-"}</span>
          <span className="team-name">
            {m.away_team ? `${m.away_team.city} ${m.away_team.name}` : "TBD"}
          </span>
        </div>
      </div>
    );
  };

  /**
   * Renders the bracket for a specific conference.
   */
  const renderConference = (conf: PlayoffConference) => {
    const wc = getMatchups(conf, PlayoffRound.WILD_CARD);
    const div = getMatchups(conf, PlayoffRound.DIVISIONAL);
    const confRound = getMatchups(conf, PlayoffRound.CONFERENCE);

    return (
      <div className="conference-bracket">
        <div className="conference-title">{conf}</div>
        <div className="bracket-rounds">
          <div className="round-column">
            <div className="round-title">Wild Card</div>
            {wc.map(renderMatchup)}
          </div>
          <div className="round-column">
            <div className="round-title">Divisional</div>
            {div.map(renderMatchup)}
          </div>
          <div className="round-column">
            <div className="round-title">Conference</div>
            {confRound.map(renderMatchup)}
          </div>
        </div>
      </div>
    );
  };

  const sbMatchup = matchups.find((m) => m.round === PlayoffRound.SUPER_BOWL);

  return (
    <div className="playoff-bracket">
      {renderConference(PlayoffConference.AFC)}
      {renderConference(PlayoffConference.NFC)}

      {sbMatchup && (
        <div className="super-bowl-section">
          <div className="conference-title">Super Bowl</div>
          <div className="bracket-rounds" style={{ justifyContent: "center" }}>
            {renderMatchup(sbMatchup)}
          </div>
        </div>
      )}
    </div>
  );
};
