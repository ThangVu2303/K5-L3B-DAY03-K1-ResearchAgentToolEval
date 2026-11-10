# Team

## Thông tin nhóm

- Tên nhóm: K1
- Lớp: L3B
- Repo nhóm: `K5-L3B-K1-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: https://github.com/ThangVu2303/K5-L3B-DAY03-K1-ResearchAgentToolEval, nhánh vudinhthang, commit chốt: 4d07ea0

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Vũ Đình Thắng | 2A202603753 | 26ai.thangvd2@vinuni.edu.vn | ThangVu2303 | TV1 — Nhóm trưởng / Prompt (C1, C3) |
|   2 | Nguyễn Nhật Minh | 2A202603745 | 26ai.minhnn7@vinuni.edu.vn | NhMinh-2610 | TV2 — Tool declaration + Tool mới (C2, C4) |
|   3 | Vũ Bá Tùng Lâm | 2A202603775 | 26ai.lamvbt@vinuni.edu.vn | lamvu-dev | TV3 — Test + Eval (C4, C5) |
|   4 | Nguyễn Hữu Thịnh | 2A202603726 | 26ai.thinhnh2@vinuni.edu.vn | huuthinh812 | TV4 — UI, Demo, Báo cáo (C6, C7) |

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

## Vũ Bá Tùng Lâm - 2A202603775 (TV3 — Test + Eval)

### Phần việc phụ trách

- Chạy kiểm thử ban đầu và đảm bảo các bài test hợp đồng `test_tool_contract.py` luôn đạt 100%.
- Viết unit tests (≥ 3 tests) cho tool mới `hn_search` trong `tests/test_tools_todo.py` bao phủ happy path, input xấu và xử lý lỗi mạng (C4).
- Xây dựng bộ đánh giá của nhóm `starter_v0/data/eval_group.json` gồm 10 cases (5 single-turn và 5 multi-turn) bao gồm case gọi tới tool mới (C5).
- Chạy đánh giá `--suite group`, phân tích kết quả và hoàn thiện bảng B3, B5a trong báo cáo nhóm.

### Đóng góp cụ thể

- Đảm bảo toàn bộ test suite chạy xanh không có lỗi.
- Xây dựng 10 eval cases độc lập với đầy đủ `what_it_tests`, `failure_type`, `expect` bao phủ các ranh giới phức tạp.
- Đánh giá chất lượng của agent trên bộ test riêng của nhóm.

### Bằng chứng

- File `starter_v0/data/eval_group.json`.
- File unit test `starter_v0/tests/test_tools_todo.py`.
- Run JSON suite group trong `starter_v0/runs/`.

---

## Nguyễn Hữu Thịnh - 2A202603726 (TV4 — UI, Demo, Báo cáo)

### Phần việc phụ trách

- Phát triển và hoàn thiện giao diện ứng dụng web tương tác với Agent bằng Streamlit trong `starter_v0/app.py` (C6).
- Hiển thị trực quan quá trình agent gọi tool, tham số truyền vào và kết quả trả về (không che giấu lỗi).
- Thiết lập đường dẫn demo trực tuyến qua Cloudflare Tunnel cho buổi Team Showdown.
- Thực hiện phiên chat trực tiếp (chat live đa lượt) với agent, thu thập file transcript vào `starter_v0/transcripts/` và viết bảng B4.
- Hoàn thiện Phần A (A1, A3) và tổng hợp báo cáo nhóm `report/team/group_report.md` (C7).

### Đóng góp cụ thể

- Hoàn thành giao diện chat trực quan với Streamlit, hỗ trợ trải nghiệm người dùng mượt mà.
- Triển khai thành công ứng dụng demo public để các nhóm khác có thể trải nghiệm trực tiếp.
- Thu thập và kiểm tra các file transcript hội thoại live multi-turn.

### Bằng chứng

- File giao diện `starter_v0/app.py`.
- File cấu hình và dependency trong `starter_v0/requirements.txt`.
- Các file transcript tại `starter_v0/transcripts/`.
- Mục A1, A3, B4 trong `report/team/group_report.md`.
