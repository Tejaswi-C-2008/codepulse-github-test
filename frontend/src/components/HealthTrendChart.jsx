import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

function HealthTrendChart({ metrics }) {
  const chartData = metrics.map((metric) => ({
    date: metric.metric_date,
    'Focus Score': metric.focus_score,
    'Context Switching': metric.context_switch_score,
  }))

  return (
    <section className="health-chart-section">
      <div className="section-header">
        <div>
          <h2>Focus &amp; Context Switching</h2>
          <p>Daily focus quality and context-switching trends.</p>
        </div>
      </div>

      <div className="health-chart">
        <ResponsiveContainer width="100%" height={320}>
          <LineChart
            data={chartData}
            margin={{
              top: 10,
              right: 20,
              left: 0,
              bottom: 10,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />

            <Line
              type="monotone"
              dataKey="Focus Score"
              stroke="#2563eb"
              strokeWidth={2}
              dot={{ r: 4 }}
            />

            <Line
              type="monotone"
              dataKey="Context Switching"
              stroke="#dc2626"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}

export default HealthTrendChart