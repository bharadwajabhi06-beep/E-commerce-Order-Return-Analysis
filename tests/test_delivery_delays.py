"""
Test Suite: Delivery Delays & Product Thresholds (OQ-09, OQ-10)
Project ID: P088
Author: Abhishek Sharma (University Roll No: 2500320140007)
Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01
Project Mentor: Dinesh Sereno
NorthStar Online Retail Pvt. Ltd.
"""

import pytest
import pandas as pd
from src.analytics import (
    get_delivery_delay_analysis,
    get_product_level_analysis,
    apply_filters,
    prepare_dataframe
)
from data.generate_dataset import generate_ecommerce_data

@pytest.fixture(scope="module")
def prepared_dataset():
    df = generate_ecommerce_data(num_records=1200)
    return prepare_dataframe(df)

def test_delivery_delay_analysis(prepared_dataset):
    """
    OQ-09: Validates delay analysis output structure and comparisons.
    """
    delay_stats = get_delivery_delay_analysis(prepared_dataset)
    assert 'avg_delay_returned' in delay_stats
    assert 'avg_delay_non_returned' in delay_stats
    assert 'delay_bracket_df' in delay_stats

    bracket_df = delay_stats['delay_bracket_df']
    assert not bracket_df.empty
    assert 'delay_category' in bracket_df.columns
    assert 'return_rate_pct' in bracket_df.columns

def test_product_level_threshold(prepared_dataset):
    """
    OQ-10: Validates that minimum-order threshold is enforced so small sample
    products do not skew return rates.
    """
    min_threshold = 15
    prod_df = get_product_level_analysis(prepared_dataset, min_orders=min_threshold)

    assert (prod_df['total_orders'] >= min_threshold).all(), f"Found products with fewer than {min_threshold} orders"
    assert (prod_df['return_rate_pct'] >= 0.0).all()
    assert (prod_df['return_rate_pct'] <= 100.0).all()

def test_interactive_filtering(prepared_dataset):
    """
    Validates filtering by date and product category.
    """
    selected_category = 'Apparel & Clothing'
    filtered = apply_filters(prepared_dataset, categories=[selected_category])

    assert (filtered['product_category'] == selected_category).all()
    assert len(filtered) < len(prepared_dataset)
