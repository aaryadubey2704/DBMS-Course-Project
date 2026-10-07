# Relational Schema & Normalization to 3NF

## Functional dependency examples

- `customer_id -> customer_code, full_name, phone, email, address`
- `measurement_id -> customer_id, bust_cm, waist_cm, hip_cm, shoulder_cm, sleeve_cm, length_cm`
- `order_id -> order_no, customer_id, order_date, delivery_date, status, special_instructions`
- `order_item_id -> order_id, garment_type_id, design_id, fabric_id, quantity, fabric_required_meters, unit_price`
- `tailor_id -> tailor_code, tailor_name, specialization, phone, status`
- `invoice_id -> invoice_no, order_id, invoice_date, subtotal, alteration_total, total_amount`
- `payment_id -> invoice_id, payment_date, amount, payment_method, reference_no`

## 1NF
All attributes contain atomic values. Repeating groups such as multiple garments or multiple payments are separated into `order_items` and `payments`.

## 2NF
Tables with composite-style business relationships are separated so that non-key attributes depend on the whole identifying key. For example, order information is stored in `orders` while line-level garment information is stored in `order_items`.

## 3NF
Non-key attributes do not depend transitively on another non-key attribute. Customer information is stored only in `customers`, tailor information only in `tailors`, fabric information only in `fabrics`, and garment/design information in their own tables.

This decomposition reduces update, insertion and deletion anomalies.
