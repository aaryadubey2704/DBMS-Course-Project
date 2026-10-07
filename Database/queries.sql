USE tailoring_boutique;

-- A. CUSTOMER HISTORY
SELECT c.full_name, o.order_no, o.status, i.total_amount
FROM customers c
JOIN orders o ON o.customer_id=c.customer_id
LEFT JOIN invoices i ON i.order_id=o.order_id
ORDER BY c.full_name;

-- B. ORDERS DUE SOON
SELECT * FROM v_delivery_due ORDER BY delivery_date;

-- C. TOP ORDER VALUES
SELECT o.order_no, c.full_name, i.total_amount
FROM invoices i
JOIN orders o ON o.order_id=i.order_id
JOIN customers c ON c.customer_id=o.customer_id
ORDER BY i.total_amount DESC;

-- D. FABRIC STOCK ALERT
SELECT f.fabric_name, fs.quantity_meters, fs.reorder_level
FROM fabrics f
JOIN fabric_stock fs ON fs.fabric_id=f.fabric_id
WHERE fs.quantity_meters <= fs.reorder_level;

-- E. ALTERATION COST
SELECT SUM(alteration_cost) AS total_alteration_cost
FROM alterations;

-- F. ACTIVE TAILORS
SELECT * FROM tailors WHERE status='ACTIVE';

-- G. TAILOR LOAD WITH LEFT JOIN
SELECT t.tailor_name,
       COUNT(ta.assignment_id) AS assigned_orders,
       SUM(CASE WHEN ta.assignment_status='COMPLETED' THEN 1 ELSE 0 END) AS completed
FROM tailors t
LEFT JOIN tailor_assignments ta ON ta.tailor_id=t.tailor_id
GROUP BY t.tailor_id, t.tailor_name;

-- H. SUBQUERY: MOST EXPENSIVE ORDER
SELECT order_no
FROM invoices i
JOIN orders o ON o.order_id=i.order_id
WHERE i.total_amount=(SELECT MAX(total_amount) FROM invoices);

-- I. PAYMENT COLLECTION
SELECT i.invoice_no, i.total_amount,
       COALESCE(SUM(p.amount),0) paid,
       i.total_amount-COALESCE(SUM(p.amount),0) balance
FROM invoices i
LEFT JOIN payments p ON p.invoice_id=i.invoice_id
GROUP BY i.invoice_id, i.invoice_no, i.total_amount;

-- J. VIEW REPORTS
SELECT * FROM v_pending_orders;
SELECT * FROM v_tailor_workload;
SELECT * FROM v_customer_history;
SELECT * FROM v_revenue;
