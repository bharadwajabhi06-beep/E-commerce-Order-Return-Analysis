# E-Commerce Order Return Analysis

## Project objective
Analyze e-commerce orders to understand return patterns, estimate the financial value of returned orders, and demonstrate a machine-learning model that estimates return probability from order attributes.

## Important data note
`data/ecommerce_orders.csv` is a **synthetic demonstration dataset** generated for this academic project. It is not real customer or company data. Replace it with an authorized real dataset if your institution requires real-world data.

## Technology
- Python: Pandas, NumPy, Matplotlib, Seaborn, scikit-learn
- SQL: SQLite
- Power BI: interactive reporting and DAX measures
- Machine Learning: Random Forest classifier

## Setup
1. Install Python 3.10 or newer.
2. Extract this project folder.
3. Open a terminal in the project folder.
4. Create a virtual environment (recommended):
   - Windows: `py -m venv .venv`
   - Activate: `.venv\\Scripts\\activate`
5. Install libraries: `pip install -r requirements.txt`
6. Run: `python run_project.py`

The pipeline creates:
- `outputs/cleaned_orders.csv`
- `outputs/powerbi_orders.csv`
- category, monthly and return-reason summaries
- EDA chart PNG files
- `ecommerce_returns.db`
- trained model at `models/return_model.joblib`
- model evaluation report and example predictions

## Power BI
1. Open Power BI Desktop.
2. Home > Get Data > Text/CSV.
3. Select `outputs/powerbi_orders.csv`.
4. Load the table and rename it `Orders`.
5. Create measures from `powerbi/measures.dax`.
6. Build visuals using the guide in `powerbi/dashboard_guide.md`.

## Suggested dashboard
- KPI cards: Total Orders, Returned Orders, Return Rate %, Gross Order Value, Returned Order Value.
- Bar chart: Return Rate % by Product_Category.
- Line chart: Return Rate % by Order_Month.
- Donut chart: Returned orders by Return_Reason (filter Is_Returned = 1).
- Bar chart: Return Rate % by Payment_Method.
- Slicers: Order_Date, Product_Category, Payment_Method, Shipping_Type.

## Modeling note
The model excludes `Is_Returned` and `Return_Reason` from input features. Return reason is only known after a return, so using it to predict a return would cause target leakage. The model is a classroom demonstration, not a production decision system. Evaluate it on representative real data before operational use.

## Definitions
Return Rate = Returned Orders / Total Orders.
Returned Order Value = sum of Order_Value for rows where Is_Returned = 1.
This is a simple returned-order value indicator, not audited accounting loss: refunds, restocking, shipping, resale and recovery costs are not modeled.
