"""
Database Manager and Query Layer
Provides structured SQL queries and data extraction for SQLite.
Author: Abhishek Sharma (Roll No: 2503201450007)
NorthStar Online Retail Pvt. Ltd.
"""

import os
import sqlite3
import pandas as pd
from typing import Optional, List

class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(base_dir, "data", "ecommerce_returns.db")
        else:
            self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Returns SQLite connection."""
        conn = sqlite3.connect(self.db_path)
        return conn

    def fetch_all_orders(self) -> pd.DataFrame:
        """Loads the full orders dataset from SQLite."""
        query = "SELECT * FROM orders ORDER BY order_date ASC;"
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
        return df

    def execute_custom_query(self, query: str, params: tuple = ()) -> pd.DataFrame:
        """Executes a custom query securely and returns DataFrame."""
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=params)
        return df

    def get_distinct_categories(self) -> List[str]:
        """Returns unique categories."""
        query = "SELECT DISTINCT product_category FROM orders ORDER BY product_category ASC;"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    def get_distinct_payment_methods(self) -> List[str]:
        """Returns unique payment methods."""
        query = "SELECT DISTINCT payment_method FROM orders ORDER BY payment_method ASC;"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    def get_distinct_regions(self) -> List[str]:
        """Returns unique delivery regions."""
        query = "SELECT DISTINCT delivery_region FROM orders ORDER BY delivery_region ASC;"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]
