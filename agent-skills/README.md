# Bộ AI Agent Skills Phục Vụ Kiểm Thử Phần Mềm

Thư mục này chứa các Agent Skills chuẩn hóa, có thể tái sử dụng cho các quy trình kiểm thử nâng cao bao gồm:
1. **Kiểm thử Giao diện & Trải nghiệm Người dùng (GUI & Usability Testing - HW03)**
2. **Kỹ thuật Kiểm thử Hiệu năng & Phân tích Log Apache JMeter (Performance Engineering - HW05)**

---

## Cấu trúc thư mục

```text
agent-skills/
├── README.md
├── SKILL_VALIDATION_REPORT.md                   # Báo cáo đánh giá và nghiệm thu toàn diện Skill
│
├── jmeter-performance-engineering/              # [MỚI - HW05] Agent Skill Kiểm thử Hiệu năng Tự động
│   ├── SKILL.md                                 # Đặc tả toàn diện quy trình 9 Module & Human-in-the-Loop
│   ├── references/                              # Tài liệu kỹ thuật chuyên đề
│   │   ├── jmeter_best_practices.md             # Hướng dẫn Non-GUI CLI, JVM tuning, listener pruning
│   │   ├── performance_metrics.md               # Ý nghĩa toán học của Percentiles, Little's Law, TPS, Connect Time
│   │   ├── test_strategy_guide.md               # Mô hình tải Load, Stress, Spike, Soak & fail-safe rules
│   │   └── log_analysis_guide.md                # Phân tích log JTL, phân loại tối ưu hóa, Two-tier p95 regression
│   ├── scripts/                                 # Bộ công cụ tự động hóa không phụ thuộc thư viện ngoài
│   │   ├── validate_jmx.py                      # Kiểm tra tính hợp lệ XML, ThreadGroup, CSV, Timers, Assertions
│   │   ├── analyze_jtl.py                       # Phân tích JTL thô, tính Mean/p50/p90/p95/p99/TPS, so sánh hồi quy
│   │   └── generate_report.py                   # Tự động xuất báo cáo Markdown kèm đánh giá SLA Quality Gates
│   └── assets/
│       └── report_template.md                   # Mẫu báo cáo hiệu năng Markdown tái sử dụng
│
├── gui-checklist-generator/                     # Skill sinh checklist GUI
│   ├── SKILL.md
│   └── templates/
│       └── checklist_schema.md
├── gui-checklist-reviewer/                      # Skill rà soát góc mù checklist GUI
│   ├── SKILL.md
│   └── references/
│       └── ai_blindspots_rubric.md
├── gui-testing-assistant/                       # Skill trợ lý kiểm thử GUI
│   ├── SKILL.md
│   └── references/
│       └── evidence_watermark_snippet.js
├── usability-evaluation-assistant/              # Skill đánh giá Usability SUS
│   ├── SKILL.md
│   └── references/
│       └── sus_scoring_rules.md
└── bug-report-generator/                        # Skill sinh báo cáo lỗi chuẩn GitHub Issues
    ├── SKILL.md
    └── templates/
        └── bug_report_template.md
```

---

## Nguyên tắc bảo toàn tính trung thực dữ liệu (Data Integrity Guardrails)
1. **Không tự tạo kết quả kiểm thử (`Actual Result`, `Status`)**: Chỉ cập nhật khi người kiểm thử cung cấp quan sát thực tế hoặc dữ liệu log thực nghiệm.
2. **Không tự tạo bằng chứng (`Screenshot Evidence`)**: Mọi bằng chứng phải do Tester chụp thực tế từ hệ thống kèm watermark định danh email sinh viên.
3. **Không tự bịa đặt số liệu hiệu năng**: Tuyệt đối không giả mạo số liệu throughput, latency, hay error rate; mọi chỉ số trong báo cáo kiểm thử hiệu năng phải được tính toán chính xác từ raw `.jtl` log.
4. **Cơ chế Human-in-the-Loop**: Bắt buộc xin xác nhận từ người dùng trước khi chạy tải lớn (Stress/Spike), trước khi can thiệp cơ sở dữ liệu hoặc ghi đè file kết quả.
