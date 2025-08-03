CREATE DATABASE appdb;
USE appdb;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

INSERT INTO products (name) VALUES 
    ('Laptop'), 
    ('Smartphone'), 
    ('Tablet'), 
    ('Headphones'), 
    ('Camera');