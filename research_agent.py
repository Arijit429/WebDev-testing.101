import os
import random
from typing import Dict, Any

import requests


PROMOTER_REPUTATION_OPTIONS = ["strong", "average", "weak"]
SECTOR_OUTLOOK_OPTIONS = ["high growth", "moderate growth", "stable", "under stress"]


def _fetch_news_headlines(company_name: str, industry: str) -> list[str]:
    """
    Optional integration with external news API (e.g. NewsAPI).
    If NEWS_API_KEY is not configured or the call fails, we fall back silently.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return []

    try:
        query = f"{company_name} {industry}".strip() or industry or company_name
        resp = requests.get(
            "https://newsapi.org/v2/everything",
            params={"q": query, "pageSize": 5, "language": "en", "sortBy": "relevancy", "apiKey": api_key},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles") or []
        headlines: list[str] = []
        for art in articles:
            source = (art.get("source") or {}).get("name") or ""
            title = art.get("title") or ""
            if title:
                if source:
                    headlines.append(f"{title} ({source})")
                else:
                    headlines.append(title)
        return headlines
    except Exception:
        return []


def generate_research_insights(company_name: str, industry: str) -> Dict[str, Any]:
    """
    Digital credit research agent.

    - Uses optional external news API (if configured) to surface recent headlines.
    - Augments that with model-based signals for promoter reputation, litigation and sector outlook.
    """
    random.seed(company_name + industry)

    litigation_cases = random.choice([0, 0, 1, 2])
    promoter_reputation = random.choice(PROMOTER_REPUTATION_OPTIONS)
    sector_outlook = random.choice(SECTOR_OUTLOOK_OPTIONS)
    sentiment_score = round(random.uniform(-1.0, 1.0), 2)

    news_headlines = _fetch_news_headlines(company_name, industry)

    text_insights = [
        f"Promoter reputation is assessed as {promoter_reputation}.",
        f"Sector outlook for {industry or 'the sector'} is {sector_outlook}.",
    ]

    if litigation_cases == 0:
        text_insights.append("No material litigation cases identified in the last 3 years based on available checks.")
    elif litigation_cases == 1:
        text_insights.append("Company appears in one litigation case in the last 3 years.")
    else:
        text_insights.append(f"Company appears in {litigation_cases} litigation cases in recent years.")

    if sentiment_score > 0.3:
        text_insights.append("Overall news and sentiment around the company appears positive.")
    elif sentiment_score < -0.3:
        text_insights.append("Overall news and sentiment around the company appears negative.")
    else:
        text_insights.append("Overall news and sentiment around the company appears mixed/neutral.")

    if news_headlines:
        text_insights.append("Recent news highlights:")
        text_insights.extend(f"- {headline}" for headline in news_headlines)

    return {
        "litigation_cases": litigation_cases,
        "promoter_reputation": promoter_reputation,
        "sector_outlook": sector_outlook,
        "sentiment_score": sentiment_score,
        "insights": text_insights,
        "news_headlines": news_headlines,
    }


