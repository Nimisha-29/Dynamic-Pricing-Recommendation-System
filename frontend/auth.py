import base64
import hashlib
from pathlib import Path
import streamlit as st

DEMO_BUSINESS_ID = "BUSINESS001"
DEMO_PASSWORD = "Demo@123"
DEMO_PASSWORD_HASH = hashlib.sha256(DEMO_PASSWORD.encode()).hexdigest()


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def is_authenticated():
    return bool(st.session_state.get("authenticated", False))


def logout():
    st.session_state["authenticated"] = False
    st.session_state["business_name"] = ""
    st.session_state["business_id"] = ""
    st.session_state["page"] = "Overview"
    try:
        st.query_params.clear()
    except Exception:
        pass


def _public_section():
    try:
        value = st.query_params.get("section", "home")
    except Exception:
        value = "home"
    value = str(value).lower()
    return value if value in {"home", "features", "about", "contact"} else "home"


def _public_nav(section):
    return f"""
    <header class="public-nav">
      <a class="public-brand" href="?section=home">
        <span class="public-brand-mark">SP</span>
        <span>Smart Pricing</span>
      </a>
      <nav class="public-links">
        <a class="{'active' if section == 'home' else ''}" href="?section=home">Home</a>
        <a class="{'active' if section == 'features' else ''}" href="?section=features">Features</a>
        <a class="{'active' if section == 'about' else ''}" href="?section=about">About</a>
        <a class="{'active' if section == 'contact' else ''}" href="?section=contact">Contact</a>
      </nav>
    </header>
    """


def _public_intro():
    st.markdown(
        """
        <section class="landing-hero">
          <div class="landing-hero-overlay"></div>
          <div class="landing-hero-content">
            <div class="landing-kicker">AI-POWERED BUSINESS PRICING</div>
            <h1>Smart Pricing</h1>
            <p class="landing-tagline">Turn every pricing decision into a smarter business decision.</p>
            <p class="landing-copy">Use demand, sales, inventory and market signals to understand what is happening in your business and price with clarity.</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _public_content(section):
    if section == "features":
        st.markdown(
            """
            <section class="public-subpage">
              <div class="public-subpage-inner">
                <div class="public-content-kicker">PLATFORM FEATURES</div>
                <h2>One workspace for the signals behind your price.</h2>
                <p>Smart Pricing connects model-driven recommendations with the sales and inventory context that helps a business understand each pricing decision.</p>
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
    elif section == "about":
        st.markdown(
            """
            <section class="public-subpage">
              <div class="public-subpage-inner narrow">
                <div class="public-content-kicker">ABOUT SMART PRICING</div>
                <h2>Pricing intelligence built for practical business decisions.</h2>
                <p>The system combines machine-learning price prediction, business pricing rules, sales trends, inventory signals and explainability in one focused workspace.</p>
                <div class="about-lines">
                  <div><strong>01</strong><span>Business data → model prediction → pricing rules → recommendation</span></div>
                  <div><strong>02</strong><span>Sales, demand, inventory and competitor signals reviewed together</span></div>
                </div>
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
    elif section == "contact":
        st.markdown(
            """
            <section class="public-subpage">
              <div class="public-subpage-inner narrow contact-content">
                <div class="public-content-kicker">CONTACT</div>
                <h2>Let’s talk about smarter pricing.</h2>
                <p>For a project demonstration or questions about the pricing workspace, use the contact details below.</p>
                <div class="contact-grid">
                  <div><span>Email</span><strong>pricing@smartpricing.demo</strong></div>
                  <div><span>Workspace</span><strong>Business Pricing Intelligence</strong></div>
                </div>
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )


def _asset_uri(filename):
    path = Path(__file__).parent / "assets" / filename
    if not path.exists():
        return ""
    return "data:image/svg+xml;base64," + base64.b64encode(path.read_bytes()).decode()


def _landing_feature_sections():
    sections = [
        ("01", "Dynamic Pricing", "Move beyond fixed prices. The existing pricing model combines product, demand, stock, competitor and sales signals to produce a practical recommended price.", "pricing_visual.svg", "image-left"),
        ("02", "Sales Trends", "See how units sold, revenue and pricing change over time. Product-level trends make it easier to spot demand movement before changing a price.", "sales_visual.svg", "image-right"),
        ("03", "Inventory Insights", "Connect stock levels with demand and recommended actions. Quickly identify products where inventory conditions create pricing pressure.", "inventory_visual.svg", "image-left"),
        ("04", "Explainable Results", "Understand the factors behind a model prediction with SHAP-based explainability, so the recommendation is supported by visible evidence.", "explain_visual.svg", "image-right"),
    ]
    for num, title, text, image, layout in sections:
        st.markdown(
            f"""
            <section class="feature-story {layout}">
              <div class="feature-story-visual"><img src="{_asset_uri(image)}" alt="{title} illustration"></div>
              <div class="feature-story-copy">
                <div class="story-number">{num}</div>
                <h2>{title}</h2>
                <p>{text}</p>
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )


def login_page():
    section = _public_section()

    st.markdown('<div class="landing-shell">', unsafe_allow_html=True)
    st.markdown(_public_nav(section), unsafe_allow_html=True)

    if section == "home":
        _public_intro()
        st.markdown('<div class="login-zone"><div class="login-zone-title">Business access</div><h2>Sign in to your pricing workspace</h2><p>Use your business credentials to open the analytics dashboard.</p></div>', unsafe_allow_html=True)
    else:
        _public_content(section)
        st.markdown('<div class="login-zone compact"><div class="login-zone-title">Business access</div><h2>Sign in to your pricing workspace</h2></div>', unsafe_allow_html=True)

    with st.container():
        _, center, _ = st.columns([1.1, 1.35, 1.1])
        with center:
            with st.form("business_login_form", clear_on_submit=False):
                st.markdown('<div class="login-heading"><div class="login-kicker">BUSINESS ACCESS</div><h2>Sign In</h2><p>Access your business dashboard and start optimizing your prices.</p></div>', unsafe_allow_html=True)
                business_id = st.text_input("Business ID", placeholder="Enter your business ID")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In", use_container_width=True)
                st.markdown(f'<div class="demo-divider"><span>Demo Access</span></div><div class="demo-box"><span>Business ID</span><b>{DEMO_BUSINESS_ID}</b><i>|</i><span>Password</span><b>{DEMO_PASSWORD}</b></div>', unsafe_allow_html=True)

    if section == "home":
        st.markdown('<section class="stories-wrap"><div class="stories-intro"><div class="public-content-kicker">WHAT YOU CAN DO</div><h2>See the business signals behind every pricing decision.</h2><p>Explore the main capabilities before you sign in. The pages inside the workspace continue to use your existing backend, model and data.</p></div>', unsafe_allow_html=True)
        _landing_feature_sections()
        st.markdown('</section>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if business_id.strip().upper() == DEMO_BUSINESS_ID and _hash(password) == DEMO_PASSWORD_HASH:
            st.session_state["authenticated"] = True
            st.session_state["business_name"] = "Demo Business"
            st.session_state["business_id"] = DEMO_BUSINESS_ID
            st.session_state["page"] = "Overview"
            try:
                st.query_params.clear()
            except Exception:
                pass
            st.rerun()
        else:
            st.error("The Business ID or password is incorrect.")

