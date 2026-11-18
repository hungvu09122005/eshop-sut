# TÀI LIỆU THIẾT KẾ & HƯỚNG DẪN KIỂM THỬ ĐỘT BIẾN (SPIKE TEST SPECIFICATION)
## Kịch bản: EShop Spike Testing (Flash Sale Simulation) | Mã sinh viên: 23120268
## File Test Plan: `23120268_Spike_20261118.jmx`

---

## 1. Tổng quan Kịch bản Spike Testing (Spike Test Overview)

* **Mục đích:** Đánh giá khả năng chịu đựng của hệ thống EShop trước một đợt tăng vọt lưu lượng truy cập đột ngột và bất thường (mô phỏng sự kiện Flash Sale hoặc chiến dịch Marketing đợt 12:00 trưa), đồng thời kiểm tra quan sát:
  1. Hệ thống có tự phục hồi (Self-heal / Elastic recovery) về trạng thái bình thường sau khi đợt tải đột biến chấm dứt hay không?
  2. Các yêu cầu trong thời gian diễn ra đột biến có bị timeout, drop kết nối hoặc gây crash tiến trình backend Node.js hay không?
  3. Có xảy ra hiện tượng đơn hàng trùng lặp (Duplicate Orders) hay hỏng dữ liệu trong SQLite do tranh chấp đồng thời hay không?
* **Quy ước đặt tên file chuẩn hóa:**
  * File kịch bản kiểm thử JMeter: [`23120268_Spike_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Spike_20261118.jmx)
  * File nhật ký kết quả thô: `23120268_Spike_20261118.jtl`
  * Thư mục báo cáo HTML Dashboard: `reports/spike_report/`
* **Nguyên tắc bảo toàn:** Giữ nguyên **100% endpoint, tham số request và logic nghiệp vụ** của Load Test và Stress Test. Không sửa bất kỳ dòng mã nguồn nào của SUT.

---

## 2. Cấu trúc Cây Test Plan trong JMeter (Test Plan Hierarchy)

Test Plan được xây dựng với **2 Thread Group song song** (Native JMeter Architecture) chạy đồng thời trên cùng một Test Plan (`serialize_threadgroups = false`) để mô phỏng chính xác đường cong tải đột biến mà không cần cài đặt thêm plugin bên thứ ba:

```
Test Plan: EShop_Spike_Test_23120268
│
├── [Config] User Defined Variables:
│     ├── BASE_URL          = localhost
│     ├── PORT              = 3000
│     ├── BASELINE_THREADS  = ${__P(baseline_threads, 20)}   (Mặc định 20 VUs)
│     ├── BASELINE_RAMPUP   = ${__P(baseline_rampup, 20)}    (20 giây ramp-up)
│     ├── TOTAL_DURATION    = ${__P(total_duration, 390)}    (Tổng thời gian 390 giây = 6.5 phút)
│     ├── SPIKE_THREADS     = ${__P(spike_threads, 130)}     (Tải tăng đột biến +130 VUs -> Đỉnh 150 VUs)
│     ├── SPIKE_RAMPUP      = ${__P(spike_rampup, 15)}       (Bùng nổ cực nhanh trong 15 giây)
│     ├── SPIKE_DURATION    = ${__P(spike_duration, 75)}     (15s ramp + 60s duy trì đỉnh)
│     └── SPIKE_DELAY       = ${__P(spike_delay, 120)}       (Trì hoãn kích hoạt lúc t = 120s)
│
├── [Config] HTTP Request Defaults (domain: ${BASE_URL}, port: ${PORT}, timeouts: connect 5s, response 10s)
├── [Config] HTTP Header Manager (Global: Content-Type & Accept: application/json)
├── [Config] CSV Data Set Config - Users
│     ├── Filename: data/users.csv (502 tài khoản test hợp lệ)
│     ├── Recycle on EOF: True (Quay vòng tài khoản độc lập)
│     └── Sharing Mode: All threads (Chia sẻ pool người dùng đồng bộ cho cả 2 Thread Group)
├── [Config] CSV Data Set Config - Products
│     ├── Filename: data/products.csv (5 sản phẩm thực tế)
│     ├── Recycle on EOF: True
│     └── Sharing Mode: All threads
│
├── [Thread Group 1] TG_01_Normal_Load_20VU (Tải nền liên tục từ t = 0 đến t = 390s)
│     │  (Threads: 20 | Ramp-up: 20s | Duration: 390s | Delay: 0s | On Error: Start Next Loop)
│     ├── [Transaction Controller] TC_01_Login         (POST /api/login -> Extract token, userId)
│     ├── [Transaction Controller] TC_02_Get_Profile   (GET /api/users/me -> Verify email)
│     ├── [Transaction Controller] TC_03_Update_Profile (PUT /api/users/me -> Update address, phone)
│     ├── [Transaction Controller] TC_04_Browse_Products (GET /api/products -> Check catalog)
│     ├── [Transaction Controller] TC_05_Product_Detail (GET /api/products/${product_id} -> View detail)
│     ├── [Transaction Controller] TC_06_Add_To_Cart   (POST /api/cart -> Add to in-memory store)
│     ├── [Transaction Controller] TC_07_Get_Cart      (GET /api/cart -> Verify item in cart)
│     ├── [Transaction Controller] TC_08_Checkout      (POST /api/checkout -> Insert order, get orderId)
│     └── [Transaction Controller] TC_09_Verify_Order  (GET /api/orders/${orderId} -> Verify status pending)
│
├── [Thread Group 2] TG_02_Sudden_Spike_130VU (Đợt sóng đột biến bùng nổ tại t = 120s)
│     │  (Threads: 130 | Ramp-up: 15s | Duration: 75s | Delay: 120s | On Error: Start Next Loop)
│     ├── [Transaction Controller] TC_01_Login         (POST /api/login -> Extract token, userId)
│     ├── [Transaction Controller] TC_02_Get_Profile   (GET /api/users/me -> Verify email)
│     ├── [Transaction Controller] TC_03_Update_Profile (PUT /api/users/me -> Update address, phone)
│     ├── [Transaction Controller] TC_04_Browse_Products (GET /api/products -> Check catalog)
│     ├── [Transaction Controller] TC_05_Product_Detail (GET /api/products/${product_id} -> View detail)
│     ├── [Transaction Controller] TC_06_Add_To_Cart   (POST /api/cart -> Add to in-memory store)
│     ├── [Transaction Controller] TC_07_Get_Cart      (GET /api/cart -> Verify item in cart)
│     ├── [Transaction Controller] TC_08_Checkout      (POST /api/checkout -> Insert order, get orderId)
│     └── [Transaction Controller] TC_09_Verify_Order  (GET /api/orders/${orderId} -> Verify status pending)
│
├── [Listener 1] Summary Report (Enabled - Thống kê tổng quan console)
├── [Listener 2] Aggregate Report (Enabled - Báo cáo phân vị độ trễ)
├── [Listener 3] Graph Results (Spike Trend Visualizer) (Enabled - View đồ thị đo nhịp biến thiên tải Spike)
├── [Listener 4] Response Time Graph (Enabled - Biểu đồ thời gian phản hồi trực quan)
└── [Listener 5] View Results Tree (Disabled - Vô hiệu hóa để bảo vệ RAM JMeter)
```

---

## 3. Mô hình Tải Đột biến (Spike Workload Modeling)

### 3.1 Biểu đồ Biên độ Tải theo Thời gian
Đồ thị biểu diễn số lượng Virtual Users đồng thời tác động vào SUT trong suốt 390 giây (6.5 phút):

```
Active VUs
150 |                          +--------------------+
    |                         /|                    |\
    |                        / |                    | \
    |                       /  |      Phase 3       |  \
    |                      /   |    (Spike Peak)    |   \
    |                     /    |     (150 VUs)      |    \
    |          Phase 2   /     |                    |     \  Phase 4
    |       (Spike Surge)/     |                    |      \ (Spike Down)
 20 |----------+--------+      |                    |       +------------------------------------+
    |          |               |                    |       |                                    |
    |          |    Phase 1    |                    |       |              Phase 5               |
    |          | (Pre-spike)   |                    |       |       (Post-spike Recovery)        |
    |          |   (20 VUs)    |                    |       |              (20 VUs)              |
  0 +----------+---------------+--------------------+-------+------------------------------------+---> Time
    0         20s            120s 135s            195s     210s                                390s
```

### 3.2 Bảng Phân kỳ 5 Giai đoạn Kiểm thử

| Giai đoạn (Phase) | Mốc Thời gian | Số lượng VUs | Tốc độ Biến thiên | Mục tiêu Kiểm thử & Trạng thái Kỳ vọng |
| :--- | :---: | :---: | :---: | :--- |
| **Phase 1: Pre-spike Baseline** | $0s \rightarrow 120s$ (2 phút) | **20 VUs** | Ramp-up 20s, giữ ổn định | Đo lường hiệu năng chuẩn của hệ thống ở trạng thái hoạt động bình thường. Response Time < 300ms, Error = 0%. |
| **Phase 2: Sudden Spike Surge** | $120s \rightarrow 135s$ (15 giây) | **20 $\rightarrow$ 150 VUs** | **+8.67 VUs / giây** (Cực mạnh) | Mô phỏng khoảnh khắc Flash Sale mở bán. Kiểm tra hàng đợi socket OS và Node.js Event Loop khi nhận lượng request tăng vọt gấp 7.5 lần. |
| **Phase 3: Spike Peak Hold** | $135s \rightarrow 195s$ (1 phút) | **150 VUs** | Giữ tải đỉnh 150 VUs | Đưa hệ thống vào vùng bão hòa (Saturation Zone). Đo lường đỉnh điểm suy giảm: p95 tăng cao, CPU đạt đỉnh, kiểm tra tranh chấp ghi SQLite. |
| **Phase 4: Sudden Spike Down** | $195s \rightarrow 210s$ (15 giây) | **150 $\rightarrow$ 20 VUs** | **-8.67 VUs / giây** | TG_02 hoàn tất thời hạn và giải phóng threads. Tải đột ngột giảm mạnh về mức nền. |
| **Phase 5: Post-spike Recovery** | $210s \rightarrow 390s$ (3 phút) | **20 VUs** | Giữ ổn định 20 VUs | **Giai đoạn cốt lõi nhất của Spike Test:** Quan sát xem hệ thống có tự xả nghẽn hàng đợi (Drain Queues), trả độ trễ về < 500ms và không bị treo vô hạn hay không. |

---

## 4. Cơ sở Khoa học Lựa chọn Cấu hình Spike (Configuration Rationale)

Tại sao lại chọn cấu hình: **20 VUs Baseline, Đột biến lên 150 VUs trong 15 giây, Duy trì 60 giây và Quan sát hồi phục trong 180 giây?**

### 4.1 Tại sao chọn Tải nền 20 VUs?
* Dựa trên phân tích kiến trúc trong [`API_INVENTORY.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/API_INVENTORY.md) và kết quả chạy thực tế của Load Test:
  * 20 VUs tương ứng với lưu lượng khoảng 5 – 8 RPS.
  * Ở mức này, mức chiếm dụng CPU của Node.js dưới 25%, RAM dưới 100 MB, Response Time trung bình chỉ 80 – 150ms.
  * Đây là "môi trường chuẩn" (Control Baseline) lý tưởng để so sánh trực quan hiệu năng trước, trong và sau đợt đột biến.

### 4.2 Tại sao chọn Đỉnh Spike 150 VUs (Thay vì 500 hay 1000 VUs)?
* **Bản chất kiến trúc SUT:**
  1. Backend là một tiến trình **Node.js duy nhất (Single-threaded Event Loop)** chạy trên Express 5.2.1.
  2. Cơ sở dữ liệu là **SQLite3 (`database.sqlite`) file-based**, sử dụng cơ chế khóa mức file (Single-writer).
* **Kết quả phân tích từ Stress Test:**
  * Điểm gãy gập suy giảm hiệu năng (**Knee of the Curve**) của hệ thống nằm ở mốc **130 – 150 VUs**.
  * Ở mốc 150 VUs, lưu lượng đạt khoảng 35 – 45 RPS và tần suất ghi vào SQLite đạt ~15 writes/giây. Hàng đợi Event Loop bắt đầu hình thành độ trễ nhưng chưa làm đứt kết nối hoàn toàn.
* **Nguyên tắc Spike Testing có kiểm soát (Controlled Spike):**
  * Mục tiêu của Spike Testing **KHÔNG PHẢI** là đánh sập hệ thống (Crash Test), mà là **thử thách độ co giãn (Resilience) và năng lực tự phục hồi (Recovery)**.
  * Nếu bơm một lượng tải đột biến thiếu kiểm soát (như 500 hay 1,000 VUs), SQLite sẽ văng lỗi `SQLITE_BUSY` hàng loạt ngay lập tức và tiến trình Node.js có thể bị crash OS Socket Overflow. Kết quả thu được chỉ là một bảng log toàn lỗi 500/Connection Refused mà không thể đo lường hay đánh giá được khả năng tự phục hồi của hệ thống.
  * Mức tải **150 VUs** là một đợt tăng vọt **gấp 7.5 lần** so với tải nền, đủ mạnh để đẩy hệ thống đến giới hạn bão hòa nhưng vẫn nằm trong phạm vi có thể hồi phục.

### 4.3 Tại sao chọn Thời gian Ramp-up 15 giây & Duy trì Đỉnh 60 giây?
* **15 giây:** Tốc độ gia tăng tải cực mạnh (+8.67 VUs/giây), mô phỏng chính xác hành vi người dùng đồng loạt nhấn F5 vào đúng 12:00:00 Flash Sale.
* **60 giây duy trì đỉnh:** 1 phút là khoảng thời gian vừa đủ để mỗi Virtual User thực hiện từ 2 đến 3 vòng lặp đầy đủ của cả 9 bước (Login $\rightarrow$ Checkout), giúp kiểm tra xem hiện tượng nghẽn hàng đợi có bị tích tụ dồn toa (Cascading Queuing) hay không.

### 4.4 Tại sao Thời gian Quan sát Hồi phục (Recovery Phase) cần tới 180 giây (3 phút)?
* Sau khi đợt tải đỉnh 150 VUs kết thúc, hệ thống cần thời gian để:
  1. Xử lý hết các request còn tồn đọng trong Socket Backlog và Event Loop.
  2. Garbage Collector của V8 dọn dẹp các object giỏ hàng tạm và JSON buffer.
  3. Hệ điều hành giải phóng các kết nối TCP socket ở trạng thái `TIME_WAIT`.
* 180 giây là khoảng thời gian chuẩn mực theo công nghệ kiểm thử hiệu năng để kết luận chắc chắn hệ thống đã hoàn toàn ổn định trở lại hay vẫn còn di chứng âm ỉ (Lagging Degeneracy).

---

## 5. Các Chỉ số Đánh giá Hiệu năng (Evaluation Metrics)

Bảng tiêu chí đối chiếu và đánh giá năng lực co giãn của hệ thống EShop:

| Chỉ số Đo lường (Metric) | Đơn vị | Giai đoạn 1: Trước Spike (0 - 120s) | Giai đoạn 3: Đỉnh Spike (135 - 195s) | Giai đoạn 5: Sau Hồi phục (210 - 390s) | Đánh giá Đạt / Không đạt (SLA) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Active Virtual Users** | Threads | 20 VUs | **150 VUs** | 20 VUs | Đúng kịch bản thiết kế |
| **Average Response Time** | ms | **< 300 ms** | 1,500 – 3,500 ms | **< 350 ms** | **ĐẠT** nếu hồi phục về sát baseline |
| **Median Response Time (p50)**| ms | **< 200 ms** | 1,000 – 2,500 ms | **< 250 ms** | **ĐẠT** |
| **90th Percentile (p90)** | ms | **< 500 ms** | 3,000 – 5,500 ms | **< 600 ms** | **ĐẠT** |
| **95th Percentile (p95)** | ms | **< 800 ms** | 4,000 – 7,000 ms | **< 900 ms** | **ĐẠT** |
| **99th Percentile (p99)** | ms | **< 1,200 ms**| 6,000 – 9,000 ms | **< 1,500 ms**| **ĐẠT** |
| **Throughput (Thông lượng)** | req/s | 6 – 10 RPS | **30 – 45 RPS** | 6 – 10 RPS | Phản ánh chính xác nhịp biến thiên tải |
| **Tỷ lệ Lỗi (Error Rate)** | % | **0.0%** | **< 5.0%** (Tạm thời do nghẽn I/O) | **0.0%** | **ĐẠT** nếu không phát sinh lỗi sau hồi phục |
| **CPU Usage (Node.js)** | % | < 30% | 85% – 100% | **< 35%** | Tự hạ nhiệt sau khi ngắt tải đỉnh |
| **Memory Usage (Node.js)**| MB | ~80 – 120 MB | Tăng do `userCarts` (< 350 MB) | Ổn định, không OOM | Không bị rò rỉ bộ nhớ nghiêm trọng |
| **Thời gian Hồi phục (MTTR)**| giây | Không áp dụng | Không áp dụng | **< 30 giây** | Kể từ khi kết thúc Phase 4 |

---

## 6. Xác minh Tính toàn vẹn Hệ thống (System Verification & Guarantees)

### 6.1 Hệ thống có phục hồi về trạng thái bình thường không?
* **Cơ chế xác nhận:**
  * Trong 180 giây của Phase 5, quan sát đồ thị `Response Time Over Time` và chỉ số trên `Aggregate Report`.
  * Nếu thời gian phản hồi của `TC_01_Login` đến `TC_09_Verify_Order` tụt từ 3,000ms xuống dưới **350ms** trong vòng 30 giây sau khi hạ tải và duy trì ổn định $\rightarrow$ **Xác nhận Hệ thống có năng lực tự hồi phục tuyệt vời (Resilient)**.
  * Nếu Response Time vẫn duy trì ở mức cao (> 2,000ms) dù VUs đã giảm về 20 $\rightarrow$ Phát hiện lỗi rò rỉ tài nguyên (Resource Leak) hoặc nghẽn khóa ngầm trong SQLite.

### 6.2 Các request có bị timeout không?
* Trong kịch bản kiểm thử, `HTTP Request Defaults` được cấu hình nghiêm ngặt:
  * `Connect Timeout`: **5,000 ms (5 giây)**.
  * `Response Timeout`: **10,000 ms (10 giây)**.
* Nếu tại thời điểm đỉnh Spike (150 VUs), thời gian phản hồi vượt quá 10 giây, JMeter sẽ tự động đánh dấu lỗi `java.net.SocketTimeoutException: Read timed out`.
* Tỷ lệ Timeout cho phép trong giai đoạn đỉnh Spike: **$\le 5\%$**. Trong giai đoạn hồi phục: **$0\%$**.

### 6.3 Checkout có xảy ra lỗi nghiệp vụ không?
* Bước `TC_08_Checkout` được kiểm tra bằng các Assertion chặt chẽ:
  1. Kiểm tra HTTP Status Code là `201 Created` hoặc `200 OK`.
  2. JSON Extractor trích xuất mã đơn hàng `${orderId}` qua `$.order.id` hoặc `$.id`.
  3. Response Assertion xác nhận JSON trả về có trường `"message"` hoặc `"order"`.
* Nếu có lỗi ghi SQLite (ví dụ `SQLITE_BUSY`), server sẽ trả mã `500` và Transaction Controller sẽ ghi nhận lỗi ngay lập tức mà không che giấu số liệu.

### 6.4 Có phát sinh Đơn hàng Trùng lặp (Duplicate Orders) không?
* **Phân tích kỹ thuật:**
  * Mỗi Virtual User được cấp phát một tài khoản độc lập từ file [`data/users.csv`](file:///home/hung/26-27/Kiem_thu/eshop-sut/data/users.csv) (gồm 502 người dùng khác nhau).
  * Mỗi vòng lặp tạo ra một phiên làm việc riêng với JWT Token độc lập.
  * Khi gọi `POST /api/checkout`, backend chèn đơn hàng với câu lệnh `INSERT INTO orders (user_id, total_amount, shipping_address, status)` ([backend/server.js#L302](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L302)).
  * Do `orderId` được sinh tự động bằng khóa chính `INTEGER PRIMARY KEY AUTOINCREMENT`, các đơn hàng được gán ID tuần tự duy nhất.
  * Bước `TC_09_Verify_Order` thực hiện `GET /api/orders/${orderId}` để kiểm tra trực tiếp trạng thái đơn hàng vừa tạo. Nếu không tìm thấy hoặc bị trùng lặp trạng thái, Assertion sẽ lập tức phát hiện.

---

## 7. Chi tiết Listener Bổ sung: Graph Results (Spike Trend Visualizer)

Để đáp ứng yêu cầu của bài tập về việc trang bị một **Report View trực quan chuyên biệt cho Spike Test**, Test Plan tích hợp **Graph Results** (`GraphVisualizer`):

### 7.1 Ý nghĩa của Graph Results trong Spike Testing
Khác với Load Test dùng *Summary Report* (xem số liệu tổng thể) hay Stress Test dùng *Aggregate Report* (xem phân vị p95/p99), **Graph Results** là công cụ trực quan hóa thời gian thực bằng đồ thị màu sắc, cho phép nhìn thấy ngay lập tức "cú giật" (Shock Wave) của hệ thống khi đợt tải đột biến ập đến:

```
Graph Results Color Indicators:
- [Đen - Black]:    Số mẫu yêu cầu (Sample Count)
- [Xanh lá - Green]:Thông lượng hiện tại (Current Throughput - req/min)
- [Xanh biển - Blue]:Thời gian phản hồi trung bình (Average Response Time)
- [Đỏ - Red]:       Độ lệch chuẩn (Standard Deviation)
```

### 7.2 Cách đọc Đồ thị Graph Results khi diễn ra Spike:
1. **Tại thời điểm $t = 120s$:** Đường màu xanh biển (Average) và màu đỏ (Deviation) bắt đầu dốc đứng lên cao, phản ánh độ trễ tăng vọt do đợt sóng 130 VUs mới tràn vào.
2. **Tại thời điểm $t = 135s - 195s$:** Đường màu xanh lá (Throughput) đạt đỉnh cực đại, đồng thời đường màu xanh biển dao động mạnh ở mức cao.
3. **Tại thời điểm $t = 210s$ trở đi:** Quan sát thấy đường màu xanh biển (Average) và màu đỏ (Deviation) **lao dốc trở lại về sát trục đáy**, chứng minh hệ thống đã xả nghẽn thành công và phục hồi hoàn toàn về trạng thái ban đầu.

> [!NOTE]
> Ngoài Graph Results, file kịch bản còn tích hợp sẵn **Response Time Graph** (`RespTimeGraphVisualizer`), **Summary Report** và **Aggregate Report**, hỗ trợ xuất báo cáo HTML Dashboard hoàn chỉnh với đầy đủ các biểu đồ tương tác cao.

---

## 8. Hướng dẫn Thực thi Kịch bản Spike Test

### 8.1 Bước 1: Chuẩn bị Môi trường SUT
Đảm bảo backend EShop đang chạy ở trạng thái sạch:
```bash
# Terminal 1: Kiểm tra hoặc khởi động backend
cd /home/hung/26-27/Kiem_thu/eshop-sut/backend
node server.js
```

Kiểm tra trạng thái tài khoản để đảm bảo không có tài khoản nào bị khóa trước khi test:
```bash
# Terminal 2: Reset khóa tài khoản (nếu cần)
node /home/hung/26-27/Kiem_thu/eshop-sut/scripts/reset_account_lockout.js
```

### 8.2 Bước 2: Chạy Spike Test Chuẩn (Non-GUI Mode)
Chạy bài test qua JMeter CLI và tự động tạo HTML Dashboard Report:
```bash
# Terminal 3: Thực thi Spike Test
cd /home/hung/26-27/Kiem_thu/eshop-sut

# Xóa dữ liệu kết quả cũ nếu có
rm -rf 23120268_Spike_20261118.jtl reports/spike_report/

# Thực thi kiểm thử
/home/hung/26-27/Kiem_thu/ex/per/apache-jmeter-5.6.3/bin/jmeter \
  -n \
  -t 23120268_Spike_20261118.jmx \
  -l 23120268_Spike_20261118.jtl \
  -e -o ./reports/spike_report/
```

### 8.3 Bước 3: Chạy Tùy biến Tham số (Tùy chọn)
Nhờ cơ chế User Defined Variables `${__P(...)}`, người dùng có thể linh hoạt điều chỉnh quy mô đợt Spike qua tham số dòng lệnh mà không cần sửa file `.jmx`:

* **Chạy thử đợt Spike nhỏ (Baseline 10 VUs, Đỉnh 50 VUs trong 3 phút):**
  ```bash
  /home/hung/26-27/Kiem_thu/ex/per/apache-jmeter-5.6.3/bin/jmeter \
    -n -t 23120268_Spike_20261118.jmx \
    -Jbaseline_threads=10 -Jbaseline_rampup=10 \
    -Jspike_threads=40 -Jspike_rampup=10 -Jspike_duration=40 -Jspike_delay=60 \
    -Jtotal_duration=180 \
    -l 23120268_Spike_20261118.jtl -e -o ./reports/spike_report/
  ```

---

## 9. Đề xuất Điều kiện Dừng Test Khẩn cấp (Fail-Safe Abort Rules)

Mặc dù kịch bản Spike Test đã được tính toán kỹ lưỡng ở mức 150 VUs (trong ngưỡng kiểm soát), kiểm thử viên vẫn cần giám sát trực tiếp và kích hoạt lệnh dừng test (`Ctrl + C` trên terminal JMeter) nếu xuất hiện một trong các dấu hiệu nguy hiểm sau:

1. **Error Rate vượt quá 20%** liên tục trong hơn 30 giây trong giai đoạn Phase 3 (Đỉnh Spike).
2. **Tiến trình Backend Node.js bị thoát đột ngột (Crash / Process Terminated)** do cạn bộ nhớ hoặc unhandled exception.
3. **RAM trống của máy Host giảm xuống dưới 200 MB** (nguy cơ treo máy kiểm thử).
4. **Hệ thống không thể hạ tải sau Phase 4:** Nếu sau thời điểm $t = 240s$ (đã qua đợt Spike hơn 30 giây) mà CPU Node.js vẫn bị ghim cứng ở mức 100% và không có dấu hiệu suy giảm, cần dừng test để giải phóng tài nguyên CPU.
