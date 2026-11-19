import streamlit as st
from styles import GREEN, AMBER, RED, ACCENT


def feature_grid(items):
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature">
              <div class="index">{item['index']}</div>
              <h3>{item['title']}</h3>
              <p>{item['text']}</p>
            </div>
            """, unsafe_allow_html=True)


def chart_box(fig, key=None, height=None):
    st.markdown('<div class="chart-frame">', unsafe_allow_html=True)
    kwargs = {"use_container_width": True, "config": {"displayModeBar": False}}
    if height is not None:
        kwargs["height"] = height
    if key is not None:
        kwargs["key"] = key
    st.plotly_chart(fig, **kwargs)
    st.markdown('</div>', unsafe_allow_html=True)


def status_text(action):
    color = {"Increase": GREEN, "Discount": RED, "Hold": AMBER}.get(action, ACCENT)
    return f'<span style="color:{color};font-weight:600;">{action}</span>'
