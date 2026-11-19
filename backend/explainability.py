# ============================================================
# FILE: backend/explainability.py
# PURPOSE: Explain WHY the ML model predicted a specific price
#          using SHAP (SHapley Additive exPlanations)
# TECH: shap, joblib, pandas, matplotlib
# ============================================================

# -------------------------------------------------------
# WHAT IS SHAP? (memorise this for your viva)
# -------------------------------------------------------
# SHAP comes from game theory (Shapley values).
# It answers: "How much did each feature CONTRIBUTE to
# this specific prediction, compared to the average?"
#
# Example output:
#   cost_price       → pushed price UP by ₹+45
#   competitor_price → pushed price UP by ₹+30
#   demand_level     → pushed price DOWN by ₹-8
#   season           → pushed price UP by ₹+5
#
# This means the model is NOT a black box — every
# recommendation is fully explainable.
# -------------------------------------------------------

import shap
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')           # non-interactive backend (safe for Streamlit)
import matplotlib.pyplot as plt
import os

# -------------------------------------------------------
# STEP 1: LOAD THE SAVED MODEL
# -------------------------------------------------------
def load_model_and_features():
    """
    Load the trained Random Forest model and feature names
    that were saved in Phase 6 (model_training.py).
    """
    model         = joblib.load('models/bakery_price_model.pkl')
    feature_names = joblib.load('models/feature_names.pkl')

    print(f"✅ Model loaded: {type(model).__name__}")
    print(f"✅ Features    : {feature_names}")

    return model, feature_names


# -------------------------------------------------------
# STEP 2: CREATE THE SHAP EXPLAINER
# -------------------------------------------------------
def create_explainer(model, X_background):
    """
    Creates a TreeExplainer — the fastest and most accurate
    SHAP explainer for tree-based models like Random Forest.

    X_background: a sample of training data used as reference.
    SHAP compares each prediction AGAINST this background
    to calculate how much each feature shifted the prediction.

    We use a sample of 100 rows (not all 4380) to keep it fast.
    """
    # Use a small background sample for speed
    background = X_background.sample(
        n=min(100, len(X_background)),
        random_state=42
    )

    explainer = shap.TreeExplainer(model, background)
    print("✅ SHAP TreeExplainer created")

    return explainer


# -------------------------------------------------------
# STEP 3: EXPLAIN A SINGLE PREDICTION
# -------------------------------------------------------
def explain_single_prediction(explainer, input_row_df, feature_names):
    """
    Computes SHAP values for ONE specific product input.

    input_row_df : a single-row DataFrame with all feature columns
                   (this comes from the frontend user's input)

    Returns:
        shap_values   : array of contribution values per feature
        expected_value: the model's average prediction (baseline)
        contributions : dict mapping feature name → shap value
    """
    # Compute SHAP values for this row
    shap_values   = explainer.shap_values(input_row_df)
    expected_value = explainer.expected_value

    # If output is a list (some RF versions), take first element
    if isinstance(shap_values, list):
        shap_values = shap_values[0]
    if isinstance(expected_value, (list, np.ndarray)):
        expected_value = expected_value[0]

    # Build a readable dictionary: feature → contribution (₹)
    contributions = {}
    for i, fname in enumerate(feature_names):
        contributions[fname] = round(float(shap_values[0][i]), 4)

    # Sort by absolute contribution (largest effect first)
    contributions = dict(
        sorted(contributions.items(),
               key=lambda x: abs(x[1]),
               reverse=True)
    )

    return shap_values, expected_value, contributions


# -------------------------------------------------------
# STEP 4: GENERATE SHAP BAR CHART (for the dashboard)
# -------------------------------------------------------
def generate_shap_bar_chart(contributions, predicted_price, save_path='models/shap_plot.png'):
    """
    Creates a horizontal bar chart showing each feature's
    contribution to the predicted price.

    Positive bars (green) → pushed price UP
    Negative bars (red)   → pushed price DOWN

    This chart is saved as a PNG and displayed in the
    Streamlit dashboard.

    Dark theme: matches the dashboard's dark background.
    """
    os.makedirs('models', exist_ok=True)

    features = list(contributions.keys())
    values   = list(contributions.values())
    colors   = ['#00FF88' if v >= 0 else '#FF4444' for v in values]

    # Reverse so largest bar is at the top
    features = features[::-1]
    values   = values[::-1]
    colors   = colors[::-1]

    fig, ax = plt.subplots(figsize=(9, 5))

    # Dark background to match dashboard theme
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    bars = ax.barh(features, values, color=colors, edgecolor='none', height=0.6)

    # Value labels on each bar
    for bar, val in zip(bars, values):
        label = f'+₹{val:.2f}' if val >= 0 else f'-₹{abs(val):.2f}'
        x_pos = val + 0.3 if val >= 0 else val - 0.3
        ha    = 'left' if val >= 0 else 'right'
        ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                label, va='center', ha=ha,
                color='white', fontsize=8, fontweight='bold')

    # Vertical line at zero
    ax.axvline(0, color='#888888', linewidth=1, linestyle='--')

    # Labels and title
    ax.set_title(
        f'Why ₹{predicted_price:.2f} was recommended\n'
        f'(Feature contributions to the ML base price)',
        color='white', fontsize=11, pad=12
    )
    ax.set_xlabel('Contribution to Price (₹)', color='#AAAAAA', fontsize=9)
    ax.tick_params(colors='white', labelsize=8)
    ax.spines['bottom'].set_color('#444444')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444444')

    plt.tight_layout()
    plt.savefig(save_path, dpi=130, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close()

    print(f"✅ SHAP bar chart saved to: {save_path}")
    return save_path


# -------------------------------------------------------
# STEP 5: GENERATE READABLE TEXT EXPLANATION
# -------------------------------------------------------
def generate_text_explanation(contributions, expected_value, predicted_price):
    """
    Produces a plain-English explanation of the top 3
    factors that drove the price recommendation.

    This text is displayed alongside the SHAP chart
    on the Streamlit dashboard.

    Example output:
    "The base price of ₹245.00 was driven mainly by:
     1. cost_price contributed +₹45.20 (pushed price up)
     2. competitor_price contributed +₹30.10 (pushed price up)
     3. demand_level contributed -₹8.50 (pushed price down)"
    """
    lines = [
        f"📌 Predicted base price: ₹{predicted_price:.2f}",
        f"📌 Model average (baseline): ₹{expected_value:.2f}",
        "",
        "🔍 Top factors that influenced this price:",
        ""
    ]

    top_3 = list(contributions.items())[:3]

    for rank, (feature, value) in enumerate(top_3, 1):
        direction = "pushed price UP ⬆️" if value >= 0 else "pushed price DOWN ⬇️"
        sign      = "+" if value >= 0 else ""
        lines.append(
            f"  {rank}. **{feature}** → {sign}₹{value:.2f}  ({direction})"
        )

    lines.append("")
    lines.append("All other features had smaller effects (see chart above).")

    explanation = "\n".join(lines)
    return explanation


# -------------------------------------------------------
# MASTER FUNCTION — called by the frontend
# -------------------------------------------------------
def explain_prediction(model, explainer, input_row_df,
                       feature_names, predicted_price):
    """
    One function the frontend calls to get everything:
    - SHAP contributions dict
    - Saved chart path
    - Plain-English explanation text

    Parameters:
        model          : loaded RandomForest model
        explainer      : SHAP TreeExplainer
        input_row_df   : single-row DataFrame from user input
        feature_names  : list of column names in correct order
        predicted_price: the ML predicted base price (float)

    Returns:
        contributions  : dict {feature: shap_value}
        chart_path     : path to saved PNG chart
        explanation    : plain-English string
    """
    shap_values, expected_value, contributions = explain_single_prediction(
        explainer, input_row_df, feature_names
    )

    chart_path  = generate_shap_bar_chart(contributions, predicted_price)
    explanation = generate_text_explanation(
        contributions, expected_value, predicted_price
    )

    return contributions, chart_path, explanation


# -------------------------------------------------------
# TEST — Run with a sample row from training data
# -------------------------------------------------------
if __name__ == "__main__":

    print("=" * 58)
    print("  PHASE 8 — EXPLAINABILITY ENGINE TEST")
    print("  Tech: SHAP (SHapley Additive exPlanations)")
    print("=" * 58)

    # Load model and features
    model, feature_names = load_model_and_features()

    # Load a few rows of training data as background
    X_train = pd.read_csv('data/X_train.csv')
    X_test  = pd.read_csv('data/X_test.csv')

    print("\n🔄 Creating SHAP explainer (may take 10–20 seconds)...")
    explainer = create_explainer(model, X_train)

    # Take the first row of test data as a sample prediction
    sample_row    = X_test.iloc[[0]]
    sample_price  = float(model.predict(sample_row)[0])

    print(f"\n🔍 Explaining prediction for sample row...")
    print(f"   Predicted base price: ₹{sample_price:.2f}")

    shap_values, expected_value, contributions = explain_single_prediction(
        explainer, sample_row, feature_names
    )

    # Print contributions table
    print(f"\n📊 SHAP CONTRIBUTIONS (baseline avg = ₹{expected_value:.2f}):")
    print(f"{'─'*50}")
    for feat, val in contributions.items():
        direction = "▲" if val >= 0 else "▼"
        bar = "█" * min(int(abs(val) / 2), 25)
        print(f"  {direction} {feat:<22} {bar:<25} {'+' if val>=0 else ''}{val:.4f}")

    # Generate and save chart
    chart_path = generate_shap_bar_chart(contributions, sample_price)

    # Generate text explanation
    explanation = generate_text_explanation(
        contributions, expected_value, sample_price
    )
    print(f"\n📝 TEXT EXPLANATION:\n{explanation}")

    # Save explainer for reuse in frontend
    joblib.dump(explainer, 'models/shap_explainer.pkl')
    print(f"\n✅ SHAP explainer saved to: models/shap_explainer.pkl")

    print(f"\n{'='*58}")
    print("  ✅ PHASE 8 COMPLETE")
    print("  Next step → frontend/app.py (Phase 10 — Dashboard)")
    print(f"{'='*58}")