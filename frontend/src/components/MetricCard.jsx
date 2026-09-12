function MetricCard({ label, value, description }) {
  return (
    <div className="metric-card">
      <span className="metric-label">{label}</span>
      <strong className="metric-value">{value}</strong>
      <span className="metric-description">{description}</span>
    </div>
  )
}

export default MetricCard