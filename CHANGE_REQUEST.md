# Khai báo tool và tìm kiếm Hacker News

## Thay đổi

- Làm rõ chức năng, khi dùng/không dùng và quy ước tham số của 10 tool hiện có.
  Giữ nguyên tên và schema; mô tả đúng giới hạn của `papers` và `paper_text`.
- Thêm `hn_search` để tìm bài theo chủ đề trên Hacker News, chọn độ liên quan
  hoặc thời gian. Bổ sung code, TOOL.md, registry và khai báo YAML.
- Kiểm tra input trước khi gọi mạng; lỗi HTTP/timeout trả error dict. URL bài
  sai định dạng chuyển sang link thảo luận HN, các kết quả khác vẫn được giữ.
- Bổ sung test, bảng A2/B5a và [tài liệu bàn giao](docs/TOOL-HANDOFF.md).
  Nhật ký cục bộ `.local/` được gitignore.

## Kiểm tra

```text
Pytest: 93 passed, 14 skipped, 0 failed
hn_search: 26 trường hợp kiểm thử offline
API thật: trả về 1 item cho query=AI agents, sort_by=date
```

Contract test kiểm tra YAML, registry, chữ ký hàm và TOOL.md. Test tool mới phủ
request/response, input sai, HTTP 429/500, timeout, response sai cấu trúc và URL
sai định dạng. Regression test đã tái hiện lỗi URL trước khi sửa và pass sau sửa.
14 test skipped là các TODO của tool có sẵn, được phép trong phần bắt buộc.

## Tích hợp

- TV1 lấy baseline v0 nguyên bản, sau đó tích hợp declaration và đo bản v2.
- TV3 nhận contract/test, thêm case gọi `hn_search` vào bộ eval nhóm.
- TV4 nhận bảng A2 và các dòng tool/test của B5a.
- Prompt, eval gốc và version log được giữ nguyên. Hiệu quả routing cần được
  xác nhận bằng run model của TV1/TV3.
- `hn_search` trả metadata, không đọc toàn văn hoặc lấy bảng xếp hạng front page;
  `summary` là tiêu đề bài. Quy tắc xác nhận `send` nằm trong declaration;
  implementation `send` không thay đổi trong PR này.

Căn cứ: [CP2/CP3](CHECKPOINTS.md), [C2/C4](RUBRIC.md),
[tool contract](starter_v0/tools/README.md) và phân công công việc của nhóm.
