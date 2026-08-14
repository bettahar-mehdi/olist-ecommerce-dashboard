Markdown
# 📊 Olist E-Commerce Analytics Dashboard

Interactive business analytics dashboard built with Plotly Dash and standalone HTML/Plotly.js for executive decision-making.

[![Live Demo](https://img.shields.io/badge/Demo-Live_Dashboard-blue?style=for-the-badge&logo=googlechrome&logoColor=white)](https://bettahar-mehdi.github.io/olist-ecommerce-dashboard/)
[![Python](https://img.shields.io/badge/Python-3.11-green?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Plotly Dash](https://img.shields.io/badge/Dash-4.4.1-blue?style=flat-square&logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 🌐 Live Interactive Demo

Test the live client-side dashboard directly in your browser (no installation required):  
👉 **[Launch Live Dashboard](https://bettahar-mehdi.github.io/olist-ecommerce-dashboard/)**

---

## 🚀 Key Features

* **Real-Time Dynamic Filtering:** Filter instantly across 25+ Brazilian regions and 70+ product categories.
* **4 Executive KPI Cards:**
  * **Total Revenue:** Multi-year aggregate gross revenue.
  * **Total Orders:** Volume of fulfilled transactions.
  * **Average Order Value (AOV):** Basket size across categories.
  * **Customer Satisfaction:** Average review score distribution.
* **Comprehensive Visual Analytics:**
  * **Revenue Trends:** Multi-year monthly timeline tracking.
  * **Regional & Category Performance:** Geographic distribution and top category sales.
  * **Operational Dynamics:** Seasonality curves, day-of-week demand patterns, and payment method splits.
  * **Logistics & Margin Analysis:** Price vs. freight cost correlation scatter analysis.
* **Responsive Dark Theme:** Modern, high-contrast dark UI designed for scannability and presentation.

---

## 🛠️ Quick Start (Local Run)

### 1. Clone the Repository
```bash
git clone [https://github.com/bettahar-mehdi/olist-ecommerce-dashboard.git](https://github.com/bettahar-mehdi/olist-ecommerce-dashboard.git)
cd olist-ecommerce-dashboard
2. Environment Setup
Bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
3. Run Application
Bash
python app.py
Open http://127.0.0.1:8050 in your browser.

🐳 Docker Deployment
Option 1: Using Make
Bash
make deploy     # Build container and run in detached mode
make logs       # Inspect live server logs
make stop       # Stop running container
make clean      # Clean up unused images and containers
Option 2: Direct Docker Commands
Bash
# Build image
docker build -t olist-dashboard .

# Run container on port 8050
docker run -d --name olist-dashboard -p 8050:8050 olist-dashboard
Option 3: VPS Fresh Deploy
Bash
chmod +x deploy.sh
./deploy.sh
📁 Project Structure
Plaintext
.
├── index.html                 # Standalone dynamic dashboard (GitHub Pages)
├── app.py                     # Plotly Dash backend application
├── config.json                # Configuration & schema definitions
├── clean_and_combine.py       # Data cleaning & ETL pipeline
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker container specification
├── Makefile                   # Automation build commands
├── deploy.sh                  # Shell deployment script for VPS
├── data/                      # Raw and processed datasets
│   └── sales_data.csv
└── README.md
📦 Data Source
Based on the Olist Brazilian E-Commerce Dataset covering 100,000+ anonymized orders between 2016 and 2018 across Brazilian marketplaces.

📄 License
Distributed under the MIT License. See LICENSE for more information.
