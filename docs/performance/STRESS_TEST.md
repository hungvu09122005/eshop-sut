# TÀI LIỆU THIẾT KẾ & HƯỚNG DẪN KIỂM THỬ CỰC HẠN (STRESS TEST SPECIFICATION)
## Kịch bản: EShop Stress Testing | Mã sinh viên: 23120268
## File Test Plan: `23120268_Stress_20261118.jmx`

---

## 1. Tổng quan Kịch bản Stress Testing (Stress Test Overview)

* **Mục đích:** Đẩy mức tải vượt qua ngưỡng vận hành bình thường (từ 50 VUs lên tới 300 VUs) để tìm kiếm:
  1. **Mức tải ổn định tối đa (Maximum Stable Load)**.
  2. **Điểm bão hòa bắt đầu suy giảm hiệu năng (Knee of the Curve / Saturation Point)**.
  3. **Ngưỡng gãy đổ của hệ thống (Breaking Point / Failure Threshold)**.
  4. Cơ chế lỗi khi hệ thống quá tải (Tranh chấp khóa SQLite `SQLITE_BUSY`, nghẽn Node.js Event Loop hay tràn bộ nhớ RAM do `userCarts`).
* **Quy ước tên file chuẩn hóa:**
  * File kịch bản kiểm thử: [`23120268_Stress_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Stress_20261118.jmx)
  * File nhật ký kết quả thô: `23120268_Stress_20261118.jtl`
  * Thư mục báo cáo HTML Dashboard: `reports/stress_report/`
* **Nguyên tắc bảo toàn:** Giữ nguyên **100% endpoint, tham số request và logic nghiệp vụ** của Load Test. Không sửa bất kỳ dòng mã nguồn nào của SUT.

---

## 2. Cấu trúc Cây Test Plan trong JMeter (Test Plan Hierarchy)

```
Test Plan: EShop_Stress_Test_23120268
│
├── [Config] User Defined Variables:
│     ├── BASE_URL  = localhost
│     ├── PORT      = 3000
│     ├── THREADS   = ${__P(threads, 300)}   (Mặc định 300 VUs, tùy biến qua CLI)
│     ├── RAMPUP    = ${__P(rampup, 300)}    (Mặc định 300 giây)
│     └── DURATION  = ${__P(duration, 900)}  (Mặc định 900 giây = 15 phút)
│
├── [Config] HTTP Request Defaults (domain: ${BASE_URL}, port: ${PORT}, timeouts: 5s/10s)
├── [Config] HTTP Header Manager (Global: Content-Type & Accept: application/json)
├── [Config] CSV Data Set Config - Users
│     ├── Filename: data/users.csv (502 tài khoản hợp lệ)
│     ├── Recycle on EOF: False (Mỗi VU trong 300 VUs nhận 1 user duy nhất, không lặp lại)
│     └── Stop thread on EOF: True
├── [Config] CSV Data Set Config - Products
│     ├── Filename: data/products.csv (5 sản phẩm thực tế)
│     └── Recycle on EOF: True (Quay vòng liên tục sản phẩm 1..5)
│
└── [Thread Group] TG_EShop_Stress_300VU
      │  (Threads: ${THREADS} | Ramp-up: ${RAMPUP}s | Duration: ${DURATION}s | On Error: Start Next Loop)
      │
      ├── [Transaction Controller] TC_01_Login         (POST /api/login -> Extract token, userId)
      ├── [Transaction Controller] TC_02_Get_Profile   (GET /api/users/me -> Verify email)
      ├── [Transaction Controller] TC_03_Update_Profile (PUT /api/users/me -> Update address, phone)
      ├── [Transaction Controller] TC_04_Browse_Products (GET /api/products -> Check catalog)
      ├── [Transaction Controller] TC_05_Product_Detail (GET /api/products/${product_id} -> View detail)
      ├── [Transaction Controller] TC_06_Add_To_Cart   (POST /api/cart -> Add to in-memory store)
      ├── [Transaction Controller] TC_07_Get_Cart      (GET /api/cart -> Verify item in cart)
      ├── [Transaction Controller] TC_08_Checkout      (POST /api/checkout -> Insert order, get orderId)
      ├── [Transaction Controller] TC_09_Verify_Order  (GET /api/orders/${orderId} -> Verify status pending)
      │
      ├── [Listener] Aggregate Report (Report view chính - Enabled)
      ├── [Listener] Summary Report (Console tracking - Enabled)
      └── [Listener] View Results Tree (Debug only - Disabled)
```

---

## 3. Mô hình Tải Bậc thang & Phân tích Giai đoạn (Step-up Workload Modeling)

Mô hình tải được thiết kế tăng dần tuyến tính (**Linear Step-up Pattern**) từ 0 đến **300 Virtual Users** trong 300 giây (tốc độ gia tăng đều đặn: 1 user/giây), sau đó duy trì tải đỉnh 300 VUs trong 600 giây (10 phút). 

```
Stress Load Profile:
Active VUs
300 |                                    +----------------------------------+
    |                                   /|                                  |
200 |                        +---------+ |                                  |
    |                       /| Stage 4   |                                  |
150 |             +--------+ |           |                                  |
    |            /| Stage 3  |           |          Stage 5                 |
100 |      +----+ |          |           |      (Extreme Stress)            |
    |     /| S2   |          |           |                                  |
 50 |----+ |      |          |           |                                  |
    | S1 | |      |          |           |                                  |
  0 +----+--+------+----------+-----------+----------------------------------+---> Time
     0   50s 100s  150s       200s        300s                               900s (15 min)
```

### Phân tích 5 Giai đoạn Tải Chi tiết

| Giai đoạn (Stage) | Khoảng Tải (VUs) | Throughput Ước tính | Tần suất Ghi SQLite | Trạng thái Kỳ vọng của Hệ thống |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1 (Baseline)** | **1 – 50 VUs** (0 – 50s) | 10 – 15 RPS | 3 – 5 writes/s | **Bình thường (Healthy):** Response Time < 500ms, Error Rate = 0%. |
| **Stage 2 (Moderate Stress)**| **51 – 100 VUs** (51 – 100s) | 20 – 30 RPS | 6 – 10 writes/s | **Ổn định tốt (Stable):** CPU Node.js bắt đầu tăng (40–60%), độ trễ phản hồi vẫn dưới 800ms. |
| **Stage 3 (Saturation Knee)**| **101 – 150 VUs** (101 – 150s)| 35 – 45 RPS | 11 – 15 writes/s| **Điểm Bão Hòa (Knee Point):** Response Time bắt đầu tăng phi tuyến (p95 vượt 2,000ms) do tranh chấp hàng đợi I/O. |
| **Stage 4 (Heavy Stress)** | **151 – 200 VUs** (151 – 200s)| 45 – 55 RPS | 15 – 20 writes/s| **Tiệm cận Điểm Gãy (Near Breaking Point):** SQLite bắt đầu xuất hiện độ trễ khóa ghi; lỗi `SQLITE_BUSY` thỉnh thoảng xuất hiện. |
| **Stage 5 (Extreme Stress)**| **201 – 300 VUs** (201 – 900s)| Dao động mạnh | > 25 writes/s | **Quá tải Cực hạn (Overload / Breaking Point):** Tỷ lệ lỗi vượt 5–10%, Event Loop bị block, p95 vượt 5,000ms. |

---

## 4. Các Chỉ số Đánh giá Hiệu năng (Evaluation Metrics)

Các chỉ số được theo dõi và xuất bản thông qua **Aggregate Report** và công cụ giám sát tài nguyên hệ điều hành:

| Chỉ số Đo lường | Ý nghĩa Kỹ thuật trong Stress Testing | Ngưỡng Bình thường | Ngưỡng Cảnh báo Quá tải |
| :--- | :--- | :--- | :--- |
| **Average Response Time** | Thời gian đáp ứng trung bình của toàn bộ sampler | $< 500\text{ ms}$ | $> 2,500\text{ ms}$ |
| **Median (p50)** | Mức độ trễ mà 50% người dùng trải nghiệm | $< 300\text{ ms}$ | $> 1,500\text{ ms}$ |
| **95th Percentile (p95)** | Độ trễ của 95% yêu cầu (loại bỏ nhiễu cực đoan) | $< 1,200\text{ ms}$ | $> 5,000\text{ ms}$ |
| **99th Percentile (p99)** | Độ trễ của nhóm 1% người dùng chịu ảnh hưởng nặng nhất | $< 2,000\text{ ms}$ | $> 8,000\text{ ms}$ |
| **Throughput (RPS)** | Số lượng yêu cầu HTTP xử lý thành công mỗi giây | Tăng tuyến tính theo VUs | Chững lại hoặc tụt giảm dù VUs tăng |
| **Error Rate (%)** | Tỷ lệ yêu cầu thất bại (HTTP $\ne$ 200 hoặc Assertion fail) | $< 1.0\%$ | $> 5.0\%$ (**Breaking Point**) |
| **CPU Usage (Node.js)** | Mức chiếm dụng CPU của tiến trình `node server.js` | $30\% - 60\%$ | $> 85\%$ liên tục |
| **Memory Usage (Node.js)**| Dung lượng RAM (Resident Set Size - RSS) của Node.js | $< 200\text{ MB}$ | $> 500\text{ MB}$ (Dấu hiệu rò rỉ RAM) |
| **SQLite File Locks** | Tần suất xuất hiện lỗi `SQLITE_BUSY: database is locked` | 0 lần | Xuất hiện liên tục trong log backend |

---

## 5. Xác định Giới hạn & Điểm Gãy Đổ của Hệ thống (Capacity Limits)

Dựa trên phân tích kiến trúc mã nguồn và kiểm nghiệm ban đầu:

1. **Mức tải ổn định tối đa (Maximum Stable Load):**
   * Dự kiến nằm trong khoảng **100 – 120 Virtual Users** đồng thời.
   * Tại mức này, thông lượng đạt khoảng 25 – 30 RPS, SQLite xử lý an toàn ~8 – 10 giao dịch ghi/giây, thời gian phản hồi trung bình < 800ms và không có lỗi phát sinh.

2. **Điểm bão hòa (Knee of the Curve):**
   * Dự kiến xuất hiện tại mốc **~150 Virtual Users**.
   * Dấu hiệu: Thời gian phản hồi bắt đầu tăng vọt từ < 1 giây lên 2.5 – 3 giây. Thông lượng xử lý bắt đầu đi ngang (Plateau) và không tăng thêm được nữa dù số lượng VU tiếp tục gia tăng.

3. **Điểm gãy đổ (Breaking Point / Failure Threshold):**
   * Dự kiến xuất hiện tại mốc **180 – 220 Virtual Users**.
   * Cơ chế gãy đổ: SQLite là cơ sở dữ liệu file đơn với cơ chế Single-Writer lock. Khi có hơn 20 giao dịch ghi đồng thời mỗi giây (`TC_03_Update_Profile` và `TC_08_Checkout`), SQLite không kịp giải phóng lock trong thời gian timeout, dẫn đến lỗi:
     ```
     SQLITE_BUSY: database is locked
     ```
   * Server trả về mã `500 Internal Server Error`, khiến Assertion thất bại và Error Rate vượt ngưỡng 5%.

4. **Dấu hiệu nhận biết hệ thống bị quá tải trầm trọng:**
   * **Node.js Event Loop Lag:** Node.js là đơn luồng (Single-Threaded). Khi hàng trăm kết nối đồng thời xếp hàng chờ I/O SQLite, Event Loop bị phong tỏa (Starvation), thời gian xử lý các request đọc thuần túy (`GET /api/products`) cũng bị kéo dài theo.
   * **Phình to Bộ nhớ RAM (Memory Bloat):** Biến toàn cục `userCarts = {}` trong [backend/server.js#L14](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L14) liên tục nhận dữ liệu `POST /api/cart` nhưng không hề được dọn dẹp sau khi checkout. Trong bài test 300 VUs kéo dài 15 phút, kích thước RAM của tiến trình Node.js sẽ tăng liên tục, dễ dẫn đến hiện tượng Out-Of-Memory.

---

## 6. Xử lý Account Lockout & Cơ chế Reset Hợp lệ

### 6.1 Kiểm tra Giới hạn Đăng nhập từ Mã nguồn Backend
Trong [backend/server.js#L54-L64](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L54-L64):
* Mỗi lần đăng nhập sai, server tăng biến đếm thêm 2: `newAttempts = user.login_attempts + 2`.
* Ngưỡng khóa: `newAttempts >= 3`.
* Thời gian khóa: **180,000 ms = 3 phút**.
* Khi bị khóa, server từ chối request với mã `403 Forbidden` (`"Tài khoản đã bị khóa. Vui lòng thử lại sau."`).

### 6.2 Biện pháp Đảm bảo An toàn trong Stress Test
1. **Dữ liệu tài khoản chính xác 100%:** File `data/users.csv` đã được nạp đầy đủ 502 tài khoản vào `database.sqlite`. Tất cả đều sử dụng mật khẩu hợp lệ `Test1234!`. Tuyệt đối không dùng credentials sai để tạo tải.
2. **Cấu hình CSV Data Set Config cách ly:**
   * `Recycle on EOF = False`: 300 VUs sẽ nhận 300 tài khoản khác nhau trong số 502 tài khoản, không có tình trạng 2 VU dùng chung 1 tài khoản trong cùng thời điểm.
   * `Stop thread on EOF = True`: Nếu hết tài khoản, thread sẽ tự dừng thay vì gửi request lỗi.
3. **Quy trình Reset Mở khóa Tài khoản Giữa Các Lần Test:**
   Nếu vì lý do kỹ thuật (ví dụ dừng giữa chừng hoặc thử nghiệm payload sai) có tài khoản bị khóa, **tuyệt đối không tự ý xóa bảng hay chỉnh sửa mã nguồn backend**. Thay vào đó, hãy thực thi script reset chuyên dụng đã được chuẩn bị sẵn:
   ```bash
   # Mở khóa toàn bộ tài khoản và đưa login_attempts về 0 mà không làm mất dữ liệu
   node scripts/reset_account_lockout.js
   ```

---

## 7. Báo cáo & Listener Chính: Aggregate Report

Theo yêu cầu của bài tập, **Aggregate Report** (`StatVisualizer`) được thiết lập làm View chính trong kịch bản Stress Test [`23120268_Stress_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Stress_20261118.jmx):

### Các Cột Số liệu Quan trọng trong Aggregate Report:
1. **Samples:** Tổng số yêu cầu đã hoàn tất của từng bước nghiệp vụ.
2. **Average:** Thời gian phản hồi trung bình (ms).
3. **Median:** Mốc thời gian phản hồi phân vị 50% (ms).
4. **90% Line, 95% Line, 99% Line:** Các mốc phân vị then chốt để đánh giá sự phân hóa độ trễ khi hệ thống chịu tải cực hạn.
5. **Min / Max:** Thời gian phản hồi nhanh nhất và chậm nhất.
6. **Error %:** Tỷ lệ lỗi phần trăm. Đây là chỉ số quan trọng nhất để xác định Breaking Point (khi Error % bắt đầu tăng vọt trên 5%).
7. **Throughput:** Thông lượng thực tế mà server xử lý được (req/sec).
8. **Received KB/sec:** Tốc độ truyền tải mạng tải về máy kiểm thử.

> [!NOTE]
> Listener `View Results Tree` mặc định bị vô hiệu hóa (`enabled="false"`) trong file JMX để đảm bảo JMeter không bị cạn RAM JVM khi chạy tải 300 VUs.

---

## 8. Đề xuất Điều kiện Dừng Test Khẩn cấp (Abort / Fail-Safe Criteria)

Khi thực thi Stress Test, việc đẩy tải quá đà có thể gây treo hệ điều hành, hỏng file SQLite hoặc kích hoạt Linux OOM-Killer tắt các tiến trình quan trọng. Quá trình kiểm thử cần được **dừng khẩn cấp (Aborted)** nếu chạm phải một trong 5 điều kiện an toàn sau:

| STT | Điều kiện Dừng Khẩn cấp (Abort Trigger) | Cách Nhận diện | Biện pháp Xử lý Ngay |
| :--- | :--- | :--- | :--- |
| **1** | **Tỷ lệ lỗi (Error Rate) vượt quá 15%** liên tục trong 30 giây | Quan sát cột `Err %` trên console JMeter hoặc Aggregate Report | Nhấn `Ctrl + C` hoặc gửi lệnh Shutdown tới JMeter |
| **2** | **Thời gian phản hồi p95 vượt quá 10,000 ms (10 giây)** | Cột `Average` hoặc `95% Line` tăng vọt liên tục | Dừng bài test; ghi nhận mốc VUs hiện tại là vượt quá ngưỡng chịu tải |
| **3** | **Tiến trình Backend Node.js bị crash (Exit)** | Console backend biến mất hoặc trả về mã lỗi tiến trình | Dừng JMeter ngay; kiểm tra `backend.log` để tìm nguyên nhân crash |
| **4** | **RAM khả dụng của máy Host (Available RAM) < 300 MB** | Theo dõi trên `htop` hoặc `free -m` | Dừng JMeter lập tức để tránh đóng băng hệ điều hành |
| **5** | **Lỗi `SQLITE_BUSY` tràn ngập log server** | Console server in liên tục lỗi khóa file | Dừng bài test để SQLite giải phóng file lock |

---

## 9. Hướng dẫn Thực thi Kịch bản Stress Test

### 9.1 Bước 1: Khởi động Backend SUT & Giám sát Hệ thống
Mở Terminal 1 để chạy backend:
```bash
cd backend
node server.js
```

Mở Terminal 2 để theo dõi tài nguyên phần cứng thời gian thực:
```bash
htop
```

### 9.2 Bước 2: Chạy Stress Test Chuẩn (300 VUs, Ramp-up 300s, Duration 900s)
Mở Terminal 3 tại thư mục dự án và thực thi lệnh:
```bash
# Xóa log cũ nếu có
rm -rf 23120268_Stress_20261118.jtl reports/stress_report/

# Chạy Stress Test ở chế độ Non-GUI và tự động sinh HTML Dashboard
/home/hung/26-27/Kiem_thu/ex/per/apache-jmeter-5.6.3/bin/jmeter \
  -n \
  -t 23120268_Stress_20261118.jmx \
  -l 23120268_Stress_20261118.jtl \
  -e -o ./reports/stress_report/
```

### 9.3 Bước 3: Chạy Tùy biến Quy mô Tải (Tùy chọn)
Nhờ cơ chế tham số hóa User Defined Variables (`${__P(threads, ...)}`), bạn có thể dễ dàng điều chỉnh quy mô tải mà không cần sửa file `.jmx`:

* **Chạy thử tải mức vừa (100 VUs trong 5 phút):**
  ```bash
  /home/hung/26-27/Kiem_thu/ex/per/apache-jmeter-5.6.3/bin/jmeter \
    -n -t 23120268_Stress_20261118.jmx \
    -Jthreads=100 -Jrampup=60 -Jduration=300 \
    -l 23120268_Stress_20261118.jtl -e -o ./reports/stress_report/
  ```

* **Chạy thử tìm điểm bão hòa (150 VUs trong 8 phút):**
  ```bash
  /home/hung/26-27/Kiem_thu/ex/per/apache-jmeter-5.6.3/bin/jmeter \
    -n -t 23120268_Stress_20261118.jmx \
    -Jthreads=150 -Jrampup=150 -Jduration=480 \
    -l 23120268_Stress_20261118.jtl -e -o ./reports/stress_report/
  ```
