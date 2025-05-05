-- DATABASE NAME = motel

-- Staff table structure
CREATE TABLE staffs (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sex VARCHAR(10),
    birthday DATE,
    role VARCHAR(50),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50),
    permissions VARCHAR(255)
);

INSERT INTO staffs (id, name, sex, birthday, role, username, password, permissions) VALUES
(1, 'Nguyễn Văn A', 'Nam', '1990-01-01', 'Quản Trị Viên', 'admin1', 'admin', 'Toàn quyền'),
(2, 'Lê Thị B', 'Nữ', '1992-03-10', 'Quản Lí', 'recept1', 'recept', 'Đặt phòng, thanh toán'),
(3, 'Trần Văn C', 'Nam', '1985-06-20', 'Nhân Viên', 'guard1', 'guard', 'Camera'),
(4, 'Phạm Thị D', 'Nữ', '1995-02-15', 'Lễ Tân', '1', '1', 'Đặt phòng');
-- (5, 'Hoàng Văn E', 'Nam', '1988-07-21', 'Bảo Vệ', 'guard2', 'guardpass', 'Camera, An ninh'),
-- (6, 'Đặng Thị F', 'Nữ', '1993-11-05', 'Buồng Phòng', 'housekeep1', 'clean1', 'Dọn dẹp'),
-- (7, 'Vũ Văn G', 'Nam', '1991-09-12', 'Quản Lí', 'manager1', 'managepass', 'Quản lý nhân viên, Báo cáo'),
-- (8, 'Lý Thị H', 'Nữ', '1996-04-18', 'Lễ Tân', 'recept3', 'recept456', 'Đặt phòng, check-in'),
-- (9, 'Trịnh Văn I', 'Nam', '1983-12-25', 'Bảo Trì', 'maintain1', 'fixit', 'Sửa chữa'),
-- (10, 'Tô Thị K', 'Nữ', '1998-01-30', 'Buồng Phòng', 'housekeep2', 'clean2', 'Dọn dẹp'),
-- (11, 'Hồ Văn L', 'Nam', '1990-05-09', 'Bảo Vệ', 'guard3', 'secure3', 'An ninh'),
-- (12, 'Mai Thị M', 'Nữ', '1994-08-14', 'Kế Toán', 'account1', 'accpass', 'Thanh toán, Báo cáo'),
-- (13, 'Phùng Văn N', 'Nam', '1987-10-29', 'Lễ Tân', 'recept4', 'recept789', 'Check-out, thanh toán'),
-- (14, 'Đỗ Thị O', 'Nữ', '1999-03-03', 'Buồng Phòng', 'housekeep3', 'clean3', 'Dọn dẹp'),
-- (15, 'Bùi Văn P', 'Nam', '1986-06-17', 'Quản Lí Ca', 'shiftlead1', 'leadpass', 'Quản lý ca, Giám sát'),
-- (16, 'Ngô Thị Q', 'Nữ', '1992-11-22', 'Lễ Tân', 'recept5', 'recept101', 'Đặt phòng, check-in'),
-- (17, 'Lương Văn R', 'Nam', '1989-02-08', 'Bảo Vệ', 'guard4', 'secure4', 'Camera'),
-- (18, 'Lâm Thị S', 'Nữ', '1997-07-11', 'Buồng Phòng', 'housekeep4', 'clean4', 'Dọn dẹp, Kiểm tra phòng'),
-- (19, 'Dương Văn T', 'Nam', '1993-09-19', 'Bảo Trì', 'maintain2', 'fixit2', 'Sửa chữa điện nước'),
-- (20, 'Tạ Thị U', 'Nữ', '1995-12-01', 'Lễ Tân', 'recept6', 'recept112', 'Check-out'),
-- (21, 'Đoàn Văn V', 'Nam', '1984-04-25', 'Bảo Vệ', 'guard5', 'secure5', 'An ninh cổng'),
-- (22, 'Vương Thị X', 'Nữ', '1991-08-28', 'Buồng Phòng', 'housekeep5', 'clean5', 'Dọn dẹp'),
-- (23, 'Châu Văn Y', 'Nam', '1996-10-07', 'Phục Vụ', 'service1', 'servepass', 'Phục vụ ăn uống'),
-- (24, 'Kiều Thị Z', 'Nữ', '1998-05-16', 'Lễ Tân', 'recept7', 'recept131', 'Đặt phòng'),
-- (25, 'Giang Văn AA', 'Nam', '1990-03-20', 'Quản Lí', 'manager2', 'managepass2', 'Tuyển dụng, Đào tạo'),
-- (26, 'Huỳnh Thị BB', 'Nữ', '1994-06-24', 'Buồng Phòng', 'housekeep6', 'clean6', 'Kiểm tra minibar'),
-- (27, 'Mạc Văn CC', 'Nam', '1988-11-11', 'Bảo Vệ', 'guard6', 'secure6', 'Tuần tra'),
-- (28, 'Nhan Thị DD', 'Nữ', '1997-02-14', 'Lễ Tân', 'recept8', 'recept141', 'Giải quyết phàn nàn'),
-- (29, 'Phan Văn EE', 'Nam', '1992-07-07', 'Bảo Trì', 'maintain3', 'fixit3', 'Sửa chữa thiết bị'),
-- (30, 'Quách Thị FF', 'Nữ', '1995-09-09', 'Kế Toán', 'account2', 'accpass2', 'Thu chi'),


-- Customer table structure
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sex VARCHAR(10),
    birthday DATE,
    national VARCHAR(50),
    country VARCHAR(100),
    checkin_date DATE,
    room_type VARCHAR(10),
    room_number INT
);

INSERT INTO customers (id, name, sex, birthday, national, country, checkin_date, room_type, room_number) VALUES
(1, 'Nguyễn Văn An', 'Nam', '1990-05-20', 'Việt Nam', 'Việt Nam', '2025-03-15', 'VIP', 101),
(2, 'Trần Thị Hoa', 'Nữ', '1985-12-15', 'Việt Nam', 'Việt Nam', '2025-01-22', 'Thường', 102),
(3, 'Lê Minh Tú', 'Nam', '1992-07-30', 'Việt Nam', 'Việt Nam', '2025-04-10', 'VIP', 103),
(4, 'Phạm Thùy Dung', 'Nữ', '1998-09-05', 'Việt Nam', 'Việt Nam', '2025-02-28', 'Thường', 104),
(5, 'Hoàng Quốc Bảo', 'Nam', '1987-11-22', 'Việt Nam', 'Việt Nam', '2025-01-05', 'Thường', 105),
(6, 'Đặng Thu Hằng', 'Nữ', '1995-04-18', 'Việt Nam', 'Việt Nam', '2025-03-01', 'Thường', 205),
(7, 'Bùi Quang Huy', 'Nam', '1989-08-12', 'Việt Nam', 'Việt Nam', '2025-04-25', 'Thường', 201),
(8, 'Vũ Ngọc Linh', 'Nữ', '1991-06-25', 'Việt Nam', 'Việt Nam', '2025-02-12', 'Thường', 901),
(9, 'Đoàn Văn Hải', 'Nam', '1984-03-17', 'Việt Nam', 'Việt Nam', '2025-01-18', 'Thường', 401),
(10, 'Lý Thu Trang', 'Nữ', '1993-09-29', 'Việt Nam', 'Việt Nam', '2025-03-29', 'Thường', 505),
(11, 'Phan Thanh Nam', 'Nam', '1996-02-10', 'Việt Nam', 'Việt Nam', '2025-04-18', 'Thường', 402),
(12, 'Ngô Thị Mai', 'Nữ', '1990-07-05', 'Việt Nam', 'Việt Nam', '2025-01-28', 'Thường', 301),
(13, 'Trịnh Quốc Đạt', 'Nam', '1982-12-20', 'Việt Nam', 'Việt Nam', '2025-03-05', 'Thường', 302),
(14, 'Tạ Kim Oanh', 'Nữ', '1999-01-14', 'Việt Nam', 'Việt Nam', '2025-02-19', 'Thường', 303),
(15, 'Dương Hữu Phúc', 'Nam', '1994-05-23', 'Việt Nam', 'Việt Nam', '2025-04-01', 'Thường', 305),
(16, 'Hồ Minh Đức', 'Nam', '1997-11-30', 'Việt Nam', 'Việt Nam', '2025-01-10', 'Thường', 601),
(17, 'Lâm Thị Lan', 'Nữ', '1986-08-18', 'Việt Nam', 'Việt Nam', '2025-03-22', 'Thường', 602),
(18, 'Trần Gia Bảo', 'Nam', '1995-09-08', 'Việt Nam', 'Việt Nam', '2025-02-05', 'Thường', 904),
(19, 'Nguyễn Hồng Nhung', 'Nữ', '1998-04-21', 'Việt Nam', 'Việt Nam', '2025-04-30', 'Thường', 702),
(20, 'Lương Quang Hải', 'Nam', '1980-10-10', 'Việt Nam', 'Việt Nam', '2025-01-15', 'Thường', 804),
(21, 'Mai Thị Hạnh', 'Nữ', '1992-06-12', 'Việt Nam', 'Việt Nam', '2025-03-10', 'Thường', 801),
(22, 'Phùng Văn Thịnh', 'Nam', '1983-03-04', 'Việt Nam', 'Việt Nam', '2025-02-22', 'Thường', 802),
(23, 'Nguyễn Thanh Hương', 'Nữ', '1997-07-27', 'Việt Nam', 'Việt Nam', '2025-04-15', 'Thường', 803),
(24, 'Đỗ Trọng Khang', 'Nam', '1991-09-15', 'Việt Nam', 'Việt Nam', '2025-01-30', 'Thường', 902),
(25, 'Hoàng Mỹ Linh', 'Nữ', '1988-11-09', 'Việt Nam', 'Việt Nam', '2025-03-08', 'Thường', 903),
(26, 'Trịnh Minh Tuấn', 'Nam', '1996-12-01', 'Việt Nam', 'Việt Nam', '2025-02-10', 'Thường', 905),
(27, 'Bùi Hải Yến', 'Nữ', '1994-05-07', 'Việt Nam', 'Việt Nam', '2025-04-20', 'Thường', 603),
(28, 'Lê Tấn Tài', 'Nam', '1985-01-19', 'Việt Nam', 'Việt Nam', '2025-01-25', 'Thường', 604),
(29, 'Vương Phúc An', 'Nam', '1999-10-22', 'Việt Nam', 'Việt Nam', '2025-03-25', 'Thường', 605),
(30, 'Đặng Quỳnh Hoa', 'Nữ', '1993-07-13', 'Việt Nam', 'Việt Nam', '2025-02-15', 'Thường', 705),
(31, 'Nguyễn Bảo Châu', 'Nữ', '1995-03-12', 'Việt Nam', 'Việt Nam', '2025-04-05', 'VIP', 202),
(32, 'Trần Đình Khoa', 'Nam', '1988-11-01', 'Việt Nam', 'Việt Nam', '2025-01-08', 'Thường', 203),
(33, 'Lê Phương Mai', 'Nữ', '1992-08-25', 'Việt Nam', 'Việt Nam', '2025-03-18', 'Thường', 204),
(34, 'Phạm Công Danh', 'Nam', '1997-06-18', 'Việt Nam', 'Việt Nam', '2025-02-01', 'VIP', 304),
(35, 'Hoàng Thị Kim Liên', 'Nữ', '1986-04-09', 'Việt Nam', 'Việt Nam', '2025-04-28', 'Thường', 403),
(36, 'Đặng Văn Lâm', 'Nam', '1993-01-29', 'Việt Nam', 'Việt Nam', '2025-01-12', 'Thường', 404),
(37, 'Bùi Thúy Ngân', 'Nữ', '1991-10-10', 'Việt Nam', 'Việt Nam', '2025-03-03', 'VIP', 405),
(38, 'Vũ Thành Trung', 'Nam', '1989-05-05', 'Việt Nam', 'Việt Nam', '2025-02-25', 'Thường', 501),
(39, 'Đoàn Kiều Trang', 'Nữ', '1998-02-02', 'Việt Nam', 'Việt Nam', '2025-04-12', 'Thường', 502),
(40, 'Lý Minh Quang', 'Nam', '1984-09-17', 'Việt Nam', 'Việt Nam', '2025-01-20', 'VIP', 503),
(41, 'Phan Ngọc Diệp', 'Nữ', '1996-07-07', 'Việt Nam', 'Việt Nam', '2025-03-20', 'Thường', 504),
(42, 'Ngô Tuấn Kiệt', 'Nam', '1990-12-24', 'Việt Nam', 'Việt Nam', '2025-02-08', 'Thường', 701),
(43, 'Trịnh Lan Anh', 'Nữ', '1987-10-03', 'Việt Nam', 'Việt Nam', '2025-04-08', 'VIP', 703),
(44, 'Tạ Quốc Việt', 'Nam', '1994-04-28', 'Việt Nam', 'Việt Nam', '2025-01-27', 'Thường', 704),
(45, 'Dương Thùy Dương', 'Nữ', '1999-08-16', 'Việt Nam', 'Việt Nam', '2025-03-28', 'Thường', 805),
(46, 'Hồ Gia Huy', 'Nam', '1982-03-07', 'Việt Nam', 'Việt Nam', '2025-02-03', 'VIP', 106),
(47, 'Lâm Bảo Ngọc', 'Nữ', '1995-11-23', 'Việt Nam', 'Việt Nam', '2025-04-22', 'Thường', 107),
(48, 'Trần Minh Quân', 'Nam', '1997-09-13', 'Việt Nam', 'Việt Nam', '2025-01-03', 'Thường', 108),
(49, 'Nguyễn Phương Thảo', 'Nữ', '1991-01-01', 'Việt Nam', 'Việt Nam', '2025-03-12', 'VIP', 109),
(50, 'Lương Đức Hòa', 'Nam', '1986-08-08', 'Việt Nam', 'Việt Nam', '2025-02-18', 'Thường', 110),
(51, 'Mai Khánh Linh', 'Nữ', '1993-05-27', 'Việt Nam', 'Việt Nam', '2025-04-16', 'Thường', 206),
(52, 'Phùng Anh Tuấn', 'Nam', '1985-02-11', 'Việt Nam', 'Việt Nam', '2025-01-23', 'VIP', 207),
(53, 'Nguyễn Hà My', 'Nữ', '1998-10-31', 'Việt Nam', 'Việt Nam', '2025-03-06', 'Thường', 208),
(54, 'Đỗ Hoàng Long', 'Nam', '1992-12-03', 'Việt Nam', 'Việt Nam', '2025-02-20', 'Thường', 209),
(55, 'Hoàng Diệu Linh', 'Nữ', '1983-07-14', 'Việt Nam', 'Việt Nam', '2025-04-02', 'VIP', 210),
(56, 'Trịnh Đức Anh', 'Nam', '1996-04-06', 'Việt Nam', 'Việt Nam', '2025-01-06', 'Thường', 306),
(57, 'Bùi Phương Anh', 'Nữ', '1994-09-01', 'Việt Nam', 'Việt Nam', '2025-03-26', 'Thường', 307),
(58, 'Lê Quốc Khánh', 'Nam', '1989-11-18', 'Việt Nam', 'Việt Nam', '2025-02-16', 'VIP', 308),
(59, 'Vương Mỹ Duyên', 'Nữ', '1999-06-26', 'Việt Nam', 'Việt Nam', '2025-04-26', 'Thường', 309),
(60, 'Đặng Minh Hoàng', 'Nam', '1990-02-27', 'Việt Nam', 'Việt Nam', '2025-01-16', 'Thường', 310);

-- Revenue table structure
CREATE TABLE revenues (
    id INT,
    name VARCHAR(255) NOT NULL,
    sex VARCHAR(10),
    birthday DATE,
    national VARCHAR(50),
    country VARCHAR(100),
    checkin_date DATE,
    checkout_date DATE,
    room_type VARCHAR(10),
    room_number INT,
    total_price INT
);

INSERT INTO revenues (id, name, sex, birthday, national, country, checkin_date, checkout_date, room_type, room_number, total_price) VALUES
(1, 'Nguyễn Văn An', 'Nam', '1990-05-20', 'Việt Nam', 'Việt Nam', '2025-01-05', '2025-01-06', 'VIP', 101, 1850000),
(2, 'Trần Thị Hoa', 'Nữ', '1985-12-15', 'Việt Nam', 'Việt Nam', '2025-01-10', '2025-01-11', 'Thường', 102, 640000),
(3, 'Lê Minh Tú', 'Nam', '1992-07-30', 'Việt Nam', 'Việt Nam', '2025-01-15', '2025-01-17', 'VIP', 103, 1730000), -- 2 nights
(4, 'Phạm Thùy Dung', 'Nữ', '1998-09-05', 'Việt Nam', 'Việt Nam', '2025-01-20', '2025-01-21', 'Thường', 104, 920000),
(5, 'Hoàng Quốc Bảo', 'Nam', '1987-11-22', 'Việt Nam', 'Việt Nam', '2025-01-25', '2025-01-26', 'Thường', 105, 1210000),
(6, 'Đặng Thu Hằng', 'Nữ', '1995-04-18', 'Việt Nam', 'Việt Nam', '2025-01-28', '2025-01-29', 'Thường', 205, 740000),
(7, 'Bùi Quang Huy', 'Nam', '1989-08-12', 'Việt Nam', 'Việt Nam', '2025-02-01', '2025-02-02', 'Thường', 201, 1090000),
(8, 'Vũ Ngọc Linh', 'Nữ', '1991-06-25', 'Việt Nam', 'Việt Nam', '2025-02-05', '2025-02-07', 'Thường', 901, 880000), -- 2 nights
(9, 'Đoàn Văn Hải', 'Nam', '1984-03-17', 'Việt Nam', 'Việt Nam', '2025-02-10', '2025-02-11', 'Thường', 401, 960000),
(10, 'Lý Thu Trang', 'Nữ', '1993-09-29', 'Việt Nam', 'Việt Nam', '2025-02-14', '2025-02-15', 'Thường', 505, 770000),
(11, 'Phan Thanh Nam', 'Nam', '1996-02-10', 'Việt Nam', 'Việt Nam', '2025-02-18', '2025-02-19', 'Thường', 402, 1420000),
(12, 'Ngô Thị Mai', 'Nữ', '1990-07-05', 'Việt Nam', 'Việt Nam', '2025-02-22', '2025-02-23', 'Thường', 301, 870000),
(13, 'Trịnh Quốc Đạt', 'Nam', '1982-12-20', 'Việt Nam', 'Việt Nam', '2025-02-25', '2025-02-27', 'Thường', 302, 1240000), -- 2 nights
(14, 'Tạ Kim Oanh', 'Nữ', '1999-01-14', 'Việt Nam', 'Việt Nam', '2025-03-01', '2025-03-02', 'Thường', 303, 1150000),
(15, 'Dương Hữu Phúc', 'Nam', '1994-05-23', 'Việt Nam', 'Việt Nam', '2025-03-04', '2025-03-05', 'Thường', 305, 540000),
(16, 'Hồ Minh Đức', 'Nam', '1997-11-30', 'Việt Nam', 'Việt Nam', '2025-03-07', '2025-03-08', 'Thường', 601, 1380000),
(17, 'Lâm Thị Lan', 'Nữ', '1986-08-18', 'Việt Nam', 'Việt Nam', '2025-03-10', '2025-03-11', 'Thường', 602, 1320000),
(18, 'Trần Gia Bảo', 'Nam', '1995-09-08', 'Việt Nam', 'Việt Nam', '2025-03-13', '2025-03-15', 'Thường', 904, 1690000), -- 2 nights
(19, 'Nguyễn Hồng Nhung', 'Nữ', '1998-04-21', 'Việt Nam', 'Việt Nam', '2025-03-16', '2025-03-17', 'Thường', 702, 910000),
(20, 'Lương Quang Hải', 'Nam', '1980-10-10', 'Việt Nam', 'Việt Nam', '2025-03-19', '2025-03-20', 'Thường', 804, 1570000),
(21, 'Mai Thị Hạnh', 'Nữ', '1992-06-12', 'Việt Nam', 'Việt Nam', '2025-03-22', '2025-03-23', 'Thường', 801, 1020000),
(22, 'Phùng Văn Thịnh', 'Nam', '1983-03-04', 'Việt Nam', 'Việt Nam', '2025-03-25', '2025-03-26', 'Thường', 802, 650000),
(23, 'Nguyễn Thanh Hương', 'Nữ', '1997-07-27', 'Việt Nam', 'Việt Nam', '2025-03-28', '2025-03-30', 'Thường', 803, 1450000), -- 2 nights
(24, 'Đỗ Trọng Khang', 'Nam', '1991-09-15', 'Việt Nam', 'Việt Nam', '2025-04-01', '2025-04-02', 'Thường', 902, 1950000),
(25, 'Hoàng Mỹ Linh', 'Nữ', '1988-11-09', 'Việt Nam', 'Việt Nam', '2025-04-04', '2025-04-05', 'Thường', 903, 990000),
(26, 'Trịnh Minh Tuấn', 'Nam', '1996-12-01', 'Việt Nam', 'Việt Nam', '2025-04-07', '2025-04-08', 'Thường', 905, 1520000),
(27, 'Bùi Hải Yến', 'Nữ', '1994-05-07', 'Việt Nam', 'Việt Nam', '2025-04-10', '2025-04-11', 'Thường', 603, 750000),
(28, 'Lê Tấn Tài', 'Nam', '1985-01-19', 'Việt Nam', 'Việt Nam', '2025-04-13', '2025-04-15', 'Thường', 604, 1870000), -- 2 nights
(29, 'Vương Phúc An', 'Nam', '1999-10-22', 'Việt Nam', 'Việt Nam', '2025-04-16', '2025-04-17', 'Thường', 605, 570000),
(30, 'Đặng Quỳnh Hoa', 'Nữ', '1993-07-13', 'Việt Nam', 'Việt Nam', '2025-04-19', '2025-04-20', 'Thường', 705, 600000),
(31, 'Nguyễn Bảo Châu', 'Nữ', '1995-03-12', 'Việt Nam', 'Việt Nam', '2025-01-03', '2025-01-05', 'VIP', 202, 3500000), -- 2 nights
(32, 'Trần Đình Khoa', 'Nam', '1988-11-01', 'Việt Nam', 'Việt Nam', '2025-01-08', '2025-01-09', 'Thường', 203, 780000),
(33, 'Lê Phương Mai', 'Nữ', '1992-08-25', 'Việt Nam', 'Việt Nam', '2025-01-12', '2025-01-13', 'Thường', 204, 820000),
(34, 'Phạm Công Danh', 'Nam', '1997-06-18', 'Việt Nam', 'Việt Nam', '2025-01-18', '2025-01-20', 'VIP', 304, 3900000), -- 2 nights
(35, 'Hoàng Thị Kim Liên', 'Nữ', '1986-04-09', 'Việt Nam', 'Việt Nam', '2025-01-22', '2025-01-23', 'Thường', 403, 690000),
(36, 'Đặng Văn Lâm', 'Nam', '1993-01-29', 'Việt Nam', 'Việt Nam', '2025-01-26', '2025-01-27', 'Thường', 404, 950000),
(37, 'Bùi Thúy Ngân', 'Nữ', '1991-10-10', 'Việt Nam', 'Việt Nam', '2025-01-30', '2025-01-31', 'VIP', 405, 1980000),
(38, 'Vũ Thành Trung', 'Nam', '1989-05-05', 'Việt Nam', 'Việt Nam', '2025-02-03', '2025-02-05', 'Thường', 501, 1500000), -- 2 nights
(39, 'Đoàn Kiều Trang', 'Nữ', '1998-02-02', 'Việt Nam', 'Việt Nam', '2025-02-07', '2025-02-08', 'Thường', 502, 760000),
(40, 'Lý Minh Quang', 'Nam', '1984-09-17', 'Việt Nam', 'Việt Nam', '2025-02-11', '2025-02-12', 'VIP', 503, 2100000),
(41, 'Phan Ngọc Diệp', 'Nữ', '1996-07-07', 'Việt Nam', 'Việt Nam', '2025-02-16', '2025-02-17', 'Thường', 504, 810000),
(42, 'Ngô Tuấn Kiệt', 'Nam', '1990-12-24', 'Việt Nam', 'Việt Nam', '2025-02-20', '2025-02-22', 'Thường', 701, 1800000), -- 2 nights
(43, 'Trịnh Lan Anh', 'Nữ', '1987-10-03', 'Việt Nam', 'Việt Nam', '2025-02-24', '2025-02-25', 'VIP', 703, 1750000),
(44, 'Tạ Quốc Việt', 'Nam', '1994-04-28', 'Việt Nam', 'Việt Nam', '2025-02-28', '2025-03-01', 'Thường', 704, 930000),
(45, 'Dương Thùy Dương', 'Nữ', '1999-08-16', 'Việt Nam', 'Việt Nam', '2025-03-03', '2025-03-04', 'Thường', 805, 670000),
(46, 'Hồ Gia Huy', 'Nam', '1982-03-07', 'Việt Nam', 'Việt Nam', '2025-03-06', '2025-03-08', 'VIP', 106, 4200000), -- 2 nights
(47, 'Lâm Bảo Ngọc', 'Nữ', '1995-11-23', 'Việt Nam', 'Việt Nam', '2025-03-09', '2025-03-10', 'Thường', 107, 880000),
(48, 'Trần Minh Quân', 'Nam', '1997-09-13', 'Việt Nam', 'Việt Nam', '2025-03-12', '2025-03-13', 'Thường', 108, 1100000),
(49, 'Nguyễn Phương Thảo', 'Nữ', '1991-01-01', 'Việt Nam', 'Việt Nam', '2025-03-15', '2025-03-16', 'VIP', 109, 2250000),
(50, 'Lương Đức Hòa', 'Nam', '1986-08-08', 'Việt Nam', 'Việt Nam', '2025-03-18', '2025-03-20', 'Thường', 110, 1640000), -- 2 nights
(51, 'Mai Khánh Linh', 'Nữ', '1993-05-27', 'Việt Nam', 'Việt Nam', '2025-03-21', '2025-03-22', 'Thường', 206, 710000),
(52, 'Phùng Anh Tuấn', 'Nam', '1985-02-11', 'Việt Nam', 'Việt Nam', '2025-03-24', '2025-03-25', 'VIP', 207, 1890000),
(53, 'Nguyễn Hà My', 'Nữ', '1998-10-31', 'Việt Nam', 'Việt Nam', '2025-03-27', '2025-03-28', 'Thường', 208, 940000),
(54, 'Đỗ Hoàng Long', 'Nam', '1992-12-03', 'Việt Nam', 'Việt Nam', '2025-03-30', '2025-04-01', 'Thường', 209, 1780000), -- 2 nights
(55, 'Hoàng Diệu Linh', 'Nữ', '1983-07-14', 'Việt Nam', 'Việt Nam', '2025-04-03', '2025-04-04', 'VIP', 210, 2050000),
(56, 'Trịnh Đức Anh', 'Nam', '1996-04-06', 'Việt Nam', 'Việt Nam', '2025-04-06', '2025-04-07', 'Thường', 306, 850000),
(57, 'Bùi Phương Anh', 'Nữ', '1994-09-01', 'Việt Nam', 'Việt Nam', '2025-04-09', '2025-04-10', 'Thường', 307, 1050000),
(58, 'Lê Quốc Khánh', 'Nam', '1989-11-18', 'Việt Nam', 'Việt Nam', '2025-04-12', '2025-04-14', 'VIP', 308, 3600000), -- 2 nights
(59, 'Vương Mỹ Duyên', 'Nữ', '1999-06-26', 'Việt Nam', 'Việt Nam', '2025-04-15', '2025-04-16', 'Thường', 309, 660000),
(60, 'Đặng Minh Hoàng', 'Nam', '1990-02-27', 'Việt Nam', 'Việt Nam', '2025-04-18', '2025-04-19', 'Thường', 310, 1120000);
