-- Create the database
CREATE DATABASE mango_orders;

-- Use the database
USE mango_orders;

-- Create the orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    alphonso_quantity VARCHAR(50) NOT NULL,
    ratnagiri_quantity VARCHAR(50) NOT NULL,
    kesar_quantity VARCHAR(50) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);