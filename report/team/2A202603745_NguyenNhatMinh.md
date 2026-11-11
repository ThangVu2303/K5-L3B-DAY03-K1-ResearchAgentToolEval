# Báo cáo cá nhân — Nguyền Nhật Minh — 2A202603745

## 1. Thông tin thành viên

- Họ tên: Nguyền Nhật Minh
- MSSV: 2A202603745
- Email: Chưa điền.
- GitHub: [NhMinh-2610](https://github.com/NhMinh-2610)
- Vai trò: Khai báo tool và phát triển tool mới, theo phân công nhóm.

## 2. Phần việc phụ trách

- Cải thiện description và quy ước args cho 10 tool có sẵn (C2).
- Bổ sung ít nhất 1 tool mới, TOOL.md, registry và khai báo YAML (C4).
- Bàn giao routing cho TV1 và input/output cho TV3 viết test/eval.
- Viết bảng A2 và phần tool mới của B5a trong báo cáo nhóm.

## 3. Đóng góp cụ thể

Các thay đổi dưới đây được thực hiện với Codex hỗ trợ viết code, tài liệu và
chạy kiểm chứng; thành viên cần đọc và tự giải thích được trước khi nộp.

- Viết lại declaration cho 10 tool, phân biệt khi dùng/không dùng; làm rõ handle
  không có @, news/timeframe, Latest/Top và xác nhận boolean trước khi gửi Telegram.
- Thêm `hn_search` tìm bài trên Hacker News qua Algolia: validate input, phân
  biệt tìm theo liên quan/thời gian, chuẩn hóa item, trả error dict khi có lỗi.
- Viết TOOL.md và đăng ký tool đầy đủ; dùng dependency `requests` có sẵn.
- Bổ sung test minh chứng để bàn giao TV3: request/mapping, input xấu không gọi
  mạng, HTTP/timeout, response và hit không hợp lệ. Các TODO của tool cũ giữ nguyên.
- Cập nhật A2/dòng tool mới B5a và soạn `docs/TOOL-HANDOFF.md` cùng change request.

## 4. Bằng chứng và kiểm chứng

- Declaration: [tools.yaml](../../starter_v0/artifacts/tools.yaml).
- Tool mới: [tool.py](../../starter_v0/tools/hn_search/tool.py),
  [TOOL.md](../../starter_v0/tools/hn_search/TOOL.md),
  [registry](../../starter_v0/tools/__init__.py).
- Test: [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py),
  phần YOUR NEW TOOL(S).
- Báo cáo: [group_report.md](group_report.md), A2 và dòng tool mới B5a.
- Bàn giao và lệnh kiểm tra: [TOOL-HANDOFF.md](../../docs/TOOL-HANDOFF.md).
- Change request: [CHANGE_REQUEST.md](../../CHANGE_REQUEST.md).
- Commit kỹ thuật: xem [lịch sử nhánh NguyenNhatMinh](https://github.com/ThangVu2303/K5-L3B-DAY03-K1-ResearchAgentToolEval/commits/NguyenNhatMinh).

Kết quả tự động Codex đã chạy trên môi trường Python của lab:

```text
Trước thay đổi: 62 passed, 17 skipped
Sau thay đổi:   88 passed, 14 skipped, 0 failed
Smoke hn_search gọi API thật: thành công, trả về 1 item
```

Log chi tiết của AI được giữ local theo yêu cầu; handoff chứa tóm tắt và lệnh để
người khác tái kiểm chứng. Lần smoke đầu bị chặn DNS trong sandbox; chạy lại
cùng code với quyền mạng thành công. Unit test dùng mock, không gọi API thật.
Không có run model hay metric routing v0–v3 trong phần việc này.

AI/công cụ đã dùng: Codex để đọc yêu cầu, viết/sửa code và tài liệu, chạy pytest,
smoke API và chuẩn bị PR nháp. Git được dùng để lưu lịch sử thay đổi; nguồn
API là [Algolia HN Search](https://hn.algolia.com/api).

## 5. Tự đánh giá

Chưa tự đánh giá thay cho thành viên. Trước khi nộp, chính thành viên cần:

- Đọc và giải thích được sự khác nhau giữa các tool, args và boundary xác nhận.
- Tự chạy lại test, thử tool và ghi nhận kết quả kiểm tra bằng tay của mình.
- Xác nhận những gì đã hiểu, khó khăn gặp phải và phần cần cải thiện bằng trải
  nghiệm thực tế; bổ sung email và hoàn thiện mục này.
