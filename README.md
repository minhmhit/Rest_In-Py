# Ứng dụng quản lý nhà trọ sử dụng python

## Quản lý thông tin phòng trọ:

Thêm, sửa, xóa thông tin các phòng (số phòng, tình trạng phòng...).
Quản lý trạng thái phòng (đang thuê, còn trống, đang sửa chữa...).
Phân loại phòng theo loại hình (phòng đơn, phòng đôi, căn hộ mini...).
Quản lý thông tin khách thuê:

Lưu trữ thông tin chi tiết của khách thuê (Họ tên, CCCD/CMND, số điện thoại, ngày sinh, nghề nghiệp, quê quán...).
Lưu trữ ảnh chân dung của khách thuê phục vụ cho tính năng nhận diện.
Quản lý lịch sử thuê trọ của từng khách.
Ghi chú các thông tin đặc biệt về khách thuê (nếu có).
Quản lý hợp đồng thuê trọ:

Tạo và lưu trữ hợp đồng thuê trọ điện tử.
Quản lý thời hạn hợp đồng, ngày hết hạn hợp đồng.
Cảnh báo khi hợp đồng sắp hết hạn.
Lưu trữ các điều khoản trong hợp đồng.
Quản lý thu chi:

Lập hóa đơn tiền thuê hàng tháng (tiền phòng, điện, nước, dịch vụ khác...).
Tính toán tự động các khoản phí dựa trên cấu hình giá.
Ghi nhận các khoản thu khác (tiền cọc, phí phạt...).
Ghi nhận các khoản chi (sửa chữa, bảo trì...).
Thống kê và báo cáo thu chi theo tháng, quý, năm.
Nhắc nhở thanh toán tiền nhà hàng tháng cho khách thuê.
Quản lý điện, nước và các dịch vụ khác:

Nhập chỉ số công tơ điện, nước hàng tháng.
Tính toán số tiền điện, nước tiêu thụ theo giá quy định.
Quản lý các khoản phí dịch vụ khác (internet, rác, vệ sinh...).
Quản lý yêu cầu và phản hồi từ khách thuê:

Tiếp nhận yêu cầu sửa chữa, bảo trì từ khách thuê thông qua ứng dụng.
Quản lý trạng thái xử lý các yêu cầu.
Gửi thông báo về tình hình xử lý yêu cầu cho khách thuê.
Thông báo và liên lạc:

Gửi thông báo chung đến tất cả hoặc từng nhóm khách thuê (lịch sửa chữa điện nước, thông báo thu tiền...).
Hỗ trợ trò chuyện trực tiếp giữa chủ trọ và khách thuê qua ứng dụng.
II. Chức Năng Tích Hợp Camera Kiểm Tra Nhận Diện Khách:

## Tích hợp camera an ninh:

Kết nối ứng dụng với hệ thống camera an ninh lắp đặt tại các khu vực ra vào chính của nhà trọ (cổng, cửa ra vào khu nhà...).
Xem trực tiếp (live stream) hình ảnh từ camera trên ứng dụng.
Xem lại lịch sử video đã ghi hình.
Quản lý danh sách khuôn mặt:

Tạo cơ sở dữ liệu khuôn mặt của khách thuê đã đăng ký.
Cập nhật, chỉnh sửa thông tin và ảnh khuôn mặt của khách thuê.
Nhận diện khuôn mặt khách ra vào:

Hệ thống sử dụng camera để quét và nhận diện khuôn mặt của người ra vào khu vực được giám sát.
So sánh khuôn mặt được nhận diện với cơ sở dữ liệu khuôn mặt khách thuê.
Kiểm tra và xác thực khách ra vào:

Đối với khách đã đăng ký: Nếu khuôn mặt trùng khớp với dữ liệu trong hệ thống, ghi nhận thời gian ra/vào của khách thuê đó. Có thể tích hợp với hệ thống khóa cửa thông minh để tự động mở cửa cho khách hợp lệ.
Đối với người lạ: Nếu khuôn mặt không có trong cơ sở dữ liệu, hệ thống đưa ra cảnh báo (báo động, gửi thông báo đến chủ trọ/người quản lý).
Ghi lại lịch sử ra vào bằng hình ảnh/video:

Lưu lại hình ảnh hoặc đoạn video của những người ra vào cùng với thông tin thời gian và kết quả nhận diện.
Cung cấp khả năng tìm kiếm lịch sử ra vào theo thời gian hoặc theo khuôn mặt (nếu nhận diện được).
Cảnh báo an ninh:

Cảnh báo khi phát hiện người lạ hoặc có hành vi đáng ngờ tại khu vực camera giám sát.
Cảnh báo khi có người cố gắng truy cập trái phép.
Quản lý quyền truy cập (nếu tích hợp khóa cửa thông minh):

Phân quyền ra vào cho từng khách thuê dựa trên hợp đồng hoặc cài đặt của chủ trọ.
Thu hồi quyền truy cập khi khách thuê chuyển đi.
