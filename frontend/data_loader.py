from pathlib import Path
import sys
import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

@st.cache_resource
def load_models():
    model = joblib.load(ROOT / "models" / "bakery_price_model.pkl")
    feature_names = joblib.load(ROOT / "models" / "feature_names.pkl")
    encoders = joblib.load(ROOT / "models" / "label_encoders.pkl")
    shap_explainer = joblib.load(ROOT / "models" / "shap_explainer.pkl")
    return model, feature_names, encoders, shap_explainer

@st.cache_data
def load_dataset():
    df = pd.read_csv(ROOT / "data" / "bakery_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

def project_context():
    model, feature_names, encoders, shap_explainer = load_models()
    df = load_dataset()
    return {"model": model, "feature_names": feature_names, "encoders": encoders, "shap_explainer": shap_explainer, "df": df, "root": ROOT}
