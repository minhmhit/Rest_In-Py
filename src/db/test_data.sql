-- Dữ liệu do AI tạo :vv

USE QuanLyNhaTro;
-- Thêm dữ liệu phòng
INSERT INTO Phong (SoPhong, MoTa, GiaThue, TrangThai) VALUES
('P101', 'Phong co ban, 1 phong ngu, 1 phong tam', 2500000, 'DaThue'),
('P102', 'Phong co ban, 1 phong ngu, 1 phong tam', 2500000, 'DaThue'),
('P103', 'Phong co ban, 1 phong ngu, 1 phong tam', 2500000, 'DaThue'),
('P201', 'Phong rong, 2 phong ngu, 1.5 phong tam', 3200000, 'DaThue'),
('P202', 'Phong rong, 2 phong ngu, 1.5 phong tam', 3200000, 'DaThue'),
('P203', 'Phong rong, 2 phong ngu, 1.5 phong tam', 3200000, 'DaThue'),
('P301', 'Phong vip, 2 phong ngu, 2 phong tam', 3800000, 'DaThue'),
('P302', 'Phong vip, 2 phong ngu, 2 phong tam', 3800000, 'DaThue'),
('P303', 'Phong vip, 2 phong ngu, 2 phong tam', 3800000, 'DaThue'),
('P401', 'Phong thuong, 1 phong ngu, 1 phong tam', 2700000, 'DaThue'),
('P402', 'Phong thuong, 1 phong ngu, 1 phong tam', 2700000, 'DaThue'),
('P403', 'Phong thuong, 1 phong ngu, 1 phong tam', 2700000, 'DaThue'),
('P501', 'Phong studio, 1 phong ngu lon', 2900000, 'DaThue'),
('P502', 'Phong studio, 1 phong ngu lon', 2900000, 'DaThue'),
('P503', 'Phong studio, 1 phong ngu lon', 2900000, 'DaThue'),
('P601', 'Phong gia dinh, 3 phong ngu, 2 phong tam', 4500000, 'DaThue'),
('P602', 'Phong gia dinh, 3 phong ngu, 2 phong tam', 4500000, 'DaThue'),
('P603', 'Phong penthouse, 2 phong ngu, view dep', 5000000, 'DaThue'),
('P701', 'Phong don, 1 phong ngu nho', 2200000, 'DaThue'),
('P702', 'Phong don, 1 phong ngu nho', 2200000, 'Trong');

-- Thêm dữ liệu người thuê
INSERT INTO NguoiThue (HoTen, SoCMND, SoDienThoai, Email) VALUES
('Nguyen Van Anh', '012345678', '0901234567', 'vananh@email.com'),
('Tran Thi Binh', '023456789', '0912345678', 'thibinh@email.com'),
('Le Van Cuong', '034567890', '0923456789', 'vancuong@email.com'),
('Pham Thi Dung', '045678901', '0934567890', 'thidung@email.com'),
('Hoang Van Em', '056789012', '0945678901', 'vanem@email.com'),
('Vo Thi Giang', '067890123', '0956789012', 'thigiang@email.com'),
('Dang Van Hung', '078901234', '0967890123', 'vanhung@email.com'),
('Bui Thi Huong', '089012345', '0978901234', 'thihuong@email.com'),
('Nguyen Van Kien', '090123456', '0989012345', 'vankien@email.com'),
('Tran Thi Lan', '001234567', '0990123456', 'thilan@email.com'),
('Phan Van Minh', '112345678', '0901234568', 'vanminh@email.com'),
('Duong Thi Nga', '123456789', '0912345679', 'thinga@email.com'),
('Le Van Oanh', '134567890', '0923456780', 'vanoanh@email.com'),
('Huynh Thi Phuong', '145678901', '0934567891', 'thiphuong@email.com'),
('Tran Van Quang', '156789012', '0945678902', 'vanquang@email.com'),
('Mai Thi Rung', '167890123', '0956789013', 'thirung@email.com'),
('Dinh Van Son', '178901234', '0967890124', 'vanson@email.com'),
('Vu Thi Thanh', '189012345', '0978901235', 'thithanh@email.com'),
('Do Van Uyen', '190123456', '0989012346', 'vanuyen@email.com'),
('Ly Thi Van', '201234567', '0990123457', 'thivan@email.com'),
('Nguyen Van Xuong', '212345678', '0901234569', 'vanxuong@email.com'),
('Tran Thi Yen', '223456789', '0912345670', 'thiyen@email.com'),
('Cao Van Zung', '234567890', '0923456781', 'vanzung@email.com'),
('Pham Thi Hoa', '245678901', '0934567892', 'thihoa@email.com'),
('Hoang Van Tuan', '256789012', '0945678903', 'vantuan@email.com'),
('Nguyen Thi Mai', '267890123', '0956789014', 'thimai@email.com'),
('Trinh Van Nam', '278901234', '0967890125', 'vannam@email.com'),
('Vu Thi Oanh', '289012345', '0978901236', 'thioanh@email.com'),
('Tran Van Phuc', '290123456', '0989012347', 'vanphuc@email.com'),
('Le Thi Quynh', '301234567', '0990123458', 'thiquynh@email.com'),
('Nguyen Van Tri', '312345678', '0901234560', 'vantri@email.com'),
('Pham Thi Linh', '323456789', '0912345671', 'thilinh@email.com'),
('Tran Van Hung', '334567890', '0923456782', 'vanhung2@email.com'),
('Nguyen Thi Ha', '345678901', '0934567893', 'thiha@email.com'),
('Le Van Duc', '356789012', '0945678904', 'vanduc@email.com'),
('Ho Thi Thu', '367890123', '0956789015', 'thithu@email.com'),
('Nguyen Van Hai', '378901234', '0967890126', 'vanhai@email.com'),
('Vu Thi Hong', '389012345', '0978901237', 'thihong@email.com'),
('Doan Van Khanh', '390123456', '0989012348', 'vankhanh@email.com'),
('Nguyen Thi Lien', '401234567', '0990123459', 'thilien@email.com'),
('Tran Quoc Toan', '412345678', '0901234561', 'quoctoan@email.com'),
('Nguyen Thi Thu', '423456789', '0912345672', 'thithu2@email.com'),
('Pham Van Vinh', '434567890', '0923456783', 'vanvinh@email.com'),
('Nguyen Thi Xuan', '445678901', '0934567894', 'thixuan@email.com'),
('Tran Van Yen', '456789012', '0945678905', 'vanyen@email.com'),
('Nguyen Thi Kim', '467890123', '0956789016', 'thikim@email.com'),
('Le Van Long', '478901234', '0967890127', 'vanlong@email.com'),
('Pham Thi My', '489012345', '0978901238', 'thimy@email.com'),
('Nguyen Van Ninh', '490123456', '0989012349', 'vanninh@email.com'),
('Tran Thi Oanh', '501234567', '0990123450', 'thioanh2@email.com');

-- Thêm dữ liệu hợp đồng (2-3 người/phòng)
-- Phòng P101 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(1, 1, '2024-01-01', '2024-12-31'),
(2, 1, '2024-01-01', '2024-12-31');

-- Phòng P102 - 3 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(3, 2, '2024-01-15', '2025-01-14'),
(4, 2, '2024-01-15', '2025-01-14'),
(5, 2, '2024-01-15', '2025-01-14');

-- Phòng P103 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(6, 3, '2024-02-01', '2025-01-31'),
(7, 3, '2024-02-01', '2025-01-31');

-- Phòng P201 - 3 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(8, 4, '2024-01-05', '2024-12-31'),
(9, 4, '2024-01-05', '2024-12-31'),
(10, 4, '2024-01-05', '2024-12-31');

-- Phòng P202 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(11, 5, '2024-02-10', '2025-02-09'),
(12, 5, '2024-02-10', '2025-02-09');

-- Phòng P203 - 3 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(13, 6, '2024-01-20', '2024-12-31'),
(14, 6, '2024-01-20', '2024-12-31'),
(15, 6, '2024-01-20', '2024-12-31');

-- Phòng P301 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(16, 7, '2024-03-01', '2025-02-28'),
(17, 7, '2024-03-01', '2025-02-28');

-- Phòng P302 - 3 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(18, 8, '2024-02-15', '2025-02-14'),
(19, 8, '2024-02-15', '2025-02-14'),
(20, 8, '2024-02-15', '2025-02-14');

-- Phòng P303 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(21, 9, '2024-01-10', '2024-12-31'),
(22, 9, '2024-01-10', '2024-12-31');

-- Phòng P401 - 3 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(23, 10, '2024-03-15', '2025-03-14'),
(24, 10, '2024-03-15', '2025-03-14'),
(25, 10, '2024-03-15', '2025-03-14');

-- Phòng P402 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(26, 11, '2024-01-25', '2024-12-31'),
(27, 11, '2024-01-25', '2024-12-31');

-- Phòng P403 - 3 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(28, 12, '2024-02-20', '2025-02-19'),
(29, 12, '2024-02-20', '2025-02-19'),
(30, 12, '2024-02-20', '2025-02-19');

-- Phòng P501 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(31, 13, '2024-04-01', '2025-03-31'),
(32, 13, '2024-04-01', '2025-03-31');

-- Phòng P502 - 3 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(33, 14, '2024-03-10', '2025-03-09'),
(34, 14, '2024-03-10', '2025-03-09'),
(35, 14, '2024-03-10', '2025-03-09');

-- Phòng P503 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(36, 15, '2024-01-15', '2024-12-31'),
(37, 15, '2024-01-15', '2024-12-31');

-- Phòng P601 - 3 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(38, 16, '2024-02-05', '2025-02-04'),
(39, 16, '2024-02-05', '2025-02-04'),
(40, 16, '2024-02-05', '2025-02-04');

-- Phòng P602 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(41, 17, '2024-03-20', '2025-03-19'),
(42, 17, '2024-03-20', '2025-03-19');

-- Phòng P603 - 3 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(43, 18, '2024-01-30', '2024-12-31'),
(44, 18, '2024-01-30', '2024-12-31'),
(45, 18, '2024-01-30', '2024-12-31');

-- Phòng P701 - 2 người
INSERT INTO HopDong (MaNguoiThue, MaPhong, NgayBatDau, NgayKetThuc) VALUES
(46, 19, '2024-04-15', '2025-04-14'),
(47, 19, '2024-04-15', '2025-04-14');

-- Phòng P702 trống (không có hợp đồng)

-- Thêm dữ liệu sử dụng dịch vụ - Tháng 1/2024
-- Phòng P101
INSERT INTO SuDungDichVu (MaPhong, MaDichVu, ThangSuDung, ChiSoCu, ChiSoMoi, SoLuong, ThanhTien) VALUES
(1, 1, '2024-01-01', 0, 120, 120, 120 * 4500), -- Điện
(1, 2, '2024-01-01', 0, 7, 7, 7 * 30000), -- Nước
(1, 3, '2024-01-01', NULL, NULL, 1, 200000); -- Internet

-- Phòng P102
INSERT INTO SuDungDichVu (MaPhong, MaDichVu, ThangSuDung, ChiSoCu, ChiSoMoi, SoLuong, ThanhTien) VALUES
(2, 1, '2024-01-01', 0, 180, 180, 180 * 4500), -- Điện
(2, 2, '2024-01-01', 0, 10, 10, 10 * 30000), -- Nước
(2, 3, '2024-01-01', NULL, NULL, 1, 200000); -- Internet

-- Phòng P103
INSERT INTO SuDungDichVu (MaPhong, MaDichVu, ThangSuDung, ChiSoCu, ChiSoMoi, SoLuong, ThanhTien) VALUES
(3, 1, '2024-01-01', 0, 130, 130, 130 * 4500), -- Điện
(3, 2, '2024-01-01', 0, 8, 8, 8 * 30000), -- Nước
(3, 3, '2024-01-01', NULL, NULL, 1, 200000); -- Internet

-- Thêm dữ liệu thanh toán - Tháng 1/2024
INSERT INTO ThanhToan (MaHopDong, ThangThanhToan, TienPhong, TienDichVu, TongTien, NgayThanhToan, TrangThaiThanhToan) VALUES
(1, '2024-01-01', 2500000, 120 * 4500 + 7 * 30000 + 200000, 2500000 + 120 * 4500 + 7 * 30000 + 200000, '2024-01-05', 'DaThanhToan'),
(3, '2024-01-01', 2500000, 180 * 4500 + 10 * 30000 + 200000, 2500000 + 180 * 4500 + 10 * 30000 + 200000, '2024-01-05', 'DaThanhToan'),
(6, '2024-01-01', 2500000, 130 * 4500 + 8 * 30000 + 200000, 2500000 + 130 * 4500 + 8 * 30000 + 200000, '2024-01-06', 'DaThanhToan');

-- Thêm dữ liệu sử dụng dịch vụ - Tháng 2/2024
-- Phòng P101
INSERT INTO SuDungDichVu (MaPhong, MaDichVu, ThangSuDung, ChiSoCu, ChiSoMoi, SoLuong, ThanhTien) VALUES
(1, 1, '2024-02-01', 120, 250, 130, 130 * 4500), -- Điện
(1, 2, '2024-02-01', 7, 14, 7, 7 * 30000), -- Nước
(1, 3, '2024-02-01', NULL, NULL, 1, 200000); -- Internet

-- Phòng P102
INSERT INTO SuDungDichVu (MaPhong, MaDichVu, ThangSuDung, ChiSoCu, ChiSoMoi, SoLuong, ThanhTien) VALUES
(2, 1, '2024-02-01', 180, 350, 170, 170 * 4500), -- Điện
(2, 2, '2024-02-01', 10, 19, 9, 9 * 30000), -- Nước
(2, 3, '2024-02-01', NULL, NULL, 1, 200000); -- Internet

-- Phòng P103
INSERT INTO SuDungDichVu (MaPhong, MaDichVu, ThangSuDung, ChiSoCu, ChiSoMoi, SoLuong, ThanhTien) VALUES
(3, 1, '2024-02-01', 130, 260, 130, 130 * 4500), -- Điện
(3, 2, '2024-02-01', 8, 16, 8, 8 * 30000), -- Nước
(3, 3, '2024-02-01', NULL, NULL, 1, 200000); -- Internet

-- Thêm dữ liệu thanh toán - Tháng 2/2024
INSERT INTO ThanhToan (MaHopDong, ThangThanhToan, TienPhong, TienDichVu, TongTien, NgayThanhToan, TrangThaiThanhToan) VALUES
(1, '2024-02-01', 2500000, 130 * 4500 + 7 * 30000 + 200000, 2500000 + 130 * 4500 + 7 * 30000 + 200000, '2024-02-05', 'DaThanhToan'),
(3, '2024-02-01', 2500000, 170 * 4500 + 9 * 30000 + 200000, 2500000 + 170 * 4500 + 9 * 30000 + 200000, '2024-02-06', 'DaThanhToan'),
(6, '2024-02-01', 2500000, 130 * 4500 + 8 * 30000 + 200000, 2500000 + 130 * 4500 + 8 * 30000 + 200000, '2024-02-07', 'DaThanhToan');