import {
  RadialBarChart,
  RadialBar,
  PolarAngleAxis,
  ResponsiveContainer,
} from 'recharts'

function HealthScoreGauge({ score }) {
  const safeScore = Math.max(0, Math.min(100, Number(score) || 0))

  const chartData = [
    {
      name: 'Health Score',
      value: safeScore,
      fill: '#2563eb',
    },
  ]

  return (
    <section className="health-gauge-section">
      <div className="section-header">
        <div>
          <h2>Developer Health Score</h2>
          <p>Overall health score for the latest week.</p>
        </div>
      </div>

      <div className="health-gauge">
        <ResponsiveContainer width="100%" height={280}>
          <RadialBarChart
            cx="50%"
            cy="50%"
            innerRadius="65%"
            outerRadius="90%"
            startAngle={90}
            endAngle={-270}
            data={chartData}
            barSize={20}
          >
            <PolarAngleAxis
              type="number"
              domain={[0, 100]}
              angleAxisId={0}
              tick={false}
            />

            <RadialBar
              background
              dataKey="value"
              cornerRadius={10}
              angleAxisId={0}
            />

            <text
              x="50%"
              y="48%"
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize="32"
              fontWeight="700"
              fill="#172033"
            >
              {safeScore.toFixed(0)}
            </text>

            <text
              x="50%"
              y="61%"
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize="14"
              fill="#6b7280"
            >
              out of 100
            </text>
          </RadialBarChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}

export default HealthScoreGauge