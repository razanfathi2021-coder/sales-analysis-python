"""Sales data analysis: revenue trends, top products, monthly performance.
Usage: python generate_data.py  (once)  then  python analysis.py
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales_data.csv", parse_dates=["date"])

# --- Data cleaning ---
before = len(df)
df = df.dropna(subset=["product", "quantity", "unit_price"])
df = df[df["quantity"] > 0]
df = df[df["unit_price"] > 0]
df["total"] = (df["quantity"] * df["unit_price"]).round(2)
print(f"Cleaned: dropped {before - len(df)} bad rows -> {len(df)} rows")

# --- Monthly performance ---
df["month"] = df["date"].dt.to_period("M")
monthly = df.groupby("month").agg(orders=("order_id", "count"),
                                  revenue=("total", "sum"),
                                  units=("quantity", "sum")).reset_index()
print("\n=== Monthly performance ===")
print(monthly.to_string(index=False))

# --- Top products ---
top = df.groupby("product").agg(revenue=("total", "sum"),
                                units=("quantity", "sum")).sort_values("revenue", ascending=False)
print("\n=== Top products by revenue ===")
print(top.to_string())

# --- Chart 1: monthly revenue trend ---
fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(monthly["month"].astype(str), monthly["revenue"], color="#2E86AB")
ax.set_title("Monthly Revenue - Jan to Oct 2026")
ax.set_ylabel("Revenue (USD)")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig("chart_monthly_revenue.png", dpi=150)
plt.close()

# --- Chart 2: top products ---
fig, ax = plt.subplots(figsize=(9, 4))
ax.barh(top.index[::-1], top["revenue"].iloc[::-1], color="#A23B72")
ax.set_title("Top Products by Revenue")
ax.set_xlabel("Revenue (USD)")
plt.tight_layout()
plt.savefig("chart_top_products.png", dpi=150)
plt.close()

# --- Summary report ---
with open("report.txt", "w") as f:
    f.write("SALES ANALYSIS REPORT (Jan - Oct 2026)\n")
    f.write("=" * 45 + "\n")
    f.write(f"Total orders : {len(df)}\n")
    f.write(f"Total revenue: {df['total'].sum():,.2f} USD\n")
    f.write(f"Units sold   : {df['quantity'].sum()}\n")
    f.write(f"Customers    : {df['customer'].nunique()}\n")
    best = monthly.loc[monthly['revenue'].idxmax()]
    f.write(f"Best month   : {best['month']} ({best['revenue']:,.0f} USD)\n")
    f.write(f"Top product  : {top.index[0]} ({top['revenue'].iloc[0]:,.0f} USD)\n")
print("\nSaved: report.txt, chart_monthly_revenue.png, chart_top_products.png")
