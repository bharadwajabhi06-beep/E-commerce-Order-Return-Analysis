# Power BI Dashboard Build Guide

## Import
Import `outputs/powerbi_orders.csv` through Home > Get Data > Text/CSV. Rename the table `Orders`.

## Measures
Copy measures from `measures.dax` using Modeling > New measure.

## Page layout
Top row: 5 Card visuals (Total Orders, Returned Orders, Return Rate %, Gross Order Value, Returned Order Value).
Middle row: clustered bar chart (Product_Category vs Return Rate %), line chart (Order_Month vs Return Rate %).
Bottom row: donut chart (Return_Reason vs Returned Orders; visual filter Is_Returned = 1), bar chart (Payment_Method vs Return Rate %).
Add slicers for Order_Date, Product_Category and Shipping_Type.

## Formatting
- Use a consistent two- or three-colour theme.
- Format currency values as INR only if the dataset is understood as INR.
- Format Return Rate % as percentage.
- Sort month labels chronologically. If Power BI sorts text alphabetically, create a date column from Order_Month and sort by that date.
- Add a note: "Demonstration analysis using synthetic data."

## Suggested report pages
1. Executive Overview
2. Product & Return Reasons
3. Time and Delivery Analysis
4. Model Insights (use exported prediction CSV and metrics text)
