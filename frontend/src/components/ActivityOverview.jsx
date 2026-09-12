function ActivityOverview({ commits, prsOpened, prsReviewed }) {
  return (
    <section className="activity-section">
      <div className="section-header">
        <div>
          <h2>Activity Overview</h2>
          <p>Your development activity for the current week</p>
        </div>
      </div>

      <div className="activity-grid">
        <div className="activity-item">
          <span className="activity-icon">C</span>
          <div>
            <span>Commits</span>
            <strong>{commits}</strong>
          </div>
        </div>

        <div className="activity-item">
          <span className="activity-icon">P</span>
          <div>
            <span>PRs Opened</span>
            <strong>{prsOpened}</strong>
          </div>
        </div>

        <div className="activity-item">
          <span className="activity-icon">R</span>
          <div>
            <span>PRs Reviewed</span>
            <strong>{prsReviewed}</strong>
          </div>
        </div>
      </div>
    </section>
  )
}

export default ActivityOverview