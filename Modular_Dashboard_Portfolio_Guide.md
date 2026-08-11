# Blueprint: Modular Business Analytics Dashboard for Portfolio

A step-by-step technical guide to building and deploying a **modular, data-agnostic interactive dashboard** using **Python, Plotly Dash, `uv`, and PowerShell**, optimized for AI coding agents (**OpenCode** / **Google Antigravity**).

---

## Technical Stack & Architecture

- **Package & Environment Management:** `uv` (PowerShell native)
- **Framework:** Plotly Dash (`dash`, `dash-bootstrap-components`, `plotly`, `pandas`)
- **Architecture:** Schema-Agnostic Engine driven by `config.json`
- **Development Tooling:** OpenCode / Google Antigravity (Agentic AI-assisted development)

---

## 1. PowerShell Environment Setup with `uv`

Run these commands in PowerShell to establish a fast, isolated project environment:

```powershell
# Initialize a new project directory
uv init business-dashboard
cd business-dashboard

# Add core dependencies with exact locking
uv add dash pandas plotly dash-bootstrap-components pydantic

# Activate virtual environment in PowerShell
.\.venv\Scripts\Activate.ps1
```

---

## 2. Dynamic Schema Architecture (`config.json`)

To ensure the dashboard works across **any business dataset** without altering underlying application logic, define dataset mappings external to the codebase:

```json
{
  "dataset_path": "data/sales_data.csv",
  "mappings": {
    "date_column": "Order_Date",
    "category_column": "Product_Category",
    "region_column": "Region",
    "revenue_column": "Total_Sales",
    "units_column": "Quantity"
  },
  "dashboard_title": "Executive Enterprise Analytics Hub"
}
```

---

## 3. Modular Application Code (`app.py`)

This execution engine reads schema definitions from `config.json` dynamically and maps data into responsive UI controls and Plotly graphics.

```python
import json
from pathlib import Path
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

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
regions = df[mappings["region_column"]].dropna().unique().tolist()
categories = df[mappings["category_column"]].dropna().unique().tolist()

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
                        style={"color": "#000"}
                    )
                ], md=6),
                dbc.Col([
                    html.Label(f"Filter {mappings['category_column']}:"),
                    dcc.Dropdown(
                        id="category-filter",
                        options=[{"label": c, "value": c} for c in categories],
                        value=categories,
                        multi=True,
                        style={"color": "#000"}
                    )
                ], md=6),
            ])
        ])
    ], className="mb-4 shadow-sm"),

    # Dynamic KPI Summary Display
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Total Revenue", className="text-muted"),
            html.H3(id="kpi-revenue", className="text-success")
        ])), md=6),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Total Units / Orders", className="text-muted"),
            html.H3(id="kpi-volume", className="text-info")
        ])), md=6),
    ], className="mb-4"),

    # Charts Grid
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="time-trend-chart")])), md=8),
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="category-breakdown-chart")])), md=4),
    ])
], fluid=True)

# --- Interactive Callback Engine ---
@app.callback(
    [
        Output("kpi-revenue", "children"),
        Output("kpi-volume", "children"),
        Output("time-trend-chart", "figure"),
        Output("category-breakdown-chart", "figure"),
    ],
    [
        Input("region-filter", "value"),
        Input("category-filter", "value"),
    ]
)
def update_dashboard(selected_regions, selected_categories):
    reg_col = mappings["region_column"]
    cat_col = mappings["category_column"]
    rev_col = mappings["revenue_column"]
    units_col = mappings["units_column"]

    # Filter dataframe based on UI selections
    dff = df[
        (df[reg_col].isin(selected_regions or [])) & 
        (df[cat_col].isin(selected_categories or []))
    ]

    total_rev = dff[rev_col].sum() if not dff.empty else 0
    total_vol = dff[units_col].sum() if not dff.empty else 0

    # Line Chart Generation
    trend_df = dff.groupby(date_col)[rev_col].sum().reset_index()
    fig_line = px.line(
        trend_df, x=date_col, y=rev_col, 
        title=f"{rev_col} Over Time", template="plotly_dark"
    )

    # Donut Chart Generation
    cat_df = dff.groupby(cat_col)[rev_col].sum().reset_index()
    fig_pie = px.pie(
        cat_df, names=cat_col, values=rev_col, 
        title=f"{rev_col} by {cat_col}", template="plotly_dark", hole=0.4
    )

    return f"${total_rev:,.2f}", f"{total_vol:,}", fig_line, fig_pie

if __name__ == "__main__":
    app.run_server(debug=True)
```

---

## 4. Agentic Workflow (OpenCode & Google Antigravity)

1. **Auto-Refactoring via Agent Prompts:**
   - Prompt: *"Extend `app.py` to add an automatic CSV drag-and-drop uploader (`dcc.Upload`) that updates `config.json` dynamically upon file submission."*
2. **Autonomous Testing with Browser Agent (Antigravity):**
   - Point the Antigravity Browser Agent to `http://127.0.0.1:8050`.
   - Command the agent to verify multi-select dropdown behavior and assert chart responsiveness.

---

## 5. Benchmarking & Testing Datasets

Test this dynamic dashboard across different enterprise schemas by configuring `config.json` for each target dataset:

| Dataset | Schema Characteristics | Key Test Objective |
| :--- | :--- | :--- |
| **Retail Sales & Analytics** | `Sale_Date`, `Product_Category`, `Region`, `Sales_Amount`, `Quantity` | High-volume transaction stress testing and dynamic filtering speed. |
| **Online Marketplace Data** | `Date`, `Category`, `Region`, `Total Price`, `Quantity` | Multi-channel categorical breakdown & donut chart validation. |
| **Superstore Corporate Sales** | `Order Date`, `Category`, `Segment`, `Sales`, `Quantity` | Executive-level financial metric aggregations and formatting. |

---

## 6. Deployment Strategy

- **Local Showcase:** Embed a GIF or live web screen-recording in your GitHub README / portfolio.
- **Production Hosting:** Deploy using Docker or Render.com web service connected to your Git repository.
