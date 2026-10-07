# TC-FR-17-5: Tạo mã giảm giá với giá trị âm là -50

## Requirement ID
TC-FR-17-5

## Module / Test type / Technique
Coupon management (CRUD) / Functional / Domain testing

## Preconditions
- Admin đã đăng nhập

## Test data
| Mã | VIP50 |
| Loại | phần trăm |
| Giá trị | -50 |
| Đơn tối thiểu | 100000 |
| Hết hạn | 2099-12-31 |
| Giới hạn/người | 10 |

## Test steps
1. Đăng nhập tài khoản admin
2. Mở trang quản lý mã giảm giá
3. Điền thông tin vào form tạo mã giảm giá
4. Bấm "Tạo mã"

## Expected result
- Hiển thị thông báo lỗi.
- Mã giảm giá không được tạo.

## Status / Related bugs
Fail / #8
