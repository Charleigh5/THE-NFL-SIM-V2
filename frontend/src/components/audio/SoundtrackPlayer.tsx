import { useState } from "react";
import { useAudio } from "../../context/AudioContext";
import { Play, Pause, Volume2, VolumeX, Music, ChevronDown, ChevronUp } from "lucide-react";
import "./SoundtrackPlayer.css";

const SoundtrackPlayer: React.FC = () => {
  const { isPlaying, volume, isMuted, toggle, setVolume, toggleMute } = useAudio();
  const [isExpanded, setIsExpanded] = useState(false);

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setVolume(parseFloat(e.target.value));
  };

  return (
    <div className={`soundtrack-player ${isExpanded ? "expanded" : ""}`}>
      {/* Collapsed view - just the music icon */}
      {!isExpanded && (
        <button
          className="player-toggle"
          onClick={() => setIsExpanded(true)}
          aria-label="Open music player"
        >
          <Music size={20} />
          {isPlaying && <span className="playing-indicator" />}
        </button>
      )}

      {/* Expanded view - full controls */}
      {isExpanded && (
        <div className="player-controls">
          <div className="player-header">
            <div className="track-info">
              <Music size={16} />
              <span className="track-name">NFL Sim Soundtrack</span>
            </div>
            <button
              className="collapse-btn"
              onClick={() => setIsExpanded(false)}
              aria-label="Collapse player"
            >
              <ChevronDown size={16} />
            </button>
          </div>

          <div className="control-row">
            <button
              className={`play-btn ${isPlaying ? "playing" : ""}`}
              onClick={toggle}
              aria-label={isPlaying ? "Pause" : "Play"}
            >
              {isPlaying ? <Pause size={20} /> : <Play size={20} />}
            </button>

            <div className="volume-control">
              <button
                className="mute-btn"
                onClick={toggleMute}
                aria-label={isMuted ? "Unmute" : "Mute"}
              >
                {isMuted || volume === 0 ? <VolumeX size={18} /> : <Volume2 size={18} />}
              </button>
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={isMuted ? 0 : volume}
                onChange={handleVolumeChange}
                className="volume-slider"
                aria-label="Volume"
              />
            </div>
          </div>

          <button
            className="expand-indicator"
            onClick={() => setIsExpanded(false)}
            aria-label="Collapse"
          >
            <ChevronUp size={14} />
          </button>
        </div>
      )}
    </div>
  );
};

export default SoundtrackPlayer;
