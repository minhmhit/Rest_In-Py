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

-- Staff data
INSERT INTO staffs (id, name, sex, birthday, role, username, password, permissions) VALUES
(1, 'Nguyễn Văn A', 'Nam', '1990-01-01', 'Quản Trị Viên', 'admin1', 'admin', 'Toàn quyền'),
(2, 'Lê Thị B', 'Nữ', '1992-03-10', 'Quản Lí', 'recept1', 'recept', 'Đặt phòng, thanh toán'),
(3, 'Trần Văn C', 'Nam', '1985-06-20', 'Nhân Viên', 'guard1', 'guard', 'Camera');

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

-- Customer data
INSERT INTO customers (id, name, sex, birthday, national, country, checkin_date, room_type, room_number) VALUES
(1, 'Nguyễn Văn An', 'Nam', '1990-05-20', 'Việt Nam', 'Long An', '2005-08-16', 'VIP', 101),
(2, 'Trần Thị Hoa', 'Nữ', '1985-12-15', 'Việt Nam', 'Tra Vinh', '2015-02-20', 'Thường', 102),
(3, 'Lê Minh Tú', 'Nam', '1992-07-30', 'Việt Nam', 'Ho Chi Minh', '2010-02-10', 'VIP', 103),
(4, 'Phạm Thùy Dung', 'Nữ', '1998-09-05', 'Việt Nam', 'Ha Noi', '2018-11-15', 'Thường', 104),
(5, 'Hoàng Quốc Bảo', 'Nam', '1987-11-22', 'Việt Nam', 'Bac Lieu', '2020-01-01', 'Thường', 105),
(6, 'Đặng Thu Hằng', 'Nữ', '1995-04-18', 'Việt Nam', 'Hai Phong', '2015-02-20', 'Thường', 205),
(7, 'Bùi Quang Huy', 'Nam', '1989-08-12', 'Việt Nam', 'Việt Nam', '2015-02-23', 'Thường', 201),
(8, 'Vũ Ngọc Linh', 'Nữ', '1991-06-25', 'Việt Nam', 'Việt Nam', '2012-11-30', 'Thường', 901), 
(9, 'Đoàn Văn Hải', 'Nam', '1984-03-17', 'Việt Nam', 'Việt Nam', '2015-03-21', 'Thường', 401),
(10, 'Lý Thu Trang', 'Nữ', '1993-09-29', 'Việt Nam', 'Việt Nam', '2010-06-11', 'Thường', 505),
(11, 'Phan Thanh Nam', 'Nam', '1996-02-10', 'Việt Nam', 'Việt Nam', '2015-09-09', 'Thường', 402),
(12, 'Ngô Thị Mai', 'Nữ', '1990-07-05', 'Việt Nam', 'Việt Nam', '1999-01-05', 'Thường', 301),
(13, 'Trịnh Quốc Đạt', 'Nam', '1982-12-20', 'Việt Nam', 'Việt Nam', '2019-12-31', 'Thường', 302),
(14, 'Tạ Kim Oanh', 'Nữ', '1999-01-14', 'Việt Nam', 'Việt Nam', '2013-02-05', 'Thường', 303),
(15, 'Dương Hữu Phúc', 'Nam', '1994-05-23', 'Việt Nam', 'Việt Nam', '2015-05-08', 'Thường', 305),
(16, 'Hồ Minh Đức', 'Nam', '1997-11-30', 'Việt Nam', 'Việt Nam', '2000-10-12', 'Thường', 601),
(17, 'Lâm Thị Lan', 'Nữ', '1986-08-18', 'Việt Nam', 'Việt Nam', '2001-12-12', 'Thường', 602),
(18, 'Trần Gia Bảo', 'Nam', '1995-09-08', 'Việt Nam', 'Việt Nam', '2004-12-16', 'Thường', 904),
(19, 'Nguyễn Hồng Nhung', 'Nữ', '1998-04-21', 'Việt Nam', 'Việt Nam', '2017-10-10', 'Thường', 702),
(20, 'Lương Quang Hải', 'Nam', '1980-10-10', 'Việt Nam', 'Việt Nam', '2016-08-17', 'Thường', 804),
(21, 'Mai Thị Hạnh', 'Nữ', '1992-06-12', 'Việt Nam', 'Việt Nam', '2015-02-20', 'Thường', 801), 
(22, 'Phùng Văn Thịnh', 'Nam', '1983-03-04', 'Việt Nam', 'Việt Nam', '2003-12-16', 'Thường', 802),
(23, 'Nguyễn Thanh Hương', 'Nữ', '1997-07-27', 'Việt Nam', 'Việt Nam', '2006-11-15', 'Thường', 803),
(24, 'Đỗ Trọng Khang', 'Nam', '1991-09-15', 'Việt Nam', 'Việt Nam', '2014-12-14', 'Thường', 902),
(25, 'Hoàng Mỹ Linh', 'Nữ', '1988-11-09', 'Việt Nam', 'Việt Nam', '2011-01-12', 'Thường', 903),
(26, 'Trịnh Minh Tuấn', 'Nam', '1996-12-01', 'Việt Nam', 'Việt Nam', '2007-11-29', 'Thường', 905),
(27, 'Bùi Hải Yến', 'Nữ', '1994-05-07', 'Việt Nam', 'Việt Nam', '2000-02-02', 'Thường', 603),
(28, 'Lê Tấn Tài', 'Nam', '1985-01-19', 'Việt Nam', 'Việt Nam', '2001-10-19', 'Thường', 604),
(29, 'Vương Phúc An', 'Nam', '1999-10-22', 'Việt Nam', 'Việt Nam', '2002-10-10', 'Thường', 605),
(30, 'Đặng Quỳnh Hoa', 'Nữ', '1993-07-13', 'Việt Nam', 'Việt Nam', '2008-07-17', 'Thường', 705);

-- Revenue table structure
CREATE TABLE revenues (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sex VARCHAR(10),
    birthday DATE,
    national VARCHAR(50),
    country VARCHAR(100), 
    checkin_date DATE,
    room_type VARCHAR(10),
    room_number INT,
    total_price INT
);

-- Revenue data
INSERT INTO revenues (id, name, sex, birthday, national, country, checkin_date, room_type, room_number, total_price) VALUES
(1, 'Nguyễn Văn An', 'Nam', '1990-05-20', 'Việt Nam', 'Long An', '2005-08-16', 'VIP', 101, 1850000),
(2, 'Trần Thị Hoa', 'Nữ', '1985-12-15', 'Việt Nam', 'Tra Vinh', '2015-02-20', 'Thường', 102, 640000),
(3, 'Lê Minh Tú', 'Nam', '1992-07-30', 'Việt Nam', 'Ho Chi Minh', '2010-02-10', 'VIP', 103, 1730000),
(4, 'Phạm Thùy Dung', 'Nữ', '1998-09-05', 'Việt Nam', 'Ha Noi', '2018-11-15', 'Thường', 104, 920000),
(5, 'Hoàng Quốc Bảo', 'Nam', '1987-11-22', 'Việt Nam', 'Bac Lieu', '2020-01-01', 'Thường', 105, 1210000),
(6, 'Đặng Thu Hằng', 'Nữ', '1995-04-18', 'Việt Nam', 'Hai Phong', '2015-02-20', 'Thường', 205, 740000),
(7, 'Bùi Quang Huy', 'Nam', '1989-08-12', 'Việt Nam', 'Việt Nam', '2015-02-23', 'Thường', 201, 1090000),
(8, 'Vũ Ngọc Linh', 'Nữ', '1991-06-25', 'Việt Nam', 'Việt Nam', '2012-11-30', 'Thường', 901, 880000), 
(9, 'Đoàn Văn Hải', 'Nam', '1984-03-17', 'Việt Nam', 'Việt Nam', '2015-03-21', 'Thường', 401, 960000),
(10, 'Lý Thu Trang', 'Nữ', '1993-09-29', 'Việt Nam', 'Việt Nam', '2010-06-11', 'Thường', 505, 770000),
(11, 'Phan Thanh Nam', 'Nam', '1996-02-10', 'Việt Nam', 'Việt Nam', '2015-09-09', 'Thường', 402, 1420000),
(12, 'Ngô Thị Mai', 'Nữ', '1990-07-05', 'Việt Nam', 'Việt Nam', '1999-01-05', 'Thường', 301, 870000),
(13, 'Trịnh Quốc Đạt', 'Nam', '1982-12-20', 'Việt Nam', 'Việt Nam', '2019-12-31', 'Thường', 302, 1240000),
(14, 'Tạ Kim Oanh', 'Nữ', '1999-01-14', 'Việt Nam', 'Việt Nam', '2013-02-05', 'Thường', 303, 1150000),
(15, 'Dương Hữu Phúc', 'Nam', '1994-05-23', 'Việt Nam', 'Việt Nam', '2015-05-08', 'Thường', 305, 540000),
(16, 'Hồ Minh Đức', 'Nam', '1997-11-30', 'Việt Nam', 'Việt Nam', '2000-10-12', 'Thường', 601, 1380000),
(17, 'Lâm Thị Lan', 'Nữ', '1986-08-18', 'Việt Nam', 'Việt Nam', '2001-12-12', 'Thường', 602, 1320000),
(18, 'Trần Gia Bảo', 'Nam', '1995-09-08', 'Việt Nam', 'Việt Nam', '2004-12-16', 'Thường', 904, 1690000),
(19, 'Nguyễn Hồng Nhung', 'Nữ', '1998-04-21', 'Việt Nam', 'Việt Nam', '2017-10-10', 'Thường', 702, 910000),
(20, 'Lương Quang Hải', 'Nam', '1980-10-10', 'Việt Nam', 'Việt Nam', '2016-08-17', 'Thường', 804, 1570000),
(21, 'Mai Thị Hạnh', 'Nữ', '1992-06-12', 'Việt Nam', 'Việt Nam', '2015-02-20', 'Thường', 801, 1020000), 
(22, 'Phùng Văn Thịnh', 'Nam', '1983-03-04', 'Việt Nam', 'Việt Nam', '2003-12-16', 'Thường', 802, 650000),
(23, 'Nguyễn Thanh Hương', 'Nữ', '1997-07-27', 'Việt Nam', 'Việt Nam', '2006-11-15', 'Thường', 803, 1450000),
(24, 'Đỗ Trọng Khang', 'Nam', '1991-09-15', 'Việt Nam', 'Việt Nam', '2014-12-14', 'Thường', 902, 1950000),
(25, 'Hoàng Mỹ Linh', 'Nữ', '1988-11-09', 'Việt Nam', 'Việt Nam', '2011-01-12', 'Thường', 903, 990000),
(26, 'Trịnh Minh Tuấn', 'Nam', '1996-12-01', 'Việt Nam', 'Việt Nam', '2007-11-29', 'Thường', 905, 1520000),
(27, 'Bùi Hải Yến', 'Nữ', '1994-05-07', 'Việt Nam', 'Việt Nam', '2000-02-02', 'Thường', 603, 750000),
(28, 'Lê Tấn Tài', 'Nam', '1985-01-19', 'Việt Nam', 'Việt Nam', '2001-10-19', 'Thường', 604, 1870000),
(29, 'Vương Phúc An', 'Nam', '1999-10-22', 'Việt Nam', 'Việt Nam', '2002-10-10', 'Thường', 605, 570000),
(30, 'Đặng Quỳnh Hoa', 'Nữ', '1993-07-13', 'Việt Nam', 'Việt Nam', '2008-07-17', 'Thường', 705, 600000);
