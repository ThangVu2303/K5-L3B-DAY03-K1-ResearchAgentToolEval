# Báo cáo cá nhân — Nguyễn Hữu Thịnh — 2A202603726

## 1. Thông tin thành viên

- Họ tên: Nguyễn Hữu Thịnh
- MSSV: 2A202603726
- Email: 26ai.thinhnh2@vinuni.edu.vn
- GitHub: huuthinh702812
- Vai trò: TV4 — UI, Demo, Báo cáo (C6, C7)

## 2. Phần việc phụ trách

- Xây dựng UI Streamlit cho agent (`starter_v0/app.py`) và thêm dependency vào `requirements.txt`.
- Mở link dùng thử bằng Cloudflare Tunnel cho buổi Team showdown.
- Chat live với agent bản v3, thu transcript và viết bảng B4.
- Viết Phần A (A1, A3), dòng UI trong B5a, và tổng hợp báo cáo nhóm.

## 3. Đóng góp cụ thể

**UI Streamlit (`starter_v0/app.py`)**

- Dùng lại vòng lặp gọi tool `run_model_tool_loop` của `chat.py`, nên UI chạy đúng logic agent như khi chấm, và ghi transcript cùng định dạng với `chat.py`.
- Đọc trực tiếp `artifacts/system_prompt.md` và `artifacts/tools.yaml`: khi TV1/TV2 cập nhật prompt hoặc thêm tool (`hn_search`), UI tự dùng bản mới, không phải sửa code.
- Mỗi câu trả lời hiện đủ tool đã gọi, args, trạng thái (✅ ok / ⚠️ lỗi / ❓ hỏi lại / ✋ cần xác nhận) và JSON kết quả. Lỗi tool và lỗi provider luôn được hiển thị, không bị che.
- Có câu hỏi mẫu dạng nút bấm, danh sách tool lấy từ `tools.yaml`, và dòng thông tin số tool / số vòng / thời gian / trạng thái cho mỗi câu trả lời.
- Version label tự nhận theo `version_log.csv` (so hash prompt/tools), để transcript không bị gắn nhầm version.

**Script hỗ trợ phân tích (`starter_v0/scripts/show_failures.py`)**

- In nhanh run có hợp lệ hay không (`provider_error_cases`, `measured_cases`), các metric, hash và từng case FAIL (input, expect, actual, lý do). Dùng để điền bảng B2.

**Tích hợp và kiểm tra**

- Tạo nhánh `feat/huuthinh` từ nhánh của TV1 (`vudinhthang`, đã gộp tool của TV2) để ghép UI với prompt v3 và `hn_search`.
- Kiểm tra 4 run v0–v3 của TV1 và phát hiện run v3 có `provider_error_cases = 1` (case M05 bị 429), tức là chưa hợp lệ theo rubric. Đã báo TV1 để chạy lại.
- Phát hiện git trên Windows đổi ký tự xuống dòng (LF ↔ CRLF) làm hash prompt khác với hash trong `version_log.csv` dù nội dung giống hệt. Xử lý: UI so khớp hash theo cả hai kiểu xuống dòng; khi chat live dùng đúng bản prompt có hash `pd5ffefbef293`.

**Chat live và báo cáo**

- Chạy `python chat.py --provider gemini --version v3` với đủ 3 kịch bản: yêu cầu thường, thiếu thông tin rồi bổ sung, yêu cầu đăng Telegram. Kết quả: agent hỏi lại khi thiếu tài khoản, xin xác nhận yes/no trước khi gửi, gọi `lookup(news, day)` và trả tin có nguồn.
- Viết bảng B4, mục A1, A3 và dòng UI trong B5a của `group_report.md`.

## 4. Bằng chứng

- Commit: `3c4d555` — *feat(ui): add Streamlit UI for the research agent* (nhánh `feat/huuthinh`).
- Code: [`starter_v0/app.py`](../../starter_v0/app.py), [`starter_v0/scripts/show_failures.py`](../../starter_v0/scripts/show_failures.py), dòng `streamlit` trong [`starter_v0/requirements.txt`](../../starter_v0/requirements.txt).
- Transcript chat live v3: [`v3_gemini_20261111T024323043613.transcript.json`](../../starter_v0/transcripts/v3_gemini_20261111T024323043613.transcript.json) (`artifact_version = v3+pd5ffefbef293+t8a02817ed09c`).
- Báo cáo nhóm: [group_report.md](group_report.md) — A1, A3, B4, dòng UI trong B5a.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Claude Code để đọc repo, lập kế hoạch, viết `app.py`, `show_failures.py` và nháp các mục báo cáo.
  - Tự kiểm tra bằng cách:
    - chạy `streamlit run app.py` trên máy và thử các câu hỏi mẫu;
    - chạy test UI tự động (Streamlit AppTest) với provider giả để kiểm tra 3 tình huống: trả lời có tool, hỏi lại, lỗi provider;
    - chạy thật với Gemini `gemini-3.5-flash` + prompt v3;
    - chạy `pytest` sau khi ghép UI (93 passed, 0 failed);
    - đọc lại transcript để chắc không có API key trong file.

## 5. Khó khăn và cách xử lý

- **Hết quota Gemini (429):** free tier chỉ 20 request/ngày cho mỗi project và mỗi model. Tạo key mới trong cùng project không giúp được vì quota tính theo project. Cách xử lý: dùng key ở project khác, chuyển sang model `gemini-3.5-flash` giống TV1, và để dành quota cho lần chat live thật và showdown.
- **Thiếu `RAPIDAPI_KEY`:** ở lượt "Của Andrej Karpathy", model gọi đúng `timeline(screenname="karpathy", limit=5)` nhưng tool lỗi do máy chưa có key. Lỗi được hiện rõ trong UI/transcript; đã bổ sung key sau đó.
- **Nhầm môi trường lệnh:** ban đầu gõ lệnh PowerShell trong Git Bash; đã chuyển sang `source .venv/Scripts/activate` và `cp`.

## 6. Tự đánh giá

> *(Nháp — tự sửa lại theo đánh giá của bản thân)*

- Làm tốt: UI chạy được với prompt v3, hiện rõ tool call và lỗi đúng yêu cầu rubric; phát hiện run v3 chưa hợp lệ và lỗi hash do ký tự xuống dòng.
- Chưa tốt: chưa quản lý quota Gemini từ đầu nên mất nhiều request vào các lần chạy lỗi; lượt `timeline` trong transcript bị lỗi do chưa điền `RAPIDAPI_KEY` trước khi chat live.
- Nếu làm lại: chuẩn bị đủ key cho mọi tool và nhiều key Gemini trước buổi lab; chạy preflight cho từng tool trước khi chat live.
