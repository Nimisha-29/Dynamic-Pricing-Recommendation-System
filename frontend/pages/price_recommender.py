import os
from datetime import date, datetime
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import streamlit as st
from backend.pricing_rules import get_final_recommended_price
from components import chart_box, status_text
from styles import NAVY, ACCENT, GREEN, RED, AMBER, MUTED


def _safe_encode(encoders, col_name, value):
    enc = encoders.get(col_name)
    if enc is None:
        return 0
    try:
        if value in enc.classes_:
            return int(enc.transform([value])[0])
    except Exception:
        pass
    return 0


def render(ctx):
    df = ctx["df"]
    model = ctx["model"]
    feature_names = ctx["feature_names"]
    encoders = ctx["encoders"]
    shap_explainer = ctx["shap_explainer"]

    st.markdown('<div class="section-kicker">Pricing workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Price Recommender</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Enter the current business conditions. The existing trained model and pricing rules will calculate the recommended selling price.</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    product_names = sorted(df["product_name"].unique())
    categories = sorted(df["category"].unique())
    season_options = sorted(df["season"].unique())
    day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    demand_options = ["High", "Medium", "Low"]

    with st.container(key="pricing_form_shell"):
        with st.form("pricing_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                product_name = st.selectbox("Product Name", product_names)
                category = st.selectbox("Category", categories)
                season = st.selectbox("Season", season_options)
            with c2:
                selected_date = st.date_input("Date", value=date.today())
                day_of_week = st.selectbox("Day of Week", day_options)
                demand_level = st.selectbox("Demand Level", demand_options)
            with c3:
                cost_price = st.number_input("Cost Price (₹)", min_value=1.0, value=100.0, step=1.0)
                current_price = st.number_input("Current Selling Price (₹)", min_value=1.0, value=150.0, step=1.0)
                competitor_price = st.number_input("Competitor Price (₹)", min_value=1.0, value=145.0, step=1.0)

            st.markdown("<div class='pricing-section-title'>Stock & Sales</div>", unsafe_allow_html=True)
            s1, s2, s3, s4 = st.columns(4)
            with s1:
                opening_stock = st.number_input("Opening Stock", min_value=0, value=30, step=1)
            with s2:
                units_sold = st.number_input("Units Sold Today", min_value=0, value=10, step=1)
            with s3:
                closing_stock = st.number_input("Closing Stock", min_value=0, value=20, step=1)
            with s4:
                discount_pct = st.number_input("Discount %", min_value=0.0, max_value=50.0, value=0.0, step=0.5)

            submitted = st.form_submit_button("Generate recommendation", use_container_width=True)

    if not submitted:
        return

    try:
        dt = datetime.combine(selected_date, datetime.min.time())
        input_data = pd.DataFrame([{
            "category": _safe_encode(encoders, "category", category),
            "cost_price": cost_price,
            "current_price": current_price,
            "competitor_price": competitor_price,
            "opening_stock": opening_stock,
            "units_sold": units_sold,
            "closing_stock": closing_stock,
            "demand_level": _safe_encode(encoders, "demand_level", demand_level),
            "season": _safe_encode(encoders, "season", season),
            "day_of_week": _safe_encode(encoders, "day_of_week", day_of_week),
            "discount_percentage": discount_pct,
            "month": dt.month,
            "day_of_year": dt.timetuple().tm_yday,
            "is_weekend": int(dt.weekday() >= 5),
        }])[feature_names]

        ml_base_price = float(model.predict(input_data)[0])
        final_price, action, breakdown = get_final_recommended_price(
            base_price=ml_base_price,
            cost_price=cost_price,
            competitor_price=competitor_price,
            opening_stock=opening_stock,
            units_sold=units_sold,
            demand_level=demand_level,
        )
    except Exception as exc:
        st.error(f"The price calculation could not be completed: {exc}")
        return

    contributions = None
    chart_path = None
    explanation = None
    # SHAP is supplementary: a SHAP/version issue must not block the actual price recommendation.
    try:
        with st.spinner("Generating explanation..."):
            from backend.explainability import explain_prediction
            contributions, chart_path, explanation = explain_prediction(
                model, shap_explainer, input_data, feature_names, ml_base_price
            )
    except Exception as exc:
        st.warning(f"Price recommendation was generated, but the explanation chart could not be loaded: {exc}")

    st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    profit_margin = ((final_price - cost_price) / cost_price) * 100
    with m1:
        st.metric("ML Base Price", f"₹{ml_base_price:.2f}")
    with m2:
        st.metric("Recommended Price", f"₹{final_price:.2f}", delta=f"₹{final_price-current_price:+.2f} vs current")
    with m3:
        st.metric("Profit Margin", f"{profit_margin:.1f}%")
    with m4:
        st.markdown('<div class="section-kicker">Recommended action</div>', unsafe_allow_html=True)
        st.markdown(status_text(action), unsafe_allow_html=True)

    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        min_g = cost_price * 0.85
        max_g = max(competitor_price, final_price, current_price) * 1.35
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=final_price,
            delta={"reference": current_price, "increasing": {"color": GREEN}, "decreasing": {"color": RED}, "font": {"color": NAVY, "size": 16}},
            number={"prefix": "₹", "font": {"color": NAVY, "size": 36}},
            gauge={
                "axis": {"range": [min_g, max_g], "tickcolor": NAVY, "tickfont": {"color": NAVY, "size": 11}},
                "bar": {"color": ACCENT, "thickness": 0.25},
                "bgcolor": "#EEE7DC",
                "borderwidth": 0,
                "steps": [
                    {"range": [min_g, cost_price * 1.05], "color": "#EAD8D8"},
                    {"range": [cost_price * 1.05, competitor_price], "color": "#EEE7DC"},
                    {"range": [competitor_price, max_g], "color": "#DDE7E1"},
                ],
                "threshold": {"line": {"color": AMBER, "width": 3}, "thickness": 0.75, "value": current_price},
            },
        ))
        fig.update_layout(paper_bgcolor="#FFFDF9", plot_bgcolor="#FFFDF9", font={"color": NAVY, "family": "Inter, Arial, sans-serif"}, height=320, margin={"t": 55, "b": 20, "l": 20, "r": 20})
        chart_box(fig)
    with right:
        st.markdown('<div class="section-kicker">Explainability</div>', unsafe_allow_html=True)
        st.markdown("### Why this price?")
        if chart_path and os.path.exists(chart_path):
            st.image(Image.open(chart_path), use_container_width=True)
        else:
            st.info("The recommendation is available above. The SHAP explanation is unavailable for this run.")

    st.markdown('<div class="section-kicker">Rule sequence</div>', unsafe_allow_html=True)
    cols = st.columns(len(breakdown["steps"]))
    for col, step in zip(cols, breakdown["steps"]):
        with col:
            st.markdown(
                f'<div class="panel"><small>{step["rule"]}</small><h3>₹{step["price"]}</h3><p class="muted">{step["reason"]}</p></div>',
                unsafe_allow_html=True,
            )

    if explanation:
        st.markdown("### Recommendation explained")
        st.markdown(explanation)
