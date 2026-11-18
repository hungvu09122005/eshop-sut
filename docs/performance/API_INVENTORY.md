# BÁO CÁO PHÂN TÍCH SOURCE CODE VÀ DANH MỤC API (API INVENTORY)
## Dự án: EShop (System Under Test - SUT)
## Phục vụ: HW05 – Performance Testing (Apache JMeter)

---

## 1. System Architecture (Kiến trúc hệ thống)

### 1.1 Tổng quan kiến trúc & Công nghệ
Hệ thống **EShop** được xây dựng theo mô hình Client-Server gồm các thành phần sau:

```
[ Frontend Web (React/Vite) ]  ──(HTTP/REST)──┐
[ Frontend Admin (React/Vite) ] ──(HTTP/REST)──┼──> [ Backend API (Express.js/Node.js) ] ──> [ SQLite (database.sqlite) ]
[ Frontend Mobile (React Native) ](HTTP/REST)──┘                     │
                                                                     └──> [ In-Memory Store: userCarts ]
```

* **Backend Framework:**
  * **Runtime:** Node.js.
  * **Framework:** Express.js `^5.2.1` ([backend/package.json#L16](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/package.json#L16)).
  * **Middleware:**
    * `cors` `^2.8.6`: Cho phép truy vấn Cross-Origin từ các frontend ([backend/server.js#L11](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L11)).
    * `body-parser` `^2.2.2`: Parse incoming request JSON ([backend/server.js#L12](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L12)).
    * `jsonwebtoken` `^9.0.3`: Ký và giải mã JSON Web Token (JWT) cho xác thực ([backend/server.js#L5](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L5)).
* **Frontend Frameworks:**
  * **Frontend Web (Khách hàng):** React `^19.2.6`, Vite `^8.0.12`, TailwindCSS `^3.4.19`, React Router DOM `^7.15.0`, Axios `^1.16.1` ([frontend-web/package.json#L13-L27](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-web/package.json#L13-L27)).
  * **Frontend Admin (Quản trị):** React `^19.2.6`, Vite `^8.0.12`, TailwindCSS `^3.4.19`, Axios `^1.16.1` ([frontend-admin/package.json#L13-L27](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-admin/package.json#L13-L27)).
  * **Frontend Mobile (Ứng dụng di động):** React `19.1.0`, React Native `0.81.5`, Expo SDK `~54.0.33` ([frontend-mobile/package.json#L10-L15](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-mobile/package.json#L10-L15)).
* **Database & Lưu trữ:**
  * **Database chính:** SQLite 3 (thông qua package `sqlite3` `^6.0.1`, [backend/package.json#L18](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/package.json#L18)). Dữ liệu được lưu trữ trực tiếp trong một file vật lý `backend/database.sqlite` ([backend/database.js#L4](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js#L4)).
  * **Lưu trữ Giỏ hàng (Cart Store):** In-Memory JavaScript Object trong tiến trình Node.js: `const userCarts = {};` ([backend/server.js#L14](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L14)). Dữ liệu giỏ hàng hoàn toàn **không** được lưu vào SQLite.

---

### 1.2 Cách ứng dụng khởi động
Hệ thống khởi chạy thông qua các bước cụ thể:
1. **Khởi tạo và nạp dữ liệu mẫu (Database Seeding):**
   * Lệnh: `node database.js` (chạy tại thư mục `backend/`).
   * Thực thi: Hàm `initDatabase()` trong [backend/database.js#L13-L115](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js#L13-L115) thực hiện `DROP TABLE IF EXISTS` và tạo lại 6 bảng: `categories`, `coupons`, `coupon_usage`, `users`, `products`, `orders`. Đồng thời chèn dữ liệu seed (2 users, 3 categories, 5 products, 4 coupons).
2. **Khởi chạy Backend Server:**
   * Lệnh: `node server.js` (tại thư mục `backend/`).
   * Khởi động server Express lắng nghe kết nối tại cổng cấu hình ([backend/server.js#L570-L572](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L570-L572)).
3. **Khởi chạy Frontend Web:**
   * Lệnh: `npm run dev` (tại thư mục `frontend-web/`). Chạy máy chủ Vite dev.
4. **Khởi chạy Frontend Admin:**
   * Lệnh: `npm run dev` (tại thư mục `frontend-admin/`).
5. **Khởi chạy Frontend Mobile:**
   * Lệnh: `npx expo start` (tại thư mục `frontend-mobile/`).
6. **Script tự động hóa:** File [run_servers.sh](file:///home/hung/26-27/Kiem_thu/eshop-sut/run_servers.sh) cung cấp script khởi động nền song song cả Backend, Web và Admin.

---

### 1.3 Cổng dịch vụ (Ports)
* **Backend API:** Port **3000** (`http://localhost:3000`) xác định tại biến `const PORT = 3000;` ([backend/server.js#L8](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L8)).
* **Frontend Web:** Port **5173** (`http://localhost:5173/` mặc định của Vite dev server).
* **Frontend Admin:** Port **5174** (`http://localhost:5174/` mặc định của Vite dev server khi port 5173 đã bị chiếm dụng).
* **Frontend Mobile (Expo Metro Bundler):** Port **8081** (mặc định của Expo Metro). Lưu ý: Trong mã nguồn mobile [frontend-mobile/App.js#L16](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-mobile/App.js#L16), địa chỉ backend API được hardcode là `http://192.168.10.13:3000/api`.

---

### 1.4 Luồng giao tiếp (Communication Flow)
1. **Frontend đến Backend:** Các client gửi các HTTP request (GET, POST, PUT, DELETE) với payload JSON và các HTTP headers tương ứng tới `http://localhost:3000/api/...`.
2. **Backend xử lý:**
   * Request đi qua middleware `cors()` và `bodyParser.json()`.
   * Các endpoint yêu cầu xác thực sẽ đi qua middleware `authenticateToken` ([backend/server.js#L100-L110](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L100-L110)).
   * Controller tương tác với cơ sở dữ liệu SQLite thông qua driver `sqlite3` bất đồng bộ (sử dụng callback `db.get`, `db.all`, `db.run`, `db.prepare`) hoặc thao tác trên đối tượng bộ nhớ `userCarts`.
3. **Backend đến Database:** Driver `sqlite3` thực hiện đọc/ghi trực tiếp vào file SQLite duy nhất trên đĩa cứng `backend/database.sqlite`.
4. **Backend phản hồi:** Trả về HTTP Response mã trạng thái 200/400/401/403/404/500 kèm payload JSON (hoặc HTML string nếu gặp lỗi truy vấn SQL ở search).

---

### 1.5 Cơ chế Authentication & Authorization
* **Cơ chế Authentication (Xác thực):**
  * Sử dụng **JSON Web Token (JWT)** không trạng thái (stateless).
  * Chuỗi Secret Key được hardcode trực tiếp trong mã nguồn: `SECRET_KEY = "super_secret_key_that_should_not_be_here"` ([backend/server.js#L9](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L9)).
  * Khi đăng nhập thành công qua `POST /api/login`, token được ký bằng lệnh:
    ```javascript
    const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);
    ```
  * Mật khẩu người dùng được lưu trữ và kiểm tra dưới dạng **Plaintext** (`user.password === password`, [backend/server.js#L46](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L46)).
* **Cơ chế Authorization (Phân quyền):**
  * **Hạn chế nghiêm trọng trong mã nguồn:** Middleware `authenticateToken` chỉ kiểm tra tính hợp lệ của token và gán payload vào `req.user`, hoàn toàn **KHÔNG** kiểm tra phân quyền theo vai trò (Role-based Access Control - RBAC).
  * Thậm chí ở tất cả các route quản trị viên (`/api/admin/users`, `/api/admin/orders`, `/api/admin/coupons`, `/api/admin/import-products`), server chỉ gọi `authenticateToken` mà không hề kiểm tra `req.user.role === 'admin'`. Do đó, bất kỳ user thông thường nào có token hợp lệ đều có thể truy cập được các API admin này.
  * Các route quản lý sản phẩm (`POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id`) thậm chí không gắn middleware `authenticateToken`, cho phép bất kỳ ai gửi request ẩn danh để thay đổi dữ liệu sản phẩm.

---

### 1.6 Quản lý Session, Cookie và JWT
* **Phía Server:**
  * Không dùng HTTP Session, không dùng Cookie, không có session store (Redis hay Memcached).
  * JWT được kiểm tra độc lập trên từng request thông qua hàm `jwt.verify(token, SECRET_KEY)`.
  * **Tuy nhiên**, đối với giỏ hàng, server lại quản lý trạng thái in-memory qua biến toàn cục `userCarts` gắn theo `userId` lấy từ token (`req.user.id`).
* **Phía Client (Frontend Web):**
  * Khi login thành công, JWT token được lưu vào trình duyệt thông qua Web Storage API: `localStorage.setItem("token", res.data.token)` ([frontend-web/src/context/AuthContext.jsx#L32](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-web/src/context/AuthContext.jsx#L32)).
  * Axios được cấu hình đính kèm token vào header cho mọi request tiếp theo:
    ```javascript
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    ```
  * Không sử dụng HttpOnly Cookie, tiềm ẩn nguy cơ XSS lấy cắp token phía client.

---

## 2. API Inventory (Danh mục API phục vụ Workflow Kiểm thử)

Workflow cần kiểm thử:
$$\text{Login} \longrightarrow \text{Manage Profile} \longrightarrow \text{Browse Products} \longrightarrow \text{Add to Cart} \longrightarrow \text{Checkout}$$

Dưới đây là chi tiết toàn bộ các API tương ứng được xác minh trực tiếp từ mã nguồn `backend/server.js`.

---

### 2.1 Login
* **Tên API:** Đăng nhập tài khoản
* **Mã nguồn:** [backend/server.js#L32-L66](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L32-L66)
* **HTTP Method:** `POST`
* **Endpoint:** `/api/login`
* **Request Headers:**
  * `Content-Type: application/json`
* **Request Body (JSON):**
  ```json
  {
    "email": "test@eshop.com",
    "password": "Test1234!"
  }
  ```
* **Query Parameters:** Không có.
* **Authentication Requirements:** Không yêu cầu (Public endpoint).
* **Response Structure:**
  * **200 OK (Thành công):**
    ```json
    {
      "message": "Login successful",
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "id": 2,
        "name": "Test User",
        "email": "test@eshop.com",
        "password": "Test1234!",
        "role": "user",
        "login_attempts": 0,
        "locked_until": null,
        "reset_token": null,
        "shipping_address": null,
        "phone": null
      }
    }
    ```
    *(Lưu ý: Mật khẩu plaintext của user bị trả về nguyên vẹn trong payload).*
  * **401 Unauthorized:**
    ```json
    {
      "error": "Invalid email or password"
    }
    ```
  * **403 Forbidden (Tài khoản bị khóa):**
    ```json
    {
      "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau."
    }
    ```
  * **500 Internal Server Error:**
    ```json
    {
      "error": "Lỗi truy vấn database"
    }
    ```
* **Điều kiện nghiệp vụ (Business Rules):**
  * Kiểm tra tài khoản có bị khóa không: Nếu `user.locked_until && new Date() < new Date(user.locked_until)`, lập tức từ chối với status 403.
  * Nếu mật khẩu đúng: Reset `login_attempts = 0`, `locked_until = NULL`, sinh token JWT không có thời hạn hết hạn.
  * Nếu mật khẩu sai: Tăng số lần thử `newAttempts = user.login_attempts + 2`. Nếu `newAttempts >= 3`, khóa tài khoản trong 180,000ms (3 phút) bằng cách set `locked_until = new Date(Date.now() + 180000).toISOString()`.
* **API Dependencies:** Không phụ thuộc API nào trước đó. Cung cấp `token` và `user.id` cho toàn bộ các bước tiếp theo của workflow.

---

### 2.2 Get Profile
* **Tên API:** Lấy thông tin cá nhân của người dùng hiện tại
* **Mã nguồn:** [backend/server.js#L112-L116](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L112-L116)
* **HTTP Method:** `GET`
* **Endpoint:** `/api/users/me`
* **Request Headers:**
  * `Authorization: Bearer <token>`
* **Request Body:** Không có.
* **Query Parameters:** Không có.
* **Authentication Requirements:** Bắt buộc JWT hợp lệ qua header `Authorization` (xử lý bởi `authenticateToken`).
* **Response Structure:**
  * **200 OK (Thành công):**
    ```json
    {
      "id": 2,
      "name": "Test User",
      "email": "test@eshop.com",
      "password": "Test1234!",
      "role": "user",
      "login_attempts": 0,
      "locked_until": null,
      "reset_token": null,
      "shipping_address": "123 Đường Lê Lợi, Quận 1, TP.HCM",
      "phone": "0912345678"
    }
    ```
    *(Nếu user đã bị xóa khỏi DB, trả về `null`).*
  * **401 Unauthorized:**
    ```json
    {
      "error": "Unauthorized"
    }
    ```
    *(Khi thiếu Header Authorization hoặc định dạng không có token).*
  * **403 Forbidden:**
    ```json
    {
      "error": "Forbidden"
    }
    ```
    *(Khi token không đúng chữ ký, sai SECRET_KEY hoặc bị can thiệp).*
* **Điều kiện nghiệp vụ:** Lấy `id` từ token (`req.user.id`) để thực thi câu truy vấn `SELECT * FROM users WHERE id = ?`.
* **API Dependencies:** Phụ thuộc vào JWT Token nhận được từ API `POST /api/login`.

---

### 2.3 Update Profile
* **Tên API:** Cập nhật thông tin hồ sơ cá nhân
* **Mã nguồn:** [backend/server.js#L118-L135](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L118-L135)
* **HTTP Method:** `PUT`
* **Endpoint:** `/api/users/me`
* **Request Headers:**
  * `Content-Type: application/json`
  * `Authorization: Bearer <token>`
* **Request Body (JSON):**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "0912345678"
  }
  ```
  *(Chú ý: Nếu truyền thêm trường `"role": "admin"`, backend sẽ cập nhật trực tiếp role của user vào database).*
* **Query Parameters:** Không có.
* **Authentication Requirements:** Bắt buộc JWT hợp lệ (`authenticateToken`).
* **Response Structure:**
  * **200 OK (Thành công):**
    ```json
    {
      "message": "Profile updated"
    }
    ```
  * **401 Unauthorized:** `{"error": "Unauthorized"}`
  * **403 Forbidden:** `{"error": "Forbidden"}`
  * **500 Internal Server Error:** `{"error": "<db error message>"}`
* **Điều kiện nghiệp vụ:** Cập nhật các trường `name`, `shipping_address`, `phone` và `role` (nếu có) vào bảng `users` cho `id = req.user.id`. Backend không validate định dạng số điện thoại hay độ dài tên (validation số điện thoại chỉ nằm ở Frontend React).
* **API Dependencies:** Phụ thuộc vào JWT Token từ API `POST /api/login`.

---

### 2.4 Browse Products
* **Tên API:** Lấy danh sách toàn bộ sản phẩm
* **Mã nguồn:** [backend/server.js#L141-L157](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L141-L157)
* **HTTP Method:** `GET`
* **Endpoint:** `/api/products`
* **Request Headers:** Không yêu cầu.
* **Request Body:** Không có.
* **Query Parameters:** Không có.
* **Authentication Requirements:** Không yêu cầu (Public endpoint).
* **Response Structure:**
  * **200 OK (Thành công):**
    ```json
    [
      {
        "id": 1,
        "name": "iPhone 15 Pro Max",
        "price": 30000000,
        "description": "Điện thoại cao cấp của Apple",
        "imageUrl": "https://placehold.co/300x300/png?text=iPhone+15",
        "category_id": 1
      },
      {
        "id": 2,
        "name": "Samsung Galaxy S24 Ultra",
        "price": 28000000,
        "description": "Màn hình hiển thị xuất sắc, camera siêu zoom",
        "imageUrl": "https://placehold.co/300x300/png?text=Samsung+S24",
        "category_id": 1
      }
    ]
    ```
  * **500 Internal Server Error:** Khi lỗi database.
* **Điều kiện nghiệp vụ:** Truy vấn toàn bộ bảng `products` bằng câu lệnh `SELECT * FROM products`.
* **API Dependencies:** Không phụ thuộc API nào. Cung cấp danh sách `product.id`, `product.name`, `product.price` cho các bước Add to Cart và Checkout.

---

### 2.5 Search Products
* **Tên API:** Tìm kiếm sản phẩm theo tên
* **Mã nguồn:** [backend/server.js#L141-L157](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L141-L157)
* **HTTP Method:** `GET`
* **Endpoint:** `/api/products`
* **Request Headers:** Không yêu cầu.
* **Request Body:** Không có.
* **Query Parameters:**
  * `search`: Từ khóa tìm kiếm (ví dụ: `?search=iPhone` hoặc `?search=Pro`).
* **Authentication Requirements:** Không yêu cầu (Public endpoint).
* **Response Structure:**
  * **200 OK (Thành công):** Mảng các sản phẩm khớp tên dạng JSON. Nếu không tìm thấy, trả về mảng rỗng `[]`.
  * **500 Internal Server Error:** Khi từ khóa tìm kiếm chứa ký tự đặc biệt gây lỗi cú pháp SQL (ví dụ dấu nháy đơn `'`), backend trả về chuỗi HTML:
    ```html
    <h1>Database Error</h1><p>SQLITE_ERROR: unrecognized token: "..."</p>
    ```
* **Điều kiện nghiệp vụ:** Backend ghép trực tiếp query string: `SELECT * FROM products WHERE name LIKE '%${searchQuery}%'`. Đây là lỗ hổng SQL Injection cố ý trong SUT.
* **API Dependencies:** Không phụ thuộc API nào.

---

### 2.6 Product Details
* **Tên API:** Xem chi tiết một sản phẩm
* **Mã nguồn:** [backend/server.js#L159-L165](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L159-L165)
* **HTTP Method:** `GET`
* **Endpoint:** `/api/products/:id` (ví dụ: `/api/products/1`)
* **Request Headers:** Không yêu cầu.
* **Request Body:** Không có.
* **Path Parameters:**
  * `id`: ID của sản phẩm (số nguyên).
* **Authentication Requirements:** Không yêu cầu (Public endpoint).
* **Response Structure:**
  * **200 OK (Thành công):**
    ```json
    {
      "id": 1,
      "name": "iPhone 15 Pro Max",
      "price": 30000000,
      "description": "Điện thoại cao cấp của Apple",
      "imageUrl": "https://placehold.co/300x300/png?text=iPhone+15",
      "category_id": 1
    }
    ```
    * **Đặc tính bất thường (Deliberate Bug):** Tại [backend/server.js#L162](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L162), nếu `row.id % 2 === 0` (ID chẵn, ví dụ sản phẩm ID 2), thuộc tính `price` bị chuyển kiểu thành chuỗi (`"28000000"`) thay vì số nguyên.
    * **Khi sản phẩm không tồn tại:** Trả về HTTP **200 OK** kèm object rỗng `{}` ([backend/server.js#L161](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L161)), **không** trả về 404 Not Found!
* **Điều kiện nghiệp vụ:** Thực thi `SELECT * FROM products WHERE id = ?`.
* **API Dependencies:** Cần có `productId` từ danh sách `GET /api/products`.

---

### 2.7 Add to Cart
* **Tên API:** Thêm sản phẩm vào giỏ hàng
* **Mã nguồn:** [backend/server.js#L290-L295](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L290-L295)
* **HTTP Method:** `POST`
* **Endpoint:** `/api/cart`
* **Request Headers:**
  * `Content-Type: application/json`
  * `Authorization: Bearer <token>`
* **Request Body (JSON):**
  *(Backend chấp nhận bất kỳ đối tượng JSON nào và push thẳng vào mảng giỏ hàng của user)*
  ```json
  {
    "id": 1,
    "name": "iPhone 15 Pro Max",
    "price": 30000000,
    "quantity": 1
  }
  ```
* **Query Parameters:** Không có.
* **Authentication Requirements:** Bắt buộc JWT hợp lệ (`authenticateToken`).
* **Response Structure:**
  * **200 OK (Thành công):**
    ```json
    {
      "message": "Added to cart"
    }
    ```
  * **401 Unauthorized:** `{"error": "Unauthorized"}`
  * **403 Forbidden:** `{"error": "Forbidden"}`
* **Điều kiện nghiệp vụ:**
  * Dữ liệu được lưu trữ trực tiếp vào biến bộ nhớ `userCarts[userId]`.
  * Không kiểm tra schema của body, không kiểm tra sản phẩm có tồn tại trong database hay không, không kiểm tra số lượng tồn kho.
  * Dữ liệu sẽ mất sạch nếu server backend bị khởi động lại.
* **API Dependencies:** Phụ thuộc vào `token` từ `POST /api/login` và thông tin sản phẩm từ `GET /api/products`.

---

### 2.8 Get Cart
* **Tên API:** Lấy danh sách sản phẩm trong giỏ hàng
* **Mã nguồn:** [backend/server.js#L284-L288](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L284-L288)
* **HTTP Method:** `GET`
* **Endpoint:** `/api/cart`
* **Request Headers:**
  * `Authorization: Bearer <token>`
* **Request Body:** Không có.
* **Query Parameters:** Không có.
* **Authentication Requirements:** Bắt buộc JWT hợp lệ (`authenticateToken`).
* **Response Structure:**
  * **200 OK (Thành công):** Mảng các item đã thêm vào giỏ:
    ```json
    [
      {
        "id": 1,
        "name": "iPhone 15 Pro Max",
        "price": 30000000,
        "quantity": 1
      }
    ]
    ```
    *(Nếu user chưa thêm sản phẩm nào, trả về mảng rỗng `[]`).*
  * **401 Unauthorized:** `{"error": "Unauthorized"}`
  * **403 Forbidden:** `{"error": "Forbidden"}`
* **Điều kiện nghiệp vụ:** Đọc trực tiếp từ bộ nhớ `userCarts[userId]`.
* **API Dependencies:** Phụ thuộc vào `token` từ `POST /api/login`.

---

### 2.9 Update Cart
* **Trạng thái:** **NOT FOUND** (Không tồn tại trong mã nguồn Backend).
* **Chi tiết đối chiếu mã nguồn:**
  * Trong toàn bộ file `backend/server.js`, chỉ có 2 route cho cart là `app.get("/api/cart")` và `app.post("/api/cart")`. Hoàn toàn không có các route `PUT /api/cart`, `PATCH /api/cart`, `DELETE /api/cart`, hay `DELETE /api/cart/:id`.
  * Phía Frontend Web ([frontend-web/src/context/CartContext.jsx#L12-L20](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-web/src/context/CartContext.jsx#L12-L20)) và Frontend Mobile ([frontend-mobile/App.js#L141-L157](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-mobile/App.js#L141-L157)): Các thao tác xóa hoặc cập nhật số lượng giỏ hàng được xử lý **hoàn toàn ở phía client** trên React State in-memory, không bao giờ gửi bất kỳ HTTP request nào lên server.

---

### 2.10 Checkout
* **Tên API:** Đặt hàng (Tạo đơn hàng)
* **Mã nguồn:** [backend/server.js#L297-L309](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L297-L309)
* **HTTP Method:** `POST`
* **Endpoint:** `/api/checkout`
* **Request Headers:**
  * `Content-Type: application/json`
  * `Authorization: Bearer <token>`
* **Request Body (JSON):**
  * Backend trích xuất hai thuộc tính `total_amount` và `shipping_address` từ `req.body`:
    ```json
    {
      "total_amount": 30000000,
      "shipping_address": "123 Đường Lê Lợi, Quận 1, TP.HCM"
    }
    ```
  * *(Lưu ý thực tế từ Frontend Web [frontend-web/src/pages/Checkout.jsx#L45-L49](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-web/src/pages/Checkout.jsx#L45-L49): Frontend gửi `{ items: cart, total_amount: finalAmount, coupon_id: ... }`. Frontend không truyền `shipping_address`, do đó trường này sẽ nhận giá trị `null` trong SQLite nếu gọi từ Web UI).*
* **Query Parameters:** Không có.
* **Authentication Requirements:** Bắt buộc JWT hợp lệ (`authenticateToken`).
* **Response Structure:**
  * **200 OK (Thành công):**
    ```json
    {
      "message": "Checkout successful",
      "orderId": 1
    }
    ```
  * **401 Unauthorized:** `{"error": "Unauthorized"}`
  * **403 Forbidden:** `{"error": "Forbidden"}`
  * **500 Internal Server Error:** `{"error": "<db error message>"}`
* **Điều kiện nghiệp vụ:**
  * Thực hiện câu lệnh: `INSERT INTO orders (user_id, total_amount, status, shipping_address) VALUES (?, ?, 'pending', ?)`.
  * Trả về ID của đơn hàng vừa tạo (`this.lastID`).
  * **Hạn chế logic (Critical Discovery):**
    * Backend **không** liên kết với `userCarts[userId]`.
    * Backend **không** xóa giỏ hàng `userCarts[userId]` sau khi checkout.
    * Backend **không** lưu danh sách chi tiết các mặt hàng trong đơn hàng (không có bảng `order_items`).
    * Backend **không** tính toán kiểm tra lại `total_amount` (client gửi giá trị nào thì lưu giá trị đó).
* **API Dependencies:** Phụ thuộc vào `token` từ `POST /api/login` và giá trị `total_amount` được tính từ các sản phẩm được chọn.

---

## 3. Authentication Analysis (Phân tích cơ chế Xác thực & Tài khoản)

### 3.1 Cách lấy và lưu Token / Session
* **Lấy Token:** Client gửi yêu cầu đăng nhập `POST /api/login` với email và password. Backend đối chiếu thông tin trong bảng `users`. Nếu khớp, server gọi `jwt.sign({ id: user.id, role: user.role }, SECRET_KEY)` để sinh chuỗi JWT và gửi về trong response body tại trường `token`.
* **Lưu trữ Token phía Client:**
  * Trên Web: Lưu trong `localStorage` qua `localStorage.setItem("token", res.data.token)` ([frontend-web/src/context/AuthContext.jsx#L32](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-web/src/context/AuthContext.jsx#L32)).
  * Trên Mobile: Lưu trong React Component State `token` ([frontend-mobile/App.js#L34](file:///home/hung/26-27/Kiem_thu/eshop-sut/frontend-mobile/App.js#L34)).
* **Lưu trữ phía Server:** Hoàn toàn không lưu token. Server xác thực từng request bằng giải mã chữ ký mật mã đối xứng qua `jwt.verify()`.

---

### 3.2 Cách truyền Token giữa các Request
* Token được đính kèm vào HTTP Request Header theo chuẩn Bearer Token:
  ```http
  Authorization: Bearer <chuỗi_token_jwt>
  ```
* Tại [backend/server.js#L100-L103](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L100-L103), middleware `authenticateToken` thực hiện:
  1. Trích xuất giá trị header: `const authHeader = req.headers["authorization"]`.
  2. Tách chuỗi lấy phần token: `const token = authHeader && authHeader.split(" ")[1]`.
  3. Nếu không có token, trả về HTTP status `401 Unauthorized`.
  4. Xác thực token qua `jwt.verify(token, SECRET_KEY, (err, user) => ...)`: Nếu không hợp lệ trả về HTTP status `403 Forbidden`; nếu hợp lệ gán payload `{ id, role }` vào `req.user` và chuyển sang middleware tiếp theo bằng `next()`.

---

### 3.3 Token có hết hạn không?
* **KHÔNG! (Never Expires):**
  * Trong mã nguồn tại [backend/server.js#L51](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L51):
    ```javascript
    const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);
    ```
  * Lệnh gọi `jwt.sign()` **hoàn toàn không truyền tham số tùy chọn** `{ expiresIn: ... }`. Do đó trong payload của JWT không hề có trường thời gian hết hạn `exp`.
  * **Hệ quả trong Performance Testing:** Một khi Virtual User lấy được token từ bước `POST /api/login`, token đó có thể tái sử dụng vô thời hạn trong suốt toàn bộ quá trình chạy test (Load / Stress / Spike) mà không sợ bị hết hạn giữa chừng.

---

### 3.4 Cơ chế Account Lockout & Giới hạn đăng nhập thất bại
Hệ thống **CÓ** cơ chế khóa tài khoản được cài đặt trực tiếp trong cơ sở dữ liệu và mã nguồn `POST /api/login` ([backend/server.js#L40-L64](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L40-L64)).

* **Cấu trúc lưu trạng thái khóa:** Bảng `users` có 2 cột phục vụ tính năng này:
  * `login_attempts` (INTEGER DEFAULT 0): Số lần thử đăng nhập thất bại đã ghi nhận.
  * `locked_until` (DATETIME): Thời điểm hết hạn khóa tài khoản.
* **Quy tắc đếm lỗi bất thường (Deliberate Bug):**
  * Khi đăng nhập sai mật khẩu, server tăng biến đếm số lần thất bại thêm **2 đơn vị** thay vì 1 đơn vị:
    ```javascript
    const newAttempts = user.login_attempts + 2;
    ```
  * Điều kiện kích hoạt khóa tài khoản: `if (newAttempts >= 3)`.
  * Thời gian khóa: **180,000 milliseconds = 3 phút** (180 giây):
    ```javascript
    lockedUntil = new Date(Date.now() + 180000).toISOString();
    ```
* **Bảng diễn biến số lần đăng nhập sai:**
  | Lần sai | `login_attempts` trước đó | `newAttempts` tính toán | Trạng thái tài khoản | Phản hồi HTTP |
  | :--- | :--- | :--- | :--- | :--- |
  | **Lần 1** | 0 | 2 | Chưa khóa (`2 < 3`) | `401 Unauthorized` |
  | **Lần 2** | 2 | 4 | **BỊ KHÓA 3 PHÚT** (`4 >= 3`) | `401 Unauthorized` |
  | **Lần 3+** | 4 | 4 (hoặc lớn hơn) | Đang trong thời gian khóa | `403 Forbidden` ("Tài khoản đã bị khóa...") |
* **Cơ chế mở khóa (Unlock):**
  * Hết 3 phút: Biểu thức `new Date() < new Date(user.locked_until)` trả về `false`, user được phép đăng nhập lại.
  * Đăng nhập thành công: Server thực thi reset:
    ```javascript
    db.run("UPDATE users SET login_attempts = 0, locked_until = NULL WHERE id = ?", [user.id]);
    ```

---

### 3.5 Rủi ro khi nhiều Virtual Users (VUs) sử dụng chung một tài khoản
Việc cấu hình hàng chục hoặc hàng trăm Virtual Users trong Apache JMeter dùng chung một thông tin tài khoản (ví dụ tài khoản mặc định `test@eshop.com`) sẽ dẫn đến các thảm họa về tính chính xác và độ ổn định của bài kiểm thử:

1. **Nguy cơ Account Lockout dây chuyền (Cascading Failure):**
   * Nếu có bất kỳ VU nào gửi sai mật khẩu (do lỗi cấu hình, payload hỏng, hoặc test case âm tính), chỉ sau 2 request, tài khoản `test@eshop.com` sẽ bị khóa ngay lập tức trong 3 phút.
   * Kể từ thời điểm đó, **toàn bộ các Virtual Users khác** đang chạy đều sẽ nhận mã lỗi `403 Forbidden` ở bước Login, khiến tỉ lệ lỗi (Error Rate) tăng vọt lên 100% và làm hỏng toàn bộ đợt kiểm thử hiệu năng.
2. **Tranh chấp khóa ghi SQLite (SQLite Database Lock Contention):**
   * Mỗi lần login, server đều chạy câu lệnh `UPDATE users SET login_attempts = ...`.
   * Khi 50–100 VUs đồng thời login cùng một tài khoản, nhiều câu lệnh `UPDATE` cùng nhắm vào một dòng (row) và một file database duy nhất, dễ gây ra lỗi `SQLITE_BUSY: database is locked`.
3. **Ô nhiễm & Bùng nổ kích thước Giỏ hàng in-memory (`userCarts` Bloating):**
   * Backend lưu giỏ hàng theo `userCarts[userId]`. Nếu tất cả VUs đều có `userId = 2`, mọi thao tác `POST /api/cart` của tất cả VU sẽ nhồi chung vào cùng một mảng `userCarts[2]`.
   * Sau một vài phút chạy tải, giỏ hàng của user 2 có thể chứa hàng chục nghìn item, gây tốn RAM bất thường trên Node.js heap và làm biến dạng hoàn toàn response time của API `GET /api/cart`.
4. **Ghi đè xung đột dữ liệu Profile (Race Condition trên `PUT /api/users/me`):**
   * Các VUs sẽ liên tục ghi đè dữ liệu họ tên, số điện thoại, địa chỉ của nhau trên cùng một record `id = 2`.
5. **Payload phình to ở lịch sử đơn hàng (`GET /api/orders/my-orders`):**
   * Mỗi lần checkout thành công, một dòng mới được ghi vào `orders` với `user_id = 2`.
   * Càng về cuối bài test, câu lệnh `SELECT * FROM orders WHERE user_id = ?` trả về payload JSON ngày càng khổng lồ, khiến thời gian phản hồi (latency) tăng dần do kích thước truyền tải chứ không phải do năng lực xử lý của server.

> [!IMPORTANT]
> **Giải pháp bắt buộc cho JMeter:** Phải chuẩn bị sẵn danh sách nhiều tài khoản người dùng độc lập (sử dụng file `users.csv` kết hợp `CSV Data Set Config` trong JMeter), đảm bảo mỗi Virtual User chạy trên một tài khoản riêng biệt.

---

## 4. Data Model Analysis (Phân tích Mô hình Dữ liệu)

Dựa trên mã nguồn khởi tạo [backend/database.js](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js) và các thao tác trong [backend/server.js](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js):

### 4.1 Cấu trúc Entity User (`users` table)
* **Tên bảng:** `users`
* **Vị trí định nghĩa:** [backend/database.js#L50-L61](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js#L50-L61)
* **Các trường dữ liệu:**
  | Tên cột | Kiểu dữ liệu | Ràng buộc SQLite | Bắt buộc nghiệp vụ | Mô tả |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Có (Tự sinh) | Định danh người dùng |
  | `name` | TEXT | Không | Có | Họ và tên |
  | `email` | TEXT | Không (Thiếu UNIQUE!) | Có | Email đăng nhập |
  | `password` | TEXT | Không | Có | Mật khẩu plaintext |
  | `role` | TEXT | DEFAULT 'user' | Không | Quyền hạn (`user`/`admin`) |
  | `login_attempts` | INTEGER | DEFAULT 0 | Không | Số lần đăng nhập sai |
  | `locked_until` | DATETIME | Không | Không | Mốc thời gian hết hạn khóa |
  | `reset_token` | TEXT | Không | Không | Mã OTP reset mật khẩu |
  | `shipping_address`| TEXT | Không | Không | Địa chỉ giao hàng mặc định |
  | `phone` | TEXT | Không | Không | Số điện thoại liên hệ |

---

### 4.2 Cấu trúc Entity Product (`products` table)
* **Tên bảng:** `products`
* **Vị trí định nghĩa:** [backend/database.js#L64-L71](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js#L64-L71)
* **Các trường dữ liệu:**
  | Tên cột | Kiểu dữ liệu | Ràng buộc SQLite | Bắt buộc nghiệp vụ | Mô tả |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Có (Tự sinh) | ID sản phẩm |
  | `name` | TEXT | Không | Có | Tên sản phẩm |
  | `price` | INTEGER | Không | Có | Giá bán sản phẩm (VND) |
  | `description` | TEXT | Không | Không | Mô tả chi tiết |
  | `imageUrl` | TEXT | Không | Không | Đường dẫn ảnh đại diện |
  | `category_id` | INTEGER | Không | Không | Tham chiếu logic `categories.id` |

---

### 4.3 Cấu trúc Entity Cart (`userCarts` in-memory structure)
* **Trạng thái bảng Database:** **NOT FOUND** (Không có bảng `carts` hay `cart_items` trong database SQLite).
* **Cấu trúc lưu trữ:** Object trong bộ nhớ Node.js process: `const userCarts = {};` ([backend/server.js#L14](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/server.js#L14)).
* **Cấu trúc mỗi Item trong giỏ:**
  ```json
  {
    "id": 1,
    "name": "iPhone 15 Pro Max",
    "price": 30000000,
    "quantity": 1
  }
  ```
* **Ràng buộc:** Backend hoàn toàn không áp đặt schema validation hay kiểm tra tồn kho.

---

### 4.4 Cấu trúc Entity Order (`orders` table)
* **Tên bảng:** `orders`
* **Vị trí định nghĩa:** [backend/database.js#L74-L81](file:///home/hung/26-27/Kiem_thu/eshop-sut/backend/database.js#L74-L81)
* **Các trường dữ liệu:**
  | Tên cột | Kiểu dữ liệu | Ràng buộc SQLite | Bắt buộc nghiệp vụ | Mô tả |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Có (Tự sinh) | Mã đơn hàng |
  | `user_id` | INTEGER | Không | Có | ID khách hàng (lấy từ JWT) |
  | `total_amount` | INTEGER | Không | Có | Tổng tiền thanh toán (VND) |
  | `status` | TEXT | DEFAULT 'pending' | Có | Trạng thái (`pending`, `confirmed`, `shipping`, `delivered`, `canceled`) |
  | `shipping_address`| TEXT | Không | Không | Địa chỉ giao nhận |
  | `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Có (Tự sinh) | Thời điểm tạo đơn |

---

### 4.5 Quan hệ giữa các Entity (Entity Relationships)
```
[ users ] (1) ───────────────< (N) [ orders ]
    │
    ├────────────────────────< (N) [ coupon_usage ] >─────────────── (1) [ coupons ]
    │
    └──── (1 in-memory) ────< (1) [ userCarts ]

[ categories ] (1) ──────────< (N) [ products ]
```

* **users (1) ── (N) orders:** Liên kết qua `orders.user_id = users.id`.
* **categories (1) ── (N) products:** Liên kết logic qua `products.category_id = categories.id`.
* **coupons (1) ── (N) coupon_usage (N) ── (1) users:** Ghi nhận lịch sử dùng coupon.
* **users (1) ── (1) userCarts:** Liên kết logic trong RAM qua `userCarts[userId]`.
* **Thiếu sót nghiêm trọng trong Database Schema:**
  * **Không có Foreign Key Constraints:** Bảng không khai báo `FOREIGN KEY` và kết nối SQLite không kích hoạt `PRAGMA foreign_keys = ON;`.
  * **Không có bảng `order_items`:** Khi đơn hàng được tạo qua `POST /api/checkout`, hệ thống **chỉ** lưu `total_amount` mà hoàn toàn **không** lưu danh sách sản phẩm hay số lượng được mua vào database.

---

## 5. Endpoint Group Classification (Phân loại Nhóm Endpoint)

Theo yêu cầu của đề bài HW05 (Mục 5: Endpoint Selection), các API được phân thành 3 nhóm phục vụ thiết kế kịch bản test:

### 5.1 Nhóm Read-heavy
* **Danh sách API:**
  * `GET /api/products` (Lấy danh sách sản phẩm)
  * `GET /api/products?search={keyword}` (Tìm kiếm sản phẩm)
  * `GET /api/products/:id` (Xem chi tiết sản phẩm)
  * `GET /api/categories` (Xem danh mục sản phẩm)
  * `GET /api/users/me` (Lấy thông tin cá nhân)
  * `GET /api/cart` (Đọc giỏ hàng)
  * `GET /api/orders/my-orders` (Xem lịch sử đơn hàng cá nhân)
* **Đặc tính kiểm thử:**
  * Thao tác thuần đọc (SELECT) dữ liệu.
  * Không làm biến đổi trạng thái hệ thống.
  * Phù hợp để kiểm thử khả năng đáp ứng thông lượng tối đa (Throughput/RPS) và kiểm tra năng lực chịu tải đọc đồng thời của server.

---

### 5.2 Nhóm Auth-heavy
* **Danh sách API:**
  * `POST /api/login` (Xác thực đăng nhập, tạo JWT)
  * `POST /api/register` (Đăng ký người dùng mới)
  * `POST /api/forgot-password` (Tạo OTP khôi phục mật khẩu)
  * `POST /api/reset-password` (Đặt lại mật khẩu)
* **Đặc tính kiểm thử:**
  * Chịu ảnh hưởng trực tiếp bởi thuật toán mã hóa/ký JWT (`jwt.sign`) trên CPU.
  * Chịu ảnh hưởng bởi cơ chế **Account Lockout**: Nếu test tải với mật khẩu sai, tài khoản sẽ bị khóa ngay lập tức.
  * Các thao tác ghi kèm theo: Ghi nhận số lần đăng nhập sai, reset số lần đăng nhập.

---

### 5.3 Nhóm Transactional
* **Danh sách API:**
  * `POST /api/cart` (Thêm hàng vào giỏ)
  * `POST /api/checkout` (Tạo đơn hàng thanh toán)
  * `PUT /api/users/me` (Cập nhật hồ sơ cá nhân)
  * `PUT /api/orders/:id/cancel` (Hủy đơn hàng)
  * `POST /api/apply-coupon` (Áp dụng mã giảm giá)
  * `POST /api/coupon-usage` (Ghi nhận sử dụng mã giảm giá)
* **Đặc tính kiểm thử:**
  * Làm biến đổi trạng thái hệ thống (Ghi/Cập nhật dữ liệu vào SQLite hoặc RAM).
  * Chịu ảnh hưởng trực tiếp bởi cơ chế khóa file (File Lock) của SQLite và độ trễ ghi đĩa (Disk I/O).

---

### 5.4 Những điểm có thể gây Bottleneck (Nút thắt cổ chai)
1. **SQLite Database Write Concurrency (Database Lock):**
   * SQLite là cơ sở dữ liệu file đơn với cơ chế Single-Writer lock. Khi nhiều Virtual Users đồng thời thực hiện các transaction ghi (`POST /api/checkout`, `PUT /api/users/me`, hoặc `POST /api/login`), SQLite sẽ khóa toàn bộ file database.
   * Dưới tải cao (Stress/Spike), hàng loạt thread sẽ phải xếp hàng chờ giải phóng lock, dẫn đến hiện tượng bùng nổ response time hoặc lỗi `SQLITE_BUSY: database is locked`.
2. **Single-threaded Node.js Event Loop:**
   * Backend chạy trên kiến trúc đơn luồng của Node.js. Mọi tác vụ CPU-bound như parse JSON payload lớn, ký chữ ký HMAC-SHA256 của JWT (`jwt.sign`), hoặc xử lý biểu thức chính quy đều chia sẻ chung một Event Loop.
3. **Unindexed Database & Lỗ hổng SQL Injection tại Search:**
   * Bảng `products` không có Index cho cột `name`. Câu lệnh `SELECT * FROM products WHERE name LIKE '%...%'` buộc SQLite phải quét toàn bộ bảng (Full Table Scan).
   * Lỗ hổng nối chuỗi trực tiếp khiến server dễ bị crash hoặc trả về lỗi 500 HTML khi gặp ký tự lạ.
4. **Memory Leak / Memory Bloat trong biến `userCarts`:**
   * Biến toàn cục `userCarts = {}` trong Node.js không có cơ chế dọn dẹp (không có Time-to-Live, không xóa sau checkout, không giới hạn kích thước). Khi số lượng Virtual Users và số lần add-to-cart tăng cao trong các bài test Stress hoặc Soak/Endurance, dung lượng RAM của tiến trình Node.js sẽ tăng liên tục không hồi phục, tiềm ẩn nguy cơ sập server do Out-Of-Memory (OOM).

---

### 5.5 Những vấn đề ảnh hưởng đến tính chính xác của kết quả Performance Testing
1. **Dữ liệu tích lũy qua các lần chạy (Data Accumulation):** Sau mỗi bài test tải, số lượng bản ghi trong bảng `orders` sẽ tăng lên hàng chục nghìn dòng. Nếu không reset cơ sở dữ liệu trước mỗi lần chạy (Load vs Stress vs Spike), kết quả đo lường ở các đợt chạy sau sẽ bị suy thoái do dữ liệu nền quá lớn, làm sai lệch so sánh đối chứng.
2. **Hiện tượng Account Lockout:** Nếu cấu hình nhiều thread cùng login vào 1 tài khoản và có lỗi phát sinh, tài khoản bị khóa 3 phút sẽ biến bài test tải thành bài test nhận lỗi 403.
3. **Bug ép kiểu chuỗi ở Product Details:** Sản phẩm có ID chẵn trả về giá là string, nếu JMeter Assertion kiểm tra kiểu dữ liệu số sẽ bị báo lỗi sai (False Negative).

---

## 6. Workflow Dependency & Execution Sequence

Kịch bản kiểm thử hiệu năng tổng thể:
$$\text{Login} \longrightarrow \text{Manage Profile} \longrightarrow \text{Browse Products} \longrightarrow \text{Add to Cart} \longrightarrow \text{Checkout}$$

### 6.1 Thứ tự thực thi các HTTP Request trong JMeter

```
[ Thread Group (Virtual Users) ]
   │
   ├─► Step 1: HTTP Request - POST /api/login
   │     └─► JSON Extractor: Trích xuất $.token và $.user.id
   │
   ├─► Step 2a: HTTP Request - GET /api/users/me
   │     └─► Header: Authorization: Bearer ${token}
   │
   ├─► Step 2b: HTTP Request - PUT /api/users/me
   │     └─► Header: Authorization: Bearer ${token}
   │     └─► Body: Cập nhật name, phone, address
   │
   ├─► Step 3a: HTTP Request - GET /api/products
   │     └─► JSON Extractor: Trích xuất ngẫu nhiên 1 sản phẩm:
   │           - ${productId}    = $[0].id
   │           - ${productName}  = $[0].name
   │           - ${productPrice} = $[0].price
   │
   ├─► Step 3b: HTTP Request - GET /api/products/${productId} (Xem chi tiết)
   │
   ├─► Step 4: HTTP Request - POST /api/cart
   │     └─► Header: Authorization: Bearer ${token}
   │     └─► Body: { "id": ${productId}, "name": "${productName}", "price": ${productPrice}, "quantity": 1 }
   │
   └─► Step 5: HTTP Request - POST /api/checkout
         └─► Header: Authorization: Bearer ${token}
         └─► Body: { "total_amount": ${productPrice}, "shipping_address": "123 Le Loi, Q1, TP.HCM" }
         └─► JSON Extractor: Trích xuất $.orderId (xác nhận đơn tạo thành công)
```

---

### 6.2 Bảng Ma trận Dependency & Dữ liệu truyền giữa các Request

| Bước | Request | Method & Endpoint | Dữ liệu đầu vào cần thiết | Biến trích xuất (JMeter Extractor) | Phụ thuộc vào |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Login | `POST /api/login` | `email`, `password` (từ CSV Data Set) | `${token}`, `${userId}` | Không phụ thuộc |
| **2a** | Get Profile | `GET /api/users/me` | `${token}` (truyền qua Header Authorization) | Thông tin profile hiện tại | Bước 1 |
| **2b** | Update Profile | `PUT /api/users/me` | `${token}`, `name`, `phone`, `shipping_address` | Không | Bước 1 |
| **3a** | Browse Products | `GET /api/products` | Không | `${productId}`, `${productName}`, `${productPrice}` | Không |
| **3b** | Product Details | `GET /api/products/${productId}`| `${productId}` (trích xuất từ Bước 3a) | Thông tin chi tiết sản phẩm | Bước 3a |
| **4** | Add to Cart | `POST /api/cart` | `${token}`, `${productId}`, `${productName}`, `${productPrice}` | Không | Bước 1 & Bước 3a |
| **5** | Checkout | `POST /api/checkout` | `${token}`, `${productPrice}` (làm `total_amount`), `shipping_address` | `${orderId}` | Bước 1 & Bước 3a (hoặc 4) |

---

### 6.3 Điều kiện để Workflow chạy thành công 100%
1. **Tài khoản hợp lệ:** Mỗi Virtual User phải được cấp một cặp `email` và `password` hợp lệ trong cơ sở dữ liệu và **không** nằm trong trạng thái bị khóa (`locked_until` là null hoặc thời gian đã qua).
2. **Truyền Token thông suốt:** `token` trích xuất từ Bước 1 phải được đưa vào `HTTP Header Manager` ở các bước 2a, 2b, 4, 5 dưới dạng `Authorization: Bearer ${token}`.
3. **Tính sẵn sàng của dữ liệu sản phẩm:** Bảng `products` phải có ít nhất 1 sản phẩm còn tồn tại để Bước 3a có dữ liệu trích xuất cho Bước 4 và Bước 5.
4. **Không gọi API không tồn tại:** Tuyệt đối không đưa các request "Update Cart" (`PUT /api/cart`) vào workflow vì endpoint này không tồn tại trên backend.

---

## 7. Performance Testing Risks & Mitigations (Rủi ro & Biện pháp)

| STT | Rủi ro phát hiện từ mã nguồn | Tác động đến kết quả kiểm thử | Biện pháp xử lý trong JMeter & Môi trường |
| :--- | :--- | :--- | :--- |
| **1** | **Xung đột tài khoản & Khóa hàng loạt** (Account Lockout) | Khi dùng chung tài khoản, sai mật khẩu 2 lần sẽ khóa 3 phút, làm chết toàn bộ thread khác. | Chuẩn bị danh sách tài khoản riêng cho từng VU bằng `CSV Data Set Config`. Đảm bảo 100% mật khẩu trong CSV là chính xác. |
| **2** | **SQLite File Lock (`SQLITE_BUSY`)** | Khi chạy tải cao với nhiều thread ghi đồng thời (`checkout`, `update profile`), SQLite bị lock gây spike lỗi 500. | Sử dụng Ramp-up Time hợp lý. Ghi nhận ngưỡng chịu tải tối đa (Endurance/Stress threshold) khi xuất hiện lỗi lock. |
| **3** | **Memory Leak ở `userCarts`** | Bộ nhớ Node.js phình to do giỏ hàng in-memory không được giải phóng sau checkout, gây crash server khi Stress test. | Theo dõi sát sao dung lượng RAM của tiến trình Node.js bằng htop / Task Manager trong suốt quá trình chạy test. |
| **4** | **Tràn dữ liệu đơn hàng (Data Accumulation)** | Bảng `orders` tăng kích thước liên tục, làm các bài test sau chạy chậm hơn bài test trước dù cùng cấu hình. | Chạy lại lệnh `node database.js` để reset dữ liệu mẫu về trạng thái ban đầu trước mỗi đợt test (trước Load, Stress, Spike). |
| **5** | **Deliberate Bug: Giá sản phẩm ID chẵn là String** | Response assertion kiểm tra kiểu số nguyên của trường `price` sẽ thất bại giả (False Alarm) khi xem chi tiết sản phẩm ID chẵn. | Cấu hình Assertion trong JMeter linh hoạt (kiểm tra regex hoặc kiểm tra sự tồn tại của trường `price`). |
| **6** | **Nút thắt Loopback Network / Port Exhaustion** | Chạy JMeter và SUT trên cùng một máy với tải hàng nghìn RPS có thể gây cạn kiệt cổng TCP cục bộ (TIME_WAIT). | Bật `HTTP Keep-Alive` trong JMeter HTTP Request Defaults; cấu hình timeout hợp lý (Connect Timeout: 5000ms, Response Timeout: 10000ms). |

---

## 8. Unverified Information & Assumptions (Phân loại Thông tin)

Nhằm tuân thủ nguyên tắc tính xác thực và minh bạch của bài tập HW05, toàn bộ thông tin được phân loại rõ ràng:

### 8.1 Thông tin đã xác minh 100% từ Source Code (Verified Facts)
* Toàn bộ mã nguồn backend là Express.js 5.2.1 và database là SQLite3 đơn file `database.sqlite`.
* Các endpoint hiện hữu, HTTP Method, headers và cấu trúc payload JSON.
* Token JWT được ký không có thời hạn hết hạn (`jwt.sign` không có `expiresIn`).
* Khóa tài khoản kích hoạt sau 2 lần đăng nhập sai (`login_attempts + 2 >= 3`) và thời gian khóa là 3 phút (180,000ms).
* Giỏ hàng lưu trên bộ nhớ RAM tiến trình Node.js (`userCarts`), không lưu vào SQLite.
* Khi `POST /api/checkout`, server chỉ ghi đơn hàng vào bảng `orders` với `user_id` và `total_amount`, không lưu chi tiết các mặt hàng trong đơn và không xóa giỏ hàng in-memory.
* Không có kiểm tra phân quyền vai trò (Role check) ở bất kỳ endpoint admin nào; bất kỳ token hợp lệ nào cũng gọi được API admin.

### 8.2 Thông tin không tìm thấy (NOT FOUND)
* **API Cập nhật Giỏ hàng (Update Cart):** **NOT FOUND** trong mã nguồn backend (chỉ có thao tác xử lý nội bộ phía client React).
* **API Xóa sản phẩm khỏi Giỏ hàng (Delete Cart Item):** **NOT FOUND** trong backend.
* **Thời hạn hết hạn của Token:** **NOT FOUND** (Mặc định vô thời hạn).
* **Quản lý tồn kho (Inventory/Stock):** **NOT FOUND** (Hệ thống không quản lý số lượng sản phẩm trong kho; không có cột `stock` hay trừ kho khi checkout).
* **Bảng chi tiết đơn hàng (`order_items`):** **NOT FOUND** trong cơ sở dữ liệu.

### 8.3 Giả định kỹ thuật (Assumptions)
* **Giả định về Payload Add to Cart:** Mặc dù server chấp nhận bất kỳ JSON body nào vào `POST /api/cart`, ta giả định body chuẩn gồm `{ "id": number, "name": string, "price": number, "quantity": number }` để mô phỏng chính xác hành vi của ứng dụng theo tài liệu đặc tả `api_specification.md`.
* **Giả định về Checkout:** Mặc dù client web không truyền `shipping_address`, ta giả định kịch bản kiểm thử hiệu năng API sẽ truyền đủ `{ "total_amount": number, "shipping_address": string }` để kiểm tra khả năng lưu trữ toàn vẹn dữ liệu của backend.

---

## 9. Kết luận (Conclusion)

### ĐÁNH GIÁ TÍNH KHẢ THI: **ĐỦ ĐIỀU KIỆN (FEASIBLE)**

Workflow kiểm thử:
$$\text{Login} \longrightarrow \text{Manage Profile} \longrightarrow \text{Browse Products} \longrightarrow \text{Add to Cart} \longrightarrow \text{Checkout}$$
**hoàn toàn đủ điều kiện và khả thi** để thiết kế và triển khai kịch bản kiểm thử hiệu năng bằng **Apache JMeter**, với các lưu ý kỹ thuật mang tính quyết định:

1. **Về luồng API:** Chuỗi tương tác giữa các API hoàn toàn logic và thông suốt. Dữ liệu đầu ra của các bước trước (JWT token, product info) được trích xuất và truyền mượt mà vào các bước sau.
2. **Về bước Cart:** Bỏ qua endpoint "Update Cart" (do backend không hỗ trợ). Bước "Add to Cart" gọi `POST /api/cart` trước khi gọi `POST /api/checkout` nhằm phản ánh đúng tải nghiệp vụ của hệ thống.
3. **Cấu hình dữ liệu Test trong JMeter:**
   * Bắt buộc tạo bộ dữ liệu nhiều tài khoản người dùng độc lập để tránh cơ chế Account Lockout.
   * Cần có quy trình reset cơ sở dữ liệu (`node database.js`) trước mỗi phiên chạy Load / Stress / Spike để đảm bảo tính nhất quán của kết quả đo lường.
