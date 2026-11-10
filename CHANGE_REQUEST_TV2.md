# TV2: làm rõ khai báo tool và bổ sung Hacker News search

## Vấn đề và hành vi sau thay đổi

Declaration starter chưa phân biệt rõ nguồn web/Twitter/policy/paper, quy ước
args và xác nhận gửi. Model thiếu thông tin để chọn tool hoặc điền args đúng.
Bản này mô tả rõ khi dùng/không dùng cho 10 tool hiện có và bổ sung `hn_search`
để xử lý yêu cầu tìm bài trên Hacker News.

Ví dụ: yêu cầu “3 bài mới nhất trên Hacker News về AI agents” có tool phù hợp
với `query="AI agents", max_results=3, sort_by="date"`. Việc model có chọn đúng
hay không cần TV1/TV3 đo bằng eval thật; PR chưa có metric cải thiện.

## Phạm vi

- `starter_v0/artifacts/tools.yaml`: cải thiện description/arg convention, giữ
  tên và schema args của 10 tool hiện có; thêm khai báo `hn_search`.
- `starter_v0/tools/hn_search/`: code và TOOL.md; đăng ký trong registry.
- `starter_v0/tests/test_tools_todo.py`: test tool mới, mock HTTP, các TODO cũ
  còn nguyên. TV3 nhận các test này để review/bổ sung theo phân công C4.
- Báo cáo nhóm chỉ cập nhật A2 và dòng tool mới B5a; bổ sung báo cáo cá nhân TV2,
  thông tin TV2 trong TEAM và tài liệu bàn giao.
- `.gitignore`: giữ `.local/tv2/` local theo yêu cầu; log phiên làm việc, log
  pytest và smoke result không được push lên GitHub.

## Kiểm chứng

```text
Before: 62 passed, 17 skipped
After:  88 passed, 14 skipped, 0 failed
Live hn_search smoke: success, 1 item (query=AI agents, sort_by=date)
```

Toàn suite bao gồm contract check giữa YAML, registry, chữ ký hàm và TOOL.md.
Tool mới có 21 test instance, gồm input lỗi không gọi mạng, mapping request/
response, HTTP 429/500, timeout và response sai cấu trúc. Smoke API thật được
chạy riêng; lần sandbox lỗi DNS và lần có quyền mạng thành công đều lưu local.
Lệnh tái kiểm tra và chi tiết xem [TV2 handoff](docs/TV2-HANDOFF.md).

## Bàn giao và giới hạn

- **Draft cho TV1 review:** phải có baseline v0 nguyên bản trước khi ghép
  declaration mới; TV1 nhận routing và kiểm chứng v2, TV3 bổ sung eval case.
- `system_prompt.md`, eval base/extension/group và version log được giữ nguyên;
  không tạo run/metric/transcript giả hoặc chạy thay phần base eval của TV1.
- `hn_search` cần mạng, không cần API key; không có retry, không đọc toàn văn
  hoặc lấy bảng xếp hạng front page. `summary` hiện là tiêu đề tìm được.
- Thay đổi mô tả xác nhận `send` không sửa implementation guardrail của starter.
- 14 TODO skipped còn lại thuộc phần test mở rộng của TV3; không nhận bonus
  0 skipped. Chưa thực hiện bonus thêm 4 tool.
- Thông tin người khác trong TEAM, email chưa cung cấp và tự đánh giá cá nhân
  để người liên quan hoàn thiện; không nhận là các mục đã hoàn tất.

## Căn cứ

[CP2/CP3](CHECKPOINTS.md), [C2/C4](RUBRIC.md),
[tool folder contract](starter_v0/tools/README.md), [quy định nộp](SUBMISSION.md),
và phần TV2 trong bản phân công nhóm cung cấp.
