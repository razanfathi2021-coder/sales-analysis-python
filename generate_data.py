"""Generate a synthetic sales dataset: 1,300+ orders, Jan-Oct 2026."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

PRODUCTS = [
    ("Rice 10kg", "Food", 22.0),
    ("Cooking Oil 5L", "Food", 18.5),
    ("Milk Powder 900g", "Food", 14.0),
    ("Sugar 5kg", "Food", 9.5),
    ("Tea 400g", "Beverages", 7.0),
    ("Coffee 500g", "Beverages", 16.0),
    ("Detergent 3kg", "Household", 11.0),
    ("Biscuits Box", "Snacks", 5.5),
]
CUSTOMERS = [f"Cust-{i:02d}" for i in range(1, 33)]  # 32 regular customers

rows = []
order_id = 1001
dates = pd.date_range("2026-01-01", "2026-10-31", freq="D")
for d in dates:
    # slight upward trend + weekly seasonality (weekend spike)
    lam = 3.6 + 0.16 * d.month + (1.2 if d.dayofweek >= 4 else 0)
    n = rng.poisson(lam)
    for _ in range(n):
        name, cat, price = PRODUCTS[rng.integers(len(PRODUCTS))]
        qty = int(rng.integers(1, 15))
        unit = round(price * (1 + rng.normal(0, 0.04)), 2)
        rows.append({
            "order_id": order_id,
            "date": d.date().isoformat(),
            "customer": CUSTOMERS[rng.integers(len(CUSTOMERS))],
            "product": name,
            "category": cat,
            "quantity": qty,
            "unit_price": unit,
            "total": round(qty * unit, 2),
        })
        order_id += 1

df = pd.DataFrame(rows)
df.to_csv("sales_data.csv", index=False)
print(f"Rows: {len(df)} | Period: {df['date'].min()} -> {df['date'].max()}")
print(f"Total revenue: {df['total'].sum():,.0f}")
