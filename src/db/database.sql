
CREATE DATABASE QuanLyNhaTro;
USE QuanLyNhaTro;


CREATE TABLE NguoiThue (
    MaNguoiThue INT PRIMARY KEY AUTO_INCREMENT,
    HoTen VARCHAR(100) NOT NULL,
    SoCMND VARCHAR(50),
    SoDienThoai VARCHAR(20),
    Email VARCHAR(50),
    DuLieuKhuonMat BLOB, 
    NgayTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Phong (
    MaPhong INT PRIMARY KEY AUTO_INCREMENT,
    SoPhong VARCHAR(50) NOT NULL,
    MoTa TEXT,
    GiaThue DECIMAL(10,2),
    TrangThai VARCHAR(20)
);


CREATE TABLE HopDong (
    MaHopDong INT PRIMARY KEY AUTO_INCREMENT,
    MaNguoiThue INT,
    MaPhong INT,
    NgayBatDau DATE,
    NgayKetThuc DATE,
    FOREIGN KEY (MaNguoiThue) REFERENCES NguoiThue(MaNguoiThue),
    FOREIGN KEY (MaPhong) REFERENCES Phong(MaPhong)
);


CREATE TABLE DichVu (
    MaDichVu INT PRIMARY KEY AUTO_INCREMENT,
    TenDichVu VARCHAR(50) NOT NULL,
    DonGia DECIMAL(10,2),
    DonViTinh VARCHAR(20)
);


CREATE TABLE SuDungDichVu (
    MaSuDung INT PRIMARY KEY AUTO_INCREMENT,
    MaPhong INT,
    MaDichVu INT,
    ThangSuDung DATE, 
    ChiSoCu DECIMAL(10,2),
    ChiSoMoi DECIMAL(10,2),
    SoLuong DECIMAL(10,2), 
    ThanhTien DECIMAL(10,2),
    FOREIGN KEY (MaPhong) REFERENCES Phong(MaPhong),
    FOREIGN KEY (MaDichVu) REFERENCES DichVu(MaDichVu)
);


CREATE TABLE ThanhToan (
    MaThanhToan INT PRIMARY KEY AUTO_INCREMENT,
    MaHopDong INT,
    ThangThanhToan DATE, 
    TienPhong DECIMAL(10,2),
    TienDichVu DECIMAL(10,2),
    TongTien DECIMAL(10,2),
    NgayThanhToan DATE,
    TrangThaiThanhToan VARCHAR(20), 
    FOREIGN KEY (MaHopDong) REFERENCES HopDong(MaHopDong)
);


INSERT INTO DichVu (TenDichVu, DonGia, DonViTinh) VALUES
('Dien', 4500, 'kWh'),
('Nuoc', 30000, 'm3'),
('Internet', 200000, 'thang');