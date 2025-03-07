import requests
from typing import Dict, Any, Optional, List
from ..core.settings import settings
from fastapi import HTTPException
import aiohttp
import asyncio
from datetime import datetime
import time

class GitHubAPI:
    def __init__(self):
        self.base_url = settings.github_api_url
        self.headers = {
            "Authorization": f"token {settings.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = 0
        self.semaphore = asyncio.Semaphore(2)

    async def check_rate_limit(self):
        if self.rate_limit_remaining < 100:
            now = time.time()
            if now < self.rate_limit_reset:
                wait_time = self.rate_limit_reset - now
                await asyncio.sleep(wait_time)

    async def make_request(self, url: str) -> Dict:
        async with self.semaphore:
            await self.check_rate_limit()
            try:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(url) as response:
                        # Update rate limit info
                        self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 5000))
                        self.rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))

                        response_json = await response.json()

                        if response.status == 404:
                            return {"error": "Repository not found"}
                        elif response.status == 403:
                            return {"error": "Rate limit exceeded"}
                        elif response.status != 200:
                            error_message = response_json.get('message', f"GitHub API error: {response.status}")
                            return {"error": error_message}

                        return response_json
            except aiohttp.ClientError as e:
                return {"error": f"Network error: {str(e)}"}
            except Exception as e:
                return {"error": f"Request error: {str(e)}"}

    async def get_repository_activity(self, org_name: str, repo_name: str) -> Dict:
        try:
            # Get basic repo info
            repo_url = f"{self.base_url}/repos/{org_name}/{repo_name}"
            repo_data = await self.make_request(repo_url)
            
            if "error" in repo_data:
                return repo_data

            # Get commit statistics
            commits_url = f"{repo_url}/commits"
            commits_data = await self.make_request(commits_url)
            
            if "error" in commits_data:
                return commits_data

            # Get contributors
            contributors_url = f"{repo_url}/contributors"
            contributors_data = await self.make_request(contributors_url)

            # Get pull requests
            pulls_url = f"{repo_url}/pulls"
            pulls_data = await self.make_request(pulls_url)

            # Compile the data
            return {
                "total_commits": len(commits_data) if isinstance(commits_data, list) else 0,
                "open_issues": repo_data.get("open_issues_count", 0),
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "pull_requests": len(pulls_data) if isinstance(pulls_data, list) else 0,
                "contributors": [
                    {
                        "login": c.get("login"),
                        "commits": c.get("contributions", 0),
                        "avatar_url": c.get("avatar_url")
                    } for c in (contributors_data if isinstance(contributors_data, list) else [])
                ],
                "last_updated": repo_data.get("updated_at"),
                "commit_history": await self.get_commit_history(org_name, repo_name)
            }
        except Exception as e:
            return {"error": f"Failed to get repository activity: {str(e)}"}

    async def get_commit_history(self, org_name: str, repo_name: str) -> List[Dict]:
        try:
            url = f"{self.base_url}/repos/{org_name}/{repo_name}/stats/commit_activity"
            data = await self.make_request(url)
            
            if isinstance(data, list):
                # Convert the weekly data to a more readable format
                return [
                    {
                        "date": datetime.fromtimestamp(week["week"]).strftime("%Y-%m-%d"),
                        "count": week["total"]
                    } for week in data[-12:]  # Last 12 weeks
                ]
            return []
        except Exception:
            return []

github_api = GitHubAPI()

async def fetch_repo_activity(org_name: str, repo_name: str) -> Dict[str, Any]:
    """
    Fetch activity statistics for a GitHub repository
    """
    headers = {"Authorization": f"token {settings.github_token}"} if settings.github_token else {}
    
    try:
        response = requests.get(
            f"{settings.github_api_url}/repos/{org_name}/{repo_name}/stats/commit_activity",
            headers=headers
        )
        
        if response.status_code == 200:
            commit_data = response.json()
            total_commits = sum(week['total'] for week in commit_data)
            return {
                "total_commits": total_commits,
                "weekly_activity": commit_data
            }
        else:
            error_msg = response.json().get("message", "Unknown error")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"GitHub API error: {error_msg}"
            )
            
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch data: {str(e)}") 