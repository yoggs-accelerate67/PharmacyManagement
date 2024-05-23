-- Create the login table
CREATE TABLE login (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (id) REFERENCES users(id)
);

-- Create the invoice table
CREATE TABLE invoice (
    id INT PRIMARY KEY AUTO_INCREMENT,
    drug_id INT,
    manufacturer_id INT NOT NULL,
    company_phone_number VARCHAR(10),
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (drug_id) REFERENCES drugs(id),
    FOREIGN KEY (manufacturer_id , company_phone_number) REFERENCES company(id , phone_number)
);

-- Create the users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    address VARCHAR(255)
);

-- Create the drugs table
CREATE TABLE drugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    manufacturer_id INT NOT NULL,
    expiration_date DATE,
    unit_price DECIMAL(10, 2) NOT NULL,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (manufacturer_id) REFERENCES company(id)
);

-- Sales Table
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    drug_id INT,
    manufacturer_id INT NOT NULL,
    quantity INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    sale_date DATE,
    manufacturer_id INT 
    FOREIGN KEY (drug_id) REFERENCES drugs(id)
    FOREIGN KEY (manufacturer_id) REFERENCES Company(id)
);

-- Create the history_sales table
CREATE TABLE history_sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    drug_id INT,
    manufacturer_id INT NOT NULL,
    quantity_sold INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    sale_date DATE NOT NULL,
    drug_name VARCHAR(255),
    FOREIGN KEY (drug_id) REFERENCES drugs(id),
    FOREIGN KEY (manufacturer_id) REFERENCES company(id)
);

-- Create the company table
CREATE TABLE company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    industry VARCHAR(255),
    phone_number VARCHAR(10)
);
