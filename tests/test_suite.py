#!/usr/bin/env python3
"""
Test suite for GitHub Release Log Generator
"""

import unittest
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.github_release_generator.config import Config, GitHubRequest, CommitDiff, AnalysisResult
from src.github_release_generator.utils import GitHubUtils, EmailUtils, ReleaseLogUtils, ConfigValidator
from src.github_release_generator.email_service import EmailService

class TestConfig(unittest.TestCase):
    """Test configuration functionality"""
    
    def test_github_request_validation(self):
        """Test GitHubRequest validation"""
        # Valid request
        request = GitHubRequest(
            repository="owner/repo",
            from_commit="abc123",
            to_commit="def456",
            recipient_email="test@example.com"
        )
        self.assertEqual(request.repository, "owner/repo")
        self.assertEqual(request.from_commit, "abc123")
        self.assertEqual(request.to_commit, "def456")
        self.assertEqual(request.recipient_email, "test@example.com")

class TestGitHubUtils(unittest.TestCase):
    """Test GitHub utility functions"""
    
    def test_parse_repository_url(self):
        """Test repository URL parsing"""
        # Test different formats
        test_cases = [
            ("owner/repo", ("owner", "repo")),
            ("https://github.com/owner/repo", ("owner", "repo")),
            ("https://github.com/owner/repo/", ("owner", "repo")),
            ("git@github.com:owner/repo.git", ("owner", "repo")),
        ]
        
        for input_url, expected in test_cases:
            with self.subTest(input_url=input_url):
                result = GitHubUtils.parse_repository_url(input_url)
                self.assertEqual(result, expected)
    
    def test_validate_commit_sha(self):
        """Test commit SHA validation"""
        # Valid SHAs
        valid_shas = [
            "abc123",
            "1234567890abcdef",
            "1234567890abcdef1234567890abcdef12345678"
        ]
        
        for sha in valid_shas:
            with self.subTest(sha=sha):
                self.assertTrue(GitHubUtils.validate_commit_sha(sha))
        
        # Invalid SHAs
        invalid_shas = [
            "",
            "abc",
            "xyz123",  # contains non-hex characters
            "a" * 41,  # too long
        ]
        
        for sha in invalid_shas:
            with self.subTest(sha=sha):
                self.assertFalse(GitHubUtils.validate_commit_sha(sha))
    
    def test_shorten_sha(self):
        """Test SHA shortening"""
        long_sha = "1234567890abcdef1234567890abcdef12345678"
        short_sha = GitHubUtils.shorten_sha(long_sha, 7)
        self.assertEqual(short_sha, "1234567")

class TestEmailUtils(unittest.TestCase):
    """Test email utility functions"""
    
    def test_validate_email(self):
        """Test email validation"""
        # Valid emails
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "test+tag@example.org"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(EmailUtils.validate_email(email))
        
        # Invalid emails
        invalid_emails = [
            "",
            "invalid",
            "@example.com",
            "test@",
            "test.example.com"
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(EmailUtils.validate_email(email))
    
    def test_create_subject_line(self):
        """Test email subject line creation"""
        subject = EmailUtils.create_subject_line("owner/repo", "abc123def", "def456abc")
        self.assertIn("owner/repo", subject)
        self.assertIn("abc123d", subject)  # shortened SHA
        self.assertIn("def456a", subject)  # shortened SHA

class TestReleaseLogUtils(unittest.TestCase):
    """Test release log utility functions"""
    
    def test_categorize_file_changes(self):
        """Test file change categorization"""
        file_changes = [
            {"file_path": "src/main.py"},
            {"file_path": "tests/test_main.py"},
            {"file_path": "README.md"},
            {"file_path": "package.json"},
            {"file_path": "config.yaml"}
        ]
        
        categories = ReleaseLogUtils.categorize_file_changes(file_changes)
        
        self.assertIn("src/main.py", categories['source_code'])
        self.assertIn("tests/test_main.py", categories['tests'])
        self.assertIn("README.md", categories['documentation'])
        self.assertIn("package.json", categories['dependencies'])
        self.assertIn("config.yaml", categories['config'])
    
    def test_generate_version_suggestion(self):
        """Test version suggestion generation"""
        # Test breaking change
        commits_with_breaking = [
            {"message": "BREAKING: remove deprecated API"}
        ]
        version = ReleaseLogUtils.generate_version_suggestion([], commits_with_breaking)
        self.assertEqual(version, "major")
        
        # Test feature
        commits_with_feature = [
            {"message": "feat: add new feature"}
        ]
        version = ReleaseLogUtils.generate_version_suggestion([], commits_with_feature)
        self.assertEqual(version, "minor")

class TestConfigValidator(unittest.TestCase):
    """Test configuration validator functions"""
    
    def test_validate_github_token(self):
        """Test GitHub token validation"""
        # Valid tokens
        valid_tokens = [
            "ghp_1234567890abcdef1234567890abcdef123456",
            "gho_1234567890abcdef1234567890abcdef123456"
        ]
        
        for token in valid_tokens:
            with self.subTest(token=token):
                self.assertTrue(ConfigValidator.validate_github_token(token))
        
        # Invalid tokens
        invalid_tokens = [
            "",
            "invalid_token",
            "ghp_short"
        ]
        
        for token in invalid_tokens:
            with self.subTest(token=token):
                self.assertFalse(ConfigValidator.validate_github_token(token))
    
    def test_validate_openai_key(self):
        """Test OpenAI key validation"""
        # Valid key
        valid_key = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"
        self.assertTrue(ConfigValidator.validate_openai_key(valid_key))
        
        # Invalid keys
        invalid_keys = [
            "",
            "invalid_key",
            "sk-short"
        ]
        
        for key in invalid_keys:
            with self.subTest(key=key):
                self.assertFalse(ConfigValidator.validate_openai_key(key))
    
    def test_validate_smtp_config(self):
        """Test SMTP configuration validation"""
        # Valid config
        issues = ConfigValidator.validate_smtp_config("smtp.gmail.com", 587, "user", "pass")
        self.assertEqual(len(issues), 0)
        
        # Invalid config
        issues = ConfigValidator.validate_smtp_config("", 0, "", "")
        self.assertGreater(len(issues), 0)

class TestEmailService(unittest.TestCase):
    """Test email service functionality"""
    
    def test_create_html_email(self):
        """Test HTML email creation"""
        email_service = EmailService()
        release_log = "# Release v1.0\n\n## Features\n- New feature"
        html = email_service.create_html_email(release_log, "owner/repo")
        
        self.assertIn("Release v1.0", html)
        self.assertIn("owner/repo", html)
        self.assertIn("<html>", html)
    
    def test_create_release_log_subject(self):
        """Test release log subject creation"""
        email_service = EmailService()
        subject = email_service.create_release_log_subject("owner/repo", "1.0.0")
        
        self.assertIn("owner/repo", subject)
        self.assertIn("1.0.0", subject)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    @patch('config.Config.validate_config')
    def test_config_validation(self, mock_validate):
        """Test configuration validation"""
        mock_validate.return_value = True
        config = Config()
        self.assertTrue(config.validate_config())

def run_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  🧪 Running GitHub Release Log Generator Tests")
    print("="*60)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    # Add current test cases
    suite.addTest(unittest.TestLoader().loadTestsFromModule(sys.modules[__name__]))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("  ✅ ALL TESTS PASSED!")
    else:
        print("  ❌ SOME TESTS FAILED!")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    print("="*60)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_tests())
