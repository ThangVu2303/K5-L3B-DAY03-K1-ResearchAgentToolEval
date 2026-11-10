# Phân công công việc — Day 03 Research Agent Tool Eval (nhóm 4 người)

> Mọi lệnh chạy trong thư mục `starter_v0/`. Chi tiết lệnh và code mẫu: xem [KE_HOACH_THUC_HIEN.md](KE_HOACH_THUC_HIEN.md).
> Deadline: **23:59 ngày lab (GMT+7)**. Run dùng làm bằng chứng phải có `provider_error_cases == 0` và `measured_cases == total_cases`.

## Thành viên

| Vai trò | Họ tên | MSSV | Phụ trách rubric |
|---|---|---|---|
| TV1 — Nhóm trưởng / Prompt | Vũ Đình Thắng | 2A202603753 | C1, C3 |
| TV2 — Tool declaration + Tool mới | Nguyễn Nhật Minh | 2A202603745 | C2, C4 |
| TV3 — Test + Eval | Vũ Bá Tùng Lâm | 2A202603775 | C4, C5 |
| TV4 — UI, Demo, Báo cáo | Nguyễn Hữu Thịnh | 2A202603726 | C6, C7 |

## Trạng thái hiện tại

- [x] `starter_v0/app.py` (Streamlit) đã có bản đầu (TV4)
- [x] `streamlit` đã thêm vào `requirements.txt`
- [x] `starter_v0/tools/hn_search/` đã phát triển và đăng ký thành công (TV2)
- [x] `starter_v0/artifacts/tools.yaml` đã viết lại đầy đủ descriptions và conventions (TV2)
- [x] `starter_v0/artifacts/system_prompt.md` đã cải tiến từ v0 -> v3 đạt 100% accuracy (TV1)
- [x] Các run v0, v1, v2, v3 đã hoàn thành với 0 lỗi provider và ghi đầy đủ vào `version_log.csv` (TV1)
- [x] Bảng B1, B2, B6 trong `group_report.md` đã hoàn thiện (TV1)
- [ ] `data/eval_group.json` (10 eval cases nhóm) và unit tests (TV3)
- [ ] Chat live transcript và hoàn thiện Phần A, B4 (TV4)

---

## TV1 — Nhóm trưởng / Prompt Engineer (C1: 10đ, C3: 20đ)

| # | Việc | File | Mốc |
|---|---|---|---|
| 1 | Tạo repo nhóm `K5-L3B-DAY03-<TenNhom>-ResearchAgentToolEval`, mời thành viên | — | Đầu giờ |
| 2 | Điền `TEAM.md` (tên nhóm, lớp, URL repo, bảng thành viên) | `TEAM.md` | Đầu giờ |
| 3 | Sửa lỗi provider, chạy preflight cho đạt | `.env` (không commit) | Trước 15:00 |
| 4 | Chạy lại **v0 hợp lệ** (không sửa prompt/tools trước) | `runs/` | Trước 15:00 |
| 5 | Ghi dòng v0 vào `version_log.csv` | `artifacts/version_log.csv` | Trước 15:00 |
| 6 | Phân tích từng case FAIL, gán loại lỗi → bảng B2 | `group_report.md` | Trước 15:00 |
| 7 | **v1**: sửa `system_prompt.md` (bỏ chỉ dẫn xấu, thêm rule hỏi lại, xác nhận trước khi gửi, từ chối ngoài phạm vi, gọi nhiều tool khi cần) | `artifacts/system_prompt.md` | 15:30 |
| 8 | **v2**: dùng `tools.yaml` mới của TV2, chạy lại | `runs/`, `version_log.csv` | 16:00 |
| 9 | **v3**: sửa rule hội thoại nhiều lượt (lượt mới ghi đè lượt cũ, `query` ngắn) | `system_prompt.md` | 17:30 |
| 10 | Viết B1 (bảng v0–v3), B2, B6 (reflection) | `group_report.md` | Sau showdown |
| 11 | Chốt commit, ghi commit chốt vào `TEAM.md`, rà checklist nộp bài | `TEAM.md` | Cuối |

Lưu ý: mỗi version chỉ đổi **một** giả thuyết; sau mỗi version chạy `pytest tests/test_tool_contract.py` phải xanh.

---

## TV2 — Tool Declaration + Tool mới (C2: 15đ, C4: 15đ)

| # | Việc | File | Mốc |
|---|---|---|---|
| 1 | Viết lại `description` cho 10 tool có sẵn: làm gì / khi nào dùng / khi nào KHÔNG dùng | `artifacts/tools.yaml` | 15:00–15:45 |
| 2 | Mô tả quy ước args: handle không có `@`, `topic=news`, `timeframe`, `search_type=Top\|Latest` | `artifacts/tools.yaml` | 15:45 |
| 3 | `send`: ghi rõ chỉ gửi khi `confirmed=true` sau khi user xác nhận | `artifacts/tools.yaml` | 15:45 |
| 4 | Viết **tool mới #1** (gợi ý `hn_search` / `wiki_summary`, không cần API key): `tool.py` trả error dict, không raise | `tools/<tên>/tool.py` | Trước 15:30 |
| 5 | Viết `TOOL.md` đúng frontmatter (xem `tools/README.md`) | `tools/<tên>/TOOL.md` | Trước 15:30 |
| 6 | Đăng ký tool trong `TOOL_FUNCTIONS` và khai báo trong yaml | `tools/__init__.py`, `tools.yaml` | Trước 15:30 |
| 7 | Gửi TV1 câu routing cho tool mới để thêm vào prompt | — | 15:30 |
| 8 | Viết A2 (bảng tool) và B5a (phần tool mới) | `group_report.md` | Trước 16:30 |
| 9 | *(Bonus +3)* Tool mới #2–#4 (`github_repo`, `current_date`…), mỗi tool đủ TOOL.md + đăng ký + 3 test + eval case | `tools/...` | Sau phần bắt buộc |

Lưu ý: tên tham số trong yaml phải có trong chữ ký hàm. Không đổi tên tool có sẵn.

---

## TV3 — Test + Eval (C4, C5: 10đ)

| # | Việc | File | Mốc |
|---|---|---|---|
| 1 | Chạy `pytest` lúc setup, báo trạng thái cho nhóm | — | Đầu giờ |
| 2 | Viết **≥ 3 test** cho mỗi tool mới: happy path, input xấu, nhánh lỗi (HTTP 429/500) — mock bằng `fake_http` | `tests/test_tools_todo.py` | 15:30 |
| 3 | Viết **10 eval case**: 5 single turn (`query`) + 5 multi turn (`turns`), ≥ 1 case route tới tool mới, mỗi case có `failure_type`, `expect`, `metadata.what_it_tests` | `data/eval_group.json` | 16:00 |
| 4 | Chạy `--suite group` (với v2, chạy lại khi có v3) | `runs/` | 16:00 / 17:30 |
| 5 | Viết B3 (10 case + PASS/FAIL), B5a (phần test) | `group_report.md` | Sau showdown |
| 6 | *(Bonus +1)* Điền hết stub còn lại → `pytest` 0 skipped | `tests/test_tools_todo.py` | Sau 17:30 |
| 7 | *(Bonus +1)* Regression test cho bug có sẵn rồi sửa code: `send(confirmed="false")` vẫn gửi; `limit=0` thành 5; `screenname="@sama"` không bỏ `@` | `tests/`, `tools/...` | Sau 17:30 |

Lưu ý: không chép case có sẵn trong `eval_base.json`. Trong `expect.args` chỉ ghi những arg chắc chắn đúng.

---

## TV4 — UI, Demo, Báo cáo (C6: 10đ, C7: 10đ)

| # | Việc | File | Mốc |
|---|---|---|---|
| 1 | Hoàn thiện `app.py`: hiện tool đã gọi + args + lỗi tool (không được che lỗi) | `starter_v0/app.py` | 15:00–16:00 |
| 2 | Chạy `streamlit run app.py`, mở `cloudflared tunnel --url http://localhost:8501`, thử link từ máy khác | — | 16:15 |
| 3 | Viết **Phần A**: A1 (agent làm gì, lệnh chạy UI, link), A2 (lấy từ TV2), A3 (3–5 câu hỏi mẫu) | `group_report.md` | **Trước 16:30** |
| 4 | *(Tùy chọn)* Poster 1 trang | `report/team/poster.html` | Trước 16:30 |
| 5 | Giữ tunnel chạy suốt showdown | — | 16:30 |
| 6 | Chat live `chat.py --version v3` ≥ 3 lượt: tin thường / thiếu thông tin rồi bổ sung / yêu cầu gửi Telegram | `transcripts/` | Sau khi có v2/v3 |
| 7 | Viết B4 (bảng transcript), mục khó khăn; tổng hợp Phần B | `group_report.md` | Sau showdown |
| 8 | *(Bonus +2)* Telegram thật: agent hỏi → user đồng ý → `send(confirmed=true)` → `status: sent` | `transcripts/` | Sau phần bắt buộc |
| 9 | *(Bonus +4, nếu máy ≥ 16GB RAM)* Ollama 2 model, v4-local/v5-local, mục B7 | `runs/`, `group_report.md` | Sau phần bắt buộc |

Lưu ý: kiểm tra transcript không chứa key/token trước khi commit.

---

## Việc chung của cả 4 người (C8: 10đ)

- [ ] Có ít nhất **1 commit kỹ thuật** của chính mình (code, test, eval, prompt — không chỉ sửa báo cáo)
- [ ] Viết báo cáo cá nhân `report/team/<MSSV>_<HoTen>.md` (copy từ `MSSV_HoTen.md`)
- [ ] Điền mục của mình trong `TEAM.md` (phần việc, đóng góp, bằng chứng)
- [ ] Tự giải thích được phần mình làm (người chấm có thể hỏi bất kỳ ai)
- [ ] Tự nộp link repo trên LMS bằng tài khoản cá nhân trước deadline

## Quy tắc phối hợp

- Chỉ **TV1** sửa `system_prompt.md` và chạy eval base, để version không bị lẫn.
- Mỗi người làm trên branch riêng (`feat/tool-moi`, `feat/ui`, `eval/group-cases`…), tạo PR vào `main`.
- File dễ conflict — báo nhóm và `git pull` trước khi sửa: `tools/__init__.py`, `artifacts/tools.yaml`, `tests/test_tools_todo.py`, `requirements.txt`, `group_report.md`.
- Không commit `.env`, `.venv`, API key, token Telegram, `arxiv_papers/`.

## Thứ tự phụ thuộc

```
TV1 v0 hợp lệ ──► TV1 v1 (prompt) ──► TV1 v2 ──► TV1 v3
TV2 tools.yaml ─────────────────────────┘
TV2 tool mới ──► TV3 unit test ──► TV3 eval case cho tool mới ──► run group (v3)
TV4 UI (làm độc lập) ──► link showdown 16:30
TV4 chat live (cần v2/v3) ──► B4
```

## Mốc thời gian

| Mốc | Phải có |
|---|---|
| 15:00 | v0 hợp lệ + bảng B2 (TV1) |
| 15:30 | v1 (TV1); tool mới + 3 test (TV2, TV3) |
| 16:00 | `tools.yaml` mới + v2 (TV2, TV1); 10 eval case + run group (TV3) |
| 16:30 | Link UI + Phần A báo cáo (TV4) |
| 17:30 | v3 (TV1); Phần B (cả nhóm) |
| 23:59 | Push + mỗi người nộp link trên LMS |
