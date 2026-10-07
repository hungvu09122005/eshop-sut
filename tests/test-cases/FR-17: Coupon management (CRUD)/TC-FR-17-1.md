# TC-FR-17-1: Tạo mã giảm giá hợp lệ với loại phần trăm

## Requirement ID
TC-FR-17-1

## Module / Test type / Technique
Coupon management (CRUD) / Functional / Domain testing

## Preconditions
- Admin đã đăng nhập

## Test data
| Mã | "VIP50" |
| Loại | phần trăm |
| Giá trị | 50 |
| Đơn tối thiểu | 100000 |
| Hết hạn | 2099-12-31 |
| Giới hạn/người | 10 |

## Test steps
1. Mở trang quản lý mã giảm giá
2. Điền thông tin vào form tạo mã giảm giá
3. Bấm "Tạo mã"

## Expected result
- Mã giảm giá xuất hiện trong danh sách.

## Status / Related bugs
Pass / None
