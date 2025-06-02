import json
import logging
from typing import Any, Dict, List, Optional
import httpx
import asyncio
from github import Github
from github.Repository import Repository
from github.Commit import Commit
from .config import Config, CommitDiff, AnalysisResult

logger = logging.getLogger(__name__)

class GitHubMCPServer:
    """MCP Server for GitHub integration"""
    
    def __init__(self):
        self.github = Github(Config.GITHUB_TOKEN)
        self.config = Config()
    
    def parse_repository(self, repository: str) -> str:
        """Parse repository string to owner/repo format"""
        if repository.startswith("https://github.com/"):
            return repository.replace("https://github.com/", "").rstrip("/")
        elif "/" in repository:
            return repository
        else:
            raise ValueError("Invalid repository format. Use 'owner/repo' or full GitHub URL")
    
    def get_repository(self, repo_name: str) -> Repository:
        """Get GitHub repository object"""
        try:
            return self.github.get_repo(repo_name)
        except Exception as e:
            logger.error(f"Error accessing repository {repo_name}: {e}")
            raise
    
    def get_commit_diff(self, repo: Repository, from_commit: str, to_commit: str) -> List[CommitDiff]:
        """Get differences between two commits"""
        try:
            # Get the comparison between commits
            comparison = repo.compare(from_commit, to_commit)
            
            file_changes = []
            for file in comparison.files:
                diff = CommitDiff(
                    file_path=file.filename,
                    additions=file.additions,
                    deletions=file.deletions,
                    changes=file.patch or "",
                    status=file.status
                )
                file_changes.append(diff)
            
            return file_changes
        except Exception as e:
            logger.error(f"Error getting commit diff: {e}")
            raise
    
    def get_commits_info(self, repo: Repository, from_commit: str, to_commit: str) -> List[Dict[str, Any]]:
        """Get commit information between two commits"""
        try:
            commits = repo.compare(from_commit, to_commit).commits
            commit_info = []
            
            for commit in commits:
                info = {
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": commit.commit.author.name,
                    "date": commit.commit.author.date.isoformat(),
                    "url": commit.html_url
                }
                commit_info.append(info)
            
            return commit_info
        except Exception as e:
            logger.error(f"Error getting commits info: {e}")
            raise
    
    def analyze_repository_changes(self, repository: str, from_commit: str, to_commit: str) -> AnalysisResult:
        """Analyze changes between two commits in a repository"""
        try:
            # Parse repository name
            repo_name = self.parse_repository(repository)
            
            # Get repository object
            repo = self.get_repository(repo_name)
            
            # Get file changes
            file_changes = self.get_commit_diff(repo, from_commit, to_commit)
            
            # Get commits information
            commits_info = self.get_commits_info(repo, from_commit, to_commit)
            
            # Calculate totals
            total_files_changed = len(file_changes)
            total_additions = sum(change.additions for change in file_changes)
            total_deletions = sum(change.deletions for change in file_changes)
            
            # Create summary
            summary = f"Analysis of {repo_name} from {from_commit[:8]} to {to_commit[:8]}:\n"
            summary += f"- {total_files_changed} files changed\n"
            summary += f"- {total_additions} additions, {total_deletions} deletions\n"
            summary += f"- {len(commits_info)} commits analyzed"
            
            return AnalysisResult(
                repository=repo_name,
                from_commit=from_commit,
                to_commit=to_commit,
                total_files_changed=total_files_changed,
                total_additions=total_additions,
                total_deletions=total_deletions,
                file_changes=file_changes,
                summary=summary
            )
            
        except Exception as e:
            logger.error(f"Error analyzing repository changes: {e}")
            raise
    
    def get_repository_info(self, repository: str) -> Dict[str, Any]:
        """Get basic repository information"""
        try:
            repo_name = self.parse_repository(repository)
            repo = self.get_repository(repo_name)
            
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "url": repo.html_url,
                "default_branch": repo.default_branch
            }
        except Exception as e:
            logger.error(f"Error getting repository info: {e}")
            raise

# Global instance
github_mcp = GitHubMCPServer()
