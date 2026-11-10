# Bàn giao TV2 — Tool declaration và hn_search

## Phạm vi và căn cứ

Theo phân công TV2 của nhóm: cải thiện declaration, thêm ít nhất 1 tool,
bàn giao routing cho TV1, input/output cho TV3, bảng A2 và phần tool của B5a.
Yêu cầu gốc: [CP2/CP3](../CHECKPOINTS.md), [rubric C2/C4](../RUBRIC.md),
[tool contract](../starter_v0/tools/README.md).

## Thay đổi đã thực hiện

- Viết lại description và quy ước args của 10 tool có sẵn trong
  `starter_v0/artifacts/tools.yaml`: khi nào dùng, khi nào không dùng, handle
  không có `@`, news/timeframe, Latest/Top, boolean xác nhận gửi Telegram.
- Giữ nguyên tên, kiểu tham số, default, enum và required của 10 tool có sẵn.
- Thêm `hn_search`, tài liệu TOOL.md, đăng ký registry và khai báo YAML.
- Thay 3 stub YOUR NEW TOOL(S) bằng test thật; bổ sung case response thiếu/sai
  và kết quả không hợp lệ. Các TODO của tool có sẵn giữ nguyên để TV3 tiếp nhận.
- Điền A2 và dòng tool mới của B5a; có báo cáo TV2 và change request.

## Bàn giao TV1: routing và version

Câu routing đề xuất để TV1 review rồi tự tích hợp vào system prompt:

> Khi người dùng yêu cầu tìm bài trên Hacker News/HN về một chủ đề cụ thể,
> dùng hn_search với query là chủ đề đó. Chọn sort_by=date cho mới nhất và
> relevance cho độ liên quan. Nếu thiếu chủ đề, hỏi clarify. Không dùng hn_search
> cho tweet, tìm web chung hoặc bảng xếp hạng front page. Tool trả metadata;
> nếu cần đọc bài gốc, dùng fetch cho URL đã tìm được.

Ví dụ để thử bằng model (chưa phải kết quả eval):

- “Tìm 3 bài mới nhất trên Hacker News về AI agents.”
  → `hn_search(query="AI agents", max_results=3, sort_by="date")`.
- “Tìm bài liên quan đến SQLite trên HN.”
  → `hn_search(query="SQLite", sort_by="relevance")`.
- “Đọc kỹ bài ở URL này…” → `fetch`; “Mọi người nói gì trên Twitter…”
  → `social_search`; không route hai trường hợp này sang `hn_search`.

TV1 lấy v0 từ bản starter nguyên gốc trước khi tích hợp declaration này.
Nhánh TV2 giữ nguyên `system_prompt.md`, eval gốc và version log; không có
run model v0–v3 hay metric routing mới do TV2 tạo. TV1 kiểm chứng giả thuyết
v2 bằng run thật và ghi đúng hash/artifact vào version log. Không gộp nhiều
giả thuyết độc lập trong một version chỉ để đủ nhãn.

## Bàn giao TV3: contract và test

```python
hn_search(query: str = "", max_results: int = 5, sort_by: str = "relevance") -> dict
```

| Input | Hành vi |
| --- | --- |
| `query` có nội dung | Bỏ khoảng trắng đầu/cuối trước request |
| `max_results` | Integer 1–20; từ chối 0, âm, >20, boolean, float, chuỗi số |
| `sort_by` | Chỉ `relevance` hoặc `date` |
| Input sai | Error dict, không gọi HTTP |
| HTTP 429/500, timeout, JSON/response sai | Error dict, không raise ra agent |
| Không có hit hợp lệ | `items=[]`, không bịa bài |

Success: `tool`, `query`, `sort_by`, `max_results`, `items`. Item có `title`,
`url`, `source`, `summary`, `hn_url`, `author`, `date`, `metrics.points` và
`metrics.comments`. `summary` hiện là tiêu đề; không phải tóm tắt toàn văn.
URL ngoài thiếu/không phải http(s) thì dùng link thảo luận HN. Xem
[`TOOL.md`](../starter_v0/tools/hn_search/TOOL.md) để biết giới hạn.

Test nằm trong phần YOUR NEW TOOL(S) của
`starter_v0/tests/test_tools_todo.py`, dùng `fake_http` của starter. Có 21
test instance cho tool mới: request/ánh xạ dữ liệu, validation không gọi mạng,
HTTP/timeout, hit không hợp lệ và response sai schema. TV3 review/bổ sung,
đặc biệt case model routing trong 10 case nhóm; ví dụ ở trên chưa được thêm
vào eval_group.json và chưa được chạy qua model.

## Kết quả kiểm chứng thực tế

Lệnh chạy từ root repo:

```powershell
& "$env:USERPROFILE\.venvs\research-lab\Scripts\python.exe" -m pytest starter_v0/tests -q
```

| Kiểm tra | Kết quả |
| --- | --- |
| Toàn suite trước thay đổi | 62 passed, 17 skipped |
| Toàn suite sau thay đổi | 88 passed, 14 skipped, 0 failed |
| Contract YAML/registry/signature/TOOL.md | Pass trong suite trên |
| Tool mới gọi API thật với `AI agents`, 1 kết quả, sort `date` | Thành công, trả về 1 item |

14 skipped còn lại là TODO test của các tool starter; không nhận bonus 0 skipped.
Lần smoke đầu trong sandbox bị lỗi DNS; cùng code chạy có quyền mạng đã thành
công. Đây là tool smoke test, không phải model eval và không chứng minh routing
accuracy đã tăng. Kết quả tìm kiếm có thể thay đổi theo thời gian.

Log chi tiết cho AI/phiên làm việc được giữ local dưới `.local/tv2/` và gitignore.
Bản tóm tắt kiểm chứng ở đây được chia sẻ để người nhận đối chiếu và chạy lại;
không có API key/token trong tài liệu hoặc log được commit.

## Bàn giao TV4 và phần cá nhân

- A2 và dòng tool mới B5a đã cập nhật trong
  [`group_report.md`](../report/team/group_report.md); TV4 tiếp tục tổng hợp.
- TV2 có báo cáo `report/team/2A202603745_NguyenNhatMinh.md`; phần tự đánh giá
  và tự kiểm tra bằng tay cần chính thành viên hoàn thiện trung thực.
- Mỗi thành viên vẫn cần commit kỹ thuật và tự nộp link repo trên LMS theo
  [SUBMISSION](../SUBMISSION.md). Chưa đánh dấu những việc đó đã nộp xong.

## Nguồn API

[Algolia HN Search API](https://hn.algolia.com/api): `/search` và
`/search_by_date`, `query`, `tags=story`, `hitsPerPage`. Code tool là phần viết
mới cho lab, không sao chép implementation từ thư viện ngoài.
