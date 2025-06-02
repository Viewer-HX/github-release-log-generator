#!/usr/bin/env python3
"""
Demo script for GitHub Release Log Generator
Demonstrates the system with example data
"""

import asyncio
import logging
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.github_release_generator.crew import create_release_log_crew
from src.github_release_generator.config import GitHubRequest, Config

# Configure logging for demo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_demo():
    """Run a demonstration of the release log generator"""
    
    print("\n" + "="*70)
    print("  🚀 GitHub Release Log Generator - DEMO")
    print("="*70)
    
    # Check configuration
    config = Config()
    if not config.validate_config():
        print("\n❌ Configuration Error!")
        print("Please set up your .env file with required credentials.")
        print("Copy .env.example to .env and fill in your values.")
        return
    
    # Demo request (you can modify these values)
    demo_request = GitHubRequest(
        repository="microsoft/vscode",  # Popular repo for demo
        from_commit="1.80.0",  # Example version tag
        to_commit="1.81.0",    # Example version tag
        recipient_email="demo@example.com"  # Change this to your email
    )
    
    print(f"\n📋 Demo Configuration:")
    print(f"Repository: {demo_request.repository}")
    print(f"From: {demo_request.from_commit}")
    print(f"To: {demo_request.to_commit}")
    print(f"Email: {demo_request.recipient_email}")
    
    # Ask for confirmation
    response = input("\n🤔 Would you like to run this demo? (y/N): ")
    if response.lower() != 'y':
        print("Demo cancelled.")
        return
    
    # Ask for email override
    email_override = input(f"\n📧 Enter your email address (or press Enter to use {demo_request.recipient_email}): ").strip()
    if email_override:
        demo_request.recipient_email = email_override
    
    print("\n🔄 Starting demo...")
    print("This may take a few minutes as the AI agents analyze the repository.")
    
    try:
        # Create crew and process request
        crew = create_release_log_crew()
        result = await asyncio.get_event_loop().run_in_executor(
            None, crew.process_request, demo_request
        )
        
        # Display results
        print("\n" + "="*70)
        if result['status'] == 'success':
            print("  ✅ DEMO COMPLETED SUCCESSFULLY!")
            print("="*70)
            print(f"✓ Repository analyzed: {result['repository']}")
            print(f"✓ Commits compared: {result['from_commit']} → {result['to_commit']}")
            print(f"✓ Email sent to: {result['recipient_email']}")
            print("\n📧 Check your email for the generated release log!")
        else:
            print("  ❌ DEMO FAILED!")
            print("="*70)
            print(f"Error: {result['message']}")
        print("="*70)
        
    except Exception as e:
        logger.error(f"Demo error: {e}")
        print(f"\n❌ Demo failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(run_demo())
