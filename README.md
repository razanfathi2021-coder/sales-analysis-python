# Sales Data Analysis - Python (Pandas & Matplotlib)

Analysis of 1,300+ sales orders (Jan - Oct 2026): revenue trends,
top products, and monthly performance, with a written summary report.

## Run
```bash
pip install pandas matplotlib numpy
python generate_data.py   # creates sales_data.csv (synthetic sample data)
python analysis.py        # prints stats + saves charts and report.txt
```

## Outputs
- `sales_data.csv` - raw dataset (order id, date, customer, product, qty, price, total)
- `report.txt` - summary report (totals, best month, top product)
- `chart_monthly_revenue.png` - monthly revenue bar chart
- `chart_top_products.png` - top products bar chart
