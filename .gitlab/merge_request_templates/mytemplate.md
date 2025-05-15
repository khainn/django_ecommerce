## Purpose
- Why you did what you did.

## How To Test
- Where reviewers can see your changes. What they should attempt to do.

## What changed
- What changed in what you did

## Notes
- Ticket ID (link Jira or taskID)

## Pre-MR Checklist
- [X] Branch name: 
  - [X] Đảm bảo đúng, đủ tiền tố (feature/fix/update/…)
  - [X] module/feature name, subtask title… ngắn gọn
  - [X] với các fix bug cần có hậu tố bug ID.
- [X] Commit comment:\
Một branch có thể có nhiều commits nếu như khối lượng code liên quan đến nhiều phần (nhiều functions) hoặc nhiều bước, thì mỗi phần, mỗi bước này cần tách riêng ra làm các commit khác nhau. Comment của mỗi commit này cần ghi ngắn gọn
  - [X] phần đã sửa đổi
  - [X] nội dung sửa đổi
- [X] Reducing code changes:
  - [X] Hạn chế thay đổi các phần không liên quan đến task của mình.
  - [X] Chỉ commit các phần code mình chủ định sửa, còn các phần còn lại dù có sai chính tả hay format thì cũng bỏ qua, không phải vì đơn giản mà tiện tay làm luôn.
- [X] Coding convention/coding format:
  - [X] Chỉ apply coding format cho các file/phần code mình thay đổi, không apply coding format cho toàn bộ source code để tránh các thay đổi ko cần thiết.
  - [X] Nếu phát hiện có quá nhiều lỗi coding format thì cần report lại để có 1 MR/commit riêng fix riêng cho phần này.
- [X] Typo/grammar mistakes:
  - [X] Đối với các phần liên quan đến UI / language / message hiển thị phía user cần kiểm tra lại sao cho khớp với Design/tài liệu miêu tả. 
  - [X] Nếu phát hiện có lỗi về mặt chính tả và ngữ pháp thì cần báo cáo lại để xác nhận và có thay đổi phù hợp trước khi commit.
  - [X] Đối với tên biến trong code thì hạn chế đặt tên dài hoặc sai ngữ nghĩa và cần mang tính đồng nhất. 
  - [X] Khi sửa lỗi này trong code cần cẩn thận và dùng tính năng “replace” thay vì copy&paste hoặc gõ thủ công dễ gây thiếu sót.
- [X] Run Dev/Run Build to Smoke Test locally:
  - [X] Chạy các command để self-test qua trên local các tính năng mình đã sửa đổi và có thể cả các tính năng có liên quan để đảm bảo chúng vẫn hoạt động bình thường như trước.
  - [X] Với các tính năng mới cần đảm bảo khi `run build` và `run dev` đều có kết quả sản phẩm như nhau.
  - [X] Đối với các trường hợp chưa có test case: 
    - [X] cần đảm bảo UI hiển thị giống như design
    - [X] tính năng hoạt động đúng như spec miêu tả
    - [X] không xuất hiện các bug dễ thấy trong quá trình thao tác các luồng thông thường
