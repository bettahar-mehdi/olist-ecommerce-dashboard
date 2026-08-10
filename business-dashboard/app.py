import json
from pathlib import Path
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Load Configuration & Dataset ---
CONFIG_PATH = Path("config.json")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


config = load_config()
mappings = config["mappings"]

# Load target dataset dynamically
df = pd.read_csv(config["dataset_path"])

# Standardize date format
date_col = mappings["date_column"]
df[date_col] = pd.to_datetime(df[date_col])

# --- App Initialization ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = config["dashboard_title"]

# Unique dropdown filter options
regions = sorted(df[mappings["region_column"]].dropna().unique().tolist())
categories = sorted(df[mappings["category_column"]].dropna().unique().tolist())

# --- Responsive UI Layout ---
app.layout = dbc.Container([
    html.H2(config["dashboard_title"], className="my-4 text-primary text-left"),

    # Dynamic Filter Controls Card
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label(f"Filter {mappings['region_column']}:"),
                    dcc.Dropdown(
                        id="region-filter",
                        options=[{"label": r, "value": r} for r in regions],
                        value=regions,
                        multi=True,
                        style={"color": "#000"},
                    ),
                ], md=6),
                dbc.Col([
                    html.Label(f"Filter {mappings['category_column']}:"),
                    dcc.Dropdown(
                        id="category-filter",
                        options=[{"label": c, "value": c} for c in categories],
                        value=categories[:20],
                        multi=True,
                        style={"color": "#000"},
                    ),
                ], md=6),
            ])
        ])
    ], className="mb-4 shadow-sm"),

    # Dynamic KPI Summary Display
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Total Revenue", className="text-muted"),
            html.H3(id="kpi-revenue", className="text-success"),
        ])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Total Orders", className="text-muted"),
            html.H3(id="kpi-orders", className="text-info"),
        ])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Avg Review Score", className="text-muted"),
            html.H3(id="kpi-rating", className="text-warning"),
        ])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Avg Order Value", className="text-muted"),
            html.H3(id="kpi-aov", className="text-danger"),
        ])), md=3),
    ], className="mb-4"),

    # Charts Row 1
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="time-trend-chart")])), md=8),
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="category-breakdown-chart")])), md=4),
    ], className="mb-4"),

    # Charts Row 2
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="region-bar-chart")])), md=6),
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="monthly-trend-chart")])), md=6),
    ], className="mb-4"),

    # Charts Row 3 - NEW
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="payment-type-chart")])), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="review-score-chart")])), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="freight-vs-price-chart")])), md=4),
    ], className="mb-4"),

    # Charts Row 4 - NEW
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="top-cities-chart")])), md=6),
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="day-of-week-chart")])), md=6),
    ], className="mb-4"),

    # Charts Row 5 - NEW
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="category-heatmap-chart")])), md=12),
    ], className="mb-4"),

], fluid=True)


# --- Interactive Callback Engine ---
@app.callback(
    [
        Output("kpi-revenue", "children"),
        Output("kpi-orders", "children"),
        Output("kpi-rating", "children"),
        Output("kpi-aov", "children"),
        Output("time-trend-chart", "figure"),
        Output("category-breakdown-chart", "figure"),
        Output("region-bar-chart", "figure"),
        Output("monthly-trend-chart", "figure"),
        Output("payment-type-chart", "figure"),
        Output("review-score-chart", "figure"),
        Output("freight-vs-price-chart", "figure"),
        Output("top-cities-chart", "figure"),
        Output("day-of-week-chart", "figure"),
        Output("category-heatmap-chart", "figure"),
    ],
    [
        Input("region-filter", "value"),
        Input("category-filter", "value"),
    ],
)
def update_dashboard(selected_regions, selected_categories):
    reg_col = mappings["region_column"]
    cat_col = mappings["category_column"]
    rev_col = mappings["revenue_column"]
    units_col = mappings["units_column"]

    # Filter dataframe based on UI selections
    dff = df[
        (df[reg_col].isin(selected_regions or []))
        & (df[cat_col].isin(selected_categories or []))
    ]

    total_rev = dff[rev_col].sum() if not dff.empty else 0
    total_orders = dff[units_col].sum() if not dff.empty else 0
    avg_rating = dff["avg_review_score"].mean() if not dff.empty else 0
    aov = total_rev / total_orders if total_orders > 0 else 0

    # --- Time Trend Line Chart ---
    trend_df = dff.groupby(date_col)[rev_col].sum().reset_index()
    fig_line = px.line(
        trend_df,
        x=date_col,
        y=rev_col,
        title="Revenue Over Time",
        template="plotly_dark",
    )
    fig_line.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # --- Category Donut Chart ---
    cat_df = dff.groupby(cat_col)[rev_col].sum().reset_index().nlargest(10, rev_col)
    fig_pie = px.pie(
        cat_df,
        names=cat_col,
        values=rev_col,
        title="Top 10 Categories by Revenue",
        template="plotly_dark",
        hole=0.4,
    )
    fig_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # --- Region Bar Chart ---
    reg_df = dff.groupby(reg_col)[rev_col].sum().reset_index().sort_values(rev_col, ascending=True)
    fig_bar = px.bar(
        reg_df,
        x=rev_col,
        y=reg_col,
        title="Revenue by Region (State)",
        template="plotly_dark",
        orientation="h",
    )
    fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # --- Monthly Trend ---
    monthly_df = dff.groupby(dff[date_col].dt.to_period("M").astype(str))[rev_col].sum().reset_index()
    monthly_df.columns = ["month", rev_col]
    fig_monthly = px.bar(
        monthly_df,
        x="month",
        y=rev_col,
        title="Monthly Revenue Trend",
        template="plotly_dark",
    )
    fig_monthly.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # --- Payment Type Distribution (NEW) ---
    pay_df = dff.groupby("payment_type")[rev_col].sum().reset_index()
    fig_payment = px.pie(
        pay_df,
        names="payment_type",
        values=rev_col,
        title="Revenue by Payment Type",
        template="plotly_dark",
        hole=0.3,
    )
    fig_payment.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # --- Review Score Distribution (NEW) ---
    review_df = dff.groupby("avg_review_score")[units_col].sum().reset_index()
    review_df["avg_review_score"] = review_df["avg_review_score"].round(0).astype(int)
    review_agg = review_df.groupby("avg_review_score")[units_col].sum().reset_index()
    fig_review = px.bar(
        review_agg,
        x="avg_review_score",
        y=units_col,
        title="Orders by Review Score",
        template="plotly_dark",
        color=units_col,
        color_continuous_scale="Viridis",
    )
    fig_review.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # --- Freight vs Price Scatter (NEW) ---
    sample = dff.sample(min(5000, len(dff))) if len(dff) > 5000 else dff
    fig_scatter = px.scatter(
        sample,
        x="price",
        y="freight_value",
        color=cat_col,
        size=rev_col,
        title="Freight Cost vs Product Price",
        template="plotly_dark",
        opacity=0.6,
        color_continuous_scale="Plasma",
    )
    fig_scatter.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # --- Top Cities Chart (NEW) ---
    city_df = dff.groupby("customer_city")[rev_col].sum().reset_index().nlargest(15, rev_col)
    fig_cities = px.bar(
        city_df.sort_values(rev_col, ascending=True),
        x=rev_col,
        y="customer_city",
        title="Top 15 Cities by Revenue",
        template="plotly_dark",
        orientation="h",
        color=rev_col,
        color_continuous_scale="Tealgrn",
    )
    fig_cities.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # --- Day of Week Chart (NEW) ---
    dff_copy = dff.copy()
    dff_copy["day_of_week"] = dff_copy[date_col].dt.day_name()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow_df = dff_copy.groupby("day_of_week")[rev_col].sum().reindex(day_order).reset_index()
    fig_dow = px.bar(
        dow_df,
        x="day_of_week",
        y=rev_col,
        title="Revenue by Day of Week",
        template="plotly_dark",
        color=rev_col,
        color_continuous_scale="Blues",
    )
    fig_dow.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # --- Category-Region Heatmap (NEW) ---
    heatmap_df = dff.groupby([reg_col, cat_col])[rev_col].sum().reset_index()
    top_cats = dff.groupby(cat_col)[rev_col].sum().nlargest(10).index.tolist()
    top_regs = dff.groupby(reg_col)[rev_col].sum().nlargest(10).index.tolist()
    heatmap_filtered = heatmap_df[
        heatmap_df[cat_col].isin(top_cats) & heatmap_df[reg_col].isin(top_regs)
    ]
    heatmap_pivot = heatmap_filtered.pivot_table(
        index=reg_col, columns=cat_col, values=rev_col, fill_value=0
    )
    fig_heatmap = px.imshow(
        heatmap_pivot,
        title="Revenue Heatmap: Region x Category",
        template="plotly_dark",
        aspect="auto",
        color_continuous_scale="YlOrRd",
    )
    fig_heatmap.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    return (
        f"R$ {total_rev:,.2f}",
        f"{total_orders:,}",
        f"{avg_rating:.1f} / 5.0",
        f"R$ {aov:,.2f}",
        fig_line,
        fig_pie,
        fig_bar,
        fig_monthly,
        fig_payment,
        fig_review,
        fig_scatter,
        fig_cities,
        fig_dow,
        fig_heatmap,
    )


if __name__ == "__main__":
    app.run(debug=True)
