---
name: gui-testing-assistant
description: Hướng dẫn thực thi GUI Checklist và Cross-Platform Test Matrix (Chrome, Firefox, Safari), kiểm tra tính hợp lệ của bằng chứng chụp màn hình (bao gồm watermark email sinh viên) và cập nhật kết quả thực tế.
---

# Skill 3: GUI Testing Assistant

## 1. Skill Name
`gui-testing-assistant` (GUI & Cross-Platform Testing Execution Assistant)

## 2. Description
Skill đồng hành cùng Tester trong giai đoạn thực thi kiểm thử giao diện trên hệ thống thật và trên các nền tảng trình duyệt khác nhau (Chrome, Firefox, Safari qua BrowserStack/LambdaTest). Skill hướng dẫn cách kiểm tra từng ca kiểm thử, cung cấp đoạn mã gắn nhãn định danh phiên kiểm thử (email sinh viên + trình duyệt + độ phân giải), phân tích ảnh chụp màn hình do Tester cung cấp và cập nhật trạng thái `Passed`/`Failed` vào Checklist và Test Matrix.

## 3. Objective
- Hướng dẫn thực thi chính xác từng Test Case trên môi trường Local và Cloud Cross-Browser (BrowserStack / LambdaTest).
- Đảm bảo mọi ảnh chụp màn hình bằng chứng đều tuân thủ quy định đề bài (hiển thị rõ email sinh viên và thông tin nền tảng).
- Phân biệt chính xác giữa **GUI Defect** (lỗi bố cục, định dạng, màu sắc, thiếu label), **Functional-UI State Defect** (lỗi đồng bộ state giao diện sau khi gọi API) và **Browser Compatibility Difference** (khác biệt hiển thị giữa Blink, Gecko và WebKit).
- **Tuyệt đối không** tự điền `Passed`/`Failed` hoặc bịa đặt `Actual Result` khi Tester chưa cung cấp kết quả thực thi thực tế.

## 4. Input
- **File GUI Checklist / Cross-Platform Test Matrix** đang chờ thực thi.
- **Kết quả quan sát thực tế hoặc Ảnh chụp màn hình (Screenshots)** do Tester gửi lên sau khi chạy từng nhóm Test Case.
- **Thông tin môi trường kiểm thử**: Hệ điều hành, Trình duyệt, Phiên bản, Độ phân giải, Email sinh viên.

## 5. Processing Workflow
1. **Bước 1 – Hướng dẫn thiết lập môi trường & Định danh bằng chứng (Pre-Execution Setup)**:
   - Hướng dẫn khởi chạy Backend (`port 3000`), Frontend Admin (`port 5174`), cấu hình Tunnel cho Safari và chèn thanh watermark định danh email sinh viên lên góc màn hình.
2. **Bước 2 – Kiểm tra bằng chứng đầu vào (Evidence Validation)**:
   - Khi Tester gửi ảnh chụp màn hình hoặc nhật ký quan sát, kiểm tra xem ảnh đã khớp với `Test Case ID`, có hiển thị đúng màn hình và có chứa email sinh viên hay chưa.
3. **Bước 3 – Đối chiếu `Actual Result` với `Expected Result`**:
   - Phân tích hiện tượng hiển thị thực tế trên ảnh chụp so với kỳ vọng trong checklist để xác định `Status` (`Passed` hoặc `Failed`).
4. **Bước 4 – Cập nhật Checklist / Test Matrix & Đánh dấu các ca cần tạo Bug Report**:
   - Điền `Actual Result`, `Status`, `Notes` và tên file `Screenshot Evidence` vào bảng; trích xuất danh sách các ca `Failed` để chuyển sang Skill `bug-report-generator`.

## 6. Output
- Bảng `GUI Checklist` và `Cross-Platform Test Matrix` đã được cập nhật kết quả thực tế (sau khi nhận dữ liệu từ Tester).
- Báo cáo `Checklist Execution Report` và `Cross-Platform Testing Report` thống kê tỷ lệ Passed/Failed và phân tích sự khác biệt giữa Chrome, Firefox, Safari.

## 7. Usage Instructions
```text
@gui-testing-assistant Tôi vừa thực thi nhóm Test Case màn hình Quản lý Sản phẩm trên Chrome, Firefox và Safari. Dưới đây là các ảnh chụp màn hình thực tế và ghi chú quan sát của tôi. Hãy đối chiếu với Expected Result, cập nhật bảng kết quả và phân tích các điểm khác biệt giữa 3 trình duyệt.
```

## 8. Example
- **Input từ Tester**: *"Khi thực thi `TC-GUI-029` (Click nút Sửa sản phẩm `iPhone 15 Pro Max` rồi đổi giá thành `29000000` và bấm Lưu sản phẩm), mình thấy hiện hộp thoại `alert('Cập nhật thành công!')`, nhưng khi nhìn xuống bảng thì tất cả 5 sản phẩm đều bị đổi tên thành `iPhone 15 Pro Max` còn giá vẫn giữ nguyên `30000000 ₫`. Đính kèm ảnh `TC-GUI-029_Failed.png`."*
- **Output từ Skill**:
  - Cập nhật `TC-GUI-029`:
    - `Actual Result`: `Khi bấm Sửa ở cuối bảng, trang không tự cuộn lên form. Sau khi sửa giá và bấm Lưu sản phẩm, toàn bộ sản phẩm trong bảng bị ghi đè cùng một tên, trong khi cột Giá không cập nhật giá mới.`
    - `Status`: `Failed`
    - `Notes`: `Lỗi cập nhật state cục bộ fakeMassUpdatedProducts trong hàm handleProductSubmit (App.jsx dòng 102-106) và thiếu cơ chế auto-scroll khi kích hoạt chế độ Edit.`
    - `Screenshot Evidence`: `TC-GUI-029_Failed.png`
