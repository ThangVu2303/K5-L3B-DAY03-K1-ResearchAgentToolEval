# Báo cáo cá nhân — Nguyễn Hữu Thịnh — 2A202603726

## 1. Thông tin thành viên

- Họ tên: Nguyễn Hữu Thịnh
- MSSV: 2A202603726
- Email: 26ai.thinhnh2@vinuni.edu.vn
- GitHub: huuthinh812
- Vai trò: **TV3** — Test + Eval (C5, bonus test), UI, Demo, Báo cáo (C6, C7)

## 2. Phần việc phụ trách

**Test + Eval**

- Viết 10 eval case nhóm trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn, có case route tới tool mới).
- Chạy `--suite group` với prompt v3, kiểm tra run hợp lệ và điền bảng B3.
- Viết test thật cho các tool có sẵn trong `starter_v0/tests/test_tools_todo.py` (bonus test challenge: 0 skipped).

**UI, Demo, Báo cáo**

- Xây dựng UI Streamlit cho agent (`starter_v0/app.py`) và thêm dependency vào `requirements.txt`.
- Mở link dùng thử bằng Cloudflare Tunnel cho buổi Team showdown.
- Chat live với agent bản v3, thu transcript và viết bảng B4.
- Viết Phần A (A1, A3), dòng UI trong B5a, mục 5, mục 8 và tổng hợp báo cáo nhóm.

## 3. Đóng góp cụ thể

### Test + Eval

**Eval nhóm (`starter_v0/data/eval_group.json`)**

- Viết 10 case: 5 single turn + 5 multi turn. 4 case route tới tool mới `hn_search`: route theo tên Hacker News (G01), viết tắt "HN" + "mới nhất" → `sort_by="date"` (G02), thiếu chủ đề rồi bổ sung qua 3 lượt (G06), đổi nguồn web → HN bằng đại từ "nó" (G07).
- Các case còn lại phủ những chỗ bộ base chưa có: bỏ `@` khỏi handle (G03), `timeframe="month"` (G04), dịch thuật ngoài phạm vi → không gọi tool (G05), ghi đè chủ đề nhưng giữ `search_type="Top"` (G08), thêm `max_results` ở lượt sau (G09), và chiều "đã xác nhận thì phải gửi" của boundary `send` (G10).
- Không chép case nào từ `eval_base.json`; `expect.args` chỉ ghi các tham số chắc chắn đúng.
- Chạy `--suite group` với v3: run hợp lệ 10/10, tất cả PASS. Bảng B3 ghi tool call thực tế của từng case và chỉ ra 3 case tool lỗi do môi trường (RapidAPI 403, thiếu token Telegram) — eval vẫn PASS vì chỉ chấm lựa chọn tool và args, đây là giới hạn của chấm tự động.

**Unit test (bonus test challenge)**

- Thay 14 stub `pytest.skip(TODO)` trong `tests/test_tools_todo.py` bằng test thật cho `clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search`, `policy`.
- Test chạy offline (mock HTTP bằng `fake_http`, key giả qua `monkeypatch`), assert cả request gửi đi lẫn kết quả trả về. Có test guardrail: `send` không gọi mạng khi thiếu token; `policy` đưa dòng injection probe vào `untrusted_text` chứ không vào `facts`.
- Kết quả: toàn suite 107 passed, 0 skipped, 0 failed.

### UI, Demo, Báo cáo

**UI Streamlit (`starter_v0/app.py`)**

- Dùng lại vòng lặp gọi tool `run_model_tool_loop` của `chat.py`, nên UI chạy đúng logic agent như khi chấm, và ghi transcript cùng định dạng với `chat.py`.
- Đọc trực tiếp `artifacts/system_prompt.md` và `artifacts/tools.yaml`: khi TV1/TV2 cập nhật prompt hoặc thêm tool (`hn_search`), UI tự dùng bản mới, không phải sửa code.
- Mỗi câu trả lời hiện đủ tool đã gọi, args, trạng thái (✅ ok / ⚠️ lỗi / ❓ hỏi lại / ✋ cần xác nhận) và JSON kết quả. Lỗi tool và lỗi provider luôn được hiển thị, không bị che.
- Có câu hỏi mẫu dạng nút bấm, danh sách tool lấy từ `tools.yaml`, và dòng thông tin số tool / số vòng / thời gian / trạng thái cho mỗi câu trả lời.
- Version label tự nhận theo `version_log.csv` (so hash prompt/tools), để transcript không bị gắn nhầm version.

**Script hỗ trợ phân tích (`starter_v0/scripts/show_failures.py`)**

- In nhanh run có hợp lệ hay không (`provider_error_cases`, `measured_cases`), các metric, hash và từng case FAIL (input, expect, actual, lý do). Dùng cho bảng B2 và để kiểm tra run group.

**Tích hợp và kiểm tra**

- Tạo nhánh `feat/huuthinh` từ nhánh của TV1 (`vudinhthang`, đã gộp tool của TV2) để ghép UI với prompt v3 và `hn_search`.
- Kiểm tra 4 run v0–v3 của TV1 và phát hiện run v3 có `provider_error_cases = 1` (case M05 bị 429), tức là chưa hợp lệ theo rubric. Đã báo TV1 để chạy lại.
- Phát hiện git trên Windows đổi ký tự xuống dòng (LF ↔ CRLF) làm hash prompt khác với hash trong `version_log.csv` dù nội dung giống hệt. Xử lý: UI so khớp hash theo cả hai kiểu xuống dòng; khi chat live và chạy eval nhóm dùng đúng bản prompt có hash `pd5ffefbef293`.

**Chat live, demo và báo cáo**

- Chạy `python chat.py --provider gemini --version v3` với đủ 3 kịch bản: yêu cầu thường, thiếu thông tin rồi bổ sung, yêu cầu đăng Telegram. Kết quả: agent hỏi lại khi thiếu tài khoản, xin xác nhận yes/no trước khi gửi, gọi `lookup(news, day)` và trả tin có nguồn.
- Mở link demo public bằng Cloudflare Tunnel, kiểm tra link trả về trang UI.
- Viết A1, A3, B3, B4, dòng UI và ghi chú unit test trong B5a, trạng thái bonus B5/B7, mục 5 (khó khăn), mục 8 (tài liệu tham khảo) của `group_report.md`.

## 4. Bằng chứng

- Commit trên nhánh `feat/huuthinh` (PR #2):
  - `3c4d555` — _feat(ui): add Streamlit UI for the research agent_: [`app.py`](../../starter_v0/app.py), [`show_failures.py`](../../starter_v0/scripts/show_failures.py), dòng `streamlit` trong [`requirements.txt`](../../starter_v0/requirements.txt).
  - `ae13168` — transcript chat live và các mục báo cáo (A1, A3, B4, B5a, mục 5, mục 8).
  - `72c91e3` — _feat(eval): add 10 group eval cases and implement all TODO tool tests_: [`eval_group.json`](../../starter_v0/data/eval_group.json), [`test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py).
  - `c0959ae` — run eval nhóm hợp lệ và bảng B3.
- Run eval nhóm: [`v3_B_group_gemini_20261111T101011513780.json`](../../starter_v0/runs/v3_B_group_gemini_20261111T101011513780.json) (10/10 PASS, `provider_error_cases = 0`).
- Transcript chat live v3: [`v3_gemini_20261111T024323043613.transcript.json`](../../starter_v0/transcripts/v3_gemini_20261111T024323043613.transcript.json) (`artifact_version = v3+pd5ffefbef293+t8a02817ed09c`).
- Báo cáo nhóm: [group_report.md](group_report.md) — A1, A3, B3, B4, B5a (dòng UI + ghi chú unit test), B5 (test challenge), mục 5, mục 8.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Claude Code để đọc repo, lập kế hoạch, viết `app.py`, `show_failures.py`, soạn eval case, viết test và nháp các mục báo cáo.
  - Tự kiểm tra bằng cách:
    - chạy `streamlit run app.py` trên máy và thử các câu hỏi mẫu; mở link tunnel để chắc trang UI hiện ra;
    - chạy test UI tự động (Streamlit AppTest) với provider giả để kiểm tra 3 tình huống: trả lời có tool, hỏi lại, lỗi provider;
    - chạy thật với Gemini `gemini-3.5-flash` + prompt v3;
    - chạy `pytest` sau khi ghép UI (93 passed, 0 failed) và sau khi viết thêm test (107 passed, 0 skipped, 0 failed);
    - chạy `pytest tests/test_tool_contract.py` để chắc eval case chỉ dùng tool đã khai báo, rồi kiểm tra run group bằng `scripts/show_failures.py` (hợp lệ, 10/10);
    - đọc lại tool call thực tế trong run group để viết B3, và đọc lại transcript để chắc không có API key trong file.

## 5. Khó khăn và cách xử lý

- **Hết quota Gemini (429):** free tier chỉ 20 request/ngày cho mỗi project và mỗi model. Tạo key mới trong cùng project không giúp được vì quota tính theo project. Cách xử lý: dùng key ở project khác, dùng model `gemini-3.5-flash` giống TV1, và để dành quota cho chat live, eval nhóm và showdown.
- **Run eval nhóm lần đầu không hợp lệ:** hết quota sau 3 case (7/10 `provider_error`). Một key mới tạo trong cùng project vẫn hết quota, một key khác bị 401 do copy sai. Cách xử lý: kiểm tra mỗi key bằng đúng 1 request trước khi chạy cả suite, rồi chạy lại bằng key ở project khác; run lỗi bị loại, không dùng làm bằng chứng.
- **Thiếu `RAPIDAPI_KEY` khi chat live:** ở lượt "Của Andrej Karpathy", model gọi đúng `timeline(screenname="karpathy", limit=5)` nhưng tool lỗi do máy chưa có key. Lỗi được hiện rõ trong UI/transcript; đã bổ sung key sau đó.
- **RapidAPI trả 403 Forbidden:** key RapidAPI có nhưng chưa subscribe gói Twitter API45, nên `timeline`/`social_search` lỗi khi chạy thật (thấy trong run group G03, G08).
- **Nhầm môi trường lệnh:** ban đầu gõ lệnh PowerShell trong Git Bash; đã chuyển sang `source .venv/Scripts/activate` và `cp`.

## 6. Tự đánh giá

> _(Nháp — tự sửa lại theo đánh giá của bản thân)_

- Làm tốt: hoàn thành cả mảng Test + Eval lẫn UI, Demo, Báo cáo với bằng chứng hợp lệ (run group 10/10, transcript v3, UI chạy thật); `pytest` đạt 0 skipped; phát hiện run v3 base chưa hợp lệ và lỗi hash do ký tự xuống dòng.
- Chưa tốt: chưa quản lý quota Gemini từ đầu nên mất nhiều request vào các lần chạy lỗi; lượt `timeline` trong transcript bị lỗi do chưa điền `RAPIDAPI_KEY` trước khi chat live; chưa subscribe RapidAPI nên tool Twitter vẫn lỗi 403.
- Nếu làm lại: chuẩn bị đủ key cho mọi tool và nhiều key Gemini ở các project khác nhau trước buổi lab; chạy preflight cho từng tool trước khi chat live và chạy eval.
