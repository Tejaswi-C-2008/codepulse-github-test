import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from psycopg.types.json import Jsonb

from backend.models.github import GitHubRepository
from backend.database import get_connection

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

GITHUB_API_URL = "https://api.github.com"


def get_github_headers():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError("GITHUB_TOKEN is not configured")

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


def get_github_user():
    response = requests.get(
        f"{GITHUB_API_URL}/user",
        headers=get_github_headers(),
        timeout=10,
    )

    response.raise_for_status()

    return response.json()

def get_github_repositories():
    response = requests.get(
        f"{GITHUB_API_URL}/user/repos",
        headers=get_github_headers(),
        params={
            "per_page": 100,
            "sort": "updated",
        },
        timeout=10,
    )

    response.raise_for_status()

    repositories = response.json()

    return [
        GitHubRepository(
            id=repo["id"],
            name=repo["name"],
            full_name=repo["full_name"],
            html_url=repo["html_url"],
            private=repo["private"],
            description=repo.get("description"),
        )
        for repo in repositories
    ]

def save_github_repositories(user_id, repositories):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            saved_count = 0

            for repo in repositories:
                cursor.execute(
                    """
                    INSERT INTO repos (
                        user_id,
                        github_repo_id,
                        name,
                        url
                    )
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (github_repo_id)
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        url = EXCLUDED.url
                    """,
                    (
                        user_id,
                        repo.id,
                        repo.name,
                        repo.html_url,
                    ),
                )

                saved_count += 1

            connection.commit()

            return saved_count

    finally:
        connection.close()

def get_github_commits(owner, repo):
    response = requests.get(
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits",
        headers=get_github_headers(),
        params={
            "per_page": 100,
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()

def import_github_commits(user_id, repo_id, owner, repo):
    commits = get_github_commits(owner, repo)

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            imported_count = 0

            for commit in commits:
                sha = commit["sha"]
                message = commit["commit"]["message"]
                author_name = commit["commit"]["author"]["name"]
                author_date = commit["commit"]["author"]["date"]

                timestamp = datetime.fromisoformat(
                    author_date.replace("Z", "+00:00")
                ).replace(tzinfo=None)

                cursor.execute(
                    """
                    INSERT INTO events (
                        user_id,
                        repo_id,
                        type,
                        timestamp,
                        payload
                    )
                    SELECT %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM events
                        WHERE payload->>'github_sha' = %s
                    )
                    """,
                    (
                        user_id,
                        repo_id,
                        "commit",
                        timestamp,
                        Jsonb({
                            "github_sha": sha,
                            "message": message,
                            "author": author_name,
                            "repository": f"{owner}/{repo}",
                        }),
                        sha,
                    ),
                )

                if cursor.rowcount > 0:
                    imported_count += 1

            connection.commit()

            return imported_count

    finally:
        connection.close()

def get_github_pull_requests(owner, repo):
    response = requests.get(
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls",
        headers=get_github_headers(),
        params={
            "state": "all",
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()

def import_github_pull_requests(user_id, repo_id, owner, repo):
    pull_requests = get_github_pull_requests(owner, repo)

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            imported_count = 0

            for pr in pull_requests:
                pr_number = pr["number"]
                title = pr["title"]
                state = pr["state"]
                author = pr["user"]["login"]
                created_at = pr["created_at"]
                html_url = pr["html_url"]

                timestamp = datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                ).replace(tzinfo=None)

                cursor.execute(
                    """
                    INSERT INTO events (
                        user_id,
                        repo_id,
                        type,
                        timestamp,
                        payload
                    )
                    SELECT %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM events
                        WHERE payload->>'github_pr_key' = %s
                    )
                    """,
                    (
                        user_id,
                        repo_id,
                        "pr",
                        timestamp,
                        Jsonb({
                            "github_pr_key": f"{owner}/{repo}#{pr_number}",
                            "github_pr_number": pr_number,
                            "title": title,
                            "state": state,
                            "author": author,
                            "repository": f"{owner}/{repo}",
                            "url": html_url,
                        }),
                        f"{owner}/{repo}#{pr_number}",
                    ),
                )

                if cursor.rowcount > 0:
                    imported_count += 1

            connection.commit()

            return imported_count

    finally:
        connection.close()

def get_github_issues(owner, repo):
    response = requests.get(
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues",
        headers=get_github_headers(),
        params={
            "state": "all",
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
        },
        timeout=10,
    )

    response.raise_for_status()

    issues = response.json()

    # GitHub's issues endpoint also returns pull requests.
    # Keep only actual issues.
    return [
        issue for issue in issues
        if "pull_request" not in issue
    ]

def import_github_issues(user_id, repo_id, owner, repo):
    issues = get_github_issues(owner, repo)

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            imported_count = 0

            for issue in issues:
                issue_number = issue["number"]
                title = issue["title"]
                state = issue["state"]
                author = issue["user"]["login"]
                created_at = issue["created_at"]
                html_url = issue["html_url"]

                timestamp = datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                ).replace(tzinfo=None)

                cursor.execute(
                    """
                    INSERT INTO events (
                        user_id,
                        repo_id,
                        type,
                        timestamp,
                        payload
                    )
                    SELECT %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM events
                        WHERE payload->>'github_issue_key' = %s
                    )
                    """,
                    (
                        user_id,
                        repo_id,
                        "issue",
                        timestamp,
                        Jsonb({
                            "github_issue_key": f"{owner}/{repo}#{issue_number}",
                            "github_issue_number": issue_number,
                            "title": title,
                            "state": state,
                            "author": author,
                            "repository": f"{owner}/{repo}",
                            "url": html_url,
                        }),
                        f"{owner}/{repo}#{issue_number}",
                    ),
                )

                if cursor.rowcount > 0:
                    imported_count += 1

            connection.commit()

            return imported_count

    finally:
        connection.close()

def get_github_reviews(owner, repo, pull_number):
    response = requests.get(
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pull_number}/reviews",
        headers=get_github_headers(),
        params={
            "per_page": 100,
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()

def import_github_reviews(user_id, repo_id, owner, repo, pull_number):
    reviews = get_github_reviews(owner, repo, pull_number)

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            imported_count = 0

            for review in reviews:
                review_id = review["id"]
                state = review["state"]
                reviewer = review["user"]["login"]
                submitted_at = review.get("submitted_at")

                if not submitted_at:
                    continue

                timestamp = datetime.fromisoformat(
                    submitted_at.replace("Z", "+00:00")
                ).replace(tzinfo=None)

                cursor.execute(
                    """
                    INSERT INTO events (
                        user_id,
                        repo_id,
                        type,
                        timestamp,
                        payload
                    )
                    SELECT %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM events
                        WHERE payload->>'github_review_key' = %s
                    )
                    """,
                    (
                        user_id,
                        repo_id,
                        "review",
                        timestamp,
                        Jsonb({
                            "github_review_key": f"{owner}/{repo}#PR{pull_number}-REVIEW{review_id}",
                            "github_review_id": review_id,
                            "pull_request_number": pull_number,
                            "state": state,
                            "reviewer": reviewer,
                            "repository": f"{owner}/{repo}",
                        }),
                        f"{owner}/{repo}#PR{pull_number}-REVIEW{review_id}",
                    ),
                )

                if cursor.rowcount > 0:
                    imported_count += 1

            connection.commit()

            return imported_count

    finally:
        connection.close()

def import_all_github_reviews(user_id, repo_id, owner, repo):
    pull_requests = get_github_pull_requests(owner, repo)

    imported_count = 0

    for pr in pull_requests:
        imported_count += import_github_reviews(
            user_id,
            repo_id,
            owner,
            repo,
            pr["number"],
        )

    return imported_count

def sync_github_repository(user_id, repo_id, owner, repo):
    commits_imported = import_github_commits(
        user_id,
        repo_id,
        owner,
        repo,
    )

    pull_requests_imported = import_github_pull_requests(
        user_id,
        repo_id,
        owner,
        repo,
    )

    issues_imported = import_github_issues(
        user_id,
        repo_id,
        owner,
        repo,
    )

    reviews_imported = import_all_github_reviews(
        user_id,
        repo_id,
        owner,
        repo,
    )

    return {
        "commits_imported": commits_imported,
        "pull_requests_imported": pull_requests_imported,
        "issues_imported": issues_imported,
        "reviews_imported": reviews_imported,
    }