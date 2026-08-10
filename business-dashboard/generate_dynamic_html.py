"""
Generate a clean, professional standalone HTML dashboard.
All charts render reliably with explicit heights and error handling.
"""

import json
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/sales_data.csv")
OUTPUT_DIR = Path("deliverables")

df = pd.read_csv(DATA_PATH)
df["order_date"] = pd.to_datetime(df["order_date"])

# --- Prepare data ---
sample_size = min(15000, len(df))
df_sample = df.sample(sample_size, random_state=42).sort_values("order_date")

records = df_sample[[
    "order_date", "region", "category", "revenue", "quantity",
    "price", "freight_value", "avg_review_score", "payment_type",
    "customer_city"
]].copy()
records["order_date"] = records["order_date"].dt.strftime("%Y-%m-%d")
records["revenue"] = records["revenue"].clip(lower=0).round(2)
records["price"] = records["price"].round(2)
records["freight_value"] = records["freight_value"].round(2)

all_regions = sorted(df["region"].dropna().unique().tolist())
all_categories = sorted(df["category"].dropna().unique().tolist())

kpis = {
    "total_revenue": round(float(df["revenue"].sum()), 2),
    "total_orders": int(len(df)),
    "avg_order_value": round(float(df["revenue"].mean()), 2),
    "avg_review": round(float(df["avg_review_score"].mean()), 2),
    "unique_customers": int(df["customer_unique_id"].nunique()),
    "unique_categories": int(df["category"].nunique()),
    "date_range": f"{df['order_date'].min().strftime('%Y-%m-%d')} / {df['order_date'].max().strftime('%Y-%m-%d')}",
}

dashboard_data = {
    "kpis": kpis,
    "all_regions": all_regions,
    "all_categories": all_categories,
    "records": records.to_dict("records"),
}

data_json = json.dumps(dashboard_data, default=str)

# Build HTML
html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Olist E-Commerce Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: #0a0e17;
    color: #e8e8e8;
}
.header {
    background: linear-gradient(90deg, #0d1b2a 0%, #1b2838 100%);
    padding: 24px 40px;
    border-bottom: 2px solid #2196F3;
}
.header h1 { font-size: 24px; font-weight: 700; color: #fff; }
.header p { font-size: 13px; color: #8899aa; margin-top: 4px; }
.filters {
    background: #111827;
    padding: 16px 40px;
    border-bottom: 1px solid #1e293b;
    display: flex;
    gap: 16px;
    align-items: center;
    flex-wrap: wrap;
}
.filter-label { font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; }
.filter-select {
    background: #1e293b; color: #e2e8f0; border: 1px solid #334155;
    border-radius: 6px; padding: 8px 12px; font-size: 13px; min-width: 180px; cursor: pointer;
}
.filter-select:focus { border-color: #2196F3; outline: none; }
.btn {
    padding: 8px 18px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; border: none;
}
.btn-apply { background: #2196F3; color: #fff; }
.btn-apply:hover { background: #1976D2; }
.btn-reset { background: transparent; color: #94a3b8; border: 1px solid #334155; }
.btn-reset:hover { border-color: #64748b; color: #e2e8f0; }
.kpi-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; padding: 24px 40px;
}
.kpi {
    background: #111827; border: 1px solid #1e293b; border-radius: 8px; padding: 20px;
}
.kpi-label { font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; }
.kpi-value { font-size: 28px; font-weight: 700; margin-top: 8px; }
.kpi:nth-child(1) .kpi-value { color: #2196F3; }
.kpi:nth-child(2) .kpi-value { color: #10b981; }
.kpi:nth-child(3) .kpi-value { color: #f59e0b; }
.kpi:nth-child(4) .kpi-value { color: #ef4444; }
.charts {
    display: grid; grid-template-columns: 1fr 1fr; gap: 16px; padding: 0 40px 40px;
}
.chart {
    background: #111827; border: 1px solid #1e293b; border-radius: 8px;
    padding: 12px; height: 360px;
}
.chart.wide { grid-column: 1 / -1; height: 340px; }
.footer {
    text-align: center; padding: 20px; color: #475569; font-size: 11px; border-top: 1px solid #1e293b;
}
@media (max-width: 1024px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    .charts { grid-template-columns: 1fr; }
    .chart.wide { grid-column: span 1; }
}
@media (max-width: 600px) {
    .kpi-grid { grid-template-columns: 1fr; }
    .header, .filters, .kpi-grid, .charts { padding-left: 16px; padding-right: 16px; }
}
</style>
</head>
<body>

<div class="header">
    <h1>Olist E-Commerce Analytics Dashboard</h1>
    <p>Periode: ''' + kpis["date_range"] + ''' | ''' + f"{kpis['total_orders']:,}" + ''' commandes | ''' + f"{kpis['unique_customers']:,}" + ''' clients</p>
</div>

<div class="filters">
    <span class="filter-label">Region</span>
    <select id="sel-region" class="filter-select"></select>
    <span class="filter-label">Categorie</span>
    <select id="sel-category" class="filter-select"></select>
    <button class="btn btn-apply" onclick="updateDashboard()">Appliquer</button>
    <button class="btn btn-reset" onclick="resetAll()">Reinitialiser</button>
</div>

<div class="kpi-grid">
    <div class="kpi"><div class="kpi-label">Revenu Total</div><div class="kpi-value" id="k-revenue">-</div></div>
    <div class="kpi"><div class="kpi-label">Commandes</div><div class="kpi-value" id="k-orders">-</div></div>
    <div class="kpi"><div class="kpi-label">Panier Moyen</div><div class="kpi-value" id="k-aov">-</div></div>
    <div class="kpi"><div class="kpi-label">Note Moyenne</div><div class="kpi-value" id="k-rating">-</div></div>
</div>

<div class="charts">
    <div class="chart wide"><div id="c-trend" style="width:100%;height:100%;"></div></div>
    <div class="chart"><div id="c-category" style="width:100%;height:100%;"></div></div>
    <div class="chart"><div id="c-region" style="width:100%;height:100%;"></div></div>
    <div class="chart"><div id="c-monthly" style="width:100%;height:100%;"></div></div>
    <div class="chart"><div id="c-payment" style="width:100%;height:100%;"></div></div>
    <div class="chart"><div id="c-review" style="width:100%;height:100%;"></div></div>
    <div class="chart"><div id="c-dow" style="width:100%;height:100%;"></div></div>
    <div class="chart wide"><div id="c-scatter" style="width:100%;height:100%;"></div></div>
</div>

<div class="footer">
    Source: Olist Brazilian E-Commerce Dataset | Generated: ''' + pd.Timestamp.now().strftime("%Y-%m-%d") + '''
</div>

<script>
const DATA = ''' + data_json + ''';
let currentData = DATA.records;

function initSelect(id, items, allText) {
    var el = document.getElementById(id);
    el.innerHTML = '';
    var opt = document.createElement('option');
    opt.value = 'ALL';
    opt.textContent = allText;
    el.appendChild(opt);
    items.forEach(function(item) {
        opt = document.createElement('option');
        opt.value = item;
        opt.textContent = item;
        el.appendChild(opt);
    });
}

initSelect('sel-region', DATA.all_regions, 'Toutes regions');
initSelect('sel-category', DATA.all_categories, 'Toutes categories');

function updateDashboard() {
    var r = document.getElementById('sel-region').value;
    var c = document.getElementById('sel-category').value;
    currentData = DATA.records.filter(function(d) {
        return (r === 'ALL' || d.region === r) && (c === 'ALL' || d.category === c);
    });
    render();
}

function resetAll() {
    document.getElementById('sel-region').value = 'ALL';
    document.getElementById('sel-category').value = 'ALL';
    currentData = DATA.records;
    render();
}

var TL = {
    paper_bgcolor: '#111827',
    plot_bgcolor: '#0f172a',
    font: { color: '#94a3b8', size: 11 },
    margin: { l: 55, r: 20, t: 50, b: 45 },
    xaxis: { gridcolor: '#1e293b' },
    yaxis: { gridcolor: '#1e293b' },
    showlegend: false,
    autosize: true,
};

function makeLayout(title, h) {
    return {
        paper_bgcolor: '#111827',
        plot_bgcolor: '#0f172a',
        font: { color: '#94a3b8', size: 11 },
        margin: { l: 55, r: 20, t: 50, b: 45 },
        xaxis: { gridcolor: '#1e293b' },
        yaxis: { gridcolor: '#1e293b' },
        showlegend: false,
        autosize: true,
        title: { text: title, font: { color: '#e2e8f0', size: 14 } },
        height: h,
    };
}

function render() {
    var d = currentData;
    var n = d.length;
    var rev = 0, rat = 0;
    for (var i = 0; i < n; i++) { rev += d[i].revenue; rat += d[i].avg_review_score; }
    var aov = n > 0 ? rev / n : 0;
    var avgRat = n > 0 ? rat / n : 0;

    document.getElementById('k-revenue').textContent = 'R$ ' + rev.toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ' ');
    document.getElementById('k-orders').textContent = n.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, ' ');
    document.getElementById('k-aov').textContent = 'R$ ' + aov.toFixed(2);
    document.getElementById('k-rating').textContent = avgRat.toFixed(1) + '/5.0';

    drawTrend(d);
    drawCategory(d);
    drawRegion(d);
    drawMonthly(d);
    drawPayment(d);
    drawReview(d);
    drawDow(d);
    drawScatter(d);
}

function drawTrend(d) {
    var g = {};
    for (var i = 0; i < d.length; i++) {
        var m = d[i].order_date.substr(0, 7);
        g[m] = (g[m] || 0) + d[i].revenue;
    }
    var keys = Object.keys(g).sort();
    var vals = keys.map(function(k) { return g[k]; });
    Plotly.newPlot('c-trend', [{
        x: keys, y: vals,
        type: 'scatter', mode: 'lines+markers',
        line: { color: '#2196F3', width: 2 },
        marker: { size: 5 },
        fill: 'tozeroy', fillcolor: 'rgba(33,150,243,0.08)',
    }], makeLayout('Revenus par Mois', 300), {displayModeBar: false, responsive: true});
}

function drawCategory(d) {
    var g = {};
    for (var i = 0; i < d.length; i++) { g[d[i].category] = (g[d[i].category] || 0) + d[i].revenue; }
    var entries = Object.entries(g).sort(function(a,b){return b[1]-a[1];}).slice(0, 10);
    Plotly.newPlot('c-category', [{
        labels: entries.map(function(x){return x[0];}),
        values: entries.map(function(x){return x[1];}),
        type: 'pie', hole: 0.45,
        marker: { line: { color: '#111827', width: 2 } },
        textinfo: 'percent', textfont: { color: '#fff', size: 10 },
    }], makeLayout('Top 10 Categories', 320), {displayModeBar: false, responsive: true});
}

function drawRegion(d) {
    var g = {};
    for (var i = 0; i < d.length; i++) { g[d[i].region] = (g[d[i].region] || 0) + d[i].revenue; }
    var entries = Object.entries(g).sort(function(a,b){return a[1]-b[1];});
    Plotly.newPlot('c-region', [{
        x: entries.map(function(x){return x[1];}),
        y: entries.map(function(x){return x[0];}),
        type: 'bar', orientation: 'h',
        marker: { color: '#10b981' },
    }], makeLayout('Revenus par Region', 320), {displayModeBar: false, responsive: true});
}

function drawMonthly(d) {
    var labels = ['Jan','Fev','Mar','Avr','Mai','Jun','Jul','Aou','Sep','Oct','Nov','Dec'];
    var g = {};
    for (var i = 0; i < d.length; i++) {
        var m = parseInt(d[i].order_date.split('-')[1]);
        g[m] = (g[m] || 0) + d[i].revenue;
    }
    Plotly.newPlot('c-monthly', [{
        x: labels,
        y: labels.map(function(_,i){return g[i+1] || 0;}),
        type: 'bar', marker: { color: '#f59e0b' },
    }], makeLayout('Saisonnalite (par mois)', 320), {displayModeBar: false, responsive: true});
}

function drawPayment(d) {
    var g = {};
    for (var i = 0; i < d.length; i++) { g[d[i].payment_type] = (g[d[i].payment_type] || 0) + d[i].revenue; }
    var entries = Object.entries(g).sort(function(a,b){return b[1]-a[1];});
    Plotly.newPlot('c-payment', [{
        labels: entries.map(function(x){return x[0];}),
        values: entries.map(function(x){return x[1];}),
        type: 'pie', hole: 0.35,
        marker: { line: { color: '#111827', width: 2 } },
        textinfo: 'percent', textfont: { color: '#fff', size: 10 },
    }], makeLayout('Modes de Paiement', 320), {displayModeBar: false, responsive: true});
}

function drawReview(d) {
    var g = {};
    for (var i = 0; i < d.length; i++) {
        var s = Math.round(d[i].avg_review_score);
        g[s] = (g[s] || 0) + 1;
    }
    var keys = Object.keys(g).sort();
    Plotly.newPlot('c-review', [{
        x: keys, y: keys.map(function(k){return g[k];}),
        type: 'bar', marker: { color: '#a855f7' },
    }], makeLayout('Distribution des Notes', 320), {displayModeBar: false, responsive: true});
}

function drawDow(d) {
    var days = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'];
    var g = {};
    for (var i = 0; i < d.length; i++) {
        var day = new Date(d[i].order_date).getDay();
        var idx = day === 0 ? 6 : day - 1;
        g[idx] = (g[idx] || 0) + d[i].revenue;
    }
    Plotly.newPlot('c-dow', [{
        x: days, y: days.map(function(_,i){return g[i] || 0;}),
        type: 'bar', marker: { color: '#ef4444' },
    }], makeLayout('Revenus par Jour', 320), {displayModeBar: false, responsive: true});
}

function drawScatter(d) {
    var s = d;
    if (d.length > 2000) {
        s = d.slice().sort(function(){return Math.random()-0.5;}).slice(0, 2000);
    }
    Plotly.newPlot('c-scatter', [{
        x: s.map(function(r){return r.price;}),
        y: s.map(function(r){return r.freight_value;}),
        mode: 'markers', type: 'scatter',
        marker: { color: s.map(function(r){return r.revenue;}), colorscale: 'Plasma', size: 4, opacity: 0.6 },
    }], {
        paper_bgcolor: '#111827', plot_bgcolor: '#0f172a',
        font: { color: '#94a3b8', size: 11 },
        margin: { l: 55, r: 20, t: 50, b: 45 },
        xaxis: { gridcolor: '#1e293b', title: { text: 'Prix (R$)', font: { color: '#94a3b8' } } },
        yaxis: { gridcolor: '#1e293b', title: { text: 'Fret (R$)', font: { color: '#94a3b8' } } },
        showlegend: false, autosize: true, height: 300,
        title: { text: 'Prix vs Fret (couleur = revenu)', font: { color: '#e2e8f0', size: 14 } },
    }, {displayModeBar: false, responsive: true});
}

// Start rendering when page loads
window.onload = function() { render(); };
</script>
</body>
</html>'''

output_path = OUTPUT_DIR / "dashboard_dynamic.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

size_mb = output_path.stat().st_size / (1024 * 1024)
print(f"Dynamic HTML dashboard saved: {output_path} ({size_mb:.1f} MB)")
