#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        # valeur de retour simulée
        mock_get_json.return_value = {"org": org_name}

        # Création du client
        client = GithubOrgClient(org_name)
        result = client.org

        # Vérifications
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)  # get_json appelé une seule fois
        self.assertEqual(result, {"org": org_name})  # Résultat attendu


if __name__ == "__main__":
    unittest.main()
