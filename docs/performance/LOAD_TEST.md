# TÀI LIỆU THIẾT KẾ & HƯỚNG DẪN KIỂM THỬ TẢI (LOAD TEST SPECIFICATION)
## Kịch bản: EShop Load Testing | Mã sinh viên: 23120268
## File Test Plan: `23120268_Load_20261118.jmx`

---

## 1. Tổng quan Kịch bản Load Testing (Load Test Overview)

* **Mục đích:** Mô phỏng tải truy cập đồng thời của 50 người dùng trong giờ cao điểm bình thường, đo lường các chỉ số hiệu năng cơ sở (Baseline SLA: Response Time, Throughput, Error Rate) cho toàn bộ chu trình mua sắm End-to-End của ứng dụng EShop.
* **Quy ước tên file:** Tuân thủ quy định chuẩn hóa của bài tập HW05:
  * File kịch bản kiểm thử: [`23120268_Load_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Load_20261118.jmx)
  * File nhật ký kết quả thô dự kiến: `23120268_Load_20261118.jtl`
  * Thư mục báo cáo HTML Dashboard dự kiến: `reports/load_report/`
* **Môi trường thử nghiệm:**
  * SUT Backend API: `http://localhost:3000` (Node.js/Express.js + SQLite).
  * Công cụ thực thi: Apache JMeter `5.6.3` (chạy trên Java OpenJDK 17).

---

## 2. Cấu trúc Cây Test Plan trong JMeter (Test Plan Hierarchy)

```
Test Plan: EShop_Load_Test_23120268
│
├── [Config] HTTP Request Defaults (domain: localhost, port: 3000, timeouts: 5s/10s)
├── [Config] HTTP Header Manager (Global: Content-Type & Accept: application/json)
├── [Config] CSV Data Set Config - Users (data/users.csv: 502 accounts)
├── [Config] CSV Data Set Config - Products (data/products.csv: 5 real products)
│
└── [Thread Group] TG_EShop_Load_50VU
      │  (50 Threads | Ramp-up: 60s | Duration: 600s | Action on Error: Start Next Loop)
      │
      ├── [Transaction Controller] TC_01_Login
      │     └── HTTP Sampler: POST /api/login
      │           ├── JSON Extractor: token -> ${token}
      │           ├── JSON Extractor: user.id -> ${userId}
      │           ├── Response Assertion: HTTP 200
      │           ├── Response Assertion: Contains "token"
      │           ├── Response Assertion: Contains "Login successful"
      │           └── Gaussian Random Timer: 3000ms ± 1000ms
      │
      ├── [Transaction Controller] TC_02_Get_Profile
      │     └── HTTP Sampler: GET /api/users/me
      │           ├── Header Manager: Authorization: Bearer ${token}
      │           ├── Response Assertion: HTTP 200
      │           ├── Response Assertion: Contains "${user_email}"
      │           └── Gaussian Random Timer: 1500ms ± 500ms
      │
      ├── [Transaction Controller] TC_03_Update_Profile
      │     └── HTTP Sampler: PUT /api/users/me
      │           ├── Header Manager: Authorization: Bearer ${token}
      │           ├── Response Assertion: HTTP 200
      │           ├── Response Assertion: Contains "Profile updated"
      │           └── Gaussian Random Timer: 4500ms ± 1500ms
      │
      ├── [Transaction Controller] TC_04_Browse_Products
      │     └── HTTP Sampler: GET /api/products
      │           ├── Response Assertion: HTTP 200
      │           ├── Response Assertion: Contains "name"
      │           └── Gaussian Random Timer: 6000ms ± 2000ms
      │
      ├── [Transaction Controller] TC_05_Product_Detail
      │     └── HTTP Sampler: GET /api/products/${product_id}
      │           ├── Response Assertion: HTTP 200
      │           ├── Response Assertion: Contains "id":${product_id}
      │           └── Gaussian Random Timer: 7000ms ± 2500ms
      │
      ├── [Transaction Controller] TC_06_Add_To_Cart
      │     └── HTTP Sampler: POST /api/cart
      │           ├── Header Manager: Authorization: Bearer ${token}
      │           ├── Response Assertion: HTTP 200
      │           ├── Response Assertion: Contains "Added to cart"
      │           └── Gaussian Random Timer: 1500ms ± 500ms
      │
      ├── [Transaction Controller] TC_07_Get_Cart
      │     └── HTTP Sampler: GET /api/cart
      │           ├── Header Manager: Authorization: Bearer ${token}
      │           ├── Response Assertion: HTTP 200
      │           ├── Response Assertion: Contains "id":${product_id}
      │           └── Gaussian Random Timer: 1500ms ± 500ms
      │
      ├── [Transaction Controller] TC_08_Checkout
      │     └── HTTP Sampler: POST /api/checkout
      │           ├── Header Manager: Authorization: Bearer ${token}
      │           ├── JSON Extractor: orderId -> ${orderId}
      │           ├── Response Assertion: HTTP 200
      │           ├── Response Assertion: Contains "Checkout successful"
      │           ├── Response Assertion: Contains "orderId"
      │           └── Gaussian Random Timer: 3000ms ± 1000ms
      │
      ├── [Transaction Controller] TC_09_Verify_Order
      │     └── HTTP Sampler: GET /api/orders/${orderId}
      │           ├── Response Assertion: HTTP 200
      │           ├── Response Assertion: Contains "id":${orderId}
      │           ├── Response Assertion: Contains "status":"pending"
      │           └── Gaussian Random Timer: 1000ms ± 500ms
      │
      ├── [Listener] Summary Report (Report view chính - Enabled)
      └── [Listener] View Results Tree (Chỉ dùng khi Debug 1 thread - Disabled)
```

---

## 3. Chi tiết Luồng Nghiệp vụ & Thông số Từng Request

### 3.1 Bước 1: Login (`TC_01_Login`)
* **Endpoint:** `POST /api/login`
* **Mục đích:** Xác thực người dùng và nhận JWT token.
* **Payload gửi đi:**
  ```json
  {
    "email": "${user_email}",
    "password": "${user_password}"
  }
  ```
* **Post-Processors (Trích xuất dữ liệu động):**
  * `token`: JSON Path `$.token` (Lưu JWT dùng cho các bước sau).
  * `userId`: JSON Path `$.user.id`.
* **Assertions (Xác thực tính đúng đắn):**
  1. Response Code = `200`.
  2. Response Body chứa chuỗi `"token"`.
  3. Response Body chứa chuỗi `"Login successful"`.
* **Think Time:** Gaussian Random Timer (Delay: 3000ms, Dev: 1000ms $\rightarrow$ 2s–4s).

---

### 3.2 Bước 2: Get Profile (`TC_02_Get_Profile`)
* **Endpoint:** `GET /api/users/me`
* **Mục đích:** Lấy thông tin tài khoản hiện tại vào phiên làm việc.
* **Header riêng:** `Authorization: Bearer ${token}`
* **Assertions:**
  1. Response Code = `200`.
  2. Response Body chứa `"email":"${user_email}"` (Khớp chính xác email đã login).
* **Think Time:** Gaussian Random Timer (Delay: 1500ms, Dev: 500ms $\rightarrow$ 1s–2s).

---

### 3.3 Bước 3: Update Profile (`TC_03_Update_Profile`)
* **Endpoint:** `PUT /api/users/me`
* **Mục đích:** Cập nhật thông tin số điện thoại và địa chỉ nhận hàng cá nhân.
* **Header riêng:** `Authorization: Bearer ${token}`
* **Payload gửi đi:**
  ```json
  {
    "name": "${user_name}",
    "shipping_address": "${user_address}",
    "phone": "${user_phone}"
  }
  ```
* **Assertions:**
  1. Response Code = `200`.
  2. Response Body chứa `"Profile updated"`.
* **Think Time:** Gaussian Random Timer (Delay: 4500ms, Dev: 1500ms $\rightarrow$ 3s–6s).

---

### 3.4 Bước 4: Browse Products (`TC_04_Browse_Products`)
* **Endpoint:** `GET /api/products`
* **Mục đích:** Tải toàn bộ danh mục sản phẩm của cửa hàng.
* **Header:** Không yêu cầu token (Public API).
* **Assertions:**
  1. Response Code = `200`.
  2. Response Body chứa danh sách sản phẩm (chứa trường `"name"`).
* **Think Time:** Gaussian Random Timer (Delay: 6000ms, Dev: 2000ms $\rightarrow$ 4s–8s).

---

### 3.5 Bước 5: Product Detail (`TC_05_Product_Detail`)
* **Endpoint:** `GET /api/products/${product_id}`
* **Mục đích:** Xem trang chi tiết sản phẩm được chọn từ file `data/products.csv`.
* **Tham số đường dẫn:** `${product_id}` nhận giá trị từ 1 đến 5 từ CSV.
* **Assertions:**
  1. Response Code = `200`.
  2. Response Body chứa `"id":${product_id}` (Khớp chính xác ID sản phẩm cần xem).
* **Think Time:** Gaussian Random Timer (Delay: 7000ms, Dev: 2500ms $\rightarrow$ 4.5s–9.5s).

---

### 3.6 Bước 6: Add to Cart (`TC_06_Add_To_Cart`)
* **Endpoint:** `POST /api/cart`
* **Mục đích:** Thêm sản phẩm vừa xem vào giỏ hàng in-memory của server (`userCarts[userId]`).
* **Header riêng:** `Authorization: Bearer ${token}`
* **Payload gửi đi:**
  ```json
  {
    "id": ${product_id},
    "name": "${product_name}",
    "price": ${product_price},
    "quantity": ${quantity}
  }
  ```
* **Assertions:**
  1. Response Code = `200`.
  2. Response Body chứa `"Added to cart"`.
* **Think Time:** Gaussian Random Timer (Delay: 1500ms, Dev: 500ms $\rightarrow$ 1s–2s).

---

### 3.7 Bước 7: Get Cart (`TC_07_Get_Cart`)
* **Endpoint:** `GET /api/cart`
* **Mục đích:** Kiểm tra giỏ hàng để xác nhận sản phẩm đã được lưu trữ thành công trên server trước khi tiến hành thanh toán.
* **Header riêng:** `Authorization: Bearer ${token}`
* **Assertions:**
  1. Response Code = `200`.
  2. Response Body chứa `"id":${product_id}` (Sản phẩm vừa thêm thực sự nằm trong giỏ).
* **Think Time:** Gaussian Random Timer (Delay: 1500ms, Dev: 500ms $\rightarrow$ 1s–2s).

---

### 3.8 Bước 8: Checkout (`TC_08_Checkout`)
* **Endpoint:** `POST /api/checkout`
* **Mục đích:** Đặt hàng và ghi nhận đơn hàng vào cơ sở dữ liệu SQLite.
* **Header riêng:** `Authorization: Bearer ${token}`
* **Payload gửi đi:**
  ```json
  {
    "total_amount": ${product_price},
    "shipping_address": "${user_address}"
  }
  ```
* **Post-Processor:**
  * `orderId`: JSON Path `$.orderId` (Lấy mã đơn hàng vừa sinh).
* **Assertions:**
  1. Response Code = `200`.
  2. Response Body chứa `"Checkout successful"`.
  3. Response Body chứa trường `"orderId"`.
* **Think Time:** Gaussian Random Timer (Delay: 3000ms, Dev: 1000ms $\rightarrow$ 2s–4s).

---

### 3.9 Bước 9: Verify Order (`TC_09_Verify_Order`)
* **Endpoint:** `GET /api/orders/${orderId}`
* **Mục đích:** Xác minh trạng thái nghiệp vụ cuối cùng — xác nhận đơn hàng thực sự tồn tại trong SQLite với trạng thái mặc định `pending`.
* **Assertions:**
  1. Response Code = `200`.
  2. Response Body chứa `"id":${orderId}`.
  3. Response Body chứa `"status":"pending"`.
* **Think Time:** Gaussian Random Timer (Delay: 1000ms, Dev: 500ms $\rightarrow$ 1s–2s).

---

## 4. Cơ chế Kiểm tra Tính Chính xác & Ngắt Luồng Lỗi

### 4.1 Không chỉ kiểm tra HTTP 200 (Business Assertions)
Hệ thống EShop có nhiều lỗi logic cố ý (ví dụ: truy vấn sản phẩm không tồn tại vẫn trả về HTTP 200 kèm `{}`). Do đó, kịch bản Load Test áp dụng **hai lớp kiểm tra kép** trên mọi sampler:
* **Lớp 1 (HTTP Level):** Kiểm tra mã trạng thái phản hồi `Assertion.response_code = 200`.
* **Lớp 2 (Business Logic Level):** Kiểm tra nội dung JSON trả về:
  * Phải chứa đúng chuỗi thông báo (`"Login successful"`, `"Profile updated"`, `"Added to cart"`, `"Checkout successful"`).
  * Phải khớp đúng dữ liệu định danh (`${user_email}`, `${product_id}`, `${orderId}`, `"status":"pending"`).

### 4.2 Cơ chế Ngăn chặn Thảm họa Dây chuyền (Fail-Fast Mechanism)
* Trong cấu hình Thread Group:
  ```xml
  <stringProp name="ThreadGroup.on_sample_error">startnextloop</stringProp>
  ```
* **Ý nghĩa thực tế:** Nếu bước Login thất bại (hoặc không lấy được token), Thread Group sẽ **lập tức dừng toàn bộ các bước còn lại** (không gọi Profile, Cart, Checkout vô ích) và chuyển sang vòng lặp tiếp theo. Điều này ngăn chặn việc sinh ra hàng loạt request 401 giả tạo làm méo mó kết quả kiểm thử.

---

## 5. Cấu hình Thông số Tải (Workload Parameters)

Các thông số tuân thủ nghiêm ngặt theo tài liệu chiến lược [PERFORMANCE_TEST_STRATEGY.md](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/PERFORMANCE_TEST_STRATEGY.md):

| Tham số Cấu hình | Giá trị | Cơ sở Kỹ thuật |
| :--- | :--- | :--- |
| **Number of Threads (Users)** | **50 VUs** | Mức tải giờ cao điểm thông thường của ứng dụng EShop |
| **Ramp-up Period** | **60 giây** | Tăng dần ~0.83 user/giây; phân tán tải, tránh dồn 50 login cùng 1 giây |
| **Duration (Thời gian duy trì tải đỉnh)**| **600 giây (10 phút)** | Tiêu chuẩn đo lường SLA và kiểm tra độ ổn định GC của Node.js |
| **Loop Count** | **Forever (-1)** | Chạy liên tục các vòng lặp trong suốt 10 phút, kiểm soát bởi Duration |
| **Pacing / Think Time trung bình** | **~26.5 giây** | Sử dụng Gaussian Random Timer chân thực trên từng bước |
| **Throughput kỳ vọng** | **12 – 15 RPS** | 50 VU chia cho chu kỳ ~27.5s, nhân 9 HTTP requests |

---

## 6. Chiến lược Báo cáo & Listener (Reporting Strategy)

### 6.1 Sử dụng Summary Report làm View Chính
Trong file `.jmx`, thành phần Listener được cấu hình như sau:
* **`Summary Report` (Enabled):** Thu thập các chỉ số thống kê tổng hợp (Sample count, Average, Min, Max, Std. Dev., Error %, Throughput, Received KB/sec) với chi phí tài nguyên CPU/RAM cực thấp.
* **`View Results Tree` (Disabled):** Được tích hợp sẵn trong kịch bản để phục vụ việc debug lỗi 1 user khi cần thiết, nhưng mặc định bị tắt (`enabled="false"`) khi chạy tải lớn để tránh tràn bộ nhớ JVM của JMeter.

---

## 7. Hướng dẫn Thực thi Kịch bản Kiểm thử

### 7.1 Bước 1: Khởi động Backend SUT
Mở Terminal và khởi chạy backend server:
```bash
cd backend
node server.js
# Đảm bảo console thông báo: Server is running on http://localhost:3000
```

### 7.2 Bước 2: Chuẩn bị Dữ liệu Tài khoản (Bắt buộc)
Trước khi chạy tải 50 VUs, database SQLite cần được nạp đầy đủ 500 tài khoản kiểm thử từ `data/users.csv`. Thực hiện lệnh:
```bash
# Nạp 500 tài khoản vào SQLite mà không xóa bảng cũ
node scripts/seed_performance_users.js
```

### 7.3 Bước 3: Chạy Kịch bản bằng Apache JMeter ở Chế độ Non-GUI (CLI)
Thực thi lệnh kiểm thử tại thư mục gốc của dự án:
```bash
# Xóa log cũ nếu có
rm -rf 23120268_Load_20261118.jtl reports/load_report/

# Chạy Load Test và tự động sinh HTML Dashboard Report
/home/hung/26-27/Kiem_thu/ex/per/apache-jmeter-5.6.3/bin/jmeter \
  -n \
  -t 23120268_Load_20261118.jmx \
  -l 23120268_Load_20261118.jtl \
  -e -o ./reports/load_report/
```

---

## 8. Hướng dẫn Đọc Kết quả & Đánh giá Tiêu chí Đạt/Không đạt (Quality Gates)

Khi bài kiểm thử hoàn tất, mở file HTML report tại `reports/load_report/index.html` hoặc đọc kết quả từ bảng `Summary Report`:

| Chỉ số Đo lường | Ngưỡng Đạt (Pass Criteria SLA) | Ngưỡng Không Đạt (Fail) | Ý nghĩa Kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Tỷ lệ Lỗi (Error %)** | **< 1.0%** (Lý tưởng 0%) | $\ge 1.0\%$ | Đảm bảo tính sẵn sàng và tính ổn định nghiệp vụ |
| **Average Response Time** | **< 500 ms** | $\ge 500\text{ ms}$ | Thời gian phản hồi trung bình toàn hệ thống |
| **95th Percentile (p95)** | **< 1,200 ms** | $\ge 1,200\text{ ms}$ | 95% số request hoàn thành dưới 1.2 giây |
| **99th Percentile (p99)** | **< 2,000 ms** | $\ge 2,000\text{ ms}$ | Đảm bảo không có hiện tượng treo request bất thường |
| **Throughput** | **12 – 15 RPS** | $< 10\text{ RPS}$ | Năng lực thông lượng đáp ứng đúng tính toán Little's Law |

---

## 9. Báo cáo Các Điểm Chưa Xác minh (Unverified Information & Known Limitations)

Tuân thủ quy tắc minh bạch, các hạn chế và điểm chưa xác minh trong lượt triển khai này bao gồm:
1. **Trạng thái thực thi:** File kịch bản `23120268_Load_20261118.jmx` đã được **kiểm tra cú pháp và cấu trúc cây (Tree parsing validation)** thành công 100% trên binary Apache JMeter 5.6.3. Tuy nhiên, đợt chạy đầy đủ trọn vẹn 10 phút với 50 VUs **chưa được kích hoạt tự động** trong lượt này để người dùng có thể chủ động giám sát tài nguyên phần cứng (CPU/RAM bằng `htop`) và nạp dữ liệu tài khoản khi bước vào phiên test chính thức.
2. **Hạn chế của API Checkout:** Như đã phát hiện trong phân tích mã nguồn, `POST /api/checkout` không lưu chi tiết các sản phẩm trong giỏ hàng vào database (không có bảng `order_items`). Bước 9 `GET /api/orders/${orderId}` chỉ xác nhận đơn hàng tồn tại với `status: "pending"` và `total_amount`, không kiểm tra được danh sách từng item đã mua.
