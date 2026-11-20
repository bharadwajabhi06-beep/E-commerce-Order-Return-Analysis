"""
SQLite Database Initializer and Manager for NorthStar Online Retail Pvt. Ltd.
Handles table creation, synthetic data ingestion, and direct SQL execution.
"""

import os
import sqlite3
import pandas as pd

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ecommerce_returns.db")
DEFAULT_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders_returns.csv")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    product_category TEXT NOT NULL,
    product_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    order_value REAL NOT NULL,
    payment_method TEXT NOT NULL,
    delivery_city TEXT NOT NULL,
    delivery_region TEXT NOT NULL,
    expected_delivery_date TEXT NOT NULL,
    actual_delivery_date TEXT NOT NULL,
    delivery_delay_days INTEGER NOT NULL,
    delivery_status TEXT NOT NULL,
    return_status TEXT NOT NULL,
    return_date TEXT,
    return_reason TEXT,
    refund_amount REAL NOT NULL,
    refund_status TEXT
);
"""

CREATE_INDEXES_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date);",
    "CREATE INDEX IF NOT EXISTS idx_return_status ON orders(return_status);",
    "CREATE INDEX IF NOT EXISTS idx_product_category ON orders(product_category);",
    "CREATE INDEX IF NOT EXISTS idx_payment_method ON orders(payment_method);",
    "CREATE INDEX IF NOT EXISTS idx_product_id ON orders(product_id);"
]

def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Returns a SQLite connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_database(db_path: str = DEFAULT_DB_PATH, csv_path: str = DEFAULT_CSV_PATH) -> int:
    """
    Initializes the SQLite database from the CSV dataset.
    Creates schema, indexes, and loads data.
    """
    if not os.path.exists(csv_path):
        from .generate_dataset import save_and_initialize_data
        save_and_initialize_data(os.path.dirname(csv_path))

    df = pd.read_csv(csv_path)

    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute(CREATE_TABLE_SQL)

    for idx_sql in CREATE_INDEXES_SQL:
        cursor.execute(idx_sql)

    # Insert data
    df.to_sql('orders', conn, if_exists='append', index=False)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM orders;")
    count = cursor.fetchone()[0]
    conn.close()

    print(f"Database initialized at {db_path} with {count} records.")
    return count

def query_dataframe(query: str, params: tuple = (), db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Executes a SQL query and returns a pandas DataFrame."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

if __name__ == '__main__':
    init_database()
