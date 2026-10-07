# Testing Plan

| Test ID | Test | Expected Result |
|---|---|---|
| T01 | Insert a customer with unique phone | Customer is inserted |
| T02 | Insert duplicate customer code | Rejected by UNIQUE constraint |
| T03 | Create order with delivery date before order date | Rejected |
| T04 | Issue more fabric than available | Rejected by trigger |
| T05 | Schedule two trials for same tailor at same date/time | Rejected |
| T06 | Pay more than invoice balance | Rejected by trigger |
| T07 | Delete customer with measurement profile | Related measurement is removed by cascade |
| T08 | View pending orders | Only non-delivered/non-cancelled orders appear |
| T09 | Run revenue report | Aggregate invoice/payment values are displayed |
| T10 | Add alteration and view alteration report | Alteration appears in report |
