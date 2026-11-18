# CHIẾN LƯỢC KIỂM THỬ HIỆU NĂNG (PERFORMANCE TEST STRATEGY)
## Hệ thống: EShop (System Under Test - SUT)
## Công cụ thực thi: Apache JMeter | Bài tập: HW05 – Performance Testing

---

## 1. Testing Objectives (Mục tiêu kiểm thử)

### 1.1 Mục tiêu tổng thể
Xác định, đo lường và đánh giá năng lực xử lý, độ ổn định và các giới hạn tài nguyên của hệ thống **EShop Backend API** (Node.js/Express + SQLite) khi vận hành dưới các mô hình tải khác nhau, từ đó phát hiện các điểm nghẽn kiến trúc (bottlenecks), tranh chấp khóa cơ sở dữ liệu và nguy cơ rò rỉ bộ nhớ.

### 1.2 Mục tiêu cụ thể theo từng kịch bản kiểm thử
1. **Load Testing (Kiểm thử tải bình thường):**
   * Thiết lập đường cơ sở hiệu năng (Performance Baseline) của hệ thống trong điều kiện vận hành giờ cao điểm thông thường.
   * Xác minh hệ thống đáp ứng thỏa thuận mức dịch vụ (SLA): Thời gian phản hồi trung bình (Average Response Time) < 500ms, tỷ lệ lỗi (Error Rate) < 1%, thông lượng (Throughput) đạt từ 12 – 18 RPS ổn định trong suốt 10 phút tải đỉnh.
   * Đánh giá mức độ chiếm dụng tài nguyên CPU (< 60%) và RAM (< 200MB) của tiến trình Node.js.
2. **Stress Testing (Kiểm thử tải cực hạn / Tăng dần):**
   * Xác định **Điểm bão hòa (Knee of the Curve / Saturation Point)**: Mốc số lượng người dùng đồng thời khiến thời gian phản hồi bắt đầu tăng phi tuyến tính.
   * Xác định **Ngưỡng gãy đổ (Breaking Point / Failure Threshold)**: Mốc tải khiến hệ thống xuất hiện lỗi hàng loạt (Error Rate > 5%), lỗi khóa file `SQLITE_BUSY: database is locked`, hoặc phản hồi vượt quá 5,000ms.
   * Đánh giá hành vi suy giảm hiệu năng có kiểm soát (Graceful Degradation) và giới hạn chịu tải tối đa (Endurance Threshold).
   * Kiểm tra hiện tượng rò rỉ bộ nhớ (Memory Leak) trong biến toàn cục `userCarts` khi số lượng đơn hàng và giỏ hàng tăng liên tục.
3. **Spike Testing (Kiểm thử tải đột biến / Flash Sale):**
   * Đánh giá khả năng chịu sốc của hệ thống khi lưu lượng người dùng tăng đột ngột gấp **7.5 lần** (từ 20 VU lên 150 VU) trong vòng 15 giây.
   * Đo lường tỷ lệ lỗi và độ trễ tăng vọt trong 60 giây duy trì đỉnh đột biến.
   * Đánh giá **Khả năng tự phục hồi (System Recovery / Resilience)**: Thời gian để hệ thống giải phóng hàng đợi, ổn định lại CPU/RAM và đưa thời gian phản hồi về mức bình thường sau khi đột biến kết thúc.

---

## 2. Workflow Design (Thiết kế Luồng Nghiệp vụ Duy nhất)

Nhằm đảm bảo tính nhất quán và khả năng so sánh đối chứng giữa 3 kịch bản, toàn bộ quá trình kiểm thử sẽ sử dụng **một End-to-End (E2E) Workflow duy nhất** phản ánh trọn vẹn hành trình mua sắm thực tế của khách hàng:

$$\mathbf{Login} \longrightarrow \mathbf{Manage\ Profile} \longrightarrow \mathbf{Browse\ Products} \longrightarrow \mathbf{Add\ to\ Cart} \longrightarrow \mathbf{Checkout}$$

```
+---------------------------------------------------------------------------------------------------------+
|                                    END-TO-END ESHOP WORKFLOW (JMeter)                                   |
+---------------------------------------------------------------------------------------------------------+
| [ Step 1: POST /api/login ] -----------------------------------------> Extract: ${token}, ${userId}    |
|       │                                                                                                 |
|       ▼ (Think Time: 2s - 4s)                                                                           |
| [ Step 2a: GET /api/users/me ] --------------------------------------> Header: Bearer ${token}          |
|       │                                                                                                 |
|       ▼ (Think Time: 1s - 2.5s)                                                                         |
| [ Step 2b: PUT /api/users/me ] --------------------------------------> Header: Bearer ${token}          |
|       │                                                                Body: Update name, phone, address|
|       ▼ (Think Time: 3s - 6s)                                                                           |
| [ Step 3a: GET /api/products ] --------------------------------------> Extract: ${productId}, ${price} |
|       │                                                                                                 |
|       ▼ (Think Time: 4s - 8s)                                                                           |
| [ Step 3b: GET /api/products/${productId} ] -------------------------> View Product Detail             |
|       │                                                                                                 |
|       ▼ (Think Time: 5s - 10s)                                                                          |
| [ Step 4: POST /api/cart ] ------------------------------------------> Header: Bearer ${token}          |
|       │                                                                Body: Add item to userCarts      |
|       ▼ (Think Time: 1s - 2s)                                                                           |
| [ Step 5: POST /api/checkout ] --------------------------------------> Header: Bearer ${token}          |
|                                                                        Body: total_amount, shipping_addr|
|                                                                        Extract: ${orderId}              |
+---------------------------------------------------------------------------------------------------------+
```

### Chi tiết 7 HTTP Samplers trong Workflow:

1. **Sampler 1: Login (`POST /api/login`)**
   * **Mục đích:** Xác thực người dùng, sinh JWT Token.
   * **Request Header:** `Content-Type: application/json`
   * **Request Body:** `{"email": "${user_email}", "password": "${user_password}"}`
   * **Hậu xử lý (Post-Processor):**
     * `JSON Extractor`: Trích xuất `$.token` gán vào biến `${token}`.
     * `JSON Extractor`: Trích xuất `$.user.id` gán vào biến `${userId}`.
   * **Kiểm tra (Assertion):** `Response Code = 200`, JSON Path `$.token` tồn tại.

2. **Sampler 2: Get Profile (`GET /api/users/me`)**
   * **Mục đích:** Tải thông tin tài khoản hiện tại vào phiên làm việc.
   * **Request Header:** `Authorization: Bearer ${token}`
   * **Kiểm tra (Assertion):** `Response Code = 200`, JSON Path `$.email` khớp `${user_email}`.

3. **Sampler 3: Update Profile (`PUT /api/users/me`)**
   * **Mục đích:** Mô phỏng thao tác cập nhật địa chỉ giao hàng và số điện thoại trước khi mua sắm.
   * **Request Header:** `Content-Type: application/json`, `Authorization: Bearer ${token}`
   * **Request Body:**
     ```json
     {
       "name": "${user_name}",
       "shipping_address": "${user_address}",
       "phone": "${user_phone}"
     }
     ```
   * **Kiểm tra (Assertion):** `Response Code = 200`, chuỗi phản hồi chứa `"Profile updated"`.

4. **Sampler 4: Browse Products (`GET /api/products`)**
   * **Mục đích:** Tải danh mục toàn bộ sản phẩm trên trang chủ.
   * **Request Header:** Không yêu cầu xác thực.
   * **Hậu xử lý (Post-Processor):**
     * `JSON Extractor`: Trích xuất ngẫu nhiên 1 sản phẩm từ danh sách:
       * `Match No. = 0` (chọn ngẫu nhiên)
       * JSON Path `$.[*].id` gán vào `${productId}`.
       * JSON Path `$.[*].name` gán vào `${productName}`.
       * JSON Path `$.[*].price` gán vào `${productPrice}`.
   * **Kiểm tra (Assertion):** `Response Code = 200`.

5. **Sampler 5: Product Detail (`GET /api/products/${productId}`)**
   * **Mục đích:** Người dùng bấm vào xem trang chi tiết sản phẩm đã chọn.
   * **Request Header:** Không yêu cầu xác thực.
   * **Kiểm tra (Assertion):** `Response Code = 200`, JSON Path `$.name` tồn tại.

6. **Sampler 6: Add to Cart (`POST /api/cart`)**
   * **Mục đích:** Thêm sản phẩm vừa xem vào giỏ hàng cá nhân.
   * **Request Header:** `Content-Type: application/json`, `Authorization: Bearer ${token}`
   * **Request Body:**
     ```json
     {
       "id": ${productId},
       "name": "${productName}",
       "price": ${productPrice},
       "quantity": 1
     }
     ```
   * **Kiểm tra (Assertion):** `Response Code = 200`, phản hồi chứa `"Added to cart"`.

7. **Sampler 7: Checkout (`POST /api/checkout`)**
   * **Mục đích:** Chốt đơn hàng và thanh toán.
   * **Request Header:** `Content-Type: application/json`, `Authorization: Bearer ${token}`
   * **Request Body:**
     ```json
     {
       "total_amount": ${productPrice},
       "shipping_address": "${user_address}"
     }
     ```
   * **Hậu xử lý (Post-Processor):**
     * `JSON Extractor`: Trích xuất `$.orderId` gán vào biến `${orderId}`.
   * **Kiểm tra (Assertion):** `Response Code = 200`, JSON Path `$.orderId` tồn tại.

---

## 3. Endpoint Classification (Phân loại Nhóm Endpoint)

Theo yêu cầu chuẩn hóa của đề bài HW05, cả 3 nhóm endpoint đều hiện diện trực tiếp và đóng vai trò mắt xích trong workflow:

| Nhóm Endpoint | Endpoint trong Workflow | Thao tác Kỹ thuật | Tính chất Tải & Rủi ro Tiềm ẩn |
| :--- | :--- | :--- | :--- |
| **Auth-heavy** | `POST /api/login` | CPU: Thuật toán ký JWT HMAC-SHA256 (`jwt.sign`)<br>DB: Đọc user, kiểm tra lockout, cập nhật `login_attempts` | **Rủi ro Lockout:** Sai 2 lần là bị khóa 3 phút. Nhiều VU tranh chấp ghi SQLite khi reset biến đếm. |
| **Read-heavy** | `GET /api/users/me`<br>`GET /api/products`<br>`GET /api/products/:id` | DB: `SELECT * FROM users WHERE id = ?`<br>DB: `SELECT * FROM products` (Full Scan)<br>DB: `SELECT * FROM products WHERE id = ?` | **Tải Đọc:** Chiếm tỷ lệ request lớn (3/7 request = 43%). Dễ gây nghẽn I/O khi không có Index hoặc Cache. |
| **Transactional** | `PUT /api/users/me`<br>`POST /api/cart`<br>`POST /api/checkout` | DB: `UPDATE users SET ...` (Write Lock SQLite)<br>RAM: `userCarts[userId].push()` (Memory Store)<br>DB: `INSERT INTO orders ...` (Write Lock SQLite) | **Nút thắt Khóa Ghi:** SQLite có cơ chế Single-Writer. Đồng thời ghi sẽ gây xếp hàng chờ (Queue) hoặc lỗi `SQLITE_BUSY`. |

---

## 4. Workload Modeling & Thiết kế Think Time

### 4.1 Cơ sở Toán học: Định luật Little (Little's Law)
Mối quan hệ giữa số lượng người dùng đồng thời ($N$), thông lượng ($X$), thời gian phản hồi kỹ thuật ($R$) và thời gian suy nghĩ của người dùng ($Z$):

$$N = X \times (R + Z)$$

* **Thời gian phản hồi kỹ thuật ($R$):** Trên môi trường thử nghiệm localhost, thời gian phản hồi trung bình của 7 HTTP request dao động từ **0.5s đến 1.5s**.
* **Thời gian chu kỳ người dùng ($T_{cycle} = R + Z$):** Thời gian để 1 Virtual User thực hiện xong 1 lượt mua sắm hoàn chỉnh.

### 4.2 Thiết kế Think Time Chân thực (Realistic User Behavior)
Không áp dụng cùng một Think Time cứng nhắc cho tất cả các request. Hành vi con người thay đổi theo từng bước tương tác:

| Bước tương tác | Thao tác thực tế của người dùng | Bộ định thời JMeter (Timer) | Think Time trung bình | Độ lệch chuẩn (Dev) | Khoảng thời gian thực tế |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Trước Login** | Mở trang đăng nhập, gõ email và mật khẩu | Gaussian Random Timer | 3,000 ms | 1,000 ms | 2.0s – 4.0s |
| **Xem Profile** | Màn hình hồ sơ tải lên, người dùng lướt đọc | Gaussian Random Timer | 1,500 ms | 500 ms | 1.0s – 2.0s |
| **Cập nhật Profile**| Điền thông tin địa chỉ giao hàng và số điện thoại | Gaussian Random Timer | 4,500 ms | 1,500 ms | 3.0s – 6.0s |
| **Duyệt Danh sách** | Cuộn trang chủ, xem hình ảnh và so sánh giá | Gaussian Random Timer | 6,000 ms | 2,000 ms | 4.0s – 8.0s |
| **Xem Chi tiết SP** | Đọc mô tả chi tiết, kiểm tra thông số kỹ thuật | Gaussian Random Timer | 7,000 ms | 2,500 ms | 4.5s – 9.5s |
| **Thêm vào Giỏ** | Chọn số lượng và bấm nút thêm vào giỏ | Gaussian Random Timer | 1,500 ms | 500 ms | 1.0s – 2.0s |
| **Thanh toán** | Rà soát tổng tiền, xác nhận đặt hàng | Gaussian Random Timer | 3,000 ms | 1,000 ms | 2.0s – 4.0s |
| **TỔNG CỘNG ($Z$)** | **Toàn bộ hành trình 1 đơn hàng** | **Gaussian Distribution** | **26,500 ms (~26.5s)** | **—** | **18.5s – 35.5s** |

$$\Rightarrow T_{cycle} = R + Z \approx 1.0\text{s} + 26.5\text{s} = \mathbf{27.5\text{ giây}}$$

---

## 5. Load Test Configuration (Kiểm thử Tải Bình thường)

### 5.1 Cơ sở Lựa chọn Thông số (Rationale)
* **Quy mô hệ thống:** EShop là ứng dụng thương mại điện tử đơn khối (monolith) phục vụ người dùng nội địa với quy mô nhỏ/vừa. Mức tải thông thường vào giờ cao điểm dự kiến khoảng 50 người dùng duyệt mua hàng liên tục.
* **Tính toán Throughput lý thuyết:**
  $$X = \frac{N}{T_{cycle}} = \frac{50}{27.5\text{s}} \approx 1.82\text{ workflows/giây}$$
  * Tổng thông lượng HTTP dự kiến: $1.82 \times 7 \approx \mathbf{12.7\text{ RPS}}$ (Requests Per Second).
  * Tần suất ghi vào SQLite: Mỗi workflow có 3 thao tác ghi (Login update, Update profile, Checkout insert) $\Rightarrow 1.82 \times 3 \approx \mathbf{5.5\text{ writes/giây}}$. Mức này hoàn toàn nằm trong ngưỡng an toàn của SQLite single-writer lock mà không gây nghẽn.
* **Thời gian chạy (Duration):** 10 phút tải đỉnh (Steady State) là khoảng thời gian tiêu chuẩn theo ISTQB để kiểm tra độ ổn định của Garbage Collection (GC) trong Node.js và xác nhận không có memory leakage phát sinh tức thời.

### 5.2 Bảng Thông số Kịch bản Load Testing
```
Load Profile:
VU
50 |                +----------------------------------+
   |               /                                    \
   |              /                                      \
   |             /                                        \
 0 +------------+------------------------------------------+------
   0           60s                660s                    690s  Time
```

| Tham số cấu hình JMeter | Giá trị thiết lập | Cơ sở / Giải thích lý do |
| :--- | :--- | :--- |
| **Thread Group Type** | Standard Thread Group | Đủ tính năng cho tải phẳng đơn giản |
| **Number of Threads (VUs)**| **50 Virtual Users** | Đại diện cho mức tải cao điểm thông thường |
| **Ramp-up Period** | **60 giây** | Tăng dần ~0.83 VU/giây; tránh nghẽn CPU và DB do 50 user login cùng 1 giây |
| **Hold Target Rate (Duration)**| **600 giây (10 phút)** | Duy trì tải đỉnh để đo lường thông số thống kê p90, p95, Throughput |
| **Ramp-down Period** | **30 giây** | Hạ tải dần để các thread hoàn thành transaction dang dở |
| **Loop Count** | **Forever** (bị chặn bởi Duration) | Đảm bảo các VU liên tục lặp lại workflow trong suốt 10 phút |
| **Throughput dự kiến** | **12 – 15 RPS** | 50 VU chia cho chu kỳ ~27.5s, nhân 7 request |
| **Tổng thời gian chạy** | **690 giây (~11.5 phút)** | 60s Ramp-up + 600s Hold + 30s Ramp-down |

---

## 6. Stress Test Configuration (Kiểm thử Tải Cực hạn / Step-up)

### 6.1 Cơ sở Lựa chọn Thông số (Rationale)
* **Phương pháp tiếp cận:** Sử dụng mô hình bậc thang (**Step-up Load Pattern**) gồm 5 giai đoạn, mỗi giai đoạn tăng thêm 50 VUs và giữ ổn định trong 2 phút (120s) để đo lường điểm suy giảm hiệu năng.
* **Ước tính tải tối đa (300 VUs):**
  * Tại mức 150 VUs: Tần suất ghi SQLite đạt $\approx 16.4\text{ writes/giây}$. Bắt đầu xuất hiện độ trễ ghi đĩa (Knee point).
  * Tại mức 200 – 300 VUs: Tần suất ghi SQLite đạt $25 - 35\text{ writes/giây}$ kết hợp với hàng trăm concurrent connections. SQLite file lock bắt đầu nghẽn nghiêm trọng, kích hoạt lỗi `SQLITE_BUSY` (Breaking point).
* **Kiểm soát phần cứng:** Giới hạn trần ở 300 VUs trên máy tính thử nghiệm (Core i7-10750H, 12 vCPUs, 7.1GB RAM) để tránh làm sập hoàn toàn hệ điều hành host do cạn kiệt socket hoặc RAM.

### 6.2 Bảng Thông số Kịch bản Stress Testing
```
Stress Profile (Step-up):
VU
300 |                                    +----------+
    |                                   /            \
200 |                        +---------+              \
    |                       /                          \
150 |             +--------+                            \
    |            /                                       \
100 |      +----+                                         \
    |     /                                                \
 50 |----+                                                  \
  0 +----+------+--------+----+--------+----+--------+------+--- Time
     2m    2m       2m          2m             2m        1m
```

| Giai đoạn (Stage) | Số lượng VUs | Ramp-up | Thời gian duy trì (Hold) | Mục tiêu kiểm tra |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1 (Baseline)** | 50 VUs | 30 giây | 120 giây (2 phút) | Xác nhận trạng thái bình thường |
| **Stage 2 (Moderate Stress)**| 100 VUs | 30 giây | 120 giây (2 phút) | Bắt đầu gây áp lực lên Event Loop |
| **Stage 3 (Saturation Knee)**| 150 VUs | 30 giây | 120 giây (2 phút) | **Tìm Knee Point**: Latency bắt đầu tăng |
| **Stage 4 (Heavy Stress)** | 200 VUs | 30 giây | 120 giây (2 phút) | **Tìm Breaking Point**: Tranh chấp SQLite lock |
| **Stage 5 (Extreme Stress)**| 300 VUs | 30 giây | 120 giây (2 phút) | Giới hạn cực hạn của Node.js & RAM heap |
| **Ramp-down** | Giảm về 0 | 60 giây | — | Kết thúc an toàn |
| **TỔNG THỜI GIAN** | — | — | **~15.5 phút (930 giây)** | Toàn bộ 5 giai đoạn bậc thang |

### 6.3 Kế hoạch Dừng Khẩn cấp (Abort / Fail-Safe Criteria)
Quá trình chạy Stress Test sẽ bị hủy ngay lập tức nếu thỏa mãn một trong các điều kiện sau:
1. **Error Rate vượt quá 15%** liên tục trong vòng 30 giây.
2. **Thời gian phản hồi p95 vượt quá 10,000 ms (10 giây)** liên tục qua 2 giai đoạn lấy mẫu.
3. **Tiến trình Backend Node.js bị crash** (Process terminated / Exit code khác 0).
4. **Dung lượng RAM hệ thống tự do (Available RAM) giảm xuống dưới 300MB** (ngăn chặn tình trạng đóng băng toàn bộ hệ điều hành do Linux OOM Killer).

---

## 7. Spike Test Configuration (Kiểm thử Tải Đột biến / Flash Sale)

### 7.1 Cơ sở Lựa chọn Thông số (Rationale)
* **Kịch bản mô phỏng:** Một đợt Flash Sale hoặc phát hành mã giảm giá số lượng có hạn bắt đầu lúc 12:00. Hàng loạt người dùng đổ xô vào hệ thống cùng một thời điểm.
* **Tải nền (Pre-spike):** 20 VUs (mô phỏng lưu lượng thấp trước giờ mở bán).
* **Độ dốc Spike:** Tăng đột ngột từ 20 VUs lên **150 VUs** chỉ trong vòng **15 giây** (tốc độ gia tăng tải cực mạnh: 8.67 VUs/giây).
* **Thời gian duy trì đỉnh (Hold Peak):** **60 giây** (1 phút). Khoảng thời gian đủ dài để dồn ứ các request vào hàng đợi của Node.js và SQLite, nhưng đủ ngắn để không làm sập hoàn toàn hệ thống.
* **Thời gian quan sát hồi phục (Post-spike Recovery):** **180 giây (3 phút)** ở mức tải 20 VUs. Đây là giai đoạn quan trọng nhất của Spike Testing để xác định:
  * Hệ thống có tự giải phóng hàng đợi bị nghẽn không?
  * Thời gian phản hồi có quay trở về mức bình thường (< 500ms) không?
  * Có request nào bị treo vô hạn (Hung requests) không?

### 7.2 Bảng Thông số Kịch bản Spike Testing
```
Spike Profile:
VU
150 |             +----+
    |            /|    |\
    |           / |    | \
 20 |----------+  |    |  +--------------------------
    |          |  |    |  |
  0 +----------+--+----+--+--------------------------+--- Time
     0        120s 135s 195s 210s                   390s
```

| Giai đoạn (Phase) | Số VUs | Thời lượng | Mô tả hành vi |
| :--- | :--- | :--- | :--- |
| **Phase 1: Pre-spike Baseline** | 20 VUs | 120 giây (2 phút) | Đo lường hiệu năng ổn định trước khi có biến động |
| **Phase 2: Sudden Surge (Spike Up)** | 20 $\rightarrow$ 150 VUs | **15 giây** | Tăng vọt tải gấp 7.5 lần trong thời gian cực ngắn |
| **Phase 3: Spike Peak** | 150 VUs | **60 giây (1 phút)** | Duy trì tải đỉnh cực đại; kiểm tra phản ứng của hệ thống |
| **Phase 4: Fast Recovery (Spike Down)**| 150 $\rightarrow$ 20 VUs | **15 giây** | Hạ tải nhanh về mức tải nền |
| **Phase 5: Post-spike Observation** | 20 VUs | 180 giây (3 phút) | Đánh giá khả năng hồi phục về baseline ban đầu |
| **TỔNG THỜI GIAN** | — | **390 giây (6.5 phút)**| Toàn bộ chu kỳ kiểm thử đột biến |

---

## 8. Metrics and Success Criteria (Tiêu chí Đánh giá & Chỉ số)

Bảng đối chiếu tiêu chí chất lượng (SLA / Quality Gates) giữa 3 kịch bản:

| Chỉ số Đo lường (Metric) | Đơn vị | Load Testing (Pass/Fail SLA) | Stress Testing (Ngưỡng cảnh báo) | Spike Testing (Giai đoạn Peak) | Spike Testing (Sau khi hồi phục) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Average Response Time** | ms | **< 500 ms** | < 2,500 ms | < 4,000 ms | **< 500 ms** |
| **Median Response Time (p50)**| ms | **< 300 ms** | < 1,500 ms | < 2,500 ms | **< 300 ms** |
| **90th Percentile (p90)** | ms | **< 800 ms** | < 4,000 ms | < 6,000 ms | **< 800 ms** |
| **95th Percentile (p95)** | ms | **< 1,200 ms** | < 6,000 ms | < 8,000 ms | **< 1,200 ms** |
| **99th Percentile (p99)** | ms | **< 2,000 ms** | < 8,000 ms | < 10,000 ms | **< 2,000 ms** |
| **Error Rate (%)** | % | **< 1.0%** (Lý tưởng = 0%) | Ghi nhận mốc khi > 5% | < 5% tạm thời | **0.0%** |
| **Throughput (RPS)** | req/s | **12 – 18 RPS** ổn định | Đạt đỉnh rồi suy giảm | Tăng vọt 30 – 50 RPS | Trở lại 5 – 8 RPS |
| **Connect Time** | ms | **< 20 ms** | < 200 ms | < 500 ms | **< 20 ms** |
| **Latency** | ms | **< 400 ms** | < 2,000 ms | < 3,500 ms | **< 400 ms** |
| **CPU Usage (Node.js)** | % | **< 60%** | 85% – 100% | 90% – 100% | Giảm về **< 30%** |
| **Memory Usage (Node.js)** | MB | **< 200 MB** ổn định | Tăng do `userCarts` (< 500MB)| Tăng tức thời | Không bị OOM crash |
| **Thời gian hồi phục (Recovery)**| giây | Không áp dụng | Không áp dụng | Không áp dụng | **< 30 giây** sau khi hạ tải |

---

## 9. Risk Management (Quản lý Rủi ro trong Kiểm thử)

| STT | Rủi ro Kỹ thuật | Nguyên nhân từ Source Code | Hậu quả đối với Bài test | Giải pháp Giảm thiểu trong Kế hoạch Test |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Kích hoạt Khóa tài khoản (Login Lockout)** | Mã nguồn tăng 2 lần mỗi lần sai (`newAttempts + 2 >= 3`), khóa 3 phút ([backend/server.js#L54-L58](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L54-L58)). | Nếu các VU gửi sai pass, tài khoản bị khóa, hàng loạt request sau đó bị lỗi 403 Forbidden. | **Chuẩn bị file `users.csv` chứa 300 - 500 tài khoản hợp lệ 100%**. Tuyệt đối không đưa mật khẩu sai vào bộ test tải. |
| **2** | **Dùng chung tài khoản (Shared Accounts)** | Nhiều VU cùng login vào `test@eshop.com`. | 1) Ghi đè profile liên tục.<br>2) Tranh chấp `UPDATE login_attempts`.<br>3) Tất cả item bị nhồi vào cùng 1 giỏ `userCarts[2]`. | **Mỗi VU được cấp 1 tài khoản độc lập duy nhất** thông qua cấu hình `CSV Data Set Config` (Recycle on EOF = False). |
| **3** | **SQLite File Lock Contention (`SQLITE_BUSY`)** | SQLite là Single-Writer database file đơn `database.sqlite` ([backend/database.js#L4](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js#L4)). | Khi hàng chục VU cùng lúc gọi `checkout` hoặc `update profile`, SQLite báo lỗi khóa file. | Thiết lập Ramp-up hợp lý; áp dụng Think Time ngẫu nhiên để phân tán thời điểm ghi; ghi nhận ngưỡng xảy ra lock làm Breaking Point. |
| **4** | **Rò rỉ Bộ nhớ Giỏ hàng (`userCarts` Memory Leak)** | `userCarts` là object in-memory toàn cục ([backend/server.js#L14](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L14)), checkout xong không bị xóa. | Chạy Stress test lâu sẽ khiến RAM tiến trình Node.js phình to liên tục, dẫn đến crash OOM. | Giám sát `free -m` và `htop` liên tục trong bài test; kiểm tra kích thước tiến trình trước và sau khi test. |
| **5** | **Ô nhiễm Dữ liệu Đơn hàng (Data Accumulation)** | Mỗi lần checkout tạo 1 bản ghi mới trong bảng `orders` ([backend/server.js#L302](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L302)). | Sau nhiều lần test, bảng `orders` có hàng chục nghìn dòng, làm chậm câu truy vấn ở các đợt test sau. | **Bắt buộc reset database (`node database.js`) về trạng thái sạch trước mỗi kịch bản test**. |
| **6** | **Tồn kho Sản phẩm (Product Inventory)** | Không có quản lý tồn kho (không có cột `stock`). | Không có rủi ro hết hàng (out-of-stock), nhưng có thể lỗi nếu ID sản phẩm bị xóa. | Đảm bảo dữ liệu mẫu 5 sản phẩm ban đầu được giữ nguyên vẹn trong DB. |
| **7** | **Hết hạn Token (Token Expiration)** | Hàm `jwt.sign()` không cấu hình `expiresIn` ([backend/server.js#L51](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L51)). | Không có nguy cơ token hết hạn giữa chừng trong bài test. | An toàn tái sử dụng token trong suốt vòng đời của 1 thread iteration. |

---

## 10. JMeter Architecture & Test Plan Implementation (Đề xuất Cấu hình JMeter)

### 10.1 Cây Cấu trúc Thành phần trong Apache JMeter (Test Plan Hierarchy)

```
Test Plan: EShop_Performance_Testing_HW05
│
├── [Config] HTTP Request Defaults
│     ├── Protocol: http
│     ├── Server Name or IP: localhost (hoặc 127.0.0.1)
│     ├── Port Number: 3000
│     └── Timeouts: Connect = 5000ms | Response = 10000ms
│
├── [Config] HTTP Header Manager (Global)
│     └── Content-Type: application/json
│
├── [Config] CSV Data Set Config
│     ├── Filename: data/users.csv
│     ├── Variable Names: user_email,user_password,user_name,user_phone,user_address
│     ├── Delimiter: ,
│     ├── Recycle on EOF: False (cho Stress) / True (cho Load với pacing)
│     └── Stop thread on EOF: True
│
└── [Thread Group] (Tùy chọn theo từng kịch bản: Load / Stress / Spike)
      │
      ├── [Transaction Controller] TC_01_Login
      │     ├── HTTP Request: POST /api/login
      │     ├── JSON Extractor: $.token -> ${token}
      │     ├── JSON Extractor: $.user.id -> ${userId}
      │     ├── Response Assertion: Response Code = 200
      │     └── Gaussian Random Timer: Deviation = 1000ms | Offset = 3000ms
      │
      ├── [Transaction Controller] TC_02_Get_Profile
      │     ├── HTTP Request: GET /api/users/me
      │     ├── HTTP Header Manager: Authorization = Bearer ${token}
      │     ├── Response Assertion: Response Code = 200
      │     └── Gaussian Random Timer: Deviation = 500ms | Offset = 1500ms
      │
      ├── [Transaction Controller] TC_03_Update_Profile
      │     ├── HTTP Request: PUT /api/users/me
      │     ├── HTTP Header Manager: Authorization = Bearer ${token}
      │     ├── Response Assertion: Response Code = 200
      │     └── Gaussian Random Timer: Deviation = 1500ms | Offset = 4500ms
      │
      ├── [Transaction Controller] TC_04_Browse_Products
      │     ├── HTTP Request: GET /api/products
      │     ├── JSON Extractor: $[*].id -> ${productId} (Match No. = 0)
      │     ├── JSON Extractor: $[*].name -> ${productName} (Match No. = 0)
      │     ├── JSON Extractor: $[*].price -> ${productPrice} (Match No. = 0)
      │     ├── Response Assertion: Response Code = 200
      │     └── Gaussian Random Timer: Deviation = 2000ms | Offset = 6000ms
      │
      ├── [Transaction Controller] TC_05_Product_Detail
      │     ├── HTTP Request: GET /api/products/${productId}
      │     ├── Response Assertion: Response Code = 200
      │     └── Gaussian Random Timer: Deviation = 2500ms | Offset = 7000ms
      │
      ├── [Transaction Controller] TC_06_Add_To_Cart
      │     ├── HTTP Request: POST /api/cart
      │     ├── HTTP Header Manager: Authorization = Bearer ${token}
      │     ├── Response Assertion: Response Code = 200
      │     └── Gaussian Random Timer: Deviation = 500ms | Offset = 1500ms
      │
      └── [Transaction Controller] TC_07_Checkout
            ├── HTTP Request: POST /api/checkout
            ├── HTTP Header Manager: Authorization = Bearer ${token}
            ├── JSON Extractor: $.orderId -> ${orderId}
            ├── Response Assertion: Response Code = 200
            └── Gaussian Random Timer: Deviation = 1000ms | Offset = 3000ms
```

### 10.2 Giải thích Chi tiết các Thành phần JMeter Sử dụng:
1. **HTTP Cookie Manager:**
   * **Quyết định: KHÔNG SỬ DỤNG.**
   * **Giải thích:** Phân tích mã nguồn cho thấy hệ thống EShop hoàn toàn không sử dụng Cookie hay HTTP Session. Toàn bộ cơ chế xác thực dựa trên Header `Authorization: Bearer <token>`. Việc thêm Cookie Manager là dư thừa và làm tăng chi phí quản lý context trong JMeter engine.
2. **Transaction Controller:**
   * Được áp dụng cho từng bước nghiệp vụ với thuộc tính `Generate parent sample = true`. Giúp đo lường chính xác toàn bộ thời gian thực hiện của từng nghiệp vụ (Response Time của cả bước) thay vì chỉ đo từng request rời rạc.
3. **JSON Extractor:**
   * Sử dụng để trích xuất dữ liệu động phục vụ liên kết chuỗi (Data Correlation):
     * Lấy `${token}` từ Login truyền vào Header Manager của các request sau.
     * Lấy ngẫu nhiên `${productId}`, `${productName}`, `${productPrice}` (`Match No. = 0`) từ danh sách sản phẩm để truyền vào bước Add to Cart và Checkout.
4. **Gaussian Random Timer:**
   * Phân bổ thời gian chờ giữa các request theo phân phối chuẩn Gaussian (Bell Curve) để phản ánh chân thực độ ngẫu nhiên trong suy nghĩ và thao tác của người dùng thật.
5. **Listeners & Chiến lược Thu thập Kết quả:**
   * **Tuyệt đối không bật Listener dạng bảng/cây trong GUI khi chạy test thật** (như View Results Tree hay Graph Results) vì chúng ngốn rất nhiều RAM của JMeter máy test.
   * Sử dụng cờ CLI để ghi nhật ký trực tiếp ra file nhị phân/CSV `.jtl`:
     ```bash
     jmeter -n -t test_plan.jmx -l results.jtl -e -o ./html_report/
     ```

---

## 11. Execution Strategy (Chiến lược Thực thi Chi tiết)

### 11.1 Chuẩn bị Dữ liệu Thử nghiệm (Data Preparation)
Do hệ thống chỉ có sẵn 2 tài khoản mẫu trong `database.js`, để đáp ứng quy mô lên tới 300 VUs trong kịch bản Stress Testing, ta cần chuẩn bị:
1. **Tạo tập dữ liệu 500 Users:** Tạo file script tạo dữ liệu mẫu chèn 500 tài khoản người dùng vào cơ sở dữ liệu SQLite:
   * Email định dạng: `user_001@eshop.com` đến `user_500@eshop.com`.
   * Mật khẩu đồng nhất: `Test1234!` (đảm bảo mật khẩu đúng để tránh lockout).
   * Họ tên, địa chỉ, số điện thoại ngẫu nhiên hợp lệ.
2. **Xuất file `data/users.csv`:** Cung cấp đầy đủ các cột cho `CSV Data Set Config` của JMeter.

### 11.2 Quy trình Thực thi Chuẩn (Standard Operating Procedure - SOP)
Mỗi đợt chạy kịch bản (Load, Stress, Spike) bắt buộc tuân thủ 5 bước tuần tự:

```
[ Bước 1: Reset Database ] ──> [ Bước 2: Khởi động SUT ] ──> [ Bước 3: Bật Giám sát Hệ thống ]
                                                                     │
[ Bước 5: Phân tích & Báo cáo ] <── [ Bước 4: Chạy JMeter CLI ] <────┘
```

* **Bước 1 — Reset Cơ sở dữ liệu:**
  Thực thi lệnh reset để đưa database về trạng thái sạch ban đầu:
  ```bash
  cd backend && node database.js && node seed_users.js
  ```
* **Bước 2 — Khởi động Backend API:**
  Khởi chạy server trong một tiến trình riêng biệt để ghi log:
  ```bash
  node server.js > backend.log 2>&1 &
  ```
* **Bước 3 — Bật Giám sát Tài nguyên (Resource Monitoring):**
  * Khởi chạy công cụ đo tài nguyên phần cứng (CPU, Memory, Disk I/O) theo thời gian thực (ghi log vào file CSV bằng `vmstat 1` hoặc `pidstat -p <PID> 1` hoặc `top -b -d 1`).
  * Ghi lại ảnh chụp màn hình `htop` trước khi chạy test.
* **Bước 4 — Thực thi JMeter ở Chế độ Non-GUI:**
  * Đặt tên file theo đúng quy ước chống gian lận của đề bài:
    `{StudentID}_{ScenarioType}_{YYYYMMDD}.jmx`
    `{StudentID}_{ScenarioType}_{YYYYMMDD}.jtl`
  * Ví dụ chạy Load Test:
    ```bash
    jmeter -n -t 25127001_Load_20261118.jmx -l 25127001_Load_20261118.jtl -e -o ./reports/load_report/
    ```
* **Bước 5 — Hậu kiểm tra & Thu thập Bằng chứng:**
  * Dừng tiến trình giám sát phần cứng.
  * Kiểm tra file `backend.log` xem có lỗi `SQLITE_BUSY` hay exception không.
  * Lưu lại toàn bộ file `.jtl` thô, thư mục HTML Dashboard Report và ảnh chụp tài nguyên.

---

## 12. Tổng kết Chiến lược (Strategy Summary)

| Kịch bản (Scenario) | Mục tiêu Chính | Số VU tối đa | Thời lượng chạy | Throughput dự kiến | Nguy cơ chính cần theo dõi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Load Testing** | Xác lập Baseline SLA dưới tải bình thường | **50 VUs** | **11.5 phút** | 12 – 18 RPS | CPU/RAM rò rỉ, SLA response time |
| **Stress Testing** | Tìm điểm gãy (Breaking point) & giới hạn chịu tải | **300 VUs** (5 bậc) | **15.5 phút** | 40 – 70 RPS | Lỗi `SQLITE_BUSY`, memory bloat ở `userCarts` |
| **Spike Testing** | Kiểm tra độ co giãn & khả năng tự phục hồi | **150 VUs** (tăng trong 15s)| **6.5 phút** | 30 – 50 RPS (peak)| Hàng đợi request bị nghẽn, thời gian hồi phục |

Chiến lược trên đã bao quát toàn diện các yêu cầu nghiệp vụ, tuân thủ chặt chẽ các phát hiện từ mã nguồn thực tế, và sẵn sàng để chuyển sang giai đoạn tạo các kịch bản kiểm thử cụ thể (`.jmx`) trên Apache JMeter.
