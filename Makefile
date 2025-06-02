# Makefile for GitHub Release Log Generator

.PHONY: help install setup test demo clean web cli lint format check-deps health

# Default target
help:
	@echo "GitHub Release Log Generator - Available Commands:"
	@echo ""
	@echo "Setup and Installation:"
	@echo "  install      Install all dependencies"
	@echo "  setup        Run complete project setup"
	@echo "  check-deps   Check for required dependencies"
	@echo ""
	@echo "Running the Application:"
	@echo "  web          Start web interface (http://localhost:5000)"
	@echo "  cli          Show command line usage help"
	@echo "  demo         Run demonstration script"
	@echo ""
	@echo "Development:"
	@echo "  test         Run test suite"
	@echo "  lint         Run code linting"
	@echo "  format       Format code with black"
	@echo "  health       Check system health"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean        Clean temporary files"
	@echo "  logs         Show recent logs"
	@echo ""
	@echo "Examples:"
	@echo "  make install                    # Install dependencies"
	@echo "  make web                        # Start web interface"
	@echo "  make demo                       # Run demo"
	@echo "  make cli ARGS='--help'          # Show CLI help"

# Installation and Setup
install:
	@echo "🔄 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed successfully"

setup:
	@echo "🚀 Running project setup..."
	python setup.py
	@echo "✅ Setup completed"

check-deps:
	@echo "🔍 Checking dependencies..."
	@python -c "import sys; print(f'Python {sys.version}')"
	@python -c "import crewai; print(f'CrewAI {crewai.__version__}')" 2>/dev/null || echo "❌ CrewAI not installed"
	@python -c "import github; print('✅ PyGithub available')" 2>/dev/null || echo "❌ PyGithub not installed"
	@python -c "import flask; print('✅ Flask available')" 2>/dev/null || echo "❌ Flask not installed"
	@python -c "import dotenv; print('✅ python-dotenv available')" 2>/dev/null || echo "❌ python-dotenv not installed"

# Running the Application
web:
	@echo "🌐 Starting web interface..."
	@echo "Visit http://localhost:5000"
	python web_app.py

cli:
	@echo "💻 Command Line Interface:"
	python main.py $(ARGS)

demo:
	@echo "🎯 Running demonstration..."
	python demo.py

# Development and Testing
test:
	@echo "🧪 Running test suite..."
	python test_suite.py

lint:
	@echo "🔍 Running code linting..."
	@python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics 2>/dev/null || echo "⚠️  flake8 not installed, skipping lint check"
	@python -m pylint *.py 2>/dev/null || echo "⚠️  pylint not installed, skipping lint check"

format:
	@echo "🎨 Formatting code..."
	@python -m black . 2>/dev/null || echo "⚠️  black not installed, skipping code formatting"

health:
	@echo "🏥 Checking system health..."
	@python -c "from config import Config; c = Config(); print('✅ Configuration valid' if c.validate_config() else '❌ Configuration invalid')"
	@python -c "import requests; requests.get('https://api.github.com').raise_for_status(); print('✅ GitHub API accessible')" 2>/dev/null || echo "❌ GitHub API not accessible"
	@test -f .env && echo "✅ Environment file exists" || echo "⚠️  No .env file found"

# Maintenance
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup completed"

logs:
	@echo "📋 Recent logs:"
	@test -f release_log_generator.log && tail -20 release_log_generator.log || echo "No log file found"

# Advanced targets
requirements-update:
	@echo "📦 Updating requirements..."
	pip freeze > requirements.txt
	@echo "✅ Requirements updated"

backup-config:
	@echo "💾 Backing up configuration..."
	@test -f .env && cp .env .env.backup.$(shell date +%Y%m%d_%H%M%S) && echo "✅ Configuration backed up" || echo "❌ No .env file to backup"

# Development helpers
dev-install:
	@echo "🛠️  Installing development dependencies..."
	pip install black flake8 pylint pytest
	@echo "✅ Development dependencies installed"

# Quick start for new users
quick-start: install setup
	@echo ""
	@echo "🎉 Quick start completed!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit .env file with your credentials"
	@echo "2. Run 'make demo' to test the system"
	@echo "3. Run 'make web' to start the web interface"
	@echo ""

# Production targets
prod-check:
	@echo "🔒 Production readiness check..."
	@python -c "from config import Config; c = Config(); exit(0 if c.validate_config() else 1)" && echo "✅ Configuration valid for production" || echo "❌ Configuration not ready for production"
	@test -f .env && echo "✅ Environment file exists" || echo "❌ Environment file missing"
	@python -c "import ssl; print('✅ SSL support available')" 2>/dev/null || echo "❌ SSL support not available"
