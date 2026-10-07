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