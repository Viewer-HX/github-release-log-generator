#!/usr/bin/env python3
"""
System verification script for GitHub Release Log Generator
Performs comprehensive system checks and validation
"""

import sys
import os
import importlib
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description}")
        return False

def check_import(module_name, description):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}")
        return True
    except ImportError:
        print(f"❌ {description}")
        return False

def main():
    """Run system verification"""
    print("\n" + "="*60)
    print("  🔍 GitHub Release Log Generator - System Verification")
    print("="*60)
    
    all_good = True
    
    # Check core files
    print("\n📁 Core Files:")
    files_to_check = [
        ("main.py", "Main application entry point"),
        ("web_app.py", "Flask web interface"),
        ("src/github_release_generator/crew.py", "CrewAI orchestration"),
        ("src/github_release_generator/agents.py", "AI agent definitions"),
        ("src/github_release_generator/tasks.py", "Task definitions"),
        ("src/github_release_generator/mcp_server.py", "MCP server implementation"),
        ("src/github_release_generator/email_service.py", "Email service"),
        ("src/github_release_generator/config.py", "Configuration management"),
        ("src/github_release_generator/utils.py", "Utility functions"),
    ]
    
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # Check configuration files
    print("\n⚙️  Configuration Files:")
    config_files = [
        ("requirements.txt", "Python dependencies"),
        (".env.example", "Environment template"),
        ("README.md", "Project documentation"),
        ("docs/ARCHITECTURE.md", "Technical documentation"),
        ("Makefile", "Project automation"),
    ]
    
    for file_path, description in config_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # Check template files
    print("\n🌐 Web Interface:")
    template_files = [
        ("templates/", "Templates directory"),
        ("templates/index.html", "Web interface template"),
    ]
    
    for file_path, description in template_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # Check Python imports (optional dependencies)
    print("\n🐍 Python Dependencies:")
    dependencies = [
        ("dotenv", "Environment variable loading"),
        ("pydantic", "Data validation"),
        ("requests", "HTTP requests"),
        ("flask", "Web framework"),
        ("jinja2", "Template engine"),
    ]
    
    for module, description in dependencies:
        check_import(module, description)  # Don't mark as critical failure
    
    # Check CrewAI and specialized dependencies
    print("\n🤖 AI Dependencies:")
    ai_dependencies = [
        ("crewai", "CrewAI framework"),
        ("github", "PyGithub library"),
        ("openai", "OpenAI API client"),
    ]
    
    for module, description in ai_dependencies:
        if not check_import(module, description):
            all_good = False
    
    # Check environment setup
    print("\n🔧 Environment Setup:")
    if check_file_exists(".env", "Environment configuration"):
        print("   📝 Remember to configure your credentials in .env")
    else:
        print("   ⚠️  No .env file found - copy from .env.example and configure")
    
    # Final status
    print("\n" + "="*60)
    if all_good:
        print("  ✅ SYSTEM VERIFICATION PASSED!")
        print("="*60)
        print("\n🎉 Your GitHub Release Log Generator is ready to use!")
        print("\nNext steps:")
        print("1. Configure .env file with your credentials")
        print("2. Run 'make demo' to test the system")
        print("3. Run 'make web' to start the web interface")
        print("4. Run 'python main.py --help' for CLI usage")
    else:
        print("  ❌ SYSTEM VERIFICATION FAILED!")
        print("="*60)
        print("\n🔧 Please address the missing components above.")
        print("Run 'make install' to install dependencies.")
    
    print("\n" + "="*60)
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
