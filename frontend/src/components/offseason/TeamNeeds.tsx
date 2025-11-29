export const TeamNeeds: React.FC<TeamNeedsProps> = ({ needs }) => {
  return (
    <div className="team-needs">
      <h3>Team Needs Analysis</h3>
      <div className="needs-grid">
        {needs.map((need) => (
          <div
            key={need.position}
            className={`need-card ${
              need.need_score > 0 ? "high-need" : "low-need"
            }`}
          >
            <div className="need-header">
              <span className="need-pos">{need.position}</span>
              {need.need_score > 0 && <span className="need-badge">Need</span>}
            </div>
            <div className="need-counts">
              <div className="count-item">
                <span className="label">Current</span>
                <span className="value">{need.current_count}</span>
              </div>
              <div className="count-item">
                <span className="label">Target</span>
                <span className="value">{need.target_count}</span>
              </div>
            </div>
            <div className="need-progress">
              <div
                className="need-fill"
                style={{
                  width: `${Math.min(
                    100,
                    (need.current_count / need.target_count) * 100
                  )}%`,
                  backgroundColor:
                    need.current_count >= need.target_count
                      ? "#4caf50"
                      : "#f44336",
                }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
