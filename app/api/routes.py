from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from ..utils.github import github_api
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api")

@router.post("/activity/")
async def get_repository_activity(org_name: str, repo_names: str):
    try:
        repos = [repo.strip() for repo in repo_names.split(",")]
        results = {}
        
        for repo in repos:
            activity = await github_api.get_repository_activity(org_name, repo)
            
            # Check for errors in the response
            if isinstance(activity, dict) and "error" in activity:
                if "rate limit" in activity["error"].lower():
                    raise HTTPException(
                        status_code=429,
                        detail="GitHub API rate limit reached. Please try again later."
                    )
                return JSONResponse(
                    status_code=400,
                    content={"detail": activity["error"], "repo": repo}
                )
            
            results[repo] = activity
                
        return JSONResponse(status_code=200, content=results)
        
    except Exception as e:
        if "rate limit" in str(e).lower():
            raise HTTPException(
                status_code=429,
                detail="GitHub API rate limit reached. Please try again later."
            )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze repositories: {str(e)}"
        )
