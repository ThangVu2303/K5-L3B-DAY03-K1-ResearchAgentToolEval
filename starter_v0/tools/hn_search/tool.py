from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import requests

from tools._shared import TIMEOUT, domain, err


def hn_search(query: str = "", max_results: int = 5, sort_by: str = "relevance") -> dict[str, Any]:
    """Search Hacker News stories through the public Algolia API."""
    try:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if isinstance(max_results, bool) or not isinstance(max_results, int) or not 1 <= max_results <= 20:
            raise ValueError("max_results must be an integer between 1 and 20")
        if not isinstance(sort_by, str) or sort_by not in ("relevance", "date"):
            raise ValueError("sort_by must be relevance or date")

        query = query.strip()
        endpoint = "search_by_date" if sort_by == "date" else "search"
        response = requests.get(
            f"https://hn.algolia.com/api/v1/{endpoint}",
            params={"query": query, "tags": "story", "hitsPerPage": max_results},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict) or not isinstance(payload.get("hits"), list):
            raise ValueError("Hacker News response must contain a hits list")

        items: list[dict[str, Any]] = []
        for hit in payload["hits"]:
            if not isinstance(hit, dict):
                continue
            story_id = str(hit.get("objectID", ""))
            title = hit.get("title")
            if not story_id.isascii() or not story_id.isdigit() or not isinstance(title, str) or not title.strip():
                continue
            hn_url = f"https://news.ycombinator.com/item?id={story_id}"
            url = hn_url
            candidate = hit.get("url")
            if isinstance(candidate, str):
                try:
                    parsed = urlparse(candidate)
                except ValueError:
                    parsed = None
                if parsed is not None and parsed.scheme in ("http", "https") and parsed.netloc:
                    url = candidate
            items.append({
                "title": title.strip(),
                "url": url,
                "source": domain(url),
                "summary": title.strip(),
                "hn_url": hn_url,
                "author": hit.get("author"),
                "date": hit.get("created_at"),
                "metrics": {"points": hit.get("points"), "comments": hit.get("num_comments")},
            })
            if len(items) >= max_results:
                break
        return {"tool": "hn_search", "query": query, "sort_by": sort_by, "max_results": max_results, "items": items}
    except Exception as exc:
        return err("hn_search", exc)
