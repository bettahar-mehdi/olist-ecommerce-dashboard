"""
Data Cleaning & Combining Script for Olist E-Commerce Dataset
Combines all 7 CSV files into a single unified dataset for dashboard consumption.
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(r"D:\dashbord")
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

print("=== Loading datasets ===")

# Load all datasets
customers = pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")
geolocation = pd.read_csv(DATA_DIR / "olist_geolocation_dataset.csv")
orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
order_payments = pd.read_csv(DATA_DIR / "olist_order_payments_dataset.csv")
order_reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")

print(f"Customers: {customers.shape}")
print(f"Geolocation: {geolocation.shape}")
print(f"Orders: {orders.shape}")
print(f"Order Items: {order_items.shape}")
print(f"Order Payments: {order_payments.shape}")
print(f"Order Reviews: {order_reviews.shape}")
print(f"Products: {products.shape}")

print("\n=== Cleaning datasets ===")

# --- Customers ---
# Remove duplicates on customer_unique_id to get unique customers
customers = customers.drop_duplicates(subset=["customer_unique_id"], keep="first")

# --- Geolocation ---
# Average lat/lng per zip code to get one row per location
geolocation = (
    geolocation
    .groupby("geolocation_zip_code_prefix", as_index=False)
    .agg(
        geolocation_lat=("geolocation_lat", "mean"),
        geolocation_lng=("geolocation_lng", "mean"),
        geolocation_city=("geolocation_city", "first"),
        geolocation_state=("geolocation_state", "first"),
    )
)

# --- Orders ---
# Convert date columns
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

# Keep only delivered orders for meaningful analysis
orders = orders[orders["order_status"] == "delivered"].copy()

# Remove rows with missing purchase timestamp
orders = orders.dropna(subset=["order_purchase_timestamp"])

# --- Order Items ---
# Calculate total value (price + freight)
order_items["total_item_value"] = order_items["price"] + order_items["freight_value"]

# --- Order Payments ---
# Aggregate payments per order (sum of payment_value gives total paid)
payments_agg = (
    order_payments
    .groupby("order_id", as_index=False)
    .agg(
        total_payment=("payment_value", "sum"),
        payment_type=("payment_type", "first"),
        max_installments=("payment_installments", "max"),
    )
)

# --- Order Reviews ---
# Get the latest review per order (in case of multiple reviews)
reviews_agg = (
    order_reviews
    .sort_values("review_creation_date")
    .groupby("order_id", as_index=False)
    .agg(
        avg_review_score=("review_score", "mean"),
        review_count=("review_id", "count"),
    )
)

# --- Products ---
# Rename for clarity
products = products.rename(columns={"product_category_name": "product_category"})

print("\n=== Merging datasets ===")

# Start with order_items as the base (one row per item in an order)
df = order_items.merge(orders, on="order_id", how="inner")
print(f"After merging orders: {df.shape}")

# Merge with customers
df = df.merge(
    customers[["customer_id", "customer_unique_id", "customer_state", "customer_city", "customer_zip_code_prefix"]],
    on="customer_id",
    how="left",
)
print(f"After merging customers: {df.shape}")

# Merge with products
df = df.merge(
    products[["product_id", "product_category", "product_weight_g", "product_photos_qty"]],
    on="product_id",
    how="left",
)
print(f"After merging products: {df.shape}")

# Merge with aggregated payments
df = df.merge(payments_agg, on="order_id", how="left")
print(f"After merging payments: {df.shape}")

# Merge with aggregated reviews
df = df.merge(reviews_agg, on="order_id", how="left")
print(f"After merging reviews: {df.shape}")

# Merge with geolocation for customer location
df = df.merge(
    geolocation.rename(columns={"geolocation_zip_code_prefix": "customer_zip_code_prefix"}),
    on="customer_zip_code_prefix",
    how="left",
)
print(f"After merging geolocation: {df.shape}")

print("\n=== Final cleaning ===")

# Fill missing product_category with "Unknown"
df["product_category"] = df["product_category"].fillna("Unknown")

# Fill missing review scores with median
df["avg_review_score"] = df["avg_review_score"].fillna(df["avg_review_score"].median())

# Use total_payment as revenue (fallback to total_item_value)
df["revenue"] = df["total_payment"].fillna(df["total_item_value"])

# Create quantity column (each item row = 1 unit)
df["quantity"] = 1

# Extract date components for analysis
df["order_date"] = df["order_purchase_timestamp"].dt.date
df["order_year"] = df["order_purchase_timestamp"].dt.year
df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
df["order_week"] = df["order_purchase_timestamp"].dt.isocalendar().week.astype(int)

# Rename state to region for dashboard mapping
df = df.rename(columns={"customer_state": "region", "product_category": "category"})

# Select and reorder final columns
final_columns = [
    "order_id",
    "order_date",
    "order_year",
    "order_month",
    "order_week",
    "region",
    "customer_city",
    "geolocation_lat",
    "geolocation_lng",
    "category",
    "revenue",
    "quantity",
    "price",
    "freight_value",
    "total_item_value",
    "total_payment",
    "payment_type",
    "max_installments",
    "avg_review_score",
    "review_count",
    "product_weight_g",
    "product_photos_qty",
    "customer_unique_id",
    "product_id",
    "seller_id",
]

df = df[[col for col in final_columns if col in df.columns]]

# Final deduplication
df = df.drop_duplicates()

print(f"\nFinal dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"\nDate range: {df['order_date'].min()} to {df['order_date'].max()}")
print(f"Unique regions: {df['region'].nunique()}")
print(f"Unique categories: {df['category'].nunique()}")
print(f"Total revenue: R$ {df['revenue'].sum():,.2f}")

# Save to CSV
output_path = OUTPUT_DIR / "sales_data.csv"
df.to_csv(output_path, index=False)
print(f"\n=== Saved combined dataset to: {output_path} ===")
