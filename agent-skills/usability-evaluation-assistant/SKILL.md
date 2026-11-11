---
name: usability-evaluation-assistant
description: Thiết kế bộ tài liệu chuẩn bị đánh giá khả năng sử dụng (Task Scenario, Moderator Script, Observation Sheet, SUS Questionnaire 10 câu của John Brooke), tính điểm SUS chính xác và phân tích các vấn đề Usability theo chuẩn ISO 9241-11.
---

# Skill 4: Usability Evaluation Assistant

## 1. Skill Name
`usability-evaluation-assistant` (Usability Evaluation & SUS Analysis Assistant)

## 2. Description
Skill hỗ trợ trọn vẹn 3 giai đoạn của quy trình đánh giá khả năng sử dụng (Usability Evaluation): từ bước kiểm tra tính khả thi của luồng End-to-End trong mã nguồn, soạn thảo kịch bản nhiệm vụ nghiệp vụ không chứa từ khóa chỉ dẫn giao diện, thiết lập bảng quan sát và bộ 10 câu hỏi **System Usability Scale (SUS)** chuẩn John Brooke (1986), đến bước tính điểm SUS và phân loại các vấn đề Usability theo mức độ nghiêm trọng (`Critical`, `Major`, `Moderate`, `Minor`).

## 3. Objective
- Xác minh luồng nghiệp vụ End-to-End có thực sự hoạt động trên hệ thống trước khi chốt kịch bản.
- Xây dựng **Task Scenario** thuần mục tiêu nghiệp vụ (không chỉ dẫn bấm nút nào hay vào menu nào).
- Áp dụng chính xác 100% bộ 10 câu hỏi SUS thang Likert 5 mức và công thức tính điểm gốc trong tài liệu `SUS.pdf` của John Brooke.
- Bảo vệ tính trung thực học thuật: **Tuyệt đối không** tự bịa danh sách người tham gia, thời gian hoàn thành hay điểm SUS giả nếu chưa có dữ liệu khảo sát thật.

## 4. Input
- **Luồng nghiệp vụ dự kiến (Proposed End-to-End Flow)** và mã nguồn giao diện (`frontend-admin/src/App.jsx`).
- **Tài liệu chuẩn `SUS.pdf` (John Brooke, 1986)**.
- **Dữ liệu quan sát thực tế & Bảng điểm thô 10 câu SUS của người tham gia** *(hoặc thông báo giới hạn thực thi nếu chỉ thực hiện Cognitive Walkthrough)*.

## 5. Processing Workflow
1. **Bước 1 – Xác minh luồng trên Code & UI (Flow Feasibility Verification)**:
   - Kiểm tra từng điểm chuyển tiếp trong `App.jsx` và `server.js` để đảm bảo người dùng có thể đi từ điểm đầu tới điểm cuối của kịch bản.
2. **Bước 2 – Khởi tạo bộ công cụ Phase 1 (Plan & Prepare Kit)**:
   - Tạo `Usability Evaluation Objectives` (Effectiveness, Efficiency, Satisfaction theo ISO 9241-11), `Participant Roster Template` (ẩn danh/mask thông tin liên lạc), `Task Scenario`, `Moderator Script`, `Think Aloud Instructions`, `Observation Sheet`, `SUS Questionnaire (10 items)` và `Post-task Interview Questions`.
3. **Bước 3 – Tính điểm SUS tự động theo công thức gốc (khi có dữ liệu thật)**:
   - Câu lẻ (`1, 3, 5, 7, 9`): $	ext{Điểm quy đổi} = R_i - 1$ (từ 0 đến 4).
   - Câu chẵn (`2, 4, 6, 8, 10`): $	ext{Điểm quy đổi} = 5 - R_j$ (từ 0 đến 4).
   - $	ext{SUS Score} = (\sum 	ext{Điểm quy đổi}) 	imes 2.5$ (thang `0–100`).
4. **Bước 4 – Phân loại Usability Findings & Đề xuất cải tiến (Phase 3 Analysis)**:
   - Tổng hợp các điểm nghẽn giao diện, ánh xạ với 10 nguyên lý Heuristic của Nielsen và tiêu chuẩn ISO 9241-11, đánh giá mức độ nghiêm trọng và đề xuất giải pháp sửa đổi UI/UX cụ thể.

## 6. Output
- Bộ tài liệu `Task Scenario`, `Participant List`, `Observation Notes`, bảng tính `SUS Results (.xlsx)` và báo cáo hoàn chỉnh `Usability_Evaluation.md`.

## 7. Usage Instructions
```text
@usability-evaluation-assistant Hãy thiết kế bộ tài liệu Phase 1 (Task Scenario không chỉ dẫn từng bước, Observation Sheet, SUS Questionnaire 10 câu chuẩn John Brooke) và phân tích các vấn đề Usability trên luồng Admin Dashboard -> Tạo Category -> Tạo Product -> Sửa Product -> Quản lý Product.
```

## 8. Example
- **Input**: Kiểm tra bước `Nhiệm vụ 4: Chỉnh sửa thông tin sản phẩm` trên `frontend-admin/src/App.jsx`.
- **Output trích mẫu**:
  - `Issue ID`: `USAB-01`
  - `Vấn đề phát hiện`: Sau khi sửa sản phẩm và bấm `Lưu sản phẩm`, giao diện cập nhật mảng cục bộ `fakeMassUpdatedProducts` làm toàn bộ sản phẩm trong bảng bị đổi sang cùng một tên, trong khi giá tiền mới không hiển thị trên bảng.
  - `Nguyên lý vi phạm`: *Visibility of System Status* & *Consistency and Standards*.
  - `Mức độ nghiêm trọng`: `Critical`
  - `Đề xuất cải tiến`: Gọi `await fetchData()` sau khi `PUT /api/products/:id` thành công và thay `window.alert()` bằng thông báo Toast không chặn màn hình.
