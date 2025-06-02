# 🚀 GitHub Release Log Generator

A sophisticated multi-agent system using CrewAI and Model Context Protocol (MCP) server that automatically analyzes GitHub repository differences between commits, generates comprehensive release logs, and sends professional email notifications.

## ✨ Features

- 🤖 **Multi-agent AI system** with specialized roles using CrewAI
- 📊 **GitHub integration** via MCP server for repository analysis
- 🔄 **Intelligent commit analysis** with automatic change categorization
- 📝 **Professional release logs** with markdown formatting
- 📧 **Automated email notifications** with HTML styling
- 🌐 **Web interface** for easy interaction
- 💻 **Command line interface** for automation
- 🧪 **Comprehensive testing** suite included

## 🤖 AI Agents

The system employs four specialized AI agents working in sequence:

1. **GitHub Analyzer Agent** 🔍
   - Fetches repository metadata and commit differences
   - Analyzes file changes and statistics
   - Provides structured data for further processing

2. **Code Analysis Agent** 🧠
   - Categorizes changes (features, bug fixes, breaking changes)
   - Assesses impact and significance of modifications
   - Recommends version bump strategies

3. **Release Log Generator Agent** ✍️
   - Creates comprehensive, well-formatted release logs
   - Organizes information into logical sections
   - Generates professional documentation

4. **Email Sender Agent** 📧
   - Formats content for email delivery
   - Sends professional notifications with HTML styling
   - Handles delivery confirmation and error reporting

## 🚀 Quick Start

### Using Makefile (Recommended)
```bash
# Complete setup in one command
make quick-start

# Edit your credentials
nano .env

# Run demonstration
make demo

# Start web interface
make web
```

### Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your credentials

# 3. Run setup script
python setup.py

# 4. Test the system
python demo.py
```

## 📋 Environment Configuration

Create a `.env` file with the following variables:

```bash
# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here

# Email Configuration (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com

# Server Configuration
MCP_SERVER_PORT=8000
```

### 🔑 Getting Required Credentials

**OpenAI API Key**:
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and navigate to API keys
3. Generate a new API key

**GitHub Token**:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Copy the token (starts with `ghp_`)

**Email Configuration**:
- For Gmail: Use App Passwords instead of your regular password
- For other providers: Check SMTP settings documentation

## 💻 Usage Options

### 1. Web Interface
```bash
make web
# or
python web_app.py
```
Visit `http://localhost:5000` for the user-friendly web interface.

### 2. Command Line
```bash
# Interactive mode
python main.py --interactive

# Direct parameters
python main.py \
  --repository "owner/repo" \
  --from-commit "abc123" \
  --to-commit "def456" \
  --email "user@example.com"
```

### 3. API Integration
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "owner/repo",
    "from_commit": "abc123",
    "to_commit": "def456",
    "recipient_email": "user@example.com"
  }'
```

## 📁 Project Structure

```
github_email_crew/
├── main.py              # Main CLI application
├── web_app.py           # Flask web interface
├── demo.py              # Demonstration script
├── setup.py             # Installation and setup
├── crew.py              # CrewAI orchestration
├── agents.py            # AI agent definitions
├── tasks.py             # Task definitions
├── mcp_server.py        # GitHub MCP server
├── email_service.py     # Email functionality
├── config.py            # Configuration management
├── utils.py             # Utility functions
├── test_suite.py        # Comprehensive tests
├── requirements.txt     # Python dependencies
├── Makefile            # Project automation
├── templates/
│   └── index.html       # Web interface template
├── ARCHITECTURE.md      # Technical documentation
└── README.md           # This file
```

## 🔧 Available Commands

Use the Makefile for convenient project management:

```bash
# Setup and Installation
make install           # Install dependencies
make setup            # Complete project setup
make check-deps       # Verify dependencies

# Running the Application
make web              # Start web interface
make cli              # Command line help
make demo             # Run demonstration

# Development
make test             # Run test suite
make lint             # Code quality checks
make format           # Code formatting
make health           # System health check

# Maintenance
make clean            # Remove temporary files
make logs             # View recent logs
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
make test
# or
python test_suite.py
```

Tests cover:
- Configuration validation
- GitHub utilities
- Email functionality
- Integration workflows
- Error handling

## 📊 Example Output

The system generates professional release logs like:

```markdown
# 🚀 Release Log: my-project v2.1.0
**Date**: June 1, 2025  
**Repository**: owner/my-project

## 📋 Summary
This release includes 15 commits with significant new features and bug fixes...

## ✨ New Features
- Added user authentication system
- Implemented real-time notifications
- Enhanced mobile responsiveness

## 🐛 Bug Fixes
- Fixed memory leak in data processing
- Resolved API timeout issues
- Corrected responsive layout bugs

## 🔧 Technical Details
- Updated dependencies to latest versions
- Improved error handling and logging
- Enhanced test coverage to 95%
```

## 🚨 Troubleshooting

### Common Issues

**Configuration Errors**:
```bash
make health  # Check system status
```

**GitHub API Issues**:
- Verify token has correct permissions
- Check rate limits (5000 requests/hour)

**Email Delivery Problems**:
- Verify SMTP settings
- For Gmail, use App Passwords
- Check firewall/network restrictions

**Import Errors**:
```bash
make check-deps  # Verify all dependencies
make install     # Reinstall if needed
```

## 🔒 Security Considerations

- Store credentials in `.env` file (never commit to git)
- Use GitHub tokens with minimal required permissions
- Enable 2FA on all accounts
- Regularly rotate API keys and tokens

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `make test`
4. Submit a pull request

## 📚 Documentation

- **Technical Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **API Documentation**: Available in code comments
- **Test Documentation**: See [test_suite.py](test_suite.py)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Run `make health` to diagnose problems
3. Review logs with `make logs`
4. Create an issue on GitHub for bugs or feature requests

---

**Made with ❤️ using CrewAI and MCP**
