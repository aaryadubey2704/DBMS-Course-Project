# DBMS Course Project — Project 68

## Tailoring and Boutique Order Management System

This package is a ready-to-run project starter prepared around the faculty requirements for Project 68.

### Main components
- MySQL database and sample data
- SQL queries, joins, aggregates, subqueries and views
- Python Tkinter front-end connected to MySQL
- ER diagram
- Data dictionary and normalization notes
- Presentation PPTX
- Project report PDF
- Test cases
- GitHub-ready folder structure

## Important
Before presentation, replace the placeholders for the two other group members in:
- `README.md`
- `Presentation/Project_68_Presentation.pptx`
- `Project-Report/Project_68_Report.pdf` (the report currently marks them as placeholders)

### Requirements
- MySQL 8.x (XAMPP MySQL is fine)
- Python 3.10+
- `mysql-connector-python`

### Quick setup
1. Start MySQL in XAMPP.
2. Open MySQL/phpMyAdmin and run `Database/tailoring_boutique.sql`.
3. Open `UI/config.py` and set MySQL username/password if needed.
4. In a terminal inside `UI`:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
5. Use the Customers tab to demonstrate INSERT, DELETE and VIEW.
6. Use the other tabs for measurements, orders, fabric issue, tailor assignment, trials, alterations, billing/payment and reports.

## GitHub structure

```text
DBMS-Course-Project/
├── Presentation/
├── Project-Report/
├── Database/
├── UI/
├── ER_Diagram/
└── Screenshots/
```

## Member 1
Aarya Dubey — 25WU0101003

## Member 2
[ADD NAME] — [ADD ROLL NUMBER]

## Member 3
[ADD NAME] — [ADD ROLL NUMBER]

### One-line description
A relational DBMS that manages customers, measurements, boutique orders, fabrics, tailors, trials, alterations, invoices and payments.
