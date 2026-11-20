-- SQLite schema. Python pipeline creates this table automatically.
CREATE TABLE IF NOT EXISTS orders (
    Order_ID TEXT PRIMARY KEY,
    Customer_ID TEXT,
    Order_Date TEXT,
    Product_Category TEXT,
    Product_Price REAL,
    Quantity INTEGER,
    Discount_Percent REAL,
    Payment_Method TEXT,
    Shipping_Type TEXT,
    Delivery_Days INTEGER,
    Customer_Rating INTEGER,
    Is_Returned INTEGER,
    Return_Reason TEXT,
    Order_Value REAL,
    Order_Month TEXT,
    Returned_Value REAL,
    Return_Flag TEXT
);
