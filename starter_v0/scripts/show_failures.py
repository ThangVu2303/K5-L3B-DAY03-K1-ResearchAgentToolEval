"""In tóm tắt một run JSON: metric, hash, và từng case FAIL (dùng để điền bảng B2).

Cách dùng (từ starter_v0/):
    python scripts/show_failures.py                 # run mới nhất trong runs/
    python scripts/show_failures.py runs/<file>.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        runs = sorted((ROOT / "runs").glob("*.json"), key=lambda p: p.stat().st_mtime)
        if not runs:
            raise SystemExit("Chưa có run nào trong runs/")
        path = runs[-1]

    run = json.loads(path.read_text(encoding="utf-8"))
    s = run["summary"]
    valid = s["provider_error_cases"] == 0 and s["measured_cases"] == s["total_cases"]

    try:
        shown = path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        shown = str(path)
    print(f"Run file        : {shown}")
    print(f"artifact_version: {run['artifact_version']}")
    print(f"prompt_hash     : {run['prompt_hash'][:12]}   tools_hash: {run['tools_hash'][:12]}")
    print(f"Hợp lệ          : {'CÓ' if valid else 'KHÔNG - chạy lại'} "
          f"(provider_error_cases={s['provider_error_cases']}, measured={s['measured_cases']}/{s['total_cases']})")
    for key in ("case_accuracy", "tool_routing_accuracy", "argument_accuracy", "multiturn_accuracy"):
        print(f"{key:<22}: {s.get(key)}")
    print(f"failure_counts        : {s.get('failure_counts')}")
    print()

    failed = [item for item in run["results"] if not item["result"]["passed"]]
    print(f"=== {len(failed)} case FAIL ===")
    for item in failed:
        r = item["result"]
        user_input = item["input"]
        if isinstance(user_input, list):
            user_input = " -> ".join(turn["content"] for turn in user_input)
        actual = ", ".join(
            f"{c['name']}({json.dumps(c['args'], ensure_ascii=False)})" for c in r.get("actual_tool_calls", [])
        ) or "(không gọi tool)"
        print(f"\n[{item['id']}]  failure_type={r.get('failure_type')}  mismatch={r.get('observed_mismatch')}")
        print(f"  Input   : {user_input}")
        print(f"  Expect  : {json.dumps(item['expect'], ensure_ascii=False)}")
        print(f"  Actual  : {actual}")
        if r.get("actual_text"):
            print(f"  Text    : {r['actual_text'][:200]}")
        print(f"  Failures: {r.get('failures')}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
