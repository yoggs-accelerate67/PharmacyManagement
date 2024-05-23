-- create_tables.sql

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Drugs Table
CREATE TABLE drugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    drug_name VARCHAR(255) NOT NULL,
    manufacturer_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (manufacturer_id) REFERENCES company(id)
);

-- Sales Table
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    drug_id INT,
    quantity INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    sale_date DATE,
    FOREIGN KEY (drug_id) REFERENCES drugs(id)
);

-- History Sales Table
CREATE TABLE history_sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    drug_id INT,
    manufacturer_id INT,
    quantity_sold INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    sale_date DATE,
    FOREIGN KEY (drug_id) REFERENCES drugs(id)
);

-- Company Table
CREATE TABLE company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    industry VARCHAR(255),
);
