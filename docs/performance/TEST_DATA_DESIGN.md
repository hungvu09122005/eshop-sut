# THIẾT KẾ DỮ LIỆU KIỂM THỬ HIỆU NĂNG (TEST DATA DESIGN)
## Dự án: EShop | Công cụ: Apache JMeter
## Kịch bản: Login → Manage Profile → Browse Products → Add to Cart → Checkout

---

## 1. Phân tích Nhu cầu Dữ liệu (Data Requirements Identification)

Để thực thi trọn vẹn kịch bản kiểm thử hiệu năng End-to-End, dữ liệu cần thiết được xác định và đối chiếu chính xác với mã nguồn thực tế của từng API:

$$\mathbf{Login} \longrightarrow \mathbf{Manage\ Profile} \longrightarrow \mathbf{Browse\ Products} \longrightarrow \mathbf{Add\ to\ Cart} \longrightarrow \mathbf{Checkout}$$

### Bảng Ma trận Nhu cầu Dữ liệu theo từng Endpoint

| Bước | API Endpoint | HTTP Method | Dữ liệu Đầu vào Cần thiết | Nguồn Cung cấp Dữ liệu | Bắt buộc nghiệp vụ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `/api/login` | `POST` | `email`, `password` | `data/users.csv` | **Có** (Khớp tài khoản trong bảng `users`) |
| **2a**| `/api/users/me` | `GET` | `token` | Dynamic correlation từ Bước 1 (`$.token`) | **Có** (Header `Authorization: Bearer <token>`) |
| **2b**| `/api/users/me` | `PUT` | `token`, `name`, `phone`, `shipping_address` | `token` (Bước 1) + Thông tin từ `data/users.csv` | **Có** (Phone phải khớp regex `/^[1-9][0-9]{8,9}$/`) |
| **3a**| `/api/products` | `GET` | Không yêu cầu | Không có | **Không** (Public endpoint) |
| **3b**| `/api/products/:id` | `GET` | `product_id` | `data/products.csv` hoặc trích xuất từ Bước 3a | **Có** (ID phải tồn tại trong bảng `products`) |
| **4** | `/api/cart` | `POST` | `token`, `id`, `name`, `price`, `quantity` | `token` (Bước 1) + Thông tin từ `data/products.csv` | **Có** (Dữ liệu sản phẩm hợp lệ) |
| **5** | `/api/checkout` | `POST` | `token`, `total_amount`, `shipping_address` | `token` (Bước 1) + Tính từ Sản phẩm + `data/users.csv` | **Có** (`total_amount` phải là số nguyên dương) |

---

## 2. Danh mục File Dữ liệu CSV Đã Khởi tạo (CSV Files Inventory)

Hệ thống đã được trang bị bộ dữ liệu CSV hoàn chỉnh đặt tại thư mục `data/`:

### 2.1 File `data/users.csv` (Dữ liệu Người dùng & Hồ sơ)
* **Số lượng bản ghi:** **502 dòng** (1 dòng Header + 2 tài khoản có sẵn trong DB + 500 tài khoản chuyên dụng cho kiểm thử tải).
* **Cấu trúc cột:**
  ```csv
  user_email,user_password,user_name,user_phone,user_address
  ```
* **Chi tiết các trường dữ liệu:**
  1. `user_email`: Email đăng nhập duy nhất cho từng Virtual User.
     * Dòng 2: `test@eshop.com` (Tài khoản mẫu có sẵn trong DB).
     * Dòng 3: `admin@eshop.com` (Tài khoản mẫu có sẵn trong DB).
     * Dòng 4 – 503: `perf_user_001@eshop.com` đến `perf_user_500@eshop.com`.
  2. `user_password`: Mật khẩu chuẩn `Test1234!` (đồng bộ với cơ chế mật khẩu plaintext của hệ thống EShop).
  3. `user_name`: Họ và tên hiển thị riêng biệt cho từng người dùng (`Test User`, `Admin User`, `Perf User 001`, ...).
  4. `user_phone`: Số điện thoại hợp lệ tuân thủ biểu thức chính quy frontend `/^[1-9][0-9]{8,9}$/` (ví dụ: `0980000001` đến `0980000500`).
  5. `user_address`: Địa chỉ giao hàng cụ thể, độc lập cho từng người dùng tại TP.HCM (ví dụ: `"2 Le Loi, Q2, TP.HCM"`).

---

### 2.2 File `data/products.csv` (Dữ liệu Danh mục Sản phẩm)
* **Số lượng bản ghi:** **6 dòng** (1 dòng Header + 5 sản phẩm hiện hữu 100% trong database SQLite).
* **Cấu trúc cột:**
  ```csv
  product_id,product_name,product_price,quantity
  ```
* **Dữ liệu đối chiếu trực tiếp từ `backend/database.js#L98-L102`:**
  | `product_id` | `product_name` | `product_price` | `quantity` | Danh mục |
  | :--- | :--- | :--- | :--- | :--- |
  | `1` | iPhone 15 Pro Max | 30000000 | 1 | Điện thoại |
  | `2` | Samsung Galaxy S24 Ultra | 28000000 | 1 | Điện thoại |
  | `3` | MacBook Pro M3 | 45000000 | 1 | Laptop |
  | `4` | Tai nghe AirPods Pro 2 | 6000000 | 1 | Phụ kiện |
  | `5` | Bàn phím cơ Keychron Q1 | 4000000 | 1 | Phụ kiện |

---

### 2.3 File `data/checkout_data.csv` (Dữ liệu Thanh toán Mở rộng)
* **Số lượng bản ghi:** **501 dòng** (1 dòng Header + 500 bản ghi địa chỉ giao hàng và mã giảm giá).
* **Cấu trúc cột:**
  ```csv
  checkout_address,coupon_code
  ```
* **Đánh giá tính cần thiết (Evaluation):**
  * Trong luồng kiểm thử cơ bản của đề bài (`Login → Manage Profile → Browse Products → Add to Cart → Checkout`), trường địa chỉ giao hàng `shipping_address` **đã có sẵn trong `data/users.csv`** (`${user_address}`), và `total_amount` được tính trực tiếp từ giá sản phẩm (`${product_price} * ${quantity}`).
  * Tuy nhiên, file `data/checkout_data.csv` được tạo ra để phục vụ các tình huống kiểm thử mở rộng:
    1. Khi muốn kiểm thử hành vi người dùng nhập **địa chỉ giao hàng khác với địa chỉ trong hồ sơ**.
    2. Khi muốn tích hợp kiểm thử API mã giảm giá (`POST /api/apply-coupon`) trước khi thanh toán, với các mã coupon thực tế có trong database (`SAVE10`, `BIGBUY`, `VIP100`).
  * **Khuyến nghị kiến trúc JMeter:** Đối với kịch bản chính, nên ưu tiên dùng trường `user_address` từ `data/users.csv` để giảm số lượng file CSV cần đọc đồng thời, tránh nguy cơ lệch con trỏ đọc (Cursor Desynchronization) giữa các Thread.

---

## 3. Nguyên tắc Đảm bảo Tính Toàn vẹn & Cách ly Dữ liệu

1. **Ngăn chặn triệt để Account Lockout:**
   * Trong mã nguồn [backend/server.js#L54-L58](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L54-L58), mỗi lần đăng nhập sai hệ thống cộng 2 lần thử (`newAttempts = user.login_attempts + 2`). Chỉ cần sai **2 lần liên tiếp** là tài khoản bị khóa trong 3 phút.
   * Tất cả 502 tài khoản trong `data/users.csv` đều sử dụng chính xác mật khẩu `Test1234!`. Không chứa bất kỳ bản ghi sai mật khẩu nào trong bộ test tải.
2. **Cách ly Giỏ hàng in-memory (`userCarts` Isolation):**
   * Backend lưu trữ giỏ hàng trong RAM theo định danh người dùng: `userCarts[userId]`.
   * Việc mỗi Virtual User sở hữu một tài khoản riêng biệt đảm bảo mỗi VU thao tác trên một mảng giỏ hàng độc lập, không gây hiện tượng hàng trăm user cùng nhồi item vào giỏ của nhau.
3. **Tránh Xung đột Ghi đè Hồ sơ (Profile Race Condition):**
   * Khi gọi `PUT /api/users/me`, mỗi VU chỉ cập nhật dữ liệu của chính mình, loại bỏ hoàn toàn hiện tượng tranh chấp cập nhật dòng (Row lock contention) trong SQLite.
4. **Tránh Dữ liệu Rác & Không tồn tại:**
   * File `data/products.csv` chỉ sử dụng 5 sản phẩm thực sự tồn tại trong cơ sở dữ liệu (`ID: 1..5`). Tuyệt đối không sinh ID giả định (như ID 999) gây ra lỗi 200 rỗng hoặc 404 không mong muốn.
5. **Bảo mật Thông tin (Data Privacy):**
   * 100% dữ liệu trong các file CSV là dữ liệu giả lập (Mock data) cho mục đích kiểm thử. Không chứa email, số điện thoại, địa chỉ hoặc mật khẩu thật của bất kỳ cá nhân nào.

---

## 4. Kiểm tra Cơ chế Đọc CSV trong JMeter (CSV Data Set Config)

Để cấu hình chính xác `CSV Data Set Config` trong Apache JMeter, cần hiểu rõ ý nghĩa kỹ thuật của 5 thuộc tính cốt lõi:

```
[ CSV Data Set Config ]
  ├── Filename: data/users.csv
  ├── File encoding: UTF-8
  ├── Variable Names: user_email,user_password,user_name,user_phone,user_address
  ├── Ignore first line: True
  ├── Delimiter: ,
  ├── Allow quoted data: True
  ├── Recycle on EOF: False (cho Stress) / True (cho Load dài hạn)
  ├── Stop thread on EOF: True
  └── Sharing mode: All threads
```

### 4.1 Thuộc tính `Sharing Mode`
* **Ý nghĩa:** Quyết định phạm vi chia sẻ con trỏ đọc (File Pointer) giữa các Virtual Users (Threads).
* **Các chế độ:**
  * `All threads` (Khuyến nghị sử dụng): Con trỏ đọc được chia sẻ chung cho toàn bộ Thread Group. Khi Thread 1 đọc dòng 1, Thread 2 sẽ đọc dòng 2, Thread 3 đọc dòng 3,... Đảm bảo **mỗi VU nhận một tài khoản duy nhất**, không có hai VU nào đọc trùng dữ liệu trong cùng một vòng lặp.
  * `Current thread group`: Mỗi Thread Group có một con trỏ riêng (áp dụng khi có nhiều Thread Group chạy độc lập).
  * `Current thread`: Mỗi Thread tự mở file và đọc lại từ đầu (Gây trùng lặp tài khoản giữa các VU $\rightarrow$ **Không dùng**).

### 4.2 Thuộc tính `Recycle on EOF` (Quay vòng khi hết file)
* **Ý nghĩa:** Xác định hành vi của JMeter khi con trỏ đọc chạm tới dòng cuối cùng của file CSV (End Of File).
* **Áp dụng theo kịch bản:**
  * **Kịch bản Stress Testing (300 VUs):** Thiết lập `Recycle on EOF = False`. Vì file có 500 tài khoản, 300 VUs sẽ nhận 300 tài khoản độc lập mà không bị lặp lại.
  * **Kịch bản Load Testing dài hạn (50 VUs chạy trong 10 phút):** Nếu số lượt lặp (Iterations) vượt quá 500 lượt, có thể đặt `Recycle on EOF = True` kết hợp với Think Time để các user tái sử dụng phiên sau khi đã hoàn tất đơn hàng trước.

### 4.3 Thuộc tính `Stop thread on EOF` (Dừng thread khi hết file)
* **Ý nghĩa:** Khi hết file CSV và `Recycle on EOF = False`, thuộc tính này quyết định Thread có dừng chạy hay không.
* **Khuyến nghị:** Thiết lập `Stop thread on EOF = True` khi chạy Stress test để ngăn chặn các Thread chạy không có dữ liệu tài khoản (gây lỗi 401).

### 4.4 Thuộc tính `Ignore first line` (Bỏ qua dòng tiêu đề)
* **Ý nghĩa:** Bỏ qua dòng đầu tiên của file CSV.
* **Khuyến nghị:** Thiết lập **`True`** vì tất cả các file CSV của chúng ta đều có dòng tiêu đề Header (`user_email,user_password,...`).

### 4.5 Thuộc tính `Variable Names` (Danh sách tên biến)
* Khai báo danh sách tên biến JMeter tương ứng với thứ tự các cột trong CSV:
  `user_email,user_password,user_name,user_phone,user_address`
* Khi đọc xong một dòng, JMeter tự động gán giá trị vào các biến `${user_email}`, `${user_password}`, `${user_name}`,... để sử dụng trong các Sampler.

---

## 5. Hướng dẫn Cấu hình CSV Data Set Config trong JMeter

### 5.1 Cấu hình cho `data/users.csv` (Đặt ở đầu Test Plan)

| Thuộc tính trong JMeter | Giá trị Thiết lập | Mục đích Kỹ thuật |
| :--- | :--- | :--- |
| **Filename** | `data/users.csv` | Đường dẫn tương đối tính từ thư mục chạy JMeter |
| **File encoding** | `UTF-8` | Đảm bảo đọc chính xác tiếng Việt có dấu trong địa chỉ |
| **Variable Names** | `user_email,user_password,user_name,user_phone,user_address` | Khai báo 5 biến đại diện cho người dùng |
| **Delimiter** | `,` | Dấu phẩy ngăn cách trường |
| **Allow quoted data?** | **True** | Bắt buộc `True` vì địa chỉ chứa dấu phẩy được bọc trong ngoặc kép `""` |
| **Recycle on EOF?** | **False** (Stress) / **True** (Load dài hạn) | Tránh lặp lại tài khoản trong các bài test đột biến |
| **Stop thread on EOF?** | **True** | Dừng an toàn khi hết dữ liệu |
| **Sharing mode** | **All threads** | Đảm bảo phân bổ tài khoản duy nhất cho từng VU |

---

### 5.2 Cấu hình cho `data/products.csv` (Dùng để duyệt sản phẩm cố định)

| Thuộc tính trong JMeter | Giá trị Thiết lập | Mục đích Kỹ thuật |
| :--- | :--- | :--- |
| **Filename** | `data/products.csv` | File chứa 5 sản phẩm thực tế |
| **File encoding** | `UTF-8` | Hỗ trợ tiếng Việt |
| **Variable Names** | `product_id,product_name,product_price,quantity` | Khai báo 4 biến sản phẩm |
| **Delimiter** | `,` | Dấu phẩy ngăn cách |
| **Allow quoted data?** | **False** | Tên sản phẩm đơn giản, không chứa dấu phẩy |
| **Recycle on EOF?** | **True** | **Bắt buộc True**: Để các thread liên tục xoay vòng 5 sản phẩm |
| **Stop thread on EOF?** | **False** | Không dừng thread khi đọc hết 5 sản phẩm |
| **Sharing mode** | **All threads** | Các thread chia sẻ xoay vòng sản phẩm |

---

## 6. Ma trận Tương thích giữa CSV và Request Body Thực tế

Bảng đối chiếu kiểm tra tính tương thích 100% giữa dữ liệu biến từ CSV và cấu trúc JSON Payload mà backend Express.js yêu cầu:

### 6.1 Sampler `POST /api/login`
* **JSON Payload trong HTTP Request:**
  ```json
  {
    "email": "${user_email}",
    "password": "${user_password}"
  }
  ```
* **Mã nguồn Backend xử lý ([backend/server.js#L33-L35](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L33-L35)):**
  `const { email, password } = req.body;`
  `db.get("SELECT * FROM users WHERE email = ?", [email], ...)`
* **Kết quả đối chiếu:** **TƯƠNG THÍCH HOÀN TOÀN.**

---

### 6.2 Sampler `PUT /api/users/me`
* **JSON Payload trong HTTP Request:**
  ```json
  {
    "name": "${user_name}",
    "shipping_address": "${user_address}",
    "phone": "${user_phone}"
  }
  ```
* **Mã nguồn Backend xử lý ([backend/server.js#L119-L121](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L119-L121)):**
  `const { name, shipping_address, phone, role } = req.body;`
  `let query = "UPDATE users SET name = ?, shipping_address = ?, phone = ? WHERE id = ?";`
* **Kết quả đối chiếu:** **TƯƠNG THÍCH HOÀN TOÀN.**

---

### 6.3 Sampler `POST /api/cart`
* **JSON Payload trong HTTP Request:**
  ```json
  {
    "id": ${product_id},
    "name": "${product_name}",
    "price": ${product_price},
    "quantity": ${quantity}
  }
  ```
* **Mã nguồn Backend xử lý ([backend/server.js#L293](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L293)):**
  `userCarts[userId].push(req.body);`
* **Kết quả đối chiếu:** **TƯƠNG THÍCH HOÀN TOÀN.**

---

### 6.4 Sampler `POST /api/checkout`
* **JSON Payload trong HTTP Request:**
  ```json
  {
    "total_amount": ${product_price},
    "shipping_address": "${user_address}"
  }
  ```
* **Mã nguồn Backend xử lý ([backend/server.js#L299-L303](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L299-L303)):**
  `const { total_amount, shipping_address } = req.body;`
  `db.run("INSERT INTO orders (user_id, total_amount, status, shipping_address) VALUES (?, ?, 'pending', ?)", ...)`
* **Kết quả đối chiếu:** **TƯƠNG THÍCH HOÀN TOÀN.**

---

## 7. Hướng dẫn Quản lý Dữ liệu Cơ sở Dữ liệu & Script Seeder

### 7.1 Hiện trạng Cơ sở Dữ liệu Hiện tại
* Database `backend/database.sqlite` hiện chỉ có sẵn **2 tài khoản người dùng**:
  1. `admin@eshop.com` / `Admin123!` (Role: admin)
  2. `test@eshop.com` / `Test1234!` (Role: user)
* Nếu chạy kiểm thử nhanh (Smoke Test hoặc Sanity Check) với 1–2 Virtual Users: Có thể sử dụng trực tiếp 2 tài khoản này mà không cần thay đổi bất cứ điều gì.

### 7.2 Hướng dẫn Chạy Script Seed khi Thực thi Kiểm thử Tải Cao (50 – 300 VUs)
Để tuân thủ nghiêm ngặt nguyên tắc **"Không tự ý chạy hoặc thay đổi dữ liệu hiện có"**, hệ thống đã cung cấp một script độc lập tại [scripts/seed_performance_users.js](file:///home/hung/26-27/Kiem_thu/eshop-sut/scripts/seed_performance_users.js).

> [!IMPORTANT]
> **Đặc điểm Kỹ thuật của Script Seeder:**
> * Script này **KHÔNG** import file `backend/database.js` để tránh kích hoạt hàm `initDatabase()` vốn sẽ DROP và xóa sạch dữ liệu cũ.
> * Script sử dụng câu lệnh `INSERT ... WHERE NOT EXISTS` để chỉ chèn các tài khoản mới (`perf_user_001` đến `perf_user_500`), tuyệt đối không ghi đè hoặc làm hỏng 2 tài khoản mẫu `admin` và `test`.

Khi người dùng chuẩn bị chạy kịch bản kiểm thử tải cao (Load Test 50 VU hoặc Stress Test 300 VU), người dùng chỉ cần chủ động thực hiện lệnh sau:

```bash
# Nạp 500 tài khoản từ data/users.csv vào backend/database.sqlite
node scripts/seed_performance_users.js
```

Sau khi chạy xong, database sẽ sở hữu đầy đủ 502 tài khoản hợp lệ, sẵn sàng 100% để Apache JMeter thực thi với tải đồng thời lớn mà không gặp bất kỳ lỗi xác thực nào.
