import React, { useEffect, useState } from "react";
import { X } from "lucide-react";
import { api } from "../../services/api";
import type { Player, PlayerStats } from "../../services/api";
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
    const fetchData = async () => {
      try {
        const [playerData, statsData] = await Promise.all([
          api.getPlayer(playerId),
          api.getPlayerStats(playerId),
        ]);
        setPlayer(playerData);
        setStats(statsData);
      } catch (error) {
        console.error("Failed to load player details", error);
      } finally {
        setLoading(false);
      }
    };
    if (playerId) {
      fetchData();
    }
  }, [playerId]);
  if (!playerId) return null;
  return (
    <div className="player-modal-overlay" onClick={onClose}>
      {" "}
      <div className="player-modal-content" onClick={(e) => e.stopPropagation()}>
        {" "}
        <div className="player-modal-header">
          {" "}
          <div className="player-info">
            {" "}
            {loading ? (
              <h2>Loading...</h2>
            ) : (
              <>
                {" "}
                <h2>
                  {" "}
                  {player?.first_name} {player?.last_name}{" "}
                </h2>{" "}
                <div className="player-meta">
                  {" "}
                  <span>#{player?.jersey_number}</span> <span>{player?.position}</span>{" "}
                </div>{" "}
              </>
            )}{" "}
          </div>{" "}
          <button className="close-button" onClick={onClose}>
            {" "}
            <X size={24} />{" "}
          </button>{" "}
        </div>{" "}
        <div className="player-modal-body">
          {" "}
          {loading ? (
            <div className="p-10 text-center">Loading player details...</div>
          ) : (
            <>
              {" "}
              <div className="attributes-grid">
                {" "}
                <div className="attribute-item">
                  {" "}
                  <span className="attribute-label">Overall</span>{" "}
                  <span className="attribute-value">{player?.overall_rating}</span>{" "}
                </div>{" "}
                <div className="attribute-item">
                  {" "}
                  <span className="attribute-label">Age</span>{" "}
                  <span className="attribute-value">{player?.age}</span>{" "}
                </div>{" "}
                <div className="attribute-item">
                  {" "}
                  <span className="attribute-label">Exp</span>{" "}
                  <span className="attribute-value">{player?.experience}</span>{" "}
                </div>{" "}
                <div className="attribute-item">
                  {" "}
                  <span className="attribute-label">Height</span>{" "}
                  <span className="attribute-value">
                    {" "}
                    {player?.height
                      ? `${Math.floor(player.height / 12)}'${player.height % 12}"`
                      : "-"}{" "}
                  </span>{" "}
                </div>{" "}
                <div className="attribute-item">
                  {" "}
                  <span className="attribute-label">Weight</span>{" "}
                  <span className="attribute-value">{player?.weight} lbs</span>{" "}
                </div>{" "}
                <div className="attribute-item">
                  {" "}
                  <span className="attribute-label">Speed</span>{" "}
                  <span className="attribute-value">{player?.speed}</span>{" "}
                </div>{" "}
                <div className="attribute-item">
                  {" "}
                  <span className="attribute-label">Strength</span>{" "}
                  <span className="attribute-value">{player?.strength}</span>{" "}
                </div>{" "}
              </div>{" "}
              <div className="career-stats-section">
                {" "}
                <h3>Career Stats</h3>{" "}
                {stats ? (
                  <table className="career-stats-table">
                    {" "}
                    <thead>
                      {" "}
                      <tr>
                        {" "}
                        <th>Games</th> <th>Pass Yds</th> <th>Pass TDs</th> <th>Rush Yds</th>{" "}
                        <th>Rush TDs</th> <th>Rec Yds</th> <th>Rec TDs</th>{" "}
                      </tr>{" "}
                    </thead>{" "}
                    <tbody>
                      {" "}
                      <tr>
                        {" "}
                        <td>{stats.games_played}</td> <td>{stats.passing_yards}</td>{" "}
                        <td>{stats.passing_tds}</td> <td>{stats.rushing_yards}</td>{" "}
                        <td>{stats.rushing_tds}</td> <td>{stats.receiving_yards}</td>{" "}
                        <td>{stats.receiving_tds}</td>{" "}
                      </tr>{" "}
                    </tbody>{" "}
                  </table>
                ) : (
                  <p>No stats available.</p>
                )}{" "}
              </div>{" "}
            </>
          )}{" "}
        </div>{" "}
      </div>{" "}
    </div>
  );
};
