# TC-FR-17-3: Tạo mã giảm giá hợp lệ với loại cố định

## Requirement ID
TC-FR-17-3

## Module / Test type / Technique
Coupon management (CRUD) / Functional / Domain testing

## Preconditions
- Admin đã đăng nhập

## Test data
| Mã | "VIP50" |
| Loại | cố định |
| Giá trị | 50000 |
| Đơn tối thiểu | 100000 |
| Hết hạn | 2099-12-31 |
| Giới hạn/người | 10 |

## Test steps
1. Đăng nhập tài khoản admin
2. Mở trang quản lý mã giảm giá
3. Điền thông tin vào form tạo mã giảm giá
4. Bấm "Tạo mã"

## Expected result
- Hiển thị thông báo tạo thành công.
- Mã giảm giá xuất hiện trong danh sách.

## Status / Related bugs
Pass / None
