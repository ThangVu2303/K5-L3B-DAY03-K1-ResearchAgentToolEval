# Team

## Thông tin nhóm

- Tên nhóm: K1
- Lớp: L3B
- Repo nhóm: `K5-L3B-K1-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: main

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Vũ Đình Thắng | 2A202603753 | 26ai.thangvd2@vinuni.edu.vn | ThangVu2303 | Nhóm trưởng |
|   2 | Nguyễn Hữu Thịnh | 2A202603726 | 26ai.thinhnh2@vinuni.edu.vn | huuthinh812 | Thành viên |
|   3 | Vũ Bá Tùng Lâm | 2A202603775 | 26ai.lamvbt@vinuni.edu.vn | lamvu-dev | Thành viên |
|   4 | Nguyễn Nhật Minh | 2A202603745 | 26ai.minhnn7@vinuni.edu.vn | NhMinh-2610 | Thành viên |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/team/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/2A202603753_VuDinhThang.md`.

---

## Vũ Đình Thắng - 2A202603753

### Phần việc phụ trách

- Quản lý nhóm, phân chia công việc và tổng hợp báo cáo.
- Thiết lập môi trường dự án, cấu hình API Keys, chạy và theo dõi quá trình đánh giá baseline (v0 -> v3).

### Đóng góp cụ thể

- Setup môi trường ban đầu, chạy preflight và bộ eval.
- Phân tích nguyên nhân lỗi và tham gia tối ưu system prompt và tool declarations.

### Bằng chứng

- Các commit thiết lập và cải tiến prompt trong repo.

---

## Nguyễn Hữu Thịnh - 2A202603726

### Phần việc phụ trách

- Phát triển công cụ mới (Custom Tools) và viết unit test cho tool.

### Đóng góp cụ thể

- Xây dựng tool mới kèm `TOOL.md` và đăng ký trong registry `tools/__init__.py`.
- Viết các trường hợp kiểm thử (happy path, edge cases, error handling) trong `tests/test_tools_todo.py`.

### Bằng chứng

- Code tool mới trong `starter_v0/tools/` và unit tests tương ứng.

---

## Vũ Bá Tùng Lâm - 2A202603775

### Phần việc phụ trách

- Xây dựng bộ đánh giá của nhóm (`eval_group.json`) và phân tích failure logs.

### Đóng góp cụ thể

- Soạn thảo 10 eval cases (5 single-turn và 5 multi-turn) bao phủ các lỗi routing, arguments và boundary.
- Đánh giá độ chính xác của agent qua từng phiên bản.

### Bằng chứng

- File `starter_v0/data/eval_group.json` và phân tích kết quả test.

---

## Nguyễn Nhật Minh - 2A202603745

### Phần việc phụ trách

- Xây dựng giao diện người dùng (UI Streamlit), tích hợp chat live và deploy dùng thử.

### Đóng góp cụ thể

- Phát triển ứng dụng web chat tương tác trực tiếp với Agent.
- Thực hiện các phiên chat live (multi-turn) và thu thập file transcript.

### Bằng chứng

- File giao diện `starter_v0/app.py` và các file transcript trong `starter_v0/transcripts/`.
