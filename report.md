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