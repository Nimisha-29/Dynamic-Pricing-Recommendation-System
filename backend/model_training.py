# ============================================================
# FILE: backend/model_training.py
# PURPOSE: Train and evaluate the ML model on bakery data
# TECH: scikit-learn, pandas, numpy, joblib
# ============================================================

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os

# -------------------------------------------------------
# STEP 1: LOAD THE PREPARED DATA
# -------------------------------------------------------
def load_prepared_data():
    """
    Load the 4 CSV files that feature_engineering.py created.
    X = features (inputs), y = base_price (target/output)
    """
    X_train = pd.read_csv('data/X_train.csv')
    X_test  = pd.read_csv('data/X_test.csv')
    y_train = pd.read_csv('data/y_train.csv').squeeze()  # squeeze converts DataFrame to Series
    y_test  = pd.read_csv('data/y_test.csv').squeeze()

    print(f"✅ Data loaded successfully")
    print(f"   X_train : {X_train.shape}  |  y_train : {y_train.shape}")
    print(f"   X_test  : {X_test.shape}   |  y_test  : {y_test.shape}")

    return X_train, X_test, y_train, y_test


# -------------------------------------------------------
# STEP 2: TRAIN THE MODEL
# -------------------------------------------------------
def train_model(X_train, y_train):
    """
    We train a RandomForestRegressor.

    WHY Random Forest?
    - Works well even without scaling (no need to normalise data)
    - Handles both numerical and encoded categorical features
    - Gives feature importances (useful for SHAP explanation later)
    - Rarely overfits badly with default settings
    - Easy to explain in viva: 'It builds many decision trees
      and averages their predictions for a more reliable result'

    Key parameters explained (for your viva):
    n_estimators=200   → builds 200 decision trees (more = more stable)
    max_depth=10       → each tree can go 10 levels deep (prevents overfitting)
    min_samples_leaf=4 → each leaf node needs at least 4 samples (smooths predictions)
    random_state=42    → same result every run (reproducible)
    n_jobs=-1          → use all CPU cores (trains faster)
    """
    print("\n🔄 Training Random Forest model...")
    print("   (This may take 30–60 seconds — please wait)")

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    print("✅ Model training complete")

    return model


# -------------------------------------------------------
# STEP 3: EVALUATE THE MODEL
# -------------------------------------------------------
def evaluate_model(model, X_test, y_test):
    """
    We evaluate how well the model predicts on data it has NEVER seen.

    Three metrics explained (memorise these for your viva):

    MAE  (Mean Absolute Error)
         Average rupee difference between predicted and actual price.
         Example: MAE = 12 means predictions are off by ₹12 on average.
         Lower is better. Easy to explain to non-technical audience.

    RMSE (Root Mean Squared Error)
         Like MAE but penalises large errors more heavily.
         Lower is better. More sensitive to outliers.

    R²   (R-squared / Coefficient of Determination)
         How much of the price variation the model explains.
         Range: 0 to 1. Closer to 1 is better.
         Example: R²=0.92 means the model explains 92% of price variation.

    A good model for this dataset would have:
    R²   > 0.85
    MAE  < 15 (for bakery prices in ₹100–₹500 range)
    """
    y_pred = model.predict(X_test)

    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = r2_score(y_test, y_pred)

    print("\n" + "=" * 45)
    print("  MODEL EVALUATION RESULTS")
    print("=" * 45)
    print(f"  MAE  (Mean Absolute Error) : ₹{mae:.2f}")
    print(f"  RMSE (Root Mean Sq. Error) : ₹{rmse:.2f}")
    print(f"  R²   (R-squared Score)     : {r2:.4f}")
    print("=" * 45)

    # Interpret the R² score automatically
    if r2 >= 0.90:
        print("  ✅ Excellent model performance")
    elif r2 >= 0.80:
        print("  ✅ Good model performance")
    elif r2 >= 0.70:
        print("  ⚠️  Acceptable — consider tuning")
    else:
        print("  ❌ Poor performance — review features")

    return y_pred, mae, rmse, r2


# -------------------------------------------------------
# STEP 4: SHOW FEATURE IMPORTANCES
# -------------------------------------------------------
def show_feature_importances(model, feature_names):
    """
    Random Forest tells us which features influenced the
    predictions the most — this is very useful for your viva.

    Example output might show:
    cost_price        → 35% importance
    competitor_price  → 22% importance
    current_price     → 18% importance
    ...etc
    """
    importances = model.feature_importances_
    feature_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)

    print("\n📊 FEATURE IMPORTANCES (top influencers of base_price):")
    print("-" * 40)
    for _, row in feature_df.iterrows():
        bar = "█" * int(row['Importance'] * 50)
        print(f"  {row['Feature']:<20} {bar}  {row['Importance']:.4f}")

    return feature_df


# -------------------------------------------------------
# STEP 5: SAVE THE TRAINED MODEL
# -------------------------------------------------------
def save_model(model, feature_names):
    """
    Save the trained model to disk using joblib.
    This means we NEVER need to retrain — the frontend
    simply loads this file and makes predictions instantly.

    We also save the feature names so the frontend knows
    exactly which columns to pass to the model in the same order.
    """
    os.makedirs('models', exist_ok=True)

    joblib.dump(model, 'models/bakery_price_model.pkl')
    joblib.dump(feature_names, 'models/feature_names.pkl')

    print("\n✅ Model saved to: models/bakery_price_model.pkl")
    print("✅ Feature names saved to: models/feature_names.pkl")


# -------------------------------------------------------
# STEP 6: QUICK SANITY CHECK — TEST ONE PREDICTION
# -------------------------------------------------------
def test_single_prediction(model, X_test, y_test):
    """
    Pick one random row from test data and predict its price.
    Compare the prediction against the actual base_price.
    This is a simple way to 'see' the model working.
    """
    sample = X_test.iloc[[0]]   # take the first row
    actual = y_test.iloc[0]
    predicted = model.predict(sample)[0]

    print("\n🔍 SANITY CHECK — Single Prediction:")
    print(f"   Actual base_price    : ₹{actual:.2f}")
    print(f"   Predicted base_price : ₹{predicted:.2f}")
    print(f"   Difference           : ₹{abs(actual - predicted):.2f}")


# -------------------------------------------------------
# MAIN — Run all steps in order
# -------------------------------------------------------
if __name__ == "__main__":

    print("=" * 55)
    print("  PHASE 6 — MODEL TRAINING & EVALUATION")
    print("  Tech: scikit-learn RandomForestRegressor")
    print("=" * 55)

    # Load data
    X_train, X_test, y_train, y_test = load_prepared_data()

    # Train
    model = train_model(X_train, y_train)

    # Evaluate
    y_pred, mae, rmse, r2 = evaluate_model(model, X_test, y_test)

    # Feature importances
    feature_df = show_feature_importances(model, X_train.columns.tolist())

    # Save model
    save_model(model, X_train.columns.tolist())

    # Quick check
    test_single_prediction(model, X_test, y_test)

    print("\n" + "=" * 55)
    print("  ✅ PHASE 6 COMPLETE")
    print("  Next step → pricing_rules.py (Phase 7)")
    print("=" * 55)