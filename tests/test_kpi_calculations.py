"""
Test Suite: KPI Calculation Accuracy (SC-02, SC-03, OBJ-02)
Uses hand-calculated synthetic sample to verify 100% calculation accuracy.
Author: Abhishek Sharma (Roll No: 2503201450007)
NorthStar Online Retail Pvt. Ltd.
"""

import pytest
import pandas as pd
from src.analytics import (
    calculate_core_kpis,
    get_monthly_trends,
    get_category_metrics,
    get_return_reasons_breakdown,
    get_payment_method_metrics,
    prepare_dataframe
)

@pytest.fixture
def sample_benchmark_df():
    """
    Fixed 10-row dataset with known, hand-verified numbers:
    - Total Orders: 10
    - Returned: 3 (ORD-01, ORD-03, ORD-07)
    - Not Returned: 7
    - Expected Return Rate: (3 / 10) * 100 = 30.00%
    - Total Order Value: 1000 + 2000 + 1500 + 800 + 1200 + 2500 + 3000 + 500 + 1400 + 1100 = 15000.00
    - Returned Values: ORD-01 (1000) + ORD-03 (1500) + ORD-07 (3000) = 5500.00
    - Expected Total Refund: 5500.00
    - Expected Net Revenue: 15000 - 5500 = 9500.00
    - Expected Avg Order Value: 1500.00
    """
    data = [
        {"order_id": "ORD-01", "order_date": "2025-01-10", "product_category": "Apparel & Clothing", "product_id": "P1", "product_name": "Shirt", "order_value": 1000.0, "return_status": "Returned", "return_reason": "Size/Fit Issue", "refund_amount": 1000.0, "payment_method": "UPI", "delivery_delay_days": 2, "expected_delivery_date": "2025-01-15", "actual_delivery_date": "2025-01-17"},
        {"order_id": "ORD-02", "order_date": "2025-01-12", "product_category": "Apparel & Clothing", "product_id": "P1", "product_name": "Shirt", "order_value": 2000.0, "return_status": "Not Returned", "return_reason": "Not Applicable", "refund_amount": 0.0, "payment_method": "UPI", "delivery_delay_days": 0, "expected_delivery_date": "2025-01-16", "actual_delivery_date": "2025-01-16"},
        {"order_id": "ORD-03", "order_date": "2025-01-15", "product_category": "Electronics & Gadgets", "product_id": "P2", "product_name": "Earbuds", "order_value": 1500.0, "return_status": "Returned", "return_reason": "Damaged / Defective Item", "refund_amount": 1500.0, "payment_method": "Credit Card", "delivery_delay_days": 3, "expected_delivery_date": "2025-01-20", "actual_delivery_date": "2025-01-23"},
        {"order_id": "ORD-04", "order_date": "2025-02-05", "product_category": "Electronics & Gadgets", "product_id": "P2", "product_name": "Earbuds", "order_value": 800.0, "return_status": "Not Returned", "return_reason": "Not Applicable", "refund_amount": 0.0, "payment_method": "Credit Card", "delivery_delay_days": -1, "expected_delivery_date": "2025-02-10", "actual_delivery_date": "2025-02-09"},
        {"order_id": "ORD-05", "order_date": "2025-02-10", "product_category": "Footwear", "product_id": "P3", "product_name": "Shoes", "order_value": 1200.0, "return_status": "Not Returned", "return_reason": "Not Applicable", "refund_amount": 0.0, "payment_method": "Debit Card", "delivery_delay_days": 0, "expected_delivery_date": "2025-02-15", "actual_delivery_date": "2025-02-15"},
        {"order_id": "ORD-06", "order_date": "2025-02-14", "product_category": "Footwear", "product_id": "P3", "product_name": "Shoes", "order_value": 2500.0, "return_status": "Not Returned", "return_reason": "Not Applicable", "refund_amount": 0.0, "payment_method": "Cash on Delivery (COD)", "delivery_delay_days": 1, "expected_delivery_date": "2025-02-18", "actual_delivery_date": "2025-02-19"},
        {"order_id": "ORD-07", "order_date": "2025-02-20", "product_category": "Apparel & Clothing", "product_id": "P1", "product_name": "Shirt", "order_value": 3000.0, "return_status": "Returned", "return_reason": "Size/Fit Issue", "refund_amount": 3000.0, "payment_method": "Cash on Delivery (COD)", "delivery_delay_days": 4, "expected_delivery_date": "2025-02-25", "actual_delivery_date": "2025-03-01"},
        {"order_id": "ORD-08", "order_date": "2025-03-02", "product_category": "Home & Kitchen", "product_id": "P4", "product_name": "Kettle", "order_value": 500.0, "return_status": "Not Returned", "return_reason": "Not Applicable", "refund_amount": 0.0, "payment_method": "UPI", "delivery_delay_days": 0, "expected_delivery_date": "2025-03-06", "actual_delivery_date": "2025-03-06"},
        {"order_id": "ORD-09", "order_date": "2025-03-10", "product_category": "Home & Kitchen", "product_id": "P4", "product_name": "Kettle", "order_value": 1400.0, "return_status": "Not Returned", "return_reason": "Not Applicable", "refund_amount": 0.0, "payment_method": "UPI", "delivery_delay_days": -2, "expected_delivery_date": "2025-03-15", "actual_delivery_date": "2025-03-13"},
        {"order_id": "ORD-10", "order_date": "2025-03-15", "product_category": "Books & Stationery", "product_id": "P5", "product_name": "Book", "order_value": 1100.0, "return_status": "Not Returned", "return_reason": "Not Applicable", "refund_amount": 0.0, "payment_method": "Net Banking", "delivery_delay_days": 0, "expected_delivery_date": "2025-03-20", "actual_delivery_date": "2025-03-20"}
    ]
    df = pd.DataFrame(data)
    return prepare_dataframe(df)

def test_hand_calculated_kpis(sample_benchmark_df):
    """
    SC-02: 100% match for hand-calculated sample dataset.
    """
    kpis = calculate_core_kpis(sample_benchmark_df)

    assert kpis['total_orders'] == 10
    assert kpis['returned_orders'] == 3
    assert kpis['non_returned_orders'] == 7
    assert kpis['return_rate_pct'] == 30.0
    assert kpis['total_revenue'] == 15000.0
    assert kpis['total_refund'] == 5500.0
    assert kpis['net_revenue'] == 9500.0
    assert kpis['avg_order_value'] == 1500.0

    # Delay for returned: ORD-01 (2), ORD-03 (3), ORD-07 (4) -> avg = 9 / 3 = 3.0
    assert kpis['avg_delivery_delay_returned'] == 3.0

def test_monthly_trends_calculation(sample_benchmark_df):
    """
    OQ-03: Monthly grouping correctness.
    Jan 2025: 3 orders, 2 returned (ORD-01, ORD-03) -> 66.67%
    Feb 2025: 4 orders, 1 returned (ORD-07) -> 25.00%
    Mar 2025: 3 orders, 0 returned -> 0.00%
    """
    trends = get_monthly_trends(sample_benchmark_df)
    assert len(trends) == 3

    jan = trends[trends['year_month'] == '2025-01'].iloc[0]
    assert jan['total_orders'] == 3
    assert jan['returned_orders'] == 2
    assert jan['return_rate_pct'] == 66.67

    feb = trends[trends['year_month'] == '2025-02'].iloc[0]
    assert feb['total_orders'] == 4
    assert feb['returned_orders'] == 1
    assert feb['return_rate_pct'] == 25.00

    mar = trends[trends['year_month'] == '2025-03'].iloc[0]
    assert mar['total_orders'] == 3
    assert mar['returned_orders'] == 0
    assert mar['return_rate_pct'] == 0.00

def test_category_metrics_calculation(sample_benchmark_df):
    """
    OQ-04 & OQ-05: Category metrics.
    Apparel: 3 orders, 2 returned -> 66.67%
    Electronics: 2 orders, 1 returned -> 50.00%
    Footwear: 2 orders, 0 returned -> 0.00%
    """
    cat_df = get_category_metrics(sample_benchmark_df)
    apparel = cat_df[cat_df['product_category'] == 'Apparel & Clothing'].iloc[0]
    assert apparel['total_orders'] == 3
    assert apparel['returned_orders'] == 2
    assert apparel['return_rate_pct'] == 66.67
    assert apparel['total_refund'] == 4000.0

def test_return_reasons_breakdown(sample_benchmark_df):
    """
    OQ-06: Reasons distribution among returns.
    Returned: 3 orders.
    Size/Fit Issue: 2 (66.67%)
    Damaged / Defective Item: 1 (33.33%)
    Sum of percentages must equal 100%.
    """
    reasons = get_return_reasons_breakdown(sample_benchmark_df)
    assert len(reasons) == 2
    assert reasons['count'].sum() == 3
    assert pytest.approx(reasons['percentage_of_returns'].sum(), 0.01) == 100.0

def test_payment_method_metrics(sample_benchmark_df):
    """
    OQ-08: Payment methods returns.
    """
    pm_df = get_payment_method_metrics(sample_benchmark_df)
    assert pm_df['returned_orders'].sum() == 3
