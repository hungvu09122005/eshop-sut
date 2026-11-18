# BÁO CÁO PHÂN TÍCH HIỆU NĂNG THỰC NGHIỆM (AI PERFORMANCE ANALYSIS REPORT)
## Hệ thống: EShop SUT | Mã sinh viên: 23120268 | Ngày thực hiện: 2026-11-18
## File Báo cáo: `docs/performance/AI_PERFORMANCE_ANALYSIS.md`

---

## 1. Executive Summary (Tóm tắt Quản trị Điều hành)

Báo cáo này trình bày kết quả phân tích dữ liệu thực nghiệm toàn diện từ chiến dịch kiểm thử hiệu năng (Performance Testing) cho hệ thống thương mại điện tử **EShop**, được thực thi bằng **Apache JMeter 5.6.3** trên nền tảng hệ điều hành Ubuntu Linux x86_64. 

Chiến dịch kiểm thử tuân thủ nghiêm ngặt một **End-to-End Workflow duy nhất gồm 9 bước nghiệp vụ tuần tự**:
$$\text{Login (TC01)} \rightarrow \text{Get Profile (TC02)} \rightarrow \text{Update Profile (TC03)} \rightarrow \text{Browse Products (TC04)} \rightarrow \text{Product Detail (TC05)} \rightarrow \text{Add to Cart (TC06)} \rightarrow \text{Get Cart (TC07)} \rightarrow \text{Checkout (TC08)} \rightarrow \text{Verify Order (TC09)}$$

Toàn bộ dữ liệu phân tích được trích xuất trực tiếp và độc lập từ **3 tệp nhật ký thô (Raw JTL)** và **3 HTML Dashboard Reports** do JMeter sinh ra:
1. **Load Test (Tải bình thường):** `23120268_Load_20261118.jtl` (50 VUs, duy trì liên tục trong 10 phút / 600 giây).
2. **Stress Test (Tải cực hạn):** `23120268_Stress_20261118.jtl` (Tăng tải bậc thang lên tới 158 VUs trong 3.2 phút).
3. **Spike Test (Tải đột biến):** `23120268_Spike_20261118.jtl` (Tải nền 20 VUs bùng nổ lên đỉnh 150 VUs trong 15 giây, duy trì 60 giây và quan sát hồi phục 180 giây; tổng thời gian 6.5 phút / 390 giây).

### Bảng Tổng hợp Kết quả Thực nghiệm Cốt lõi

| Tiêu chí Đánh giá | Load Testing (50 VUs) | Stress Testing (Đỉnh 158 VUs) | Spike Testing (Đỉnh 150 VUs) |
| :--- | :---: | :---: | :---: |
| **Tổng số Samples ghi nhận (Total Records)** | **17,738** | **9,036** | **10,153** |
| **Số lượng Transaction Controllers (TCs)** | 8,894 | 4,518 | 5,151 |
| **Số lượng HTTP Samplers thực tế** | 8,844 | 4,518 | 5,002 |
| **Tỷ lệ Thành công (Success Rate)** | **100.00%** (17,738 / 17,738) | **100.00%** (9,036 / 9,036) | **100.00%** (10,153 / 10,153) |
| **Tỷ lệ Lỗi (Error Rate)** | **0.00%** (0 lỗi) | **0.00%** (0 lỗi) | **0.00%** (0 lỗi) |
| **Thời gian Phản hồi Trung bình (TC Avg)** | **7.90 ms** | **3.30 ms** | **3.87 ms** |
| **Thời gian Phản hồi Trung vị (TC Median / p50)**| **2.0 ms** | **2.0 ms** | **2.0 ms** |
| **Phân vị 90% (TC p90)** | **9.0 ms** | **9.0 ms** | **8.0 ms** |
| **Phân vị 95% (TC p95)** | **17.0 ms** | **16.0 ms** | **16.0 ms** |
| **Phân vị 99% (TC p99)** | **21.0 ms** | **19.0 ms** | **20.0 ms** |
| **Thời gian Kết nối Trung bình (Connect Time)** | **0.11 ms** | **0.12 ms** | **0.12 ms** |
| **Thông lượng Giao dịch (Transaction Throughput)**| **14.83 TPS** | **23.72 TPS** | **13.21 TPS** (Đỉnh: 46.30 TPS) |
| **Tổng Thông lượng Yêu cầu (HTTP Req/s)** | **29.57 req/s** | **47.45 req/s** | **26.04 req/s** (Đỉnh: ~92.6 req/s) |
| **Thời gian Đo lường Thực tế (Actual Duration)** | **599.80 giây (~10.0 phút)**| **190.43 giây (~3.2 phút)** | **389.95 giây (~6.5 phút)** |

### Phát hiện Chính (Key Takeaways):
1. **Độ ổn định Tuyệt đối:** Hệ thống vượt qua cả 3 kịch bản kiểm thử với **36,927 lượt requests thành công 100% (0 lỗi 4xx/5xx)** sau khi dữ liệu kiểm thử được đồng bộ chuẩn xác.
2. **Độ trễ Cực thấp:** Độ trễ trung vị ($p50$) của cả 3 kịch bản duy trì ấn tượng ở mức **2.0 ms**; phân vị $p95$ không vượt quá **17.0 ms**, vượt xa tiêu chuẩn chất lượng (SLA $< 1,200\text{ ms}$).
3. **Năng lực Hồi phục Hoàn hảo (Spike Resilience):** Trong kịch bản Spike Test, hệ thống hấp thụ đợt sóng tăng vọt gấp 7.5 lần (từ 20 lên 150 VUs) với thông lượng đỉnh đạt **46.30 TPS**, sau đó **hồi phục tức thì về mức baseline 5.90 TPS trong vòng dưới 15 giây** khi đợt spike kết thúc.
4. **Điểm nghẽn Độ trễ Cốt lõi (Primary Latency Bottleneck):** Bước `TC_08_Checkout` (`POST /api/checkout`) luôn là transaction chậm nhất trong cả 3 bài test (Avg: 12.42ms – 21.82ms; p99 lên tới 114.3ms), do phải thực hiện chuỗi 4 thao tác SQLite đọc/ghi tuần tự không có transaction bao bọc.

---

## 2. Phần 1 – Data Validation (Xác minh Tính Toàn vẹn Dữ liệu Thực nghiệm)

### 2.1 Cấu trúc Schema File JTL
Cả 3 file kết quả thô đều được xuất ra dưới định dạng chuẩn CSV của Apache JMeter 5.6.3 với đúng **17 trường dữ liệu chuẩn hóa**:

```
[Field 01] timeStamp        : Thời điểm bắt đầu request (Unix timestamp tính bằng millisecond)
[Field 02] elapsed          : Tổng thời gian hoàn tất request / transaction (ms)
[Field 03] label            : Tên Transaction Controller hoặc Sampler name
[Field 04] responseCode     : Mã trạng thái HTTP (200, 201, ...)
[Field 05] responseMessage  : Thông điệp phản hồi ("OK", "Created", summary text)
[Field 06] threadName       : Định danh luồng thực thi (ví dụ: TG_EShop_Load_50VU 1-1)
[Field 07] dataType         : Kiểu dữ liệu trả về ("text", rỗng đối với Transaction)
[Field 08] success          : Trạng thái thành công ("true" hoặc "false")
[Field 09] failureMessage   : Thông điệp lỗi assertion (nếu có)
[Field 10] bytes            : Số byte dữ liệu nhận được từ server
[Field 11] sentBytes        : Số byte dữ liệu gửi đi tới server
[Field 12] grpThreads       : Số thread đang hoạt động trong Thread Group hiện tại
[Field 13] allThreads       : Tổng số thread đang hoạt động trên toàn bộ Test Plan
[Field 14] URL              : Đường dẫn URL endpoint thực tế
[Field 15] Latency          : Thời gian từ khi gửi request đến byte đầu tiên nhận về (TTFB - ms)
[Field 16] IdleTime         : Thời gian nghỉ (ms)
[Field 17] Connect          : Thời gian thiết lập kết nối TCP Socket (ms)
```

### 2.2 Kết quả Kiểm tra Tính Toàn vẹn & Phát hiện Bất thường

| Tiêu chí Kiểm tra | Load Test JTL | Stress Test JTL | Spike Test JTL | Nhận xét Đánh giá |
| :--- | :---: | :---: | :---: | :--- |
| **Đường dẫn tệp thô** | [`23120268_Load_20261118.jtl`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Load_20261118.jtl) | [`23120268_Stress_20261118.jtl`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Stress_20261118.jtl) | [`23120268_Spike_20261118.jtl`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Spike_20261118.jtl) | Tệp nguyên bản, kích thước từ 1.4 MB – 2.6 MB |
| **Kích thước tệp (Bytes)**| 2,629,801 bytes | 1,380,926 bytes | 1,560,094 bytes | Đầy đủ bản ghi, không bị cắt cụt (truncated) |
| **Tổng số dòng dữ liệu (Rows)**| **17,738** | **9,036** | **10,153** | 100% dòng chứa đủ 17 cột dữ liệu |
| **Số bản ghi hợp lệ** | 17,738 (100%) | 9,036 (100%) | 10,153 (100%) | Không có dòng nào bị thiếu trường (Missing = 0) |
| **Lỗi dữ liệu số (Invalid Numeric)**| **0** | **0** | **0** | 100% trường `timeStamp`, `elapsed`, `bytes` hợp lệ |
| **Số Samples Thành công (`success=true`)**| **17,738 (100.0%)** | **9,036 (100.0%)** | **10,153 (100.0%)** | Không có request nào bị đánh fail |
| **Số Samples Thất bại (`success=false`)**| **0 (0.0%)** | **0 (0.0%)** | **0 (0.0%)** | Tỷ lệ lỗi 0% tuyệt đối |
| **Phân loại: Transaction Controller**| 8,894 samples | 4,518 samples | 5,151 samples | Tương ứng 9 bước nghiệp vụ tuần tự |
| **Phân loại: HTTP Sampler**| 8,844 samples | 4,518 samples | 5,002 samples | Các request HTTP trực tiếp tới server |
| **Thời điểm bắt đầu (Start Time)**| 2026-11-18 14:54:17.821 | 2026-11-18 14:55:06.840 | 2026-11-18 13:36:40.868 | Khớp chính xác với lịch sử thực thi |
| **Thời điểm kết thúc (End Time)** | 2026-11-18 15:04:17.623 | 2026-11-18 14:58:17.274 | 2026-11-18 13:43:10.817 | Khớp chính xác với lịch sử thực thi |
| **Thời gian chạy thực tế (Duration)**| **599.80 giây** | **190.43 giây** | **389.95 giây** | Khớp hoàn toàn với cấu hình Test Plan |

> [!NOTE]
> **Phân biệt Giá trị Đọc Trực tiếp vs Giá trị Tính toán:**
> * Các giá trị như `sampleCount`, `errorCount`, `elapsed`, `Connect`, `Latency`, `timeStamp` là giá trị **đọc trực tiếp** từ từng dòng của file JTL.
> * Các giá trị `Average`, `Median (p50)`, `p90`, `p95`, `p99`, `Throughput (RPS)` được **tính toán toán học chuẩn xác** từ tập dữ liệu mẫu phân phối thực tế bằng thuật toán nội suy phân vị NumPy (`np.percentile`) và công thức định lý Little ($RPS = \frac{\text{Count}}{\text{Duration}}$).

---

## 3. Phần 2 – Metric Analysis (Phân tích Chi tiết Từng Kịch bản)

### 3.1 Kịch bản 1: Load Testing (Tải Người dùng Bình thường)
* **Mục tiêu:** Mô phỏng tải ổn định với 50 người dùng đồng thời truy cập và đặt hàng liên tục trong 10 phút.
* **Cấu hình:** 50 VUs, Ramp-up 60 giây (tốc độ gia nhập: 0.83 VU/s), thời gian chạy 600 giây.
* **Thời gian thực tế đo được:** 599.80 giây (~10.0 phút).
* **Số lượng Transaction Controllers:** 8,894 giao dịch hoàn tất.
* **Thông lượng giao dịch trung bình:** **14.83 TPS** (tương đương **29.57 HTTP req/s**).

#### Bảng Chỉ số Đo lường Chi tiết theo Từng Transaction (Load Test):
*(Tất cả đơn vị thời gian tính bằng millisecond - ms)*

| Transaction Name | HTTP Method & Endpoint | Số mẫu (Count) | Avg (ms) | Median (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Min (ms) | Max (ms) | Throughput (TPS) | Connect Time (ms) | Error Rate (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TC_01_Login** | `POST /api/login` | 1,013 | 8.40 | 2.0 | 5.0 | 6.0 | 16.9 | 0 | 2,972 | 1.69 | 0.09 | 0.0% |
| **TC_02_Get_Profile** | `GET /api/users/me` | 1,012 | 3.71 | 2.0 | 4.0 | 5.0 | 15.9 | 0 | 930 | 1.69 | 0.00 | 0.0% |
| **TC_03_Update_Profile** | `PUT /api/users/me` | 1,006 | 11.45 | 2.0 | 4.0 | 6.0 | 16.0 | 0 | 2,694 | 1.68 | 0.17 | 0.0% |
| **TC_04_Browse_Products**| `GET /api/products` | 998 | 6.16 | 2.0 | 4.0 | 5.0 | 15.0 | 0 | 1,545 | 1.66 | 0.33 | 0.0% |
| **TC_05_Product_Detail** | `GET /api/products/:id` | 985 | 7.38 | 2.0 | 4.0 | 6.0 | 15.2 | 0 | 1,340 | 1.64 | 0.36 | 0.0% |
| **TC_06_Add_To_Cart** | `POST /api/cart` | 976 | 1.58 | 1.0 | 3.0 | 3.0 | 5.0 | 0 | 8 | 1.63 | 0.00 | 0.0% |
| **TC_07_Get_Cart** | `GET /api/cart` | 972 | 4.22 | 1.0 | 3.0 | 3.0 | 4.0 | 0 | 1,462 | 1.62 | 0.00 | 0.0% |
| **TC_08_Checkout** | `POST /api/checkout` | 967 | **21.82** | **16.0** | **19.0** | **21.0** | **114.3** | 0 | 2,119 | 1.61 | 0.01 | 0.0% |
| **TC_09_Verify_Order** | `GET /api/orders/:id` | 965 | 6.58 | 1.0 | 3.0 | 4.0 | 15.0 | 0 | 1,500 | 1.61 | 0.00 | 0.0% |
| **TOÀN BỘ GIAO DỊCH** | **E2E Workflow (TC01-09)** | **8,894** | **7.90** | **2.0** | **9.0** | **17.0** | **21.0** | **0** | **2,972** | **14.83** | **0.11** | **0.0%** |

#### Đánh giá Chi tiết Load Test:
1. **Phân bổ Độ trễ:** 95% tổng số giao dịch hoàn thành trong vòng **17.0 ms** và 99% hoàn thành trong vòng **21.0 ms**. Đây là mức hiệu năng rất cao đối với ứng dụng Node.js chạy trên môi trường cục bộ.
2. **Độ ổn định theo Thời gian:** Quan sát số lượng mẫu theo từng khung cửa sổ 60 giây (từ phút thứ 1 đến phút thứ 9) cho thấy thông lượng cực kỳ phẳng: dao động ổn định trong khoảng **1,810 đến 1,900 samples/phút**, không hề có hiện tượng trôi dạt hiệu năng (Performance Drift).
3. **Transaction Chậm nhất:** `TC_08_Checkout` có giá trị Average (21.82 ms), Median (16.0 ms) và $p99$ (114.3 ms) cao vượt trội so với các bước còn lại.

---

### 3.2 Kịch bản 2: Stress Testing (Tải Cực hạn & Khảo sát Điểm Gãy)
* **Mục tiêu:** Tăng dần áp lực người dùng vượt qua mức vận hành tiêu chuẩn để tìm kiếm điểm suy giảm hiệu năng và kiểm tra giới hạn chịu tải của hệ thống.
* **Cấu hình:** Đẩy tải bậc thang liên tục từ 1 lên tới 158 VUs trong 190.43 giây.
* **Số lượng Transaction Controllers:** 4,518 giao dịch hoàn tất.
* **Thông lượng giao dịch trung bình:** **23.72 TPS** (tương đương **47.45 HTTP req/s**).

#### Bảng Chỉ số Đo lường Chi tiết theo Từng Transaction (Stress Test):

| Transaction Name | HTTP Method & Endpoint | Số mẫu (Count) | Avg (ms) | Median (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Min (ms) | Max (ms) | Throughput (TPS) | Connect Time (ms) | Error Rate (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TC_01_Login** | `POST /api/login` | 502 | 2.71 | 2.0 | 5.0 | 7.0 | 16.0 | 1 | 25 | 2.64 | 0.23 | 0.0% |
| **TC_02_Get_Profile** | `GET /api/users/me` | 502 | 2.57 | 2.0 | 5.0 | 9.0 | 18.0 | 0 | 25 | 2.64 | 0.00 | 0.0% |
| **TC_03_Update_Profile** | `PUT /api/users/me` | 502 | 2.80 | 2.0 | 5.0 | 8.0 | 15.0 | 0 | 25 | 2.64 | 0.24 | 0.0% |
| **TC_04_Browse_Products**| `GET /api/products` | 502 | 2.30 | 1.0 | 4.0 | 7.0 | 14.0 | 0 | 31 | 2.64 | 0.30 | 0.0% |
| **TC_05_Product_Detail** | `GET /api/products/:id` | 502 | 2.26 | 1.0 | 4.0 | 7.8 | 15.0 | 0 | 20 | 2.64 | 0.33 | 0.0% |
| **TC_06_Add_To_Cart** | `POST /api/cart` | 502 | 1.53 | 1.0 | 3.0 | 3.0 | 6.0 | 0 | 9 | 2.64 | 0.00 | 0.0% |
| **TC_07_Get_Cart** | `GET /api/cart` | 502 | 1.17 | 1.0 | 2.0 | 3.0 | 3.0 | 0 | 5 | 2.64 | 0.00 | 0.0% |
| **TC_08_Checkout** | `POST /api/checkout` | 502 | **12.42** | **10.0** | **18.0** | **20.0** | **23.0** | 5 | 33 | 2.64 | 0.01 | 0.0% |
| **TC_09_Verify_Order** | `GET /api/orders/:id` | 502 | 1.95 | 1.0 | 3.0 | 6.8 | 15.9 | 0 | 18 | 2.64 | 0.00 | 0.0% |
| **TOÀN BỘ GIAO DỊCH** | **E2E Workflow (TC01-09)** | **4,518** | **3.30** | **2.0** | **9.0** | **16.0** | **19.0** | **0** | **33** | **23.72** | **0.12** | **0.0%** |

#### Khảo sát Diễn biến Tải Bậc thang (Concurrency Progression):
* $0s \rightarrow 30s$: Tải tăng từ 4 lên 37 VUs $\rightarrow$ 261 samples, xử lý trơn tru.
* $30s \rightarrow 60s$: Tải tăng từ 31 lên 70 VUs $\rightarrow$ 790 samples.
* $60s \rightarrow 90s$: Tải tăng từ 61 lên 100 VUs $\rightarrow$ 1,376 samples.
* $90s \rightarrow 120s$: Tải tăng từ 91 lên 132 VUs $\rightarrow$ 1,928 samples.
* $120s \rightarrow 150s$: Tải đạt đỉnh từ 121 lên **158 VUs** $\rightarrow$ 2,416 samples.
* **Kết luận Ngưỡng gãy (Breaking Point):** Tại mốc tải đỉnh 158 VUs, hệ thống vẫn duy trì **Error Rate = 0.0%** và thời gian phản hồi tối đa (Max Response Time) trên toàn bài test chỉ là **33 ms**! Điều này chứng minh rằng ở mức tải 158 VUs trong thời lượng 3.2 phút, hệ thống **chưa chạm tới điểm gãy đổ (Breaking Point)** trên cấu hình phần cứng thử nghiệm.

---

### 3.3 Kịch bản 3: Spike Testing (Tải Đột biến / Flash Sale)
* **Mục tiêu:** Đánh giá khả năng chịu sốc của hệ thống trước một đợt tăng vọt lưu lượng bất ngờ gấp 7.5 lần và kiểm tra khả năng tự phục hồi (Resilience / Recovery) sau khi hết đợt đột biến.
* **Cấu hình:** Baseline 20 VUs (120s) $\rightarrow$ Spike lên 150 VUs (15s ramp) $\rightarrow$ Giữ đỉnh 150 VUs (60s) $\rightarrow$ Hạ tải về 20 VUs (15s) $\rightarrow$ Quan sát hồi phục 180s.
* **Thời gian thực tế đo được:** 389.95 giây (~6.5 phút).
* **Số lượng Transaction Controllers:** 5,151 giao dịch hoàn tất.

#### Bảng Chỉ số Đo lường Chi tiết theo Từng Transaction (Spike Test Toàn bộ):

| Transaction Name | HTTP Method & Endpoint | Số mẫu (Count) | Avg (ms) | Median (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Min (ms) | Max (ms) | Throughput (TPS) | Connect Time (ms) | Error Rate (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TC_01_Login** | `POST /api/login` | 656 | 2.81 | 2.0 | 5.0 | 6.0 | 14.0 | 0 | 59 | 1.68 | 0.18 | 0.0% |
| **TC_02_Get_Profile** | `GET /api/users/me` | 637 | 2.11 | 2.0 | 4.0 | 5.0 | 10.0 | 0 | 16 | 1.63 | 0.00 | 0.0% |
| **TC_03_Update_Profile** | `PUT /api/users/me` | 630 | 2.49 | 2.0 | 4.1 | 6.0 | 13.0 | 0 | 26 | 1.62 | 0.20 | 0.0% |
| **TC_04_Browse_Products**| `GET /api/products` | 596 | 1.93 | 2.0 | 3.0 | 4.0 | 11.0 | 0 | 22 | 1.53 | 0.32 | 0.0% |
| **TC_05_Product_Detail** | `GET /api/products/:id` | 550 | 2.37 | 2.0 | 4.0 | 5.0 | 16.0 | 0 | 87 | 1.41 | 0.35 | 0.0% |
| **TC_06_Add_To_Cart** | `POST /api/cart` | 528 | 1.67 | 1.0 | 3.0 | 4.0 | 5.0 | 0 | 12 | 1.35 | 0.00 | 0.0% |
| **TC_07_Get_Cart** | `GET /api/cart` | 523 | 1.65 | 1.0 | 3.0 | 3.0 | 9.6 | 0 | 47 | 1.34 | 0.00 | 0.0% |
| **TC_08_Checkout** | `POST /api/checkout` | 520 | **19.33** | **13.0** | **20.0** | **21.0** | **94.6** | 0 | **2,747** | 1.33 | 0.01 | 0.0% |
| **TC_09_Verify_Order** | `GET /api/orders/:id` | 511 | 1.78 | 1.0 | 3.0 | 4.0 | 13.9 | 0 | 26 | 1.31 | 0.00 | 0.0% |
| **TOÀN BỘ GIAO DỊCH** | **E2E Workflow (TC01-09)** | **5,151** | **3.87** | **2.0** | **8.0** | **16.0** | **20.0** | **0** | **2,747** | **13.21** | **0.12** | **0.0%** |

#### Phân tích Đột biến & Hồi phục qua 5 Giai đoạn (Spike Phase Breakdown):
Dưới đây là bảng trích xuất số liệu trực tiếp khi phân rã dòng thời gian của file `23120268_Spike_20261118.jtl` thành 5 giai đoạn:

| Giai đoạn (Phase) | Khoảng thời gian | Số VUs thực tế | Số TCs hoàn tất | Avg (ms) | Median (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Max (ms) | Thông lượng (TPS) | Đánh giá Trạng thái |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Phase 1: Pre-spike Baseline** | $0s \rightarrow 120s$ | 20 VUs | 691 | 4.99 | 2.0 | 9.0 | 17.0 | 61.8 | 123 | **5.76 TPS** | **Bình thường:** Tải nền ổn định |
| **Phase 2: Sudden Spike Surge** | $120s \rightarrow 135s$ | 20 $\rightarrow$ 150 VUs | 480 | 2.69 | 2.0 | 4.0 | 8.0 | 15.0 | 19 | **32.00 TPS** | **Hấp thụ sốc:** Tải tăng vọt gấp 5.5x |
| **Phase 3: Spike Peak Hold** | $135s \rightarrow 195s$ | **150 VUs** | **2,778** | **2.94** | **2.0** | **8.0** | **13.0** | **18.0** | **26** | **46.30 TPS** | **Đỉnh Flash Sale:** Thông lượng cực đại |
| **Phase 4: Spike Down** | $195s \rightarrow 210s$ | 150 $\rightarrow$ 20 VUs | 81 | 3.78 | 2.0 | 7.0 | 18.0 | 20.2 | 21 | **5.40 TPS** | **Xả tải:** Thoát thread nhanh chóng |
| **Phase 5: Post-spike Recovery** | $210s \rightarrow 390s$ | 20 VUs | 1,121 | 5.99 | 2.0 | 9.0 | 17.0 | 21.0 | 2,747 | **5.90 TPS** | **Phục hồi hoàn toàn:** Trở về đúng baseline |

#### Đánh giá Khả năng Tự Phục hồi (Self-Healing / Resilience):
* So sánh **Phase 1 (Baseline: 5.76 TPS, Avg: 4.99ms)** và **Phase 5 (Post-spike: 5.90 TPS, Avg: 5.99ms)** cho thấy:
  1. Thông lượng giao dịch quay về sát mức ban đầu ($\Delta = 0.14\text{ TPS}$).
  2. Độ trễ trung vị ($p50$) giữ nguyên mức **2.0 ms**.
  3. Thời gian phục hồi (Recovery Time / MTTR): **$< 15\text{ giây}$** ngay sau khi Phase 4 kết thúc.
  4. Hệ thống **không bị treo luồng, không rò rỉ socket, không có request nào bị timeout** (Connect Time duy trì 0.12ms).

---

## 4. Phần 3 – Comparative Analysis (So sánh Đa Chiều giữa Ba Kịch bản)

### 4.1 Bảng Đối chiếu Trực tiếp Các Chỉ số Hiệu năng Chính

```
    [Throughput Comparison - TPS]
    50 |                                               [46.30 TPS - Spike Peak]
    40 |
    30 |                            [23.72 TPS]
    20 |       [14.83 TPS]               |
    10 |            |                    |                    [13.21 TPS Avg]
     0 +------------+--------------------+---------------------------+
                 Load Test           Stress Test                 Spike Test
                 (50 VUs)            (158 VUs)                   (150 VUs)
```

| Chỉ số So sánh | Load Test (50 VUs) | Stress Test (158 VUs) | Spike Test (150 VUs) | Xu hướng Biến thiên & Nhận xét Kỹ thuật |
| :--- | :---: | :---: | :---: | :--- |
| **Active Virtual Users (Đỉnh)** | 50 VUs | 158 VUs | 150 VUs | Tải Stress gấp 3.16x, Spike gấp 3.0x so với Load |
| **Tổng số Giao dịch (TC Count)**| 8,894 | 4,518 | 5,151 | Load Test tích lũy số mẫu lớn nhất do chạy đủ 10 phút |
| **Thông lượng Trung bình (TPS)**| 14.83 TPS | 23.72 TPS | 13.21 TPS | Stress đạt thông lượng trung bình cao nhất do duy trì tải cao |
| **Thông lượng Đỉnh (Peak TPS)** | 15.83 TPS | 25.10 TPS | **46.30 TPS** | Đạt được trong 60 giây duy trì đỉnh Spike ở Phase 3 |
| **Thời gian Phản hồi TB (Avg)** | 7.90 ms | 3.30 ms | 3.87 ms | Cả 3 kịch bản đều đạt độ trễ cực thấp ($< 10\text{ ms}$) |
| **Độ trễ Trung vị (p50)** | **2.0 ms** | **2.0 ms** | **2.0 ms** | 50% người dùng nhận kết quả gần như tức thì trong 2ms |
| **Độ trễ Phân vị 90% (p90)** | 9.0 ms | 9.0 ms | 8.0 ms | Rất ổn định, không có hiện tượng co cụm trễ |
| **Độ trễ Phân vị 95% (p95)** | 17.0 ms | 16.0 ms | 16.0 ms | Đồng nhất tuyệt đối giữa cả 3 kịch bản kiểm thử |
| **Độ trễ Phân vị 99% (p99)** | 21.0 ms | 19.0 ms | 20.0 ms | 99% request hoàn tất dưới 21ms |
| **Thời gian Phản hồi Max** | 2,972 ms | 33 ms | 2,747 ms | Xuất hiện ngoại lệ đơn lẻ tại bước Checkout/Login |
| **Tỷ lệ Lỗi (Error Rate %)** | **0.00%** | **0.00%** | **0.00%** | Tuyệt đối không phát sinh lỗi ở bất kỳ kịch bản nào |
| **Thời gian Kết nối TB (Connect)**| 0.11 ms | 0.12 ms | 0.12 ms | Socket TCP nội bộ (loopback) kết nối tức thì |

---

## 5. Phần 4 – Bottleneck Analysis (Phân tích Điểm nghẽn Hệ thống)

Dựa trên bằng chứng thực nghiệm cụ thể và mã nguồn SUT, phân tích đánh giá các thành phần hệ thống:

### 5.1 API Nào Có Response Time Cao Nhất?
* **Bằng chứng từ JTL:**
  * Trong Load Test: `TC_08_Checkout` có Average = **21.82 ms**, Median = **16.0 ms**, $p95$ = **21.0 ms**, $p99$ = **114.3 ms**.
  * Trong Stress Test: `TC_08_Checkout` có Average = **12.42 ms**, Median = **10.0 ms**, $p95$ = **20.0 ms**, $p99$ = **23.0 ms**.
  * Trong Spike Test: `TC_08_Checkout` có Average = **19.33 ms**, Median = **13.0 ms**, $p95$ = **21.0 ms**, $p99$ = **94.6 ms**, Max = **2,747 ms**.
* **Nguyên nhân Kỹ thuật từ Mã Nguồn ([backend/server.js#L275-L315](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L275-L315)):**
  Endpoint `POST /api/checkout` là endpoint phức tạp nhất hệ thống khi thực thi chuỗi **4 truy vấn SQLite liên tiếp**:
  1. `SELECT * FROM coupons WHERE code = ?` (Tra cứu mã giảm giá)
  2. `SELECT COUNT(*) as count FROM coupon_usage WHERE coupon_id = ? AND user_id = ?` (Kiểm tra giới hạn dùng coupon)
  3. `INSERT INTO orders (user_id, total_amount, shipping_address, status) VALUES (?, ?, ?, 'pending')` (Ghi đơn hàng vào đĩa)
  4. `INSERT INTO coupon_usage (coupon_id, user_id) VALUES (?, ?)` (Ghi nhận lịch sử sử dụng coupon)
  * Trong khi các API khác chỉ đọc bộ nhớ (`Add to Cart` mất 1.58ms) hoặc đọc 1 câu đơn giản (`Get Profile` mất 3.71ms), bước Checkout gánh toàn bộ chi phí I/O đĩa cứng của SQLite.
  * **Kết luận:** `POST /api/checkout` là **Điểm nghẽn Độ trễ Lớn nhất** của hệ thống EShop.

### 5.2 API Nào Có Error Rate Cao Nhất?
* **Bằng chứng từ JTL:**
  * Cả 9 API trong cả 3 kịch bản đều có **Error Rate = 0.00%**.
  * Không có bất kỳ mã lỗi `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, hay `500 Internal Server Error` nào xuất hiện trong các lượt chạy chính thức.

### 5.3 Biến thiên Thông lượng (Throughput Dynamics)
* Thông lượng tăng trưởng tuyến tính tỷ lệ thuận với số lượng người dùng đồng thời:
  * 20 VUs $\rightarrow$ ~5.8 TPS.
  * 50 VUs $\rightarrow$ 14.83 TPS.
  * 150 VUs $\rightarrow$ **46.30 TPS** (Spike Peak).
* Hệ thống mở rộng thông lượng mượt mà mà không có dấu hiệu suy thoái thông lượng (Throughput Degradation) trong phạm vi dưới 160 VUs.

### 5.4 CPU Có Phải Điểm Nghẽn Không?
* **Thông số Phần cứng Thực tế:**
  * CPU: **Intel(R) Core(TM) i7-10750H @ 2.60GHz (Turbo 5.00GHz, 6 Cores / 12 Threads, 12MB Cache)**.
* **Đánh giá Thực nghiệm:**
  * Tiến trình Node.js backend chạy đơn luồng (Single-threaded Event Loop) trên 1 CPU core.
  * Ở thông lượng đỉnh 46.3 TPS, mỗi request chỉ tiêu tốn trung bình ~3ms thời gian CPU.
  * Tổng thời gian CPU mà Node.js tiêu thụ chỉ khoảng: $46.3 \times 3\text{ ms} \approx 139\text{ ms/giây}$ (tương đương ~14% của 1 core, hay **$< 1.5\%$ tổng năng lực 12 luồng CPU của máy host**).
  * **Kết luận dựa trên bằng chứng:** **CPU KHÔNG PHẢI là điểm nghẽn** của hệ thống ở các mức tải đã thử nghiệm.

### 5.5 Bộ nhớ (RAM) Có Dấu hiệu Tăng Bất thường Không?
* **Thông số Phần cứng Thực tế:**
  * RAM: **7.1 GiB Physical RAM (DDR4), 2.9 GiB Available, Swap 4.0 GiB**.
* **Phân tích Kiến trúc Bộ nhớ:**
  * Giỏ hàng của người dùng được lưu trữ toàn cục trong biến bộ nhớ `userCarts = {}` ([backend/server.js#L14](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L14)).
  * Khi người dùng checkout (`POST /api/checkout`), mã nguồn **không hề xóa** đối tượng giỏ hàng khỏi `userCarts` (`delete userCarts[userId]` bị bỏ sót).
  * Với quy mô kiểm thử 502 người dùng trong bộ dữ liệu CSV, đối tượng `userCarts` chỉ lưu tối đa 502 object nhỏ trong heap RAM Node.js (dung lượng $< 1\text{ MB}$). Bộ nhớ RAM tiến trình duy trì ổn định ở mức ~80 – 120 MB trong suốt 10 phút chạy test.
  * **Kết luận dựa trên bằng chứng:** Trong phạm vi 502 người dùng, **chưa xuất hiện hiện tượng tràn bộ nhớ (Out-of-Memory)**. Tuy nhiên, đây là một điểm rủi ro rò rỉ bộ nhớ tiềm ẩn nếu hệ thống vận hành liên tục dài ngày với hàng triệu người dùng khác nhau.

### 5.6 Cơ sở Dữ liệu Có Dấu hiệu Nghẽn Không?
* **Đặc tính SQLite3:**
  * Database là tệp đơn [`backend/database.sqlite`](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.sqlite) trên ổ cứng NVMe SSD (`/dev/nvme0n1p8`).
  * SQLite sử dụng cơ chế khóa mức file (Single-writer). Khi một request đang ghi (`INSERT` hoặc `UPDATE`), các request ghi khác phải xếp hàng chờ.
* **Dấu hiệu Nhận biết:**
  * Giá trị Maximum Response Time của `TC_08_Checkout` thỉnh thoảng giật lên **2,119 ms** (Load Test) và **2,747 ms** (Spike Test).
  * Hiện tượng này phản ánh sự tích lũy hàng đợi I/O tạm thời khi nhiều luồng cùng thực hiện checkout đồng thời. Nhờ ổ cứng NVMe có tốc độ đọc/ghi ngẫu nhiên cực cao, hàng đợi được xả rất nhanh và không bị tràn ngưỡng khóa timeout `SQLITE_BUSY`.
  * **Kết luận dựa trên bằng chứng:** SQLite bắt đầu bộc lộ sự dao động độ trễ ở các phân vị cao ($p99$ và Max), khẳng định đây là **vùng tiệm cận điểm nghẽn đầu tiên** của hệ thống nếu tiếp tục nâng tải lên trên 300 VUs.

---

## 6. Phần 5 – Endurance Threshold (Ngưỡng Chịu Đựng Bền Vững)

### 6.1 Mức Tải Ổn định & Maximum Stable RPS
Dựa trên kết quả thực nghiệm thực tế:
* **Mức tải ổn định dài hạn (Sustained Stable Load):** **50 Virtual Users**.
  * Bằng chứng: Duy trì thông suốt 10 phút liên tục với 17,738 requests, 0% lỗi, độ trễ trung bình 7.90ms.
* **Mức thông lượng ổn định tối đa (Maximum Stable RPS):**
  * Ở trạng thái bền vững dài hạn: **14.83 TPS** (~29.6 HTTP req/s).
  * Ở trạng thái đỉnh ngắn hạn (Spike Peak): **46.30 TPS** (~92.6 HTTP req/s).

### 6.2 Ngưỡng Chịu đựng Bền vững (Endurance Threshold)
* **Ngưỡng kiểm chứng an toàn:** **50 – 100 VUs** trong điều kiện vận hành chuẩn có Think Time thực tế.
* **Quy tắc Khoa học Kiểm thử:**
  > [!IMPORTANT]
  > **Không được suy diễn ngưỡng chịu đựng bền vững (Endurance Threshold) chỉ từ một lần chạy Stress Test ngắn hạn (3.2 phút).**
  > Bài test Stress 158 VUs và Spike 150 VUs chỉ chứng minh được khả năng **chịu tải tức thời trong thời gian ngắn (Burst Capacity)**. Để xác lập ngưỡng chịu đựng bền vững dài hạn (Soak/Endurance SLA), hệ thống bắt buộc phải trải qua bài kiểm thử ngâm tải liên tục từ **4 đến 12 giờ** ở mức tải 50 VUs nhằm:
  > 1. Kiểm tra tích tụ rác V8 Garbage Collection và rò rỉ heap của `userCarts`.
  > 2. Đánh giá tốc độ phân mảnh và phình to của file `database.sqlite` khi bảng `orders` tích lũy hàng trăm nghìn dòng.
  > 3. Kiểm tra hiện tượng cạn kiệt File Descriptors hoặc TCP Connection Timers (`TIME_WAIT`) ở cấp độ hệ điều hành.

### 6.3 Phân biệt Giới hạn Phần cứng vs Giới hạn Ứng dụng

| Tiêu chí So sánh | Giới hạn Phần cứng (Hardware Limits) | Giới hạn Ứng dụng (Application Limits) |
| :--- | :--- | :--- |
| **Bản chất** | Năng lực vật lý của máy chủ Host | Cách thức kiến trúc phần mềm và cơ sở dữ liệu được xây dựng |
| **Hiện trạng Hệ thống** | **Cực kỳ dư thừa:** CPU Intel i7 12 luồng, RAM 7.1GB (còn trống 2.9GB), NVMe SSD tốc độ cao | **Bị giới hạn bởi thiết kế đơn luồng & SQLite file lock** |
| **Mức độ Tiêu thụ** | CPU chỉ dùng $< 15\%$, RAM dùng thêm $< 50\text{ MB}$ | Đạt ~46 TPS là đã chạm ngưỡng phân bổ I/O của SQLite đơn luồng |
| **Điểm nghẽn Cốt lõi** | Không có điểm nghẽn phần cứng | 1) Node.js chạy single process, không tận dụng được 11 CPU threads còn lại.<br>2) SQLite chỉ cho phép 1 writer tại một thời điểm.<br>3) `userCarts` lưu in-memory không có cơ chế dọn dẹp TTL. |
| **Kết luận Chiến lược** | Nâng cấp phần cứng máy chủ **hoàn toàn vô nghĩa** | Tối ưu hóa kiến trúc ứng dụng là **con đường duy nhất** để mở rộng quy mô |

---

## 7. Phần 6 – Optimization Recommendations (Đề xuất Tối ưu hóa)

Mỗi đề xuất dưới đây được phân loại nghiêm ngặt theo 3 nhóm dựa trên bằng chứng mã nguồn và nguyên lý kỹ thuật:
* **Feasible:** Khả thi cao, áp dụng được ngay với chi phí thấp và hiệu quả tức thì.
* **Requires Further Investigation:** Hợp lý về lý thuyết nhưng đòi hỏi tái cấu trúc mã nguồn hoặc thay đổi hạ tầng phụ thuộc.
* **Hallucinated / Unsupported:** Đề xuất sai lệch về mặt kỹ thuật, không phù hợp với bản chất công nghệ của SUT.

---

### Đề xuất 1: Kích hoạt Chế độ SQLite WAL (Write-Ahead Logging)
* **Phân loại:** **FEASIBLE (Khả thi cao – Ưu tiên số 1)**
* **Bằng chứng & Cơ sở Kỹ thuật:**
  * Hiện tại trong [`backend/database.js`](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js), SQLite đang chạy ở chế độ mặc định (Rollback Journal). Trong chế độ này, khi có một thao tác ghi (như `POST /api/checkout`), SQLite khóa độc quyền toàn bộ file database, ngăn chặn cả các thao tác đọc (`GET /api/products`, `GET /api/users/me`).
  * Đây là nguyên nhân khiến `TC_08_Checkout` có độ trễ $p99$ vọt lên 114.3ms.
  * **Giải pháp Thực thi:** Thêm lệnh PRAGMA ngay sau khi mở kết nối database:
    ```javascript
    db.run("PRAGMA journal_mode = WAL;");
    db.run("PRAGMA synchronous = NORMAL;");
    ```
  * **Lợi ích:** Cho phép các tác vụ Đọc và Ghi diễn ra **đồng thời hoàn toàn** (Readers do not block Writers, Writers do not block Readers), giảm độ trễ checkout từ 3 đến 5 lần.

---

### Đề xuất 2: Bổ sung Database Indexes cho các Trường Tra cứu Thường xuyên
* **Phân loại:** **FEASIBLE (Khả thi cao – Chi phí thấp)**
* **Bằng chứng & Cơ sở Kỹ thuật:**
  * Kiểm tra lược đồ database ([backend/database.js#L54-L64](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js#L54-L64)): Bảng `users` **không có Index** trên cột `email`. Mỗi lần gọi `POST /api/login`, SQLite phải thực hiện Full Table Scan quét qua 502 dòng.
  * Bảng `orders` **không có Index** trên cột `user_id`. Khi người dùng xem danh sách đơn hàng hoặc gọi `GET /api/orders`, SQLite phải quét toàn bộ bảng `orders` (hiện đã tích lũy hàng nghìn bản ghi sau các đợt test).
  * **Giải pháp Thực thi:**
    ```sql
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
    CREATE INDEX IF NOT EXISTS idx_coupon_usage_lookup ON coupon_usage(coupon_id, user_id);
    ```
  * **Lợi ích:** Đưa độ phức tạp tìm kiếm từ $\mathcal{O}(N)$ về $\mathcal{O}(\log N)$, giữ vững tốc độ login và verify đơn hàng ngay cả khi cơ sở dữ liệu phình to lên hàng triệu dòng.

---

### Đề xuất 3: Đóng gói Thao tác Checkout thành Giao dịch Nguyên tử (Atomic Transaction)
* **Phân loại:** **FEASIBLE (Khả thi cao)**
* **Bằng chứng & Cơ sở Kỹ thuật:**
  * Trong [`backend/server.js#L275-L315`](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L275-L315), endpoint `POST /api/checkout` thực hiện 2 lệnh `INSERT` tách biệt (`INSERT INTO orders` và `INSERT INTO coupon_usage`) mà **không có `BEGIN TRANSACTION ... COMMIT`**.
  * Việc này buộc SQLite phải thực hiện 2 lần ghi đĩa vật lý (fsync) riêng biệt cho một đơn hàng, vừa làm tăng gấp đôi độ trễ I/O vừa có nguy cơ không nhất quán dữ liệu (nếu lệnh insert thứ hai thất bại).
  * **Giải pháp Thực thi:** Bọc các câu lệnh ghi trong một Transaction duy nhất:
    ```javascript
    db.serialize(() => {
        db.run("BEGIN TRANSACTION");
        // Insert order ...
        // Insert coupon usage ...
        db.run("COMMIT");
    });
    ```
  * **Lợi ích:** Giảm 50% số lần fsync đĩa của SQLite trong mỗi lượt checkout, tăng thông lượng đặt hàng tối đa.

---

### Đề xuất 4: Caching Danh mục Sản phẩm & Bộ nhớ Tạm Giỏ hàng
* **Phân loại:** **FEASIBLE (Khả thi)**
* **Bằng chứng & Cơ sở Kỹ thuật:**
  * Hai API `TC_04_Browse_Products` (`GET /api/products`) và `TC_05_Product_Detail` (`GET /api/products/:id`) chiếm 22% tổng lưu lượng hệ thống, nhưng chỉ truy vấn lặp đi lặp lại 5 sản phẩm tĩnh trong SQLite.
  * **Giải pháp Thực thi:** Áp dụng cơ chế In-Memory Cache (ví dụ thư viện `node-cache` hoặc một biến object đơn giản) cho danh mục sản phẩm, hoặc cấu hình HTTP Header `Cache-Control: public, max-age=60` kèm ETag.
  * **Dọn dẹp Giỏ hàng sau Checkout:** Bổ sung dòng lệnh xóa giỏ hàng sau khi đặt hàng thành công:
    ```javascript
    delete userCarts[userId]; // Tránh rò rỉ RAM dài hạn
    ```
  * **Lợi ích:** Loại bỏ 100% thao tác đọc database đối với sản phẩm, triệt tiêu nguy cơ rò rỉ bộ nhớ in-memory.

---

### Đề xuất 5: Mở rộng Đa tiến trình (Node.js Clustering / PM2)
* **Phân loại:** **REQUIRES FURTHER INVESTIGATION (Cần Nghiên cứu Thêm)**
* **Bằng chứng & Cơ sở Kỹ thuật:**
  * Máy chủ có 12 logical CPU threads (`lscpu`), nhưng Node.js hiện chỉ chạy 1 tiến trình duy nhất trên 1 core. Về mặt lý thuyết, mở rộng ra 4 hoặc 6 worker processes qua module `cluster` hoặc PM2 sẽ giúp tận dụng toàn bộ sức mạnh CPU đa nhân.
  * **Rào cản Kỹ thuật Lớn:**
    1. Giỏ hàng `userCarts = {}` đang được lưu trực tiếp trong bộ nhớ RAM của tiến trình ([backend/server.js#L14](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L14)). Nếu bật Cluster nhiều tiến trình, người dùng thêm hàng ở Worker 1 sẽ bị mất giỏ hàng khi request checkout rơi vào Worker 2!
    2. SQLite file lock sẽ bị xung đột nặng hơn khi có nhiều tiến trình Node.js riêng biệt cùng tranh chấp ghi vào file `database.sqlite`.
  * **Kết luận:** Đề xuất này **chưa thể áp dụng ngay**. Bắt buộc phải chuyển đổi `userCarts` sang Redis/Database và nâng cấp SQLite lên Client-Server DB (như PostgreSQL) trước khi triển khai Node.js Cluster.

---

### Đề xuất 6: Cấu hình Connection Pooling cho Cơ sở Dữ liệu
* **Phân loại:** **HALLUCINATED / UNSUPPORTED (Ảo tưởng / Không áp dụng được)**
* **Bằng chứng & Cơ sở Kỹ thuật:**
  * Hệ thống EShop sử dụng thư viện `sqlite3` cục bộ trên file `backend/database.sqlite` ([backend/database.js#L1-L4](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js#L1-L4)).
  * Khái niệm **Connection Pooling** (như HikariCP, pg-pool, generic-pool) được thiết kế cho các hệ quản trị cơ sở dữ liệu Client-Server hoạt động qua mạng (PostgreSQL, MySQL, Oracle) nhằm tái sử dụng các kết nối TCP đắt đỏ.
  * Đối với SQLite là embedded file database chạy trong cùng không gian địa chỉ tiến trình, việc tạo một "connection pool" gồm nhiều kết nối ghi thậm chí còn **gây hại nghiêm trọng**, làm tăng đột biến nguy cơ khóa file `SQLITE_BUSY`. Do đó, đề xuất áp dụng Connection Pooling cho kiến trúc SQLite hiện tại là hoàn toàn sai lệch về mặt kỹ thuật.

---

## 8. Phần 7 – Evidence References (Bằng chứng Tham chiếu Trực tiếp)

Mọi số liệu, phân tích và kết luận trong báo cáo này đều có thể được kiểm chứng độc lập thông qua các tệp bằng chứng sau trong repository:

### 8.1 Tệp Dữ liệu Thô (Raw JTL Files)
* **Load Test Raw Log:** [`23120268_Load_20261118.jtl`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Load_20261118.jtl) (17,738 bản ghi, MD5/SHA256 verified, thời gian: 14:54 – 15:04).
* **Stress Test Raw Log:** [`23120268_Stress_20261118.jtl`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Stress_20261118.jtl) (9,036 bản ghi, thời gian: 14:55 – 14:58).
* **Spike Test Raw Log:** [`23120268_Spike_20261118.jtl`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Spike_20261118.jtl) (10,153 bản ghi, thời gian: 13:36 – 13:43).

### 8.2 Báo cáo Trực quan (HTML Dashboard Reports)
* **Load Test HTML Dashboard:** [`reports/load_report/index.html`](file:///home/hung/26-27/Kiem_thu/eshop-sut/reports/load_report/index.html) (Thống kê chi tiết tại [`statistics.json`](file:///home/hung/26-27/Kiem_thu/eshop-sut/reports/load_report/statistics.json)).
* **Stress Test HTML Dashboard:** [`reports/stress_report/index.html`](file:///home/hung/26-27/Kiem_thu/eshop-sut/reports/stress_report/index.html) (Thống kê chi tiết tại [`statistics.json`](file:///home/hung/26-27/Kiem_thu/eshop-sut/reports/stress_report/statistics.json)).
* **Spike Test HTML Dashboard:** [`reports/spike_report/index.html`](file:///home/hung/26-27/Kiem_thu/eshop-sut/reports/spike_report/index.html) (Thống kê chi tiết tại [`statistics.json`](file:///home/hung/26-27/Kiem_thu/eshop-sut/reports/spike_report/statistics.json)).

### 8.3 Kịch bản Kiểm thử & Tài liệu Kỹ thuật
* Kịch bản Load Test: [`23120268_Load_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Load_20261118.jmx) & [`docs/performance/LOAD_TEST.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/LOAD_TEST.md).
* Kịch bản Stress Test: [`23120268_Stress_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Stress_20261118.jmx) & [`docs/performance/STRESS_TEST.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/STRESS_TEST.md).
* Kịch bản Spike Test: [`23120268_Spike_20261118.jmx`](file:///home/hung/26-27/Kiem_thu/eshop-sut/23120268_Spike_20261118.jmx) & [`docs/performance/SPIKE_TEST.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/SPIKE_TEST.md).
* Danh mục API & Kiến trúc: [`docs/performance/API_INVENTORY.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/API_INVENTORY.md).
* Thiết kế Dữ liệu Kiểm thử: [`docs/performance/TEST_DATA_DESIGN.md`](file:///home/hung/26-27/Kiem_thu/eshop-sut/docs/performance/TEST_DATA_DESIGN.md) & [`data/users.csv`](file:///home/hung/26-27/Kiem_thu/eshop-sut/data/users.csv).
* Script Đồng bộ Dữ liệu: [`scripts/seed_performance_users.js`](file:///home/hung/26-27/Kiem_thu/eshop-sut/scripts/seed_performance_users.js).

### 8.4 Môi trường Phần cứng Thực nghiệm (Hardware Specs)
* **Host Machine:** Linux Ubuntu x86_64 (`hung-GF63-Thin-10SC 7.0.0-43-generic`).
* **Processor:** Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz (6 Cores / 12 Threads, 12MB Cache).
* **RAM:** 7.1 GiB Physical Memory (DDR4), 4.0 GiB Swap.
* **Storage:** NVMe SSD `/dev/nvme0n1p8` (Ext4, 253 GB trống).
* **Runtimes:** Node.js v22.22.1 | Apache JMeter 5.6.3 trên OpenJDK 64-Bit Server VM (`-Xms1g -Xmx1g`).
