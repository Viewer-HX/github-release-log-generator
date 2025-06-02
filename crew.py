from crewai import Crew, Process
from crewai.tools import BaseTool
import logging
from typing import Dict, Any
import json
from agents import (
    create_github_analyzer_agent,
    create_code_analysis_agent,
    create_release_log_generator_agent,
    create_email_sender_agent
)
from tasks import (
    create_github_analysis_task,
    create_code_analysis_task,
    create_release_log_task,
    create_email_sending_task
)
from email_service import email_service
from config import Config, GitHubRequest

logger = logging.getLogger(__name__)

class EmailSenderTool(BaseTool):
    """Tool for sending emails with release logs"""
    name: str = "email_sender"
    description: str = "Sends email notifications with release logs"

    def _run(self, recipient_email: str, subject: str, release_log: str, repository: str) -> str:
        """Send email with release log"""
        try:
            success = email_service.send_email(
                recipient_email=recipient_email,
                subject=subject,
                release_log=release_log,
                repository=repository
            )
            
            if success:
                return f"Email successfully sent to {recipient_email} with subject: {subject}"
            else:
                return f"Failed to send email to {recipient_email}"
                
        except Exception as e:
            return f"Error sending email: {str(e)}"

class GitHubReleaseLogCrew:
    """Main crew orchestrator for GitHub release log generation"""
    
    def __init__(self):
        self.config = Config()
        
        # Validate configuration
        if not self.config.validate_config():
            raise ValueError("Missing required configuration. Please check your .env file.")
        
        # Create agents
        self.github_analyzer_agent = create_github_analyzer_agent()
        self.code_analysis_agent = create_code_analysis_agent()
        self.release_log_generator_agent = create_release_log_generator_agent()
        self.email_sender_agent = create_email_sender_agent()
        
        # Add email tool to the email sender agent
        self.email_sender_agent.tools.append(EmailSenderTool())
    
    def process_request(self, request: GitHubRequest) -> Dict[str, Any]:
        """Process a GitHub release log request"""
        try:
            logger.info(f"Processing request for repository: {request.repository}")
            
            # Create tasks
            github_task = create_github_analysis_task(
                self.github_analyzer_agent,
                request.repository,
                request.from_commit,
                request.to_commit
            )
            
            code_analysis_task = create_code_analysis_task(
                self.code_analysis_agent,
                "{{github_analysis_result}}"  # Will be replaced with actual result
            )
            code_analysis_task.context = [github_task]
            
            release_log_task = create_release_log_task(
                self.release_log_generator_agent,
                "{{code_analysis_result}}",  # Will be replaced with actual result
                request.repository
            )
            release_log_task.context = [code_analysis_task]
            
            email_task = create_email_sending_task(
                self.email_sender_agent,
                "{{release_log}}",  # Will be replaced with actual result
                request.recipient_email,
                request.repository
            )
            email_task.context = [release_log_task]
            
            # Create and execute crew
            crew = Crew(
                agents=[
                    self.github_analyzer_agent,
                    self.code_analysis_agent,
                    self.release_log_generator_agent,
                    self.email_sender_agent
                ],
                tasks=[
                    github_task,
                    code_analysis_task,
                    release_log_task,
                    email_task
                ],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the crew
            result = crew.kickoff()
            
            logger.info("Release log generation and email sending completed successfully")
            
            return {
                "status": "success",
                "message": "Release log generated and email sent successfully",
                "repository": request.repository,
                "from_commit": request.from_commit,
                "to_commit": request.to_commit,
                "recipient_email": request.recipient_email,
                "result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return {
                "status": "error",
                "message": f"Error processing request: {str(e)}",
                "repository": request.repository,
                "from_commit": request.from_commit,
                "to_commit": request.to_commit,
                "recipient_email": request.recipient_email
            }

def create_release_log_crew() -> GitHubReleaseLogCrew:
    """Factory function to create a new crew instance"""
    return GitHubReleaseLogCrew()
