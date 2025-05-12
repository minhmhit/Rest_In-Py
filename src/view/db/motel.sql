USE motel;

DROP TABLE IF EXISTS revenues;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS staffs;


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

-- Randomly assigning one of the 63 Vietnamese provinces/cities to the country field
INSERT INTO customers (id, name, sex, birthday, national, country, checkin_date, room_type, room_number) VALUES
(1, 'Nguyễn Văn An', 'Nam', '1990-05-20', 'Việt Nam', 'Sơn La', '2025-03-15', 'VIP', 101),
(2, 'Trần Thị Hoa', 'Nữ', '1985-12-15', 'Việt Nam', 'Kiên Giang', '2025-01-22', 'Thường', 102),
(3, 'Lê Minh Tú', 'Nam', '1992-07-30', 'Việt Nam', 'Bình Phước', '2025-04-10', 'VIP', 103),
(4, 'Phạm Thùy Dung', 'Nữ', '1998-09-05', 'Việt Nam', 'Hậu Giang', '2025-02-28', 'Thường', 104),
(5, 'Hoàng Quốc Bảo', 'Nam', '1987-11-22', 'Việt Nam', 'Nam Định', '2025-01-05', 'Thường', 105),
(6, 'Đặng Thu Hằng', 'Nữ', '1995-04-18', 'Việt Nam', 'Đắk Nông', '2025-03-01', 'Thường', 205),
(7, 'Bùi Quang Huy', 'Nam', '1989-08-12', 'Việt Nam', 'Quảng Trị', '2025-04-25', 'Thường', 201),
(8, 'Vũ Ngọc Linh', 'Nữ', '1991-06-25', 'Việt Nam', 'Thanh Hóa', '2025-02-12', 'Thường', 901),
(9, 'Đoàn Văn Hải', 'Nam', '1984-03-17', 'Việt Nam', 'Phú Thọ', '2025-01-18', 'Thường', 401),
(10, 'Lý Thu Trang', 'Nữ', '1993-09-29', 'Việt Nam', 'Bạc Liêu', '2025-03-29', 'Thường', 505),
(11, 'Phan Thanh Nam', 'Nam', '1996-02-10', 'Việt Nam', 'Cà Mau', '2025-04-18', 'Thường', 402),
(12, 'Ngô Thị Mai', 'Nữ', '1990-07-05', 'Việt Nam', 'Vĩnh Phúc', '2025-01-28', 'Thường', 301),
(13, 'Trịnh Quốc Đạt', 'Nam', '1982-12-20', 'Việt Nam', 'Quảng Ngãi', '2025-03-05', 'Thường', 302),
(14, 'Tạ Kim Oanh', 'Nữ', '1999-01-14', 'Việt Nam', 'Hải Dương', '2025-02-19', 'Thường', 303),
(15, 'Dương Hữu Phúc', 'Nam', '1994-05-23', 'Việt Nam', 'Bình Thuận', '2025-04-01', 'Thường', 305),
(16, 'Hồ Minh Đức', 'Nam', '1997-11-30', 'Việt Nam', 'Hải Phòng', '2025-01-10', 'Thường', 601),
(17, 'Lâm Thị Lan', 'Nữ', '1986-08-18', 'Việt Nam', 'Lạng Sơn', '2025-03-22', 'Thường', 602),
(18, 'Trần Gia Bảo', 'Nam', '1995-09-08', 'Việt Nam', 'Đồng Tháp', '2025-02-05', 'Thường', 904),
(19, 'Nguyễn Hồng Nhung', 'Nữ', '1998-04-21', 'Việt Nam', 'Ninh Bình', '2025-04-30', 'Thường', 702),
(20, 'Lương Quang Hải', 'Nam', '1980-10-10', 'Việt Nam', 'Bình Dương', '2025-01-15', 'Thường', 804),
(21, 'Mai Thị Hạnh', 'Nữ', '1992-06-12', 'Việt Nam', 'Đà Nẵng', '2025-03-10', 'Thường', 801),
(22, 'Phùng Văn Thịnh', 'Nam', '1983-03-04', 'Việt Nam', 'Hà Giang', '2025-02-22', 'Thường', 802),
(23, 'Nguyễn Thanh Hương', 'Nữ', '1997-07-27', 'Việt Nam', 'Thái Nguyên', '2025-04-15', 'Thường', 803),
(24, 'Đỗ Trọng Khang', 'Nam', '1991-09-15', 'Việt Nam', 'Quảng Ninh', '2025-01-30', 'Thường', 902),
(25, 'Hoàng Mỹ Linh', 'Nữ', '1988-11-09', 'Việt Nam', 'An Giang', '2025-03-08', 'Thường', 903),
(26, 'Trịnh Minh Tuấn', 'Nam', '1996-12-01', 'Việt Nam', 'Lai Châu', '2025-02-10', 'Thường', 905),
(27, 'Bùi Hải Yến', 'Nữ', '1994-05-07', 'Việt Nam', 'Cần Thơ', '2025-04-20', 'Thường', 603),
(28, 'Lê Tấn Tài', 'Nam', '1985-01-19', 'Việt Nam', 'Bắc Ninh', '2025-01-25', 'Thường', 604),
(29, 'Vương Phúc An', 'Nam', '1999-10-22', 'Việt Nam', 'Bình Định', '2025-03-25', 'Thường', 605),
(30, 'Đặng Quỳnh Hoa', 'Nữ', '1993-07-13', 'Việt Nam', 'Gia Lai', '2025-02-15', 'Thường', 705),
(31, 'Nguyễn Bảo Châu', 'Nữ', '1995-03-12', 'Việt Nam', 'Cao Bằng', '2025-04-05', 'VIP', 202),
(32, 'Trần Đình Khoa', 'Nam', '1988-11-01', 'Việt Nam', 'Hòa Bình', '2025-01-08', 'Thường', 203),
(33, 'Lê Phương Mai', 'Nữ', '1992-08-25', 'Việt Nam', 'Đắk Lắk', '2025-03-18', 'Thường', 204),
(34, 'Phạm Công Danh', 'Nam', '1997-06-18', 'Việt Nam', 'Thái Bình', '2025-02-01', 'VIP', 304),
(35, 'Hoàng Thị Kim Liên', 'Nữ', '1986-04-09', 'Việt Nam', 'Lào Cai', '2025-04-28', 'Thường', 403),
(36, 'Đặng Văn Lâm', 'Nam', '1993-01-29', 'Việt Nam', 'Quảng Bình', '2025-01-12', 'Thường', 404),
(37, 'Bùi Thúy Ngân', 'Nữ', '1991-10-10', 'Việt Nam', 'Kon Tum', '2025-03-03', 'VIP', 405),
(38, 'Vũ Thành Trung', 'Nam', '1989-05-05', 'Việt Nam', 'Hà Nội', '2025-02-25', 'Thường', 501),
(39, 'Đoàn Kiều Trang', 'Nữ', '1998-02-02', 'Việt Nam', 'Hà Nam', '2025-04-12', 'Thường', 502),
(40, 'Lý Minh Quang', 'Nam', '1984-09-17', 'Việt Nam', 'TP Hồ Chí Minh', '2025-01-20', 'VIP', 503),
(41, 'Phan Ngọc Diệp', 'Nữ', '1996-07-07', 'Việt Nam', 'Quảng Nam', '2025-03-20', 'Thường', 504),
(42, 'Ngô Tuấn Kiệt', 'Nam', '1990-12-24', 'Việt Nam', 'Vĩnh Long', '2025-02-08', 'Thường', 701),
(43, 'Trịnh Lan Anh', 'Nữ', '1987-10-03', 'Việt Nam', 'Yên Bái', '2025-04-08', 'VIP', 703),
(44, 'Tạ Quốc Việt', 'Nam', '1994-04-28', 'Việt Nam', 'Bắc Giang', '2025-01-27', 'Thường', 704),
(45, 'Dương Thùy Dương', 'Nữ', '1999-08-16', 'Việt Nam', 'Tây Ninh', '2025-03-28', 'Thường', 805),
(46, 'Hồ Gia Huy', 'Nam', '1982-03-07', 'Việt Nam', 'Nghệ An', '2025-02-03', 'VIP', 106),
(47, 'Lâm Bảo Ngọc', 'Nữ', '1995-11-23', 'Việt Nam', 'Điện Biên', '2025-04-22', 'Thường', 107),
(48, 'Trần Minh Quân', 'Nam', '1997-09-13', 'Việt Nam', 'Hà Tĩnh', '2025-01-03', 'Thường', 108),
(49, 'Nguyễn Phương Thảo', 'Nữ', '1991-01-01', 'Việt Nam', 'Lâm Đồng', '2025-03-12', 'VIP', 109),
(50, 'Lương Đức Hòa', 'Nam', '1986-08-08', 'Việt Nam', 'Đồng Nai', '2025-02-18', 'Thường', 110),
(51, 'Mai Khánh Linh', 'Nữ', '1993-05-27', 'Việt Nam', 'Phú Yên', '2025-04-16', 'Thường', 206),
(52, 'Phùng Anh Tuấn', 'Nam', '1985-02-11', 'Việt Nam', 'Bắc Kạn', '2025-01-23', 'VIP', 207),
(53, 'Nguyễn Hà My', 'Nữ', '1998-10-31', 'Việt Nam', 'Trà Vinh', '2025-03-06', 'Thường', 208),
(54, 'Đỗ Hoàng Long', 'Nam', '1992-12-03', 'Việt Nam', 'Long An', '2025-02-20', 'Thường', 209),
(55, 'Hoàng Diệu Linh', 'Nữ', '1983-07-14', 'Việt Nam', 'Ninh Thuận', '2025-04-02', 'VIP', 210),
(56, 'Trịnh Đức Anh', 'Nam', '1996-04-06', 'Việt Nam', 'Tiền Giang', '2025-01-06', 'Thường', 306),
(57, 'Bùi Phương Anh', 'Nữ', '1994-09-01', 'Việt Nam', 'Bến Tre', '2025-03-26', 'Thường', 307),
(58, 'Lê Quốc Khánh', 'Nam', '1989-11-18', 'Việt Nam', 'Bà Rịa - Vũng Tàu', '2025-02-16', 'VIP', 308),
(59, 'Vương Mỹ Duyên', 'Nữ', '1999-06-26', 'Việt Nam', 'Tuyên Quang', '2025-04-26', 'Thường', 309),
(60, 'Đặng Minh Hoàng', 'Nam', '1990-02-27', 'Việt Nam', 'Sóc Trăng', '2025-01-16', 'Thường', 310);

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

-- Randomly assigning one of the 63 Vietnamese provinces/cities to the country field
INSERT INTO revenues (id, name, sex, birthday, national, country, checkin_date, checkout_date, room_type, room_number, total_price) VALUES
(1, 'Nguyễn Văn An', 'Nam', '1990-05-20', 'Việt Nam', 'Lạng Sơn', '2025-01-05', '2025-01-06', 'VIP', 101, 1850000),
(2, 'Trần Thị Hoa', 'Nữ', '1985-12-15', 'Việt Nam', 'Hà Nam', '2025-01-10', '2025-01-11', 'Thường', 102, 640000),
(3, 'Lê Minh Tú', 'Nam', '1992-07-30', 'Việt Nam', 'Đắk Lắk', '2025-01-15', '2025-01-17', 'VIP', 103, 1730000), -- 2 nights
(4, 'Phạm Thùy Dung', 'Nữ', '1998-09-05', 'Việt Nam', 'Bắc Giang', '2025-01-20', '2025-01-21', 'Thường', 104, 920000),
(5, 'Hoàng Quốc Bảo', 'Nam', '1987-11-22', 'Việt Nam', 'Lào Cai', '2025-01-25', '2025-01-26', 'Thường', 105, 1210000),
(6, 'Đặng Thu Hằng', 'Nữ', '1995-04-18', 'Việt Nam', 'Khánh Hòa', '2025-01-28', '2025-01-29', 'Thường', 205, 740000),
(7, 'Bùi Quang Huy', 'Nam', '1989-08-12', 'Việt Nam', 'Hậu Giang', '2025-02-01', '2025-02-02', 'Thường', 201, 1090000),
(8, 'Vũ Ngọc Linh', 'Nữ', '1991-06-25', 'Việt Nam', 'An Giang', '2025-02-05', '2025-02-07', 'Thường', 901, 880000), -- 2 nights
(9, 'Đoàn Văn Hải', 'Nam', '1984-03-17', 'Việt Nam', 'Gia Lai', '2025-02-10', '2025-02-11', 'Thường', 401, 960000),
(10, 'Lý Thu Trang', 'Nữ', '1993-09-29', 'Việt Nam', 'Quảng Ninh', '2025-02-14', '2025-02-15', 'Thường', 505, 770000),
(11, 'Phan Thanh Nam', 'Nam', '1996-02-10', 'Việt Nam', 'Lai Châu', '2025-02-18', '2025-02-19', 'Thường', 402, 1420000),
(12, 'Ngô Thị Mai', 'Nữ', '1990-07-05', 'Việt Nam', 'Bình Dương', '2025-02-22', '2025-02-23', 'Thường', 301, 870000),
(13, 'Trịnh Quốc Đạt', 'Nam', '1982-12-20', 'Việt Nam', 'Đồng Tháp', '2025-02-25', '2025-02-27', 'Thường', 302, 1240000), -- 2 nights
(14, 'Tạ Kim Oanh', 'Nữ', '1999-01-14', 'Việt Nam', 'Tây Ninh', '2025-03-01', '2025-03-02', 'Thường', 303, 1150000),
(15, 'Dương Hữu Phúc', 'Nam', '1994-05-23', 'Việt Nam', 'Nam Định', '2025-03-04', '2025-03-05', 'Thường', 305, 540000),
(16, 'Hồ Minh Đức', 'Nam', '1997-11-30', 'Việt Nam', 'TP Hồ Chí Minh', '2025-03-07', '2025-03-08', 'Thường', 601, 1380000),
(17, 'Lâm Thị Lan', 'Nữ', '1986-08-18', 'Việt Nam', 'Hải Dương', '2025-03-10', '2025-03-11', 'Thường', 602, 1320000),
(18, 'Trần Gia Bảo', 'Nam', '1995-09-08', 'Việt Nam', 'Cần Thơ', '2025-03-13', '2025-03-15', 'Thường', 904, 1690000), -- 2 nights
(19, 'Nguyễn Hồng Nhung', 'Nữ', '1998-04-21', 'Việt Nam', 'Thừa Thiên Huế', '2025-03-16', '2025-03-17', 'Thường', 702, 910000),
(20, 'Lương Quang Hải', 'Nam', '1980-10-10', 'Việt Nam', 'Ninh Bình', '2025-03-19', '2025-03-20', 'Thường', 804, 1570000),
(21, 'Mai Thị Hạnh', 'Nữ', '1992-06-12', 'Việt Nam', 'Vĩnh Long', '2025-03-22', '2025-03-23', 'Thường', 801, 1020000),
(22, 'Phùng Văn Thịnh', 'Nam', '1983-03-04', 'Việt Nam', 'Nghệ An', '2025-03-25', '2025-03-26', 'Thường', 802, 650000),
(23, 'Nguyễn Thanh Hương', 'Nữ', '1997-07-27', 'Việt Nam', 'Quảng Ngãi', '2025-03-28', '2025-03-30', 'Thường', 803, 1450000), -- 2 nights
(24, 'Đỗ Trọng Khang', 'Nam', '1991-09-15', 'Việt Nam', 'Sóc Trăng', '2025-04-01', '2025-04-02', 'Thường', 902, 1950000),
(25, 'Hoàng Mỹ Linh', 'Nữ', '1988-11-09', 'Việt Nam', 'Bình Định', '2025-04-04', '2025-04-05', 'Thường', 903, 990000),
(26, 'Trịnh Minh Tuấn', 'Nam', '1996-12-01', 'Việt Nam', 'Bình Phước', '2025-04-07', '2025-04-08', 'Thường', 905, 1520000),
(27, 'Bùi Hải Yến', 'Nữ', '1994-05-07', 'Việt Nam', 'Đắk Nông', '2025-04-10', '2025-04-11', 'Thường', 603, 750000),
(28, 'Lê Tấn Tài', 'Nam', '1985-01-19', 'Việt Nam', 'Cao Bằng', '2025-04-13', '2025-04-15', 'Thường', 604, 1870000), -- 2 nights
(29, 'Vương Phúc An', 'Nam', '1999-10-22', 'Việt Nam', 'Phú Yên', '2025-04-16', '2025-04-17', 'Thường', 605, 570000),
(30, 'Đặng Quỳnh Hoa', 'Nữ', '1993-07-13', 'Việt Nam', 'Thái Bình', '2025-04-19', '2025-04-20', 'Thường', 705, 600000),
(31, 'Nguyễn Bảo Châu', 'Nữ', '1995-03-12', 'Việt Nam', 'Hải Phòng', '2025-01-03', '2025-01-05', 'VIP', 202, 3500000), -- 2 nights
(32, 'Trần Đình Khoa', 'Nam', '1988-11-01', 'Việt Nam', 'Yên Bái', '2025-01-08', '2025-01-09', 'Thường', 203, 780000),
(33, 'Lê Phương Mai', 'Nữ', '1992-08-25', 'Việt Nam', 'Long An', '2025-01-12', '2025-01-13', 'Thường', 204, 820000),
(34, 'Phạm Công Danh', 'Nam', '1997-06-18', 'Việt Nam', 'Bạc Liêu', '2025-01-18', '2025-01-20', 'VIP', 304, 3900000), -- 2 nights
(35, 'Hoàng Thị Kim Liên', 'Nữ', '1986-04-09', 'Việt Nam', 'Vĩnh Phúc', '2025-01-22', '2025-01-23', 'Thường', 403, 690000),
(36, 'Đặng Văn Lâm', 'Nam', '1993-01-29', 'Việt Nam', 'Kiên Giang', '2025-01-26', '2025-01-27', 'Thường', 404, 950000),
(37, 'Bùi Thúy Ngân', 'Nữ', '1991-10-10', 'Việt Nam', 'Trà Vinh', '2025-01-30', '2025-01-31', 'VIP', 405, 1980000),
(38, 'Vũ Thành Trung', 'Nam', '1989-05-05', 'Việt Nam', 'Cà Mau', '2025-02-03', '2025-02-05', 'Thường', 501, 1500000), -- 2 nights
(39, 'Đoàn Kiều Trang', 'Nữ', '1998-02-02', 'Việt Nam', 'Bình Thuận', '2025-02-07', '2025-02-08', 'Thường', 502, 760000),
(40, 'Lý Minh Quang', 'Nam', '1984-09-17', 'Việt Nam', 'Kon Tum', '2025-02-11', '2025-02-12', 'VIP', 503, 2100000),
(41, 'Phan Ngọc Diệp', 'Nữ', '1996-07-07', 'Việt Nam', 'Tiền Giang', '2025-02-16', '2025-02-17', 'Thường', 504, 810000),
(42, 'Ngô Tuấn Kiệt', 'Nam', '1990-12-24', 'Việt Nam', 'Đà Nẵng', '2025-02-20', '2025-02-22', 'Thường', 701, 1800000), -- 2 nights
(43, 'Trịnh Lan Anh', 'Nữ', '1987-10-03', 'Việt Nam', 'Thái Nguyên', '2025-02-24', '2025-02-25', 'VIP', 703, 1750000),
(44, 'Tạ Quốc Việt', 'Nam', '1994-04-28', 'Việt Nam', 'Hà Giang', '2025-02-28', '2025-03-01', 'Thường', 704, 930000),
(45, 'Dương Thùy Dương', 'Nữ', '1999-08-16', 'Việt Nam', 'Quảng Trị', '2025-03-03', '2025-03-04', 'Thường', 805, 670000),
(46, 'Hồ Gia Huy', 'Nam', '1982-03-07', 'Việt Nam', 'Sơn La', '2025-03-06', '2025-03-08', 'VIP', 106, 4200000), -- 2 nights
(47, 'Lâm Bảo Ngọc', 'Nữ', '1995-11-23', 'Việt Nam', 'Bến Tre', '2025-03-09', '2025-03-10', 'Thường', 107, 880000),
(48, 'Trần Minh Quân', 'Nam', '1997-09-13', 'Việt Nam', 'Hòa Bình', '2025-03-12', '2025-03-13', 'Thường', 108, 1100000),
(49, 'Nguyễn Phương Thảo', 'Nữ', '1991-01-01', 'Việt Nam', 'Điện Biên', '2025-03-15', '2025-03-16', 'VIP', 109, 2250000),
(50, 'Lương Đức Hòa', 'Nam', '1986-08-08', 'Việt Nam', 'Bà Rịa - Vũng Tàu', '2025-03-18', '2025-03-20', 'Thường', 110, 1640000), -- 2 nights
(51, 'Mai Khánh Linh', 'Nữ', '1993-05-27', 'Việt Nam', 'Hà Tĩnh', '2025-03-21', '2025-03-22', 'Thường', 206, 710000),
(52, 'Phùng Anh Tuấn', 'Nam', '1985-02-11', 'Việt Nam', 'Ninh Thuận', '2025-03-24', '2025-03-25', 'VIP', 207, 1890000),
(53, 'Nguyễn Hà My', 'Nữ', '1998-10-31', 'Việt Nam', 'Bắc Ninh', '2025-03-27', '2025-03-28', 'Thường', 208, 940000),
(54, 'Đỗ Hoàng Long', 'Nam', '1992-12-03', 'Việt Nam', 'Quảng Bình', '2025-03-30', '2025-04-01', 'Thường', 209, 1780000), -- 2 nights
(55, 'Hoàng Diệu Linh', 'Nữ', '1983-07-14', 'Việt Nam', 'Lâm Đồng', '2025-04-03', '2025-04-04', 'VIP', 210, 2050000),
(56, 'Trịnh Đức Anh', 'Nam', '1996-04-06', 'Việt Nam', 'Bắc Kạn', '2025-04-06', '2025-04-07', 'Thường', 306, 850000),
(57, 'Bùi Phương Anh', 'Nữ', '1994-09-01', 'Việt Nam', 'Tuyên Quang', '2025-04-09', '2025-04-10', 'Thường', 307, 1050000),
(58, 'Lê Quốc Khánh', 'Nam', '1989-11-18', 'Việt Nam', 'Phú Thọ', '2025-04-12', '2025-04-14', 'VIP', 308, 3600000), -- 2 nights
(59, 'Vương Mỹ Duyên', 'Nữ', '1999-06-26', 'Việt Nam', 'Đồng Nai', '2025-04-15', '2025-04-16', 'Thường', 309, 660000),
(60, 'Đặng Minh Hoàng', 'Nam', '1990-02-27', 'Việt Nam', 'Thanh Hóa', '2025-04-18', '2025-04-19', 'Thường', 310, 1120000);
