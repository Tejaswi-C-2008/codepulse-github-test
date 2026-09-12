import { useState } from 'react'

function Login({ onLogin }) {
  const [githubId, setGithubId] = useState('100001')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleLogin(event) {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          github_id: Number(githubId),
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail || 'Login request failed',
        )
      }

      if (!data.user) {
        throw new Error('User not found')
      }

      onLogin(data.user)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>CodePulse</h1>
        <p>Developer Health &amp; Productivity</p>

        <form onSubmit={handleLogin}>
          <label htmlFor="github-id">GitHub ID</label>

          <input
            id="github-id"
            type="number"
            value={githubId}
            onChange={(event) => setGithubId(event.target.value)}
            required
          />

          {error && <p className="login-error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default Login