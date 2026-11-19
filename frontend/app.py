import streamlit as st

from auth import is_authenticated, login_page, logout
from styles import inject_css, topbar

st.set_page_config(
    page_title="Smart Pricing",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# The public screen gets the business/laptop visual.
# The bakery visual is injected only after authentication.
authenticated = is_authenticated()
inject_css(authenticated=authenticated)

if not authenticated:
    login_page()
    st.stop()

# Backend/model files are loaded only after the bakery/business user signs in.
from data_loader import project_context
from pages import home, price_recommender, sales_trends, inventory_insights, know_how_we_work

ctx = project_context()

st.markdown(
    '<div class="topbar">'
    '<div class="brand">Smart Pricing <span>Pricing Intelligence</span></div>'
    '<div class="nav-note">Business pricing workspace</div>'
    '</div>',
    unsafe_allow_html=True,
)

current = st.session_state.get("page", "Overview")
choice = topbar(current, True)
st.session_state["page"] = choice

left, right = st.columns([8, 1])
with right:
    if st.button("Sign out", use_container_width=True):
        logout()
        st.rerun()

st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

if choice == "Overview":
    home.render(ctx)
elif choice == "Price Recommender":
    price_recommender.render(ctx)
elif choice == "Sales Trends":
    sales_trends.render(ctx)
elif choice == "Inventory Insights":
    inventory_insights.render(ctx)
elif choice == "Know How We Work":
    know_how_we_work.render(ctx)
