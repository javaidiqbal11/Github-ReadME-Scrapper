import requests
import re


class GithubReadmeScraper:
    """
    Handles scraping README content from a GitHub repository.
    """

    @staticmethod
    def scrape_readme(repo_url: str) -> str:
        """
        Scrapes the README content from a GitHub repository.
        :param repo_url: URL of the GitHub repository.
        :return: README content as a string.
        """
        match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)
        if not match:
            raise ValueError("Invalid GitHub repository URL. Please ensure the URL is correct.")

        owner, repo = match.groups()
        api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        headers = {"Accept": "application/vnd.github.v3.raw"}

        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch README. Status code: {response.status_code}")
