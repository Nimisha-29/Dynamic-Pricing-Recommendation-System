import base64
from pathlib import Path
import streamlit as st

NAVY = "#111B35"
NAVY_2 = "#1B294B"
CREAM = "#F7F2E8"
CREAM_2 = "#EDE5D7"
INK = "#111B35"
MUTED = "#5F6675"
WHITE = "#FFFFFF"
ACCENT = "#6574D8"
LINE = "rgba(17,27,53,.18)"
GREEN = "#2E6B55"
AMBER = "#A36B19"
RED = "#A84444"


def _data_uri(filename):
    path = Path(__file__).parent / "assets" / filename
    if not path.exists():
        return ""
    suffix = path.suffix.lower().replace(".", "") or "png"
    return f"data:image/{suffix};base64," + base64.b64encode(path.read_bytes()).decode()


def inject_css(authenticated=False):
    bakery = _data_uri("bakery_hero.png")
    public = _data_uri("business_hero.png")

    # The bakery photograph remains the authenticated workspace background.
    # The public business photograph is used only in the top landing hero.
    app_background = (
        f"linear-gradient(rgba(247,242,232,.72),rgba(247,242,232,.82)), url('{bakery}')"
        if authenticated
        else "linear-gradient(#f5f6fa,#f5f6fa)"
    )

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap');

        :root {{
          --navy:{NAVY}; --navy2:{NAVY_2}; --cream:{CREAM}; --cream2:{CREAM_2};
          --ink:{INK}; --muted:{MUTED}; --line:{LINE}; --accent:{ACCENT};
        }}
        * {{ box-sizing:border-box; }}
        .stApp {{ background:{app_background} center/cover fixed; color:var(--ink); }}
        .main .block-container {{ max-width:1440px; padding:0 3.2rem 4rem; }}
        [data-testid="stHeader"] {{ background:transparent; }}
        [data-testid="stToolbar"] {{ visibility:hidden; height:0; }}
        footer {{ visibility:hidden; }}
        html, body, [class*="css"] {{ font-family:'Inter',sans-serif; }}
        h1,h2,h3,h4 {{ color:var(--ink) !important; font-family:'Inter',sans-serif; letter-spacing:-.035em; }}
        p, label, [data-testid="stMarkdownContainer"] {{ color:var(--ink); }}
        .muted {{ color:var(--muted) !important; }}

        /* AUTHENTICATED WORKSPACE */
        .topbar {{
          min-height:76px; display:flex; align-items:center; justify-content:space-between;
          border-bottom:1px solid var(--line); margin:0 -3.2rem; padding:0 3.2rem;
          background:rgba(247,242,232,.97); position:relative; z-index:5;
        }}
        .brand {{ font-weight:700; letter-spacing:-.04em; font-size:1.18rem; color:var(--ink); }}
        .brand span {{ color:var(--accent); font-weight:500; margin-left:8px; }}
        .nav-note {{ font-size:.76rem; letter-spacing:.10em; text-transform:uppercase; color:var(--muted); }}
        div[role="radiogroup"] {{ gap:1.5rem; align-items:center; }}
        div[role="radiogroup"] label {{
          border:0 !important; background:transparent !important; padding:7px 0 !important;
          border-radius:0 !important; color:var(--muted) !important; font-size:.82rem !important;
          transition:color .22s ease,transform .22s ease !important;
        }}
        div[role="radiogroup"] label:hover {{ color:var(--ink) !important; transform:translateY(-2px); }}
        div[role="radiogroup"] label[data-checked="true"], div[role="radiogroup"] label:has(input:checked) {{ color:var(--ink) !important; font-weight:700 !important; }}

        .hero {{
          min-height:600px; position:relative; overflow:hidden; margin:24px 0 54px;
          background-image:linear-gradient(90deg,rgba(10,13,30,.72) 0%,rgba(10,13,30,.48) 46%,rgba(10,13,30,.18) 100%),url('{bakery}');
          background-size:cover; background-position:center; display:flex; align-items:center;
          border:1px solid rgba(17,27,53,.22); transition:transform .35s ease,box-shadow .35s ease;
        }}
        .hero:hover {{ transform:scale(1.004); box-shadow:0 22px 48px rgba(17,27,53,.15); }}
        .hero-copy {{ max-width:760px; padding:72px; color:#fff; }}
        .eyebrow {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.18em; font-weight:600; color:rgba(255,255,255,.84); margin-bottom:22px; }}
        .hero h1 {{ color:#fff !important; font-family:'DM Serif Display',Georgia,serif; font-size:clamp(3.1rem,6vw,6rem); line-height:.94; letter-spacing:-.045em; margin:0 0 24px; font-weight:400; }}
        .hero p {{ color:rgba(255,255,255,.92) !important; max-width:650px; font-size:1rem; line-height:1.75; margin:0 0 30px; }}
        .hero-meta {{ display:flex; gap:28px; margin-top:34px; padding-top:18px; border-top:1px solid rgba(255,255,255,.35); }}
        .hero-meta strong {{ display:block; color:#fff; font-size:1.1rem; }}
        .hero-meta span {{ color:rgba(255,255,255,.78); font-size:.72rem; text-transform:uppercase; letter-spacing:.1em; }}

        /* BUTTONS */
        div.stButton > button, div[data-testid="stFormSubmitButton"] button {{
          border-radius:2px !important; border:1px solid var(--navy) !important; background:var(--navy) !important;
          color:#FFFFFF !important; min-height:46px; font-weight:700; letter-spacing:.01em;
          transition:background .25s ease,color .25s ease,transform .25s ease,box-shadow .25s ease !important;
          box-shadow:0 4px 0 rgba(17,27,53,.15) !important;
        }}
        div.stButton > button *, div[data-testid="stFormSubmitButton"] button * {{ color:#FFFFFF !important; }}
        div.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover {{
          background:var(--accent) !important; border-color:var(--accent) !important; color:#FFFFFF !important;
          transform:translateY(-4px) !important; box-shadow:0 14px 26px rgba(17,27,53,.22) !important;
        }}
        div.stButton > button:hover *, div[data-testid="stFormSubmitButton"] button:hover * {{ color:#FFFFFF !important; }}

        div[data-baseweb="select"] > div, input, textarea {{
          border-radius:2px !important; border:1px solid rgba(17,27,53,.24) !important;
          background:#FFFDF9 !important; color:var(--ink) !important; min-height:44px;
        }}
        input::placeholder {{ color:#7B808B !important; opacity:1 !important; }}
        div[data-baseweb="select"] > div:focus-within, input:focus, textarea:focus {{
          border-color:var(--accent) !important; box-shadow:0 0 0 2px rgba(101,116,216,.15) !important;
        }}
        [data-testid="stForm"] {{ border:0 !important; padding:0 !important; }}

        .section-kicker {{ color:var(--muted); text-transform:uppercase; letter-spacing:.16em; font-size:.7rem; font-weight:700; margin-bottom:8px; }}
        .section-title {{ font-size:2.1rem; font-weight:600; margin:0 0 8px; }}
        .section-copy {{ color:var(--muted) !important; line-height:1.7; max-width:720px; }}
        .section-kicker-light {{ color:rgba(255,255,255,.78); text-transform:uppercase; letter-spacing:.16em; font-size:.68rem; font-weight:700; margin-bottom:8px; }}

        .panel {{ background:rgba(255,255,255,.96); border:1px solid var(--line); padding:28px; border-radius:2px; transition:transform .28s ease,border-color .28s ease,box-shadow .28s ease; }}
        .panel:hover {{ transform:translateY(-5px); border-color:rgba(17,27,53,.34); box-shadow:0 18px 38px rgba(17,27,53,.11); }}
        .feature {{ background:#FFFDF9; border-top:2px solid var(--ink); padding:24px; min-height:210px; transition:transform .28s ease,box-shadow .28s ease,border-color .28s ease; }}
        .feature:hover {{ transform:translateY(-7px); border-top-color:var(--accent); box-shadow:0 18px 38px rgba(17,27,53,.13); }}
        .feature .index {{ color:var(--muted); font-size:.7rem; letter-spacing:.12em; }}
        .feature h3 {{ margin:30px 0 10px; font-size:1.18rem; letter-spacing:-.02em; }}
        .feature p {{ color:var(--muted) !important; line-height:1.65; font-size:.88rem; margin:0; }}
        [data-testid="stMetric"] {{ background:#FFFDF9 !important; border:1px solid var(--line); border-radius:2px; padding:22px 20px !important; transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease; }}
        [data-testid="stMetric"] * {{ color:var(--ink) !important; opacity:1 !important; }}
        [data-testid="stMetric"]:hover {{ transform:translateY(-5px); border-color:rgba(17,27,53,.32); box-shadow:0 14px 30px rgba(17,27,53,.10); }}
        [data-testid="stMetricLabel"] {{ color:var(--muted) !important; font-size:.72rem !important; text-transform:uppercase; letter-spacing:.09em; }}
        [data-testid="stMetricValue"] {{ color:var(--ink) !important; font-size:1.7rem !important; letter-spacing:-.04em; }}
        [data-testid="stMetricDelta"] {{ color:var(--muted) !important; }}
        [data-testid="stDataFrame"] {{ border:1px solid var(--line); border-radius:2px; overflow:hidden; background:#FFFDF9; }}
        .chart-frame {{ background:#FFFDF9; border:1px solid var(--line); padding:8px; border-radius:2px; transition:box-shadow .28s ease,border-color .28s ease; }}
        /* Keep Plotly titles, axis labels, ticks and legends readable on the light chart surface. */
        .chart-frame .js-plotly-plot, .chart-frame .plot-container {{ color:var(--ink) !important; }}
        .chart-frame .js-plotly-plot text, .chart-frame .js-plotly-plot .xtick text, .chart-frame .js-plotly-plot .ytick text, .chart-frame .js-plotly-plot .gtitle, .chart-frame .js-plotly-plot .axis-title, .chart-frame .js-plotly-plot .legendtext {{ fill:var(--ink) !important; color:var(--ink) !important; }}
        .chart-frame .js-plotly-plot .xaxislayer-above text, .chart-frame .js-plotly-plot .yaxislayer-above text {{ fill:var(--ink) !important; }}
        .chart-frame .js-plotly-plot .legendtext {{ fill:var(--ink) !important; }}
        .chart-frame:hover {{ border-color:rgba(17,27,53,.30); box-shadow:0 14px 30px rgba(17,27,53,.09); }}
        [data-testid="stAlert"] {{ background:rgba(255,253,249,.97) !important; color:var(--ink) !important; border:1px solid var(--line) !important; }}
        [data-testid="stAlert"] * {{ color:var(--ink) !important; }}
        
        /* PUBLIC LANDING */
        .landing-shell {{ margin:0 -3.2rem; }}
        .public-nav {{
          position:relative; z-index:10; height:78px; padding:0 3.2rem;
          display:flex; align-items:center; justify-content:space-between;
          background:#fff; border-bottom:1px solid rgba(17,27,53,.10);
        }}
        .public-brand {{ display:flex; align-items:center; gap:12px; color:var(--ink) !important; text-decoration:none !important; font-size:1.18rem; font-weight:700; letter-spacing:-.035em; }}
        .public-brand-mark {{ width:34px; height:34px; display:inline-flex; align-items:center; justify-content:center; border:1.5px solid var(--ink); color:var(--ink); font-size:.64rem; font-weight:700; letter-spacing:-.02em; }}
        .public-links {{ display:flex; align-items:center; gap:34px; font-size:.82rem; }}
        .public-links a {{ color:#2D3445 !important; text-decoration:none !important; padding:9px 0; border-bottom:2px solid transparent; transition:color .25s ease,transform .25s ease,border-color .25s ease; }}
        .public-links a:hover {{ color:var(--ink) !important; transform:translateY(-2px); border-bottom-color:var(--accent); }}
        .public-links a.active {{ color:var(--ink) !important; border-bottom-color:var(--accent); font-weight:700; }}

        .landing-hero {{
          position:relative; min-height:650px; overflow:hidden;
          background-image:url('{public}'); background-size:cover; background-position:center 48%;
          display:flex; align-items:center; justify-content:center; text-align:center;
        }}
        .landing-hero-overlay {{ position:absolute; inset:0; background:linear-gradient(90deg,rgba(9,15,32,.73),rgba(9,15,32,.47),rgba(9,15,32,.68)); }}
        .landing-hero-content {{ position:relative; z-index:2; width:min(900px,92%); padding:72px 30px 82px; }}
        .landing-kicker {{ color:#D8DDFB; font-size:.72rem; font-weight:700; letter-spacing:.24em; margin-bottom:18px; }}
        .landing-hero h1 {{ color:#fff !important; font-family:'DM Serif Display',Georgia,serif !important; font-size:clamp(4rem,8vw,7.3rem); font-weight:400; line-height:.92; letter-spacing:-.055em; margin:0; text-shadow:0 4px 25px rgba(0,0,0,.35); }}
        .landing-tagline {{ color:#fff !important; font-size:clamp(1.35rem,2.4vw,2rem); font-weight:600; line-height:1.25; margin:24px auto 0; max-width:760px; text-shadow:0 2px 16px rgba(0,0,0,.45); }}
        .landing-copy {{ color:rgba(255,255,255,.91) !important; max-width:650px; margin:18px auto 0; line-height:1.7; font-size:1rem; text-shadow:0 2px 12px rgba(0,0,0,.40); }}

        .login-zone {{ text-align:center; margin:42px auto 22px; max-width:820px; padding:0 20px; }}
        .login-zone.compact {{ margin-top:34px; }}
        .login-zone-title {{ color:#5969C8; font-size:.68rem; font-weight:700; text-transform:uppercase; letter-spacing:.18em; }}
        .login-zone h2 {{ margin:8px 0 5px; font-size:2rem; }}
        .login-zone p {{ margin:0; color:var(--muted) !important; line-height:1.6; }}
        div[data-testid="stForm"] {{
          width:100%; max-width:520px; margin:0 auto 48px; padding:30px 34px 25px !important;
          background:#111B35 !important; border:1px solid rgba(17,27,53,.16) !important; border-radius:3px !important;
          box-shadow:0 25px 65px rgba(17,27,53,.24) !important; transition:transform .32s ease,box-shadow .32s ease,border-color .32s ease;
        }}
        div[data-testid="stForm"]:hover {{ transform:translateY(-7px); box-shadow:0 35px 78px rgba(17,27,53,.31) !important; border-color:rgba(255,255,255,.28) !important; }}
        .login-heading {{ text-align:center; margin-bottom:18px; }}
        .login-kicker {{ color:#BFC7F5; font-size:.63rem; font-weight:700; letter-spacing:.18em; margin-bottom:8px; }}
        .login-heading h2 {{ margin:0 0 5px; color:#fff !important; font-size:1.9rem; letter-spacing:-.03em; }}
        .login-heading p {{ margin:0 auto; max-width:370px; color:rgba(255,255,255,.78) !important; font-size:.81rem; line-height:1.5; }}
        div[data-testid="stForm"] label, div[data-testid="stForm"] label p, div[data-testid="stForm"] label span {{ color:#fff !important; font-size:.78rem !important; font-weight:600 !important; opacity:1 !important; }}
        div[data-testid="stForm"] input {{ background:#fff !important; color:var(--ink) !important; border:1px solid rgba(255,255,255,.35) !important; border-radius:2px !important; min-height:44px; }}
        div[data-testid="stForm"] input::placeholder {{ color:#707786 !important; opacity:1 !important; }}
        div[data-testid="stForm"] [data-testid="stFormSubmitButton"] button {{ min-height:46px; margin-top:8px; background:#6574D8 !important; color:#fff !important; border:1px solid #7E8AE5 !important; }}
        div[data-testid="stForm"] [data-testid="stFormSubmitButton"] button * {{ color:#fff !important; opacity:1 !important; }}
        div[data-testid="stForm"] [data-testid="stFormSubmitButton"] button:hover {{ background:#7D89E8 !important; transform:translateY(-3px); box-shadow:0 12px 24px rgba(0,0,0,.24); }}
        .demo-divider {{ display:flex; align-items:center; gap:12px; margin:20px 0 12px; color:rgba(255,255,255,.58); font-size:.69rem; }}
        .demo-divider:before,.demo-divider:after {{ content:""; height:1px; flex:1; background:rgba(255,255,255,.25); }}
        .demo-box {{ min-height:42px; display:flex; align-items:center; justify-content:center; gap:7px; border:1px solid rgba(255,255,255,.20); background:rgba(255,255,255,.045); padding:9px 10px; color:rgba(255,255,255,.65); font-size:.66rem; }}
        .demo-box b {{ color:#fff; font-weight:600; }} .demo-box i {{ color:rgba(255,255,255,.35); font-style:normal; margin:0 3px; }}

        .stories-wrap {{ background:#f5f6fa; padding:68px 3.2rem 84px; border-top:1px solid rgba(17,27,53,.08); }}
        .stories-intro {{ max-width:900px; margin:0 auto 55px; text-align:center; }}
        .stories-intro h2 {{ margin:8px 0 12px; font-size:clamp(2.1rem,4vw,3.4rem); line-height:1.03; }}
        .stories-intro p {{ max-width:720px; margin:0 auto; color:var(--muted) !important; line-height:1.75; }}
        .feature-story {{ width:min(1160px,100%); margin:0 auto; min-height:390px; display:grid; grid-template-columns:1fr 1fr; align-items:center; gap:70px; padding:58px 0; border-top:1px solid rgba(17,27,53,.12); }}
        .feature-story:first-of-type {{ border-top:0; }}
        .feature-story.image-right .feature-story-visual {{ order:2; }}
        .feature-story.image-right .feature-story-copy {{ order:1; }}
        .feature-story-visual {{ background:#fff; border:1px solid rgba(17,27,53,.12); padding:18px; box-shadow:0 18px 45px rgba(17,27,53,.08); transition:transform .35s ease,box-shadow .35s ease; }}
        .feature-story-visual:hover {{ transform:translateY(-8px); box-shadow:0 28px 55px rgba(17,27,53,.14); }}
        .feature-story-visual img {{ display:block; width:100%; height:auto; }}
        .feature-story-copy {{ padding:20px 15px; max-width:520px; }}
        .story-number {{ color:#6574D8; font-size:.72rem; font-weight:700; letter-spacing:.18em; margin-bottom:16px; }}
        .feature-story-copy h2 {{ margin:0 0 16px; font-family:'DM Serif Display',Georgia,serif !important; font-size:3.2rem; line-height:.98; font-weight:400; }}
        .feature-story-copy p {{ margin:0; color:#5C6473 !important; font-size:1.02rem; line-height:1.8; }}

        .public-subpage {{ background:#f5f6fa; padding:62px 3.2rem 30px; }}
        .public-subpage-inner {{ width:min(1000px,100%); margin:0 auto; padding:44px 48px; background:#fff; border:1px solid rgba(17,27,53,.12); box-shadow:0 18px 42px rgba(17,27,53,.08); }}
        .public-subpage-inner.narrow {{ width:min(820px,100%); }}
        .public-content-kicker {{ color:#5969C8; font-size:.68rem; font-weight:700; letter-spacing:.18em; margin-bottom:10px; }}
        .public-subpage h2 {{ margin:0 0 15px; font-family:'DM Serif Display',Georgia,serif !important; font-size:3.2rem; line-height:1; font-weight:400; }}
        .public-subpage p {{ color:#566071 !important; line-height:1.75; max-width:760px; margin:0 0 24px; }}
        .about-lines {{ border-top:1px solid rgba(17,27,53,.16); margin-top:30px; }}
        .about-lines div {{ display:flex; gap:24px; padding:18px 0; border-bottom:1px solid rgba(17,27,53,.16); }}
        .about-lines strong {{ color:#6574D8; width:35px; }} .about-lines span {{ color:#374157; }}
        .contact-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:1px; background:rgba(17,27,53,.16); border:1px solid rgba(17,27,53,.16); margin-top:28px; }}
        .contact-grid div {{ background:#fff; padding:24px; }} .contact-grid span {{ display:block; color:#707786; text-transform:uppercase; font-size:.66rem; letter-spacing:.12em; margin-bottom:8px; }} .contact-grid strong {{ color:#111B35; font-size:.92rem; }}

        /* Pricing workspace */
        .st-key-pricing_form_shell {{ width:100%; }}
        .st-key-pricing_form_shell div[data-testid="stForm"] {{ width:100%; max-width:none; margin:0; padding:28px !important; background:rgba(255,253,249,.97) !important; border:1px solid rgba(17,27,53,.18) !important; border-radius:2px !important; box-shadow:0 16px 36px rgba(17,27,53,.10) !important; }}
        .st-key-pricing_form_shell div[data-testid="stForm"] label, .st-key-pricing_form_shell div[data-testid="stForm"] label p, .st-key-pricing_form_shell div[data-testid="stForm"] label span {{ color:var(--ink) !important; opacity:1 !important; }}
        .st-key-pricing_form_shell div[data-testid="stForm"] [data-testid="stFormSubmitButton"] button {{ background:var(--navy) !important; color:#fff !important; border-color:var(--navy) !important; }}
        .st-key-pricing_form_shell div[data-testid="stForm"] [data-testid="stFormSubmitButton"] button * {{ color:#fff !important; }}
        .pricing-section-title {{ color:var(--ink); font-size:.78rem; font-weight:700; text-transform:uppercase; letter-spacing:.13em; margin:10px 0 14px; }}

        .dark-band {{ background:var(--navy); color:#fff; margin:40px 0; padding:48px 54px; }}
        .dark-band h2,.dark-band h3 {{ color:#fff !important; }}
        .dark-band p {{ color:rgba(255,255,255,.84) !important; }}
        .system-step {{ background:rgba(255,255,255,.96); border:1px solid var(--line); padding:24px; margin:0 0 14px; }}
        .system-step h3 {{ margin:0 0 7px; }} .system-step p {{ margin:0; color:var(--muted) !important; line-height:1.7; }}

        @media (max-width:900px) {{
          .main .block-container {{ padding:0 1.2rem 3rem; }}
          .topbar {{ margin:0 -1.2rem; padding:0 1.2rem; }}
          .landing-shell {{ margin:0 -1.2rem; }}
          .public-nav {{ padding:0 1.2rem; }}
          .public-links {{ gap:16px; }}
          .landing-hero {{ min-height:590px; }}
          .landing-hero-content {{ padding:55px 20px; }}
          .stories-wrap,.public-subpage {{ padding-left:1.2rem; padding-right:1.2rem; }}
          .feature-story {{ grid-template-columns:1fr; gap:25px; padding:45px 0; }}
          .feature-story.image-right .feature-story-visual,.feature-story.image-right .feature-story-copy {{ order:initial; }}
          .feature-story-copy {{ max-width:none; }}
          .hero-copy {{ padding:42px 30px; }}
          .hero h1 {{ font-size:3.2rem; }}
        }}
        @media (max-width:650px) {{
          .public-links {{ display:none; }}
          .public-brand {{ margin:auto; }}
          .landing-hero {{ min-height:540px; }}
          .landing-hero h1 {{ font-size:4rem; }}
          .landing-tagline {{ font-size:1.25rem; }}
          .feature-story-copy h2 {{ font-size:2.5rem; }}
          .public-subpage-inner {{ padding:28px 22px; }}
          .public-subpage h2 {{ font-size:2.4rem; }}
          .contact-grid {{ grid-template-columns:1fr; }}
          div[data-testid="stForm"] {{ padding:25px 20px 22px !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def topbar(current, authenticated):
    pages = ["Overview", "Price Recommender", "Sales Trends", "Inventory Insights", "Know How We Work"]
    if authenticated:
        return st.radio(
            "Navigation", pages,
            index=pages.index(current) if current in pages else 0,
            horizontal=True,
            label_visibility="collapsed",
            key="top_navigation",
        )
    return current


def page_header(kicker, title, copy):
    st.markdown(f'<div class="section-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if copy:
        st.markdown(f'<div class="section-copy">{copy}</div>', unsafe_allow_html=True)
