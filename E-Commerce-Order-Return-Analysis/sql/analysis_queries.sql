-- 1. Overall business KPIs
SELECT COUNT(*) AS total_orders,
       SUM(Is_Returned) AS returned_orders,
       ROUND(100.0 * SUM(Is_Returned) / COUNT(*), 2) AS return_rate_pct,
       ROUND(SUM(Order_Value), 2) AS gross_order_value,
       ROUND(SUM(Returned_Value), 2) AS returned_order_value
FROM orders;

-- 2. Category-wise return analysis
SELECT Product_Category, COUNT(*) AS total_orders,
       SUM(Is_Returned) AS returned_orders,
       ROUND(100.0 * SUM(Is_Returned)/COUNT(*), 2) AS return_rate_pct
FROM orders GROUP BY Product_Category ORDER BY return_rate_pct DESC;

-- 3. Return reasons
SELECT Return_Reason, COUNT(*) AS return_count
FROM orders WHERE Is_Returned = 1
GROUP BY Return_Reason ORDER BY return_count DESC;

-- 4. Monthly trend
SELECT Order_Month, COUNT(*) AS total_orders, SUM(Is_Returned) AS returned_orders,
       ROUND(100.0 * SUM(Is_Returned)/COUNT(*), 2) AS return_rate_pct
FROM orders GROUP BY Order_Month ORDER BY Order_Month;

-- 5. Payment method comparison
SELECT Payment_Method, COUNT(*) AS total_orders, SUM(Is_Returned) AS returned_orders,
       ROUND(100.0 * SUM(Is_Returned)/COUNT(*), 2) AS return_rate_pct
FROM orders GROUP BY Payment_Method ORDER BY return_rate_pct DESC;

-- 6. Delivery time and returns
SELECT CASE WHEN Delivery_Days <= 3 THEN '1-3 days'
            WHEN Delivery_Days <= 6 THEN '4-6 days'
            ELSE '7+ days' END AS delivery_bucket,
       COUNT(*) AS total_orders, SUM(Is_Returned) AS returned_orders,
       ROUND(100.0 * SUM(Is_Returned)/COUNT(*), 2) AS return_rate_pct
FROM orders GROUP BY delivery_bucket ORDER BY delivery_bucket;

-- 7. High-value returned orders
SELECT Order_ID, Product_Category, Order_Value, Return_Reason
FROM orders WHERE Is_Returned = 1
ORDER BY Order_Value DESC LIMIT 20;
