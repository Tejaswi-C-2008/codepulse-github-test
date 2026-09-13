# CodePulse

**An AI-powered developer health & productivity platform.**

CodePulse looks past the usual commit-counting dashboards and asks a different question: is this developer's activity actually *sustainable*? It pulls in real GitHub activity, turns it into daily and weekly metrics, and layers AI-generated analysis on top to surface things like focus quality, context switching, and burnout risk — not just "how much code did you write today."

---

## Table of Contents

- [Why CodePulse Exists](#why-codepulse-exists)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Backend Modules](#backend-modules)
- [GitHub Integration](#github-integration)
- [AI Health Analysis](#ai-health-analysis)
- [Database Schema](#database-schema)
- [Frontend Dashboard](#frontend-dashboard)
- [Getting Started](#getting-started)
- [API Health Checks](#api-health-checks)
- [Testing & Verification](#testing--verification)
- [Security & Privacy](#security--privacy)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [Demo Walkthrough](#demo-walkthrough)
- [Project Status](#project-status)
- [Contributing](#contributing)
- [License](#license)

---

## Why CodePulse Exists

Most developer productivity tools stop at raw activity — commits, pull requests, issues opened and closed. The problem is that a high volume of activity doesn't automatically mean someone is being productive in a healthy or sustainable way. Someone grinding through 40 context switches a day and shipping late-night commits every night might look "productive" on paper while quietly heading toward burnout.

CodePulse tries to close that gap. It combines raw development activity with derived signals — focus quality, context-switching frequency, a computed health score — and then asks an AI layer to turn those numbers into something a human can actually read and act on.

## Key Features

- GitHub repository integration with commit activity sync
- An events pipeline for commits, pull requests, issues, and reviews
- Daily metrics (commit count, PR activity, focus score, context-switch score)
- Weekly health rollups, including a burnout-risk flag
- A computed Developer Health Score
- AI-generated health insights and summaries, with runs tracked for auditability
- A React dashboard with activity charts, health trend charts, and a health score gauge
- Authenticated user flow with persistent sessions
- A FastAPI backend backed by PostgreSQL, with CORS handling and input validation baked in

## How It Works

```text
GitHub Activity
      ↓
FastAPI Backend
      ↓
Event & Activity Data
      ↓
Metrics Processing
      ↓
Daily / Weekly Health Metrics
      ↓
AI Health Analysis
      ↓
React Dashboard
```

In practice: CodePulse syncs activity from GitHub, stores it as structured events, crunches those events into daily and weekly metrics, hands the results to an AI analysis step, and renders everything on a dashboard you can actually check in the morning with your coffee.

## Tech Stack

| Layer | Tools |
|---|---|
| Backend | Python, FastAPI, Uvicorn, Psycopg 3, Pydantic |
| Frontend | React, Vite, JavaScript, Recharts |
| Database | PostgreSQL |
| Integration | GitHub API |
| Dev Tools | VS Code, Git, GitHub |

## Project Structure

```text
CodePulse/
│
├── backend/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── database.py
│   └── main.py
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── api/
│       ├── components/
│       ├── data/
│       ├── App.jsx
│       └── main.jsx
│
├── .gitignore
└── README.md
```

## Backend Modules

**Users** — manages CodePulse accounts and per-user settings.

**Repositories** — stores the GitHub repositories a user has connected to CodePulse.

**Events** — the raw feed: commits, pull requests, issues, and reviews as they come in from GitHub.

**Daily Metrics** — the first layer of processing: commit counts, PR activity, focus score, and context-switch score per day.

**Weekly Health** — the rollup layer: weekly health score, burnout-risk flag, and a written summary.

**AI Runs** — a record of every AI analysis execution, including the input snapshot that was sent, the output text that came back, which prompt version was used, and any evaluation notes. Keeping this history matters for debugging and for trusting the AI's output over time.

## GitHub Integration

CodePulse talks to the GitHub API to pull in repository and commit activity for connected repos. The main sync endpoint is:

```text
POST /github/sync
```

GitHub credentials are never hard-coded — they live in environment variables, kept out of source control entirely.

## AI Health Analysis

This is the layer that turns numbers into narrative. Rather than just reporting "12 commits, 3 PRs," the AI analysis step looks at patterns across:

- Overall developer health
- Focus quality
- Context switching
- Burnout-risk signals
- General activity patterns

The result is a short, human-readable summary that shows up right on the dashboard next to the raw numbers.

## Database Schema

CodePulse runs on PostgreSQL. The core tables:

| Table | Purpose |
|---|---|
| `users` | Account and settings data |
| `repos` | Connected GitHub repositories |
| `events` | Raw commit/PR/issue/review activity |
| `daily_metrics` | Per-day computed metrics |
| `weekly_health` | Weekly health score and burnout flag |
| `ai_runs` | History of AI analysis executions |

Application data lives in the database; secrets and connection details stay in environment variables, not in the schema or the code.

## Frontend Dashboard

The React frontend is a single-page dashboard built around a login flow and persistent auth. Once you're in, you get:

- Developer metric cards
- A health card and health score gauge
- An AI-generated summary
- An activity overview
- A daily activity chart and a health trend chart
- A logout flow that actually works

Everything talks to the FastAPI backend over a straightforward REST API.

## Getting Started

### Requirements

**Software:**
- Windows, Linux, or macOS
- Python 3.13 (or a compatible version)
- Node.js and npm
- PostgreSQL
- Git
- A GitHub account, for the GitHub integration

**Hardware:**
Nothing special — any modern machine that can run Python, Node.js, PostgreSQL, and a browser will do.

### 1. Clone the repo

```bash
git clone https://github.com/Tejaswi-C-2008/codepulse-github-test.git
cd codepulse-github-test
```

### 2. Set up the backend

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Then install the backend dependencies (per whatever's listed in the backend's requirements file).

### 3. Configure environment variables

Create a `backend/.env` file and fill in your database and GitHub credentials there. `.env` is already excluded via `.gitignore` — keep it that way, and never commit it.

### 4. Set up the database

Create the PostgreSQL database CodePulse will use, then point `backend/.env` at it.

### 5. Run the backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

### 6. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

- Frontend: `http://localhost:5173/`

## API Health Checks

```text
GET /
GET /health
GET /db-health
```

Expected responses:

```json
{"message": "CodePulse API is running"}
```

```json
{"status": "healthy"}
```

```json
{"database": "connected"}
```

## Testing & Verification

Version 1 was verified through backend checks, API testing, frontend validation, and a full build pass.

**Frontend:**

```bash
npm run lint
npm run build
```

**Backend:**

```bash
python -m compileall .\backend
```

Worth noting: the project currently relies on script-style checks for several models and services rather than a full pytest suite, so don't expect (or advertise) complete automated test coverage yet.

## Security & Privacy

- All sensitive configuration lives in environment variables, not in code.
- `.env` is excluded from version control via `.gitignore`.
- Secrets are never committed to the repository.
- GitHub credentials are stored securely, not hard-coded.
- Only the GitHub activity that's actually needed is synced — nothing extra.
- Raw sensitive data is never surfaced directly on the dashboard.

## Known Limitations

- AI-generated insights are only as good as the underlying activity data — sparse or noisy data means less useful analysis.
- GitHub integration currently covers the activity types implemented in Version 1, not the full range of what GitHub exposes.
- This is a development/demo build, not a hardened production service.
- Automated checks are script-style rather than a complete pytest suite.

## Roadmap

Ideas for where this could go next:

- More advanced burnout prediction
- Support for more GitHub activity types
- IDE telemetry integration
- CI/CD activity integration
- Deeper AI analysis
- Personalized productivity recommendations
- Manager/team-level dashboards
- Production-grade authentication
- Background job processing
- Cloud deployment
- Broader automated test coverage
- Better user-controlled data storage and privacy controls

## Demo Walkthrough

A quick sequence for showing CodePulse off:

1. Start PostgreSQL.
2. Start the FastAPI backend.
3. Start the React frontend.
4. Open the login page.
5. Log in.
6. Walk through the dashboard.
7. Explain the health score and metric cards.
8. Show the activity and health trend charts.
9. Show the AI health summary.
10. Trigger a GitHub sync.
11. Log out and back in to show session persistence.

## Project Status

**Version 1 — Implementation Complete**

Backend, database integration, GitHub integration, AI health analysis, the React dashboard, authentication, API integration, and verification work are all in place for this first version.

## Contributing

<!-- TODO: add contribution guidelines here if you're accepting outside contributions (branch naming, PR process, code style, etc.) -->

## License

<!-- TODO: add a license (MIT, Apache 2.0, etc.) and reference it here — GitHub will show a "no license" warning until you do -->

## Repository

```text
https://github.com/Tejaswi-C-2008/codepulse-github-test
```

---

CodePulse is an attempt to treat developer well-being as a first-class metric instead of an afterthought — combining activity, health signals, and AI analysis into one place that's meant to encourage sustainable work, not just more of it.
