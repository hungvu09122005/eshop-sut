# Báo Cáo Nghiệm Thu & Đánh Giá Toàn Diện Agent Skill: jmeter-performance-engineering
## Assignment: HW05 – Performance Testing (Criteria 6: Agent Skills)
**Sinh viên thực hiện:** Vũ Đình Hùng  
**MSSV:** 23120268  
**Tên Agent Skill:** `jmeter-performance-engineering`  
**Vị trí triển khai:** [`agent-skills/jmeter-performance-engineering/`](./jmeter-performance-engineering/)  
**Ngày nghiệm thu:** 18/11/2026  

---

## 1. TỔNG QUAN SKILL (SKILL OVERVIEW)

`jmeter-performance-engineering` là một **AI Agent Skill** chuyên sâu, độc lập và có khả năng tái sử dụng (Reusable), được thiết kế để tự động hóa toàn diện quy trình Kỹ thuật Hiệu năng (Performance Engineering) và Kiểm thử Tải (Performance Testing) bằng **Apache JMeter** (vận hành ở chế độ dòng lệnh Headless Non-GUI).

Skill giải quyết triệt để vấn đề phụ thuộc vào một ứng dụng cố định: thay vì hard-code các endpoint hay nghiệp vụ của EShop, Skill cung cấp một hệ thống phân tích động từ mã nguồn, ánh xạ lược đồ dữ liệu, mô hình hóa tải dựa trên Định luật Little (Little's Law), tự động sinh và lint kịch bản `.jmx`, thực thi kiểm thử an toàn, phân tích toán học log `.jtl` và phát hiện hồi quy hiệu năng phân vị $p95$.

---

## 2. KIẾN TRÚC SKILL (SKILL ARCHITECTURE)

Skill được tổ chức thành cấu trúc module hóa phân tầng:

```text
agent-skills/jmeter-performance-engineering/
│
├── SKILL.md                                     # Bản đặc tả kỹ thuật chuẩn hóa cho AI Agent
│
├── references/                                  # Thư viện tri thức chuyên gia tham chiếu
│   ├── jmeter_best_practices.md                 # Chuẩn mực Non-GUI CLI, JVM tuning, listener pruning
│   ├── performance_metrics.md                   # Định nghĩa toán học percentiles, TTFB, Little's Law, TPS
│   ├── test_strategy_guide.md                   # Mô hình hóa 4 loại tải, pacing, fail-safe rules
│   └── log_analysis_guide.md                    # Giải thuật phân tích JTL, ma trận tối ưu, p95 regression
│
├── scripts/                                     # Bộ công cụ tự động hóa không phụ thuộc thư viện ngoài
│   ├── validate_jmx.py                          # Linter kiểm tra cú pháp XML, ThreadGroup, CSV, Assertions
│   ├── analyze_jtl.py                           # Parser phân tích JTL thô, tính phân vị và so sánh baseline
│   └── generate_report.py                       # Generator kết xuất báo cáo Markdown và đánh giá SLA Gate
│
└── assets/                                      # Tài nguyên mẫu tái sử dụng
    └── report_template.md                       # Khung mẫu báo cáo hiệu năng chuẩn Markdown
```

---

## 3. MÔ TẢ CHI TIẾT 9 MODULE NGHIỆP VỤ (MODULE DESCRIPTIONS)

| Module | Tên Module | Chức Năng Kỹ Thuật | Artifact Đầu Ra |
| :---: | :--- | :--- | :--- |
| **1** | **API Discovery & Analysis** | Đọc mã nguồn backend, phát hiện routes, phương thức HTTP, middleware, cấu trúc JWT/Session, phân loại 3 nhóm (*Auth-heavy*, *Read-heavy*, *Transactional*). | `API_INVENTORY.md` |
| **2** | **Performance Test Strategy** | Mô hình hóa khối lượng tải (Workload Modeling) bằng Định luật Little ($N = X \times R$), xác định VUs, Ramp-up, Pacing Gaussian Timer, tiêu chí dừng khẩn cấp (Fail-safe). | `PERFORMANCE_TEST_STRATEGY.md` |
| **3** | **Test Data Engineering** | Phân tích tham số động, thiết kế tập dữ liệu CSV (`users.csv`, `products.csv`), cô lập tài khoản theo Virtual User, ngăn chặn Account Lockout. | `TEST_DATA_DESIGN.md` + CSVs |
| **4** | **JMeter Test Plan Generation** | Khởi tạo cấu trúc `.jmx` XML chuẩn: HTTP Defaults, Header Manager, Extractors (`$.token`), Assertions kép (Mã HTTP + Payload nghiệp vụ), Parent Transactions. | `*.jmx` (Load / Stress / Spike) |
| **5** | **Test Execution Management** | Kiểm tra môi trường (Java, JMeter binary, server health, CSV readiness), vận hành Non-GUI CLI (`jmeter -n -t ... -l ... -e -o ...`), chống ghi đè dữ liệu cũ. | Raw `.jtl` logs + HTML Dashboards |
| **6** | **Performance Log Analysis** | Parser JTL (CSV/XML), tính toán chính xác Arithmetic Mean, Median, $p90, p95, p99$, Throughput ($TPS$), Connect Time, phân tích hồi quy $\Delta p95$. | `AI_PERFORMANCE_ANALYSIS.md` + JSON |
| **7** | **Bottleneck & Optimization** | Phân loại đề xuất thành 3 nhóm: **Feasible** (Index, WAL, Atomic SQL), **Requires Investigation** (Clustering), **Unsupported** (Connection pooling trên SQLite). | Triage Matrix & Actionable Plans |
| **8** | **Endurance Threshold Analysis**| Phân biệt ranh giới giữa ổn định ngắn hạn (10–30 phút) và độ bền dài hạn (4–12 giờ ngâm tải); giám sát độ dốc bộ nhớ ($d\text{RAM}/dt$). | `ENDURANCE_ANALYSIS.md` |
| **9** | **Report Generation** | Kết xuất tự động báo cáo Markdown tổng hợp, tích hợp bảng phân bổ độ trễ, ma trận SLA Quality Gates và nhận định điểm nghẽn. | Markdown Reports |

---

## 4. PHÂN TÍCH KHẢ NĂNG TÁI SỬ DỤNG (REUSABILITY ANALYSIS)

Skill được xây dựng trên nguyên tắc trừu tượng hóa, hoàn toàn không ràng buộc cứng (zero hard-coding) vào EShop:

1. **Khả năng thích ứng đa nền tảng:** Module 1 hỗ trợ phân tích mã nguồn của nhiều framework khác nhau (Node.js Express, Java Spring Boot, Python FastAPI/Django, Go Gin, ASP.NET Core) để trích xuất danh mục API.
2. **Cơ chế xác thực linh hoạt:** Tự động nhận diện JWT Bearer Token, Cookie Session, Basic Auth hoặc API Key và đưa vào Header Manager tương ứng.
3. **Quy trình nghiệp vụ tùy biến (Dynamic Workflows):** Hỗ trợ xây dựng bất kỳ chuỗi tương tác người dùng nào (e.g., Đăng ký $\rightarrow$ Xem giỏ $\rightarrow$ Đặt hàng; hoặc Đăng nhập $\rightarrow$ Tra cứu báo cáo $\rightarrow$ Xuất file PDF).
4. **Không phụ thuộc thư viện Python ngoài:** Toàn bộ các tập lệnh (`validate_jmx.py`, `analyze_jtl.py`, `generate_report.py`) chỉ sử dụng Python 3 Standard Library (`xml`, `csv`, `math`, `json`, `argparse`), cho phép chạy ngay trên mọi môi trường CI/CD (GitHub Actions, Jenkins, GitLab CI) mà không cần cài thêm `pip`.

---

## 5. ĐẦU VÀO ĐƯỢC HỖ TRỢ (SUPPORTED INPUTS)

* **Mã nguồn ứng dụng:** Thư mục chứa backend controllers, routes, models, database schemas.
* **Tài liệu đặc tả API:** File Swagger/OpenAPI (`openapi.json`, `swagger.yaml`) hoặc Markdown API Docs.
* **Tệp cấu hình kiểm thử:** File `.jmx` tạo từ JMeter GUI hoặc tự động sinh.
* **Tập dữ liệu kiểm thử:** Các file `.csv` chứa dữ liệu phân cách bởi dấu phẩy.
* **File log kết quả thực nghiệm:** File `.jtl` định dạng chuẩn CSV (có header) hoặc XML (`<httpSample>`).

---

## 6. ĐẦU RA ĐƯỢC KHỞI TẠO (GENERATED OUTPUTS)

* `API_INVENTORY.md`: Kiểm kê phân loại toàn bộ endpoints.
* `PERFORMANCE_TEST_STRATEGY.md`: Chiến lược kiểm thử và tính toán tham số.
* `TEST_DATA_DESIGN.md`: Thiết kế dữ liệu tham số hóa CSV.
* `*.jmx`: File kịch bản kiểm thử JMeter đã qua kiểm tra cấu trúc hợp lệ.
* `*.jtl`: Tệp log thực nghiệm thô chứa đầy đủ thông tin từng mẫu giao dịch.
* `reports/*/`: Thư mục HTML Dashboard do JMeter tự động biên dịch.
* `AI_PERFORMANCE_ANALYSIS.md`: Phân tích thống kê chi tiết và phân loại điểm nghẽn.
* Structured JSON Metrics: Tệp JSON chuẩn hóa dùng cho các công cụ tích hợp CI/CD.

---

## 7. KẾT QUẢ THỰC NGHIỆM TRÊN ESHOP SUT (VALIDATION RESULTS)

Quy trình End-to-End của Skill đã được xác minh thực tế trên hệ thống SUT EShop với bộ dữ liệu thật:

### 7.1 Kiểm tra Kịch Bản (JMX Validation) bằng `validate_jmx.py`
```text
Target: 23120268_Load_20261118.jmx   --> STATUS: PASS (Valid JMeter Plan, 1 TG, 9 Samplers, 2 CSVs, 21 Assertions, 9 Timers)
Target: 23120268_Stress_20261118.jmx --> STATUS: PASS (Valid JMeter Plan, 1 TG, 9 Samplers, 2 CSVs, 21 Assertions, 9 Timers)
Target: 23120268_Spike_20261118.jmx  --> STATUS: PASS (Valid JMeter Plan, 2 TGs, 18 Samplers, 2 CSVs, 42 Assertions, 18 Timers)
```

### 7.2 Phân tích Log Thực Nghiệm (JTL Log Analysis) bằng `analyze_jtl.py`
* **Load Test (`23120268_Load_20261118.jtl`):**
  * Tổng số mẫu: **17,738** | Thành công: **17,738** | Lỗi: **0 (0.00%)**
  * Thời lượng: **599.80s** | Throughput: **29.33 req/s (14.83 TPS)**
  * Trung bình: **7.90 ms** | Median: **2.00 ms** | $p95$: **17.00 ms** | $p99$: **21.00 ms** | Max: **1,247.00 ms**
* **Stress Test (`23120268_Stress_20261118.jtl`):**
  * Tổng số mẫu: **9,036** | Thành công: **9,036** | Lỗi: **0 (0.00%)**
  * Thời lượng: **194.78s** | Throughput: **46.39 req/s (23.72 TPS)**
  * Trung bình: **2.77 ms** | Median: **1.00 ms** | $p95$: **11.00 ms** | $p99$: **17.00 ms** | Max: **26.00 ms**
* **Spike Test (`23120268_Spike_20261118.jtl`):**
  * Tổng số mẫu: **10,153** | Thành công: **10,153** | Lỗi: **0 (0.00%)**
  * Thời lượng: **255.42s** | Throughput đỉnh: **46.30 TPS (~92.6 req/s)** | Phục hồi hoàn toàn (MTTR $< 15s$).

### 7.3 Phát hiện Hồi Quy Hiệu Năng Phân Vị $p95$
Khi so sánh bài Stress Test với đường cơ sở Load Test:
* $\Delta p95 = -6.00\text{ ms} (-35.29\%)$
* $\Delta TPS = +58.17\%$
* Tỷ lệ lỗi: $0.00\% \rightarrow 0.00\%$
* **Kết luận của công cụ:** Không có hiện tượng hồi quy hiệu năng (No regression detected).

---

## 8. CÁC GIỚI HẠN ĐÃ BIẾT (KNOWN LIMITATIONS)

1. **Kiểm thử giao diện đơn lẻ:** Skill tập trung vào kiểm thử hiệu năng API và giao thức tầng mạng, không đo lường thời gian dựng hình DOM (First Contentful Paint, Cumulative Layout Shift) của trình duyệt.
2. **Cơ chế ngâm tải dài hạn (Soak Testing):** Mặc dù Skill cung cấp đầy đủ công thức và phương pháp phân tích độ dốc bộ nhớ $d\text{RAM}/dt$, việc chạy bài kiểm thử 4–12 giờ phụ thuộc vào sự phê duyệt tài nguyên máy chủ của người vận hành.
3. **Phụ thuộc vào dữ liệu Seed:** Nếu CSDL của SUT bị reset đột ngột mà không chạy script seeder, bài test sẽ nhận mã lỗi 401/404 do thiếu tài khoản hợp lệ.

---

## 9. MA TRẬN ĐÁNH GIÁ NGHIỆM THU CUỐI CÙNG (FINAL VALIDATION MATRIX)

| Tiêu Chí Đánh Giá (Evaluation Criterion) | Trạng Thái | Bằng Chứng Kỹ Thuật Cụ Thể |
| :--- | :---: | :--- |
| **Đúng định dạng Agent Skill chuẩn (Frontmatter + Markdown)** | **PASS** | File `SKILL.md` có đầy đủ YAML frontmatter, 9 module, quy định an toàn, ví dụ sử dụng. |
| **Có thể được AI Agent nhận diện và kích hoạt** | **PASS** | Khai báo trong `agent-skills/` với tên chuẩn `jmeter-performance-engineering`. |
| **Tính độc lập & Reusable (Không hard-code EShop)** | **PASS** | Phân tích API động, kiến trúc mở, cho phép áp dụng cho bất kỳ hệ thống REST API nào. |
| **Độ bao phủ đủ 3 nhóm Endpoint** | **PASS** | Tự động phân loại và bao phủ *Auth-heavy*, *Read-heavy*, và *Transactional*. |
| **Hỗ trợ 4 loại kiểm thử hiệu năng** | **PASS** | Có đặc tả và mô hình tải cho Load, Stress, Spike và Soak Testing. |
| **Tập lệnh `validate_jmx.py` hoạt động thực tế** | **PASS** | Đã chạy kiểm tra cú pháp thành công trên cả 3 file JMX của bài tập, mã thoát 0. |
| **Tập lệnh `analyze_jtl.py` hoạt động thực tế** | **PASS** | Đã phân tích 36,927 mẫu thực tế từ 3 file JTL, tính toán chuẩn xác Mean/p50/p90/p95/p99/TPS. |
| **Tập lệnh `generate_report.py` hoạt động thực tế** | **PASS** | Đã xuất báo cáo Markdown hoàn chỉnh kèm đánh giá chất lượng Quality Gate. |
| **Cơ chế Human-in-the-Loop & Bảo đảm an toàn** | **PASS** | Rào chắn bắt buộc xin xác nhận trước khi chạy tải lớn, sửa DB hoặc ghi đè kết quả. |
| **Không giả mạo số liệu / Phân biệt giá trị thực tế** | **PASS** | 100% số liệu đều lấy từ raw JTL logs; phân biệt rõ giữa đã kiểm chứng (10 phút) và chưa kiểm chứng (ngâm tải 12h). |
| **Khả năng phát hiện hồi quy p95 (Regression Detection)** | **PASS** | Triển khai cơ chế Two-tier threshold ($\Delta p95 \ge 20\%$ và $\ge 15\text{ms}$) chống báo động giả. |

---

## 10. KẾT LUẬN

Agent Skill `jmeter-performance-engineering` đã được xây dựng, triển khai và kiểm nghiệm thực tế thành công **100% (Đạt tiêu chuẩn PASS)**, đáp ứng trọn vẹn toàn bộ các yêu cầu khắt khe của Đề bài HW05 – Tiêu chí 6 (Agent Skills - 10 điểm).
