-- Tạo cơ sở dữ liệu
CREATE DATABASE IF NOT EXISTS quanlynhatro;
USE quanlynhatro;

-- Bảng rooms
DROP TABLE IF EXISTS rooms;
CREATE TABLE rooms (
    id INTEGER NOT NULL PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    price FLOAT NOT NULL,
    status VARCHAR(20)
);

-- Bảng services
DROP TABLE IF EXISTS services;
CREATE TABLE services (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL
);

-- Bảng tenants
DROP TABLE IF EXISTS tenants;
CREATE TABLE tenants (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    identity_number VARCHAR(20) UNIQUE,
    image_path VARCHAR(200),
    move_in_date DATETIME,
    room_id INTEGER NOT NULL REFERENCES rooms.id,
    user_id INTEGER REFERENCES users.id
);

-- Bảng users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(10) NOT NULL,
    tenant_id INTEGER REFERENCES tenants.id
);

-- Bảng bills
DROP TABLE IF EXISTS bills;
CREATE TABLE bills (
    id INTEGER NOT NULL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants.id,
    room_id INTEGER NOT NULL REFERENCES rooms.id,
    total_amount FLOAT NOT NULL,
    created_at DATETIME
);

-- Bảng bill_services
DROP TABLE IF EXISTS bill_services;
CREATE TABLE bill_services (
    bill_id INTEGER NOT NULL PRIMARY KEY REFERENCES bills.id,
    service_id INTEGER NOT NULL PRIMARY KEY REFERENCES services.id
);

