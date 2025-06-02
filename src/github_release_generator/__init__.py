"""
GitHub Release Log Generator

A sophisticated multi-agent system using CrewAI and Model Context Protocol (MCP) 
server that automatically analyzes GitHub repository differences between commits, 
generates comprehensive release logs, and sends professional email notifications.
"""

__version__ = "1.0.0"
__author__ = "GitHub Release Generator Team"
__email__ = "contact@example.com"

from .crew import create_release_log_crew
from .config import Config, GitHubRequest
from .email_service import EmailService

__all__ = [
    "create_release_log_crew",
    "Config", 
    "GitHubRequest",
    "EmailService",
    "__version__",
]
