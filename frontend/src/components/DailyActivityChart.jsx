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

function DailyActivityChart({ metrics }) {
  const chartData = metrics.map((metric) => ({
    date: metric.metric_date,
    Commits: metric.commits_count,
    'PRs Opened': metric.prs_opened,
    'PRs Reviewed': metric.prs_reviewed,
  }))

  return (
    <section className="activity-chart-section">
      <div className="section-header">
        <div>
          <h2>Daily Development Activity</h2>
          <p>Commits and pull request activity over time.</p>
        </div>
      </div>

      <div className="activity-chart">
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
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Legend />

            <Line
              type="monotone"
              dataKey="Commits"
              stroke="#2563eb"
              strokeWidth={2}
              dot={{ r: 4 }}
            />

            <Line
              type="monotone"
              dataKey="PRs Opened"
              stroke="#16a34a"
              strokeWidth={2}
              dot={{ r: 4 }}
            />

            <Line
              type="monotone"
              dataKey="PRs Reviewed"
              stroke="#9333ea"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}

export default DailyActivityChart