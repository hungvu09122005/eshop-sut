# Bộ 5 AI Agent Skills phục vụ Kiểm thử GUI & Usability (HW03 – Member 5)

Thư mục này chứa 5 Agent Skills chuẩn hóa, có thể tái sử dụng cho quy trình **GUI Testing**, **Usability Evaluation (ISO 9241-11 & SUS)** và **Cross-Platform Testing** trên hệ thống `EShop Admin`.

## Cấu trúc thư mục
```text
agent-skills/
├── README.md
├── gui-checklist-generator/
│   ├── SKILL.md
│   └── templates/
│       └── checklist_schema.md
├── gui-checklist-reviewer/
│   ├── SKILL.md
│   └── references/
│       └── ai_blindspots_rubric.md
├── gui-testing-assistant/
│   ├── SKILL.md
│   └── references/
│       └── evidence_watermark_snippet.js
├── usability-evaluation-assistant/
│   ├── SKILL.md
│   └── references/
│       └── sus_scoring_rules.md
└── bug-report-generator/
    ├── SKILL.md
    └── templates/
        └── bug_report_template.md
```

## Nguyên tắc bảo toàn tính trung thực dữ liệu (Data Integrity Guardrails)
1. **Không tự tạo kết quả kiểm thử (`Actual Result`, `Status`)**: Chỉ cập nhật khi người kiểm thử cung cấp quan sát thực tế hoặc ảnh chụp màn hình.
2. **Không tự tạo bằng chứng (`Screenshot Evidence`)**: Mọi bằng chứng phải do Tester chụp thực tế từ hệ thống kèm watermark định danh email sinh viên.
3. **Không tự tạo dữ liệu người tham gia (`Participants`, `SUS Scores`, `Observation Notes`)**: Nếu chưa có dữ liệu khảo sát thực tế, chỉ xuất biểu mẫu trống hoặc phân tích nhận thức chuyên môn (Cognitive Walkthrough / Heuristic Analysis).
