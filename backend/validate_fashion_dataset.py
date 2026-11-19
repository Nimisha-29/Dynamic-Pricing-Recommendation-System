import pandas as pd

# =========================================================
# FASHION DATASET VALIDATION
# =========================================================

FILE_PATH = "data/fashion_dataset.csv"

EXPECTED_COLUMNS = [
    "date",
    "business_type",
    "product_id",
    "product_name",
    "category",
    "size",
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
    "product_age_days",
    "base_price"
]

EXPECTED_PRODUCTS = 15
EXPECTED_DAYS = 365


# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv(FILE_PATH)

print("==========================================")
print("FASHION DATASET VALIDATION")
print("==========================================")


failed_checks = 0


# =========================================================
# 1. ROW COUNT
# =========================================================

# Number of rows is determined by the actual
# product-size combinations.

product_sizes = (
    df[["product_id", "size"]]
    .drop_duplicates()
    .shape[0]
)

expected_rows = product_sizes * EXPECTED_DAYS
actual_rows = len(df)

print(f"Expected rows : {expected_rows}")
print(f"Actual rows   : {actual_rows}")

if actual_rows == expected_rows:
    print("✓ Row count is correct")
else:
    print("✗ Row count is incorrect")
    failed_checks += 1


# =========================================================
# 2. COLUMN CHECK
# =========================================================

actual_columns = df.columns.tolist()

print(f"\nExpected columns : {len(EXPECTED_COLUMNS)}")
print(f"Actual columns   : {len(actual_columns)}")

if actual_columns == EXPECTED_COLUMNS:
    print("✓ Columns are correct")
else:
    print("✗ Columns are incorrect")

    missing_columns = [
        col for col in EXPECTED_COLUMNS
        if col not in actual_columns
    ]

    extra_columns = [
        col for col in actual_columns
        if col not in EXPECTED_COLUMNS
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)

    if extra_columns:
        print("Extra columns:", extra_columns)

    failed_checks += 1


# =========================================================
# 3. MISSING VALUES
# =========================================================

missing_values = df.isnull().sum().sum()

print(f"\nMissing values : {missing_values}")

if missing_values == 0:
    print("✓ No missing values")
else:
    print("✗ Missing values found")
    failed_checks += 1


# =========================================================
# 4. DUPLICATE ROWS
# =========================================================

duplicate_rows = df.duplicated().sum()

print(f"\nDuplicate rows : {duplicate_rows}")

if duplicate_rows == 0:
    print("✓ No duplicate rows")
else:
    print("✗ Duplicate rows found")
    failed_checks += 1


# =========================================================
# 5. PRODUCT COUNT
# =========================================================

unique_products = df["product_id"].nunique()

print(f"\nUnique products : {unique_products}")

if unique_products == EXPECTED_PRODUCTS:
    print("✓ Correct number of products")
else:
    print("✗ Incorrect number of products")
    failed_checks += 1


# =========================================================
# 6. BUSINESS TYPE
# =========================================================

invalid_business_types = (
    df["business_type"] != "Boutique"
).sum()

print(f"\nInvalid business types : {invalid_business_types}")

if invalid_business_types == 0:
    print("✓ Business type is correct")
else:
    print("✗ Invalid business types found")
    failed_checks += 1


# =========================================================
# 7. STOCK CALCULATION
# =========================================================

stock_errors = (
    df["opening_stock"]
    - df["units_sold"]
    - df["closing_stock"]
)

stock_errors = (stock_errors != 0).sum()

print(f"\nStock calculation errors : {stock_errors}")

if stock_errors == 0:
    print("✓ Stock calculations are correct")
else:
    print("✗ Stock calculation errors found")
    failed_checks += 1


# =========================================================
# 8. IMPOSSIBLE SALES
# =========================================================

impossible_sales = (
    df["units_sold"] > df["opening_stock"]
).sum()

negative_sales = (
    df["units_sold"] < 0
).sum()

print(
    f"\nImpossible sales records : "
    f"{impossible_sales + negative_sales}"
)

if impossible_sales == 0 and negative_sales == 0:
    print("✓ Units sold are valid")
else:
    print("✗ Invalid sales records found")
    failed_checks += 1


# =========================================================
# 9. NEGATIVE STOCK
# =========================================================

negative_stock = (
    df["closing_stock"] < 0
).sum()

print(f"\nNegative closing stock : {negative_stock}")

if negative_stock == 0:
    print("✓ Closing stock is valid")
else:
    print("✗ Negative closing stock found")
    failed_checks += 1


# =========================================================
# 10. DEMAND LEVEL
# =========================================================

valid_demand_levels = {
    "Low",
    "Medium",
    "High"
}

invalid_demand = (
    ~df["demand_level"].isin(valid_demand_levels)
).sum()

print(f"\nInvalid demand levels : {invalid_demand}")

if invalid_demand == 0:
    print("✓ Demand levels are valid")
else:
    print("✗ Invalid demand levels found")
    failed_checks += 1


# =========================================================
# 11. SEASON
# =========================================================

valid_seasons = {
    "Regular",
    "Summer",
    "Monsoon",
    "Festival"
}

invalid_seasons = (
    ~df["season"].isin(valid_seasons)
).sum()

print(f"\nInvalid seasons : {invalid_seasons}")

if invalid_seasons == 0:
    print("✓ Seasons are valid")
else:
    print("✗ Invalid seasons found")
    failed_checks += 1


# =========================================================
# 12. SIZE VALIDATION
# =========================================================

valid_sizes = {
    "S",
    "M",
    "L",
    "XL",
    "XXL",
    "Free Size"
}

invalid_sizes = (
    ~df["size"].isin(valid_sizes)
).sum()

print(f"\nInvalid sizes : {invalid_sizes}")

if invalid_sizes == 0:
    print("✓ Sizes are valid")
else:
    print("✗ Invalid sizes found")
    failed_checks += 1


# =========================================================
# 13. PRODUCT-SIZE COMBINATION
# =========================================================

# Products that should have Free Size only
free_size_products = {
    "F009",
    "F010",
    "F013",
    "F014",
    "F015"
}

invalid_free_size = df[
    df["product_id"].isin(free_size_products)
    & (df["size"] != "Free Size")
].shape[0]

# Products that should NOT have Free Size
invalid_clothing_size = df[
    ~df["product_id"].isin(free_size_products)
    & (df["size"] == "Free Size")
].shape[0]

invalid_product_sizes = (
    invalid_free_size + invalid_clothing_size
)

print(
    f"\nInvalid product-size combinations : "
    f"{invalid_product_sizes}"
)

if invalid_product_sizes == 0:
    print("✓ Product-size combinations are valid")
else:
    print("✗ Invalid product-size combinations found")
    failed_checks += 1


# =========================================================
# 14. DISCOUNT VALIDATION
# =========================================================

valid_discounts = {
    0,
    5,
    10,
    15,
    20,
    25
}

invalid_discounts = (
    ~df["discount_percentage"].isin(valid_discounts)
).sum()

print(f"\nInvalid discounts : {invalid_discounts}")

if invalid_discounts == 0:
    print("✓ Discount values are valid")
else:
    print("✗ Invalid discount values found")
    failed_checks += 1


# =========================================================
# 15. PRICE VALIDATION
# =========================================================

invalid_cost = (
    df["cost_price"] <= 0
).sum()

invalid_current_price = (
    df["current_price"] <= 0
).sum()

invalid_competitor_price = (
    df["competitor_price"] <= 0
).sum()

invalid_base_price = (
    df["base_price"] <= 0
).sum()

invalid_prices = (
    invalid_cost
    + invalid_current_price
    + invalid_competitor_price
    + invalid_base_price
)

print(f"\nInvalid price records : {invalid_prices}")

if invalid_prices == 0:
    print("✓ All prices are positive")
else:
    print("✗ Invalid prices found")
    failed_checks += 1


# =========================================================
# 16. PRODUCT AGE
# =========================================================

invalid_age = (
    df["product_age_days"] <= 0
).sum()

print(f"\nInvalid product ages : {invalid_age}")

if invalid_age == 0:
    print("✓ Product ages are valid")
else:
    print("✗ Invalid product ages found")
    failed_checks += 1


# =========================================================
# 17. REVENUE CALCULATION
# =========================================================

# The generator calculates revenue internally as:
#
# units_sold × current_price × (1 - discount / 100)
#
# Revenue is not stored as a column in this dataset,
# so we verify the calculated values are mathematically valid.

calculated_revenue = (
    df["units_sold"]
    * df["current_price"]
    * (1 - df["discount_percentage"] / 100)
)

invalid_revenue = (
    calculated_revenue < 0
).sum()

print(f"\nRevenue calculation errors : {invalid_revenue}")

if invalid_revenue == 0:
    print("✓ Revenue calculations are valid")
else:
    print("✗ Revenue calculation errors found")
    failed_checks += 1


# =========================================================
# 18. BASE PRICE VS COST
# =========================================================

# The generator rounds the minimum profitable price
# to 2 decimal places before assigning base_price.
# We must use the exact same calculation here.

minimum_profitable_price = (
    df["cost_price"] * 1.08
).round(2)

invalid_base_cost_relationship = (
    df["base_price"] < minimum_profitable_price
).sum()

print(
    f"\nBase price below minimum margin : "
    f"{invalid_base_cost_relationship}"
)

if invalid_base_cost_relationship == 0:
    print("✓ Base prices maintain minimum margin")
else:
    print("✗ Some base prices are below minimum margin")
    failed_checks += 1

# =========================================================
# FINAL RESULT
# =========================================================

print("\n==========================================")

if failed_checks == 0:

    print("✓ DATASET VALIDATION PASSED")
    print("The fashion dataset is ready for analysis.")

else:

    print("✗ DATASET VALIDATION FAILED")
    print(
        f"Number of validation checks failed: "
        f"{failed_checks}"
    )

print("==========================================")