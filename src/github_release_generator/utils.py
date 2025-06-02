#!/usr/bin/env python3
"""
Utility functions and helpers for the GitHub Release Log Generator
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class GitHubUtils:
    """Utility functions for GitHub operations"""
    
    @staticmethod
    def parse_repository_url(repo_input: str) -> tuple[str, str]:
        """Parse repository input and return owner, repo"""
        # Remove trailing slash
        repo_input = repo_input.rstrip('/')
        
        # Handle full GitHub URLs
        if repo_input.startswith('https://github.com/'):
            repo_input = repo_input.replace('https://github.com/', '')
        elif repo_input.startswith('git@github.com:'):
            repo_input = repo_input.replace('git@github.com:', '').replace('.git', '')
        
        # Split owner/repo
        if '/' in repo_input:
            parts = repo_input.split('/')
            if len(parts) >= 2:
                return parts[0], parts[1]
        
        raise ValueError(f"Invalid repository format: {repo_input}")
    
    @staticmethod
    def validate_commit_sha(sha: str) -> bool:
        """Validate that a string looks like a git commit SHA"""
        if not sha:
            return False
        
        # Git SHAs are 40 characters of hexadecimal (full) or at least 4-40 chars (abbreviated)
        if len(sha) < 4 or len(sha) > 40:
            return False
        
        # Check if all characters are hexadecimal
        return all(c in '0123456789abcdefABCDEF' for c in sha)
    
    @staticmethod
    def shorten_sha(sha: str, length: int = 7) -> str:
        """Shorten a SHA to specified length"""
        return sha[:length] if len(sha) > length else sha

class EmailUtils:
    """Utility functions for email operations"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def create_subject_line(repository: str, from_commit: str, to_commit: str) -> str:
        """Create a descriptive subject line for the email"""
        short_from = GitHubUtils.shorten_sha(from_commit)
        short_to = GitHubUtils.shorten_sha(to_commit)
        return f"🚀 Release Log: {repository} ({short_from}→{short_to})"

class ReleaseLogUtils:
    """Utility functions for release log processing"""
    
    @staticmethod
    def categorize_file_changes(file_changes: List[Dict]) -> Dict[str, List[str]]:
        """Categorize file changes by type"""
        categories = {
            'source_code': [],
            'tests': [],
            'documentation': [],
            'config': [],
            'dependencies': [],
            'other': []
        }
        
        for change in file_changes:
            file_path = change.get('file_path', '')
            
            # Categorize based on file path and extension
            if any(pattern in file_path for pattern in ['/test/', '_test.', '.test.', '/tests/', 'spec.']) or \
               file_path.startswith('test/') or file_path.startswith('tests/') or \
               '/test/' in file_path or '/tests/' in file_path:
                categories['tests'].append(file_path)
            elif any(file_path.endswith(ext) for ext in ['.md', '.txt', '.rst', '.adoc']):
                categories['documentation'].append(file_path)
            elif any(pattern in file_path for pattern in ['package.json', 'requirements.txt', 'Gemfile', 'pom.xml', 'build.gradle']):
                categories['dependencies'].append(file_path)
            elif any(file_path.endswith(ext) for ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.env']):
                categories['config'].append(file_path)
            elif any(file_path.endswith(ext) for ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rb', '.php', '.rs', '.swift']):
                categories['source_code'].append(file_path)
            else:
                categories['other'].append(file_path)
        
        return categories
    
    @staticmethod
    def generate_version_suggestion(file_changes: List[Dict], commits_info: List[Dict]) -> str:
        """Suggest version bump based on changes"""
        # Analyze commit messages for breaking changes
        breaking_keywords = ['BREAKING', 'breaking change', 'breaking:', 'major:']
        feature_keywords = ['feat:', 'feature:', 'add:', 'new:']
        
        has_breaking = False
        has_features = False
        
        for commit in commits_info:
            message = commit.get('message', '').lower()
            if any(keyword.lower() in message for keyword in breaking_keywords):
                has_breaking = True
            elif any(keyword.lower() in message for keyword in feature_keywords):
                has_features = True
        
        # Analyze file changes
        categories = ReleaseLogUtils.categorize_file_changes(file_changes)
        has_code_changes = len(categories['source_code']) > 0
        
        if has_breaking:
            return "major"
        elif has_features or has_code_changes:
            return "minor"
        else:
            return "patch"

class ConfigValidator:
    """Configuration validation utilities"""
    
    @staticmethod
    def validate_github_token(token: str) -> bool:
        """Validate GitHub token format"""
        if not token:
            return False
        
        # GitHub tokens start with specific prefixes
        valid_prefixes = ['ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_']
        return any(token.startswith(prefix) for prefix in valid_prefixes) and len(token) > 10
    
    @staticmethod
    def validate_openai_key(key: str) -> bool:
        """Validate OpenAI API key format"""
        if not key:
            return False
        
        # OpenAI keys start with 'sk-' and are about 51 characters
        return key.startswith('sk-') and len(key) > 40
    
    @staticmethod
    def validate_smtp_config(host: str, port: int, username: str, password: str) -> List[str]:
        """Validate SMTP configuration and return list of issues"""
        issues = []
        
        if not host:
            issues.append("SMTP host is required")
        
        if not (1 <= port <= 65535):
            issues.append("SMTP port must be between 1 and 65535")
        
        if not username:
            issues.append("SMTP username is required")
        
        if not password:
            issues.append("SMTP password is required")
        
        return issues

class FileUtils:
    """File operation utilities"""
    
    @staticmethod
    def ensure_directory(path: Path) -> None:
        """Ensure directory exists, create if not"""
        path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def save_json(data: Any, file_path: Path) -> bool:
        """Save data as JSON file"""
        try:
            FileUtils.ensure_directory(file_path.parent)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Error saving JSON to {file_path}: {e}")
            return False
    
    @staticmethod
    def load_json(file_path: Path) -> Optional[Any]:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON from {file_path}: {e}")
            return None

class DateUtils:
    """Date and time utilities"""
    
    @staticmethod
    def format_datetime(dt: datetime, format_type: str = 'iso') -> str:
        """Format datetime in various formats"""
        if format_type == 'iso':
            return dt.isoformat()
        elif format_type == 'human':
            return dt.strftime('%B %d, %Y at %I:%M %p')
        elif format_type == 'date_only':
            return dt.strftime('%Y-%m-%d')
        else:
            return str(dt)
    
    @staticmethod
    def get_current_timestamp() -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
