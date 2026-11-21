"""
Synthetic Dataset Generator for NorthStar Online Retail Pvt. Ltd.
Project: E-Commerce Order Return Analysis
Project ID: P088
Author: Abhishek Sharma (University Roll No: 2500320140007)
Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01
Institution: ABES Engineering College, Ghaziabad
Project Mentor: Dinesh Sereno
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Set random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

def generate_ecommerce_data(num_records: int = 3000) -> pd.DataFrame:
    """
    Generates a realistic synthetic e-commerce order and return dataset.
    Fulfills all requirements for OQ-01 to OQ-10.
    """
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    total_days = (end_date - start_date).days

    # Catalog definition: Categories, Products, and Baseline Prices
    catalog = {
        'Apparel & Clothing': [
            ('PRD-APP-001', "Men's Slim Fit Denim Jeans", 1899),
            ('PRD-APP-002', "Women's Cotton Floral Maxi Dress", 2499),
            ('PRD-APP-003', "Classic Polo T-Shirt", 899),
            ('PRD-APP-004', "Formal Slim Fit Linen Shirt", 1699),
            ('PRD-APP-005', "Unisex Fleece Pullover Hoodie", 2199),
            ('PRD-APP-006', "Ethnic Embroidered Kurti", 1399),
        ],
        'Footwear': [
            ('PRD-FTW-001', "Breathable Running Sports Shoes", 3499),
            ('PRD-FTW-002', "Men's Genuine Leather Oxford Shoes", 4599),
            ('PRD-FTW-003', "Women's Cushioned Walking Sneakers", 2799),
            ('PRD-FTW-004', "Comfort Slide Sandals", 1199),
            ('PRD-FTW-005', "Lightweight Athletic Gym Trainers", 3199),
        ],
        'Electronics & Gadgets': [
            ('PRD-ELE-001', "True Wireless Bluetooth Earbuds", 2999),
            ('PRD-ELE-002', "Smart Fitness Tracking Watch", 4999),
            ('PRD-ELE-003', "Fast Charging 20000mAh Power Bank", 1999),
            ('PRD-ELE-004', "Portable Waterproof Bluetooth Speaker", 3299),
            ('PRD-ELE-005', "Noise Cancelling Over-Ear Headphones", 7499),
            ('PRD-ELE-006', "Adjustable Aluminum Laptop Stand", 1499),
        ],
        'Home & Kitchen': [
            ('PRD-HOM-001', "Stainless Steel Tri-Ply Cookware Set", 5499),
            ('PRD-HOM-002', "Ceramic Non-Stick Frying Pan (26cm)", 1799),
            ('PRD-HOM-003', "Orthopedic Memory Foam Sleeping Pillow", 1699),
            ('PRD-HOM-004', "Pure Cotton 300TC King Bedsheet", 2299),
            ('PRD-HOM-005', "Electric Cordless Water Kettle (1.8L)", 1399),
            ('PRD-HOM-006', "Airtight Glass Food Storage Containers (6 Pcs)", 1899),
        ],
        'Beauty & Personal Care': [
            ('PRD-BTY-001', "Organic Vitamin C Radiance Face Serum", 899),
            ('PRD-BTY-002', "Hydrating Sunscreen Gel SPF 50+", 649),
            ('PRD-BTY-003', "Sulfate-Free Argan Oil Hair Shampoo", 799),
            ('PRD-BTY-004', "Rejuvenating Night Repair Cream", 1199),
            ('PRD-BTY-005', "Complete Professional Makeup Brush Kit", 1499),
        ],
        'Sports & Fitness': [
            ('PRD-SPT-001', "High-Density Anti-Slip Yoga Mat (6mm)", 1299),
            ('PRD-SPT-002', "Adjustable Hex Rubber Dumbbell Pair (10kg)", 3299),
            ('PRD-SPT-003', "Heavy Duty Resistance Exercise Bands Set", 899),
            ('PRD-SPT-004', "Vacuum Insulated Stainless Steel Sipper (1L)", 999),
            ('PRD-SPT-005', "Multi-Grip Chin-Up Pull-Up Bar", 2199),
        ],
        'Books & Stationery': [
            ('PRD-BKS-001', "Data Science & Python Analytics Handbook", 1199),
            ('PRD-BKS-002', "Hardcover Executive Daily Planner & Journal", 699),
            ('PRD-BKS-003', "Set of 12 Fine-Liner Sketching Pens", 499),
            ('PRD-BKS-004', "Modern Indian History & Economics Compendium", 850),
        ]
    }

    categories = list(catalog.keys())
    # Category weights reflect realistic online retail basket
    cat_weights = [0.26, 0.18, 0.20, 0.15, 0.10, 0.07, 0.04]

    cities_regions = [
        ('Noida', 'North'),
        ('Delhi', 'North'),
        ('Gurugram', 'North'),
        ('Lucknow', 'North'),
        ('Jaipur', 'North'),
        ('Mumbai', 'West'),
        ('Pune', 'West'),
        ('Ahmedabad', 'West'),
        ('Bengaluru', 'South'),
        ('Hyderabad', 'South'),
        ('Chennai', 'South'),
        ('Kolkata', 'East')
    ]

    payment_methods = ['UPI', 'Credit Card', 'Debit Card', 'Cash on Delivery (COD)', 'Net Banking']
    pm_weights = [0.42, 0.25, 0.12, 0.15, 0.06]

    # Return propensity by category (Apparel & Footwear higher, Beauty & Books lower)
    cat_return_baseline = {
        'Apparel & Clothing': 0.31,
        'Footwear': 0.28,
        'Electronics & Gadgets': 0.18,
        'Home & Kitchen': 0.16,
        'Beauty & Personal Care': 0.09,
        'Sports & Fitness': 0.14,
        'Books & Stationery': 0.05
    }

    # Reasons distribution by category
    reasons_by_category = {
        'Apparel & Clothing': [
            ('Size/Fit Issue', 0.52),
            ('Item Different from Description', 0.20),
            ('Damaged / Defective Item', 0.08),
            ('Changed Mind / No Longer Needed', 0.12),
            ('Late Delivery', 0.05),
            ('Wrong Item Received', 0.03)
        ],
        'Footwear': [
            ('Size/Fit Issue', 0.58),
            ('Item Different from Description', 0.16),
            ('Damaged / Defective Item', 0.09),
            ('Changed Mind / No Longer Needed', 0.08),
            ('Late Delivery', 0.05),
            ('Wrong Item Received', 0.04)
        ],
        'Electronics & Gadgets': [
            ('Damaged / Defective Item', 0.42),
            ('Item Different from Description', 0.22),
            ('Late Delivery', 0.15),
            ('Changed Mind / No Longer Needed', 0.12),
            ('Wrong Item Received', 0.09)
        ],
        'Home & Kitchen': [
            ('Damaged / Defective Item', 0.35),
            ('Item Different from Description', 0.25),
            ('Changed Mind / No Longer Needed', 0.20),
            ('Late Delivery', 0.12),
            ('Wrong Item Received', 0.08)
        ],
        'Beauty & Personal Care': [
            ('Damaged / Defective Item', 0.35),
            ('Item Different from Description', 0.30),
            ('Wrong Item Received', 0.20),
            ('Late Delivery', 0.15)
        ],
        'Sports & Fitness': [
            ('Damaged / Defective Item', 0.30),
            ('Size/Fit Issue', 0.25),
            ('Item Different from Description', 0.20),
            ('Changed Mind / No Longer Needed', 0.15),
            ('Late Delivery', 0.10)
        ],
        'Books & Stationery': [
            ('Damaged / Defective Item', 0.45),
            ('Wrong Item Received', 0.25),
            ('Changed Mind / No Longer Needed', 0.15),
            ('Late Delivery', 0.15)
        ]
    }

    records = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-2025-{10000 + i}"
        cust_id = f"CUST-{random.randint(1000, 9999)}"

        # Order Date with realistic seasonal fluctuations (peaks in festive Oct-Nov)
        random_day = random.randint(0, total_days)
        order_date = start_date + timedelta(days=random_day)

        # Pick Category and Product
        category = random.choices(categories, weights=cat_weights)[0]
        prod_tuple = random.choice(catalog[category])
        product_id, product_name, unit_price = prod_tuple

        # Quantity and Order Value
        quantity = random.choices([1, 2, 3, 4], weights=[0.72, 0.20, 0.06, 0.02])[0]
        order_value = unit_price * quantity

        # Payment & City
        payment_method = random.choices(payment_methods, weights=pm_weights)[0]
        city, region = random.choice(cities_regions)

        # Delivery timelines: Expected transit is 3-6 days
        transit_days_expected = random.randint(3, 6)
        expected_delivery = order_date + timedelta(days=transit_days_expected)

        # Actual delivery with realistic delay distribution
        # 75% on time or early, 25% delayed
        delay_prob = random.random()
        if delay_prob < 0.25:
            # Delayed by 1 to 6 days
            delay_days = random.randint(1, 6)
        elif delay_prob < 0.50:
            # Delivered exactly on expected date
            delay_days = 0
        else:
            # Delivered 1 or 2 days early
            delay_days = -random.randint(1, 2)

        actual_delivery = expected_delivery + timedelta(days=delay_days)
        delivery_status = 'Delivered'

        # Return probability: influenced by category baseline, payment method (COD slightly higher), and delays
        p_return = cat_return_baseline[category]
        if payment_method == 'Cash on Delivery (COD)':
            p_return += 0.05
        if delay_days > 2:
            p_return += 0.12  # Delay directly increases return rate
        elif delay_days > 0:
            p_return += 0.05

        # Some specific products have slightly higher defect / fit issues (OQ-10 support)
        if product_id in ['PRD-APP-001', 'PRD-FTW-001', 'PRD-ELE-005']:
            p_return += 0.08

        # Cap probability
        p_return = min(max(p_return, 0.02), 0.70)

        is_returned = random.random() < p_return

        if is_returned:
            return_status = 'Returned'
            # Return requested 1 to 7 days after delivery
            return_days = random.randint(1, 7)
            return_date = actual_delivery + timedelta(days=return_days)

            # Assign return reason
            reason_options = reasons_by_category[category]
            reasons = [r[0] for r in reason_options]
            weights = [r[1] for r in reason_options]

            # If delayed, boost probability of Late Delivery reason
            if delay_days > 0 and 'Late Delivery' in reasons:
                idx = reasons.index('Late Delivery')
                weights = list(weights)
                weights[idx] += 0.35

            # Normalize weights
            weight_sum = sum(weights)
            weights = [w / weight_sum for w in weights]

            return_reason = random.choices(reasons, weights=weights)[0]
            refund_amount = float(order_value)
            refund_status = 'Completed'
        else:
            return_status = 'Not Returned'
            return_date = None
            return_reason = 'Not Applicable'
            refund_amount = 0.0
            refund_status = 'Not Applicable'

        records.append({
            'order_id': order_id,
            'customer_id': cust_id,
            'order_date': order_date.strftime('%Y-%m-%d'),
            'product_category': category,
            'product_id': product_id,
            'product_name': product_name,
            'quantity': quantity,
            'unit_price': unit_price,
            'order_value': order_value,
            'payment_method': payment_method,
            'delivery_city': city,
            'delivery_region': region,
            'expected_delivery_date': expected_delivery.strftime('%Y-%m-%d'),
            'actual_delivery_date': actual_delivery.strftime('%Y-%m-%d'),
            'delivery_delay_days': delay_days,
            'delivery_status': delivery_status,
            'return_status': return_status,
            'return_date': return_date.strftime('%Y-%m-%d') if return_date else None,
            'return_reason': return_reason,
            'refund_amount': refund_amount,
            'refund_status': refund_status
        })

    df = pd.DataFrame(records)
    return df

def save_and_initialize_data(output_dir: str = None) -> str:
    """Generates synthetic dataset and saves it to CSV."""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "orders_returns.csv")

    df = generate_ecommerce_data(num_records=3000)
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} records successfully saved to {csv_path}")
    print(f"Total Orders: {df['order_id'].nunique()}")
    print(f"Returned Orders: {(df['return_status'] == 'Returned').sum()}")
    print(f"Return Rate: {((df['return_status'] == 'Returned').sum() / len(df) * 100):.2f}%")
    print(f"Total Refund Value: ₹{df['refund_amount'].sum():,.2f}")
    return csv_path

if __name__ == '__main__':
    save_and_initialize_data()
