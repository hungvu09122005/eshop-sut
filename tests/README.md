# Bảng tự đánh giá
|No. |Criteria |Grade |Self-Assessed Grade|
| --- | --- | --- | --- |   
|1 |Feature A (Domain + Boundary) | 25| 25|
|2 |Feature B (Domain + Boundary) | 25| 25|
|3 |Feature C (Domain + Boundary) | 25| 25|
|4 |Feature D (Mobile, Domain + Boundary) |15| 15|
|5 |Agent Skills |10| 10|
|  |Total |100| 100|

# Tóm tắt kiểm thử.

- Số lượng tính năng: 4.
- Số lượng ca kiểm thử đã thiết kế: 53
- Số lượng ca kiểm thử đã thực thi: 53
- Số lượng ca kiểm thử đạt: 29
- Số lượng ca kiểm thử không đạt: 24
- Số lượng ca kiểm thử chưa thực thi: 0

# Các lỗi tìm được.
Được ghi chi tiết trên Github Issues: https://github.com/KTPM2026/HW2/issues

- [BUG][FR-06] Có thể thêm vào giỏ hàng với số lượng âm
- [BUG][FR-06] lỗi khi nhập số lượng là số thực
- [BUG][FR-06] Có thể thêm vào giỏ hàng với số lượng là chữ
- [BUG][FR-06] Có thể thêm vào giỏ hàng với số lượng là kí tự đặc biệt
- [BUG][FR-06] Có thể thêm vào giỏ hàng với số lượng là rỗng
- [BUG][FR-06] Có thể thêm vào giỏ hàng với số lượng là 0
- [BUG][FR-11] Có thể hủy đơn hàng với trạng thái đang giao.
- [BUG][FR-17] Tạo mã giảm giá với giá trị âm là -50
- [BUG][FR-17] Tạo mã giảm giá với đơn tối thiểu âm là -100000
- [BUG][FR-17] Tạo mã giảm giá với đơn tối thiểu rỗng
- [BUG][FR-17] Tạo mã giảm giá với ngày hết hạn trong quá khứ
- [BUG][FR-17] Tạo mã giảm giá với giới hạn/người rỗng
- [BUG][FR-17] Tạo mã giảm giá với giá trị dưới biên dưới là -1.00001
- [BUG][FR-17] Tạo mã giảm giá với đơn tối thiểu tại biên dưới là -1
- [BUG][FR-17] Tạo mã giảm giá với ngày hết hạn trước ngày hiện tại là 2026-10-06
- [BUG][MOBILE-FR-06] Không hiển thị trang product để có thể vào trang detail