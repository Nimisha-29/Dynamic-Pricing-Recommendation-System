import pandas as pd

# ---------------------------------------------------------
# 1. LOAD DATASET
# ---------------------------------------------------------

file_path = "data/bakery_dataset.csv"

df = pd.read_csv(file_path)

print("==========================================")
print("BAKERY DATASET ANALYSIS")
print("==========================================")


# ---------------------------------------------------------
# 2. BASIC INFORMATION
# ---------------------------------------------------------

print("\n--- BASIC INFORMATION ---")

print(f"Rows       : {len(df)}")
print(f"Columns    : {len(df.columns)}")
print(f"Products   : {df['product_id'].nunique()}")
print(f"Date range : {df['date'].min()} to {df['date'].max()}")


# ---------------------------------------------------------
# 3. NUMERICAL STATISTICS
# ---------------------------------------------------------

print("\n--- NUMERICAL SUMMARY ---")

numerical_columns = [
    "cost_price",
    "current_price",
    "competitor_price",
    "opening_stock",
    "units_sold",
    "closing_stock",
    "discount_percentage",
    "sales_revenue",
    "base_price"
]

print(df[numerical_columns].describe().round(2))


# ---------------------------------------------------------
# 4. DEMAND DISTRIBUTION
# ---------------------------------------------------------

print("\n--- DEMAND DISTRIBUTION ---")

demand_counts = df["demand_level"].value_counts()

print(demand_counts)

print("\nDemand percentages:")

demand_percentages = (
    df["demand_level"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(demand_percentages)


# ---------------------------------------------------------
# 5. SALES BY PRODUCT
# ---------------------------------------------------------

print("\n--- SALES BY PRODUCT ---")

product_sales = (
    df.groupby(["product_id", "product_name"])["units_sold"]
    .sum()
    .sort_values(ascending=False)
)

print(product_sales)


# ---------------------------------------------------------
# 6. REVENUE BY PRODUCT
# ---------------------------------------------------------

print("\n--- REVENUE BY PRODUCT ---")

product_revenue = (
    df.groupby(["product_id", "product_name"])["sales_revenue"]
    .sum()
    .sort_values(ascending=False)
)

print(product_revenue.round(2))


# ---------------------------------------------------------
# 7. AVERAGE PRICE BY PRODUCT
# ---------------------------------------------------------

print("\n--- AVERAGE PRICES ---")

average_prices = (
    df.groupby("product_name")[["current_price", "base_price"]]
    .mean()
    .sort_values("base_price", ascending=False)
)

print(average_prices.round(2))


# ---------------------------------------------------------
# 8. DEMAND VS SALES
# ---------------------------------------------------------

print("\n--- DEMAND VS AVERAGE SALES ---")

demand_sales = (
    df.groupby("demand_level")
    .agg(
        average_units_sold=("units_sold", "mean"),
        average_closing_stock=("closing_stock", "mean"),
        average_base_price=("base_price", "mean")
    )
    .round(2)
)

print(demand_sales)


# ---------------------------------------------------------
# 9. SEASONAL ANALYSIS
# ---------------------------------------------------------

print("\n--- SEASONAL ANALYSIS ---")

season_analysis = (
    df.groupby("season")
    .agg(
        average_units_sold=("units_sold", "mean"),
        average_revenue=("sales_revenue", "mean"),
        average_base_price=("base_price", "mean")
    )
    .round(2)
)

print(season_analysis)


# ---------------------------------------------------------
# 10. WEEKDAY VS WEEKEND
# ---------------------------------------------------------

print("\n--- DAY OF WEEK ANALYSIS ---")

day_analysis = (
    df.groupby("day_of_week")
    .agg(
        average_units_sold=("units_sold", "mean"),
        average_revenue=("sales_revenue", "mean"),
        average_base_price=("base_price", "mean")
    )
    .round(2)
)

print(day_analysis)


# ---------------------------------------------------------
# 11. DISCOUNT ANALYSIS
# ---------------------------------------------------------

print("\n--- DISCOUNT ANALYSIS ---")

discount_analysis = (
    df.groupby("discount_percentage")
    .agg(
        number_of_records=("discount_percentage", "count"),
        average_units_sold=("units_sold", "mean"),
        average_revenue=("sales_revenue", "mean")
    )
    .round(2)
)

print(discount_analysis)


# ---------------------------------------------------------
# 12. STOCK ANALYSIS
# ---------------------------------------------------------

print("\n--- STOCK ANALYSIS ---")

stock_analysis = (
    df.groupby("demand_level")
    .agg(
        average_opening_stock=("opening_stock", "mean"),
        average_units_sold=("units_sold", "mean"),
        average_closing_stock=("closing_stock", "mean")
    )
    .round(2)
)

print(stock_analysis)


# ---------------------------------------------------------
# 13. CORRELATION WITH BASE PRICE
# ---------------------------------------------------------

print("\n--- CORRELATION WITH BASE PRICE ---")

correlation_columns = [
    "cost_price",
    "current_price",
    "competitor_price",
    "opening_stock",
    "units_sold",
    "closing_stock",
    "discount_percentage",
    "sales_revenue",
    "base_price"
]

correlations = (
    df[correlation_columns]
    .corr()["base_price"]
    .sort_values(ascending=False)
)

print(correlations.round(3))


# ---------------------------------------------------------
# 14. FINAL SUMMARY
# ---------------------------------------------------------

print("\n==========================================")
print("ANALYSIS COMPLETED")
print("==========================================")

print("\nTarget variable:")
print("base_price")

print("\nDataset size:")
print(f"{len(df)} rows × {len(df.columns)} columns")

print("\nThe dataset is ready for deeper analysis and ML preparation.")