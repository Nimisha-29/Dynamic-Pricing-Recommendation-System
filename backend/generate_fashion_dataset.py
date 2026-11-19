import pandas as pd
import random
from datetime import date, timedelta

# =========================================================
# PRODUCT INFORMATION
# =========================================================

products = [
    {
        "product_id": "F001",
        "product_name": "Cotton Kurti",
        "category": "Ethnic Wear",
        "cost_price": 400,
        "selling_price": 850,
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "product_id": "F002",
        "product_name": "Anarkali Dress",
        "category": "Ethnic Wear",
        "cost_price": 800,
        "selling_price": 1600,
        "sizes": ["S", "M", "L", "XL", "XXL"]
    },
    {
        "product_id": "F003",
        "product_name": "Printed Salwar Suit",
        "category": "Ethnic Wear",
        "cost_price": 900,
        "selling_price": 1800,
        "sizes": ["S", "M", "L", "XL", "XXL"]
    },
    {
        "product_id": "F004",
        "product_name": "Embroidered Kurta",
        "category": "Ethnic Wear",
        "cost_price": 700,
        "selling_price": 1400,
        "sizes": ["S", "M", "L", "XL", "XXL"]
    },
    {
        "product_id": "F005",
        "product_name": "Casual Top",
        "category": "Western Wear",
        "cost_price": 350,
        "selling_price": 750,
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "product_id": "F006",
        "product_name": "Denim Jeans",
        "category": "Western Wear",
        "cost_price": 900,
        "selling_price": 1800,
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "product_id": "F007",
        "product_name": "Palazzo Pants",
        "category": "Western Wear",
        "cost_price": 400,
        "selling_price": 850,
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "product_id": "F008",
        "product_name": "Maxi Dress",
        "category": "Western Wear",
        "cost_price": 800,
        "selling_price": 1700,
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "product_id": "F009",
        "product_name": "Saree",
        "category": "Traditional Wear",
        "cost_price": 1200,
        "selling_price": 2500,
        "sizes": ["Free Size"]
    },
    {
        "product_id": "F010",
        "product_name": "Chiffon Saree",
        "category": "Traditional Wear",
        "cost_price": 800,
        "selling_price": 1600,
        "sizes": ["Free Size"]
    },
    {
        "product_id": "F011",
        "product_name": "Party Gown",
        "category": "Occasion Wear",
        "cost_price": 1500,
        "selling_price": 3200,
        "sizes": ["S", "M", "L", "XL", "XXL"]
    },
    {
        "product_id": "F012",
        "product_name": "Lehenga",
        "category": "Occasion Wear",
        "cost_price": 2200,
        "selling_price": 4500,
        "sizes": ["S", "M", "L", "XL", "XXL"]
    },
    {
        "product_id": "F013",
        "product_name": "Handbag",
        "category": "Accessories",
        "cost_price": 600,
        "selling_price": 1200,
        "sizes": ["Free Size"]
    },
    {
        "product_id": "F014",
        "product_name": "Scarf",
        "category": "Accessories",
        "cost_price": 180,
        "selling_price": 400,
        "sizes": ["Free Size"]
    },
    {
        "product_id": "F015",
        "product_name": "Fashion Belt",
        "category": "Accessories",
        "cost_price": 180,
        "selling_price": 400,
        "sizes": ["Free Size"]
    }
]

# =========================================================
# SETTINGS
# =========================================================

START_DATE = date(2025, 1, 1)
NUMBER_OF_DAYS = 365

records = []

# =========================================================
# SIZE DEMAND WEIGHTS
# =========================================================

size_demand_weights = {
    "S": 0.90,
    "M": 1.10,
    "L": 1.05,
    "XL": 0.90,
    "XXL": 0.70,
    "Free Size": 1.00
}

# =========================================================
# GENERATE DATA
# =========================================================

for day_number in range(NUMBER_OF_DAYS):

    current_date = START_DATE + timedelta(days=day_number)
    day_name = current_date.strftime("%A")
    month = current_date.month

    # -----------------------------------------------------
    # SEASON
    # -----------------------------------------------------

    if month in [10, 11, 12]:
        season = "Festival"
    elif month in [4, 5]:
        season = "Summer"
    elif month in [6, 7, 8, 9]:
        season = "Monsoon"
    else:
        season = "Regular"

    is_weekend = day_name in ["Saturday", "Sunday"]

    # =====================================================
    # PRODUCTS
    # =====================================================

    for product in products:

        product_id = product["product_id"]
        product_name = product["product_name"]
        category = product["category"]

        typical_cost = product["cost_price"]
        typical_price = product["selling_price"]

        # Each product gets a fixed starting age.
        # This avoids unrealistic daily random age changes.
        if day_number == 0:
            initial_age = random.randint(5, 120)

        # Deterministic age based on product ID and day.
        # This keeps age increasing naturally.
        product_number = int(product_id[1:])
        initial_age = 5 + ((product_number * 17) % 116)

        product_age_days = initial_age + day_number

        # =================================================
        # SIZES
        # =================================================

        for size in product["sizes"]:

            size_weight = size_demand_weights[size]

            # -------------------------------------------------
            # COST PRICE
            # -------------------------------------------------

            cost_price = round(
                typical_cost * random.uniform(0.95, 1.05),
                2
            )

            # -------------------------------------------------
            # CURRENT PRICE
            # -------------------------------------------------

            current_price = round(
                typical_price * random.uniform(0.96, 1.04),
                2
            )

            # -------------------------------------------------
            # COMPETITOR PRICE
            # -------------------------------------------------

            competitor_price = round(
                typical_price * random.uniform(0.90, 1.10),
                2
            )

            # =================================================
            # DEMAND SCORE
            # =================================================

            demand_score = random.uniform(0.25, 0.75)

            demand_score *= size_weight

            if is_weekend:
                demand_score += 0.08

            if season == "Festival":

                if category in [
                    "Ethnic Wear",
                    "Traditional Wear",
                    "Occasion Wear"
                ]:
                    demand_score += 0.20
                else:
                    demand_score += 0.08

            if season == "Summer":

                if product_name in [
                    "Cotton Kurti",
                    "Casual Top",
                    "Palazzo Pants",
                    "Scarf"
                ]:
                    demand_score += 0.12

            if season == "Monsoon":

                if product_name in [
                    "Denim Jeans",
                    "Maxi Dress"
                ]:
                    demand_score -= 0.05

            if category == "Occasion Wear":
                demand_score += 0.05

            elif category == "Accessories":
                demand_score += 0.02

            if product_age_days > 150:
                demand_score -= 0.08

            if product_age_days > 250:
                demand_score -= 0.12

            demand_score += random.uniform(-0.10, 0.10)

            demand_score = max(
                0.10,
                min(demand_score, 1.00)
            )

            # -------------------------------------------------
            # DEMAND LEVEL
            # -------------------------------------------------

            if demand_score >= 0.70:
                demand_level = "High"
            elif demand_score >= 0.45:
                demand_level = "Medium"
            else:
                demand_level = "Low"

            # =================================================
            # OPENING STOCK
            # =================================================

            if category == "Occasion Wear":

                opening_stock = random.randint(3, 18)

            elif category in [
                "Ethnic Wear",
                "Traditional Wear"
            ]:

                opening_stock = random.randint(5, 25)

            elif category == "Accessories":

                opening_stock = random.randint(15, 50)

            else:

                opening_stock = random.randint(8, 30)

            # Size-specific inventory behavior

            if size == "M":
                opening_stock += random.randint(0, 5)

            elif size == "L":
                opening_stock += random.randint(0, 4)

            elif size == "XXL":
                opening_stock = max(
                    2,
                    opening_stock - random.randint(0, 4)
                )

            # =================================================
            # UNITS SOLD
            # =================================================

            expected_sales = demand_score * opening_stock

            units_sold = int(
                expected_sales
                * random.uniform(0.60, 1.05)
            )

            units_sold = max(
                0,
                min(units_sold, opening_stock)
            )

            # -------------------------------------------------
            # CLOSING STOCK
            # -------------------------------------------------

            closing_stock = (
                opening_stock - units_sold
            )

            # =================================================
            # DISCOUNT
            # =================================================

            discount_percentage = 0

            stock_ratio = (
                closing_stock / opening_stock
                if opening_stock > 0
                else 0
            )

            if (
                product_age_days > 180
                and stock_ratio >= 0.50
            ):

                discount_percentage = random.choice(
                    [10, 15, 20, 25]
                )

            elif (
                demand_level == "Low"
                and stock_ratio >= 0.50
            ):

                discount_percentage = random.choice(
                    [5, 10, 15]
                )

            elif random.random() < 0.06:

                discount_percentage = random.choice(
                    [5, 10]
                )

            # =================================================
            # SALES REVENUE
            # =================================================

            effective_price = (
                current_price
                * (1 - discount_percentage / 100)
            )

            sales_revenue = round(
                units_sold * effective_price,
                2
            )

            # =================================================
            # BASE / FAIR PRICE
            # =================================================

            base_price = cost_price * 1.45

            # Demand effect

            if demand_level == "High":

                base_price *= random.uniform(
                    1.12, 1.25
                )

            elif demand_level == "Medium":

                base_price *= random.uniform(
                    1.03, 1.12
                )

            else:

                base_price *= random.uniform(
                    0.92, 1.02
                )

            # Inventory effect

            if stock_ratio >= 0.60:

                base_price *= random.uniform(
                    0.82, 0.93
                )

            elif stock_ratio <= 0.20:

                base_price *= random.uniform(
                    1.05, 1.15
                )

            # Product age effect

            if product_age_days > 180:

                base_price *= random.uniform(
                    0.90, 0.97
                )

            if product_age_days > 300:

                base_price *= random.uniform(
                    0.85, 0.95
                )

            # Competitor effect

            competitor_ratio = (
                competitor_price / current_price
            )

            if competitor_ratio > 1.05:

                base_price *= random.uniform(
                    1.02, 1.07
                )

            elif competitor_ratio < 0.95:

                base_price *= random.uniform(
                    0.92, 0.98
                )

            # Weekend effect

            if is_weekend:

                base_price *= random.uniform(
                    1.01, 1.05
                )

            # Festival effect

            if season == "Festival":

                if category in [
                    "Ethnic Wear",
                    "Traditional Wear",
                    "Occasion Wear"
                ]:

                    base_price *= random.uniform(
                        1.05, 1.12
                    )

                else:

                    base_price *= random.uniform(
                        1.02, 1.06
                    )

            # Sales momentum

            sales_ratio = (
                units_sold / opening_stock
                if opening_stock > 0
                else 0
            )

            if sales_ratio >= 0.70:

                base_price *= random.uniform(
                    1.03, 1.08
                )

            elif sales_ratio <= 0.25:

                base_price *= random.uniform(
                    0.92, 0.98
                )

            # Controlled randomness

            base_price *= random.uniform(
                0.97, 1.03
            )

            # -------------------------------------------------
            # MINIMUM PROFITABLE PRICE
            # -------------------------------------------------

            # Round the minimum first so that the generator
            # and validator use the exact same 2-decimal value.

            minimum_price = round(
                cost_price * 1.08,
                2
            )

            base_price = max(
                base_price,
                minimum_price
            )

            base_price = round(
                base_price,
                2
            )

            # =================================================
            # SAVE RECORD
            # =================================================

            records.append({

                "date": current_date.strftime(
                    "%Y-%m-%d"
                ),

                "business_type": "Boutique",

                "product_id": product_id,

                "product_name": product_name,

                "category": category,

                "size": size,

                "cost_price": cost_price,

                "current_price": current_price,

                "competitor_price": competitor_price,

                "opening_stock": opening_stock,

                "units_sold": units_sold,

                "closing_stock": closing_stock,

                "demand_level": demand_level,

                "season": season,

                "day_of_week": day_name,

                "discount_percentage": discount_percentage,

                "product_age_days": product_age_days,

                "base_price": base_price
            })


# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame(records)


# =========================================================
# SAVE DATASET
# =========================================================

output_file = "data/fashion_dataset.csv"

df.to_csv(
    output_file,
    index=False
)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("==========================================")
print("FASHION DATASET GENERATED SUCCESSFULLY")
print("==========================================")

print(f"Rows       : {len(df)}")
print(f"Columns    : {len(df.columns)}")
print(f"Products   : {df['product_id'].nunique()}")
print(f"Sizes      : {df['size'].nunique()}")

print("\nExpected structure:")
print(df.columns.tolist())

print("\nDataset saved at:")
print(output_file)

print("\nFirst 5 rows:")
print(df.head())