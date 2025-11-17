# agents/fetcher_agent.py
# Fetches AI news from NewsAPI

import os
import json
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from utils.logger import setup_logger

# Setup logger
logger = setup_logger("fetcher_agent")

load_dotenv()

# Optional: import config values if you prefer centralized config
try:
    from config.settings import NEWS_API_KEY, TOPIC
except Exception:
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    TOPIC = os.getenv("TOPIC", "Artificial Intelligence")

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"


def _save_raw(response_json: dict, fname: str = "latest_fetch.json"):
    """Save raw NewsAPI response for debugging."""
    path = CACHE_DIR / fname
    with path.open("w", encoding="utf-8") as f:
        json.dump(response_json, f, ensure_ascii=False, indent=2)
    logger.info(f"Raw response saved to {path}")


def run_fetcher(
    query: str = None,
    page_size: int = 10,
    from_days: int = 2,
    language: str = "en",
) -> List[Dict]:
    """
    Fetch news articles from NewsAPI.org.

    Returns:
        List of dicts with keys: title, description, url, source, publishedAt, content
    """
    logger.info("🚀 Fetcher started")

    if query is None:
        query = TOPIC or "Artificial Intelligence"
    logger.info(f"Fetching news for topic: {query}")

    if not NEWS_API_KEY:
        logger.error("NEWS_API_KEY not found in environment.")
        raise RuntimeError("NEWS_API_KEY environment variable not set. Add it to your .env")

    # Limit time window to reduce noisy old results
    dt_from = (datetime.now(timezone.utc) - timedelta(days=from_days)).isoformat()

    params = {
        "q": query,
        "pageSize": page_size,
        "language": language,
        "sortBy": "publishedAt",
        # "from": dt_from,  # Uncomment if needed
    }

    headers = {"Authorization": NEWS_API_KEY}

    try:
        resp = requests.get(NEWSAPI_ENDPOINT, params=params, headers=headers, timeout=15)
        logger.info("NewsAPI request sent successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to call NewsAPI: {e}")
        raise RuntimeError(f"Failed to call NewsAPI: {e}")

    if resp.status_code != 200:
        logger.error(f"NewsAPI returned error {resp.status_code}: {resp.text}")
        raise RuntimeError(f"NewsAPI returned status {resp.status_code}: {resp.text}")

    data = resp.json()
    _save_raw(data)

    articles = data.get("articles", [])
    logger.info(f"Fetched {len(articles)} articles from NewsAPI.")

    cleaned = []
    for a in articles:
        cleaned.append({
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "source": a.get("source", {}).get("name"),
            "publishedAt": a.get("publishedAt"),
            "content": a.get("content"),
        })

    logger.info(f"✅ Fetcher completed. {len(cleaned)} articles cleaned and returned.")
    return cleaned


# Quick manual test
if __name__ == "__main__":
    print("Running fetcher_agent test...")
    try:
        items = run_fetcher(page_size=5)
        print(f"Fetched {len(items)} articles.")
        if items:
            print("First article:")
            print("Title:", items[0]["title"])
            print("URL:", items[0]["url"])
    except Exception as e:
        print("Error:", e)
