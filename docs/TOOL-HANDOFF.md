# Bàn giao khai báo tool và hn_search

## Đối chiếu yêu cầu

| Yêu cầu | Sản phẩm | Căn cứ |
| --- | --- | --- |
| Mô tả chức năng, khi dùng/không dùng và args của tool | `starter_v0/artifacts/tools.yaml`, 10 tool hiện có | CP2, rubric C2 |
| Ít nhất 1 tool mới, TOOL.md và đăng ký | `starter_v0/tools/hn_search/`, registry và YAML | CP3, rubric C4 |
| Ít nhất 3 test/tool mới, suite không failed | 26 trường hợp trong `tests/test_tools_todo.py` | CP3, README Step 4b |
| Routing, bảng tool và bằng chứng tool mới | Hướng dẫn dưới đây, A2 và B5a | Phân công nhóm, mẫu báo cáo nhóm |

Nguồn: [CHECKPOINTS](../CHECKPOINTS.md), [RUBRIC](../RUBRIC.md),
[tool contract](../starter_v0/tools/README.md).

## TV1 — Declaration và routing

Nhận `starter_v0/artifacts/tools.yaml`. Tên, kiểu tham số, default, enum và
required của 10 tool hiện có được giữ nguyên. Description bổ sung handle không
có `@`, news/timeframe, Latest/Top, xác nhận gửi, giới hạn 10 paper và đoạn text
arXiv 1000–20000 ký tự.

Quy tắc tích hợp vào prompt:

> Khi yêu cầu tìm bài trên Hacker News/HN theo một chủ đề cụ thể, dùng hn_search.
> Chọn sort_by=date cho mới nhất, relevance cho độ liên quan. Thiếu chủ đề thì
> hỏi clarify. Với tweet dùng tool Twitter/X, với tìm web chung dùng lookup.
> hn_search trả metadata; dùng fetch để đọc URL bài gốc nếu cần.

Bản starter nguyên gốc nằm ở commit
`c68da4cdb50c118c9f00622bd72e6cd7afc57b18`. Nếu chưa có run v0, TV1 chạy baseline
trên commit này; bản main có declaration mới dành cho các vòng cải tiến. Không
dùng declaration đã sửa để ghi kết quả v0. TV1 kiểm chứng các thay đổi bằng base
eval và ghi giả thuyết, hash, metric vào version log.
Prompt, các bộ eval và version log chưa được thay đổi trong phần khai báo và bổ sung tool.

## TV3 — Tool, test và eval case

```python
hn_search(query: str = "", max_results: int = 5, sort_by: str = "relevance") -> dict
```

| Input hoặc tình huống | Hành vi |
| --- | --- |
| `query` | Chuỗi có nội dung; bỏ khoảng trắng đầu/cuối |
| `max_results` | Integer 1–20; mặc định 5; từ chối boolean, float và chuỗi số |
| `sort_by` | `relevance` hoặc `date`; mặc định `relevance` |
| Input sai | Error dict, không gọi HTTP |
| HTTP/timeout/JSON hoặc response sai | Error dict, không raise ra agent |
| URL bài thiếu hoặc sai định dạng | Dùng link thảo luận HN; giữ các hit khác |
| Không có hit hợp lệ | `items=[]` |

Success có `tool`, `query`, `sort_by`, `max_results`, `items`. Mỗi item gồm
`title`, `url`, `source`, `summary`, `hn_url`, `author`, `date`, `metrics`.
`summary` là tiêu đề, không phải tóm tắt toàn văn. Xem
[TOOL.md](../starter_v0/tools/hn_search/TOOL.md).

Test nằm ở phần YOUR NEW TOOL(S) trong `starter_v0/tests/test_tools_todo.py`.
TV3 tiếp nhận để review/bổ sung và thêm ít nhất 1 case route tới tool mới vào
bộ 10 case nhóm. Ví dụ đầu vào và kết quả mong đợi:

| Yêu cầu | Tool/args mong đợi |
| --- | --- |
| Tìm 3 bài mới nhất trên Hacker News về AI agents | `hn_search(query="AI agents", max_results=3, sort_by="date")` |

Ví dụ trên là đề xuất case, chưa phải kết quả chạy model.

## TV4 — Báo cáo nhóm

A2 đã có đủ 11 tool. B5a đã có nguồn code, kết quả tool và unit test; TV4 tổng
hợp cùng phần UI/live chat. Xem [group_report.md](../report/team/group_report.md).

## Kiểm tra

Chạy lại từ `starter_v0/` bằng môi trường Python đã cài dependency:

```bash
python -m pytest -q
```

- Toàn suite: **93 passed, 14 skipped, 0 failed**; gồm contract test và 26
  trường hợp cho tool mới. 14 skipped là các TODO của tool có sẵn.
- Regression test bắt được lỗi URL `https://[invalid` trước sửa; sau sửa cả
  5 trường hợp URL không hợp lệ đều pass và giữ được hit hợp lệ tiếp theo.
- Tool đã gọi API thật với `query="AI agents", max_results=1, sort_by="date"`
  và trả về 1 item. Đây là kiểm tra tool; hiệu quả model routing do TV1/TV3 đo.

Nguồn API: [Algolia HN Search](https://hn.algolia.com/api), `/search`,
`/search_by_date`, `query`, `tags=story`, `hitsPerPage`.
