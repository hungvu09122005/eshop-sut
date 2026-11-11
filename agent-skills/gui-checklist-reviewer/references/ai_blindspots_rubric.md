# Danh mục 7 Điểm mù của AI khi Thiết kế GUI Checklist (Rubric Kiểm toán)

1. **Visual Anchoring Bias (Thiên kiến neo vào ảnh tĩnh)**: Chỉ kiểm tra trạng thái có dữ liệu giống trong ảnh chụp, bỏ sót trạng thái bảng rỗng (`Empty State`).
2. **Linear Flow Assumption (Giả định luồng tuyến tính)**: Không kiểm tra tương tác chéo gây xung đột trạng thái trên cùng một màn hình (ví dụ: vừa bật `Edit` vừa bấm `Delete` cùng một phần tử).
3. **Screen-Isolated Analysis (Phân tích cô lập màn hình)**: Bỏ sót việc kiểm tra vòng đời state khi chuyển đổi qua lại giữa các tab trên Sidebar.
4. **DOM Event Quirk Blindness**: Bỏ qua đặc thù sự kiện `onChange` của `<input type="file">` khi chọn lại cùng một tệp tin.
5. **Happy-Path Cross-Screen Dependency**: Chỉ kiểm tra chiều thêm mới dữ liệu liên màn hình mà quên chiều xóa sạch dữ liệu nguồn của `<select>`.
6. **CSS Unbroken String Rendering**: Không phân biệt chuỗi văn bản dài có khoảng trắng và chuỗi ký tự liền mạch không khoảng trắng (`word-break`).
7. **Visual-First over WCAG Standards**: Đánh giá màu sắc bằng cảm quan thị giác mà không đo tỷ lệ tương phản chuẩn WCAG AA ($\ge 4.5:1$) và các thuộc tính `alt`, `aria-label`.
