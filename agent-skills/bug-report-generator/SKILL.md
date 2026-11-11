---
name: bug-report-generator
description: Chuyển đổi các Test Case có trạng thái Failed từ GUI Checklist và Cross-Platform Test Matrix thành các tệp Bug Report chuẩn Markdown (tương thích thư mục bug-report/ của dự án EShop và GitHub Issues).
---

# Skill 5: Bug Report Generator

## 1. Skill Name
`bug-report-generator` (Standardized Bug Report & GitHub Issue Generator)

## 2. Description
Skill tự động chuẩn hóa các lỗi đã được xác nhận (`Failed` test cases kèm ghi chú và ảnh chụp màn hình thực tế) thành các bản báo cáo lỗi (`Bug Report`) theo đúng cấu trúc thư mục `eshop-sut-main/bug-report/#N.md` của dự án và định dạng tạo Issue trực tiếp trên GitHub.

## 3. Objective
- Đảm bảo 100% các lỗi báo cáo đều truy vết ngược (traceability) về đúng `Test Case ID` trong `GUI Checklist` hoặc `Cross-Platform Test Matrix` và đúng `Interface Aspect` (`IA-01`..`IA-04`).
- Phân loại chính xác bản chất lỗi: **GUI Defect** vs. **Usability Issue** vs. **Functional-UI State Defect**.
- Cung cấp đầy đủ các trường chuẩn: `Title`, `Found by Test Case`, `Interface Aspect`, `Bug Classification`, `Severity / Priority`, `Môi trường`, `Steps to reproduce`, `Actual result`, `Expected result`, `Root Cause (Code Reference)` và `Screenshot Evidence`.
- **Tuyệt đối không** tự bịa đặt lỗi không tồn tại trên giao diện/source code hoặc tự gán ảnh chụp màn hình giả.

## 4. Input
- **Danh sách các Test Cases có trạng thái `Failed`** từ `GUI Checklist` hoặc `Cross-Platform Test Matrix`.
- **Ảnh chụp màn hình bằng chứng (`Screenshot Evidence`)** và thông tin môi trường thực thi.
- **Đoạn mã nguồn liên quan trong `frontend-admin/src/App.jsx` hoặc `backend/server.js`** (để chỉ rõ dòng code gây lỗi nếu có).

## 5. Processing Workflow
1. **Bước 1 – Xác thực thông tin lỗi & Gom nhóm chống trùng lặp (Defect Deduplication)**:
   - Kiểm tra xem nhiều Test Case bị `Failed` có xuất phát từ cùng một nguyên nhân gốc trên giao diện hay không để gom nhóm hợp lý và liệt kê đầy đủ các `Test Case ID` liên quan.
2. **Bước 2 – Phân loại & Định mức độ nghiêm trọng (Classification & Severity Triage)**:
   - Phân loại lỗi (`GUI Defect` / `Usability Issue` / `Functional-UI State Defect`).
   - Đánh giá `Severity` (`Critical`, `Major`, `Moderate`, `Minor`) và `Priority` (`P1`, `P2`, `P3`) dựa trên mức độ ảnh hưởng tới trải nghiệm và khả năng thao tác của người dùng.
3. **Bước 3 – Khởi tạo nội dung Bug Report theo chuẩn `eshop-sut-main/bug-report/`**:
   - Sinh nội dung Markdown cho từng bug report (và lệnh `gh issue create` nếu người dùng muốn đẩy nhanh lên GitHub Issues).

## 6. Output
- Các tệp Markdown riêng lẻ (`bug-report/BUG-GUI-01.md`, `BUG-GUI-02.md`, ...) hoặc bảng tổng hợp `Bug_Report_Member5.md` sẵn sàng nộp bài và tạo GitHub Issues.

## 7. Usage Instructions
```text
@bug-report-generator Hãy tạo Bug Report chuẩn Markdown cho lỗi phát hiện tại TC-GUI-026 (Cột Giá trong bảng Quản lý Sản phẩm hiển thị liền 30000000 ₫ không có dấu phân cách hàng nghìn) trên môi trường Chrome 130 / Windows 11, ảnh bằng chứng TC-GUI-026_Failed.png.
```

## 8. Example
- **Input**: `TC-GUI-026` (`Failed`), Màn hình `Quản lý Sản phẩm`, ảnh `TC-GUI-026_Failed.png`.
- **Output trích mẫu**:
```markdown
# Title: [BUG][IA-01][Product Management] Cột Giá trong bảng danh sách sản phẩm không có dấu phân cách hàng nghìn gây khó đọc

## Found by Test Case
TC-GUI-026 (Liên kết Cross-Platform: CP-P1-12, CP-P2-12, CP-P3-12)

## Requirement / Interface Aspect liên quan
IA-01: General UI Standards (Typography & Number Formatting Consistency)

## Bug Classification
GUI Defect & Usability Issue

## Severity / Priority
Minor / P3

## Môi trường
- OS: Windows 11 / macOS Sonoma
- Browser: Google Chrome 130.0, Mozilla Firefox 132.0, Apple Safari 17.6 (1920x1080)

## Steps to reproduce
1. Đăng nhập vào hệ thống `EShop Admin` với tài khoản quản trị (`admin@eshop.com`).
2. Trên thanh Sidebar bên trái, click vào mục `Sản phẩm` để mở màn hình `Quản lý Sản phẩm`.
3. Quan sát cột `Giá` trong bảng danh sách sản phẩm ở cuối trang (`iPhone 15 Pro Max`, `Samsung Galaxy S24 Ultra`, `MacBook Pro M3`).

## Actual result
- Giá tiền hiển thị thành một dãy số viết liền không có dấu chấm/phẩy phân cách hàng nghìn (`30000000 ₫`, `28000000 ₫`, `45000000 ₫`), không nhất quán với định dạng `.toLocaleString()` đang dùng trên màn hình `Dashboard` và khiến người quản trị rất dễ đếm nhầm số chữ số 0.

## Expected result
- Giá tiền trong bảng sản phẩm phải được định dạng có dấu phân cách hàng nghìn rõ ràng (ví dụ: `30.000.000 ₫` hoặc `30,000,000 ₫`) đồng nhất với toàn hệ thống.

## Root Cause (Code Reference)
- Tại tệp `frontend-admin/src/App.jsx` (dòng 447), cột giá đang render trực tiếp biến thô `<td className="p-3">{p.price} ₫</td>` thay vì gọi `{Number(p.price).toLocaleString('vi-VN')} ₫`.

## Screenshot Evidence
- `screenshots/TC-GUI-026_Failed.png`
```
