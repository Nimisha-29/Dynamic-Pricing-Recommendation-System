# ============================================================
# FILE: backend/feature_engineering.py
# PURPOSE: Prepare the bakery dataset for ML model training
# TECH: pandas, numpy, scikit-learn
# ============================================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import os
import joblib  # to save encoders for reuse later

# -------------------------------------------------------
# STEP 1: LOAD THE DATASET
# -------------------------------------------------------
def load_data(filepath):
    """
    Loads the CSV file into a pandas DataFrame.
    A DataFrame is like an Excel table inside Python.
    """
    df = pd.read_csv(filepath)
    print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


# -------------------------------------------------------
# STEP 2: DROP COLUMNS WE DON'T NEED
# -------------------------------------------------------
def drop_unnecessary_columns(df):
    """
    Some columns must be removed before feeding data into the ML model.

    WHY we drop each one:
    - business_type : same value for every row in this dataset → useless
    - product_id    : just an ID number, not a meaningful feature
    - product_name  : text name — we keep category instead
    - sales_revenue : this = units_sold × current_price (calculated from
                      other columns already in the data, keeping it would
                      give the model an unfair "cheat")
    - date          : raw dates confuse models; we extract useful parts below
    - base_price    : this is our TARGET (y), never an input (X)
    """
    columns_to_drop = [
        'business_type',
        'product_id',
        'product_name',
        'sales_revenue',
        'date'           # we extract features from date in the next step
    ]

    # Only drop columns that actually exist in the file
    columns_to_drop = [c for c in columns_to_drop if c in df.columns]
    df = df.drop(columns=columns_to_drop)

    print(f"✅ Dropped unnecessary columns. Remaining: {list(df.columns)}")
    return df


# -------------------------------------------------------
# STEP 3: EXTRACT USEFUL FEATURES FROM THE DATE COLUMN
# -------------------------------------------------------
def extract_date_features(df, date_column='date'):
    """
    Raw dates like '2024-01-15' are meaningless to an ML model.
    We extract patterns from the date that ARE useful:
    - month      : pricing changes by month (Jan vs Dec)
    - day_of_year: captures seasonal position (day 1 to 365)
    - is_weekend : weekend vs weekday affects demand

    We do this BEFORE dropping the date column.
    """
    # Re-read date from original df — so call this BEFORE drop_unnecessary_columns
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month           # 1 = January, 12 = December
    df['day_of_year'] = df['date'].dt.dayofyear # 1 to 365
    df['is_weekend'] = df['date'].dt.dayofweek.isin([5, 6]).astype(int)  # 1=weekend, 0=weekday

    print("✅ Date features extracted: month, day_of_year, is_weekend")
    return df


# -------------------------------------------------------
# STEP 4: ENCODE CATEGORICAL (TEXT) COLUMNS INTO NUMBERS
# -------------------------------------------------------
def encode_categorical_columns(df):
    """
    ML models only understand numbers — not text like 'High' or 'Festival'.
    We convert text columns into numbers using LabelEncoder.

    Examples after encoding:
    demand_level : Low=0, Medium=1, High=2  (or similar)
    season       : Festival=0, Monsoon=1, Regular=2, Summer=3
    day_of_week  : Friday=0, Monday=1, Saturday=2 ...

    We save each encoder to disk so the frontend can later decode
    the numbers back to human-readable labels.
    """
    os.makedirs('models', exist_ok=True)  # create models/ folder if it doesn't exist

    categorical_columns = ['demand_level', 'season', 'day_of_week']

    # For fashion dataset, these extra columns also exist:
    if 'category' in df.columns:
        categorical_columns.append('category')
    if 'size' in df.columns:
        categorical_columns.append('size')

    encoders = {}  # store encoder for each column

    for col in categorical_columns:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le
            print(f"  ✅ Encoded '{col}': {list(le.classes_)} → {list(range(len(le.classes_)))}")

    # Save all encoders to disk so we can reuse them in the frontend
    joblib.dump(encoders, 'models/label_encoders.pkl')
    print("✅ All encoders saved to models/label_encoders.pkl")

    return df, encoders


# -------------------------------------------------------
# STEP 5: SEPARATE FEATURES (X) AND TARGET (y)
# -------------------------------------------------------
def split_features_and_target(df, target_column='base_price'):
    """
    X = input features (everything the model learns FROM)
    y = target (what the model is trying to PREDICT)

    Think of it like:
    X = question paper
    y = answer key
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    print(f"\n✅ Features (X): {list(X.columns)}")
    print(f"✅ Target   (y): {target_column}")
    print(f"   X shape: {X.shape}  |  y shape: {y.shape}")

    return X, y


# -------------------------------------------------------
# STEP 6: SPLIT INTO TRAINING AND TESTING SETS
# -------------------------------------------------------
def split_train_test(X, y, test_size=0.2, random_state=42):
    """
    We split the data into:
    - Training set (80%) : model LEARNS from this
    - Testing set  (20%) : we CHECK how well the model learned

    random_state=42 means the split is always the same every time
    you run the code (reproducible result for viva).

    WHY we need a test set:
    If we test on the same data we trained on, the model looks
    perfect but fails on new data. Test set simulates 'new data'.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    print(f"\n✅ Train/Test Split done:")
    print(f"   Training rows : {X_train.shape[0]}")
    print(f"   Testing rows  : {X_test.shape[0]}")

    return X_train, X_test, y_train, y_test


# -------------------------------------------------------
# STEP 7: SAVE PREPARED DATA TO DISK
# -------------------------------------------------------
def save_prepared_data(X_train, X_test, y_train, y_test):
    """
    Save all 4 splits to the data/ folder as CSV files.
    This way, model_training.py can just load these directly
    without running feature engineering again.
    """
    os.makedirs('data', exist_ok=True)

    X_train.to_csv('data/X_train.csv', index=False)
    X_test.to_csv('data/X_test.csv',   index=False)
    y_train.to_csv('data/y_train.csv', index=False)
    y_test.to_csv('data/y_test.csv',   index=False)

    print("\n✅ Saved prepared data to data/ folder:")
    print("   data/X_train.csv")
    print("   data/X_test.csv")
    print("   data/y_train.csv")
    print("   data/y_test.csv")


# -------------------------------------------------------
# MAIN — Run all steps in order
# -------------------------------------------------------
if __name__ == "__main__":

    # ← Change this path if your CSV has a different name
    DATASET_PATH = 'data/bakery_dataset.csv'

    print("=" * 55)
    print("  PHASE 5 — ML PREPARATION: FEATURE ENGINEERING")
    print("=" * 55)

    # Run every step in order
    df = load_data(DATASET_PATH)
    df = extract_date_features(df)       # must come BEFORE drop
    df = drop_unnecessary_columns(df)
    df, encoders = encode_categorical_columns(df)

    X, y = split_features_and_target(df)
    X_train, X_test, y_train, y_test = split_train_test(X, y)

    save_prepared_data(X_train, X_test, y_train, y_test)

    print("\n" + "=" * 55)
    print("  ✅ FEATURE ENGINEERING COMPLETE")
    print("  Next step → model_training.py")
    print("=" * 55)