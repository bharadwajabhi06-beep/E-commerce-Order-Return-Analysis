# E-Commerce Order Return Analysis
## Academic Project Report

### 1. Abstract
This project analyzes e-commerce order data to identify patterns associated with product returns. Python is used for data preparation, exploratory analysis and a demonstration machine-learning model. SQL is used to store and query order records, while Power BI is used to present interactive business dashboards. The objective is to help stakeholders understand return rates by product category, payment method, delivery time and return reason.

### 2. Problem Statement
Product returns can affect customer experience, inventory planning and business revenue. Without structured analysis, a retailer may struggle to identify categories or order characteristics associated with higher return rates. This project provides a data-driven view of return patterns and demonstrates how order-level attributes can be used to estimate return probability.

### 3. Objectives
- Clean and prepare order-level data.
- Calculate overall and segment-wise return rates.
- Analyze return reasons, categories, payment methods and delivery times.
- Estimate returned-order value as a financial-impact indicator.
- Build and evaluate a Random Forest classification model.
- Present findings in a Power BI dashboard.

### 4. Scope
The project is an academic prototype using a synthetic dataset. It demonstrates an end-to-end analytics workflow. It does not connect to a live e-commerce platform and does not make automated refund or customer decisions.

### 5. Tools and Technologies
Python, Pandas, NumPy, Matplotlib, Seaborn, scikit-learn, SQLite SQL and Microsoft Power BI.

### 6. Dataset Description
The demonstration dataset contains 2,500 generated order records. Fields include Order_ID, Customer_ID, Order_Date, Product_Category, Product_Price, Quantity, Discount_Percent, Payment_Method, Shipping_Type, Delivery_Days, Customer_Rating, Is_Returned and Return_Reason. The dataset is synthetic and should not be represented as real company data.

### 7. Methodology
1. Generate/read CSV data.
2. Remove duplicate order identifiers and handle missing numeric and categorical values.
3. Create derived fields such as Order_Month, Order_Value and Returned_Value.
4. Load records into SQLite.
5. Run SQL aggregations and exploratory data analysis.
6. Train a Random Forest classifier using an 80:20 train-test split.
7. Evaluate using precision, recall, F1-score, confusion matrix and ROC-AUC.
8. Import prepared CSV data into Power BI and create KPI cards, charts and slicers.

### 8. Machine Learning Design
Target: Is_Returned (1 = returned, 0 = not returned).
Features: Product_Category, Product_Price, Quantity, Discount_Percent, Payment_Method, Shipping_Type, Delivery_Days and Customer_Rating.
Categorical variables are one-hot encoded; numeric variables are imputed and scaled. Random Forest is trained with class balancing. Return_Reason is excluded because it is only known after the return event; Is_Returned is the target and is never used as an input feature.

### 9. Evaluation
The pipeline writes the actual test-set classification report, confusion matrix and ROC-AUC to `outputs/model_metrics.txt`. Insert those measured values in the final submitted report after running the project. Do not invent model accuracy or claim that a particular score was achieved before execution.

### 10. Business Metrics
Return Rate = Returned Orders / Total Orders.
Returned Order Value = sum of Order_Value for returned orders.
Returned Order Value is an indicator of order value associated with returns, not a complete measure of net financial loss.

### 11. Expected Outcomes
The dashboard allows users to compare return rates across product categories, months, payment methods and delivery-time groups. The model provides a probability estimate for demonstration and supports discussion of potential risk factors. Findings must be interpreted from the generated output rather than assumed in advance.

### 12. Limitations
- Synthetic data may not reflect actual customer behaviour.
- The model may not generalize to real business data.
- Customer rating and delivery days must be available at the intended prediction time.
- Refund costs, reverse logistics, restocking and resale recovery are not included.
- Model probabilities are not guarantees.

### 13. Future Enhancements
Use a verified real dataset, add product-level and seller-level data, incorporate shipping and refund costs, compare gradient boosting models, monitor model drift, and deploy a secure API with role-based access.

### 14. Conclusion
The project demonstrates an end-to-end e-commerce returns analytics solution using Python, SQL, machine learning and Power BI. It converts order-level data into measurable return trends and an interactive reporting experience. The prototype can be extended with verified business data and operational cost information.
