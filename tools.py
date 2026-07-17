from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# ==========================
# Web Search Tool
# ==========================

@tool
def web_search(query: str) -> str:
    """
    Search the web using Tavily and return the most relevant sources.
    """

    try:
        results = tavily.search(
            query=query,
            search_depth="advanced",
            topic="general",
            max_results=5
        )

        output = []

        for idx, result in enumerate(results["results"], start=1):
            output.append(
                f"""
Source {idx}

Title: {result.get("title", "N/A")}

URL: {result.get("url", "N/A")}

Snippet:
{result.get("content", "")[:400]}
"""
            )

        return "\n" + ("-" * 80 + "\n").join(output)

    except Exception as e:
        return f"Web search failed: {str(e)}"


# ==========================
# URL Scraper Tool
# ==========================

@tool
def scrape_url(url: str) -> str:
    """
    Scrape readable text from a webpage.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary HTML tags
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "noscript",
            "svg"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if len(text) < 200:
            return f"Very little content could be extracted from: {url}"

        return text[:5000]

    except requests.exceptions.Timeout:
        return f"Timeout while scraping: {url}"

    except requests.exceptions.RequestException as e:
        return f"Failed to access {url}: {str(e)}"

    except Exception as e:
        return f"Scraping failed: {str(e)}"