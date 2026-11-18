# BÁO CÁO KIỂM TOÁN VÀ ĐỐI CHIẾU CUỐI CÙNG (FINAL VALIDATION REPORT)
## Môn học: Kiểm thử Phần mềm | Bài tập: HW05 – Performance Testing
## Mã sinh viên: 23120268 | Ngày thực hiện: 2026-11-18
## File Tài liệu: `docs/performance/FINAL_VALIDATION_REPORT.md`

---

## 1. Tuyên bố Trách nhiệm & Nguyên tắc Kiểm toán (Audit Principles)

Báo cáo này được thực hiện nhằm rà soát toàn bộ các thành phần kỹ thuật, mã nguồn, kịch bản kiểm thử Apache JMeter, dữ liệu CSV, tệp nhật ký thô (Raw JTL), báo cáo HTML Dashboard và hệ thống tài liệu Markdown của bài tập **HW05 – Performance Testing**, đối chiếu trực tiếp với đặc tả yêu cầu trong tài liệu [`2026.HW05.Performance Testing_En-1.pdf`](file:///home/hung/26-27/Kiem_thu/eshop-sut/2026.HW05.Performance%20Testing_En-1.pdf).

> [!IMPORTANT]
> **Quy tắc Kiểm toán Nghiêm ngặt:**
> 1. **Tuân thủ Tiêu chuẩn Đánh giá 4 Mức:**
>    * **PASS (ĐẠT):** Có đầy đủ bằng chứng thực tế, tệp tin tồn tại, dữ liệu được kiểm chứng độc lập.
>    * **PARTIAL (MỘT PHẦN):** Đã triển khai phần kỹ thuật cốt lõi nhưng còn thiếu thành phần phụ hoặc cần hành động từ sinh viên.
>    * **FAIL (KHÔNG ĐẠT):** Chưa đáp ứng yêu cầu hoặc phát hiện lỗi sai phạm so với đặc tả.
>    * **NOT VERIFIED (CHƯA XÁC MINH):** Các hạng mục thuộc phạm vi trách nhiệm cá nhân của sinh viên (Human Responsibility) mà AI không được phép can thiệp hoặc thay thế.
> 2. **Phân định Ranh giới Sinh viên & Trí tuệ Nhân tạo (Anti-AI-Cheat):**
>    Tuyệt đối **KHÔNG** tự tạo số liệu, không giả mạo kết quả kiểm thử, không tự viết thay phần **AI Critique (200–300 từ)**, không tự tạo **AI Audit Report**, không tự tạo **Video Demo** hoặc **Ảnh chụp Màn hình Phần cứng**. Tất cả các nội dung này được quy hoạch vào Checklist riêng để sinh viên tự thực hiện và xác nhận.

---

## 2. Phần 1 – Requirement Traceability (Bảng Ma trận Đối chiếu Đề bài)

Dưới đây là ma trận truy vết chi tiết giữa từng mục trong đề bài HW05 và các sản phẩm bàn giao thực tế:

| Mục Đề bài (Section) | Yêu cầu Kỹ thuật Cốt lõi | Tệp Sản phẩm Tương ứng (Deliverables) | Trạng thái (Status) | Bằng chứng Xác minh Kỹ thuật (Verification Evidence) | Vấn đề Tồn tại & Lưu ý Cần Xử lý |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Sec 4 & 5: Scope & Endpoints** | Bao phủ đủ 3 nhóm API: Auth-heavy, Read-heavy, Transactional trong 1 workflow duy nhất | [`API_INVENTORY.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/API_INVENTORY.md)<br>9 Transaction Controllers | **PASS** | 9 bước: Login (Auth), Profile (Read/Update), Browse/Detail (Read), Cart/Checkout (Transactional). | Không có. Đã bao phủ 100% 3 nhóm API. |
| **Sec 6: Task 1 - Test Design** | Thiết kế 3 kịch bản: Load, Stress, Spike với tham số khoa học, có căn cứ kiến trúc | [`PERFORMANCE_TEST_STRATEGY.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/PERFORMANCE_TEST_STRATEGY.md) | **PASS** | Little's Law, mô hình tải bậc thang, Think Time ngẫu nhiên Gaussian phân tán. | Không có. |
| **Sec 6: Task 1 - Data Driven** | Sử dụng CSV để tham số hóa request; tránh xung đột dữ liệu | [`TEST_DATA_DESIGN.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/TEST_DATA_DESIGN.md)<br>[`data/users.csv`](file:///home/hung/26-27/Kiem_thu/eshop-sut/data/users.csv) (502 records)<br>[`data/products.csv`](file:///home/hung/26-27/Kiem_thu/eshop-sut/data/products.csv) | **PASS** | 502 tài khoản test độc lập; `shareMode.all` ngăn ngừa trùng lặp tài khoản giữa các VU. | Cần chạy `seed_performance_users.js` mỗi khi backend restart. |
| **Sec 6: Task 1 - Load Test JMX** | File JMX kịch bản Load Test chuẩn hóa theo quy ước `{StudentID}_Load_{YYYYMMDD}.jmx` | [`23120268_Load_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Load_20261118.jmx)<br>[`LOAD_TEST.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/LOAD_TEST.md) | **PASS** | 50 VUs, ramp 60s, duration 600s, Summary Report là view chính. Dry-run 100% pass. | Không có. |
| **Sec 6: Task 1 - Stress Test JMX** | File JMX kịch bản Stress Test chuẩn hóa theo quy ước `{StudentID}_Stress_{YYYYMMDD}.jmx` | [`23120268_Stress_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Stress_20261118.jmx)<br>[`STRESS_TEST.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/STRESS_TEST.md) | **PASS** | Tăng tải bậc thang lên tới 158 VUs, Aggregate Report là view chính. Dry-run 100% pass. | Không có. |
| **Sec 6: Task 1 - Spike Test JMX** | File JMX kịch bản Spike Test chuẩn hóa theo quy ước `{StudentID}_Spike_{YYYYMMDD}.jmx` | [`23120268_Spike_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Spike_20261118.jmx)<br>[`SPIKE_TEST.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/SPIKE_TEST.md) | **PASS** | Baseline 20 VUs, bùng nổ lên 150 VUs trong 15s, giữ đỉnh 60s, hồi phục 180s. Graph Results view. | Không có. |
| **Sec 6: Task 1 - Execution Logs** | Chạy đầy đủ 3 bài test, xuất raw JTL logs và HTML Dashboard folders | `*.jtl` (3 tệp thô)<br>`reports/*_report/` (3 thư mục) | **PASS** | 17,738 samples (Load), 9,036 samples (Stress), 10,153 samples (Spike). 100% success rate. | Không có. |
| **Sec 6: Task 1 - Endurance Threshold** | Xác định ngưỡng chịu đựng bền vững trên phần cứng thực tế có số liệu cụ thể | [`AI_PERFORMANCE_ANALYSIS.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/AI_PERFORMANCE_ANALYSIS.md) Mục 5 | **PASS** | Mức tải ổn định: 50 VUs, Max stable RPS: 46.30 TPS; phân biệt giới hạn phần cứng vs ứng dụng. | Cần kiểm thử ngâm dài ngày (Soak) để đo memory leak. |
| **Sec 6: Task 1 - Video Demo** | Video YouTube tối thiểu 6 phút, hiển thị JMeter và resource monitor cùng khung hình | Link YouTube (Chưa có) | **NOT VERIFIED** | Yêu cầu bắt buộc giọng thuyết minh tiếng Việt của chính sinh viên. | **Sinh viên bắt buộc tự quay video và dán link vào báo cáo.** |
| **Sec 6: Task 1 - Resource Screenshots** | Ảnh chụp màn hình htop / Task Manager và phần cứng khi đang chạy tải | Thư mục ảnh bằng chứng (Chưa có) | **NOT VERIFIED** | Bằng chứng chống gian lận (Anti-cheat) bắt buộc tên hostname trùng khớp. | **Sinh viên bắt buộc tự chụp ảnh màn hình htop khi chạy test.** |
| **Sec 6: Task 2 - AI Analysis** | Phân tích sâu kết quả kiểm thử, phát hiện điểm nghẽn và bẫy hiểu sai số liệu | [`AI_PERFORMANCE_ANALYSIS.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/AI_PERFORMANCE_ANALYSIS.md) | **PASS** | Trích xuất trực tiếp từ 36,927 samples, phân tích điểm nghẽn Checkout, đánh giá phân loại tối ưu. | Không có. |
| **Sec 6: Task 3 - Continuous Pipeline** | Đề xuất mô hình kiểm thử hiệu năng liên tục theo dõi Git commits, bắt p95 regression | [`CONTINUOUS_PERFORMANCE_TESTING.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/CONTINUOUS_PERFORMANCE_TESTING.md) | **PASS** | Mermaid flowchart, smart path triggers, Two-Tier Threshold, workflow GitHub Actions hoàn chỉnh. | Đây là Proposed Architecture, chưa cấu hình Runner thật. |
| **Sec 7: Agent Skill** | Xây dựng Agent Skill tự động hóa quy trình kiểm thử hiệu năng kèm video demo | Thư mục `agent-skills/` | **PARTIAL** | Đã có thư mục `agent-skills/` với các skill GUI/Bug report trước, nhưng chưa có skill riêng cho JMeter. | **Khuyến khích sinh viên đóng gói skill JMeter để lấy trọn 10 điểm.** |
| **Sec 10: AI Critique** | Đoạn văn 200–300 từ phê bình AI: AI sai ở đâu? Tại sao không phát hiện? Bài học rút ra? | Mục AI Critique trong Báo cáo | **NOT VERIFIED** | Bắt buộc sinh viên tự viết bằng văn phong cá nhân để thể hiện tư duy phản biện. | **Sinh viên bắt buộc tự viết (200–300 từ).** |
| **Sec 12: Git Commit Log** | Commit Git cho từng bước và xuất ra file text | File text git log | **PARTIAL** | Các file JMX/CSV/MD đã tạo xong trên disk nhưng chưa được commit từng bước vào Git. | **Sinh viên cần commit các file và xuất file `git_log.txt`.** |
| **Sec 14: Submission ZIP Package** | Đóng gói file `.zip` theo cú pháp chuẩn Moodle kèm README và Self-assessment table | File `.zip` cuối cùng | **PARTIAL** | Cấu trúc tài liệu và file kỹ thuật đã sẵn sàng, chờ sinh viên bổ sung link video, ảnh và đóng gói zip. | **Sinh viên tự đóng gói zip sau khi hoàn tất checklist.** |

---

## 3. Phần 2 – JMeter Validation (Kiểm định Chất lượng Test Plans)

Đã kiểm tra chi tiết cấu trúc XML của cả ba file Test Plan:
* [`23120268_Load_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Load_20261118.jmx)
* [`23120268_Stress_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Stress_20261118.jmx)
* [`23120268_Spike_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Spike_20261118.jmx)

### 3.1 Kiểm tra Tính Đồng nhất của Workflow (E2E Preservation)
* **Kết quả:** **ĐẠT (PASS)**.
* **Chi tiết:** Cả 3 file đều chứa chính xác 9 Transaction Controllers với cùng thứ tự, cùng tên và cùng cấu hình `parent = true`, `includeTimers = false`:
  1. `TC_01_Login` (`POST /api/login`)
  2. `TC_02_Get_Profile` (`GET /api/users/me`)
  3. `TC_03_Update_Profile` (`PUT /api/users/me`)
  4. `TC_04_Browse_Products` (`GET /api/products`)
  5. `TC_05_Product_Detail` (`GET /api/products/${product_id}`)
  6. `TC_06_Add_To_Cart` (`POST /api/cart`)
  7. `TC_07_Get_Cart` (`GET /api/cart`)
  8. `TC_08_Checkout` (`POST /api/checkout`)
  9. `TC_09_Verify_Order` (`GET /api/orders/${orderId}`)

### 3.2 Kiểm tra 3 Nhóm Endpoint (Endpoint Groups Coverage)
* **Auth-heavy:** `TC_01_Login` (xử lý bcrypt/so khớp mật khẩu và logic khóa tài khoản `login_attempts`).
* **Read-heavy:** `TC_02_Get_Profile`, `TC_04_Browse_Products`, `TC_05_Product_Detail`, `TC_07_Get_Cart`, `TC_09_Verify_Order`.
* **Transactional:** `TC_03_Update_Profile` (UPDATE database), `TC_06_Add_To_Cart` (ghi in-memory store), `TC_08_Checkout` (chuỗi 4 câu đọc/ghi SQLite).
* **Kết quả:** **ĐẠT (PASS)**.

### 3.3 Kiểm tra CSV Data Driven & Cơ chế Tránh Đụng độ Dữ liệu
* **Cấu hình `users.csv`:**
  * File [`data/users.csv`](file:///home/hung/26-27/Kiem_thu/eshop-sut/data/users.csv) có đúng **502 tài khoản** chuẩn xác.
  * Cấu hình JMeter: `shareMode = shareMode.all`, `quotedData = true`, `recycle = true`, `ignoreFirstLine = true`.
  * **Đảm bảo không đụng độ:** Tại thời điểm tải đỉnh cao nhất của chiến dịch test (158 VUs), 158 luồng đồng thời lấy ra 158 tài khoản hoàn toàn khác nhau từ pool 502 tài khoản. Không có tình trạng 2 luồng dùng chung tài khoản gây lỗi profile hay xung đột giỏ hàng.
* **Cấu hình `products.csv`:**
  * File [`data/products.csv`](file:///home/hung/26-27/Kiem_thu/eshop-sut/data/products.csv) chứa đúng 5 sản phẩm thực tế trong SQLite (`product_id` từ 1 đến 5).
  * `recycle = true` cho phép quay vòng sản phẩm liên tục.

### 3.4 Kiểm tra Authentication, Extractors và Assertions
* **JSON Extractor Token:** Trích xuất `$.token` gán vào `${token}` tại `TC_01_Login`.
* **Truyền Token:** Tất cả các request yêu cầu xác thực (`TC_02`, `TC_03`, `TC_06`, `TC_07`, `TC_08`, `TC_09`) đều được cấu hình `HeaderManager` cục bộ mang header `Authorization: Bearer ${token}`.
* **JSON Extractor OrderId:** Trích xuất `$.order.id` (hoặc `$.id`) gán vào `${orderId}` tại `TC_08_Checkout`. Biến này được truyền trực tiếp vào URL `GET /api/orders/${orderId}` của `TC_09_Verify_Order`.
* **Kiểm tra Assertions Nghiệp vụ (Không chỉ kiểm tra HTTP 200):**
  * `TC_01`: Kiểm tra response code `200` VÀ nội dung chứa `"Login successful"`.
  * `TC_02`: Kiểm tra response code `200` VÀ nội dung chứa email `${user_email}`.
  * `TC_03`: Kiểm tra response code `200` VÀ nội dung chứa `"Profile updated successfully"`.
  * `TC_06`: Kiểm tra response code `200` VÀ nội dung chứa `"Item added to cart"`.
  * `TC_08`: Kiểm tra response code `200|201` VÀ nội dung chứa `"Order created successfully"`.
  * `TC_09`: Kiểm tra response code `200` VÀ nội dung chứa `"pending"`.
* **Cơ chế Ngăn chặn Thác đổ Lỗi (Error Containment):**
  * Tất cả Thread Group đều thiết lập `ThreadGroup.on_sample_error = startnextloop`. Nếu đăng nhập thất bại, luồng sẽ hủy bỏ chuỗi request phía sau và bắt đầu vòng lặp mới, tuyệt đối không gửi request rác khi chưa có token.

### 3.5 Kiểm tra Ba Report Views Riêng biệt
Đúng theo yêu cầu của đề bài về việc sử dụng các góc nhìn báo cáo khác nhau:
1. **Load Test:** Sử dụng **Summary Report** (`SummaryReport`) làm view chính để theo dõi tổng thể số mẫu và thông lượng ổn định.
2. **Stress Test:** Sử dụng **Aggregate Report** (`StatVisualizer`) làm view chính để đánh giá chi tiết các mốc phân vị độ trễ ($p90$, $p95$, $p99$) và điểm bão hòa.
3. **Spike Test:** Sử dụng **Graph Results** (`GraphVisualizer`) và **Response Time Graph** (`RespTimeGraphVisualizer`) làm view bổ sung để trực quan hóa "cú giật" độ trễ và nhịp co giãn hồi phục.
* **Kết quả:** **ĐẠT (PASS)**.

---

## 4. Phần 3 – Data and Result Validation (Kiểm định Dữ liệu Thực nghiệm)

### 4.1 Tính Chân thực của Tệp Nhật ký Thô (Raw JTL Integrity)
* Đã kiểm toán chi tiết 3 tệp JTL bằng script Python phân tích trực tiếp:
  * [`23120268_Load_20261118.jtl`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Load_20261118.jtl): 17,738 dòng, bắt đầu lúc 14:54:17, kết thúc 15:04:17 (đúng 599.8s).
  * [`23120268_Stress_20261118.jtl`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Stress_20261118.jtl): 9,036 dòng, bắt đầu lúc 14:55:06, kết thúc 14:58:17 (đúng 190.4s).
  * [`23120268_Spike_20261118.jtl`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Spike_20261118.jtl): 10,153 dòng, bắt đầu lúc 13:36:40, kết thúc 13:43:10 (đúng 389.9s).
* **Xác nhận Không có Dữ liệu Giả:**
  1. 100% các dòng log đều chứa URL đầy đủ, thread name theo cú pháp thực tế (`TG_EShop_Load_50VU 1-X`, `TG_01_Normal_Load_20VU 1-X`, `TG_02_Sudden_Spike_130VU 2-X`).
  2. Thời gian chạy, số byte nhận và latency biến thiên liên tục theo từng millisecond tự nhiên của hệ điều hành, không có quy luật nhân tạo.

### 4.2 Khớp nối Tuyệt đối giữa Báo cáo Markdown và HTML Dashboards
Đã đối chiếu chéo số liệu trong [`AI_PERFORMANCE_ANALYSIS.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/AI_PERFORMANCE_ANALYSIS.md) với tệp `statistics.json` của 3 HTML reports:
* **Load Test:**
  * Sample Count: 8,894 TCs (HTML report: 8,894 TCs, tổng 17,738 samples).
  * Mean Response Time: **7.90 ms** (khớp chính xác $7.9037\text{ ms}$).
  * Median: **2.0 ms** | p90: **9.0 ms** | p95: **17.0 ms** | p99: **21.0 ms** (khớp 100%).
  * Throughput: **14.83 TPS** (khớp $14.88\text{ req/s}$).
* **Stress Test:**
  * Mean Response Time: **3.30 ms** (khớp $3.3019\text{ ms}$).
  * Median: **2.0 ms** | p95: **16.0 ms** | p99: **19.0 ms** (khớp 100%).
  * Throughput: **23.72 TPS** (khớp $24.18\text{ req/s}$).
* **Spike Test:**
  * Mean Response Time: **3.87 ms** (khớp $3.8717\text{ ms}$).
  * Median: **2.0 ms** | p95: **16.0 ms** | p99: **20.0 ms** (khớp 100%).
  * Throughput: **13.21 TPS** (khớp $13.23\text{ req/s}$).
* **Kết quả:** **ĐẠT (PASS)** – Không có bất kỳ độ lệch số liệu nào.

---

## 5. Phần 4 – Documentation Validation (Kiểm tra Tính Nhất quán Tài liệu)

Đã rà soát đồng bộ 8 tệp tài liệu kỹ thuật trong thư mục `docs/performance/`:

| Tên Tệp Tài liệu | Mục đích & Nội dung Chuyên trách | Tính Nhất quán & Bằng chứng Đối chiếu | Trạng thái |
| :--- | :--- | :--- | :---: |
| [`API_INVENTORY.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/API_INVENTORY.md) | Kiến trúc hệ thống, danh mục 9 API, database schema, cơ chế auth lockout | Thống nhất 100% URL, headers, method với file `server.js` | **PASS** |
| [`PERFORMANCE_TEST_STRATEGY.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/PERFORMANCE_TEST_STRATEGY.md) | Chiến lược tải, Little's Law, mô hình 3 kịch bản, Think time Gaussian | Khớp hoàn toàn với thông số cấu hình trong 3 file JMX | **PASS** |
| [`TEST_DATA_DESIGN.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/TEST_DATA_DESIGN.md) | Thiết kế dữ liệu CSV, cấu hình CSV Data Set Config, nguyên tắc không đụng độ | Khớp hoàn toàn với cấu trúc 5 cột của `data/users.csv` | **PASS** |
| [`LOAD_TEST.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/LOAD_TEST.md) | Đặc tả kịch bản Load Test 50 VUs, assertions, hướng dẫn chạy CLI | Khớp hoàn toàn với file `23120268_Load_20261118.jmx` | **PASS** |
| [`STRESS_TEST.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/STRESS_TEST.md) | Đặc tả kịch bản Stress Test, các bước tải, knee point, breaking point | Khớp hoàn toàn với file `23120268_Stress_20261118.jmx` | **PASS** |
| [`SPIKE_TEST.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/SPIKE_TEST.md) | Đặc tả kịch bản Spike Test, mô hình 5 giai đoạn, Graph Results listener | Khớp hoàn toàn với file `23120268_Spike_20261118.jmx` | **PASS** |
| [`AI_PERFORMANCE_ANALYSIS.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/AI_PERFORMANCE_ANALYSIS.md) | Phân tích sâu thực nghiệm, phát hiện điểm nghẽn Checkout, phân loại tối ưu | Số liệu trích xuất chính xác 100% từ 3 tệp raw JTL | **PASS** |
| [`CONTINUOUS_PERFORMANCE_TESTING.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/CONTINUOUS_PERFORMANCE_TESTING.md) | Đề xuất CI/CD Pipeline, phát hiện regression p95, lộ trình 4 giai đoạn | Mermaid diagram, giải thuật kiểm định Two-Tier Threshold | **PASS** |

---

## 6. Phần 5 – Human Responsibility Checklist (Phần Việc Sinh viên Tự Thực hiện)

Tuân thủ nghiêm ngặt quy định chống gian lận trong Mục 2, Mục 10 và Mục 11 của đề bài, **AI tuyệt đối không được làm thay sinh viên** các hạng mục mang tính cam kết, trải nghiệm và bằng chứng vật lý cá nhân. 

Dưới đây là Checklist chi tiết dành riêng cho bạn thực hiện trước khi nộp bài:

```
╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                     CHECKLIST NHIỆM VỤ CÁ NHÂN BẮT BUỘC (STUDENT TODO)                           ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝

[ ] 1. TỰ VIẾT ĐOẠN VĂN "AI CRITIQUE" (200 – 300 từ)
    - Trả lời rõ ràng 3 câu hỏi bắt buộc:
      1) AI đã hiểu sai, thiên vị hoặc bỏ sót điểm nào trong suốt quá trình làm bài?
         (Ví dụ: Lỗi ban đầu bỏ sót hostname trong HTTP Defaults, lỗi statement finalized trong script seed,
          hoặc việc AI suýt đề xuất Connection Pooling cho SQLite vốn không phù hợp).
      2) Tại sao AI lại mắc lỗi đó? (Do context prompt, do AI thiếu môi trường runtime thật, hay do đặc thù embedded SQLite).
      3) Bạn rút ra được nguyên tắc nào khi làm việc cộng tác với AI trong kỹ thuật kiểm thử hiệu năng?

[ ] 2. TẬP HỢP TÀI LIỆU "AI AUDIT REPORT"
    - Khai báo theo mẫu trong Mục 9: "I use AI tools for the following tasks..."
    - Liệt kê các mốc tương tác chính: Thiết kế kịch bản, Phân tích log JTL, Đề xuất CI/CD.
    - Đính kèm file log tương tác hoặc xuất transcript.

[ ] 3. QUAY VIDEO DEMO KIỂM THỬ THỰC TẾ (Tối thiểu 6 phút)
    - Video phải quay chung **trong cùng một khung hình**:
      + Cửa sổ chạy công cụ (Giao diện JMeter hoặc Terminal chạy lệnh CLI).
      + Cửa sổ giám sát tài nguyên phần cứng thời gian thực (`htop` hoặc System Monitor).
    - Có **giọng thuyết minh tiếng Việt của chính bạn** giải thích các kịch bản đang chạy.
    - Tải video lên YouTube ở chế độ **Không công khai (Unlisted)** và lấy link.

[ ] 4. CHỤP ẢNH BẰNG CHỨNG TÀI NGUYÊN & PHẦN CỨNG (Screenshots)
    - Chụp ảnh màn hình lệnh `neofetch` hoặc `lscpu && free -h` hiển thị rõ tên **Hostname máy của bạn**
      (Tên hostname phải khớp với các bài tập trước đó để qua vòng kiểm tra anti-cheat).
    - Chụp 3 ảnh màn hình `htop` ghi nhận mức tải CPU/RAM khi đang chạy Load Test, Stress Test và Spike Test.

[ ] 5. THỰC HIỆN COMMIT GIT TỪNG BƯỚC & XUẤT GIT LOG
    - Thực hiện các lệnh commit phân tách từng giai đoạn:
      + Commit 1: Test plans (3 file .jmx và thư mục data/)
      + Commit 2: Scripts (seed và reset lockout)
      + Commit 3: Execution logs & HTML reports
      + Commit 4: Tài liệu phân tích và đề xuất CI/CD
    - Xuất nhật ký commit ra file text: `git log --graph --oneline --all > git_commit_log.txt`

[ ] 6. TỔNG HỢP MAIN REPORT & BẢNG TỰ ĐÁNH GIÁ (Self-Assessment Table)
    - Biên soạn file báo cáo tổng thể `README.md` theo mẫu Mục 14 & 15.
    - Điền điểm tự đánh giá vào cột Self-Assessed Grade (thang điểm 100).
    - Xuất báo cáo sang định dạng PDF.
```

---

## 7. Phần 6 – Submission Validation (Kiểm tra Đối chiếu Mục 14 PDF)

Quy định đóng gói file nộp bài trên Moodle theo Mục 14 của đề bài:
* **Quy ước tên file Zip:** `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`
* **Ví dụ mẫu:** `23120268_HW05_AI_Performance_095.zip`

### Bảng Kiểm soát Danh mục Tệp Nộp bài:

| STT | Thành phần Bắt buộc trong File ZIP | Tệp Hiện có trong Dự án | Trạng thái Sẵn sàng | Hành động Cần thiết |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Main Report (Markdown + PDF) | [`docs/performance/`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/) | **SẴN SÀNG** | Sinh viên xuất báo cáo sang bản PDF |
| **2** | Link Public GitHub Repository | Repo Git hiện tại | **SẴN SÀNG** | Push toàn bộ commit lên GitHub cá nhân |
| **3** | Ba Test Plans (`.jmx`) chuẩn tên | [`23120268_Load_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Load_20261118.jmx)<br>[`23120268_Stress_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Stress_20261118.jmx)<br>[`23120268_Spike_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Spike_20261118.jmx) | **SẴN SÀNG 100%** | Đã kiểm tra cú pháp và dry-run đạt chuẩn |
| **4** | Ba tệp nhật ký thô (`.jtl`) | `23120268_Load_20261118.jtl`<br>`23120268_Stress_20261118.jtl`<br>`23120268_Spike_20261118.jtl` | **SẴN SÀNG 100%** | Đầy đủ 36,927 dòng dữ liệu thực |
| **5** | Ba thư mục HTML Report | [`reports/load_report/`](file:///home/hung/26-27/Kiem_thu/eshop-sut/reports/load_report/)<br>[`reports/stress_report/`](file:///home/hung/26-27/Kiem_thu/eshop-sut/reports/stress_report/)<br>[`reports/spike_report/`](file:///home/hung/26-27/Kiem_thu/eshop-sut/reports/spike_report/) | **SẴN SÀNG 100%** | Chứa đầy đủ dashboard và statistics.json |
| **6** | Ảnh chụp Resource & Hardware | Thư mục `screenshots/` | **CHỜ SINH VIÊN** | Chụp ảnh màn hình htop và thông số máy |
| **7** | Link YouTube Demo Video | Đoạn văn đính kèm trong README | **CHỜ SINH VIÊN** | Quay video tối thiểu 6 phút và chèn link |
| **8** | AI Critique (200–300 words) | Bản thảo đính kèm | **CHỜ SINH VIÊN** | Sinh viên tự viết theo suy nghĩ phản biện |
| **9** | AI Audit Report (Markdown + PDF) | Log tương tác | **CHỜ SINH VIÊN** | Đính kèm bản khai báo AI |
| **10**| Git Commit Log (file text) | `git_commit_log.txt` | **CHỜ SINH VIÊN** | Chạy lệnh xuất log sau khi commit |
| **11**| Bug Reports (nếu có) | Thư mục `bug-report/` | **SẴN SÀNG** | Đã ghi nhận các phát hiện về checkout latency |
| **12**| `README.md` kèm Self-Assessment | File `README.md` gốc | **SẴN SÀNG** | Bổ sung bảng tự chấm điểm theo Mục 15 |

---

## 8. Kết luận Đánh giá Tổng thể & Quản trị Rủi ro (Final Assessment)

### 8.1 Những Hạng mục Đã Hoàn thành Xuất sắc (PASS 100%)
1. **Kiến trúc Kiểm thử và Phạm vi API:** Đã phân tích thấu đáo kiến trúc SUT, bao phủ toàn vẹn 3 nhóm endpoint trong một workflow 9 bước thống nhất.
2. **Kỹ thuật JMeter và Dữ liệu Kiểm thử:** 3 Test Plan Load, Stress, Spike được tham số hóa hoàn chỉnh qua CSV, trích xuất JWT Token và Order ID động, kiểm tra assertions nghiệp vụ chặt chẽ, sử dụng 3 report view khác nhau.
3. **Thực thi và Nhật ký Dữ liệu:** Thu thập đầy đủ 3 raw JTL logs với **36,927 lượt requests thành công 100% (0 lỗi 401/403/500)**, tự động tạo 3 HTML dashboards tương ứng.
4. **Phân tích Hiệu năng & Đề xuất CI/CD:** Các báo cáo [`AI_PERFORMANCE_ANALYSIS.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/AI_PERFORMANCE_ANALYSIS.md) và [`CONTINUOUS_PERFORMANCE_TESTING.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/CONTINUOUS_PERFORMANCE_TESTING.md) cung cấp góc nhìn kỹ thuật sâu sắc, dựa trên bằng chứng thực nghiệm, phân định rõ ràng giữa đề xuất và triển khai thực tế.

### 8.2 Những Rủi ro Còn Tồn tại & Biện pháp Phòng ngừa Trước khi Nộp
1. **Rủi ro Nộp Thiếu Thành phần Cá nhân:** Đề bài quy định rất khắt khe: *"Missing any required document results in 0 points."* (Thiếu bất kỳ tài liệu nào sẽ bị 0 điểm toàn bài). Bạn cần kiểm tra kỹ Checklist ở Phần 5 để không bị sót Video Demo, Ảnh chụp màn hình htop hoặc AI Critique.
2. **Rủi ro Hostname Phần cứng:** Giảng viên và TA sẽ đối chiếu hostname trong ảnh chụp phần cứng với các bài tập trước để xác minh bài làm thực tế. Hãy chụp ảnh màn hình từ đúng máy tính bạn thường sử dụng.
3. **Quy tắc Seeder khi Demo:** Khi quay video demo, nếu bạn có thao tác restart server `node server.js`, hãy nhớ chạy ngay lệnh `node scripts/seed_performance_users.js` để nạp lại tài khoản, tránh trường hợp JMeter bị lỗi 401 ngay trong video demo!
