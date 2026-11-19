# ============================================================
# FILE: backend/pricing_rules.py
# PURPOSE: Apply business rules on top of ML predicted price
#          to produce a final recommended selling price
# TECH: Pure Python (no ML libraries needed here)
# ============================================================

# -------------------------------------------------------
# WHY DO WE NEED RULES ON TOP OF THE ML MODEL?
# -------------------------------------------------------
# The ML model predicts a statistically fair 'base price'.
# But it doesn't know real-time business context like:
#   - "We have 80 units left and almost no one is buying"
#   - "A competitor just dropped their price by 20%"
#   - "It's festival season — we can charge a little more"
#
# Business rules handle these situations intelligently.
# This is what separates a pricing SYSTEM from just a model.
# -------------------------------------------------------


# -------------------------------------------------------
# RULE 1: INVENTORY-BASED ADJUSTMENT
# -------------------------------------------------------
def apply_inventory_rule(base_price, opening_stock, units_sold, cost_price):
    """
    Adjusts price based on stock levels and how fast stock is moving.

    Logic:
    - If stock is very HIGH and sales are LOW  → suggest discount (reduce price)
      Reason: avoid dead stock, recover some revenue
    - If stock is CRITICALLY LOW               → suggest price increase
      Reason: scarcity — don't run out; earn more per unit
    - Otherwise                                → keep base price

    Parameters:
        base_price    : ML predicted fair price (₹)
        opening_stock : stock available at start of day
        units_sold    : units sold that day
        cost_price    : cost to produce/buy the item (₹)

    Returns:
        adjusted_price : price after inventory rule
        action         : human-readable label ('Discount' / 'Increase' / 'Hold')
        reason         : explanation string shown on the dashboard
    """

    # Sales velocity = what % of available stock was sold today
    if opening_stock == 0:
        sales_velocity = 0
    else:
        sales_velocity = units_sold / opening_stock  # 0.0 to 1.0

    # Thresholds (easy to tune later)
    HIGH_STOCK_THRESHOLD   = 50    # more than 50 units = high stock
    LOW_STOCK_THRESHOLD    = 5     # fewer than 5 units = critically low
    LOW_VELOCITY_THRESHOLD = 0.15  # selling less than 15% of stock = slow

    if opening_stock > HIGH_STOCK_THRESHOLD and sales_velocity < LOW_VELOCITY_THRESHOLD:
        # High stock, slow sales → discount by 10%
        discount_factor = 0.90
        adjusted_price  = round(base_price * discount_factor, 2)
        action = "Discount"
        reason = (f"High stock ({opening_stock} units) with slow sales "
                  f"({sales_velocity*100:.1f}% velocity) → 10% discount applied")

    elif opening_stock < LOW_STOCK_THRESHOLD:
        # Critically low stock → increase by 8%
        increase_factor = 1.08
        adjusted_price  = round(base_price * increase_factor, 2)
        action = "Increase"
        reason = (f"Critically low stock ({opening_stock} units remaining) "
                  f"→ 8% price increase applied")

    else:
        # Normal range → hold base price
        adjusted_price = round(base_price, 2)
        action = "Hold"
        reason = (f"Stock level normal ({opening_stock} units, "
                  f"{sales_velocity*100:.1f}% velocity) → no adjustment")

    return adjusted_price, action, reason


# -------------------------------------------------------
# RULE 2: COMPETITOR-BASED ADJUSTMENT
# -------------------------------------------------------
def apply_competitor_rule(price, competitor_price):
    """
    Adjusts price if we are too far above or below the competitor.

    Business logic:
    - If our price is MORE than 15% above competitor → reduce slightly
      Reason: customers will choose competitor over us
    - If our price is MORE than 20% BELOW competitor → increase slightly
      Reason: we are leaving money on the table (underpricing)
    - Otherwise → no adjustment

    Parameters:
        price            : price after inventory rule (₹)
        competitor_price : what the competitor is charging (₹)

    Returns:
        adjusted_price : price after competitor check
        comp_note      : explanation string
    """

    if competitor_price <= 0:
        return price, "Competitor price unavailable — no adjustment"

    # How much higher/lower are we vs competitor (as a ratio)
    our_vs_comp = price / competitor_price  # e.g., 1.20 means we're 20% higher

    TOO_HIGH_RATIO = 1.15   # we are 15%+ above competitor
    TOO_LOW_RATIO  = 0.80   # we are 20%+ below competitor

    if our_vs_comp > TOO_HIGH_RATIO:
        # We are too expensive vs competitor — nudge down
        adjusted_price = round(competitor_price * 1.05, 2)
        comp_note = (f"Our price ₹{price} is {(our_vs_comp-1)*100:.1f}% above "
                     f"competitor ₹{competitor_price} → adjusted to ₹{adjusted_price}")

    elif our_vs_comp < TOO_LOW_RATIO:
        # We are underpricing vs competitor — nudge up
        adjusted_price = round(competitor_price * 0.92, 2)
        comp_note = (f"Our price ₹{price} is {(1-our_vs_comp)*100:.1f}% below "
                     f"competitor ₹{competitor_price} → adjusted to ₹{adjusted_price}")

    else:
        adjusted_price = round(price, 2)
        comp_note = (f"Price ₹{price} is within acceptable range of "
                     f"competitor ₹{competitor_price} → no adjustment")

    return adjusted_price, comp_note


# -------------------------------------------------------
# RULE 3: DEMAND-BASED FINE TUNING
# -------------------------------------------------------
def apply_demand_rule(price, demand_level):
    """
    Fine-tunes price based on current demand level.

    Business logic:
    - High demand   → slight upward nudge (+5%)
      Reason: customers are buying anyway, capture extra margin
    - Low demand    → slight downward nudge (-5%)
      Reason: stimulate purchases
    - Medium demand → no change

    Parameters:
        price        : price after competitor rule (₹)
        demand_level : 'High', 'Medium', or 'Low' (string from the dataset)

    Returns:
        adjusted_price : final demand-adjusted price
        demand_note    : explanation string
    """

    demand_level = str(demand_level).strip().capitalize()

    if demand_level == 'High':
        adjusted_price = round(price * 1.05, 2)
        demand_note = f"High demand → +5% applied → ₹{adjusted_price}"

    elif demand_level == 'Low':
        adjusted_price = round(price * 0.95, 2)
        demand_note = f"Low demand → -5% applied → ₹{adjusted_price}"

    else:
        adjusted_price = round(price, 2)
        demand_note = f"Medium demand → no adjustment → ₹{adjusted_price}"

    return adjusted_price, demand_note


# -------------------------------------------------------
# RULE 4: MINIMUM MARGIN GUARD (SAFETY NET)
# -------------------------------------------------------
def apply_margin_guard(price, cost_price, min_margin_pct=10):
    """
    This is the FINAL safety net rule — the most important one.

    No matter what all other rules do, we NEVER recommend a price
    that results in a loss or unacceptably thin profit margin.

    Minimum acceptable price = cost_price × (1 + min_margin_pct/100)

    Example:
    cost_price = ₹100, min_margin = 10%
    → minimum price = ₹110
    → if rules pushed price to ₹95, we override it to ₹110

    Parameters:
        price         : price after all other rules (₹)
        cost_price    : production/purchase cost (₹)
        min_margin_pct: minimum profit margin % (default 10%)

    Returns:
        final_price  : safe final price
        margin_note  : explanation
        margin_pct   : actual margin % of the final price
    """

    min_acceptable = round(cost_price * (1 + min_margin_pct / 100), 2)
    actual_margin  = round(((price - cost_price) / cost_price) * 100, 2)

    if price < min_acceptable:
        final_price  = min_acceptable
        margin_note  = (f"⚠️ Price ₹{price} below minimum margin "
                        f"→ overridden to ₹{min_acceptable} "
                        f"(ensures {min_margin_pct}% minimum profit)")
        actual_margin = min_margin_pct
    else:
        final_price = price
        margin_note = f"✅ Margin check passed — profit margin: {actual_margin:.1f}%"

    return final_price, margin_note, actual_margin


# -------------------------------------------------------
# MASTER FUNCTION — Apply all rules in sequence
# -------------------------------------------------------
def get_final_recommended_price(
    base_price,
    cost_price,
    competitor_price,
    opening_stock,
    units_sold,
    demand_level,
    min_margin_pct=10
):
    """
    This is the MAIN function the frontend will call.

    It runs all 4 rules in the correct order and returns:
    - final_price      : the recommended selling price
    - price_breakdown  : step-by-step trace of every rule applied
    - action_badge     : 'Discount' / 'Increase' / 'Hold'

    Full pipeline:
    ML base_price
         ↓ Rule 1: Inventory
         ↓ Rule 2: Competitor
         ↓ Rule 3: Demand
         ↓ Rule 4: Margin Guard
    Final Recommended Price

    Parameters match the bakery dataset column names exactly.
    """

    price_breakdown = {
        'ml_base_price'      : round(base_price, 2),
        'steps'              : []
    }

    # ── Rule 1: Inventory ──────────────────────────────
    price, action, reason = apply_inventory_rule(
        base_price, opening_stock, units_sold, cost_price
    )
    price_breakdown['steps'].append({
        'rule'   : 'Inventory Rule',
        'price'  : price,
        'action' : action,
        'reason' : reason
    })

    # ── Rule 2: Competitor ─────────────────────────────
    price, comp_note = apply_competitor_rule(price, competitor_price)
    price_breakdown['steps'].append({
        'rule'   : 'Competitor Rule',
        'price'  : price,
        'reason' : comp_note
    })

    # ── Rule 3: Demand ─────────────────────────────────
    price, demand_note = apply_demand_rule(price, demand_level)
    price_breakdown['steps'].append({
        'rule'   : 'Demand Rule',
        'price'  : price,
        'reason' : demand_note
    })

    # ── Rule 4: Margin Guard ───────────────────────────
    price, margin_note, margin_pct = apply_margin_guard(
        price, cost_price, min_margin_pct
    )
    price_breakdown['steps'].append({
        'rule'   : 'Margin Guard',
        'price'  : price,
        'reason' : margin_note
    })

    price_breakdown['final_recommended_price'] = price
    price_breakdown['profit_margin_pct']        = margin_pct

    return price, action, price_breakdown


# -------------------------------------------------------
# TEST — Run a few sample scenarios to verify rules work
# -------------------------------------------------------
if __name__ == "__main__":

    print("=" * 58)
    print("  PHASE 7 — PRICING RULES ENGINE TEST")
    print("  Tech: Pure Python business logic")
    print("=" * 58)

    # Test scenarios — each represents a different business situation
    test_cases = [
        {
            "label"           : "Scenario 1: High stock, low sales (should DISCOUNT)",
            "base_price"      : 250.00,
            "cost_price"      : 120.00,
            "competitor_price": 260.00,
            "opening_stock"   : 80,
            "units_sold"      : 5,
            "demand_level"    : "Low"
        },
        {
            "label"           : "Scenario 2: Critically low stock (should INCREASE)",
            "base_price"      : 180.00,
            "cost_price"      : 100.00,
            "competitor_price": 190.00,
            "opening_stock"   : 3,
            "units_sold"      : 2,
            "demand_level"    : "High"
        },
        {
            "label"           : "Scenario 3: Normal stock, medium demand (should HOLD)",
            "base_price"      : 320.00,
            "cost_price"      : 180.00,
            "competitor_price": 315.00,
            "opening_stock"   : 30,
            "units_sold"      : 12,
            "demand_level"    : "Medium"
        },
        {
            "label"           : "Scenario 4: Margin guard test (price too low after rules)",
            "base_price"      : 95.00,
            "cost_price"      : 100.00,
            "competitor_price": 90.00,
            "opening_stock"   : 60,
            "units_sold"      : 4,
            "demand_level"    : "Low"
        }
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"\n{'─'*58}")
        print(f"  {tc['label']}")
        print(f"{'─'*58}")

        final_price, action, breakdown = get_final_recommended_price(
            base_price       = tc['base_price'],
            cost_price       = tc['cost_price'],
            competitor_price = tc['competitor_price'],
            opening_stock    = tc['opening_stock'],
            units_sold       = tc['units_sold'],
            demand_level     = tc['demand_level']
        )

        print(f"  ML Base Price      : ₹{breakdown['ml_base_price']}")
        for step in breakdown['steps']:
            print(f"  {step['rule']:<22}: ₹{step['price']}  |  {step['reason']}")

        print(f"\n  ✅ FINAL RECOMMENDED PRICE : ₹{final_price}")
        print(f"  📊 Action Badge             : {action}")
        print(f"  💰 Profit Margin            : {breakdown['profit_margin_pct']}%")

    print(f"\n{'='*58}")
    print("  ✅ PHASE 7 COMPLETE")
    print("  Next step → explainability.py (Phase 8)")
    print(f"{'='*58}")