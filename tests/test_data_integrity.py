"""
Test Suite: Data Integrity & Schema Validation (SC-01)
Validates dataset completeness, types, constraints, and business rules.
Project ID: P088
Author: Abhishek Sharma (University Roll No: 2500320140007)
Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01
Project Mentor: Dinesh Sereno
NorthStar Online Retail Pvt. Ltd.
"""

import os
import pytest
import pandas as pd
from data.generate_dataset import generate_ecommerce_data

@pytest.fixture(scope="module")
def dataset():
    """Generates a dataset instance for testing."""
    df = generate_ecommerce_data(num_records=1500)
    return df

def test_record_count(dataset):
    """SC-01 Target: At least 1,000 records."""
    assert len(dataset) >= 1000
    assert len(dataset) == 1500

def test_required_columns_present(dataset):
    """Verifies that all columns required for OQ-01 through OQ-10 exist."""
    required_cols = [
        'order_id', 'customer_id', 'order_date', 'product_category',
        'product_id', 'product_name', 'quantity', 'unit_price', 'order_value',
        'payment_method', 'delivery_city', 'delivery_region',
        'expected_delivery_date', 'actual_delivery_date', 'delivery_delay_days',
        'delivery_status', 'return_status', 'return_date', 'return_reason',
        'refund_amount', 'refund_status'
    ]
    for col in required_cols:
        assert col in dataset.columns, f"Missing required column: {col}"

def test_order_id_uniqueness(dataset):
    """Ensures each order ID is unique with no duplicates or nulls."""
    assert dataset['order_id'].isnull().sum() == 0
    assert dataset['order_id'].nunique() == len(dataset)

def test_return_status_validity(dataset):
    """Ensures return_status contains only controlled valid values."""
    valid_statuses = {'Returned', 'Not Returned'}
    unique_statuses = set(dataset['return_status'].unique())
    assert unique_statuses.issubset(valid_statuses)

def test_refund_amount_consistency(dataset):
    """
    Business Rule:
    - If return_status == 'Returned', refund_amount > 0
    - If return_status == 'Not Returned', refund_amount == 0
    """
    returned = dataset[dataset['return_status'] == 'Returned']
    not_returned = dataset[dataset['return_status'] == 'Not Returned']

    assert (returned['refund_amount'] > 0).all(), "Returned orders must have refund_amount > 0"
    assert (not_returned['refund_amount'] == 0).all(), "Non-returned orders must have refund_amount == 0"

def test_delivery_delay_calculation(dataset):
    """
    Delivery delay = actual_delivery_date - expected_delivery_date (calendar days).
    """
    actual_dates = pd.to_datetime(dataset['actual_delivery_date'])
    expected_dates = pd.to_datetime(dataset['expected_delivery_date'])
    calculated_delays = (actual_dates - expected_dates).dt.days

    assert (dataset['delivery_delay_days'] == calculated_delays).all(), "delivery_delay_days mismatch"

def test_order_value_consistency(dataset):
    """Order value must equal quantity * unit_price."""
    expected_value = dataset['quantity'] * dataset['unit_price']
    assert (dataset['order_value'] == expected_value).all(), "order_value must equal quantity * unit_price"
