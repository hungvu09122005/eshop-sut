# HW02 – Domain Testing

**MỤC LỤC**

[**1\. FR-06: Product detail view.**](#1-fr-06-product-detail-view)

[**2\. FR-11: Order history view (user).**](#2-fr-11-order-history-view-user)

[**3\. Web Admin - FR-17: Coupon management (CRUD)**](#3-web-admin---fr-17-coupon-management-crud)

[**4\. Mobile App - FR-17: Coupon management (CRUD)**](#4-mobile-app---fr-17-coupon-management-crud)

[**5\. Mandatory Disclosure**](#5-mandatory-disclosure)

[**Phụ lục**](#phụ-lục)

[**TÀI LIỆU THAM KHẢO**](#tài-liệu-tham-khảo)

#

## 1. FR-06: Product detail view.

Bước 1: xác định các input, output và xác định miền.
Input:
 - Số lượng: số nguyên >= 1, số  nguyên < 1, số thực, ký tự đặc biệt, chữ cái, rỗng.
Output:
 - Số lượng không hợp lệ.
 - Thêm giỏ hàng thành công.

Bước 2: Chọn giá trị đại diện cho miền.
  - Số lượng: 5

Bước 3: thiết kế các test cases theo Domain testing.

| ID |Số lượng |Expected result 
| --- | --- | ---|
| TC-FR-06-1| 5 | Thêm giỏ hàng thành công.|
| TC-FR-06-2| -5 | Số lượng không hợp lệ.|
| TC-FR-06-3| 5.5 | Số lượng không hợp lệ.|
| TC-FR-06-4| "a" | Số lượng không hợp lệ.|
| TC-FR-06-5| "@" | Số lượng không hợp lệ.|
| TC-FR-06-6| "" | Số lượng không hợp lệ.|

Bước 4: Rút gọn test cases theo Domain testing.
  - Không cần rút gọn test case.

Bước 5: thiết kế các test cases theo BVA 3 points.
  - Ta có giá trị biên ở số lượng là 1. Do đó, ta có test case.
| ID |Số lượng |Expected result 
| --- | --- | ---|
| TC-FR-06-7| 2 | Thêm giỏ hàng thành công.| 
| TC-FR-06-8| 1 | Thêm giỏ hàng thành công.| 
| TC-FR-06-9| 0 | Số lượng không hợp lệ.| 

## 2. FR-11: Order history view (user).

Bước 1: xác định các output và xác định miền.
Input:
 - Trạng thái: Chờ xác nhận, Đã xác nhận, Đang giao, Đã giao, Đã hủy.
Output:
 - Hủy thành công.
 - Không thể hủy.

Bước 2: Chọn giá trị đại diện cho miền.
 - Trạng thái: Chờ xác nhận.

Bước 3: thiết kế các test cases theo Domain testing.

| ID |Trạng thái |Expected result 
| --- | --- | ---|
| TC-FR-11-1| Chờ xác nhận | Hủy thành công.|
| TC-FR-11-2| Đã xác nhận | Hủy thành công.|
| TC-FR-11-3| Đang giao | Không thể hủy.|
| TC-FR-11-4| Đã giao | Không thể hủy.|
| TC-FR-11-5| Đã hủy | Không thể hủy.|


Bước 4: Rút gọn test cases theo Domain testing.
  - Không cần rút gọn test case.

Bước 5: thiết kế các test cases theo BVA 3 points.
  - Không thể dùng BVA vì ở tính năng này không có miền giá trị liên tục để xác định biên.

## 3. Web Admin - FR-17: Coupon management (CRUD)**

Bước 1: xác định các output và xác định miền.
Input:
  - Mã: có giá trị, rỗng
  - Loại: phần trăm, cố định
  - Giá trị: >0, <=0, rỗng, ký tự đặc biệt, chữ cái.
  - Đơn tối thiểu: >=0, <0, rỗng, ký tự đặc biệt, chữ cái.
  - Hết hạn: Ngày >= hiện tại, ngày quá khứ, rỗng.
  - Giới hạn/người: nguyên >0, nguyên <=0, số thực, rỗng, ký tự đặc biệt, chữ cái.

Output:
  - Tạo thành công
  - Tạo thất bại

Bước 2: Chọn giá trị đại diện cho miền.
  - Mã: VIP50
  - Loại: phần trăm
  - Giá trị: 50
  - Đơn tối thiểu: 100000
  - Hết hạn: 2099-12-31
  - Giới hạn/người: 10

Bước 3: thiết kế các test cases.

| ID |Mã |Loại |Giá trị |Đơn tối thiểu |Hết hạn |Giới hạn/người |Expected result 
| --- | --- | --- | --- | --- | --- | --- | ---|
| TC-FR-17-1| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 10 | Tạo thành công.| 
| TC-FR-17-2| "" | phần trăm | 50 | 100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-3| "VIP50" | cố định | 50000 | 100000 | 2099-12-31 | 10 | Tạo thành công.| 
| TC-FR-17-4| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 10 | Tạo thành công.|
| TC-FR-17-5| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 10 | Tạo thành công.|  
| TC-FR-17-6| VIP50 | phần trăm | "" | 100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-7| VIP50 | phần trăm | -50 | 100000 | 2099-12-31 | 10 | Tạo thất bại.|
| TC-FR-17-8| VIP50 | phần trăm | "a" | 100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-9| VIP50 | phần trăm | "@" | 100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-10| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 10 | Tạo thành công.| 
| TC-FR-17-11| VIP50 | phần trăm | 50 | "" | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-12| VIP50 | phần trăm | 50 | -100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-13| VIP50 | phần trăm | 50 | "a" | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-14| VIP50 | phần trăm | 50 | "@" | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-15| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 10 | Tạo thành công.| 
| TC-FR-17-16| VIP50 | phần trăm | 50 | 100000 | "" | 10 | Tạo thất bại.| 
| TC-FR-17-17| VIP50 | phần trăm | 50 | 100000 | 2000-01-01 | 10 | Tạo thất bại.| 
| TC-FR-17-18| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 10 | Tạo thành công.| 
| TC-FR-17-19| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | "" | Tạo thất bại.| 
| TC-FR-17-20| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | -10 | Tạo thất bại.| 
| TC-FR-17-21| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | 10.5 | Tạo thất bại.| 
| TC-FR-17-22| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | "a" | Tạo thất bại.| 
| TC-FR-17-23| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | "@" | Tạo thất bại.| 

Bước 4: Rút gọn test cases theo Domain testing

| ID |Mã |Loại |Giá trị |Đơn tối thiểu |Hết hạn |Giới hạn/người |Expected result 
| --- | --- | --- | --- | --- | --- | --- | ---|
| TC-FR-17-1| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 10 | Tạo thành công.| 
| TC-FR-17-2| "" | phần trăm | 50 | 100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-3| "VIP50" | cố định | 50000 | 100000 | 2099-12-31 | 10 | Tạo thành công.|
| TC-FR-17-4| VIP50 | phần trăm | "" | 100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-5| VIP50 | phần trăm | -50 | 100000 | 2099-12-31 | 10 | Tạo thất bại.|
| TC-FR-17-6| VIP50 | phần trăm | "a" | 100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-7| VIP50 | phần trăm | "@" | 100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-8| VIP50 | phần trăm | 50 | "" | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-9| VIP50 | phần trăm | 50 | -100000 | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-10| VIP50 | phần trăm | 50 | "a" | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-11| VIP50 | phần trăm | 50 | "@" | 2099-12-31 | 10 | Tạo thất bại.| 
| TC-FR-17-12| VIP50 | phần trăm | 50 | 100000 | "" | 10 | Tạo thất bại.| 
| TC-FR-17-13| VIP50 | phần trăm | 50 | 100000 | 2000-01-01 | 10 | Tạo thất bại.| 
| TC-FR-17-14| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | "" | Tạo thất bại.| 
| TC-FR-17-15| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | -10 | Tạo thất bại.| 
| TC-FR-17-16| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | 10.5 | Tạo thất bại.| 
| TC-FR-17-17| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | "a" | Tạo thất bại.| 
| TC-FR-17-18| VIP50 | phần trăm | 50 | 100000 | 2099-12-31 | "@" | Tạo thất bại.| 

Bước 5: thiết kế các test cases theo BVA 3 points.
Ta có giá trị biên ở
  - Giá trị: 0.00001.
  - Đơn tối thiểu: 0.
  - Hết hạn: 2026-10-7, giả sử ngày hiện tại là 2026-10-07.
  - Giới hạn/người: 1.

| ID |Mã |Loại |Giá trị |Đơn tối thiểu |Hết hạn |Giới hạn/người |Expected result 
| --- | --- | --- | --- | --- | --- | --- | ---|
| TC-FR-17-19| "VIP50" | phần trăm | 0.00001 | 100000 | 2099-12-31 | 10 | Tạo thành công.|
| TC-FR-17-20| "VIP50" | phần trăm | 1.00001 | 100000 | 2099-12-31 | 10 | Tạo thành công.|
| TC-FR-17-21| "VIP50" | phần trăm | -1.00001 | 100000 | 2099-12-31 | 10 | Tạo thất bại.|
| TC-FR-17-22| "VIP50" | phần trăm | 50 | 0 | 2099-12-31 | 10 | Tạo thành công.|
| TC-FR-17-23| "VIP50" | phần trăm | 50 | 1 | 2099-12-31 | 10 | Tạo thành công.|
| TC-FR-17-24| "VIP50" | phần trăm | 50 | -1 | 2099-12-31 | 10 | Tạo thất bại.|
| TC-FR-17-25| "VIP50" | phần trăm | 50 | 100000 | 2026-10-7 | 10 | Tạo thành công.|
| TC-FR-17-26| "VIP50" | phần trăm | 50 | 100000 | 2026-10-8 | 10 | Tạo thành công.|
| TC-FR-17-27| "VIP50" | phần trăm | 50 | 100000 | 2026-10-6 | 10 | Tạo thất bại.|
| TC-FR-17-28| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 1 | Tạo thành công.|
| TC-FR-17-29| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 2 | Tạo thành công.|
| TC-FR-17-30| "VIP50" | phần trăm | 50 | 100000 | 2099-12-31 | 0 | Tạo thất bại.|

