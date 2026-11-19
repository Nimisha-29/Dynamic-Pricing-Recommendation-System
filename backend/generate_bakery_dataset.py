import pandas as pd
import random
from datetime import date, timedelta

# =========================================================
# 1. PRODUCT INFORMATION
# =========================================================

products = [
    {
        "product_id": "B001",
        "product_name": "Chocolate Cake",
        "category": "Cake",
        "cost_price": 300,
        "selling_price": 550
    },
    {
        "product_id": "B002",
        "product_name": "Vanilla Cake",
        "category": "Cake",
        "cost_price": 250,
        "selling_price": 475
    },
    {
        "product_id": "B003",
        "product_name": "Red Velvet Cake",
        "category": "Cake",
        "cost_price": 400,
        "selling_price": 700
    },
    {
        "product_id": "B004",
        "product_name": "Black Forest Cake",
        "category": "Cake",
        "cost_price": 350,
        "selling_price": 650
    },
    {
        "product_id": "B005",
        "product_name": "Brownie",
        "category": "Dessert",
        "cost_price": 32,
        "selling_price": 80
    },
    {
        "product_id": "B006",
        "product_name": "Cheesecake",
        "category": "Dessert",
        "cost_price": 280,
        "selling_price": 500
    },
    {
        "product_id": "B007",
        "product_name": "Fruit Tart",
        "category": "Dessert",
        "cost_price": 120,
        "selling_price": 220
    },
    {
        "product_id": "B008",
        "product_name": "Chocolate Cupcake",
        "category": "Cupcake",
        "cost_price": 28,
        "selling_price": 70
    },
    {
        "product_id": "B009",
        "product_name": "Vanilla Cupcake",
        "category": "Cupcake",
        "cost_price": 25,
        "selling_price": 65
    },
    {
        "product_id": "B010",
        "product_name": "Croissant",
        "category": "Baked Item",
        "cost_price": 40,
        "selling_price": 95
    },
    {
        "product_id": "B011",
        "product_name": "Chocolate Muffin",
        "category": "Muffin",
        "cost_price": 35,
        "selling_price": 85
    },
    {
        "product_id": "B012",
        "product_name": "Blueberry Muffin",
        "category": "Muffin",
        "cost_price": 40,
        "selling_price": 95
    },
    {
        "product_id": "B013",
        "product_name": "Donut",
        "category": "Baked Item",
        "cost_price": 25,
        "selling_price": 65
    },
    {
        "product_id": "B014",
        "product_name": "Cookies",
        "category": "Baked Item",
        "cost_price": 22,
        "selling_price": 60
    },
    {
        "product_id": "B015",
        "product_name": "Garlic Bread",
        "category": "Baked Item",
        "cost_price": 55,
        "selling_price": 120
    }
]


# =========================================================
# 2. SETTINGS
# =========================================================

START_DATE = date(2025, 1, 1)
NUMBER_OF_DAYS = 365

records = []


# =========================================================
# 3. GENERATE DAILY DATA
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


    # -----------------------------------------------------
    # WEEKEND
    # -----------------------------------------------------

    is_weekend = day_name in ["Saturday", "Sunday"]


    # =====================================================
    # EACH PRODUCT
    # =====================================================

    for product in products:

        product_id = product["product_id"]
        product_name = product["product_name"]
        category = product["category"]

        typical_cost = product["cost_price"]
        typical_price = product["selling_price"]


        # -------------------------------------------------
        # DAILY COST PRICE
        # -------------------------------------------------

        cost_variation = random.uniform(0.95, 1.05)

        cost_price = round(
            typical_cost * cost_variation,
            2
        )


        # -------------------------------------------------
        # DAILY CURRENT PRICE
        # -------------------------------------------------

        price_variation = random.uniform(0.96, 1.04)

        current_price = round(
            typical_price * price_variation,
            2
        )


        # -------------------------------------------------
        # COMPETITOR PRICE
        # -------------------------------------------------

        competitor_variation = random.uniform(
            0.92,
            1.10
        )

        competitor_price = round(
            typical_price * competitor_variation,
            2
        )


        # -------------------------------------------------
        # DEMAND SCORE
        # -------------------------------------------------

        demand_score = random.uniform(
            0.30,
            0.85
        )


        # Weekend demand increase
        if is_weekend:
            demand_score += 0.10


        # Festival demand increase
        if season == "Festival":
            demand_score += 0.15


        # Product category effects
        if category == "Cake":
            demand_score += 0.05

        elif category == "Muffin":
            demand_score += 0.03

        elif category == "Dessert":
            demand_score += 0.02


        # Daily randomness
        demand_score += random.uniform(
            -0.10,
            0.10
        )

        demand_score = max(
            0.20,
            min(demand_score, 1.00)
        )


        # -------------------------------------------------
        # DEMAND LEVEL
        # -------------------------------------------------

        if demand_score >= 0.75:
            demand_level = "High"

        elif demand_score >= 0.50:
            demand_level = "Medium"

        else:
            demand_level = "Low"


        # -------------------------------------------------
        # OPENING STOCK
        # -------------------------------------------------

        if category == "Cake":
            opening_stock = random.randint(5, 30)

        elif category == "Dessert":
            opening_stock = random.randint(10, 40)

        else:
            opening_stock = random.randint(20, 80)


        # -------------------------------------------------
        # UNITS SOLD
        # -------------------------------------------------

        expected_sales = (
            demand_score * opening_stock
        )

        sales_variation = random.uniform(
            0.65,
            1.05
        )

        units_sold = int(
            expected_sales * sales_variation
        )

        units_sold = max(
            1,
            units_sold
        )

        units_sold = min(
            units_sold,
            opening_stock
        )


        # -------------------------------------------------
        # CLOSING STOCK
        # -------------------------------------------------

        closing_stock = (
            opening_stock - units_sold
        )


        # -------------------------------------------------
        # DISCOUNT
        # -------------------------------------------------

        discount_percentage = 0

        # Excess stock + low demand
        if (
            demand_level == "Low"
            and closing_stock >= opening_stock * 0.50
        ):

            discount_percentage = random.choice(
                [5, 10, 15]
            )

        # Occasional promotion
        elif random.random() < 0.08:

            discount_percentage = random.choice(
                [5, 10]
            )


        # -------------------------------------------------
        # EFFECTIVE SELLING PRICE
        # -------------------------------------------------

        effective_price = (
            current_price
            * (1 - discount_percentage / 100)
        )


        # -------------------------------------------------
        # SALES REVENUE
        # -------------------------------------------------

        sales_revenue = round(
            units_sold * effective_price,
            2
        )


        # =================================================
        # BASE / FAIR PRICE
        # =================================================

        # Start from cost-based pricing
        base_price = cost_price * 1.45


        # -------------------------------------------------
        # Demand effect
        # -------------------------------------------------

        if demand_level == "High":

            base_price *= random.uniform(
                1.15,
                1.30
            )

        elif demand_level == "Medium":

            base_price *= random.uniform(
                1.05,
                1.15
            )

        else:

            base_price *= random.uniform(
                0.95,
                1.05
            )


        # -------------------------------------------------
        # Inventory effect
        # -------------------------------------------------

        stock_ratio = (
            closing_stock / opening_stock
            if opening_stock > 0
            else 0
        )


        if stock_ratio >= 0.50:

            # Excess stock → lower price
            base_price *= random.uniform(
                0.85,
                0.95
            )

        elif stock_ratio <= 0.20:

            # Very low stock → higher price
            base_price *= random.uniform(
                1.05,
                1.15
            )


        # -------------------------------------------------
        # COMPETITOR PRICE EFFECT
        # -------------------------------------------------

        competitor_ratio = (
            competitor_price / current_price
        )


        if competitor_ratio > 1.05:

            # Competitors are more expensive
            # → business can price slightly higher

            base_price *= random.uniform(
                1.02,
                1.07
            )

        elif competitor_ratio < 0.95:

            # Competitors are cheaper
            # → reduce pricing pressure

            base_price *= random.uniform(
                0.93,
                0.98
            )


        # -------------------------------------------------
        # WEEKEND EFFECT
        # -------------------------------------------------

        if is_weekend:

            base_price *= random.uniform(
                1.02,
                1.06
            )


        # -------------------------------------------------
        # FESTIVAL EFFECT
        # -------------------------------------------------

        if season == "Festival":

            base_price *= random.uniform(
                1.03,
                1.10
            )


        # -------------------------------------------------
        # SALES MOMENTUM
        # -------------------------------------------------

        if units_sold >= opening_stock * 0.70:

            base_price *= random.uniform(
                1.03,
                1.08
            )

        elif units_sold <= opening_stock * 0.30:

            base_price *= random.uniform(
                0.93,
                0.98
            )


        # -------------------------------------------------
        # CONTROLLED RANDOMNESS
        # -------------------------------------------------

        base_price *= random.uniform(
            0.97,
            1.03
        )


        # -------------------------------------------------
        # MINIMUM PROFITABLE PRICE
        # -------------------------------------------------

        minimum_price = (
            cost_price * 1.10
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

            "business_type": "Bakery",

            "product_id": product_id,

            "product_name": product_name,

            "category": category,

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

            "sales_revenue": sales_revenue,

            "base_price": base_price
        })


# =========================================================
# 4. CREATE DATAFRAME
# =========================================================

df = pd.DataFrame(records)


# =========================================================
# 5. SAVE DATASET
# =========================================================

output_file = "data/bakery_dataset.csv"

df.to_csv(
    output_file,
    index=False
)


# =========================================================
# 6. OUTPUT INFORMATION
# =========================================================

print("==========================================")
print("BAKERY DATASET GENERATED SUCCESSFULLY")
print("==========================================")

print(f"Rows       : {len(df)}")
print(f"Columns    : {len(df.columns)}")
print(f"Products   : {df['product_id'].nunique()}")

print("\nColumns:")
print(df.columns.tolist())

print("\nDataset saved at:")
print(output_file)

print("\nFirst 5 rows:")
print(df.head())