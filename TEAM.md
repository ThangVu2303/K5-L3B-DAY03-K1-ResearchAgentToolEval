# Team

## Thông tin nhóm

- Tên nhóm: K1
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-K1-ResearchAgentToolEval`
- URL repo: https://github.com/ThangVu2303/K5-L3B-DAY03-K1-ResearchAgentToolEval
- Nhánh nộp, commit chốt: TV1 cập nhật trước khi nộp.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Chưa điền | Chưa điền | Chưa điền | Chưa điền | TV1 — Nhóm trưởng / Prompt, base eval v0–v3 |
|   2 | Nguyền Nhật Minh | 2A202603745 | Chưa điền | [NhMinh-2610](https://github.com/NhMinh-2610) | TV2 — Tool declaration + tool mới |
|   3 | Chưa điền | Chưa điền | Chưa điền | Chưa điền | TV3 — Unit test + eval nhóm |
|   4 | Chưa điền | Chưa điền | Chưa điền | Chưa điền | TV4 — UI, demo, tổng hợp báo cáo |

Phân vai theo bản `PHAN_CONG.md` nhóm cung cấp. Yêu cầu công việc và bằng chứng
đối chiếu [CHECKPOINTS](CHECKPOINTS.md), [RUBRIC](RUBRIC.md) và
[SUBMISSION](SUBMISSION.md); cách chia TV1–TV4 là phân công của nhóm.

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## TV2 — Nguyền Nhật Minh — 2A202603745

### Phần việc phụ trách

- Cải thiện khai báo 10 tool có sẵn và thêm tool mới, theo phần TV2 của nhóm.
- Bàn giao routing cho TV1, contract/test minh chứng cho TV3, A2/B5a cho TV4.

### Đóng góp cụ thể

- Nhánh `NguyenNhatMinh`: cải thiện description/args convention và boundary xác
  nhận gửi; bổ sung `hn_search`, TOOL.md, registry và YAML.
- Bổ sung test tool mới với Codex hỗ trợ; suite thực tế 88 passed, 14 skipped,
  0 failed. Live tool smoke trả về 1 item; chưa đo model routing.
- Cập nhật A2/dòng tool mới B5a, tài liệu bàn giao và change request. Phần tự
  đánh giá cá nhân và email còn để chính thành viên hoàn thiện.

### Bằng chứng

- [Bàn giao TV2](docs/TV2-HANDOFF.md), có link code, test, kết quả và giới hạn.
- [Báo cáo cá nhân TV2](report/team/2A202603745_NguyenNhatMinh.md).
- [Change request](CHANGE_REQUEST_TV2.md).
- [Lịch sử commit kỹ thuật trên nhánh](https://github.com/ThangVu2303/K5-L3B-DAY03-K1-ResearchAgentToolEval/commits/NguyenNhatMinh).
