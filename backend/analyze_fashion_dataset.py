import pandas as pd

# =========================================================
# FASHION DATASET ANALYSIS
# =========================================================

FILE_PATH = "data/fashion_dataset.csv"

df = pd.read_csv(FILE_PATH)

print("==========================================")
print("FASHION DATASET ANALYSIS")
print("==========================================")


# =========================================================
# BASIC INFORMATION
# =========================================================

print("\n--- BASIC INFORMATION ---")

print(f"Rows       : {len(df)}")
print(f"Columns    : {len(df.columns)}")
print(f"Products   : {df['product_id'].nunique()}")
print(f"Sizes      : {df['size'].nunique()}")
print(f"Date range : {df['date'].min()} to {df['date'].max()}")


# =========================================================
# NUMERICAL SUMMARY
# =========================================================

print("\n--- NUMERICAL SUMMARY ---")

numerical_columns = [
    "cost_price",
    "current_price",
    "competitor_price",
    "opening_stock",
    "units_sold",
    "closing_stock",
    "discount_percentage",
    "product_age_days",
    "base_price"
]

print(
    df[numerical_columns]
    .describe()
    .round(2)
)


# =========================================================
# DEMAND DISTRIBUTION
# =========================================================

print("\n--- DEMAND DISTRIBUTION ---")

demand_counts = (
    df["demand_level"]
    .value_counts()
)

print(demand_counts)

print("\nDemand percentages:")

demand_percentages = (
    df["demand_level"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(demand_percentages)


# =========================================================
# SALES BY PRODUCT
# =========================================================

print("\n--- SALES BY PRODUCT ---")

sales_by_product = (
    df.groupby(
        ["product_id", "product_name"]
    )["units_sold"]
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_product)


# =========================================================
# REVENUE BY PRODUCT
# =========================================================

print("\n--- REVENUE BY PRODUCT ---")

df["sales_revenue"] = (
    df["units_sold"]
    * df["current_price"]
    * (1 - df["discount_percentage"] / 100)
)

revenue_by_product = (
    df.groupby(
        ["product_id", "product_name"]
    )["sales_revenue"]
    .sum()
    .sort_values(ascending=False)
)

print(revenue_by_product.round(2))


# =========================================================
# AVERAGE PRICES BY PRODUCT
# =========================================================

print("\n--- AVERAGE PRICES ---")

average_prices = (
    df.groupby("product_name")[
        [
            "cost_price",
            "current_price",
            "competitor_price",
            "base_price"
        ]
    ]
    .mean()
    .sort_values(
        "current_price",
        ascending=False
    )
)

print(average_prices.round(2))


# =========================================================
# DEMAND VS SALES
# =========================================================

print("\n--- DEMAND VS AVERAGE SALES ---")

demand_analysis = (
    df.groupby("demand_level")[
        [
            "units_sold",
            "closing_stock",
            "base_price"
        ]
    ]
    .mean()
    .rename(
        columns={
            "units_sold": "average_units_sold",
            "closing_stock": "average_closing_stock",
            "base_price": "average_base_price"
        }
    )
)

print(demand_analysis.round(2))


# =========================================================
# CATEGORY ANALYSIS
# =========================================================

print("\n--- CATEGORY ANALYSIS ---")

category_analysis = (
    df.groupby("category")[
        [
            "units_sold",
            "sales_revenue",
            "base_price"
        ]
    ]
    .mean()
    .rename(
        columns={
            "units_sold": "average_units_sold",
            "sales_revenue": "average_revenue",
            "base_price": "average_base_price"
        }
    )
    .sort_values(
        "average_revenue",
        ascending=False
    )
)

print(category_analysis.round(2))


# =========================================================
# SIZE ANALYSIS
# =========================================================

print("\n--- SIZE ANALYSIS ---")

size_analysis = (
    df.groupby("size")[
        [
            "units_sold",
            "closing_stock",
            "base_price"
        ]
    ]
    .mean()
    .rename(
        columns={
            "units_sold": "average_units_sold",
            "closing_stock": "average_closing_stock",
            "base_price": "average_base_price"
        }
    )
    .sort_values(
        "average_units_sold",
        ascending=False
    )
)

print(size_analysis.round(2))


# =========================================================
# SEASONAL ANALYSIS
# =========================================================

print("\n--- SEASONAL ANALYSIS ---")

season_analysis = (
    df.groupby("season")[
        [
            "units_sold",
            "sales_revenue",
            "base_price"
        ]
    ]
    .mean()
    .rename(
        columns={
            "units_sold": "average_units_sold",
            "sales_revenue": "average_revenue",
            "base_price": "average_base_price"
        }
    )
)

print(season_analysis.round(2))


# =========================================================
# DAY OF WEEK ANALYSIS
# =========================================================

print("\n--- DAY OF WEEK ANALYSIS ---")

day_analysis = (
    df.groupby("day_of_week")[
        [
            "units_sold",
            "sales_revenue",
            "base_price"
        ]
    ]
    .mean()
    .rename(
        columns={
            "units_sold": "average_units_sold",
            "sales_revenue": "average_revenue",
            "base_price": "average_base_price"
        }
    )
)

# Put days in normal weekly order

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_analysis = day_analysis.reindex(day_order)

print(day_analysis.round(2))


# =========================================================
# DISCOUNT ANALYSIS
# =========================================================

print("\n--- DISCOUNT ANALYSIS ---")

discount_analysis = (
    df.groupby("discount_percentage")[
        [
            "units_sold",
            "sales_revenue",
            "closing_stock"
        ]
    ]
    .agg(
        number_of_records=("units_sold", "count"),
        average_units_sold=("units_sold", "mean"),
        average_revenue=("sales_revenue", "mean"),
        average_closing_stock=("closing_stock", "mean")
    )
)

print(discount_analysis.round(2))


# =========================================================
# PRODUCT AGE ANALYSIS
# =========================================================

print("\n--- PRODUCT AGE ANALYSIS ---")

df["age_group"] = pd.cut(
    df["product_age_days"],
    bins=[
        0,
        90,
        180,
        270,
        float("inf")
    ],
    labels=[
        "0-90 days",
        "91-180 days",
        "181-270 days",
        "271+ days"
    ]
)

age_analysis = (
    df.groupby(
        "age_group",
        observed=True
    )[
        [
            "units_sold",
            "closing_stock",
            "discount_percentage",
            "base_price"
        ]
    ]
    .mean()
)

print(age_analysis.round(2))


# =========================================================
# STOCK ANALYSIS
# =========================================================

print("\n--- STOCK ANALYSIS ---")

stock_analysis = (
    df.groupby("demand_level")[
        [
            "opening_stock",
            "units_sold",
            "closing_stock"
        ]
    ]
    .mean()
)

print(stock_analysis.round(2))


# =========================================================
# COMPETITOR PRICE ANALYSIS
# =========================================================

print("\n--- COMPETITOR PRICE ANALYSIS ---")

df["competitor_price_difference"] = (
    df["current_price"]
    - df["competitor_price"]
)

competitor_analysis = (
    df.groupby("demand_level")[
        [
            "current_price",
            "competitor_price",
            "competitor_price_difference",
            "base_price"
        ]
    ]
    .mean()
)

print(competitor_analysis.round(2))


# =========================================================
# CORRELATION WITH BASE PRICE
# =========================================================

print("\n--- CORRELATION WITH BASE PRICE ---")

correlation_columns = [
    "base_price",
    "cost_price",
    "current_price",
    "competitor_price",
    "opening_stock",
    "units_sold",
    "closing_stock",
    "discount_percentage",
    "product_age_days",
    "sales_revenue"
]

correlation = (
    df[correlation_columns]
    .corr()["base_price"]
    .sort_values(ascending=False)
)

print(correlation.round(3))


# =========================================================
# DATASET SUMMARY
# =========================================================

print("\n==========================================")
print("ANALYSIS COMPLETED")
print("==========================================")

print("\nTarget variable:")
print("base_price")

print("\nDataset size:")
print(
    f"{len(df)} rows × "
    f"{len(df.columns)} columns"
)

print("\nImportant pricing factors included:")

print("✓ Product cost")
print("✓ Current price")
print("✓ Competitor price")
print("✓ Demand")
print("✓ Inventory")
print("✓ Size")
print("✓ Season")
print("✓ Day of week")
print("✓ Discount")
print("✓ Product age")

print("\nThe fashion dataset is ready for deeper ML preparation.")