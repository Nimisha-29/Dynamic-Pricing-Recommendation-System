import pandas as pd

# Load the bakery dataset
file_path = "data/bakery_dataset.csv"

df = pd.read_csv(file_path)

print("==========================================")
print("BAKERY DATASET VALIDATION")
print("==========================================")

# ---------------------------------------------------------
# 1. Check number of rows
# ---------------------------------------------------------

expected_rows = 15 * 365

print(f"\nExpected rows : {expected_rows}")
print(f"Actual rows   : {len(df)}")

if len(df) == expected_rows:
    print("✓ Row count is correct")
else:
    print("✗ Row count is incorrect")


# ---------------------------------------------------------
# 2. Check number of columns
# ---------------------------------------------------------

expected_columns = [
    "date",
    "business_type",
    "product_id",
    "product_name",
    "category",
    "cost_price",
    "current_price",
    "competitor_price",
    "opening_stock",
    "units_sold",
    "closing_stock",
    "demand_level",
    "season",
    "day_of_week",
    "discount_percentage",
    "sales_revenue",
    "base_price"
]

print(f"\nExpected columns : {len(expected_columns)}")
print(f"Actual columns   : {len(df.columns)}")

if list(df.columns) == expected_columns:
    print("✓ Columns are correct")
else:
    print("✗ Column structure is incorrect")


# ---------------------------------------------------------
# 3. Check missing values
# ---------------------------------------------------------

missing_values = df.isnull().sum().sum()

print(f"\nMissing values : {missing_values}")

if missing_values == 0:
    print("✓ No missing values")
else:
    print("✗ Missing values found")


# ---------------------------------------------------------
# 4. Check duplicate rows
# ---------------------------------------------------------

duplicates = df.duplicated().sum()

print(f"\nDuplicate rows : {duplicates}")

if duplicates == 0:
    print("✓ No duplicate rows")
else:
    print("✗ Duplicate rows found")


# ---------------------------------------------------------
# 5. Check stock calculation
# ---------------------------------------------------------

stock_errors = (
    df["opening_stock"] - df["units_sold"]
    != df["closing_stock"]
).sum()

print(f"\nStock calculation errors : {stock_errors}")

if stock_errors == 0:
    print("✓ Stock calculations are correct")
else:
    print("✗ Stock calculation errors found")


# ---------------------------------------------------------
# 6. Check units sold cannot exceed opening stock
# ---------------------------------------------------------

sales_errors = (
    df["units_sold"] > df["opening_stock"]
).sum()

print(f"\nImpossible sales records : {sales_errors}")

if sales_errors == 0:
    print("✓ Units sold never exceed opening stock")
else:
    print("✗ Impossible sales records found")


# ---------------------------------------------------------
# 7. Check demand levels
# ---------------------------------------------------------

valid_demand_levels = ["Low", "Medium", "High"]

invalid_demand = (
    ~df["demand_level"].isin(valid_demand_levels)
).sum()

print(f"\nInvalid demand levels : {invalid_demand}")

if invalid_demand == 0:
    print("✓ Demand levels are valid")
else:
    print("✗ Invalid demand levels found")


# ---------------------------------------------------------
# 8. Check business type
# ---------------------------------------------------------

invalid_business = (
    df["business_type"] != "Bakery"
).sum()

print(f"\nInvalid business types : {invalid_business}")

if invalid_business == 0:
    print("✓ Business type is correct")
else:
    print("✗ Invalid business types found")


# ---------------------------------------------------------
# 9. Check product count
# ---------------------------------------------------------

product_count = df["product_id"].nunique()

print(f"\nUnique products : {product_count}")

if product_count == 15:
    print("✓ Correct number of products")
else:
    print("✗ Product count is incorrect")


# ---------------------------------------------------------
# 10. Check discount range
# ---------------------------------------------------------

invalid_discount = (
    (df["discount_percentage"] < 0)
    | (df["discount_percentage"] > 100)
).sum()

print(f"\nInvalid discounts : {invalid_discount}")

if invalid_discount == 0:
    print("✓ Discount values are valid")
else:
    print("✗ Invalid discount values found")


# ---------------------------------------------------------
# 11. Check revenue
# ---------------------------------------------------------

calculated_price = (
    df["current_price"]
    * (1 - df["discount_percentage"] / 100)
)

calculated_revenue = (
    df["units_sold"] * calculated_price
).round(2)

revenue_errors = (
    abs(df["sales_revenue"] - calculated_revenue) > 0.10
).sum()

print(f"\nRevenue calculation errors : {revenue_errors}")

if revenue_errors == 0:
    print("✓ Revenue calculations are correct")
else:
    print("✗ Revenue calculation errors found")


# ---------------------------------------------------------
# FINAL RESULT
# ---------------------------------------------------------

print("\n==========================================")

total_errors = (
    (len(df) != expected_rows)
    + (list(df.columns) != expected_columns)
    + (missing_values != 0)
    + (duplicates != 0)
    + (stock_errors != 0)
    + (sales_errors != 0)
    + (invalid_demand != 0)
    + (invalid_business != 0)
    + (product_count != 15)
    + (invalid_discount != 0)
    + (revenue_errors != 0)
)

if total_errors == 0:
    print("✓ DATASET VALIDATION PASSED")
    print("The bakery dataset is ready for analysis.")
else:
    print("✗ DATASET VALIDATION FAILED")
    print(f"Number of validation checks failed: {total_errors}")

print("==========================================")