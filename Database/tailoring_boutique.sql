-- ============================================================
-- DBMS COURSE PROJECT — PROJECT 68
-- TAILORING AND BOUTIQUE ORDER MANAGEMENT SYSTEM
-- MySQL 8.x
-- ============================================================

CREATE DATABASE IF NOT EXISTS tailoring_boutique;
USE tailoring_boutique;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS alterations;
DROP TABLE IF EXISTS trials;
DROP TABLE IF EXISTS tailor_assignments;
DROP TABLE IF EXISTS fabric_issues;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS fabric_stock;
DROP TABLE IF EXISTS fabrics;
DROP TABLE IF EXISTS designs;
DROP TABLE IF EXISTS garment_types;
DROP TABLE IF EXISTS tailors;
DROP TABLE IF EXISTS measurement_profiles;
DROP TABLE IF EXISTS customers;
SET FOREIGN_KEY_CHECKS = 1;

-- ---------------- CUSTOMER ----------------
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_code VARCHAR(10) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(120) UNIQUE,
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------- MEASUREMENTS ----------------
CREATE TABLE measurement_profiles (
    measurement_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL UNIQUE,
    bust_cm DECIMAL(5,2) CHECK (bust_cm > 0),
    waist_cm DECIMAL(5,2) CHECK (waist_cm > 0),
    hip_cm DECIMAL(5,2) CHECK (hip_cm > 0),
    shoulder_cm DECIMAL(5,2) CHECK (shoulder_cm > 0),
    sleeve_cm DECIMAL(5,2) CHECK (sleeve_cm > 0),
    length_cm DECIMAL(5,2) CHECK (length_cm > 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_measure_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

-- ---------------- GARMENT TYPES ----------------
CREATE TABLE garment_types (
    garment_type_id INT AUTO_INCREMENT PRIMARY KEY,
    garment_name VARCHAR(60) NOT NULL UNIQUE,
    description VARCHAR(255),
    base_price DECIMAL(10,2) NOT NULL CHECK (base_price >= 0)
);

-- ---------------- DESIGNS ----------------
CREATE TABLE designs (
    design_id INT AUTO_INCREMENT PRIMARY KEY,
    design_code VARCHAR(15) NOT NULL UNIQUE,
    design_name VARCHAR(100) NOT NULL,
    garment_type_id INT NOT NULL,
    description VARCHAR(255),
    CONSTRAINT fk_design_garment
        FOREIGN KEY (garment_type_id) REFERENCES garment_types(garment_type_id)
);

-- ---------------- FABRICS ----------------
CREATE TABLE fabrics (
    fabric_id INT AUTO_INCREMENT PRIMARY KEY,
    fabric_code VARCHAR(15) NOT NULL UNIQUE,
    fabric_name VARCHAR(100) NOT NULL,
    fabric_type VARCHAR(50) NOT NULL,
    colour VARCHAR(40),
    price_per_meter DECIMAL(10,2) NOT NULL CHECK (price_per_meter >= 0)
);

-- ---------------- FABRIC STOCK ----------------
CREATE TABLE fabric_stock (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    fabric_id INT NOT NULL UNIQUE,
    quantity_meters DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (quantity_meters >= 0),
    reorder_level DECIMAL(10,2) NOT NULL DEFAULT 5 CHECK (reorder_level >= 0),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_stock_fabric
        FOREIGN KEY (fabric_id) REFERENCES fabrics(fabric_id)
        ON DELETE CASCADE
);

-- ---------------- ORDERS ----------------
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_no VARCHAR(20) NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    delivery_date DATE NOT NULL,
    status ENUM('PLACED','IN_PROGRESS','TRIAL','ALTERATION','READY','DELIVERED','CANCELLED')
        NOT NULL DEFAULT 'PLACED',
    special_instructions VARCHAR(500),
    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT chk_delivery_date CHECK (delivery_date >= order_date)
);

-- ---------------- ORDER ITEMS ----------------
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    garment_type_id INT NOT NULL,
    design_id INT,
    fabric_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    fabric_required_meters DECIMAL(10,2) NOT NULL CHECK (fabric_required_meters > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    CONSTRAINT fk_item_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_item_garment
        FOREIGN KEY (garment_type_id) REFERENCES garment_types(garment_type_id),
    CONSTRAINT fk_item_design
        FOREIGN KEY (design_id) REFERENCES designs(design_id),
    CONSTRAINT fk_item_fabric
        FOREIGN KEY (fabric_id) REFERENCES fabrics(fabric_id)
);

-- ---------------- FABRIC ISSUE ----------------
-- Transaction table used to record fabric issued against an order item.
CREATE TABLE fabric_issues (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    order_item_id INT NOT NULL,
    fabric_id INT NOT NULL,
    issue_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    quantity_meters DECIMAL(10,2) NOT NULL CHECK (quantity_meters > 0),
    CONSTRAINT fk_issue_item
        FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id) ON DELETE CASCADE,
    CONSTRAINT fk_issue_fabric
        FOREIGN KEY (fabric_id) REFERENCES fabrics(fabric_id)
);

-- ---------------- TAILORS ----------------
CREATE TABLE tailors (
    tailor_id INT AUTO_INCREMENT PRIMARY KEY,
    tailor_code VARCHAR(15) NOT NULL UNIQUE,
    tailor_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(80),
    phone VARCHAR(15) UNIQUE,
    status ENUM('ACTIVE','INACTIVE') NOT NULL DEFAULT 'ACTIVE'
);

-- ---------------- ASSIGNMENTS ----------------
CREATE TABLE tailor_assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    tailor_id INT NOT NULL,
    assigned_on DATE NOT NULL DEFAULT (CURRENT_DATE),
    expected_completion DATE,
    assignment_status ENUM('ASSIGNED','IN_PROGRESS','COMPLETED') NOT NULL DEFAULT 'ASSIGNED',
    UNIQUE(order_id, tailor_id),
    CHECK (expected_completion IS NULL OR expected_completion >= assigned_on),
    CONSTRAINT fk_assignment_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_assignment_tailor
        FOREIGN KEY (tailor_id) REFERENCES tailors(tailor_id)
);

-- ---------------- TRIALS ----------------
CREATE TABLE trials (
    trial_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    tailor_id INT NOT NULL,
    trial_datetime DATETIME NOT NULL,
    trial_status ENUM('SCHEDULED','COMPLETED','RESCHEDULED','CANCELLED')
        NOT NULL DEFAULT 'SCHEDULED',
    notes VARCHAR(255),
    UNIQUE(tailor_id, trial_datetime),
    CONSTRAINT fk_trial_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_trial_tailor
        FOREIGN KEY (tailor_id) REFERENCES tailors(tailor_id)
);

-- ---------------- ALTERATIONS ----------------
CREATE TABLE alterations (
    alteration_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    trial_id INT,
    alteration_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    alteration_details VARCHAR(500) NOT NULL,
    alteration_cost DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (alteration_cost >= 0),
    alteration_status ENUM('PENDING','IN_PROGRESS','COMPLETED')
        NOT NULL DEFAULT 'PENDING',
    CONSTRAINT fk_alteration_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_alteration_trial
        FOREIGN KEY (trial_id) REFERENCES trials(trial_id) ON DELETE SET NULL
);

-- ---------------- INVOICES ----------------
CREATE TABLE invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_no VARCHAR(20) NOT NULL UNIQUE,
    order_id INT NOT NULL UNIQUE,
    invoice_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    alteration_total DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (alteration_total >= 0),
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    CONSTRAINT fk_invoice_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CHECK (total_amount = subtotal + alteration_total)
);

-- ---------------- PAYMENTS ----------------
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT NOT NULL,
    payment_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    payment_method ENUM('CASH','UPI','CARD','BANK_TRANSFER') NOT NULL,
    reference_no VARCHAR(40) UNIQUE,
    CONSTRAINT fk_payment_invoice
        FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id) ON DELETE CASCADE
);

-- ---------------- INDEXES ----------------
CREATE INDEX idx_orders_delivery_status ON orders(delivery_date, status);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_trials_datetime ON trials(trial_datetime);
CREATE INDEX idx_payments_invoice ON payments(invoice_id);
CREATE INDEX idx_fabric_issue_date ON fabric_issues(issue_date);

-- ============================================================
-- BUSINESS-RULE TRIGGERS
-- ============================================================

DELIMITER $$

-- Fabric issue cannot exceed available stock.
CREATE TRIGGER trg_fabric_issue_before_insert
BEFORE INSERT ON fabric_issues
FOR EACH ROW
BEGIN
    DECLARE available DECIMAL(10,2);
    DECLARE stock_fabric INT;

    SELECT quantity_meters, fabric_id
      INTO available, stock_fabric
      FROM fabric_stock
     WHERE fabric_id = NEW.fabric_id
     FOR UPDATE;

    IF stock_fabric IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Fabric stock record does not exist.';
    END IF;

    IF NEW.quantity_meters > available THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Fabric issue exceeds available stock.';
    END IF;
END$$

-- Deduct issued fabric from stock.
CREATE TRIGGER trg_fabric_issue_after_insert
AFTER INSERT ON fabric_issues
FOR EACH ROW
BEGIN
    UPDATE fabric_stock
       SET quantity_meters = quantity_meters - NEW.quantity_meters
     WHERE fabric_id = NEW.fabric_id;
END$$

-- Payment cannot exceed invoice balance.
CREATE TRIGGER trg_payment_before_insert
BEFORE INSERT ON payments
FOR EACH ROW
BEGIN
    DECLARE invoice_total DECIMAL(10,2);
    DECLARE paid_total DECIMAL(10,2);

    SELECT total_amount INTO invoice_total
      FROM invoices WHERE invoice_id = NEW.invoice_id;

    SELECT COALESCE(SUM(amount),0) INTO paid_total
      FROM payments WHERE invoice_id = NEW.invoice_id;

    IF NEW.amount + paid_total > invoice_total THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Payment exceeds remaining invoice balance.';
    END IF;
END$$

DELIMITER ;

-- ============================================================
-- SAMPLE DATA: 5+ RECORDS PER TABLE
-- ============================================================

INSERT INTO customers(customer_id,customer_code,full_name,phone,email,address) VALUES
(1,'C001','Aanya Sharma','9876500001','aanya@example.com','Banjara Hills, Hyderabad'),
(2,'C002','Riya Mehta','9876500002','riya@example.com','Kondapur, Hyderabad'),
(3,'C003','Kavya Singh','9876500003','kavya@example.com','Gachibowli, Hyderabad'),
(4,'C004','Meera Patel','9876500004','meera@example.com','Madhapur, Hyderabad'),
(5,'C005','Ananya Rao','9876500005','ananya@example.com','Begumpet, Hyderabad'),
(6,'C006','Nisha Verma','9876500006','nisha@example.com','Jubilee Hills, Hyderabad');

INSERT INTO measurement_profiles(measurement_id,customer_id,bust_cm,waist_cm,hip_cm,shoulder_cm,sleeve_cm,length_cm) VALUES
(1,1,86,70,92,36,56,42),(2,2,90,74,96,37,57,44),(3,3,88,72,94,36,55,43),
(4,4,92,78,100,38,58,45),(5,5,84,68,90,35,54,41),(6,6,94,80,102,39,59,46);

INSERT INTO garment_types VALUES
(1,'Kurti','Custom stitched kurti',1200),(2,'Blouse','Designer blouse',1800),
(3,'Lehenga','Bridal/festive lehenga',6500),(4,'Salwar Suit','Custom salwar suit',2500),
(5,'Gown','Evening gown',4500),(6,'Saree Blouse','Traditional blouse',1600);

INSERT INTO designs VALUES
(1,'D001','Floral Neckline',1,'Floral embroidered neckline'),
(2,'D002','Princess Cut',2,'Fitted princess cut'),
(3,'D003','Mirror Work',3,'Mirror work festive design'),
(4,'D004','Straight Cut',4,'Classic straight cut'),
(5,'D005','A-Line',5,'Elegant A-line gown'),
(6,'D006','Boat Neck',6,'Simple boat neck blouse');

INSERT INTO fabrics VALUES
(1,'F001','Cotton Slub','Cotton','Pink',420),
(2,'F002','Raw Silk','Silk','Maroon',850),
(3,'F003','Georgette','Synthetic','Black',620),
(4,'F004','Velvet','Velvet','Wine',1100),
(5,'F005','Chanderi','Cotton Silk','Gold',980),
(6,'F006','Organza','Silk Blend','Ivory',760);

INSERT INTO fabric_stock VALUES
(1,1,45,10),(2,2,32,8),(3,3,28,6),(4,4,20,5),(5,5,38,8),(6,6,25,5);

INSERT INTO tailors VALUES
(1,'T001','Ramesh Kumar','Blouse Specialist','9000000001','ACTIVE'),
(2,'T002','Sana Khan','Lehenga Specialist','9000000002','ACTIVE'),
(3,'T003','Priya Nair','Western Wear','9000000003','ACTIVE'),
(4,'T004','Arjun Das','Traditional Wear','9000000004','ACTIVE'),
(5,'T005','Neha Joshi','Alterations','9000000005','ACTIVE'),
(6,'T006','Vikram Rao','General Tailoring','9000000006','ACTIVE');

INSERT INTO orders(order_id,order_no,customer_id,order_date,delivery_date,status,special_instructions) VALUES
(1,'ORD001',1,'2026-10-01','2026-10-10','IN_PROGRESS','Add lining'),
(2,'ORD002',2,'2026-10-01','2026-10-08','TRIAL','Fitting required'),
(3,'ORD003',3,'2026-10-02','2026-10-15','PLACED','Festive order'),
(4,'ORD004',4,'2026-10-03','2026-10-12','ALTERATION','Shorten sleeves'),
(5,'ORD005',5,'2026-10-03','2026-10-20','READY','Ready for collection'),
(6,'ORD006',6,'2026-10-04','2026-10-18','PLACED','Ivory finishing');

INSERT INTO order_items VALUES
(1,1,1,1,1,1,2.20,1450),
(2,2,2,2,2,1,1.80,2350),
(3,3,3,3,5,1,5.50,8200),
(4,4,4,4,3,1,3.00,3200),
(5,5,5,5,4,1,4.00,5600),
(6,6,6,6,6,1,1.70,2100);

INSERT INTO tailor_assignments VALUES
(1,1,1,'2026-10-01','2026-10-08','IN_PROGRESS'),
(2,2,2,'2026-10-01','2026-10-06','COMPLETED'),
(3,3,4,'2026-10-02','2026-10-12','ASSIGNED'),
(4,4,5,'2026-10-03','2026-10-10','IN_PROGRESS'),
(5,5,3,'2026-10-03','2026-10-15','COMPLETED'),
(6,6,6,'2026-10-04','2026-10-16','ASSIGNED');

INSERT INTO trials VALUES
(1,1,1,'2026-10-06 11:00:00','COMPLETED','Minor waist adjustment'),
(2,2,2,'2026-10-05 15:00:00','COMPLETED','Check neckline'),
(3,3,4,'2026-10-10 11:00:00','SCHEDULED','First fitting'),
(4,4,5,'2026-10-07 12:00:00','SCHEDULED','Sleeve alteration'),
(5,5,3,'2026-10-09 16:00:00','COMPLETED','Final fitting'),
(6,6,6,'2026-10-12 11:00:00','SCHEDULED','Initial trial');

INSERT INTO alterations VALUES
(1,1,1,'2026-10-06','Reduce waist by 1 cm',150,'COMPLETED'),
(2,2,2,'2026-10-05','Adjust neckline',200,'COMPLETED'),
(3,3,3,'2026-10-10','Tighten waist',250,'PENDING'),
(4,4,4,'2026-10-07','Shorten sleeves',180,'IN_PROGRESS'),
(5,5,5,'2026-10-09','No alteration required',0,'COMPLETED'),
(6,6,6,'2026-10-12','Check shoulder fit',200,'PENDING');

INSERT INTO invoices VALUES
(1,'INV001',1,'2026-10-06',1450,150,1600),
(2,'INV002',2,'2026-10-05',2350,200,2550),
(3,'INV003',3,'2026-10-04',8200,250,8450),
(4,'INV004',4,'2026-10-07',3200,180,3380),
(5,'INV005',5,'2026-10-09',5600,0,5600),
(6,'INV006',6,'2026-10-05',2100,200,2300);

INSERT INTO payments VALUES
(1,1,'2026-10-01',800,'UPI','UPI1001'),
(2,2,'2026-10-01',1000,'CARD','CARD1002'),
(3,3,'2026-10-04',4000,'UPI','UPI1003'),
(4,4,'2026-10-07',1500,'CASH','CASH1004'),
(5,5,'2026-10-09',5600,'UPI','UPI1005'),
(6,6,'2026-10-05',1000,'BANK_TRANSFER','BANK1006');

-- Issue fabric only after all parent rows exist.
INSERT INTO fabric_issues(issue_id,order_item_id,fabric_id,issue_date,quantity_meters) VALUES
(1,1,1,'2026-10-02',2.00),
(2,2,2,'2026-10-02',1.50),
(3,3,5,'2026-10-03',5.00),
(4,4,3,'2026-10-04',2.50),
(5,5,4,'2026-10-04',3.50),
(6,6,6,'2026-10-05',1.50);

-- ============================================================
-- VIEWS / REPORTS
-- ============================================================

CREATE OR REPLACE VIEW v_pending_orders AS
SELECT o.order_no, c.full_name AS customer, o.order_date, o.delivery_date, o.status
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status NOT IN ('DELIVERED','CANCELLED');

CREATE OR REPLACE VIEW v_delivery_due AS
SELECT o.order_no, c.full_name AS customer, o.delivery_date, o.status
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.delivery_date <= DATE_ADD(CURRENT_DATE, INTERVAL 7 DAY)
  AND o.status NOT IN ('DELIVERED','CANCELLED');

CREATE OR REPLACE VIEW v_tailor_workload AS
SELECT t.tailor_name, COUNT(ta.assignment_id) AS assigned_orders,
       SUM(ta.assignment_status <> 'COMPLETED') AS active_orders
FROM tailors t
LEFT JOIN tailor_assignments ta ON ta.tailor_id=t.tailor_id
GROUP BY t.tailor_id, t.tailor_name;

CREATE OR REPLACE VIEW v_customer_history AS
SELECT c.customer_code, c.full_name, o.order_no, o.order_date,
       o.delivery_date, o.status, i.total_amount
FROM customers c
LEFT JOIN orders o ON o.customer_id=c.customer_id
LEFT JOIN invoices i ON i.order_id=o.order_id;

CREATE OR REPLACE VIEW v_revenue AS
SELECT DATE_FORMAT(invoice_date,'%Y-%m') AS revenue_month,
       SUM(total_amount) AS invoiced_revenue,
       SUM(COALESCE((SELECT SUM(p.amount) FROM payments p WHERE p.invoice_id=i.invoice_id),0)) AS collected_amount
FROM invoices i
GROUP BY DATE_FORMAT(invoice_date,'%Y-%m');

-- ============================================================
-- REQUIRED DEMO QUERIES
-- ============================================================

-- 1. Simple SELECT
SELECT * FROM customers;

-- 2. INNER JOIN
SELECT o.order_no, c.full_name, o.delivery_date, o.status
FROM orders o
INNER JOIN customers c ON c.customer_id=o.customer_id;

-- 3. Aggregate
SELECT status, COUNT(*) AS total_orders
FROM orders
GROUP BY status;

-- 4. Revenue
SELECT SUM(total_amount) AS total_invoice_value FROM invoices;

-- 5. Tailor workload
SELECT t.tailor_name, COUNT(ta.assignment_id) AS orders_assigned
FROM tailors t
LEFT JOIN tailor_assignments ta ON ta.tailor_id=t.tailor_id
GROUP BY t.tailor_id, t.tailor_name;

-- 6. Fabric use
SELECT f.fabric_name, SUM(fi.quantity_meters) AS meters_issued
FROM fabrics f
JOIN fabric_issues fi ON fi.fabric_id=f.fabric_id
GROUP BY f.fabric_id, f.fabric_name;

-- 7. Nested query: customers with above-average order value
SELECT c.full_name, i.total_amount
FROM customers c
JOIN orders o ON o.customer_id=c.customer_id
JOIN invoices i ON i.order_id=o.order_id
WHERE i.total_amount > (SELECT AVG(total_amount) FROM invoices);

-- 8. Pending orders view
SELECT * FROM v_pending_orders;

-- 9. Delivery due view
SELECT * FROM v_delivery_due;

-- 10. Customer history
SELECT * FROM v_customer_history WHERE customer_code='C001';

-- 11. Alterations
SELECT o.order_no, a.alteration_details, a.alteration_cost, a.alteration_status
FROM alterations a JOIN orders o ON o.order_id=a.order_id;

-- 12. Payment balance
SELECT i.invoice_no, i.total_amount,
       COALESCE(SUM(p.amount),0) AS paid,
       i.total_amount-COALESCE(SUM(p.amount),0) AS balance
FROM invoices i
LEFT JOIN payments p ON p.invoice_id=i.invoice_id
GROUP BY i.invoice_id, i.invoice_no, i.total_amount;

-- ============================================================
-- OPTIONAL DEMO TRANSACTION
-- ============================================================
-- START TRANSACTION;
-- INSERT INTO payments(invoice_id,amount,payment_method,reference_no)
-- VALUES (1,100,'UPI','DEMO100');
-- COMMIT;
-- ROLLBACK;
