-- Booth Organizer System Database Schema
-- MySQL Database

CREATE DATABASE IF NOT EXISTS booth_system;
USE booth_system;

-- 1. Users Table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    citizen_id VARCHAR(20),
    contact_info VARCHAR(100),
    role ENUM('GENERAL_USER','MERCHANT','BOOTH_MANAGER') NOT NULL,
    approval_status ENUM('PENDING','APPROVED','REJECTED') DEFAULT 'PENDING',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Merchants Table
CREATE TABLE merchants (
    merchant_id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    seller_information TEXT,
    product_description TEXT,
    approved_by CHAR(36),
    approved_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- 3. Events Table
CREATE TABLE events (
    event_id CHAR(36) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    location VARCHAR(200),
    start_date DATE,
    end_date DATE,
    created_by CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- 4. Booths Table
CREATE TABLE booths (
    booth_id CHAR(36) PRIMARY KEY,
    event_id CHAR(36) NOT NULL,
    booth_number VARCHAR(20) NOT NULL,
    size VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    location VARCHAR(100),
    type ENUM('INDOOR','OUTDOOR') NOT NULL,
    classification ENUM('FIXED','TEMPORARY') NOT NULL,
    duration_type ENUM('SHORT_TERM','LONG_TERM') NOT NULL,
    electricity BOOLEAN DEFAULT FALSE,
    water_supply BOOLEAN DEFAULT FALSE,
    outlets INT DEFAULT 0,
    status ENUM('AVAILABLE','RESERVED','OCCUPIED') DEFAULT 'AVAILABLE',
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- 5. Reservations Table
CREATE TABLE reservations (
    reservation_id CHAR(36) PRIMARY KEY,
    booth_id CHAR(36) NOT NULL,
    merchant_id CHAR(36) NOT NULL,
    reservation_type ENUM('SHORT_TERM','LONG_TERM') NOT NULL,
    status ENUM('PENDING_PAYMENT','CONFIRMED','CANCELLED') DEFAULT 'PENDING_PAYMENT',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booth_id) REFERENCES booths(booth_id),
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

-- 6. Payments Table
CREATE TABLE payments (
    payment_id CHAR(36) PRIMARY KEY,
    reservation_id CHAR(36) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    method ENUM('CREDIT_CARD','TRUEMONEY','BANK_TRANSFER') NOT NULL,
    payment_status ENUM('PENDING','APPROVED','REJECTED') DEFAULT 'PENDING',
    slip_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id)
);