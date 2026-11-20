"""
E-Commerce Order Return Analysis Dashboard
Organisation: NorthStar Online Retail Pvt. Ltd. (Noida, Uttar Pradesh)
Author: Abhishek Sharma (Roll No: 2503201450007)
Programme: MCA 2nd Year – Data Analytics, ABES Engineering College, Ghaziabad
Mentor: Dinesh Sereno
"""

import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st

# Configure page layout and metadata
st.set_page_config(
    page_title="E-Commerce Order Return Analysis | NorthStar Retail",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from src.analytics import (
    prepare_dataframe,
    apply_filters,
    calculate_core_kpis,
    get_monthly_trends,
    get_category_metrics,
    get_return_reasons_breakdown,
    get_payment_method_metrics,
    get_delivery_delay_analysis,
    get_product_level_analysis,
    get_region_metrics
)
from src.charts import (
    plot_monthly_trend,
    plot_category_performance,
    plot_return_reasons_breakdown,
    plot_payment_methods,
    plot_delivery_delay_comparison,
    plot_product_risk_matrix,
    plot_refund_value_by_category
)
from src.db_manager import DatabaseManager
from data.database import init_database

# Custom Responsive Styling (Zero Overlapping Text)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        padding: 24px 28px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.0rem;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.3;
        word-wrap: break-word;
    }
    .main-header p {
        margin: 8px 0 12px 0;
        font-size: 1.0rem;
        color: #CBD5E1;
        line-height: 1.4;
    }
    .meta-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.82rem;
        margin-right: 8px;
        margin-top: 6px;
        margin-bottom: 4px;
        white-space: nowrap;
        line-height: 1.4;
    }
    .kpi-card {
        background: #FFFFFF;
        padding: 18px 22px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        text-align: left;
        margin-bottom: 14px;
        min-height: 115px;
        box-sizing: border-box;
    }
    .kpi-title {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        line-height: 1.3;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #0F172A;
        font-size: 1.85rem;
        font-weight: 700;
        line-height: 1.2;
        word-break: break-word;
    }
    .kpi-subtitle {
        color: #64748B;
        font-size: 0.82rem;
        margin-top: 6px;
        line-height: 1.3;
    }
    .kpi-bad { color: #DC2626 !important; }
    .kpi-good { color: #16A34A !important; }
    .kpi-warn { color: #D97706 !important; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        background-color: #F8FAFC;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 16px;
        font-weight: 600;
        font-size: 0.92rem;
        white-space: nowrap;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E2E8F0 !important;
        color: #1E3A8A !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_and_initialize_data():
    """Initializes SQLite and returns cached DataFrame."""
    db_path = os.path.join(current_dir, "data", "ecommerce_returns.db")
    csv_path = os.path.join(current_dir, "data", "orders_returns.csv")

    if not os.path.exists(db_path) or not os.path.exists(csv_path):
        init_database(db_path=db_path, csv_path=csv_path)

    db_manager = DatabaseManager(db_path=db_path)
    df = db_manager.fetch_all_orders()
    df = prepare_dataframe(df)
    return df, db_manager

# Header Banner
st.markdown("""
<div class="main-header">
    <h1>📦 NorthStar Retail — E-Commerce Order Return Analytics</h1>
    <p>Operational decision-support dashboard measuring return velocity, root causes, financial leakage, and delivery delays.</p>
    <div>
        <span class="meta-badge"><b>Student:</b> Abhishek Sharma</span>
        <span class="meta-badge"><b>Roll No:</b> 2503201450007</span>
        <span class="meta-badge"><b>Course:</b> MCA 2nd Year (Data Analytics)</span>
        <span class="meta-badge"><b>Mentor:</b> Dinesh Sereno</span>
        <span class="meta-badge"><b>Institution:</b> ABES Engineering College, Ghaziabad</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Load Data
with st.spinner("Connecting to SQLite database and loading dataset..."):
    df_raw, db_mgr = load_and_initialize_data()

# ================= SIDEBAR CONTROLS =================
st.sidebar.image("https://img.icons8.com/fluency/96/delivery.png", width=64)
st.sidebar.title("Filter & Slicing Panel")
st.sidebar.caption("Filter order records interactively to analyze subsets.")

min_date = df_raw['order_date'].min().date()
max_date = df_raw['order_date'].max().date()

# Date Range Filter
date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

start_date, end_date = None, None
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range[0], date_range[1]
elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
    start_date = date_range[0]
    end_date = max_date

# Category Multi-Select
all_categories = sorted(df_raw['product_category'].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Product Categories",
    options=all_categories,
    default=all_categories
)

# Payment Method Multi-Select
all_payment_methods = sorted(df_raw['payment_method'].unique().tolist())
selected_pm = st.sidebar.multiselect(
    "Payment Methods",
    options=all_payment_methods,
    default=all_payment_methods
)

# Region Multi-Select
all_regions = sorted(df_raw['delivery_region'].unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Delivery Regions",
    options=all_regions,
    default=all_regions
)

# Return Status
return_status_filter = st.sidebar.radio(
    "Return Status Slicer",
    options=["All", "Returned Only", "Not Returned Only"],
    index=0
)
status_map = {
    "All": "All",
    "Returned Only": "Returned",
    "Not Returned Only": "Not Returned"
}

# Apply Filters
df_filtered = apply_filters(
    df=df_raw,
    start_date=start_date,
    end_date=end_date,
    categories=selected_categories,
    payment_methods=selected_pm,
    regions=selected_regions,
    return_status=status_map[return_status_filter]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filtered Orders:** `{len(df_filtered):,}` / `{len(df_raw):,}`")
st.sidebar.caption("⚡ Powered by SQLite, Pandas, Plotly & Streamlit")

# ================= TOP KPI SUMMARY CARDS (2 Rows x 3 Columns) =================
# Avoids cramped 6-column layout to prevent any text overlapping
kpis = calculate_core_kpis(df_filtered)

# Row 1: Volume & Return Rates
r1_c1, r1_c2, r1_c3 = st.columns(3)

with r1_c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Orders (OQ-01)</div>
        <div class="kpi-value">{kpis['total_orders']:,}</div>
        <div class="kpi-subtitle">Distinct order records in period</div>
    </div>
    """, unsafe_allow_html=True)

with r1_c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Returned Orders (OQ-02)</div>
        <div class="kpi-value kpi-bad">{kpis['returned_orders']:,}</div>
        <div class="kpi-subtitle">Customer return requests filed</div>
    </div>
    """, unsafe_allow_html=True)

with r1_c3:
    rate_class = "kpi-bad" if kpis['return_rate_pct'] > 20 else "kpi-good"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Return Rate (OQ-02)</div>
        <div class="kpi-value {rate_class}">{kpis['return_rate_pct']:.2f}%</div>
        <div class="kpi-subtitle">Benchmark Target: &lt; 18.0%</div>
    </div>
    """, unsafe_allow_html=True)

# Row 2: Financial Outflow & Logistics Delays
r2_c1, r2_c2, r2_c3 = st.columns(3)

with r2_c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Refund Outflow (OQ-07)</div>
        <div class="kpi-value kpi-bad">₹{kpis['total_refund']:,.0f}</div>
        <div class="kpi-subtitle">Gross refund loss from returns</div>
    </div>
    """, unsafe_allow_html=True)

with r2_c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Net Retained Sales</div>
        <div class="kpi-value kpi-good">₹{kpis['net_revenue']:,.0f}</div>
        <div class="kpi-subtitle">Gross Revenue: ₹{kpis['total_revenue']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with r2_c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Fulfillment Delay Gap (OQ-09)</div>
        <div class="kpi-value kpi-warn">{kpis['avg_delivery_delay_returned']:+.1f} days</div>
        <div class="kpi-subtitle">Non-returned orders: {kpis['avg_delivery_delay_non_returned']:+.1f} days</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ================= TAB NAVIGATION =================
tabs = st.tabs([
    "📈 Trends & Macro KPIs",
    "🏷️ Categories & Reasons",
    "🚚 Fulfillment & Payments",
    "🎯 Product Risk Review",
    "🗃️ SQL & Data Explorer",
    "📑 Academic Traceability"
])

# ----------------- TAB 1: Trends & Macro KPIs -----------------
with tabs[0]:
    st.subheader("Monthly Return Velocity & Financial Leakage")
    st.write("Tracking the progression of return rates and order volumes over time answers **OQ-03** and **OQ-07**.")

    col_t1, col_t2 = st.columns([1.5, 1])

    with col_t1:
        trends_df = get_monthly_trends(df_filtered)
        fig_trend = plot_monthly_trend(trends_df)
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_t2:
        cat_metrics = get_category_metrics(df_filtered)
        fig_refund = plot_refund_value_by_category(cat_metrics)
        st.plotly_chart(fig_refund, use_container_width=True)

    st.markdown("### 💡 Key Observations & Monthly Insights")
    st.info(
        f"Across the filtered window, NorthStar processed **{kpis['total_orders']:,}** orders yielding **₹{kpis['total_revenue']:,.2f}** in gross sales. "
        f"A total of **{kpis['returned_orders']:,}** orders were returned, representing an overall return rate of **{kpis['return_rate_pct']:.2f}%** "
        f"and causing a direct revenue refund leakage of **₹{kpis['total_refund']:,.2f}**."
    )

    with st.expander("📊 View Detailed Monthly Aggregates Table"):
        display_trends = trends_df.rename(columns={
            'year_month': 'Month',
            'month_name': 'Month Name',
            'total_orders': 'Total Orders',
            'returned_orders': 'Returned Orders',
            'return_rate_pct': 'Return Rate (%)',
            'total_revenue': 'Gross Revenue (₹)',
            'total_refund': 'Refund Amount (₹)'
        })
        st.dataframe(display_trends, use_container_width=True)

# ----------------- TAB 2: Categories & Reasons -----------------
with tabs[1]:
    st.subheader("Category Return Analysis & Root Reason Breakdown")
    st.write("Examines which product categories suffer highest return counts (**OQ-04**), highest return rates (**OQ-05**), and root customer causes (**OQ-06**).")

    cat_df = get_category_metrics(df_filtered)
    fig_cat = plot_category_performance(cat_df)
    st.plotly_chart(fig_cat, use_container_width=True)

    col_r1, col_r2 = st.columns([1, 1])

    with col_r1:
        drill_cat = st.selectbox(
            "Drilldown Return Reasons by Category",
            options=["All"] + all_categories,
            index=0
        )
        reasons_df = get_return_reasons_breakdown(df_filtered, category=drill_cat)
        fig_reasons = plot_return_reasons_breakdown(reasons_df)
        st.plotly_chart(fig_reasons, use_container_width=True)

    with col_r2:
        st.markdown(f"#### Return Reasons Breakdown Table ({drill_cat})")
        if not reasons_df.empty:
            display_reasons = reasons_df.rename(columns={
                'return_reason': 'Customer Return Reason',
                'count': 'Returned Orders Count',
                'percentage_of_returns': 'Share of Total Returns (%)',
                'refund_amount': 'Refund Impact (₹)'
            })
            st.dataframe(display_reasons, use_container_width=True)

            top_reason = reasons_df.iloc[0]['return_reason']
            top_share = reasons_df.iloc[0]['percentage_of_returns']
            st.warning(f"⚠️ Primary Return Driver: **{top_reason}** accounts for **{top_share:.1f}%** of returns in this category selection.")
        else:
            st.info("No returns recorded for the selected category filter.")

# ----------------- TAB 3: Delivery Delays & Payments -----------------
with tabs[2]:
    st.subheader("Operational Influencers: Delivery Delays & Payment Channels")
    st.write("Investigating fulfillment bottlenecks (**OQ-09**) and payment method return propensity (**OQ-08**).")

    # Payment Methods
    pm_df = get_payment_method_metrics(df_filtered)
    fig_pm = plot_payment_methods(pm_df)
    st.plotly_chart(fig_pm, use_container_width=True)

    st.markdown("---")
    st.subheader("Delivery Delay Correlation Analysis (OQ-09)")

    delay_stats = get_delivery_delay_analysis(df_filtered)
    fig_delays = plot_delivery_delay_comparison(df_filtered, delay_stats['delay_bracket_df'])
    st.plotly_chart(fig_delays, use_container_width=True)

    c_d1, c_d2 = st.columns(2)
    with c_d1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Fulfillment Delay Comparison (OQ-09)</div>
            <p style="margin: 8px 0 4px 0; font-size: 1rem;"><b>Returned Orders Avg Delay:</b> <span class="kpi-bad" style="font-weight:700;">{delay_stats['avg_delay_returned']:+.2f} days</span></p>
            <p style="margin: 4px 0 8px 0; font-size: 1rem;"><b>Non-Returned Orders Avg Delay:</b> <span class="kpi-good" style="font-weight:700;">{delay_stats['avg_delay_non_returned']:+.2f} days</span></p>
            <div class="kpi-subtitle">Difference: <b>{delay_stats['avg_delay_returned'] - delay_stats['avg_delay_non_returned']:+.2f} days longer</b></div>
        </div>
        """, unsafe_allow_html=True)

    with c_d2:
        st.markdown("#### Delivery Delay Bracket Return Rates")
        bracket_table = delay_stats['delay_bracket_df'].rename(columns={
            'delay_category': 'Delivery Transit Bracket',
            'total_orders': 'Total Orders',
            'returned_orders': 'Returned Orders',
            'return_rate_pct': 'Return Rate (%)'
        })
        st.dataframe(bracket_table, use_container_width=True)

    st.success(
        "📌 **Operational Decision Insight:** Data demonstrates a strong positive correlation between courier transit delays and customer return propensity. "
        "Orders delayed by 3+ days demonstrate a significantly elevated return rate. Prioritizing expedited dispatch and proactive courier tracking notifications in Noida and North zone warehouses will immediately mitigate return volume."
    )

# ----------------- TAB 4: Product Risk Review -----------------
with tabs[3]:
    st.subheader("Product-Level Return Rate & Defect Investigation (OQ-10)")
    st.write("Identifies anomalous SKUs requiring listing revision, vendor quality audit, or sizing chart enhancement. Includes minimum order threshold protection.")

    col_ctrl1, col_ctrl2 = st.columns([1, 1])
    with col_ctrl1:
        min_order_thresh = st.slider("Minimum Orders Threshold (Filters out low-sample noise)", min_value=5, max_value=80, value=15, step=5)
    with col_ctrl2:
        benchmark_thresh = st.slider("Benchmark Alert Threshold (% Return Rate)", min_value=10.0, max_value=40.0, value=22.0, step=1.0)

    prod_analysis_df = get_product_level_analysis(df_filtered, min_orders=min_order_thresh)

    fig_prod_matrix = plot_product_risk_matrix(prod_analysis_df, benchmark_rate=benchmark_thresh)
    st.plotly_chart(fig_prod_matrix, use_container_width=True)

    st.markdown("#### Ranked High-Return Products Requiring Immediate Investigation")
    high_risk_skus = prod_analysis_df[prod_analysis_df['return_rate_pct'] >= benchmark_thresh]

    if not high_risk_skus.empty:
        st.error(f"🚨 **{len(high_risk_skus)} products** exceed the critical threshold of {benchmark_thresh:.1f}% return rate.")
    else:
        st.success(f"✅ No products exceed the {benchmark_thresh:.1f}% threshold at minimum order count of {min_order_thresh}.")

    display_prod = prod_analysis_df.rename(columns={
        'product_id': 'Product ID',
        'product_name': 'Product Name',
        'product_category': 'Category',
        'total_orders': 'Total Orders',
        'returned_orders': 'Returned Orders',
        'return_rate_pct': 'Return Rate (%)',
        'unit_price': 'Unit Price (₹)',
        'total_refund': 'Refund Outflow (₹)'
    })
    st.dataframe(display_prod, use_container_width=True)

# ----------------- TAB 5: SQL & Data Explorer -----------------
with tabs[4]:
    st.subheader("Raw Data Explorer & SQLite SQL Query Studio")
    st.write("Enables academic reviewers and analysts to inspect the SQLite backend schema, execute custom SQL, and export data.")

    col_sql1, col_sql2 = st.columns([1.8, 1.2])

    with col_sql1:
        st.markdown("#### Execute SQL Query on `orders` Table")
        sample_queries = {
            "Select Category Summary": "SELECT product_category, COUNT(order_id) as total_orders, SUM(CASE WHEN return_status = 'Returned' THEN 1 ELSE 0 END) as returns, ROUND(SUM(refund_amount), 2) as total_refund FROM orders GROUP BY product_category ORDER BY returns DESC;",
            "Select Delay Analysis": "SELECT delivery_delay_days, COUNT(*) as count, SUM(CASE WHEN return_status = 'Returned' THEN 1 ELSE 0 END) as returns FROM orders GROUP BY delivery_delay_days ORDER BY delivery_delay_days ASC;",
            "Top 5 Refunded Products": "SELECT product_id, product_name, SUM(refund_amount) as total_refund, COUNT(*) as total_orders FROM orders WHERE return_status = 'Returned' GROUP BY product_id ORDER BY total_refund DESC LIMIT 5;",
            "Payment Method Return Rates": "SELECT payment_method, COUNT(*) as total_orders, ROUND(100.0 * SUM(CASE WHEN return_status = 'Returned' THEN 1 ELSE 0 END) / COUNT(*), 2) as return_rate_pct FROM orders GROUP BY payment_method ORDER BY return_rate_pct DESC;"
        }

        query_choice = st.selectbox("Choose a pre-defined evaluation query or write your own below:", list(sample_queries.keys()))
        custom_sql = st.text_area("SQL Query Input", value=sample_queries[query_choice], height=110)

        if st.button("Run SQL Query", type="primary"):
            try:
                sql_result = db_mgr.execute_custom_query(custom_sql)
                st.success(f"Query returned {len(sql_result)} rows.")
                st.dataframe(sql_result, use_container_width=True)
            except Exception as e:
                st.error(f"SQL Execution Error: {str(e)}")

    with col_sql2:
        st.markdown("#### Database Schema Information")
        st.markdown("""
        **Table:** `orders` (SQLite 3)
        - `order_id` (PK, TEXT)
        - `customer_id` (TEXT)
        - `order_date` (TEXT ISO8601)
        - `product_category` (TEXT)
        - `product_id`, `product_name` (TEXT)
        - `quantity` (INT), `unit_price`, `order_value` (REAL)
        - `payment_method`, `delivery_city`, `delivery_region` (TEXT)
        - `expected_delivery_date`, `actual_delivery_date` (TEXT)
        - `delivery_delay_days` (INT)
        - `delivery_status`, `return_status` (TEXT)
        - `return_date`, `return_reason` (TEXT)
        - `refund_amount` (REAL), `refund_status` (TEXT)
        """)

    st.markdown("---")
    st.markdown("#### Filtered Records Data Grid")
    st.dataframe(df_filtered.head(100), use_container_width=True)

    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name="northstar_order_returns_filtered.csv",
        mime="text/csv"
    )

# ----------------- TAB 6: Academic Traceability -----------------
with tabs[5]:
    st.subheader("Academic Requirements & Operational Question (OQ) Traceability Matrix")
    st.markdown("Complete mapping from **Step 1 – Project Understanding Document** to application implementation.")

    traceability_data = [
        {"OQ ID": "OQ-01", "Operational Question": "How many total orders are present in the selected period?", "Dataset Fields": "order_id, order_date", "Calculation": "COUNT(DISTINCT order_id)", "Status": "Implemented (KPI Card 1, Tab 1)"},
        {"OQ ID": "OQ-02", "Operational Question": "How many orders were returned, and what is the overall return rate?", "Dataset Fields": "order_id, return_status", "Calculation": "(Returned orders / Total orders) * 100", "Status": "Implemented (KPI Cards 2 & 3)"},
        {"OQ ID": "OQ-03", "Operational Question": "How does the return rate change month by month?", "Dataset Fields": "order_id, order_date, return_status", "Calculation": "Monthly aggregation & rate", "Status": "Implemented (Tab 1 Combo Chart)"},
        {"OQ ID": "OQ-04", "Operational Question": "Which product categories have highest number of returns?", "Dataset Fields": "order_id, product_category, return_status", "Calculation": "COUNT(order_id) WHERE Returned by category", "Status": "Implemented (Tab 2 Bar Chart)"},
        {"OQ ID": "OQ-05", "Operational Question": "Which product categories have the highest return rate?", "Dataset Fields": "order_id, product_category, return_status", "Calculation": "Category returns / category orders * 100", "Status": "Implemented (Tab 2 Bar Chart)"},
        {"OQ ID": "OQ-06", "Operational Question": "What are the most common reasons customers return products?", "Dataset Fields": "return_status, return_reason", "Calculation": "COUNT & % distribution by reason", "Status": "Implemented (Tab 2 Donut Chart)"},
        {"OQ ID": "OQ-07", "Operational Question": "What is the total refund value associated with returns?", "Dataset Fields": "return_status, refund_amount", "Calculation": "SUM(refund_amount) for returned orders", "Status": "Implemented (KPI Card 4, Tab 1)"},
        {"OQ ID": "OQ-08", "Operational Question": "Which payment methods are associated with largest returns?", "Dataset Fields": "payment_method, return_status", "Calculation": "Returns count & rate by payment method", "Status": "Implemented (Tab 3 Dual Axis)"},
        {"OQ ID": "OQ-09", "Operational Question": "Do delivery delays appear more frequently among returned orders?", "Dataset Fields": "expected_delivery_date, actual_delivery_date, delay_days", "Calculation": "actual_date - expected_date; comparison", "Status": "Implemented (Tab 3 Delay Box/Bar)"},
        {"OQ ID": "OQ-10", "Operational Question": "Which products show unusually high return rates and should be reviewed?", "Dataset Fields": "product_id, product_name, return_status", "Calculation": "Product rate with min order threshold", "Status": "Implemented (Tab 4 Scatter Matrix)"}
    ]
    st.dataframe(pd.DataFrame(traceability_data), use_container_width=True)

    st.markdown("### Stakeholders & Decision Support Mapping")
    stakeholders = [
        {"SH ID": "SH-01", "Stakeholder": "Operations / E-commerce Manager", "App View": "KPI Cards & Tab 1 Trends", "Primary Decision": "Prioritize operational interventions and weekly performance targets"},
        {"SH ID": "SH-02", "Stakeholder": "Business / Data Analyst", "App View": "Tab 5 SQL Console & Filters", "Primary Decision": "Slice cohorts, evaluate correlations and prepare deep-dive reports"},
        {"SH ID": "SH-03", "Stakeholder": "Customer Support Lead", "App View": "Tab 2 Return Reasons Donut", "Primary Decision": "Refine customer feedback loops and return authorization rules"},
        {"SH ID": "SH-04", "Stakeholder": "Product / Category Manager", "App View": "Tab 4 Product Risk Matrix", "Primary Decision": "Audit vendor quality, update sizing guides, or delist high-return SKUs"},
        {"SH ID": "SH-05", "Stakeholder": "Warehouse / Fulfilment Lead", "App View": "Tab 3 Delivery Delay Analysis", "Primary Decision": "Address logistics courier bottlenecks and packaging damage rates"},
        {"SH ID": "SH-06", "Stakeholder": "Student Developer (Abhishek Sharma)", "App View": "Entire Prototype & Pytest Suite", "Primary Decision": "Ensure academic rigor, clean architecture, and test coverage"},
        {"SH ID": "SH-07", "Stakeholder": "Mentor (Dinesh Sereno)", "App View": "Academic Traceability & Report", "Primary Decision": "Verify academic excellence and project requirement fulfillment"}
    ]
    st.dataframe(pd.DataFrame(stakeholders), use_container_width=True)
