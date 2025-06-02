from crewai import Agent
from crewai.tools import BaseTool
from typing import Any, Dict
from pydantic import BaseModel, Field
import json
from mcp_server import github_mcp
from config import Config

class GitHubAnalyzerTool(BaseTool):
    """Tool for analyzing GitHub repository changes"""
    name: str = "github_analyzer"
    description: str = "Analyzes changes between two commits in a GitHub repository"

    def _run(self, repository: str, from_commit: str, to_commit: str) -> str:
        """Execute the GitHub analysis"""
        try:
            result = github_mcp.analyze_repository_changes(repository, from_commit, to_commit)
            return json.dumps(result.dict(), indent=2)
        except Exception as e:
            return f"Error analyzing repository: {str(e)}"

class RepositoryInfoTool(BaseTool):
    """Tool for getting repository information"""
    name: str = "repository_info"
    description: str = "Gets basic information about a GitHub repository"

    def _run(self, repository: str) -> str:
        """Get repository information"""
        try:
            info = github_mcp.get_repository_info(repository)
            return json.dumps(info, indent=2)
        except Exception as e:
            return f"Error getting repository info: {str(e)}"

def create_github_analyzer_agent():
    """Create the GitHub Analyzer Agent"""
    return Agent(
        role="GitHub Repository Analyzer",
        goal="Analyze GitHub repositories and extract detailed information about changes between commits",
        backstory="""You are an expert in version control systems and GitHub repositories. 
        You specialize in analyzing code changes, commit differences, and repository structures.
        Your primary responsibility is to fetch and analyze data from GitHub repositories,
        providing detailed insights about what has changed between different commits.""",
        tools=[GitHubAnalyzerTool(), RepositoryInfoTool()],
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )

def create_code_analysis_agent():
    """Create the Code Analysis Agent"""
    return Agent(
        role="Code Change Analyst",
        goal="Analyze code changes and categorize them into features, bug fixes, and breaking changes",
        backstory="""You are a senior software engineer with expertise in code review and analysis.
        You excel at understanding code changes, identifying patterns, and categorizing modifications
        into meaningful categories like new features, bug fixes, performance improvements, and breaking changes.
        You can read code diffs and understand the impact of changes on the overall system.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )

def create_release_log_generator_agent():
    """Create the Release Log Generator Agent"""
    return Agent(
        role="Release Log Generator",
        goal="Generate comprehensive and well-formatted release logs from analyzed code changes",
        backstory="""You are a technical writer specializing in software release documentation.
        You excel at creating clear, concise, and informative release logs that help users understand
        what has changed in a software release. You organize information logically and write in a way
        that is accessible to both technical and non-technical audiences.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )

def create_email_sender_agent():
    """Create the Email Sender Agent"""
    return Agent(
        role="Email Communication Specialist",
        goal="Format and send professional email notifications with release logs",
        backstory="""You are a communication specialist who excels at creating professional,
        well-formatted emails. You understand how to present technical information in an accessible way
        and ensure that email communications are clear, engaging, and properly formatted for business use.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
