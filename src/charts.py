"""
Plotly Visualisation Generator for E-Commerce Order Return Analysis
Provides 7+ interactive charts for the Streamlit Dashboard.
Author: Abhishek Sharma (Roll No: 2503201450007)
NorthStar Online Retail Pvt. Ltd.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any

# Primary Theme Colors
COLOR_PRIMARY = "#1E3A8A"    # Deep Navy
COLOR_ACCENT = "#EF4444"     # Crimson Red (Returns)
COLOR_SUCCESS = "#10B981"    # Emerald Green (Delivered/Retained)
COLOR_WARNING = "#F59E0B"    # Amber Yellow
COLOR_SECONDARY = "#3B82F6"  # Royal Blue
COLOR_MUTED = "#64748B"      # Slate Gray
COLOR_PURPLE = "#8B5CF6"     # Violet

THEME_LAYOUT = dict(
    font=dict(family="Segoe UI, Inter, sans-serif", size=12),
    plot_bgcolor="rgba(248, 250, 252, 0.5)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=40, t=50, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

def plot_monthly_trend(trends_df: pd.DataFrame) -> go.Figure:
    """
    OQ-03: Monthly Order Volume vs Return Rate %
    Dual-axis combo chart.
    """
    if trends_df.empty:
        return go.Figure()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Bar: Total Orders
    fig.add_trace(
        go.Bar(
            x=trends_df['year_month'],
            y=trends_df['total_orders'],
            name="Total Orders",
            marker_color=COLOR_SECONDARY,
            opacity=0.6,
            hovertemplate="Month: %{x}<br>Total Orders: %{y}<extra></extra>"
        ),
        secondary_y=False
    )

    # Bar: Returned Orders
    fig.add_trace(
        go.Bar(
            x=trends_df['year_month'],
            y=trends_df['returned_orders'],
            name="Returned Orders",
            marker_color=COLOR_ACCENT,
            opacity=0.85,
            hovertemplate="Month: %{x}<br>Returned Orders: %{y}<extra></extra>"
        ),
        secondary_y=False
    )

    # Line: Return Rate %
    fig.add_trace(
        go.Scatter(
            x=trends_df['year_month'],
            y=trends_df['return_rate_pct'],
            name="Return Rate (%)",
            mode="lines+markers+text",
            text=[f"{val:.1f}%" for val in trends_df['return_rate_pct']],
            textposition="top center",
            line=dict(color="#B91C1C", width=3),
            marker=dict(size=8, symbol="diamond"),
            hovertemplate="Month: %{x}<br>Return Rate: %{y:.2f}%<extra></extra>"
        ),
        secondary_y=True
    )

    fig.update_layout(
        title="<b>Monthly Order Volume vs Return Rate Trend (OQ-03)</b>",
        barmode="group",
        **THEME_LAYOUT
    )
    fig.update_xaxes(title_text="Order Month", showgrid=False)
    fig.update_yaxes(title_text="Order Count", secondary_y=False, showgrid=True, gridcolor="#E2E8F0")
    fig.update_yaxes(title_text="Return Rate (%)", secondary_y=True, showgrid=False, range=[0, max(trends_df['return_rate_pct'].max() * 1.3, 40)])
    return fig

def plot_category_performance(cat_df: pd.DataFrame) -> go.Figure:
    """
    OQ-04 & OQ-05: Category Return Volume and Return Rate %
    """
    if cat_df.empty:
        return go.Figure()

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Returned Orders by Category (OQ-04)", "Return Rate (%) by Category (OQ-05)"),
        horizontal_spacing=0.12
    )

    # Bar 1: Returned Order Count (OQ-04)
    cat_df_sorted_vol = cat_df.sort_values('returned_orders', ascending=True)
    fig.add_trace(
        go.Bar(
            x=cat_df_sorted_vol['returned_orders'],
            y=cat_df_sorted_vol['product_category'],
            orientation='h',
            name="Returned Orders",
            marker=dict(color=COLOR_ACCENT),
            text=cat_df_sorted_vol['returned_orders'],
            textposition='auto',
            hovertemplate="Category: %{y}<br>Returned Orders: %{x}<extra></extra>"
        ),
        row=1, col=1
    )

    # Bar 2: Return Rate % (OQ-05)
    cat_df_sorted_rate = cat_df.sort_values('return_rate_pct', ascending=True)
    fig.add_trace(
        go.Bar(
            x=cat_df_sorted_rate['return_rate_pct'],
            y=cat_df_sorted_rate['product_category'],
            orientation='h',
            name="Return Rate %",
            marker=dict(color=COLOR_WARNING),
            text=[f"{v:.1f}%" for v in cat_df_sorted_rate['return_rate_pct']],
            textposition='auto',
            hovertemplate="Category: %{y}<br>Return Rate: %{x:.2f}%<extra></extra>"
        ),
        row=1, col=2
    )

    fig.update_layout(
        showlegend=False,
        **THEME_LAYOUT
    )
    fig.update_xaxes(title_text="Count of Returned Orders", row=1, col=1, gridcolor="#E2E8F0")
    fig.update_xaxes(title_text="Return Rate (%)", row=1, col=2, gridcolor="#E2E8F0")
    return fig

def plot_return_reasons_breakdown(reasons_df: pd.DataFrame) -> go.Figure:
    """
    OQ-06: Most Common Return Reasons
    Interactive Donut Chart with count and percentage.
    """
    if reasons_df.empty:
        return go.Figure()

    color_palette = ['#EF4444', '#F97316', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6', '#64748B']

    fig = go.Figure(data=[
        go.Pie(
            labels=reasons_df['return_reason'],
            values=reasons_df['count'],
            hole=0.45,
            marker=dict(colors=color_palette[:len(reasons_df)]),
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Returned Orders: %{value}<br>Share: %{percent}<extra></extra>"
        )
    ])

    fig.update_layout(
        title="<b>Distribution of Customer Return Reasons (OQ-06)</b>",
        **THEME_LAYOUT
    )
    return fig

def plot_payment_methods(pm_df: pd.DataFrame) -> go.Figure:
    """
    OQ-08: Returned Orders & Return Rate by Payment Method
    """
    if pm_df.empty:
        return go.Figure()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=pm_df['payment_method'],
            y=pm_df['returned_orders'],
            name="Returned Orders",
            marker_color=COLOR_PRIMARY,
            text=pm_df['returned_orders'],
            textposition="auto",
            hovertemplate="Payment: %{x}<br>Returns: %{y}<extra></extra>"
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=pm_df['payment_method'],
            y=pm_df['return_rate_pct'],
            name="Return Rate (%)",
            mode="lines+markers+text",
            text=[f"{v:.1f}%" for v in pm_df['return_rate_pct']],
            textposition="top center",
            line=dict(color=COLOR_ACCENT, width=3),
            marker=dict(size=9, symbol="circle"),
            hovertemplate="Payment: %{x}<br>Return Rate: %{y:.2f}%<extra></extra>"
        ),
        secondary_y=True
    )

    fig.update_layout(
        title="<b>Returns and Return Rate by Payment Method (OQ-08)</b>",
        **THEME_LAYOUT
    )
    fig.update_xaxes(title_text="Payment Method", showgrid=False)
    fig.update_yaxes(title_text="Returned Order Count", secondary_y=False, gridcolor="#E2E8F0")
    fig.update_yaxes(title_text="Return Rate (%)", secondary_y=True, showgrid=False, range=[0, max(pm_df['return_rate_pct'].max() * 1.35, 40)])
    return fig

def plot_delivery_delay_comparison(raw_df: pd.DataFrame, delay_bracket_df: pd.DataFrame) -> go.Figure:
    """
    OQ-09: Delivery Delays vs Order Returns
    Left: Box plot of delay distribution. Right: Return Rate % by Delay Category.
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Delivery Delay Days Distribution (OQ-09)", "Return Rate % by Delay Category"),
        horizontal_spacing=0.12
    )

    # Box Plot for delay days
    fig.add_trace(
        go.Box(
            x=raw_df['return_status'],
            y=raw_df['delivery_delay_days'],
            marker_color=COLOR_PRIMARY,
            boxpoints='outliers',
            name="Delay Days",
            hovertemplate="Status: %{x}<br>Delay: %{y} days<extra></extra>"
        ),
        row=1, col=1
    )

    # Bar chart for return rate by delay category
    if not delay_bracket_df.empty:
        fig.add_trace(
            go.Bar(
                x=delay_bracket_df['delay_category'],
                y=delay_bracket_df['return_rate_pct'],
                marker_color=[COLOR_SUCCESS, COLOR_SECONDARY, COLOR_WARNING, COLOR_ACCENT, COLOR_MUTED][:len(delay_bracket_df)],
                text=[f"{v:.1f}%" for v in delay_bracket_df['return_rate_pct']],
                textposition='auto',
                name="Return Rate %",
                hovertemplate="Category: %{x}<br>Return Rate: %{y:.2f}%<extra></extra>"
            ),
            row=1, col=2
        )

    fig.update_layout(
        showlegend=False,
        **THEME_LAYOUT
    )
    fig.update_yaxes(title_text="Delay Days (Actual - Expected)", row=1, col=1, gridcolor="#E2E8F0")
    fig.update_yaxes(title_text="Return Rate (%)", row=1, col=2, gridcolor="#E2E8F0")
    fig.update_xaxes(title_text="Return Status", row=1, col=1)
    fig.update_xaxes(title_text="Delivery Timeline Category", row=1, col=2)
    return fig

def plot_product_risk_matrix(prod_df: pd.DataFrame, benchmark_rate: float = 20.0) -> go.Figure:
    """
    OQ-10: Products with High Return Rates & Threshold Review
    Bubble / Scatter plot: Total Orders vs Return Rate %, sized by Refund Amount.
    """
    if prod_df.empty:
        return go.Figure()

    fig = px.scatter(
        prod_df,
        x="total_orders",
        y="return_rate_pct",
        size="total_refund",
        color="product_category",
        hover_name="product_name",
        hover_data={
            "product_id": True,
            "total_orders": True,
            "returned_orders": True,
            "return_rate_pct": ":.2f",
            "unit_price": ":.2f",
            "total_refund": ":,.2f"
        },
        labels={
            "total_orders": "Total Orders Placed",
            "return_rate_pct": "Return Rate (%)",
            "total_refund": "Total Refund (₹)",
            "product_category": "Category"
        },
        title=f"<b>Product Return Risk Matrix (OQ-10) — Minimum Order Filter Applied</b>"
    )

    # Benchmark reference line
    fig.add_hline(
        y=benchmark_rate,
        line_dash="dash",
        line_color=COLOR_ACCENT,
        annotation_text=f"Benchmark Return Rate ({benchmark_rate:.1f}%)",
        annotation_position="bottom right"
    )

    fig.update_layout(
        **THEME_LAYOUT
    )
    fig.update_xaxes(gridcolor="#E2E8F0")
    fig.update_yaxes(gridcolor="#E2E8F0")
    return fig

def plot_refund_value_by_category(cat_df: pd.DataFrame) -> go.Figure:
    """
    OQ-07: Total Financial Refund Impact by Product Category
    """
    if cat_df.empty:
        return go.Figure()

    sorted_df = cat_df.sort_values('total_refund', ascending=True)

    fig = go.Figure(go.Bar(
        x=sorted_df['total_refund'],
        y=sorted_df['product_category'],
        orientation='h',
        marker=dict(
            color=sorted_df['total_refund'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Refund (₹)")
        ),
        text=[f"₹{v:,.0f}" for v in sorted_df['total_refund']],
        textposition='auto',
        hovertemplate="Category: %{y}<br>Total Refund: ₹%{x:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        title="<b>Total Refund Value by Category (OQ-07 Financial Impact)</b>",
        **THEME_LAYOUT
    )
    fig.update_xaxes(title_text="Total Refund Amount (₹)", gridcolor="#E2E8F0")
    fig.update_yaxes(title_text="Category")
    return fig
