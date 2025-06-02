#!/usr/bin/env python3
"""
Setup and installation script for GitHub Release Log Generator
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    return True

def setup_environment():
    """Set up environment configuration"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Setting up environment configuration...")
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from .env.example")
        print("⚠️  Please edit .env file with your actual credentials")
        return True
    elif env_file.exists():
        print("✅ Environment file already exists")
        return True
    else:
        print("❌ No .env.example file found")
        return False

def create_directories():
    """Create necessary directories"""
    dirs = ["logs", "temp"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Created directory: {dir_name}")

def verify_installation():
    """Verify that the installation is working"""
    print("🧪 Verifying installation...")
    try:
        # Try importing main modules
        import crewai
        import github
        import dotenv
        print("✅ All main dependencies imported successfully")
        
        # Check configuration
        from config import Config
        config = Config()
        print("✅ Configuration module loaded successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("  🚀 GitHub Release Log Generator - Setup")
    print("="*70)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Incompatible Python version")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        return 1
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup failed: Could not setup environment")
        return 1
    
    # Create directories
    create_directories()
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Setup failed: Installation verification failed")
        return 1
    
    print("\n" + "="*70)
    print("  ✅ SETUP COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\n📝 Next steps:")
    print("1. Edit .env file with your credentials:")
    print("   - OPENAI_API_KEY")
    print("   - GITHUB_TOKEN")
    print("   - Email settings (SMTP_USERNAME, SMTP_PASSWORD, etc.)")
    print("\n2. Run the application:")
    print("   - Command line: python main.py --help")
    print("   - Web interface: python web_app.py")
    print("   - Demo: python demo.py")
    print("\n🎉 Happy release log generating!")
    print("="*70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
