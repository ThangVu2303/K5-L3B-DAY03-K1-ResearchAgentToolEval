# Báo cáo cá nhân — Nguyền Nhật Minh — 2A202603745

## 1. Thông tin thành viên

- Họ tên: Nguyền Nhật Minh
- MSSV: 2A202603745
- Email: nnhatminh2610@gmail.com
- GitHub: [NhMinh-2610](https://github.com/NhMinh-2610)
- Vai trò: Khai báo tool và phát triển tool mới, theo phân công nhóm.

## 2. Phần việc phụ trách

- Cải thiện description và quy ước args cho 10 tool có sẵn (C2).
- Bổ sung ít nhất 1 tool mới, TOOL.md, registry và khai báo YAML (C4).
- Bàn giao routing cho TV1 và input/output cho TV3 viết test/eval.
- Viết bảng A2 và phần tool mới của B5a trong báo cáo nhóm.

## 3. Đóng góp cụ thể

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

Kết quả kiểm tra:

```text
Trước thay đổi: 62 passed, 17 skipped
Sau thay đổi:   93 passed, 14 skipped, 0 failed
Smoke hn_search gọi API thật: thành công, trả về 1 item
```

Tôi đã tự chạy lại toàn bộ suite từ thư mục `starter_v0` trên Python 3.13.7,
pytest 9.2.0 bằng lệnh:

```powershell
& "$env:USERPROFILE\.venvs\research-lab\Scripts\python.exe" -m pytest
```

Terminal thu thập 107 test: 93 passed, 14 skipped, không có failed, thời gian
1.35 giây. Các test skipped là TODO của tool có sẵn; 26 trường hợp của tool mới
đều chạy thành công. Unit test sử dụng mock HTTP; kết quả pytest không đo
model routing.

Tôi cũng đã gọi trực tiếp `hn_search(query="AI agents", max_results=1,
sort_by="date")` để kiểm tra API thật. Kết quả trả về 1 item:

- Tiêu đề: “Ask HN: How do you keep secrets out of your AI agents' context?”
- Nguồn: [Hacker News, bài 50439393](https://news.ycombinator.com/item?id=50439393).
- Tác giả: `timbowhite`; tại thời điểm kiểm tra có 1 điểm và 1 bình luận.
- `url` và `hn_url` cùng trỏ tới trang thảo luận HN; `summary` là tiêu đề bài.

Lần gọi này xác nhận tool truy cập API và trả dữ liệu thật; chưa kiểm tra việc
model tự chọn tool trong hội thoại.

AI/công cụ đã dùng: Codex để đọc yêu cầu, viết/sửa code và tài liệu, chạy pytest,
smoke API và chuẩn bị PR nháp. Git được dùng để lưu lịch sử thay đổi; nguồn
API là [Algolia HN Search](https://hn.algolia.com/api).

## 5. Tự đánh giá

- Phần đã tự kiểm tra: chạy toàn bộ pytest và gọi trực tiếp hn_search qua API thật;
  kết quả được ghi ở mục 4.
- Nội dung đã hiểu: Chưa bổ sung.
- Khó khăn thực tế và cách xử lý: Chưa bổ sung.
- Điểm cần cải thiện: Chưa bổ sung.
