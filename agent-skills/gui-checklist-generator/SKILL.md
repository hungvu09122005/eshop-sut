---
name: gui-checklist-generator
description: Thiết kế GUI Checklist chuẩn hóa (>40 test items) từ source code Frontend, ảnh chụp màn hình (screenshots) và phạm vi kiểm thử được phân công, bao phủ đầy đủ 4 Interface Aspects (IA-01, IA-02, IA-03, IA-04).
---

# Skill 1: GUI Checklist Generator

## 1. Skill Name
`gui-checklist-generator` (GUI Checklist Generator)

## 2. Description
Skill tự động phân tích giao diện thực tế (screenshots) kết hợp với cấu trúc JSX/CSS trong mã nguồn Frontend (`frontend-admin/src/App.jsx`, `index.css`) để sinh danh sách kiểm thử giao diện (GUI Checklist) có cấu trúc, phân bổ đều qua 4 khía cạnh giao diện (`IA-01` đến `IA-04`) mà không lấn sang kiểm thử nghiệp vụ Backend thuần túy.

## 3. Objective
- Tạo bộ GUI Checklist ban đầu có **trên 40 test items** bám sát 100% các thành phần UI có thật trên màn hình.
- Bao phủ đầy đủ 4 Interface Aspects:
  - `IA-01: General UI Standards` (Layout, Alignment, Typography, Colors, Contrast, Visual Consistency, Responsiveness).
  - `IA-02: Forms` (Labels, Placeholders, Input Types, Dropdowns, Textarea, Inline Validation Messages).
  - `IA-03: Navigation` (Sidebar Links, Active Tab Highlight, Keyboard Tab/Enter Flow, Auto-scroll).
  - `IA-04: Feedback / State` (Disabled/Enabled Buttons, Hover/Focus States, Edit Mode Transition, Confirmation Dialogs).
- Đảm bảo có cả kịch bản hợp lệ (Positive) và không hợp lệ (Negative), không trùng lặp, và **để trống hoàn toàn** các cột kết quả thực thi (`Actual Result`, `Status`, `Notes`, `Screenshot Evidence`).

## 4. Input
- **Phạm vi kiểm thử (Testing Scope)**: Danh sách màn hình/chức năng được phân công (VD: Member 5 – `Admin Dashboard`, `Category Management`, `Product Management`, `Product Import from CSV`).
- **Ảnh chụp màn hình thực tế (Screenshots)**: Ảnh chụp các màn hình đang chạy của hệ thống.
- **Source Code giao diện**: Tệp mã nguồn Frontend (`frontend-admin/src/App.jsx`, `index.css`, `tailwind.config.js`).

## 5. Processing Workflow
1. **Bước 1 – Trích xuất Inventory thành phần giao diện (UI Component Inventory)**:
   - Quét ảnh chụp màn hình và cây JSX trong code để lập danh sách tất cả các phần tử hiển thị: Containers, Metric Cards, Tables, Text Inputs, Number Inputs, Select Dropdowns, Textareas, File Inputs, Links và Action Buttons.
2. **Bước 2 – Ánh xạ vào 4 Interface Aspects (`IA-01` -> `IA-04`)**:
   - Gán từng UI Component vào đúng khía cạnh kiểm thử GUI (bố cục, biểu mẫu, điều hướng, trạng thái phản hồi).
3. **Bước 3 – Thiết kế kịch bản Positive & Negative trên GUI**:
   - Xây dựng các bước thao tác (`Test Steps`) và kỳ vọng hiển thị (`Expected Result`) dựa trên chuẩn UI/UX.
4. **Bước 4 – Kiểm tra ràng buộc toàn vẹn (Guardrail Verification)**:
   - Loại bỏ các test case trùng lặp hoặc kiểm thử sâu Database/API; giữ trống 4 cột thực thi (`Actual Result`, `Status`, `Notes`, `Screenshot Evidence`).

## 6. Output
- Bảng Markdown và tệp Excel (`.xlsx`) gồm tối thiểu 12 cột chuẩn:
  `Test Case ID | Screen | Interface Aspect | UI Component | Test Objective | Preconditions | Test Steps | Expected Result | Actual Result | Status | Notes | Screenshot Evidence`.

## 7. Usage Instructions
Gọi Skill bằng câu lệnh kèm ảnh chụp màn hình và file code giao diện:
```text
@gui-checklist-generator Hãy phân tích file frontend-admin/src/App.jsx và 3 ảnh chụp màn hình Dashboard, Quản lý Danh mục, Quản lý Sản phẩm để tạo GUI Checklist (>40 test items) cho phạm vi Member 5 theo 4 Interface Aspects (IA-01..IA-04). Không điền kết quả thực thi.
```

## 8. Example
- **Input**: Ảnh màn hình `Quản lý Sản phẩm` + đoạn code `<form onSubmit={handleProductSubmit}>` trong `App.jsx`.
- **Output trích mẫu**:
  - `Test Case ID`: `TC-GUI-020`
  - `Screen`: `Product Management`
  - `Interface Aspect`: `IA-02: Forms`
  - `UI Component`: `Form Field Labels (Tên sản phẩm, Giá tiền, URL Ảnh, Mô tả, Category Select)`
  - `Test Objective`: `Kiểm tra sự tồn tại của nhãn <label> cố định và ký hiệu đánh dấu trường bắt buộc (*) trên form Sản phẩm.`
  - `Preconditions`: `Đang ở màn hình Quản lý Sản phẩm.`
  - `Test Steps`: `1. Quan sát 5 trường nhập liệu trong khung Thêm sản phẩm mới khi chưa nhập và sau khi đã nhập dữ liệu. 2. Quan sát ô Dropdown chọn danh mục.`
  - `Expected Result`: `Mỗi trường nhập liệu có nhãn <label> cố định phía trên để khi người dùng đã nhập chữ hoặc đang ở chế độ Sửa vẫn phân biệt được từng trường.`
  - `Actual Result` / `Status` / `Notes` / `Screenshot Evidence`: *(Để trống)*
