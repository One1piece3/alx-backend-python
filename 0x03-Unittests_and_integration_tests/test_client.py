#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that org returns correct payload"""
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repos"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=unittest.mock.PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://fake-url.com"

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Vérifier que la liste correspond aux noms des repos
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Vérifier que _public_repos_url est appelé 1 fois
            mock_repos_url.assert_called_once()

            # Vérifier que get_json est appelé 1 fois avec l'URL mockée
            mock_get_json.assert_called_once_with("https://fake-url.com")
