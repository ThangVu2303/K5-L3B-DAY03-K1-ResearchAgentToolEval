# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: K1
- Lớp: L3B
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
  + TV1: Vũ Đình Thắng (Nhóm trưởng / Prompt Engineer — C1, C3)
  + TV2: Nguyễn Nhật Minh (Tool Declaration & Custom Tool — C2, C4)
  + TV3: Vũ Bá Tùng Lâm (Test & Eval — C4, C5)
  + TV4: Nguyễn Hữu Thịnh (UI, Demo & Báo cáo — C6, C7)
- Provider/model dùng cho v0–v3: Google Gemini (`gemini-3.5-flash`)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại khi thiếu thông tin hoặc cần xác nhận trước khi gửi | không |
| timeline | Lấy các bài đăng gần đây của một tài khoản Twitter/X đã xác định | không |
| social_search | Tìm bài đăng Twitter/X theo chủ đề, Latest hoặc Top | không |
| lookup | Tìm thông tin/tin tức trên web theo từ khóa và khoảng thời gian | không |
| fetch | Đọc nội dung một URL đã biết | không |
| format | Trình bày item đã có thành markdown digest/danh sách/thread | không |
| send | Gửi văn bản lên Telegram sau khi người dùng xác nhận đúng nội dung | không |
| policy | Tra cứu quy định trong knowledge base policy nội bộ | không |
| papers | Tìm metadata paper/preprint trên arXiv | không |
| paper_text | Tải PDF arXiv đã xác định và trích text | không |
| hn_search | Tìm bài trên Hacker News theo chủ đề, độ liên quan hoặc thời gian | có |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

- **Tối ưu hóa `system_prompt.md` (TV1):**
  + **v0 ➔ v1:** Loại bỏ toàn bộ chỉ dẫn độc hại của starter (đoán mò khi thiếu info, tự tiện gửi tin nhắn không hỏi, ép buộc hoàn thành trong 1 bước). Bổ sung quy tắc: gọi `clarify` khi thiếu handle hoặc URL bài viết; bắt buộc xin xác nhận của người dùng trước khi gọi `send`; thiết lập ranh giới từ chối các yêu cầu ngoài phạm vi research (code, thời tiết); và cho phép gọi đồng thời nhiều tool (`multi-tool call`).
  + **v2 ➔ v3:** Tinh chỉnh việc trích xuất argument cho `lookup` (chỉ lấy keyword cốt lõi, không mở rộng từ đồng nghĩa gây sai lệch query); trích xuất handle Twitter (bỏ tiền tố `@`); bắt buộc dùng `response_type="yes_no"` khi xin xác nhận gửi Telegram; bổ sung quy tắc routing cho tool mới `hn_search`; và thiết lập cơ chế duy trì/ghi đè ngữ cảnh trong hội thoại nhiều lượt (`multi-turn`).
- **Khai báo chuẩn hóa `tools.yaml` (TV2):**
  + Viết lại mô tả cho 10 tool có sẵn, phân định rõ ranh giới "khi nào nên dùng" và "khi nào KHÔNG ĐƯỢC dùng".
  + Chuẩn hóa quy ước tham số: handle không chứa ký tự `@`, định dạng `timeframe`, `search_type=Top|Latest`, tham số `confirmed=True` cho `send`.
- **Phát triển tool mới `hn_search` (TV2 & TV3):**
  + Tìm kiếm bài thảo luận trên Hacker News qua Algolia API (`query`, `max_results`, `sort_by=relevance|date`). Trả về error dict an toàn, không raise exception ra ngoài agent.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu của starter prompt | - | 0.55 | starter_v0/runs/v0_B_base_gemini_20261110T195405860459.json |
| v1 | system_prompt.md | Bỏ chỉ dẫn xấu (đoán mò, tự gửi) và thêm rule clarify + xác nhận gửi + từ chối out-of-scope | 0.55 | 0.80 | starter_v0/runs/v1_B_base_gemini_20261110T215625710195.json |
| v2 | tools.yaml | Khai báo lại tools.yaml theo TV2: chi tiết when to use/not use và convention args | 0.80 | 0.85 | starter_v0/runs/v2_B_base_gemini_20261110T221714362720.json |
| v3 | system_prompt.md | Tối ưu prompt đa lượt: chuẩn hóa query, trích xuất handle timeline, routing hn_search, clarify yes_no cho send | 0.85 | 1.00 | starter_v0/runs/v3_B_base_gemini_20261110T225014036508.json |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_tool | `['lookup']` | query: expected 'AI', got 'tin tức AI mới nhất artificial intelligence news' | Bỏ chỉ dẫn đoán mò, thêm quy tắc phân biệt web_search với web_news/read_url trong prompt |
| R08_out_of_scope | out_of_scope | `['lookup']` | expected no tool call | Thêm boundary rule: từ chối các câu hỏi ngoài phạm vi research (như dự báo thời tiết) |
| R09_no_tool_capability | unnecessary_tool | `['format']` | expected no tool call | Thêm rule: nếu không có tool hỗ trợ trực tiếp thì trả lời trực tiếp hoặc từ chối, không gọi bừa |
| R10_missing_handle | missing_info | `['timeline']` | missing tool call clarify; extra tool call timeline | Bỏ chỉ dẫn bịa tên tài khoản nổi tiếng, thêm rule gọi clarify khi thiếu handle |
| R11_missing_url | missing_info | `['fetch']` | missing tool call clarify; extra tool call fetch | Bỏ chỉ dẫn đoán URL, thêm rule gọi clarify khi thiếu link bài viết |
| R12_confirm_before_send | wrong_boundary | `['send']` | missing tool call clarify; extra tool call send | Bỏ rule tự động gửi, bắt buộc yêu cầu user xác nhận (confirmed=True) trước khi gọi send_telegram |
| R13_parallel_web_and_tweets | wrong_tool | `['lookup']` | query: expected 'AI', got 'tin tức AI artificial intelligence'; missing tool call social_search | Cho phép agent gọi đồng thời nhiều tool (multi-tool call) trong 1 lượt thay vì chỉ 1 tool duy nhất |
| R14_out_of_scope_coding | out_of_scope | `['send']` | expected no tool call | Thêm boundary rule từ chối viết code / việc ngoài phạm vi research |
| M02_carryover_timeframe | wrong_arg_value | `['lookup']` | query: expected 'robotics', got 'robotics news' | Cải thiện system prompt cho multi-turn: duy trì timeframe từ lượt trước sang lượt sau |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới `hn_search` | [Code](../../starter_v0/tools/hn_search/tool.py), [TOOL.md](../../starter_v0/tools/hn_search/TOOL.md), [bàn giao và kiểm chứng](../../docs/TOOL-HANDOFF.md) | Registry/YAML/signature contract pass; smoke API thật trả 1 item; output dùng được với format trong test offline | Input sai và HTTP/timeout trả error dict; không đọc toàn văn; nội dung ngoài là dữ liệu, không phải chỉ dẫn |
| Unit test tool mới `hn_search` | [Test](../../starter_v0/tests/test_tools_todo.py), [kết quả và lệnh chạy](../../docs/TOOL-HANDOFF.md) | 26 trường hợp cho tool mới; toàn suite 93 passed, 14 skipped, 0 failed; có regression test URL sai định dạng | Mock HTTP, không gọi mạng thật; TV3 tiếp nhận review/bổ sung |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

- **Lỗi Provider và Hạn ngạch API (429 RESOURCE_EXHAUSTED):** Ban đầu gặp lỗi cạn quota do chính sách Free Tier của Google AI Studio giới hạn 20 requests/ngày cho mỗi project. Nhóm đã xử lý bằng cách: tối ưu `gemini_provider.py` (thêm delay an toàn 3s giữa các request, bổ sung cơ chế retry với exponential backoff khi gặp lỗi 429/503), chuyển đổi model sang `gemini-3.5-flash`, và phân bổ key hợp lý cho từng phiên bản để đảm bảo mọi run làm bằng chứng đều có `provider_error_cases == 0` và `measured_cases == 20`.
- **Ranh giới an toàn (Confirmation Boundary):** Starter prompt ban đầu có chỉ dẫn nguy hiểm ("tự gửi đi để user không phải đợi"). Nhóm đã loại bỏ chỉ dẫn này, áp dụng quy tắc bắt buộc xin xác nhận qua `clarify(response_type="yes_no")` trước khi kích hoạt `send`.
- **Over-clarification:** Ở v1 model có xu hướng hỏi lại quá nhiều cả khi user đã cung cấp handle `@sama`. Nhóm đã tinh chỉnh prompt ở v2/v3 để model phân biệt rõ khi nào đủ thông tin thì gọi `timeline`, chỉ thiếu hẳn mới gọi `clarify`.

## 6. Tổng hợp đóng góp

- **Vũ Đình Thắng (TV1 — C1, C3):** Thiết lập môi trường và sửa lỗi provider (`gemini_provider.py`); chạy baseline v0 hợp lệ và phân tích 9 failure cases (Bảng B2); thực hiện chuỗi cải tiến lặp v0 ➔ v1 ➔ v2 ➔ v3 trên `system_prompt.md`, đưa độ chính xác từ 55.0% lên 100.0%; ghi nhận lịch sử phiên bản `version_log.csv`; hoàn thiện B1, B2, Mục 1, 3, 5, 7 trong báo cáo nhóm.
- **Nguyễn Nhật Minh (TV2 — C2, C4):** Viết lại khai báo cho 10 công cụ trong `artifacts/tools.yaml`; phát triển công cụ mới `hn_search` kèm `TOOL.md` và đăng ký registry; viết tài liệu bàn giao `TOOL-HANDOFF.md`, Mục A2 và B5a.
- **Vũ Bá Tùng Lâm (TV3 — C4, C5):** Viết bộ unit tests cho tool mới trong `tests/test_tools_todo.py`; xây dựng bộ đánh giá của nhóm gồm 10 cases trong `data/eval_group.json`; chạy eval suite group và hoàn thiện bảng B3, B5a.
- **Nguyễn Hữu Thịnh (TV4 — C6, C7):** Phát triển ứng dụng Streamlit `app.py`; triển khai tunnel demo public; thực hiện các phiên chat live đa lượt, thu thập transcript vào `transcripts/` và viết bảng B4; hoàn thiện Mục A1, A3 và tổng hợp báo cáo.

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix thuộc `system_prompt.md`:** 
  + Loại bỏ toàn bộ các chỉ dẫn xấu (đoán mò, tự gửi tin, hoàn thành trong 1 bước).
  + Thêm quy tắc gọi `clarify` khi thiếu thông tin thiết yếu (handle, URL).
  + Ràng buộc xin xác nhận với `response_type="yes_no"` trước khi gọi `send`.
  + Thiết lập boundary từ chối các yêu cầu ngoài phạm vi (lập trình, thời tiết).
  + Cho phép gọi nhiều tool song song trong cùng 1 lượt (`multi-tool calls`).
  + Bổ sung quy tắc routing cho tool mới `hn_search` và cơ chế ghi đè tham số trong hội thoại nhiều lượt.
- **Fix thuộc `tools.yaml`:** 
  + Viết lại description chi tiết cho 10 tool có sẵn: làm gì, khi nào NÊN dùng, khi nào KHÔNG ĐƯỢC dùng.
  + Chuẩn hóa quy ước arguments: handle không có `@`, định dạng `timeframe`, `search_type=Top|Latest`.
  + Ghi rõ điều kiện kích hoạt `send` chỉ khi `confirmed=True`.
  + Khai báo tool mới `hn_search` đúng định dạng OpenAPI schema.
- **Failure nào cần review thủ công thay vì chấm tự động:** 
  + Các câu hỏi clarify có cách diễn đạt tự nhiên bằng tiếng Việt khác với chuỗi mong đợi cố định trong test suite.
  + Các query tìm kiếm ngữ nghĩa tương đương nhưng model trích xuất ngắn gọn hoặc dịch từ khóa tương đương.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào:** 
  + Bổ sung Dynamic Few-shot Examples vào system prompt để tối ưu hóa việc trích xuất argument cho các câu hỏi phức tạp.
  + Tích hợp cơ chế Structured Outputs / JSON Schema validation để triệt tiêu hoàn toàn sai lệch kiểu dữ liệu arguments.

## 8. Tài liệu tham khảo

-
