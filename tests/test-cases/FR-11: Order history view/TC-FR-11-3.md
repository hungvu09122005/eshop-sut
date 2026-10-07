# TC-FR-11-3:Hủy đơn hàng với trạng thái đang giao.

## Requirement ID
TC-FR-11-3

## Module / Test type / Technique
Order history view/ Functional / Domain testing

## Preconditions
- User đã đăng nhập
- Có đơn hàng với trạng thái đang giao

## Test data
| Trạng thái | Đang giao |

## Test steps
1. Mở trang quản lý đơn hàng
2. Tìm đơn hàng có trạng thái đang giao
3. Bấm "Hủy đơn hàng"

## Expected result
- Hiển thị thông báo "Không thể hủy đơn hàng".

## Status / Related bugs
Fail / #7