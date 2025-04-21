-- Create Database
CREATE DATABASE my_website;

USE my_website;

-- Create 'categories' Table
CREATE TABLE categories (
    id INT IDENTITY(1,1) PRIMARY KEY, 
    name NVARCHAR(100) NULL, 
    description NVARCHAR(MAX) NULL,
    delete_flg BIT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE()
);

-- Add comment for 'price' column
EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Giá bán sản phẩm', 
    @level0type = N'SCHEMA', @level0name = 'dbo', 
    @level1type = N'TABLE',  @level1name = 'products', 
    @level2type = N'COLUMN', @level2name = 'price';

-- Add comment for 'products' table
EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Bảng chứa thông tin danh mục sản phẩm', 
    @level0type = N'SCHEMA', @level0name = 'dbo', 
    @level1type = N'TABLE',  @level1name = 'categories';

-- Trigger to update 'updated_at' in 'categories' table
CREATE TRIGGER trg_categories_updated_at
ON categories
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE categories
    SET updated_at = GETDATE()
    FROM categories p
    INNER JOIN inserted i ON p.id = i.id;
END;

-- Create 'products' Table
CREATE TABLE products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL, 
    summary NVARCHAR(255) NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    description NVARCHAR(MAX) NULL,
    delete_flg BIT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),
    category_id INT NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Create 'auth' Table
CREATE TABLE auth (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(100) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL,
    is_admin BIT NOT NULL DEFAULT 0,
    is_staff BIT NOT NULL DEFAULT 0,
    is_active BIT NOT NULL DEFAULT 1,
    delete_flg BIT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE()
);

-- Create 'users' Table
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    last_name NVARCHAR(50) NULL,
    first_name NVARCHAR(50) NULL,
    phone_number NVARCHAR(20) NULL,
    email NVARCHAR(50) NULL,
    position NVARCHAR(100) NULL,
    department NVARCHAR(100) NULL,
    delete_flg BIT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),
    auth_id INT NOT NULL UNIQUE,
    CONSTRAINT fk_auth FOREIGN KEY (auth_id) REFERENCES auth(id)
);

-- Create 'customers' Table
CREATE TABLE customers (
    id INT IDENTITY(1,1) PRIMARY KEY,
    last_name NVARCHAR(50) NULL,
    first_name NVARCHAR(50) NULL,
    phone_number NVARCHAR(20) NULL,
    email NVARCHAR(50) NULL,
    address NVARCHAR(100) NULL,
    auth_id INT NOT NULL UNIQUE,
    CONSTRAINT fk_customer_auth FOREIGN KEY (auth_id) REFERENCES auth(id)
);

-- Create 'orders' Table
CREATE TABLE orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_number NVARCHAR(50) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    user_id INT NULL,
    status NVARCHAR(20) NOT NULL DEFAULT 'ORDERED',
    description NVARCHAR(MAX) NULL,
    delete_flg BIT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_order_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create 'order_items' Table
CREATE TABLE order_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price AS (quantity * unit_price) PERSISTED,
    description NVARCHAR(MAX) NULL,
    delete_flg BIT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_order_item_order FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_order_item_product FOREIGN KEY (product_id) REFERENCES products(id)
);


-- Insert data into 'categories' table
INSERT INTO categories (name, description)
VALUES 
('Electronics', 'Devices, gadgets and tech products'),
('Furniture', 'Home and office furniture'),
('Clothing', 'Men and Women fashion wear'),
('Books', 'Various genres of books'),
('Toys', 'Toys and games for kids');

-- Insert data into 'products' table
INSERT INTO products (name, summary, price, quantity, description, category_id)
VALUES 
('Laptop', 'High performance laptop', 1200.00, 10, 'A powerful laptop with fast processor', 1),
('Sofa', 'Comfortable leather sofa', 500.00, 5, 'Elegant leather sofa for home living rooms', 2),
('T-shirt', 'Cotton T-shirt for men', 20.00, 100, 'Soft cotton T-shirt available in various sizes', 3),
('Novel', 'Fictional novel about adventure', 15.00, 50, 'An exciting adventure novel for young adults', 4),
('Action Figure', 'Superhero action figure toy', 25.00, 200, 'Collectible superhero action figure', 5);

-- Insert data into 'auth' table
INSERT INTO auth (username, password, is_admin, is_staff, is_active)
VALUES 
('admin1', 'password1', 1, 1, 1),
('staff1', 'password2', 0, 1, 1),
('customer1', 'password3', 0, 0, 1),
('admin2', 'password4', 1, 1, 1),
('staff2', 'password5', 0, 1, 1);

-- Insert data into 'users' table
INSERT INTO users (last_name, first_name, phone_number, email, position, department, auth_id)
VALUES 
('Doe', 'John', '1234567890', 'john.doe@example.com', 'Manager', 'Sales', 1),
('Smith', 'Jane', '2345678901', 'jane.smith@example.com', 'Staff', 'Marketing', 2),
('Brown', 'Charlie', '3456789012', 'charlie.brown@example.com', 'Customer Service', 'Support', 3),
('Taylor', 'James', '4567890123', 'james.taylor@example.com', 'Admin', 'HR', 4),
('Wilson', 'Emily', '5678901234', 'emily.wilson@example.com', 'Staff', 'Support', 5);

-- Insert data into 'customers' table
INSERT INTO customers (last_name, first_name, phone_number, email, address, auth_id)
VALUES 
('Johnson', 'Chris', '6789012345', 'chris.johnson@example.com', '123 Elm St', 3),
('Williams', 'Alex', '7890123456', 'alex.williams@example.com', '456 Oak St', 4),
('Jones', 'Patricia', '8901234567', 'patricia.jones@example.com', '789 Pine St', 1),
('Miller', 'Samuel', '9012345678', 'samuel.miller@example.com', '101 Maple St', 2),
('Davis', 'Emma', '0123456789', 'emma.davis@example.com', '202 Birch St', 5);

-- Insert data into 'orders' table
INSERT INTO orders (order_number, customer_id, user_id, status, description)
VALUES 
('ORD001', 1, 1, 'ORDERED', 'Order for electronics'),
('ORD002', 2, 2, 'SHIPPING', 'Furniture order being processed'),
('ORD003', 3, 3, 'CANCELLED', 'Cancelled book order'),
('ORD004', 4, 4, 'COMPLETED', 'Completed clothing order'),
('ORD005', 5, 5, 'ORDERED', 'Toy order placed');

-- Insert data into 'order_items' table
INSERT INTO order_items (order_id, product_id, quantity, unit_price, description)
VALUES 
(1, 1, 1, 1200.00, 'Laptop for work and study'),
(2, 2, 2, 500.00, 'Two leather sofas'),
(3, 4, 1, 15.00, 'Fictional adventure novel'),
(4, 3, 3, 20.00, 'Men’s T-shirt, size M'),
(5, 5, 5, 25.00, 'Superhero action figures for collection');
