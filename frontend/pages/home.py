import streamlit as st
from components import feature_grid
from styles import page_header


def render(ctx):
    df = ctx["df"]
    st.markdown(f"""
    <section class="hero">
      <div class="hero-copy">
        <div class="eyebrow">AI-powered pricing intelligence · Business workspace</div>
        <h1>Price with purpose.<br>Grow with confidence.</h1>
        <p>Use product, sales, inventory, demand and competitor signals to make clearer pricing decisions for your business.</p>
        <div class="hero-meta">
          <div><strong>{df['product_name'].nunique()}</strong><span>Products</span></div>
          <div><strong>{len(df):,}</strong><span>Records</span></div>
          <div><strong>{df['date'].max().date()}</strong><span>Latest data</span></div>
        </div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    page_header("Business pricing workspace", "One place for the decisions that affect your margin.", "Use the existing model, business rules and analytics together to understand demand and choose a practical price.")
    feature_grid([
        {"index":"01", "title":"Price Recommender", "text":"Generate a recommended selling price from the existing trained model and business rules."},
        {"index":"02", "title":"Sales Trends", "text":"See what sells, how demand changes and how revenue moves over time."},
        {"index":"03", "title":"Inventory Insights", "text":"Identify stock pressure and the pricing action suggested by current conditions."},
        {"index":"04", "title":"Market Comparison", "text":"Read the current price against competitor pricing before making a decision."},
        {"index":"05", "title":"Explainable Results", "text":"Understand which features contributed to each model prediction using SHAP."},
        {"index":"06", "title":"Business Analytics", "text":"Keep the important pricing signals together in one focused workspace."},
    ])

    st.markdown("<div style='height:52px'></div>", unsafe_allow_html=True)
    a, b = st.columns([1.2, 1])
    with a:
        st.markdown('<div class="panel"><div class="section-kicker">Model snapshot</div><h3>Machine learning, followed by business rules.</h3><p class="muted">The existing project workflow remains the source of the recommendations. This frontend redesign changes the presentation layer, not the trained model or pricing logic.</p></div>', unsafe_allow_html=True)
    with b:
        avg_margin = ((df['base_price'] - df['cost_price']) / df['cost_price'] * 100).mean()
        st.metric("Average model margin", f"{avg_margin:.1f}%")
