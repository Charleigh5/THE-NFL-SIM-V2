export const DraftBoard: React.FC<DraftBoardProps> = ({ prospects }) => {
  return (
    <div className="draft-board">
      <h3>Top Prospects</h3>
      <div className="prospect-list">
        {prospects.length === 0 ? (
          <div className="no-prospects">No prospects available.</div>
        ) : (
          prospects.map((p) => (
            <div key={p.id} className="prospect-card">
              <div className="prospect-info">
                <span className="prospect-pos">{p.position}</span>
                <span className="prospect-name">{p.name}</span>
              </div>
              <div className="prospect-rating">{p.overall_rating} OVR</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
