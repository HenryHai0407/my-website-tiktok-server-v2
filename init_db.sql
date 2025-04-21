-- db my-website
CREATE DATABASE my-website;

USE my-website;


CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID danh muc san pham',
    name VARCHAR(100),
    description TEXT,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT = 'Thong tin danh muc san pham';;


CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    summary VARCHAR(255),
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    description TEXT,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    category_id INT NOT NULL,
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


CREATE TABLE auth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    phone_number VARCHAR(20),
    email VARCHAR(50),
    position VARCHAR(100),
    department VARCHAR(100),
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    
    auth_id INT NOT NULL UNIQUE,
    FOREIGN KEY (auth_id) REFERENCES auth(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    phone_number VARCHAR(20),
    email VARCHAR(50),
    address VARCHAR(100),
    
    auth_id INT NOT NULL UNIQUE,
    FOREIGN KEY (auth_id) REFERENCES auth(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    
    customer_id INT NOT NULL,
    user_id INT,

    status ENUM('ORDERED', 'SHIPPING', 'CANCELLED', 'COMPLETED') NOT NULL DEFAULT 'ORDERED',

    description TEXT,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,

    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    
    description TEXT,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (product_id) REFERENCES products(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


-- Sample preview data (5 records per table) for my-website DB

-- categories
INSERT INTO categories (name, description) VALUES
('Category 1', 'Description for category 1'),
('Category 2', 'Description for category 2'),
('Category 3', 'Description for category 3'),
('Category 4', 'Description for category 4'),
('Category 5', 'Description for category 5');

-- auth
INSERT INTO auth (username, password_hash, is_admin, is_staff, is_active) VALUES
('auth1', 'hashed_pwd_1', 1, 0, 1),
('auth2', 'hashed_pwd_2', 1, 0, 1),
('auth3', 'hashed_pwd_3', 0, 0, 1),
('auth4', 'hashed_pwd_4', 0, 0, 1),
('auth5', 'hashed_pwd_5', 0, 0, 1);

-- users
INSERT INTO users (last_name, first_name, phone_number, email, position, department, auth_id) VALUES
('UserLast1', 'UserFirst1', '091100001', 'user1@example.com', 'Position 1', 'Dept 1', 1),
('UserLast2', 'UserFirst2', '091100002', 'user2@example.com', 'Position 2', 'Dept 2', 2);

-- customers
INSERT INTO customers (last_name, first_name, phone_number, email, address, auth_id) VALUES
('Last3', 'First3', '090000003', 'customer3@example.com', 'Address 3', 3),
('Last4', 'First4', '090000004', 'customer4@example.com', 'Address 4', 4),
('Last5', 'First5', '090000005', 'customer5@example.com', 'Address 5', 5);

-- products
INSERT INTO products (name, summary, price, quantity, description, category_id) VALUES
('Product 1', 'Summary 1', 77.69, 84, 'Description for product 1', 2),
('Product 2', 'Summary 2', 86.29, 1, 'Description for product 2', 1),
('Product 3', 'Summary 3', 34.75, 96, 'Description for product 3', 3),
('Product 4', 'Summary 4', 17.45, 55, 'Description for product 4', 4),
('Product 5', 'Summary 5', 90.53, 38, 'Description for product 5', 5);

-- orders
INSERT INTO orders (order_number, customer_id, user_id, status, description) VALUES
('ORD0001', 1, 1, 'CANCELLED', 'Order 3 description'),
('ORD0002', 2, 1, 'ORDERED', 'Order 4 description'),
('ORD0003', 3, 1, 'COMPLETED', 'Order 5 description');

-- order_items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, description) VALUES
(1, 1, 1, 92.24, 'Item 1'),
(2, 2, 4, 18.42, 'Item 2'),
(3, 3, 5, 19.45, 'Item 3');
