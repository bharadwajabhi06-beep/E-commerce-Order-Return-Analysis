# E-Commerce Order Return Analysis
**Decision Support Analytics System for NorthStar Online Retail Pvt. Ltd.**

---

### Project Identification
* **Project ID:** P088
* **Title:** E-Commerce Order Return Analysis
* **Domain:** E-Commerce / Data Analytics
* **Student:** Abhishek Sharma
* **University Roll No:** 2500320140007
* **Batch ID:** ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01
* **Programme:** MCA 2nd Year – Data Analytics
* **Institution:** ABES Engineering College, Ghaziabad
* **Project Mentor:** Dinesh Sereno
* **Assumed Retailer:** NorthStar Online Retail Pvt. Ltd. (Noida, Uttar Pradesh; ~500 employees)

---

## 1. Project Overview & Architecture
This project is an end-to-end data analytics and decision-support solution designed to measure, analyze, and diagnose e-commerce product returns. By integrating a clean SQLite database backend with automated statistical calculation routines and an interactive Streamlit + Plotly user interface, it provides operations managers, customer support leads, and category planners with actionable visibility into return velocity, root reasons, courier delay impacts, and financial refund leakage.

```
┌────────────────────────────────────────────────────────┐
│                   Streamlit Web UI                     │
│  (KPI Cards, Slicing Panel, Interactive Plotly Visuals) │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│               Analytical Services Layer                │
│    (Core KPIs, Trend Grouping, Delay Distributions)    │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                  SQLite 3 Data Layer                   │
│   (orders table, indexes on date, category, status)    │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│            Synthetic Dataset Generator                 │
│      (3,000 Order Records, Seeded, Reproducible)       │
└────────────────────────────────────────────────────────┘
```

---

## 2. Operational Questions (OQ) Traceability Matrix

| OQ ID | Operational Question | Primary Dataset Fields | Analytics Implementation | UI Location |
|---|---|---|---|---|
| **OQ-01** | How many total orders are present in the selected period? | `order_id`, `order_date` | `COUNT(DISTINCT order_id)` after date filter | Top KPI Card 1 |
| **OQ-02** | How many orders were returned, and what is the overall return rate? | `order_id`, `return_status` | `(Returned Orders / Eligible Orders) * 100` | Top KPI Cards 2 & 3 |
| **OQ-03** | How does the return rate change month by month? | `order_date`, `return_status` | Monthly group aggregation & return rate % | Tab 1: Dual-Axis Trend Chart |
| **OQ-04** | Which product categories have the highest number of returned orders? | `product_category`, `return_status` | Returned order volume grouped by category | Tab 2: Returned Volume Bar Chart |
| **OQ-05** | Which product categories have the highest return rate? | `product_category`, `return_status` | `(Category Returns / Category Total) * 100` | Tab 2: Category Rate Bar Chart |
| **OQ-06** | What are the most common reasons customers return products? | `return_reason`, `return_status` | Standardized reason count & % share | Tab 2: Donut Chart & Data Table |
| **OQ-07** | What is the total refund value associated with returned orders? | `refund_amount`, `return_status` | `SUM(refund_amount)` for returned orders | Top KPI Card 4 & Tab 1 Bar Chart |
| **OQ-08** | Which payment methods are associated with the largest number of returns? | `payment_method`, `return_status` | Return volume and return rate by payment type | Tab 3: Dual-Axis Payment Chart |
| **OQ-09** | Do delivery delays appear more frequently among returned orders? | `actual_delivery_date`, `expected_delivery_date` | `actual_date - expected_date` in days; boxplot | Tab 3: Fulfillment Delay Comparison |
| **OQ-10** | Which products show unusually high return rates and should be reviewed? | `product_id`, `product_name`, `return_status` | SKU-level rate with minimum order filter | Tab 4: Product Risk Matrix |

---

## 3. Directory Structure

```
ecommerce_return_analysis/
│
├── app.py                      # Main Streamlit Dashboard Application
├── requirements.txt            # Python dependencies
├── README.md                   # Complete Academic & Technical Documentation
│
├── data/
│   ├── generate_dataset.py     # Reproducible synthetic dataset generator (3,000 records)
│   ├── database.py             # SQLite database initializer, schema definition & query API
│   ├── orders_returns.csv      # Generated CSV dataset
│   └── ecommerce_returns.db    # SQLite 3 database file with pre-built indexes
│
├── src/
│   ├── __init__.py
│   ├── analytics.py            # Business logic answering OQ-01 through OQ-10
│   ├── charts.py               # 7+ Interactive Plotly visualizations
│   └── db_manager.py           # SQLite connection layer and query abstraction
│
└── tests/
    ├── __init__.py
    ├── test_data_integrity.py  # SC-01 Schema, null-check, and constraint tests
    ├── test_kpi_calculations.py # SC-02 & SC-03 Hand-calculated benchmark verification
    └── test_delivery_delays.py # OQ-09 & OQ-10 Delay and product threshold tests
```

---

## 4. Setup and Local Execution Guide

### Prerequisites
* Python 3.10+ (tested and verified on Python 3.14)
* pip package manager

### 1. Installation
Install all required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Dataset Generation and Database Initialization
Generate the 3,000 synthetic order records and initialize the SQLite database:
```bash
python data/generate_dataset.py
python data/database.py
```

### 3. Running Automated Test Suite
Run the 15-test pytest verification suite to validate calculations against hand-checked samples:
```bash
pytest tests/ -v
```

### 4. Launching the Interactive Streamlit Dashboard
Start the local web application:
```bash
streamlit run app.py
```
Open your browser and navigate to: **`http://localhost:8501`**

---

## 5. Key Analytical Insights for NorthStar Online Retail Pvt. Ltd.

1. **High-Return Categories:**
   * **Apparel & Clothing** and **Footwear** exhibit the highest return rates (~28%–32%), driven primarily by **Size/Fit Issues** and discrepancy with online imagery.
   * Recommendation: Implement interactive 3D sizing charts and customer fit recommendation widgets on product listing pages.

2. **Delivery Delay Correlation:**
   * Orders delayed by 3 or more days beyond promised SLA experience a return propensity greater than 40%.
   * Late delivery is a top stated return reason for delayed orders.
   * Recommendation: Prioritize dispatch velocity and establish strict SLA tracking for courier partners in the North regional hub (Noida/Delhi).

3. **Payment Method Dynamics:**
   * **Cash on Delivery (COD)** orders show a slightly higher return and cancellation rate compared to prepaid digital payments (UPI, Credit/Debit card).
   * Recommendation: Introduce instant discount incentives for prepaid UPI checkouts.

4. **Product Defect Thresholds (OQ-10):**
   * Using the minimum order threshold filter (default: 15 orders), specific SKUs like high-end noise-cancelling headphones and certain denim variants emerge as quality outliers requiring immediate vendor inspection.

---

## 6. Academic Deliverables & Compliance Checklist
- [x] **SC-01:** Structural completeness (3,000 valid records, no null order IDs, strict enum status).
- [x] **SC-02:** Calculation accuracy verified (100% match against hand-calculated 10-order benchmark).
- [x] **SC-03:** All 10 Operational Questions answerable and mapped.
- [x] **SC-04:** Streamlit UI with >6 interactive Plotly visualisations and dynamic filters.
- [x] **SC-05:** Automated pytest suite with 100% pass rate (15/15 passed).
- [x] **SC-06:** Evaluator-friendly UI with raw data explorer and interactive SQL console.
