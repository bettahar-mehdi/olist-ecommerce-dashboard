# Olist E-Commerce Analytics Dashboard

Interactive business analytics dashboard built with Plotly Dash, deployed with Docker.

![Dashboard](https://img.shields.io/badge/Dash-4.4.1-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **4 KPI Cards**: Total Revenue, Total Orders, Avg Review Score, Avg Order Value
- **9 Interactive Charts**: Time Trend, Category Breakdown, Region Bar, Monthly Trend, Payment Type, Review Score, Freight vs Price, Top Cities, Day of Week, Heatmap
- **Dynamic Filters**: Multi-select dropdowns for Region and Category
- **Dark Theme**: CYBORG Bootstrap theme with Plotly dark templates

## Quick Start (Local)

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/olist-dashboard.git
cd olist-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run dashboard
python app.py
```

Open http://127.0.0.1:8050

## Docker Deployment

### Option 1: Using Make
```bash
make deploy    # Build and run
make logs      # View logs
make stop      # Stop container
make clean     # Remove everything
```

### Option 2: Manual Docker
```bash
docker build -t olist-dashboard .
docker run -d --name olist-dashboard -p 8050:8050 olist-dashboard
```

### Option 3: VPS Fresh Deploy
```bash
chmod +x deploy.sh
./deploy.sh
```

## Project Structure

```
.
├── app.py                 # Main Dash application
├── config.json            # Schema configuration
├── clean_and_combine.py   # Data cleaning script
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image definition
├── Makefile               # Build commands
├── deploy.sh              # VPS deployment script
├── data/
│   └── sales_data.csv     # Combined dataset
└── README.md
```

## Data Source

[Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-e-commerce) — 100K+ orders from 2016-2018.

## License

MIT
