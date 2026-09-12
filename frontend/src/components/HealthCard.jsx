function HealthCard({
  averageFocus,
  contextSwitching,
  healthStatus,
  burnoutRisk,
}) {
  return (
    <section className="health-section">
      <div className="section-header">
        <div>
          <h2>Weekly Health</h2>
          <p>Current developer health analysis</p>
        </div>

        <span className="health-badge">
          {burnoutRisk} Burnout Risk
        </span>
      </div>

      <div className="health-details">
        <div className="health-item">
          <span>Average Focus</span>
          <strong>{averageFocus}%</strong>
        </div>

        <div className="health-item">
          <span>Context Switching</span>
          <strong>{contextSwitching}%</strong>
        </div>

        <div className="health-item">
          <span>Health Status</span>
          <strong>{healthStatus}</strong>
        </div>
      </div>
    </section>
  )
}

export default HealthCard