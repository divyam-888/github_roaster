import asyncio
import aiohttp
import random
import os
from functools import lru_cache
from dotenv import load_dotenv

# Initialize environment variables at module load
load_dotenv()

# We pull the token once during boot. 
# If it's missing, we send empty headers, falling back to GitHub's unauthenticated 60 req/hr limit.
TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"


async def _fetch_json(session: aiohttp.ClientSession, url: str) -> dict | list | None:
    """
    Base async fetcher. Yields thread execution back to the event loop while waiting for GitHub's TCP response.
    """
    try:
        async with session.get(url, headers=HEADERS) as response:
            # Defensive programming: If we hit a 404 (user doesn't exist) or 403 (Rate Limit), fail gracefully.
            if response.status != 200:
                return None
            return await response.json()
    except aiohttp.ClientError:
        # Catch DNS or connection drops without crashing the server thread
        return None


async def _get_commits_for_repo(session: aiohttp.ClientSession, username: str, repo_name: str) -> list:
    """
    Fetches commit history for a single repo. Designed to be run concurrently.
    """
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    data = await _fetch_json(session, url)
    
    # API might return None or a dictionary (error message) instead of a list of commits
    if not data or isinstance(data, dict):
        return []

    # Randomize the payload to keep the AI roast fresh, capping at 10 to save LLM context window tokens
    if len(data) > 10:
        random.shuffle(data)
        data = data[:10]

    return [commit["commit"]["message"] for commit in data]


async def _build_user_profile(username: str) -> dict | None:
    """
    The core async orchestration engine. Implements the Scatter-Gather concurrency pattern.
    """
    # Open a single persistent TCP connection pool for all outbound requests in this lifecycle
    async with aiohttp.ClientSession() as session:
        
        # PHASE 1: SCATTER - Fetch user profile AND repos at the exact same time
        user_url = f"https://api.github.com/users/{username}"
        repos_url = f"https://api.github.com/users/{username}/repos"

        user_data, repos_data = await asyncio.gather(
            _fetch_json(session, user_url),
            _fetch_json(session, repos_url)
        )

        if not user_data:
            return None

        # Filter valid repos (ignore forks and empty repos to avoid wasting AI tokens)
        valid_repos = []
        if repos_data and isinstance(repos_data, list):
            valid_repos = [
                r["name"] for r in repos_data 
                if not r.get("fork") and r.get("size", 0) > 0
            ]

        random.shuffle(valid_repos)
        selected_repos = valid_repos[:5]

        # PHASE 2: SCATTER - Fire off up to 5 concurrent requests for commit histories
        commit_tasks = [
            _get_commits_for_repo(session, username, repo) 
            for repo in selected_repos
        ]
        
        # GATHER - Wait for all commit requests to resolve simultaneously
        commits_results = await asyncio.gather(*commit_tasks)
        commits_dict = {repo: commits for repo, commits in zip(selected_repos, commits_results)}

        # Assemble the final contract expected by main.py
        github_data = {
            "name": user_data.get("name"),
            "followers": user_data.get("followers"),
            "following": user_data.get("following"),
            "public_repos": user_data.get("public_repos"),
        }

        # Prevent injecting null keys into the prompt context window
        for field in ["bio", "location", "email"]:
            if user_data.get(field):
                github_data[field] = user_data.get(field)

        github_data["5_random_repos"] = selected_repos
        github_data["commits_of_5_random_repos"] = commits_dict

        return github_data


# -------------------------------------------------------------------------
# THE PUBLIC INTERFACE BOUNDARY
# -------------------------------------------------------------------------

@lru_cache(maxsize=128)
def get_github_user_data(username: str) -> dict | None:
    """
    Sync-to-Async Bridge & Caching Perimeter.
    
    1. LRU Cache: Bypasses network entirely if the username was queried recently. Max 128 users in RAM.
    2. Event Loop Runner: Streamlit is synchronous. This wrapper spins up an isolated event loop, 
       executes the async network logic, shuts down the loop, and returns standard Python objects.
       This allows us to optimize network latency without rewriting the entire Streamlit UI layer.
    """
    # Force lowercase to normalize cache keys (preventing duplicate network calls for "torvalds" vs "Torvalds")
    clean_username = username.strip().lower()
    return asyncio.run(_build_user_profile(clean_username))