# Team

## Thông tin nhóm

- Tên nhóm: K1
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-K1-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: https://github.com/ThangVu2303/K5-L3B-DAY03-K1-ResearchAgentToolEval, nhánh vudinhthang, commit chốt: 4d07ea0

## Thành viên

| STT | Họ tên           | MSSV        | Email                       | GitHub      | Vai trò                                    |
| --: | ---------------- | ----------- | --------------------------- | ----------- | ------------------------------------------ |
|   1 | Vũ Đình Thắng    | 2A202603753 | 26ai.thangvd2@vinuni.edu.vn | ThangVu2303 | TV1 — Nhóm trưởng / Prompt (C1, C3)        |
|   2 | Nguyễn Nhật Minh | 2A202603745 | 26ai.minhnn7@vinuni.edu.vn  | NhMinh-2610 | TV2 — Tool declaration + Tool mới (C2, C4) |
|   3 | Vũ Bá Tùng Lâm   | 2A202603775 | 26ai.lamvbt@vinuni.edu.vn   | lamvu-dev   | Phân công ban đầu: TV3 — Test + Eval; phần việc TV3 đã chuyển cho Thịnh (xem mục dưới) |
|   4 | Nguyễn Hữu Thịnh | 2A202603726 | 26ai.thinhnh2@vinuni.edu.vn | huuthinh812 | TV3 + TV4 — Eval nhóm, Test, UI, Demo, Báo cáo (C5, C6, C7) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/team/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/2A202603753_VuDinhThang.md`.

---

## Vũ Đình Thắng - 2A202603753 (TV1 — Nhóm trưởng / Prompt)

### Phần việc phụ trách

- Quản lý tiến độ nhóm, phân chia công việc và điều phối dự án.
- Thiết lập môi trường dự án, cấu hình API keys và provider (`gemini_provider.py`).
- Thực hiện chuỗi đánh giá cải tiến từ baseline `v0` đến `v3` theo đúng Rubric C1 và C3.
- Phân tích lỗi các case FAIL (Bảng B2), cập nhật `version_log.csv` và hoàn thiện B1, B6 (Reflection) trong `group_report.md`.

### Đóng góp cụ thể

- Setup môi trường ban đầu, preflight test và cấu hình retry logic cho provider.
- Chạy đánh giá v0 và phân tích 9 failure cases do prompt ban đầu gây ra.
- Viết lại và tối ưu `system_prompt.md` qua các vòng v1, v2, v3 (loại bỏ hướng dẫn xấu, bổ sung rule `clarify`, an toàn trước khi gửi, routing `hn_search` và ngữ cảnh multi-turn).
- Đưa độ chính xác tăng từ 55.0% (v0) lên 80.0% (v1), 85.0% (v2) và 100.0% (v3).

### Bằng chứng

- Các file run trong `starter_v0/runs/`: `v0`, `v1`, `v2`, `v3`.
- File ghi nhận lịch sử phiên bản `starter_v0/artifacts/version_log.csv`.
- Bảng B1, B2, Mục 5 và Mục 7 (B6) trong `report/team/group_report.md`.
- Các commit trên nhánh `vudinhthang`.

---

## Nguyễn Nhật Minh - 2A202603745 (TV2 — Tool declaration + Tool mới)

### Phần việc phụ trách

- Viết lại `description` cho 10 tool có sẵn: nêu rõ công dụng, khi nào NÊN dùng, khi nào KHÔNG ĐƯỢC dùng (C2).
- Chuẩn hóa quy ước tham số (arguments): handle không có `@`, định dạng `timeframe`, `search_type=Top|Latest`, boundary xác nhận cho `send` (`confirmed=True`).
- Phát triển công cụ mới `hn_search` (tìm kiếm Hacker News) kèm `TOOL.md` và đăng ký trong registry `tools/__init__.py` (C4).
- Soạn thảo tài liệu bàn giao `docs/TOOL-HANDOFF.md` và viết Phần A2, B5a trong báo cáo nhóm.

### Đóng góp cụ thể

- Hoàn thành viết lại khai báo công cụ trong `starter_v0/artifacts/tools.yaml`.
- Xây dựng module `starter_v0/tools/hn_search/` (xử lý lỗi an toàn qua error dict, không raise exception).
- Viết đầy đủ tài liệu `TOOL.md` và bàn giao quy tắc routing cho TV1 cùng input/output cho TV3.

### Bằng chứng

- File khai báo `starter_v0/artifacts/tools.yaml`.
- Thư mục code và tài liệu tool mới `starter_v0/tools/hn_search/`.
- Tài liệu bàn giao `docs/TOOL-HANDOFF.md`.
- Báo cáo cá nhân `report/team/2A202603745_NguyenNhatMinh.md` và commit nhánh `NguyenNhatMinh`.

---

## Vũ Bá Tùng Lâm - 2A202603775 (phân công ban đầu: TV3 — Test + Eval)

### Phần việc phụ trách

- Theo phân công ban đầu: viết 10 eval case nhóm, chạy `--suite group`, điền bảng B3 (C5).
- Phần việc TV3 này đã được **Nguyễn Hữu Thịnh** thực hiện (commit `72c91e3`, `c0959ae` trên nhánh `feat/huuthinh`); unit test của tool mới `hn_search` do TV2 (Nguyễn Nhật Minh) viết.

### Đóng góp cụ thể

- *(Lâm tự điền phần việc thực tế đã làm, nếu có.)*

### Bằng chứng

- *(Lâm tự điền: commit, file. Tính đến 11/11 chưa có commit của tài khoản `lamvu-dev` trên repo.)*

---

## Nguyễn Hữu Thịnh - 2A202603726 (TV3 + TV4 — Eval nhóm, Test, UI, Demo, Báo cáo)

### Phần việc phụ trách

**TV3 — Test + Eval (C5, bonus test):**

- Viết 10 eval case nhóm trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn, có case route tới tool mới).
- Chạy `--suite group` với v3, kiểm tra run hợp lệ và điền bảng B3.
- Viết test cho các tool có sẵn trong `starter_v0/tests/test_tools_todo.py` (bonus test challenge: 0 skipped).

**TV4 — UI, Demo, Báo cáo (C6, C7):**

- Phát triển UI Streamlit `starter_v0/app.py`: hiện tool call, args, kết quả, không che lỗi.
- Mở link demo public qua Cloudflare Tunnel cho Team showdown.
- Chat live với agent v3, thu transcript và viết bảng B4.
- Viết Phần A (A1, A3), dòng UI trong B5a và tổng hợp báo cáo nhóm.

### Đóng góp cụ thể

**TV3:**

- 10 eval case nhóm: 4 case route tới `hn_search` (theo tên HN, `sort_by="date"`, thiếu chủ đề rồi bổ sung, đổi nguồn web → HN); các case còn lại phủ bỏ `@` khỏi handle, `timeframe="month"`, dịch thuật ngoài phạm vi, giữ `search_type="Top"`/`max_results` qua nhiều lượt, và `send(confirmed=true)` sau khi user đã xác nhận.
- Run `--suite group` v3 hợp lệ: 10/10 PASS, `provider_error_cases = 0`; B3 ghi rõ 3 case tool lỗi do môi trường (RapidAPI 403, thiếu token Telegram) mà eval không phát hiện.
- Thay 14 stub `pytest.skip(TODO)` bằng test thật, offline, cho `clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search`, `policy`; `pytest`: 107 passed, 0 skipped, 0 failed.

**TV4:**

- Viết UI Streamlit dùng lại vòng lặp tool của `chat.py`: hiện tool call, args, trạng thái và JSON kết quả; không che lỗi tool/provider; câu hỏi mẫu dạng nút bấm; tự nhận version qua hash trong `version_log.csv`; tự lưu transcript.
- Viết `scripts/show_failures.py` để in độ hợp lệ của run và các case FAIL (hỗ trợ bảng B2).
- Ghép UI với prompt v3 (TV1) và `hn_search` (TV2) trên nhánh `feat/huuthinh`, chạy thật với Gemini `gemini-3.5-flash`.
- Phát hiện run v3 base của nhóm có 1 `provider_error` (chưa hợp lệ) và lỗi lệch hash do ký tự xuống dòng trên Windows; đã báo nhóm.
- Chat live v3 đủ 3 kịch bản (yêu cầu thường, thiếu thông tin rồi bổ sung, yêu cầu gửi Telegram); viết B4, A1, A3, dòng UI B5a, mục 5 (khó khăn) và mục 8 (tài liệu tham khảo).
- Mở link demo public bằng Cloudflare Tunnel cho Team showdown: https://landing-circumstances-sie-introductory.trycloudflare.com (link chỉ sống khi máy demo chạy Streamlit + cloudflared).

### Bằng chứng

- TV3: commit `72c91e3` (`starter_v0/data/eval_group.json`, `starter_v0/tests/test_tools_todo.py`) và `c0959ae` (run `starter_v0/runs/v3_B_group_gemini_20261111T101011513780.json`, bảng B3).
- TV4: commit `3c4d555` (`starter_v0/app.py`, `starter_v0/scripts/show_failures.py`, `starter_v0/requirements.txt`) và `ae13168` (transcript, báo cáo).
- Transcript `starter_v0/transcripts/v3_gemini_20261111T024323043613.transcript.json`.
- Mục A1, A3, B3, B4, B5a (dòng UI + ghi chú unit test), B5 (test challenge) trong `report/team/group_report.md`.
- Báo cáo cá nhân `report/team/2A202603726_NguyenHuuThinh.md`.
