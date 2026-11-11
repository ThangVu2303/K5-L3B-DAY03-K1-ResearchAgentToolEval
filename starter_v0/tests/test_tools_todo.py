"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    options = ["Twitter/X", "Web"]
    result = TOOL_FUNCTIONS["clarify"](question="Bạn muốn tìm ở đâu?", response_type="choice", options=options)

    assert result["options"] == ["Twitter/X", "Web"]
    assert result["response_type"] == "choice"
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "a1", "url": "https://a.com/1", "section": "A"},
        {"title": "b1", "url": "https://b.com/1", "section": "B"},
        {"title": "a2", "url": "https://a.com/2", "section": "A"},
    ]
    markdown = TOOL_FUNCTIONS["format"](items=items, template="sections")["markdown"]

    assert markdown.count("## A") == 1
    assert markdown.count("## B") == 1
    assert markdown.index("a2") < markdown.index("## B")  # a2 is grouped under A, before B


def test_format_thread_numbers_items() -> None:
    items = [{"title": f"Tin {i}", "url": f"https://example.com/{i}"} for i in range(3)]
    markdown = TOOL_FUNCTIONS["format"](items=items, template="thread")["markdown"]
    blocks = markdown.split("\n\n")

    assert [block.split(" ", 1)[0] for block in blocks] == ["1/", "2/", "3/"]


def test_format_empty_items_does_not_crash() -> None:
    for empty in (None, []):
        result = TOOL_FUNCTIONS["format"](items=empty, template="sections")
        assert result["item_count"] == 0
        assert isinstance(result["markdown"], str)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    calls = fake_http(FakeResponse({"ok": True}))

    result = TOOL_FUNCTIONS["send"](text="Bản tin AI", confirmed=True)

    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "123:fake-token" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "-100123"
    assert calls[0]["json"]["text"] == "Bản tin AI"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))

    result = TOOL_FUNCTIONS["send"](text="Bản tin AI", confirmed=True)

    assert calls == []
    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))

    result = TOOL_FUNCTIONS["lookup"](query="AI", timeframe=None)

    assert "time_range" not in calls[0]["json"]
    assert calls[0]["json"]["query"] == "AI"
    assert result["items"] == []


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    calls = fake_http(FakeResponse({"data": {
        "markdown": "Nội dung bài viết",
        "metadata": {"title": "T", "sourceURL": "https://www.example.com/post"},
    }}))

    result = TOOL_FUNCTIONS["fetch"](url="https://www.example.com/post")

    assert calls[0]["url"] == "https://api.firecrawl.dev/v1/scrape"
    assert calls[0]["json"]["url"] == "https://www.example.com/post"
    assert result["items"][0] == {
        "title": "T",
        "url": "https://www.example.com/post",
        "source": "example.com",
        "summary": "Nội dung bài viết",
    }


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    fake_http(FakeResponse({"data": {"markdown": "x" * 5000, "metadata": {}}}))

    result = TOOL_FUNCTIONS["fetch"](url="https://example.com/long")

    assert len(result["items"][0]["summary"]) == 4000
    assert result["items"][0]["title"] == "https://example.com/long"  # falls back to url without title


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "rapid-test")
    raw = [{"text": "no id", "screen_name": "karpathy"}]
    raw += [{"tweet_id": str(i), "screen_name": "karpathy", "text": f"tweet {i}"} for i in range(6)]
    calls = fake_http(FakeResponse({"timeline": raw}))

    result = TOOL_FUNCTIONS["timeline"](screenname="karpathy", limit=3)

    assert calls[0]["params"] == {"screenname": "karpathy"}
    assert len(result["items"]) == 3
    assert [item["url"] for item in result["items"]] == [
        f"https://x.com/karpathy/status/{i}" for i in range(3)
    ]


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "rapid-test")
    calls = fake_http(FakeResponse({"timeline": []}))

    result = TOOL_FUNCTIONS["social_search"](query="OpenAI", search_type="Top")

    assert calls[0]["url"].endswith("/search.php")
    assert calls[0]["params"] == {"query": "OpenAI", "search_type": "Top"}
    assert calls[0]["headers"]["x-rapidapi-key"] == "rapid-test"
    assert result["search_type"] == "Top"


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    for query in ("", "   ", "và của"):  # empty, whitespace, only stopwords
        result = TOOL_FUNCTIONS["policy"](query=query)
        assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = TOOL_FUNCTIONS["policy"](query="API key customer data prompt", policy_area="data_privacy", top_k=5)

    assert result["results"], "expected at least one data_privacy hit"
    assert {hit["policy_area"] for hit in result["results"]} == {"data_privacy"}


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = TOOL_FUNCTIONS["policy"](query="injection probe viral tweet citation", policy_area="source_citation", top_k=10)
    probe = [hit for hit in result["results"] if hit["section"] == "Injection probe"]

    assert probe, "expected the 'Injection probe' section to be returned"
    assert any("viral tweet" in line for line in probe[0]["untrusted_text"])
    assert "viral tweet" not in probe[0]["facts"]
    assert "untrusted" in result["trust_boundary"]


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

@pytest.mark.parametrize("sort_by,endpoint", [("relevance", "search"), ("date", "search_by_date")])
def test_hn_search_happy_path_maps_stories_and_request(fake_http, sort_by, endpoint) -> None:
    from conftest import FakeResponse
    from tools import TOOL_FUNCTIONS

    calls = fake_http(FakeResponse({"hits": [
        {"objectID": "101", "title": "AI agents", "url": "https://example.com/agents",
         "author": "alice", "created_at": "2026-01-01T00:00:00Z", "points": 12, "num_comments": 3},
        {"objectID": "102", "title": "Ask HN: Agents", "url": None},
        {"objectID": "103", "title": "Extra result", "url": "https://example.com/extra"},
    ]}))

    result = TOOL_FUNCTIONS["hn_search"](query="  AI agents  ", max_results=2, sort_by=sort_by)

    assert len(calls) == 1
    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == f"https://hn.algolia.com/api/v1/{endpoint}"
    assert calls[0]["params"] == {"query": "AI agents", "tags": "story", "hitsPerPage": 2}
    assert calls[0]["timeout"] > 0
    assert result["tool"] == "hn_search"
    assert result["query"] == "AI agents"
    assert result["sort_by"] == sort_by
    assert len(result["items"]) == 2
    assert result["items"][0] == {
        "title": "AI agents", "url": "https://example.com/agents", "source": "example.com",
        "summary": "AI agents", "hn_url": "https://news.ycombinator.com/item?id=101",
        "author": "alice", "date": "2026-01-01T00:00:00Z", "metrics": {"points": 12, "comments": 3},
    }
    assert result["items"][1]["url"] == "https://news.ycombinator.com/item?id=102"
    digest = TOOL_FUNCTIONS["format"](items=result["items"], template="bullets")
    assert "AI agents" in digest["markdown"]
    assert "https://example.com/agents" in digest["markdown"]


@pytest.mark.parametrize("kwargs", [
    {}, {"query": ""}, {"query": "   "}, {"query": None}, {"query": ["AI"]},
    {"query": "AI", "max_results": 0}, {"query": "AI", "max_results": 21},
    {"query": "AI", "max_results": True}, {"query": "AI", "max_results": 1.5},
    {"query": "AI", "max_results": "5"}, {"query": "AI", "sort_by": "Top"},
    {"query": "AI", "sort_by": []},
])
def test_hn_search_bad_input_returns_error_without_network(fake_http, kwargs) -> None:
    from conftest import FakeResponse
    from tools import TOOL_FUNCTIONS

    calls = fake_http(FakeResponse({"hits": []}))
    result = TOOL_FUNCTIONS["hn_search"](**kwargs)

    assert result["tool"] == "hn_search"
    assert result["error"] == "ValueError"
    assert result["message"]
    assert calls == []


@pytest.mark.parametrize("failure", [429, 500, "timeout"])
def test_hn_search_request_failure_returns_error_dict(fake_http, failure) -> None:
    import requests
    from conftest import FakeResponse
    from tools import TOOL_FUNCTIONS

    response = requests.Timeout("request timed out") if failure == "timeout" else FakeResponse(status_code=failure)
    calls = fake_http(response)
    result = TOOL_FUNCTIONS["hn_search"](query="AI")

    assert len(calls) == 1
    assert result["tool"] == "hn_search"
    assert result["error"] == ("Timeout" if failure == "timeout" else "HTTPError")
    assert result["message"]


def test_hn_search_empty_and_invalid_hits_do_not_create_fake_stories(fake_http) -> None:
    from conftest import FakeResponse
    from tools import TOOL_FUNCTIONS

    fake_http(FakeResponse({"hits": [None, {}, {"objectID": "bad", "title": "Bad ID"},
                                      {"objectID": "104", "title": "  "}]}))
    assert TOOL_FUNCTIONS["hn_search"](query="AI")["items"] == []


@pytest.mark.parametrize("payload", [[], {}, {"hits": None}])
def test_hn_search_malformed_response_returns_error_dict(fake_http, payload) -> None:
    from conftest import FakeResponse
    from tools import TOOL_FUNCTIONS

    fake_http(FakeResponse(payload))
    result = TOOL_FUNCTIONS["hn_search"](query="AI")
    assert result["error"] == "ValueError"


@pytest.mark.parametrize("bad_url", ["https://[invalid", "javascript:alert(1)", "https://", None, 42])
def test_hn_search_invalid_story_url_falls_back_without_losing_other_hits(fake_http, bad_url) -> None:
    fake_http(FakeResponse({"hits": [
        {"objectID": "201", "title": "Story with invalid URL", "url": bad_url},
        {"objectID": "202", "title": "Valid story", "url": "https://example.com/valid"},
    ]}))

    result = TOOL_FUNCTIONS["hn_search"](query="AI", max_results=2)

    assert "error" not in result
    assert len(result["items"]) == 2
    assert result["items"][0]["url"] == "https://news.ycombinator.com/item?id=201"
    assert result["items"][0]["source"] == "news.ycombinator.com"
    assert result["items"][1]["url"] == "https://example.com/valid"
