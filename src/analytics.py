"""
Core Analytics and Business Metric Calculations
Supports Operational Questions OQ-01 through OQ-10
Project ID: P088
Author: Abhishek Sharma (University Roll No: 2500320140007)
Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01
Project Mentor: Dinesh Sereno
NorthStar Online Retail Pvt. Ltd.
"""

from typing import Dict, Any, Optional, Tuple, List
import pandas as pd
import numpy as np

def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes dates and computes auxiliary analytical columns.
    """
    df = df.copy()
    # Parse dates safely
    for col in ['order_date', 'expected_delivery_date', 'actual_delivery_date', 'return_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Year-Month string for time-series grouping
    if 'order_date' in df.columns:
        df['year_month'] = df['order_date'].dt.strftime('%Y-%m')
        df['month_name'] = df['order_date'].dt.strftime('%b %Y')

    # Ensure delivery delay is integer / float
    if 'actual_delivery_date' in df.columns and 'expected_delivery_date' in df.columns:
        calculated_delay = (df['actual_delivery_date'] - df['expected_delivery_date']).dt.days
        df['delivery_delay_days'] = df['delivery_delay_days'].fillna(calculated_delay)

    # Delay classification
    def classify_delay(days):
        if pd.isna(days):
            return 'Unknown'
        if days < 0:
            return 'Early Delivery'
        elif days == 0:
            return 'On Time'
        elif 1 <= days <= 2:
            return 'Slight Delay (1-2 days)'
        else:
            return 'Significant Delay (3+ days)'

    df['delay_category'] = df['delivery_delay_days'].apply(classify_delay)
    return df

def apply_filters(
    df: pd.DataFrame,
    start_date: Optional[pd.Timestamp] = None,
    end_date: Optional[pd.Timestamp] = None,
    categories: Optional[List[str]] = None,
    payment_methods: Optional[List[str]] = None,
    regions: Optional[List[str]] = None,
    return_status: Optional[str] = None
) -> pd.DataFrame:
    """
    Applies interactive UI filters to the DataFrame.
    """
    filtered = df.copy()

    if start_date is not None and 'order_date' in filtered.columns:
        filtered = filtered[filtered['order_date'] >= pd.to_datetime(start_date)]

    if end_date is not None and 'order_date' in filtered.columns:
        filtered = filtered[filtered['order_date'] <= pd.to_datetime(end_date)]

    if categories and len(categories) > 0:
        filtered = filtered[filtered['product_category'].isin(categories)]

    if payment_methods and len(payment_methods) > 0:
        filtered = filtered[filtered['payment_method'].isin(payment_methods)]

    if regions and len(regions) > 0:
        filtered = filtered[filtered['delivery_region'].isin(regions)]

    if return_status and return_status != 'All':
        filtered = filtered[filtered['return_status'] == return_status]

    return filtered

def calculate_core_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Answers:
    - OQ-01: How many total orders are present in the selected period?
    - OQ-02: How many orders were returned, and what is the overall return rate?
    - OQ-07: What is the total refund value associated with returned orders?
    """
    if df.empty:
        return {
            'total_orders': 0,
            'returned_orders': 0,
            'non_returned_orders': 0,
            'return_rate_pct': 0.0,
            'total_revenue': 0.0,
            'total_refund': 0.0,
            'net_revenue': 0.0,
            'avg_order_value': 0.0,
            'avg_delivery_delay_returned': 0.0,
            'avg_delivery_delay_non_returned': 0.0,
        }

    total_orders = int(df['order_id'].nunique())
    returned_df = df[df['return_status'] == 'Returned']
    non_returned_df = df[df['return_status'] != 'Returned']

    returned_orders = int(returned_df['order_id'].nunique())
    non_returned_orders = total_orders - returned_orders

    return_rate_pct = round((returned_orders / total_orders * 100), 2) if total_orders > 0 else 0.0

    total_revenue = float(df['order_value'].sum())
    total_refund = float(returned_df['refund_amount'].sum())
    net_revenue = total_revenue - total_refund
    avg_order_value = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0

    avg_delay_returned = round(float(returned_df['delivery_delay_days'].mean()), 2) if not returned_df.empty else 0.0
    avg_delay_non_returned = round(float(non_returned_df['delivery_delay_days'].mean()), 2) if not non_returned_df.empty else 0.0

    return {
        'total_orders': total_orders,
        'returned_orders': returned_orders,
        'non_returned_orders': non_returned_orders,
        'return_rate_pct': return_rate_pct,
        'total_revenue': total_revenue,
        'total_refund': total_refund,
        'net_revenue': net_revenue,
        'avg_order_value': avg_order_value,
        'avg_delivery_delay_returned': avg_delay_returned,
        'avg_delivery_delay_non_returned': avg_delay_non_returned,
    }

def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Answers OQ-03: How does the return rate change month by month?
    """
    if df.empty:
        return pd.DataFrame(columns=['year_month', 'month_name', 'total_orders', 'returned_orders', 'return_rate_pct', 'total_refund'])

    grouped = df.groupby('year_month').agg(
        total_orders=('order_id', 'nunique'),
        returned_orders=('return_status', lambda s: (s == 'Returned').sum()),
        total_revenue=('order_value', 'sum'),
        total_refund=('refund_amount', 'sum'),
        month_name=('month_name', 'first')
    ).reset_index()

    grouped['return_rate_pct'] = (grouped['returned_orders'] / grouped['total_orders'] * 100).round(2)
    grouped = grouped.sort_values('year_month')
    return grouped

def get_category_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Answers:
    - OQ-04: Which product categories have the highest number of returned orders?
    - OQ-05: Which product categories have the highest return rate?
    """
    if df.empty:
        return pd.DataFrame(columns=['product_category', 'total_orders', 'returned_orders', 'return_rate_pct', 'total_refund'])

    cat_df = df.groupby('product_category').agg(
        total_orders=('order_id', 'nunique'),
        returned_orders=('return_status', lambda s: (s == 'Returned').sum()),
        total_revenue=('order_value', 'sum'),
        total_refund=('refund_amount', 'sum')
    ).reset_index()

    cat_df['return_rate_pct'] = (cat_df['returned_orders'] / cat_df['total_orders'] * 100).round(2)
    cat_df['revenue_impact_pct'] = (cat_df['total_refund'] / cat_df['total_revenue'] * 100).round(2)
    cat_df = cat_df.sort_values('returned_orders', ascending=False)
    return cat_df

def get_return_reasons_breakdown(df: pd.DataFrame, category: Optional[str] = None) -> pd.DataFrame:
    """
    Answers OQ-06: What are the most common reasons customers return products?
    """
    returned_df = df[df['return_status'] == 'Returned'].copy()

    if category and category != 'All':
        returned_df = returned_df[returned_df['product_category'] == category]

    if returned_df.empty:
        return pd.DataFrame(columns=['return_reason', 'count', 'percentage_of_returns', 'refund_amount'])

    reasons_df = returned_df.groupby('return_reason').agg(
        count=('order_id', 'nunique'),
        refund_amount=('refund_amount', 'sum')
    ).reset_index()

    total_returns = returned_df['order_id'].nunique()
    reasons_df['percentage_of_returns'] = (reasons_df['count'] / total_returns * 100).round(2)
    reasons_df = reasons_df.sort_values('count', ascending=False)
    return reasons_df

def get_payment_method_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Answers OQ-08: Which payment methods are associated with the largest number of returned orders?
    """
    if df.empty:
        return pd.DataFrame(columns=['payment_method', 'total_orders', 'returned_orders', 'return_rate_pct', 'total_refund'])

    pm_df = df.groupby('payment_method').agg(
        total_orders=('order_id', 'nunique'),
        returned_orders=('return_status', lambda s: (s == 'Returned').sum()),
        total_refund=('refund_amount', 'sum')
    ).reset_index()

    pm_df['return_rate_pct'] = (pm_df['returned_orders'] / pm_df['total_orders'] * 100).round(2)
    pm_df = pm_df.sort_values('returned_orders', ascending=False)
    return pm_df

def get_delivery_delay_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Answers OQ-09: Do delivery delays appear more frequently among returned orders?
    """
    if df.empty:
        return {
            'avg_delay_returned': 0.0,
            'avg_delay_non_returned': 0.0,
            'median_delay_returned': 0.0,
            'median_delay_non_returned': 0.0,
            'delay_bracket_df': pd.DataFrame(),
            'correlation_insight': "No data available."
        }

    returned_df = df[df['return_status'] == 'Returned']
    non_returned_df = df[df['return_status'] != 'Returned']

    avg_ret = round(float(returned_df['delivery_delay_days'].mean()), 2) if not returned_df.empty else 0.0
    avg_non = round(float(non_returned_df['delivery_delay_days'].mean()), 2) if not non_returned_df.empty else 0.0
    med_ret = round(float(returned_df['delivery_delay_days'].median()), 2) if not returned_df.empty else 0.0
    med_non = round(float(non_returned_df['delivery_delay_days'].median()), 2) if not non_returned_df.empty else 0.0

    bracket_df = df.groupby('delay_category').agg(
        total_orders=('order_id', 'nunique'),
        returned_orders=('return_status', lambda s: (s == 'Returned').sum())
    ).reset_index()

    bracket_df['return_rate_pct'] = (bracket_df['returned_orders'] / bracket_df['total_orders'] * 100).round(2)

    # Order bracket logically
    bracket_order = ['Early Delivery', 'On Time', 'Slight Delay (1-2 days)', 'Significant Delay (3+ days)', 'Unknown']
    bracket_df['sort_order'] = bracket_df['delay_category'].map(lambda x: bracket_order.index(x) if x in bracket_order else 99)
    bracket_df = bracket_df.sort_values('sort_order').drop(columns=['sort_order'])

    return {
        'avg_delay_returned': avg_ret,
        'avg_delay_non_returned': avg_non,
        'median_delay_returned': med_ret,
        'median_delay_non_returned': med_non,
        'delay_bracket_df': bracket_df
    }

def get_product_level_analysis(df: pd.DataFrame, min_orders: int = 10) -> pd.DataFrame:
    """
    Answers OQ-10: Which products show unusually high return rates and should be reviewed?
    Applies minimum order threshold.
    """
    if df.empty:
        return pd.DataFrame(columns=[
            'product_id', 'product_name', 'product_category', 'total_orders',
            'returned_orders', 'return_rate_pct', 'unit_price', 'total_refund'
        ])

    prod_df = df.groupby(['product_id', 'product_name', 'product_category']).agg(
        total_orders=('order_id', 'nunique'),
        returned_orders=('return_status', lambda s: (s == 'Returned').sum()),
        unit_price=('unit_price', 'mean'),
        total_refund=('refund_amount', 'sum')
    ).reset_index()

    prod_df['unit_price'] = prod_df['unit_price'].round(2)
    prod_df['return_rate_pct'] = (prod_df['returned_orders'] / prod_df['total_orders'] * 100).round(2)

    # Filter by minimum orders threshold
    qualified = prod_df[prod_df['total_orders'] >= min_orders].copy()
    qualified = qualified.sort_values('return_rate_pct', ascending=False)
    return qualified

def get_region_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates returns and order performance by region and city.
    """
    if df.empty:
        return pd.DataFrame(columns=['delivery_region', 'total_orders', 'returned_orders', 'return_rate_pct', 'total_refund'])

    reg_df = df.groupby(['delivery_region', 'delivery_city']).agg(
        total_orders=('order_id', 'nunique'),
        returned_orders=('return_status', lambda s: (s == 'Returned').sum()),
        total_refund=('refund_amount', 'sum')
    ).reset_index()

    reg_df['return_rate_pct'] = (reg_df['returned_orders'] / reg_df['total_orders'] * 100).round(2)
    return reg_df.sort_values('returned_orders', ascending=False)
