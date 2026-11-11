# Schema Chuẩn cho GUI Checklist (12 Cột bắt buộc)

| Cột | Tên Cột | Quy tắc điền |
| :--- | :--- | :--- |
| 1 | `Test Case ID` | Mã định danh duy nhất theo chuẩn `TC-GUI-XXX` (VD: `TC-GUI-001`). |
| 2 | `Screen` | Tên màn hình thuộc phạm vi kiểm thử. |
| 3 | `Interface Aspect` | Một trong 4 giá trị: `IA-01: General UI Standards`, `IA-02: Forms`, `IA-03: Navigation`, `IA-04: Feedback / State`. |
| 4 | `UI Component` | Tên phần tử giao diện cụ thể được kiểm tra. |
| 5 | `Test Objective` | Mục tiêu kiểm thử giao diện rõ ràng, bắt đầu bằng động từ *"Kiểm tra..."*. |
| 6 | `Preconditions` | Điều kiện tiên quyết về trạng thái màn hình trước khi thực hiện. |
| 7 | `Test Steps` | Các bước thao tác tuần tự được đánh số `1., 2., 3.`. |
| 8 | `Expected Result` | Phản hồi thị giác/giao diện kỳ vọng theo chuẩn UI/UX. |
| 9 | `Actual Result` | **Để trống khi tạo checklist** — chỉ điền sau khi chạy trên hệ thống thật. |
| 10 | `Status` | **Để trống khi tạo checklist** — chỉ nhận `Passed`, `Failed`, `Blocked` sau khi thực thi. |
| 11 | `Notes` | **Để trống khi tạo checklist** — ghi chú chi tiết cho các ca `Failed`. |
| 12 | `Screenshot Evidence` | **Để trống khi tạo checklist** — tên file ảnh chụp bằng chứng thực tế. |
