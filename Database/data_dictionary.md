# Data Dictionary — Project 68

| Table | Primary Key | Important Foreign Keys | Purpose |
|---|---|---|---|
| customers | customer_id | — | Stores customer details |
| measurement_profiles | measurement_id | customer_id | Stores one current measurement profile per customer |
| garment_types | garment_type_id | — | Stores garment categories |
| designs | design_id | garment_type_id | Stores available designs |
| fabrics | fabric_id | — | Stores fabric catalogue |
| fabric_stock | stock_id | fabric_id | Tracks available fabric quantity |
| orders | order_id | customer_id | Stores boutique orders |
| order_items | order_item_id | order_id, garment_type_id, design_id, fabric_id | Stores garments in each order |
| fabric_issues | issue_id | order_item_id, fabric_id | Records fabric issued to an order |
| tailors | tailor_id | — | Stores tailor information |
| tailor_assignments | assignment_id | order_id, tailor_id | Assigns tailors to orders |
| trials | trial_id | order_id, tailor_id | Schedules fitting trials |
| alterations | alteration_id | order_id, trial_id | Tracks alteration requests |
| invoices | invoice_id | order_id | Stores billing details |
| payments | payment_id | invoice_id | Stores payment transactions |

## Constraints
- Primary keys uniquely identify rows.
- Foreign keys maintain referential integrity.
- UNIQUE constraints protect customer codes, phone numbers, order numbers, invoice numbers and other business identifiers.
- NOT NULL is used for mandatory fields.
- CHECK constraints enforce positive measurements, prices, quantities and dates.
- DEFAULT values simplify common status/date fields.
- A trigger prevents fabric issue from exceeding stock.
- A trigger prevents total payments from exceeding an invoice.
- A unique `(tailor_id, trial_datetime)` constraint prevents exact trial-slot conflicts.
