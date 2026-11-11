---
name: gui-checklist-reviewer
description: Tự kiểm toán (Self-Audit) và phản biện GUI Checklist do AI tạo ra, phát hiện các khía cạnh giao diện (UI aspects) và trạng thái chuyển tiếp bị bỏ sót, bổ sung test cases và giải thích nguyên nhân gốc rễ tại sao AI bỏ sót.
---

# Skill 2: GUI Checklist Reviewer

## 1. Skill Name
`gui-checklist-reviewer` (GUI Checklist Reviewer & AI Critique Specialist)

## 2. Description
Skill đóng vai trò Senior QA Reviewer thực hiện kiểm toán độc lập đối với bản GUI Checklist khởi tạo ban đầu của AI, đối chiếu ngược lại với mã nguồn (`App.jsx`) và tiêu chuẩn WCAG/Heuristics để chỉ ra các điểm mù của AI (AI Blind Spots), bổ sung các test items còn thiếu và lập báo cáo phân tích nguyên nhân bỏ sót phục vụ **AI Audit Report**.

## 3. Objective
- Đánh giá mức độ bao phủ của checklist ban đầu trên cả 4 khía cạnh `IA-01`, `IA-02`, `IA-03`, `IA-04`.
- Phát hiện các trạng thái giao diện động hoặc biên dễ bị AI bỏ qua (Empty State, State Collision giữa Sửa và Xóa, Cross-Tab Unsaved State, DOM File Input `onChange` trap, Double-click rapid submit, Unbroken string overflow, WCAG contrast ratio).
- Bổ sung các `Additional (Human-Reviewed)` test items vào checklist và giải thích rõ nguyên nhân nhận thức khiến AI bỏ sót ở lượt đầu tiên.

## 4. Input
- **Bản GUI Checklist ban đầu (`AI-Generated Checklist`)**.
- **Ảnh chụp màn hình thực tế & Source Code (`frontend-admin/src/App.jsx`)**.

## 5. Processing Workflow
1. **Bước 1 – Phân tích độ phủ & Kiểm tra trùng lặp (Coverage & Redundancy Audit)**:
   - Thống kê số lượng test case theo từng màn hình và từng Interface Aspect; phát hiện các test case trùng ý tưởng.
2. **Bước 2 – Quét 7 nhóm điểm mù điển hình của AI (7-Point Blindspot Scan)**:
   - *Visual Anchoring Bias*: AI chỉ nhìn dữ liệu đang có trong ảnh mà quên trạng thái rỗng (`Empty State`).
   - *Linear Flow Assumption*: AI quên kiểm tra xung đột 2 hành động đồng thời (đang `Sửa` bản ghi A nhưng bấm `Xóa` bản ghi A dưới bảng).
   - *Screen-Isolated Analysis*: AI quên kiểm tra trạng thái khi chuyển tab qua lại lúc đang nhập dở form.
   - *DOM Event Quirk Blindness*: AI bỏ qua hành vi chọn lại cùng 1 file CSV hoặc bấm Cancel trong `<input type="file">`.
   - *Cross-Screen Orphan State*: AI quên kiểm tra `<select>` danh mục khi toàn bộ danh mục bị xóa.
   - *CSS Unbroken String Overflow*: Chuỗi dài viết liền không khoảng trắng làm vỡ bảng HTML.
   - *WCAG Contrast & ARIA Accessibility*: Tỷ lệ tương phản màu chữ trắng trên nền vàng (`bg-yellow-500 text-white`) của nút `Sửa`.
3. **Bước 3 – Sinh Test Cases bổ sung & Giải thích Root Cause**:
   - Tạo các test cases bổ sung (`TC-GUI-043` -> `TC-GUI-050`), gắn nhãn `Additional (Human-Reviewed)` và xuất đoạn văn **AI Critique (200–300 từ)**.

## 6. Output
- Danh sách **Additional Test Items** chuẩn 12 cột.
- Bảng **AI Critique Log** giải thích nguyên nhân AI bỏ sót từng trường hợp.
- Đoạn phân tích **AI Critique (200–300 từ)** sẵn sàng đưa vào báo cáo chính.

## 7. Usage Instructions
```text
@gui-checklist-reviewer Hãy rà soát bảng 42 test cases ban đầu của Member 5, đối chiếu với code frontend-admin/src/App.jsx để tìm các trạng thái giao diện và tiêu chuẩn trợ năng bị bỏ sót, bổ sung thêm test items và giải thích tại sao AI bỏ sót từng trường hợp.
```

## 8. Example
- **Input**: Bảng 42 test cases ban đầu (`TC-GUI-001`..`TC-GUI-042`) + ảnh màn hình `Quản lý Sản phẩm`.
- **Output trích mẫu**:
  - **Phát hiện bỏ sót**: `TC-GUI-044` – Xung đột trạng thái khi đang mở chế độ `Sửa` sản phẩm A trên Form nhưng lại bấm nút `Xóa` chính sản phẩm A đó ở bảng bên dưới.
  - **Lý do AI bỏ sót (Root Cause)**: *Linear Flow Assumption (Giả định luồng tuyến tính)* — AI sinh kịch bản theo từng bước đơn lẻ tuần tự (Tạo -> Sửa -> Xóa) nên bỏ sót kịch bản người dùng kích hoạt 2 thao tác đối nghịch cùng lúc trên giao diện Master-Detail.
