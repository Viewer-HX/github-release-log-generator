import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # GitHub Configuration
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    # Email Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "")
    
    # MCP Server Configuration
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        required_fields = [
            cls.OPENAI_API_KEY,
            cls.GITHUB_TOKEN,
            cls.SMTP_USERNAME,
            cls.SMTP_PASSWORD,
            cls.FROM_EMAIL
        ]
        return all(field for field in required_fields)

class GitHubRequest(BaseModel):
    """GitHub analysis request model"""
    repository: str = Field(..., description="GitHub repository (owner/repo or full URL)")
    from_commit: str = Field(..., description="Source commit SHA")
    to_commit: str = Field(..., description="Target commit SHA")
    recipient_email: str = Field(..., description="Email to send the release log to")

class CommitDiff(BaseModel):
    """Commit difference model"""
    file_path: str
    additions: int
    deletions: int
    changes: str
    status: str  # added, modified, removed

class AnalysisResult(BaseModel):
    """Analysis result model"""
    repository: str
    from_commit: str
    to_commit: str
    total_files_changed: int
    total_additions: int
    total_deletions: int
    file_changes: list[CommitDiff]
    summary: str
    
class ReleaseLog(BaseModel):
    """Release log model"""
    version: str
    date: str
    repository: str
    summary: str
    features: list[str]
    bug_fixes: list[str]
    breaking_changes: list[str]
    technical_details: str
