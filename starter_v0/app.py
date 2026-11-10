"""Streamlit UI cho Research Agent.

Chạy (từ starter_v0/):  streamlit run app.py
Dùng lại vòng lặp gọi tool của chat.py và ghi transcript vào transcripts/ giống chat.py.
"""
from __future__ import annotations

import csv
import hashlib
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import (
    ARTIFACTS_DIR,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).parent
# Đọc lại .env mỗi lần Streamlit chạy lại script, để đổi key không cần khởi động lại.
load_lab_env(ROOT)

TRANSCRIPTS_DIR = ROOT / "transcripts"
PROVIDERS = ["gemini", "openrouter", "openai", "anthropic", "ollama"]
SAMPLE_QUESTIONS = [
    ("📰", "Tin AI hôm nay có gì nổi bật?"),
    ("🐦", "Mọi người đang bàn gì về GPT-5 trên Twitter?"),
    ("👤", "Lấy 5 tweet mới nhất của Andrej Karpathy"),
    ("🔗", "Tóm tắt bài này giúp mình: https://openai.com/research/"),
    ("📄", "Tìm paper arXiv về AI agent evaluation"),
    ("📣", "Đăng bản tin này lên Telegram giúp mình"),
]
USER_AVATAR = "🧑"
AGENT_AVATAR = "🔎"

st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="centered")

# ---------------- Style ----------------
st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; max-width: 860px; }
    .hero {
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, rgba(99,102,241,.18), rgba(14,165,233,.12));
        border: 1px solid rgba(99,102,241,.25);
    }
    .hero h1 { font-size: 1.8rem; margin: 0 0 .3rem 0; padding: 0; }
    .hero p { margin: 0; opacity: .85; }
    .badges { margin-top: .7rem; display: flex; flex-wrap: wrap; gap: .4rem; }
    .badge {
        font-size: .75rem; padding: .15rem .6rem; border-radius: 999px;
        background: rgba(127,127,127,.15); border: 1px solid rgba(127,127,127,.25);
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    .welcome { text-align: center; opacity: .8; margin: 1.2rem 0 .6rem 0; }
    div[data-testid="stButton"] button { border-radius: 12px; text-align: left; }
    .meta { font-size: .78rem; opacity: .65; margin-top: .2rem; }
    .tool-name { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Artifacts ----------------
system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
tools_path = ARTIFACTS_DIR / "tools.yaml"
system_prompt = system_prompt_path.read_text(encoding="utf-8")
tool_declarations = load_tool_declarations(tools_path)
openai_tools = to_openai_tools(tool_declarations)


def hash_variants(path: Path) -> set[str]:
    """Hash của file theo cả 2 kiểu xuống dòng (git trên Windows có thể đổi LF <-> CRLF)."""
    raw = path.read_bytes()
    lf = raw.replace(b"\r\n", b"\n")
    return {hashlib.sha256(data).hexdigest() for data in (raw, lf, lf.replace(b"\n", b"\r\n"))}


def detect_version_label() -> str:
    """Tìm version trong version_log.csv có cùng nội dung prompt/tools với file hiện tại."""
    prompt_hashes = hash_variants(system_prompt_path)
    tools_hashes = hash_variants(tools_path)
    log_path = ARTIFACTS_DIR / "version_log.csv"
    try:
        with log_path.open(encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
    except OSError:
        return "dev"

    def matches(logged: str | None, candidates: set[str]) -> bool:
        logged = (logged or "").strip()
        return bool(logged) and any(h.startswith(logged) for h in candidates)

    for row in reversed(rows):
        if matches(row.get("prompt_hash"), prompt_hashes) and matches(row.get("tools_hash"), tools_hashes):
            return (row.get("version") or "dev").strip()
    return "dev"  # prompt/tools chưa được ghi vào version_log

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### ⚙️ Cấu hình")
    provider_name = st.selectbox("Provider", PROVIDERS, index=0)
    model = st.text_input("Model", value="", placeholder="để trống = mặc định") or None
    version = st.text_input(
        "Version label",
        value=detect_version_label(),
        help="Tự điền theo version_log.csv (khớp prompt/tools hash). 'dev' = bản chưa ghi log.",
    )

    with st.expander("Nâng cao"):
        history_window = st.number_input("History window (cặp lượt)", 0, 20, 5)
        max_tool_rounds = st.number_input("Max tool rounds", 1, 8, 4)
        show_tools = st.toggle("Hiện tool calls + kết quả", value=True)

    with st.expander(f"🧰 Tool đang bật ({len(tool_declarations)})"):
        for item in tool_declarations:
            desc = (item.get("description") or "").strip().split("\n")[0]
            if len(desc) > 90:
                desc = desc[:87] + "..."
            st.markdown(f"<span class='tool-name'>{item['name']}</span> — {desc}", unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Cuộc trò chuyện mới", use_container_width=True):
        for key in ("messages", "history", "transcript", "transcript_path", "pending"):
            st.session_state.pop(key, None)
        st.rerun()

artifact_version = build_artifact_version(version, system_prompt_path, tools_path)


@st.cache_resource
def get_provider(name: str) -> Any:
    return make_provider(name)


try:
    provider = get_provider(provider_name)
except Exception as exc:  # thiếu SDK / provider sai
    st.error(f"Không khởi tạo được provider `{provider_name}`: {type(exc).__name__}: {exc}")
    st.stop()

selected_model = model or getattr(provider, "default_model", None)

# ---------------- Session state ----------------
if "transcript" not in st.session_state:
    transcript_id = "_".join([
        safe_slug(version), safe_slug(provider_name), "ui",
        datetime.now().strftime("%Y%m%dT%H%M%S%f"),
    ])
    st.session_state.transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": selected_model,
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": int(history_window),
        "max_tool_rounds": int(max_tool_rounds),
        "source": "streamlit_ui",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    st.session_state.messages = []  # để hiển thị
    st.session_state.history = []   # để gửi model

with st.sidebar:
    st.caption(f"📝 Transcript: `{st.session_state.transcript_path.name}`")

# ---------------- Header ----------------
st.markdown(
    f"""
    <div class="hero">
      <h1>🔎 Research Agent</h1>
      <p>Tìm tin trên web, đọc bài theo link, xem và tìm tweet, tra paper arXiv và policy công ty.
      Agent hỏi lại khi thiếu thông tin và xin xác nhận trước khi gửi.</p>
      <div class="badges">
        <span class="badge">{artifact_version.artifact_version}</span>
        <span class="badge">{provider_name} · {selected_model}</span>
        <span class="badge">{len(tool_declarations)} tools</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------- Rendering helpers ----------------
def short_error(text: str, limit: int = 180) -> str:
    first = text.split("{", 1)[0].strip() or text
    return first if len(first) <= limit else first[: limit - 3] + "..."


def event_status(event: dict[str, Any]) -> tuple[str, str]:
    result = event.get("result", {})
    if not isinstance(result, dict):
        return "✅", "ok"
    if "error" in result:
        return "⚠️", "lỗi"
    if result.get("awaiting_user"):
        return "❓", "hỏi lại"
    if result.get("status") == "needs_confirmation":
        return "✋", "cần xác nhận"
    return "✅", "ok"


def render_items(result: dict[str, Any]) -> None:
    items = result.get("items") or result.get("results") or []
    if not isinstance(items, list) or not items:
        return
    lines = []
    for item in items[:6]:
        if not isinstance(item, dict):
            continue
        title = (item.get("title") or item.get("section") or item.get("summary") or "").strip().replace("\n", " ")
        title = title[:110] + ("..." if len(title) > 110 else "")
        url = item.get("url") or ""
        source = item.get("source") or ""
        lines.append(f"- [{title}]({url}) · *{source}*" if url else f"- {title} · *{source}*")
    if lines:
        st.markdown("\n".join(lines))
    if len(items) > 6:
        st.caption(f"… và {len(items) - 6} mục khác")


def render_tool_events(events: list[dict[str, Any]]) -> None:
    for event in events:
        icon, label = event_status(event)
        result = event.get("result", {})
        args = json.dumps(event.get("args", {}), ensure_ascii=False)
        if len(args) > 80:
            args = args[:77] + "..."
        with st.expander(f"{icon} `{event.get('tool')}` {args} — {label}", expanded=(label == "lỗi")):
            # Không che lỗi tool: hiện thông báo lỗi và toàn bộ kết quả.
            if isinstance(result, dict) and "error" in result:
                st.error(f"{result.get('error')}: {result.get('message', '')}")
            elif isinstance(result, dict):
                render_items(result)
            st.markdown("**Args**")
            st.json(event.get("args", {}), expanded=True)
            st.markdown("**Kết quả (JSON)**")
            st.json(result, expanded=False)


def render_assistant(msg: dict[str, Any]) -> None:
    if msg.get("error"):
        st.error(f"**Lỗi provider:** {short_error(msg['error'])}")
        with st.expander("Chi tiết lỗi"):
            st.code(msg["error"], language=None)
    elif msg.get("status") == "waiting_for_user":
        st.info(f"❓ {msg['content']}")
    else:
        st.markdown(msg["content"] or "_(không có nội dung)_")
    if show_tools and msg.get("tool_events"):
        render_tool_events(msg["tool_events"])
    meta = msg.get("meta")
    if meta:
        st.markdown(f"<div class='meta'>{meta}</div>", unsafe_allow_html=True)


# ---------------- History ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar=AGENT_AVATAR):
            render_assistant(msg)

# ---------------- Empty state: sample questions ----------------
if not st.session_state.messages:
    st.markdown("<div class='welcome'>Thử một câu hỏi mẫu, hoặc gõ câu của bạn bên dưới 👇</div>", unsafe_allow_html=True)
    cols = st.columns(2)
    for index, (emoji, question) in enumerate(SAMPLE_QUESTIONS):
        if cols[index % 2].button(f"{emoji}  {question}", key=f"sample_{index}", use_container_width=True):
            st.session_state.pending = question
            st.rerun()

# ---------------- Chat ----------------
typed = st.chat_input("Hỏi agent, ví dụ: Tin AI hôm nay có gì nổi bật?")
user_text = typed or st.session_state.pop("pending", None)

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_text)

    transcript = st.session_state.transcript
    turn_record: dict[str, Any] = {
        "turn_index": len(transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, int(history_window)),
        {"role": "user", "content": user_text},
    ]

    msg: dict[str, Any] = {"role": "assistant", "content": "", "tool_events": []}
    started = time.perf_counter()
    with st.chat_message("assistant", avatar=AGENT_AVATAR):
        with st.spinner("Agent đang suy nghĩ và gọi tool..."):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=openai_tools,
                    model=model,
                    max_tool_rounds=int(max_tool_rounds),
                )
                turn_record.update(result)
                msg.update({
                    "content": result["assistant_text"],
                    "status": result["status"],
                    "tool_events": result["tool_events"],
                })
                st.session_state.history += [
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": result["assistant_text"]},
                ]
                rounds = len(result.get("rounds", []))
            except Exception as exc:
                turn_record.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})
                msg.update({"status": "provider_error", "error": turn_record["error"]})
                rounds = 0
        elapsed = time.perf_counter() - started
        n_tools = len(msg["tool_events"])
        status_label = {
            "answered": "đã trả lời",
            "waiting_for_user": "chờ bạn trả lời",
            "max_tool_rounds": "dừng do quá số vòng tool",
            "provider_error": "lỗi provider",
        }.get(msg.get("status", ""), msg.get("status", ""))
        msg["meta"] = f"🔧 {n_tools} tool · {rounds} vòng · {elapsed:.1f}s · {status_label}"
        render_assistant(msg)

    st.session_state.messages.append(msg)
    turn_record["ended_at"] = now_iso()
    transcript["turns"].append(turn_record)
    write_transcript(st.session_state.transcript_path, transcript)
