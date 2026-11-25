
from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load Dataset
df = pd.read_csv("sales_data.csv")

# Convert Date
df['Order_Date'] = pd.to_datetime(
    df['Order_Date'],
    dayfirst=True,
    errors='coerce'
)

# Create Charts Folder
os.makedirs("static/charts", exist_ok=True)

# Dashboard Values
total_sales = df['Sales_INR'].sum()
total_profit = df['Profit_INR'].sum()
total_orders = df['Order_ID'].nunique()
total_customers = df['Customer_ID'].nunique()

# 1. Sales by Category - Bar Chart
category_sales = df.groupby('Category')['Sales_INR'].sum()

plt.figure(figsize=(8, 5))
category_sales.plot(kind='bar', color='steelblue')
plt.title('Sales by Category')
plt.xlabel('Category')
plt.ylabel('Sales (INR)')
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('static/charts/category_sales.png')
plt.close()

# 2. Monthly Sales - Line Chart
monthly_sales = df.groupby(
    df['Order_Date'].dt.month
)['Sales_INR'].sum()

plt.figure(figsize=(9, 5))
plt.plot(monthly_sales.index, monthly_sales.values,
         marker='o', linewidth=2)
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales (INR)')
plt.xticks(range(1, 13))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('static/charts/monthly_sales.png')
plt.close()

# 3. Sales by Region - Pie Chart
region_sales = df.groupby('Region')['Sales_INR'].sum()

plt.figure(figsize=(7, 5))
plt.pie(
    region_sales,
    labels=region_sales.index,
    autopct='%1.1f%%',
    startangle=90
)
plt.title('Sales Distribution by Region')
plt.tight_layout()
plt.savefig('static/charts/region_sales.png')
plt.close()

# 4. Top 10 Products - Bar Chart
top_products = (
    df.groupby('Product_ID')['Sales_INR']
    .sum()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(9, 5))
plt.barh(top_products.index.astype(str), top_products.values)
plt.title('Top 10 Products by Sales')
plt.xlabel('Sales (INR)')
plt.ylabel('Product ID')
plt.tight_layout()
plt.savefig('static/charts/top_products.png')
plt.close()

# 5. Monthly Profit - Line Chart
monthly_profit = df.groupby(
    df['Order_Date'].dt.month
)['Profit_INR'].sum()

plt.figure(figsize=(9, 5))
plt.plot(monthly_profit.index, monthly_profit.values,
         marker='o', linewidth=2)
plt.title('Monthly Profit Trend')
plt.xlabel('Month')
plt.ylabel('Profit (INR)')
plt.xticks(range(1, 13))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('static/charts/monthly_profit.png')
plt.close()

# 6. Sales by Channel - Bar Chart
channel_sales = df.groupby('Channel')['Sales_INR'].sum()

plt.figure(figsize=(8, 5))
channel_sales.plot(kind='bar', color='teal')
plt.title('Sales by Channel')
plt.xlabel('Channel')
plt.ylabel('Sales (INR)')
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig('static/charts/channel_sales.png')
plt.close()

# Flask Route
@app.route("/")
def home():

    table = df.head(100).to_html(
        index=False,
        classes="data-table",
        border=0
    )

    return render_template(
        "index.html",
        table=table,
        total_sales=total_sales,
        total_profit=total_profit,
        total_orders=total_orders,
        total_customers=total_customers,
        total_records=len(df)
    )

if __name__ == "__main__":
    app.run(debug=True)
