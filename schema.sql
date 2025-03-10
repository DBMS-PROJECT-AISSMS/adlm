DROP DATABASE IF EXISTS DigitalLegacyDB;
CREATE DATABASE DigitalLegacyDB;
USE DigitalLegacyDB;

-- Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    is_deceased BOOLEAN DEFAULT FALSE,  -- Death verification
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Digital Assets Table
CREATE TABLE DigitalAssets (
    asset_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    asset_name VARCHAR(255) NOT NULL,
    asset_type ENUM('document', 'image', 'video', 'social_media', 'finance', 'business', 'other') NOT NULL,
    asset_url TEXT NOT NULL,
    is_encrypted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Beneficiaries Table
CREATE TABLE Beneficiaries (
    beneficiary_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    relationship VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Asset Transfers Table
CREATE TABLE AssetTransfers (
    transfer_id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,
    previous_owner_id INT NOT NULL,
    new_owner_id INT NOT NULL,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES DigitalAssets(asset_id) ON DELETE CASCADE,
    FOREIGN KEY (previous_owner_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (new_owner_id) REFERENCES Beneficiaries(beneficiary_id) ON DELETE CASCADE
);

-- Insert Sample Data
-- Users (3 Users: 2 Regular Users, 1 Admin)
INSERT INTO Users (username, email, password_hash, role) VALUES
('smriti', 'smriti@example.com', '$2b$12$KIXQ1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1', 'user'),  -- password: smriti_password
('pooja', 'pooja@example.com', '$2b$12$KIXQ1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1', 'admin'),  -- password: admin_password
('admin_user', 'admin@example.com', '$2b$12$KIXQ1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1Q1Z1', 'admin'); -- password: admin_password

-- Digital Assets (Assigned to Users)
INSERT INTO DigitalAssets (owner_id, asset_name, asset_type, asset_url, is_encrypted) VALUES
(1, 'My Will Document', 'document', 'http://example.com/mywill.pdf', TRUE),
(1, 'Family Photos', 'image', 'http://example.com/familyphotos', FALSE),
(2, 'Stock Portfolio', 'finance', 'http://example.com/portfolio', TRUE);

-- Beneficiaries (Users' Family Members)
INSERT INTO Beneficiaries (user_id, name, relationship, email) VALUES
(1, 'Jane Doe', 'Wife', 'jane.doe@example.com'),
(2, 'Sarah Lee', 'Mother', 'sarah.lee@example.com');

-- Asset Transfers (Track Past Transfers)
INSERT INTO AssetTransfers (asset_id, previous_owner_id, new_owner_id) VALUES
(1, 1, 2);  -- Smriti’s Will Document → Pooja