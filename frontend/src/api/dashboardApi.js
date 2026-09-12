const API_BASE_URL = 'http://127.0.0.1:8000'

const USER_ID = '59d3c1e2-ed4b-41db-9527-7a10faa71b9d'

async function request(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`)

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status} ${response.statusText}`,
    )
  }

  return response.json()
}

export async function getWeeklyHealth() {
  return request(`/weekly-health/${USER_ID}`)
}

export async function getHealthAnalysis(weekStart) {
  return request(`/ai-runs/health/${USER_ID}/${weekStart}`)
}

export async function getDailyMetrics() {
  return request(`/daily-metrics/${USER_ID}`)
}