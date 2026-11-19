import streamlit as st


def render(ctx):
    df = ctx["df"]
    st.markdown('<div class="section-kicker">System architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Know How We Work</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">A concise view of the pipeline behind the recommendations, using the actual project components.</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="dark-band">
          <div class="section-kicker-light">THE PRICING PIPELINE</div>
          <h2>From business data to a practical price</h2>
          <p>The frontend is the presentation layer. The existing trained model, feature engineering, pricing rules and SHAP explanation remain unchanged in the project backend.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    steps = [
        ("01", "Data collection", "Product, price, competitor, stock, sales, demand and seasonal fields enter the dataset."),
        ("02", "Data processing", "The existing preprocessing and feature engineering prepare the model inputs."),
        ("03", "Machine learning", "The trained Random Forest model predicts a base price from the feature set used during training."),
        ("04", "Recommendation engine", "The base prediction is passed through the existing inventory, competitor, demand and margin rules."),
        ("05", "Explainability", "SHAP values are used to show which features contributed to the prediction."),
        ("06", "Business view", "The frontend presents the recommendation alongside sales and inventory context."),
    ]
    for num, title, body in steps:
        st.markdown(
            f"""
            <div class="system-step">
              <div class="section-kicker">{num}</div>
              <h3>{title}</h3>
              <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title" style="font-size:1.55rem;margin-top:34px;">Project data snapshot</div>', unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Records", f"{len(df):,}")
    with k2:
        st.metric("Products", f"{df['product_name'].nunique()}")
    with k3:
        st.metric("Date range", f"{df['date'].min().date()} → {df['date'].max().date()}")
