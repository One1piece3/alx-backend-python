#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
import sys
import os

# 🔧 Fix imports (ajoute le parent directory au sys.path)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client import GithubOrgClient
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=unittest.mock.PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url returns expected value"""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}

        client = GithubOrgClient("test")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/test/repos")


if __name__ == "__main__":
    unittest.main()
