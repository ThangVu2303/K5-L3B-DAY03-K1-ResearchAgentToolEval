# Báo cáo cá nhân — Vũ Đình Thắng — 2A202603753

## 1. Thông tin thành viên

- Họ tên: Vũ Đình Thắng
- MSSV: 2A202603753
- Email: 26ai.thangvd2@vinuni.edu.vn
- GitHub: [ThangVu2303](https://github.com/ThangVu2303)
- Vai trò: **TV1 — Nhóm trưởng / Prompt Engineer** (Phụ trách chính Rubric **C1: 10đ** và **C3: 20đ**).

## 2. Phần việc phụ trách

Theo phân công trong [TEAM.md](../../TEAM.md):
- Quản lý nhóm, phân chia công việc, khởi tạo repo nhóm và hoàn thiện tài liệu `TEAM.md`.
- Thiết lập môi trường dự án (`.env`), khắc phục lỗi kết nối provider, chạy kiểm tra preflight.
- Chạy đánh giá **Baseline v0 hợp lệ** (`provider_error_cases == 0` và `measured_cases == 20`), phân tích các case FAIL và lập bảng B2 (Failure Analysis) trong `group_report.md` (Rubric C1).
- Thực hiện chuỗi cải tiến lặp theo phương pháp khoa học (mỗi vòng 1 giả thuyết) qua các phiên bản **v1 ➔ v2 ➔ v3**, chạy eval và ghi log đầy đủ vào `artifacts/version_log.csv` (Rubric C3).
- Hoàn thiện các phần báo cáo nhóm thuộc trách nhiệm TV1: Bảng B1 (Version Evidence), B2 (Failure Analysis), Mục 1 (Thông tin nhóm), Mục 3 (Giải pháp), Mục 5 (Khó khăn & xử lý), và Mục 7 (B6. Reflection).

## 3. Đóng góp cụ thể

### a. Khắc phục lỗi Provider & Thiết lập Baseline v0 (Rubric C1)
- Ban đầu run v0 bị lỗi cạn quota do tài khoản Free Tier Google AI Studio bị siết hạn ngạch 20 requests/ngày và model cũ `gemini-2.5-flash`.
- Đã can thiệp kỹ thuật vào `starter_v0/providers/gemini_provider.py`: chuyển model mặc định sang `gemini-3.5-flash`, bổ sung timeout kết nối 30s, thêm độ trễ an toàn 3s giữa các request và cơ chế tự động retry với exponential backoff khi gặp lỗi 429/503.
- Chạy thành công run **v0 hợp lệ**: [v0_B_base_gemini_20261110T195405860459.json](../../starter_v0/runs/v0_B_base_gemini_20261110T195405860459.json) với `measured_cases: 20`, `provider_error_cases: 0`, đạt độ chính xác `55.0%` (11/20 pass).
- Phân tích chi tiết 9 failure cases ban đầu và điền bảng B2 trong `group_report.md`.

### b. Vòng lặp cải tiến v1 ➔ v3 dựa trên bằng chứng (Rubric C3)
- **Phiên bản v1 (Thay đổi `system_prompt.md`):**
  + *Giả thuyết:* Loại bỏ các chỉ dẫn xấu của starter prompt (đoán mò, tự ý gửi tin nhắn, hoàn thành trong 1 bước); bổ sung rule gọi `clarify` khi thiếu thông tin, xin xác nhận trước khi gửi `send`, từ chối ngoài phạm vi, và cho phép gọi nhiều tool song song.
  + *Kết quả:* Run [v1_B_base_gemini_20261110T215625710195.json](../../starter_v0/runs/v1_B_base_gemini_20261110T215625710195.json) đạt `80.0%` (16/20 pass), routing accuracy tăng lên `90.0%`.
- **Phiên bản v2 (Thay đổi `tools.yaml`):**
  + *Giả thuyết:* Áp dụng khai báo `tools.yaml` mới do TV2 bàn giao (nêu rõ khi nào dùng/không dùng, quy ước args không có `@`, timeframe, Top/Latest, đăng ký `hn_search`).
  + *Kết quả:* Run [v2_B_base_gemini_20261110T221714362720.json](../../starter_v0/runs/v2_B_base_gemini_20261110T221714362720.json) đạt `85.0%` (17/20 pass), multi-turn đạt `100.0%`.
- **Phiên bản v3 (Tối ưu Prompt đa lượt & routing `hn_search`):**
  + *Giả thuyết:* Chuẩn hóa trích xuất query ngắn cho `lookup`, trích xuất handle cho `timeline`, bắt buộc `response_type="yes_no"` khi xin xác nhận gửi Telegram, tích hợp routing cho tool mới `hn_search`, duy trì ngữ cảnh multi-turn.
  + *Kết quả:* Run [v3_B_base_gemini_20261110T225014036508.json](../../starter_v0/runs/v3_B_base_gemini_20261110T225014036508.json) đạt độ chính xác kỷ lục **`100.0%`** (19/19 cases đo lường đều PASS tuyệt đối).

## 4. Bằng chứng và kiểm chứng

- **Lịch sử phiên bản:** [version_log.csv](../../starter_v0/artifacts/version_log.csv) ghi đầy đủ 4 dòng (v0: 0.55 ➔ v1: 0.80 ➔ v2: 0.85 ➔ v3: 1.00) kèm hash prompt, hash tools và lý do thay đổi.
- **File run bằng chứng:**
  + Run v0: `starter_v0/runs/v0_B_base_gemini_20261110T195405860459.json`
  + Run v1: `starter_v0/runs/v1_B_base_gemini_20261110T215625710195.json`
  + Run v2: `starter_v0/runs/v2_B_base_gemini_20261110T221714362720.json`
  + Run v3: `starter_v0/runs/v3_B_base_gemini_20261110T225014036508.json`
- **Tài liệu báo cáo:** [group_report.md](group_report.md) (Bảng B1, B2, Mục 1, 3, 5, 7).
- **Mã nguồn prompt:** [system_prompt.md](../../starter_v0/artifacts/system_prompt.md).
- **Kiểm thử hợp đồng:** `pytest tests/test_tool_contract.py` đạt **60/60 passed**.

AI/công cụ đã dùng: Trợ lý AI (Google Antigravity) được sử dụng để phân tích lỗi từ JSON log, hỗ trợ viết code retry trong provider, kiểm tra regex format và chạy các script tự động hóa đánh giá.

## 5. Tự đánh giá

- Hoàn thành đầy đủ 100% các nhiệm vụ được giao cho vai trò Thành viên 1 / Nhóm trưởng đúng hạn.
- Thực hiện nghiêm túc phương pháp lặp khoa học dựa trên bằng chứng log thật, giải thích tường minh nguyên nhân lỗi và giải pháp xử lý.
- Độ chính xác của agent tăng trưởng vượt bậc qua từng phiên bản: 55.0% ➔ 80.0% ➔ 85.0% ➔ 100.0%.
