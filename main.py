#!/usr/bin/env python3
"""
GitHub Release Log Generator
A multi-agent system using CrewAI and MCP server
"""

import logging
import sys
import asyncio
from typing import Optional
import argparse
from src.github_release_generator.crew import create_release_log_crew
from src.github_release_generator.config import GitHubRequest, Config
from src.github_release_generator.email_service import email_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('release_log_generator.log')
    ]
)

logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate release logs from GitHub repository commits"
    )
    parser.add_argument(
        '--repository', '-r',
        required=True,
        help='GitHub repository (owner/repo or full URL)'
    )
    parser.add_argument(
        '--from-commit', '-f',
        required=True,
        help='Source commit SHA'
    )
    parser.add_argument(
        '--to-commit', '-t',
        required=True,
        help='Target commit SHA'
    )
    parser.add_argument(
        '--email', '-e',
        required=True,
        help='Recipient email address'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    return parser.parse_args()

def get_interactive_input() -> GitHubRequest:
    """Get input from user interactively"""
    print("\n" + "="*60)
    print("  GitHub Release Log Generator")
    print("="*60)
    print()
    
    repository = input("Enter GitHub repository (owner/repo or full URL): ").strip()
    from_commit = input("Enter source commit SHA: ").strip()
    to_commit = input("Enter target commit SHA: ").strip()
    recipient_email = input("Enter recipient email address: ").strip()
    
    return GitHubRequest(
        repository=repository,
        from_commit=from_commit,
        to_commit=to_commit,
        recipient_email=recipient_email
    )

def validate_environment():
    """Validate that the environment is properly configured"""
    config = Config()
    
    if not config.validate_config():
        print("\n❌ Configuration Error!")
        print("Missing required environment variables. Please check your .env file.")
        print("\nRequired variables:")
        print("- OPENAI_API_KEY")
        print("- GITHUB_TOKEN")
        print("- SMTP_USERNAME")
        print("- SMTP_PASSWORD")
        print("- FROM_EMAIL")
        print("\nCopy .env.example to .env and fill in your values.")
        return False
    
    return True

def print_success_message(result: dict):
    """Print success message with results"""
    print("\n" + "="*60)
    print("  ✅ SUCCESS!")
    print("="*60)
    print(f"Repository: {result['repository']}")
    print(f"From Commit: {result['from_commit']}")
    print(f"To Commit: {result['to_commit']}")
    print(f"Email Sent To: {result['recipient_email']}")
    print("\nThe release log has been generated and sent successfully!")
    print("="*60)

def print_error_message(result: dict):
    """Print error message"""
    print("\n" + "="*60)
    print("  ❌ ERROR!")
    print("="*60)
    print(f"Repository: {result['repository']}")
    print(f"Error: {result['message']}")
    print("="*60)

async def main():
    """Main application entry point"""
    try:
        # Validate environment
        if not validate_environment():
            return 1
        
        # Parse arguments
        args = parse_arguments()
        
        # Get request details
        if args.interactive:
            request = get_interactive_input()
        else:
            request = GitHubRequest(
                repository=args.repository,
                from_commit=args.from_commit,
                to_commit=args.to_commit,
                recipient_email=args.email
            )
        
        # Display request info
        print(f"\n🚀 Starting release log generation...")
        print(f"Repository: {request.repository}")
        print(f"From: {request.from_commit}")
        print(f"To: {request.to_commit}")
        print(f"Email: {request.recipient_email}")
        print()
        
        # Create crew and process request
        crew = create_release_log_crew()
        result = await asyncio.get_event_loop().run_in_executor(
            None, crew.process_request, request
        )
        
        # Display results
        if result['status'] == 'success':
            print_success_message(result)
            return 0
        else:
            print_error_message(result)
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
