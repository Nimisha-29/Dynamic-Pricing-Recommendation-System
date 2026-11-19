# ============================================================
# FILE: frontend/app.py
# PURPOSE: Streamlit dashboard — Dynamic Pricing System
# TECH: Streamlit, Plotly, pandas, joblib, PIL
# RUN WITH: streamlit run frontend/app.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from PIL import Image
import sys
import os
from datetime import date, datetime

# Add project root to path so backend modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.pricing_rules import get_final_recommended_price
from backend.explainability import explain_prediction

# -------------------------------------------------------
# PAGE CONFIG — must be the VERY FIRST Streamlit command
# -------------------------------------------------------
st.set_page_config(
    page_title = "Dynamic Pricing System",
    page_icon  = "💰",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# -------------------------------------------------------
# CUSTOM CSS — Dark theme with neon green accents
# -------------------------------------------------------
st.markdown("""
<style>
    /* ── Global background ───────────────────── */
    .stApp                          { background-color: #0E1117; }
    [data-testid="stSidebar"]       { background-color: #161B22; border-right: 1px solid #30363D; }

    /* ── Metric cards ───────────────────────── */
    [data-testid="stMetric"]        { background-color: #1C2333; border: 1px solid #30363D;
                                      border-radius: 10px; padding: 16px !important; }
    [data-testid="stMetricValue"]   { color: #00FF88 !important; font-size: 1.6rem !important; }
    [data-testid="stMetricLabel"]   { color: #AAAAAA !important; }
    [data-testid="stMetricDelta"]   { font-size: 0.85rem !important; }

    /* ── Headings ───────────────────────────── */
    h1 { color: #00FF88 !important; letter-spacing: -0.5px; }
    h2 { color: #FFFFFF !important; }
    h3 { color: #CCCCCC !important; }

    /* ── Info cards ─────────────────────────── */
    .info-card {
        background-color : #1C2333;
        border           : 1px solid #30363D;
        border-radius    : 12px;
        padding          : 18px 20px;
        margin           : 8px 0;
        line-height      : 1.7;
    }
    .rule-card {
        background-color : #161B22;
        border           : 1px solid #30363D;
        border-radius    : 10px;
        padding          : 14px;
        text-align       : center;
        min-height       : 110px;
    }

    /* ── Action badges ──────────────────────── */
    .badge-discount { background:#FF4444; color:white;  padding:5px 16px;
                      border-radius:20px; font-weight:bold; font-size:1rem; }
    .badge-increase { background:#00FF88; color:black;  padding:5px 16px;
                      border-radius:20px; font-weight:bold; font-size:1rem; }
    .badge-hold     { background:#FFB800; color:black;  padding:5px 16px;
                      border-radius:20px; font-weight:bold; font-size:1rem; }

    /* ── Dataframe ──────────────────────────── */
    [data-testid="stDataFrame"] { border-radius: 10px; }

    /* ── Divider ────────────────────────────── */
    hr { border-color: #30363D; margin: 20px 0; }

    /* ── Form submit button ─────────────────── */
    div.stButton > button {
        background-color : #00FF88;
        color            : #0E1117;
        font-weight      : bold;
        border-radius    : 8px;
        font-size        : 1rem;
        padding          : 10px 0;
        border           : none;
    }
    div.stButton > button:hover { background-color: #00CC70; }
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# LOAD MODELS AND DATASET — cached so runs only once
# -------------------------------------------------------
@st.cache_resource
def load_models():
    """Load trained model, encoders, and SHAP explainer from disk."""
    model          = joblib.load('models/bakery_price_model.pkl')
    feature_names  = joblib.load('models/feature_names.pkl')
    encoders       = joblib.load('models/label_encoders.pkl')
    shap_explainer = joblib.load('models/shap_explainer.pkl')
    return model, feature_names, encoders, shap_explainer

@st.cache_data
def load_dataset():
    """Load and parse the bakery dataset."""
    df = pd.read_csv('data/bakery_dataset.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

model, feature_names, encoders, shap_explainer = load_models()
df = load_dataset()

# Reusable dark chart layout
DARK_LAYOUT = dict(
    paper_bgcolor = '#0E1117',
    plot_bgcolor  = '#0E1117',
    font          = dict(color='white'),
    xaxis         = dict(gridcolor='#1C2333', showgrid=True, zeroline=False),
    yaxis         = dict(gridcolor='#1C2333', showgrid=True, zeroline=False),
    legend        = dict(bgcolor='#1C2333', bordercolor='#30363D', borderwidth=1),
    margin        = dict(t=50, b=40, l=40, r=20)
)


# -------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------
st.sidebar.markdown("## 💰 Dynamic Pricing")
st.sidebar.markdown("### 🥐 Bakery Module")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠  Home",
     "💰  Price Recommender",
     "📈  Sales Trends",
     "📦  Inventory Insights"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset info**")
st.sidebar.markdown(f"Records &nbsp;&nbsp; `{len(df):,}`")
st.sidebar.markdown(f"Products &nbsp; `{df['product_name'].nunique()}`")
st.sidebar.markdown(f"From &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `{df['date'].min().date()}`")
st.sidebar.markdown(f"To &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `{df['date'].max().date()}`")
st.sidebar.markdown("---")
st.sidebar.markdown("**Model info**")
st.sidebar.markdown("Algorithm &nbsp;&nbsp;&nbsp; `RandomForest`")
st.sidebar.markdown("R² Score &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `0.9908`")
st.sidebar.markdown("MAE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `₹12.52`")


# ============================================================
#  PAGE 1 — HOME
# ============================================================
if page == "🏠  Home":

    st.title("💰 Dynamic Pricing Recommendation System")
    st.markdown("##### AI-powered pricing engine for small businesses · Bakery Module")
    st.markdown("---")

    # ── Top KPI row ───────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Products",    str(df['product_name'].nunique()))
    with k2:
        avg_margin = ((df['base_price'] - df['cost_price']) / df['cost_price'] * 100).mean()
        st.metric("Avg Profit Margin", f"{avg_margin:.1f}%")
    with k3:
        st.metric("Total Records",     f"{len(df):,}")
    with k4:
        st.metric("Avg Base Price",    f"₹{df['base_price'].mean():.2f}")

    st.markdown("---")

    # ── How it works + Model stats ─────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 🔧 How the system works")
        st.markdown("""
        <div class='info-card'>
            <b style='color:#00FF88'>Step 1 — ML Model (Phase 6)</b><br>
            A Random Forest Regressor trained on 5,475 records predicts
            a statistically fair <i>base price</i> from product features.<br><br>
            <b style='color:#00FF88'>Step 2 — Rules Engine (Phase 7)</b><br>
            Four business rules adjust the ML prediction:<br>
            &nbsp;&nbsp;📦 Inventory rule — stock level + sales velocity<br>
            &nbsp;&nbsp;🏪 Competitor rule — market benchmarking<br>
            &nbsp;&nbsp;📊 Demand rule — High / Medium / Low fine-tuning<br>
            &nbsp;&nbsp;🛡️ Margin guard — minimum profit safety net<br><br>
            <b style='color:#00FF88'>Step 3 — Explainability (Phase 8)</b><br>
            SHAP values reveal <i>exactly why</i> each price was recommended,
            making every decision transparent and auditable.
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("### 📊 Model Performance")
        st.markdown("""
        <div class='info-card'>
            <b style='color:#00FF88'>Algorithm</b> &nbsp; Random Forest Regressor (200 trees)<br>
            <b style='color:#00FF88'>Training</b> &nbsp;&nbsp; 4,380 rows &nbsp;|&nbsp;
            <b style='color:#00FF88'>Testing</b> 1,095 rows<br><br>
            <table style='width:100%; border-collapse:collapse; color:white'>
            <tr>
                <td style='padding:6px 0'><b>R² Score</b></td>
                <td style='color:#00FF88; font-size:1.1em'><b>0.9908</b></td>
                <td style='color:#888'>Model explains 99% of price variation</td>
            </tr>
            <tr>
                <td style='padding:6px 0'><b>MAE</b></td>
                <td style='color:#00FF88; font-size:1.1em'><b>₹12.52</b></td>
                <td style='color:#888'>Average prediction error</td>
            </tr>
            <tr>
                <td style='padding:6px 0'><b>RMSE</b></td>
                <td style='color:#00FF88; font-size:1.1em'><b>₹22.42</b></td>
                <td style='color:#888'>Penalises large errors</td>
            </tr>
            </table>
            <br>
            <b>Top price drivers:</b><br>
            &nbsp; 1. competitor_price &nbsp;(36.5%)<br>
            &nbsp; 2. cost_price &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(32.3%)<br>
            &nbsp; 3. current_price &nbsp;&nbsp;&nbsp;&nbsp;(26.5%)
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📌 Use the sidebar to navigate")
    n1, n2, n3 = st.columns(3)
    with n1:
        st.info("**💰 Price Recommender**\n\nEnter any product's details and get an AI-recommended price, gauge chart, and SHAP explanation.")
    with n2:
        st.info("**📈 Sales Trends**\n\nTrack price and sales changes over time. Filter by product, season, or demand level.")
    with n3:
        st.info("**📦 Inventory Insights**\n\nSee which products need a discount, price increase, or no change based on stock and demand.")


# ============================================================
#  PAGE 2 — PRICE RECOMMENDER
# ============================================================
elif page == "💰  Price Recommender":

    st.title("💰 Price Recommender")
    st.markdown("Fill in the product details and the system will calculate the optimal recommended price.")
    st.markdown("---")

    # Pull unique values from dataset for dropdowns
    product_names  = sorted(df['product_name'].unique())
    categories     = sorted(df['category'].unique())
    season_options = sorted(df['season'].unique())
    day_options    = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    demand_options = ['High', 'Medium', 'Low']

    # ── Input Form ──────────────────────────────────────────
    with st.form("pricing_form"):

        st.markdown("#### 📋 Product Details")
        f1, f2 = st.columns(2)

        with f1:
            product_name  = st.selectbox("Product Name",       product_names)
            category      = st.selectbox("Category",           categories)
            season        = st.selectbox("Season",             season_options)
            day_of_week   = st.selectbox("Day of Week",        day_options)
            demand_level  = st.selectbox("Demand Level",       demand_options)

        with f2:
            selected_date    = st.date_input("Date",           value=date.today())
            cost_price       = st.number_input("Cost Price (₹)",          min_value=1.0,   value=100.0, step=1.0)
            current_price    = st.number_input("Current Selling Price (₹)", min_value=1.0, value=150.0, step=1.0)
            competitor_price = st.number_input("Competitor Price (₹)",    min_value=1.0,   value=145.0, step=1.0)

        st.markdown("#### 📦 Stock & Sales")
        s1, s2, s3 = st.columns(3)
        with s1:
            opening_stock = st.number_input("Opening Stock",  min_value=0, value=30, step=1)
        with s2:
            units_sold    = st.number_input("Units Sold Today", min_value=0, value=10, step=1)
        with s3:
            closing_stock = st.number_input("Closing Stock",  min_value=0, value=20, step=1)
            discount_pct  = st.number_input("Discount %",     min_value=0.0, max_value=50.0,
                                            value=0.0, step=0.5)

        submitted = st.form_submit_button("🔮  Get Recommended Price", use_container_width=True)

    # ── On submit: predict + display results ────────────────
    if submitted:

        # Derive date features from selected date
        dt          = datetime.combine(selected_date, datetime.min.time())
        month       = dt.month
        day_of_year = dt.timetuple().tm_yday
        is_weekend  = int(dt.weekday() >= 5)

        # Encode categorical columns using saved label encoders
        def safe_encode(col_name, value):
            enc = encoders.get(col_name)
            if enc is None:
                return 0
            if value in enc.classes_:
                return int(enc.transform([value])[0])
            return 0

        # Build input DataFrame in the exact column order the model expects
        input_data = pd.DataFrame([{
            'category'            : safe_encode('category',     category),
            'cost_price'          : cost_price,
            'current_price'       : current_price,
            'competitor_price'    : competitor_price,
            'opening_stock'       : opening_stock,
            'units_sold'          : units_sold,
            'closing_stock'       : closing_stock,
            'demand_level'        : safe_encode('demand_level', demand_level),
            'season'              : safe_encode('season',       season),
            'day_of_week'         : safe_encode('day_of_week',  day_of_week),
            'discount_percentage' : discount_pct,
            'month'               : month,
            'day_of_year'         : day_of_year,
            'is_weekend'          : is_weekend
        }])[feature_names]   # reorder to match training column order

        # ── ML Prediction ────────────────────────────────────
        ml_base_price = float(model.predict(input_data)[0])

        # ── Pricing Rules Engine ─────────────────────────────
        final_price, action, breakdown = get_final_recommended_price(
            base_price       = ml_base_price,
            cost_price       = cost_price,
            competitor_price = competitor_price,
            opening_stock    = opening_stock,
            units_sold       = units_sold,
            demand_level     = demand_level
        )

        # ── SHAP Explanation ─────────────────────────────────
        with st.spinner("Generating explanation..."):
            contributions, chart_path, explanation = explain_prediction(
                model, shap_explainer, input_data, feature_names, ml_base_price
            )

        # ── Results ──────────────────────────────────────────
        st.markdown("---")
        st.markdown("## 📊 Recommendation Results")

        # Top metric row
        m1, m2, m3, m4 = st.columns(4)
        profit_margin = ((final_price - cost_price) / cost_price) * 100
        delta_vs_current = final_price - current_price
        badge_class = {"Discount":"badge-discount","Increase":"badge-increase","Hold":"badge-hold"}

        with m1:
            st.metric("ML Base Price",       f"₹{ml_base_price:.2f}")
        with m2:
            st.metric("Recommended Price",   f"₹{final_price:.2f}",
                      delta=f"₹{delta_vs_current:+.2f} vs current")
        with m3:
            st.metric("Profit Margin",       f"{profit_margin:.1f}%")
        with m4:
            st.markdown("**Pricing Action**")
            st.markdown(
                f"<span class='{badge_class.get(action, 'badge-hold')}'>{action}</span>",
                unsafe_allow_html=True
            )

        st.markdown("---")

        # ── Gauge chart (left) + SHAP chart (right) ──────────
        g_col, s_col = st.columns(2)

        with g_col:
            st.markdown("#### 🎯 Price Gauge")

            min_g = cost_price * 0.85
            max_g = max(competitor_price, final_price, current_price) * 1.35

            fig_gauge = go.Figure(go.Indicator(
                mode  = "gauge+number+delta",
                value = final_price,
                delta = {
                    'reference'  : current_price,
                    'increasing' : {'color': '#00FF88'},
                    'decreasing' : {'color': '#FF4444'}
                },
                number = {'prefix': '₹', 'font': {'color': '#00FF88', 'size': 38}},
                title  = {'text': f"vs Current Price  ₹{current_price:.0f}",
                          'font': {'color':'#AAAAAA','size':12}},
                gauge  = {
                    'axis'       : {'range': [min_g, max_g],
                                    'tickcolor': 'white',
                                    'tickfont': {'color':'white', 'size':10}},
                    'bar'        : {'color': '#00FF88', 'thickness': 0.28},
                    'bgcolor'    : '#1C2333',
                    'borderwidth': 1,
                    'bordercolor': '#30363D',
                    'steps': [
                        {'range': [min_g,             cost_price * 1.05], 'color': '#3D0000'},
                        {'range': [cost_price * 1.05, competitor_price],  'color': '#1C2333'},
                        {'range': [competitor_price,  max_g],             'color': '#001A0D'}
                    ],
                    'threshold': {
                        'line'     : {'color': '#FFB800', 'width': 3},
                        'thickness': 0.75,
                        'value'    : current_price
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor = '#0E1117',
                font          = dict(color='white'),
                height        = 300,
                margin        = dict(t=70, b=20, l=30, r=30)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Gauge legend
            st.markdown("""
            <small style='color:#888'>
            🔴 Red zone = below min margin &nbsp;|&nbsp;
            🟡 Yellow line = current price &nbsp;|&nbsp;
            🟢 Green = recommended
            </small>""", unsafe_allow_html=True)

        with s_col:
            st.markdown("#### 🔍 Why this price? (SHAP)")
            if os.path.exists(chart_path):
                shap_img = Image.open(chart_path)
                st.image(shap_img, use_container_width=True)
            else:
                st.warning("SHAP chart not found.")

        # ── Rule breakdown ────────────────────────────────────
        st.markdown("---")
        st.markdown("#### 🔧 Step-by-step Rule Breakdown")
        st.markdown("*Starting from the ML base price, each rule adjusts the price:*")

        rule_cols = st.columns(len(breakdown['steps']))
        step_colors = ['#4ECDC4','#FFB800','#FF6B6B','#00FF88']

        for i, (step, col) in enumerate(zip(breakdown['steps'], rule_cols)):
            with col:
                color = step_colors[i % len(step_colors)]
                reason_short = step['reason']
                if len(reason_short) > 65:
                    reason_short = reason_short[:62] + "..."
                st.markdown(f"""
                <div class='rule-card'>
                    <div style='color:{color}; font-weight:bold; font-size:0.85rem'>
                        {step['rule']}
                    </div>
                    <div style='color:#00FF88; font-size:1.4rem; font-weight:bold; margin:8px 0'>
                        ₹{step['price']}
                    </div>
                    <div style='color:#888; font-size:0.75rem; line-height:1.4'>
                        {reason_short}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ── Plain English explanation ──────────────────────────
        st.markdown("---")
        st.markdown("#### 📝 Plain-English Explanation")
        st.markdown(explanation)


# ============================================================
#  PAGE 3 — SALES TRENDS
# ============================================================
elif page == "📈  Sales Trends":

    st.title("📈 Sales Trend Analysis")
    st.markdown("Track price, sales, and revenue trends over time for any product.")
    st.markdown("---")

    # ── Controls ──────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        selected_product = st.selectbox("Product", sorted(df['product_name'].unique()))
    with c2:
        chart_metric = st.selectbox("Metric", [
            "Units Sold",
            "Revenue (₹)",
            "Base Price vs Current Price"
        ])
    with c3:
        smoothing = st.selectbox("Smoothing", ["None", "7-day avg", "30-day avg"])

    prod_df = df[df['product_name'] == selected_product].sort_values('date').copy()

    # ── Product KPIs ──────────────────────────────────────────
    pk1, pk2, pk3, pk4 = st.columns(4)
    with pk1:
        st.metric("Total Units Sold",  f"{prod_df['units_sold'].sum():,}")
    with pk2:
        st.metric("Avg Daily Sales",   f"{prod_df['units_sold'].mean():.1f}")
    with pk3:
        st.metric("Avg Base Price",    f"₹{prod_df['base_price'].mean():.2f}")
    with pk4:
        st.metric("Total Revenue",     f"₹{prod_df['sales_revenue'].sum():,.0f}")

    st.markdown("---")

    # ── Main Line Chart ───────────────────────────────────────
    fig_line = go.Figure()

    def apply_smoothing(series, mode):
        if mode == "7-day avg":
            return series.rolling(7, min_periods=1).mean()
        elif mode == "30-day avg":
            return series.rolling(30, min_periods=1).mean()
        return series

    if chart_metric == "Units Sold":
        y = apply_smoothing(prod_df['units_sold'], smoothing)
        fig_line.add_trace(go.Scatter(
            x=prod_df['date'], y=y, mode='lines',
            name='Units Sold',
            line=dict(color='#00FF88', width=2),
            fill='tozeroy', fillcolor='rgba(0,255,136,0.06)'
        ))
        y_title = "Units Sold"

    elif chart_metric == "Revenue (₹)":
        y = apply_smoothing(prod_df['sales_revenue'], smoothing)
        fig_line.add_trace(go.Scatter(
            x=prod_df['date'], y=y, mode='lines',
            name='Revenue (₹)',
            line=dict(color='#4ECDC4', width=2),
            fill='tozeroy', fillcolor='rgba(78,205,196,0.06)'
        ))
        y_title = "Revenue (₹)"

    else:  # Base Price vs Current Price
        bp = apply_smoothing(prod_df['base_price'],    smoothing)
        cp = apply_smoothing(prod_df['current_price'], smoothing)
        fig_line.add_trace(go.Scatter(
            x=prod_df['date'], y=bp, mode='lines',
            name='ML Base Price',
            line=dict(color='#00FF88', width=2)
        ))
        fig_line.add_trace(go.Scatter(
            x=prod_df['date'], y=cp, mode='lines',
            name='Current Price',
            line=dict(color='#FF6B6B', width=2, dash='dot')
        ))
        y_title = "Price (₹)"

    fig_line.update_layout(
        title  = f"{selected_product} — {chart_metric}"
                 + (f" ({smoothing})" if smoothing != "None" else ""),
        xaxis_title = "Date",
        yaxis_title = y_title,
        height = 400,
        **DARK_LAYOUT
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ── Demand & Season bar charts ─────────────────────────────
    st.markdown("---")
    st.markdown("#### 📊 Sales Breakdown")

    b1, b2 = st.columns(2)

    with b1:
        d_avg = prod_df.groupby('demand_level')['units_sold'].mean().reset_index()
        d_colors = {'High':'#00FF88','Medium':'#FFB800','Low':'#FF4444'}
        fig_d = go.Figure(go.Bar(
            x=d_avg['demand_level'],
            y=d_avg['units_sold'],
            marker_color=[d_colors.get(d,'#888') for d in d_avg['demand_level']],
            text=d_avg['units_sold'].round(1),
            textposition='outside',
            textfont=dict(color='white')
        ))
        fig_d.update_layout(
            title="Avg Units Sold by Demand", height=320, **DARK_LAYOUT
        )
        st.plotly_chart(fig_d, use_container_width=True)

    with b2:
        s_avg = prod_df.groupby('season')['units_sold'].mean().reset_index()
        fig_s = go.Figure(go.Bar(
            x=s_avg['season'],
            y=s_avg['units_sold'],
            marker_color='#4ECDC4',
            text=s_avg['units_sold'].round(1),
            textposition='outside',
            textfont=dict(color='white')
        ))
        fig_s.update_layout(
            title="Avg Units Sold by Season", height=320, **DARK_LAYOUT
        )
        st.plotly_chart(fig_s, use_container_width=True)

    # ── Day-of-week bar chart ─────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📅 Day-of-Week Sales Pattern")

    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dw = prod_df.groupby('day_of_week')['units_sold'].mean().reindex(day_order).reset_index()
    dw.columns = ['day','avg_sold']

    weekend_colors = ['#00FF88' if d in ['Saturday','Sunday'] else '#4ECDC4'
                      for d in dw['day']]
    fig_dw = go.Figure(go.Bar(
        x=dw['day'], y=dw['avg_sold'],
        marker_color=weekend_colors,
        text=dw['avg_sold'].round(1),
        textposition='outside',
        textfont=dict(color='white')
    ))
    fig_dw.update_layout(
        title="Avg Units Sold by Day (🟢 = weekend)",
        height=320, **DARK_LAYOUT
    )
    st.plotly_chart(fig_dw, use_container_width=True)


# ============================================================
#  PAGE 4 — INVENTORY INSIGHTS
# ============================================================
elif page == "📦  Inventory Insights":

    st.title("📦 Inventory Insights")
    st.markdown("Real-time pricing actions and stock health across all 15 products.")
    st.markdown("---")

    # Use most recent date as the inventory snapshot
    latest_date = df['date'].max()
    snap = df[df['date'] == latest_date].copy()
    st.markdown(f"*Snapshot date: **{latest_date.date()}***")

    # Apply pricing rules for every product
    actions, final_prices = [], []
    for _, row in snap.iterrows():
        fp, act, _ = get_final_recommended_price(
            base_price       = row['base_price'],
            cost_price       = row['cost_price'],
            competitor_price = row['competitor_price'],
            opening_stock    = row['opening_stock'],
            units_sold       = row['units_sold'],
            demand_level     = row['demand_level']
        )
        actions.append(act)
        final_prices.append(round(fp, 2))

    snap['action']            = actions
    snap['recommended_price'] = final_prices
    snap['price_delta']       = (snap['recommended_price'] - snap['current_price']).round(2)
    snap['margin_pct']        = ((snap['recommended_price'] - snap['cost_price'])
                                  / snap['cost_price'] * 100).round(1)

    # ── Summary KPIs ──────────────────────────────────────────
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Discount", f"{(snap['action']=='Discount').sum()} products",
                  delta="reduce price", delta_color="inverse")
    with s2:
        st.metric("Increase", f"{(snap['action']=='Increase').sum()} products",
                  delta="raise price")
    with s3:
        st.metric("Hold",     f"{(snap['action']=='Hold').sum()} products")
    with s4:
        st.metric("Avg Recommended Margin", f"{snap['margin_pct'].mean():.1f}%")

    st.markdown("---")

    # ── Opening vs Closing Stock grouped bar chart ─────────────
    st.markdown("#### 📊 Stock Levels by Product")
    st.markdown("*Closing stock bar is coloured by recommended action*")

    action_color = {
        'Discount': '#FF4444',
        'Increase': '#00FF88',
        'Hold': '#FFB800'
    }

    closing_colors = [
        action_color.get(a, '#888')
        for a in snap['action']
    ]

    fig_stock = go.Figure()

    fig_stock.add_trace(go.Bar(
        name='Opening Stock',
        x=snap['product_name'],
        y=snap['opening_stock'],
        marker_color='rgba(78,205,196,0.65)',
        text=snap['opening_stock'],
        textposition='outside',
        textfont=dict(color='white', size=9)
    ))

    fig_stock.add_trace(go.Bar(
        name='Closing Stock (coloured by action)',
        x=snap['product_name'],
        y=snap['closing_stock'],
        marker_color=closing_colors,
        text=snap['action'],
        textposition='outside',
        textfont=dict(color='white', size=9)
    ))

    fig_stock.update_layout(
        barmode='group',
        height=420,
        **DARK_LAYOUT
    )

    fig_stock.update_xaxes(
        tickangle=-35,
        gridcolor='#1C2333'
    )

    fig_stock.update_yaxes(
        title='Units',
        gridcolor='#1C2333'
    )

    st.plotly_chart(
        fig_stock,
        use_container_width=True
    )

    # ── Full Action Table ─────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📋 Inventory Action Table")

    table = snap[[
        'product_name',
        'category',
        'demand_level',
        'opening_stock',
        'closing_stock',
        'units_sold',
        'cost_price',
        'current_price',
        'recommended_price',
        'price_delta',
        'margin_pct',
        'action'
    ]].rename(columns={
        'product_name': 'Product',
        'category': 'Category',
        'demand_level': 'Demand',
        'opening_stock': 'Open Stock',
        'closing_stock': 'Close Stock',
        'units_sold': 'Sold',
        'cost_price': 'Cost (₹)',
        'current_price': 'Current (₹)',
        'recommended_price': 'Recommended (₹)',
        'price_delta': 'Δ Price (₹)',
        'margin_pct': 'Margin %',
        'action': 'Action'
    })

    def colour_action(val):
        colours = {
            'Discount': 'background-color:#3D0000; color:#FF4444; font-weight:bold',
            'Increase': 'background-color:#003D1A; color:#00FF88; font-weight:bold',
            'Hold': 'background-color:#3D3000; color:#FFB800; font-weight:bold'
        }

        return colours.get(val, '')

    styled = table.style.map(
        colour_action,
        subset=['Action']
    )

    st.dataframe(
        styled,
        use_container_width=True,
        height=500
    )