import { useEffect, useState } from 'react'
import './App.css'
import MetricCard from './components/MetricCard'
import HealthCard from './components/HealthCard'
import AISummary from './components/AISummary'
import ActivityOverview from './components/ActivityOverview'
import DailyActivityChart from './components/DailyActivityChart'
import HealthTrendChart from './components/HealthTrendChart'
import HealthScoreGauge from './components/HealthScoreGauge'
import Login from './components/Login'

import {
  getWeeklyHealth,
  getDailyMetrics,
  getHealthAnalysis,
} from './api/dashboardApi'

function App() {
  const [weeklyHealth, setWeeklyHealth] = useState(null)
  const [dailyMetrics, setDailyMetrics] = useState(null)
  const [healthAnalysis, setHealthAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('codepulse_user')
    return savedUser ? JSON.parse(savedUser) : null
  })

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [healthData, metricsData] = await Promise.all([
          getWeeklyHealth(),
          getDailyMetrics(),
        ])

        const latestHealth = healthData.weekly_health?.[0] ?? null
        setWeeklyHealth(latestHealth)
        setDailyMetrics(metricsData.metrics ?? [])

        if (latestHealth?.week_start) {
          try {
            const analysisData = await getHealthAnalysis(
              latestHealth.week_start,
            )
            setHealthAnalysis(analysisData.ai_run ?? null)
          } catch {
            setHealthAnalysis(null)
          }
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  if (!user) {
    return (
      <Login
        onLogin={(loggedInUser) => {
          localStorage.setItem(
            'codepulse_user',
            JSON.stringify(loggedInUser),
          )
          setUser(loggedInUser)
        }}
      />
    )
  }

  if (loading) {
    return <div className="dashboard-state">Loading dashboard...</div>
  }

  if (error) {
    return <div className="dashboard-state error">{error}</div>
  }

  if (!weeklyHealth || !dailyMetrics?.length) {
    return (
      <div className="dashboard-state">
        No dashboard data available.
      </div>
    )
  }

  const healthScore = weeklyHealth.health_score ?? 0
  const burnoutRisk = weeklyHealth.burnout_risk_flag ? 'High' : 'Low'

  const totalCommits = dailyMetrics.reduce(
    (total, metric) => total + metric.commits_count,
    0,
  )

  const totalPrsOpened = dailyMetrics.reduce(
    (total, metric) => total + metric.prs_opened,
    0,
  )

  const totalPrsReviewed = dailyMetrics.reduce(
    (total, metric) => total + metric.prs_reviewed,
    0,
  )

  const averageFocus =
    dailyMetrics.reduce(
      (total, metric) => total + metric.focus_score,
      0,
    ) / dailyMetrics.length

  const averageContextSwitch =
    dailyMetrics.reduce(
      (total, metric) => total + metric.context_switch_score,
      0,
    ) / dailyMetrics.length

  const metricCards = [
    {
      label: 'Health Score',
      value: healthScore,
      description: 'Latest week',
    },
    {
      label: 'Commits',
      value: totalCommits,
      description: 'Recent activity',
    },
    {
      label: 'PRs Opened',
      value: totalPrsOpened,
      description: 'Recent activity',
    },
    {
      label: 'PRs Reviewed',
      value: totalPrsReviewed,
      description: 'Recent activity',
    },
  ]

  const aiSummary =
    healthAnalysis?.output_text ||
    weeklyHealth.ai_summary_text ||
    'No AI health summary is available.'

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="brand">
          <h1>CodePulse</h1>
          <p>Developer Health &amp; Productivity</p>
        </div>

        <nav className="dashboard-nav">
          <a href="#overview">Overview</a>
          <a href="#health">Health</a>
          <a href="#activity">Activity</a>
          <a href="#summary">AI Insights</a>
        </nav>

        <div className="developer-info">
          <span className="status-dot"></span>
          <span>{user.name}</span>
          
          <button
            type="button"
            onClick={() => {
              localStorage.removeItem('codepulse_user')
              setUser(null)
            }}
          >
            Logout
          </button>
        </div>
        
      </header>

      <main className="dashboard-content" id="overview">
        <section className="welcome-section">
          <div>
            <h2>Developer Overview</h2>
            <p>
              Monitor your development activity, focus, productivity, and
              overall developer health.
            </p>
          </div>
        </section>

        <section className="metrics-grid">
          {metricCards.map((metric) => (
            <MetricCard
              key={metric.label}
              label={metric.label}
              value={metric.value}
              description={metric.description}
            />
          ))}
        </section>

        <section id="health">
          <HealthCard
            averageFocus={averageFocus.toFixed(2)}
            contextSwitching={averageContextSwitch.toFixed(2)}
            healthStatus={healthScore >= 80 ? 'Healthy' : 'Needs Attention'}
            burnoutRisk={burnoutRisk}
          />
        </section>

        <section id="health-score">
          <HealthScoreGauge score={healthScore} />
        </section>

        <section id="activity">
          <ActivityOverview
            commits={totalCommits}
            prsOpened={totalPrsOpened}
            prsReviewed={totalPrsReviewed}
          />
        </section>

        <section id="daily-activity">
          <DailyActivityChart metrics={dailyMetrics} />
        </section>

        <section id="health-trend">
          <HealthTrendChart metrics={dailyMetrics} />
        </section>

        <section id="summary">
          <AISummary summary={aiSummary} />
        </section>
      </main>
    </div>
  )
}

export default App