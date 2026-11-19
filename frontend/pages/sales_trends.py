import plotly.graph_objects as go
import streamlit as st
from components import chart_box
from styles import NAVY, ACCENT, RED, GREEN, CREAM

CHART_BG='#FFFDF9'
GRID='#E5DED2'


def base_layout(fig,title=None,height=400):
    text_font={'color':NAVY,'family':'Inter, Arial, sans-serif'}
    axis_font={'color':NAVY,'size':12}
    title_font={'color':NAVY,'size':17,'family':'Inter, Arial, sans-serif'}
    fig.update_layout(
        title={'text':title,'font':title_font,'x':0.01,'xanchor':'left'} if title else None,
        height=height,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=text_font,
        xaxis={'gridcolor':GRID,'zeroline':False,'tickfont':axis_font,'title':{'font':axis_font},'linecolor':'#C8C0B4'},
        yaxis={'gridcolor':GRID,'zeroline':False,'tickfont':axis_font,'title':{'font':axis_font},'linecolor':'#C8C0B4'},
        margin={'t':60,'b':55,'l':58,'r':20},
        legend={'bgcolor':'rgba(255,253,249,.92)','font':{'color':NAVY,'size':12}}
    )
    return fig


def render(ctx):
    df=ctx['df']
    st.markdown('<div class="section-kicker">Business analytics</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sales Trends</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Follow product sales, revenue, pricing and demand patterns using the existing project data.</div>',unsafe_allow_html=True)
    st.markdown('<div style="height:22px"></div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: selected_product=st.selectbox('Product',sorted(df['product_name'].unique()))
    with c2: chart_metric=st.selectbox('Metric',['Units Sold','Revenue (₹)','Base Price vs Current Price'])
    with c3: smoothing=st.selectbox('Smoothing',['None','7-day avg','30-day avg'])
    prod=df[df['product_name']==selected_product].sort_values('date').copy()
    k1,k2,k3,k4=st.columns(4)
    with k1: st.metric('Units sold',f"{prod['units_sold'].sum():,}")
    with k2: st.metric('Average daily sales',f"{prod['units_sold'].mean():.1f}")
    with k3: st.metric('Average base price',f"₹{prod['base_price'].mean():.2f}")
    with k4: st.metric('Revenue',f"₹{prod['sales_revenue'].sum():,.0f}")
    def smooth(s): return s.rolling(7,min_periods=1).mean() if smoothing=='7-day avg' else s.rolling(30,min_periods=1).mean() if smoothing=='30-day avg' else s
    fig=go.Figure()
    if chart_metric=='Units Sold':
        fig.add_trace(go.Scatter(x=prod['date'],y=smooth(prod['units_sold']),mode='lines',name='Units sold',line={'color':ACCENT,'width':2}))
        ytitle='Units sold'
    elif chart_metric=='Revenue (₹)':
        fig.add_trace(go.Scatter(x=prod['date'],y=smooth(prod['sales_revenue']),mode='lines',name='Revenue',line={'color':GREEN,'width':2}))
        ytitle='Revenue (₹)'
    else:
        fig.add_trace(go.Scatter(x=prod['date'],y=smooth(prod['base_price']),mode='lines',name='ML base price',line={'color':ACCENT,'width':2}))
        fig.add_trace(go.Scatter(x=prod['date'],y=smooth(prod['current_price']),mode='lines',name='Current price',line={'color':RED,'width':2,'dash':'dot'}))
        ytitle='Price (₹)'
    fig.update_yaxes(title=ytitle)
    chart_box(base_layout(fig,f'{selected_product} — {chart_metric}'))
    a,b=st.columns(2)
    with a:
        d=prod.groupby('demand_level')['units_sold'].mean().reset_index()
        figd=go.Figure(go.Bar(x=d['demand_level'],y=d['units_sold'],marker_color=[ACCENT, '#B89B52', '#A35B5B'][:len(d)]))
        chart_box(base_layout(figd,'Average units sold by demand',320))
    with b:
        s=prod.groupby('season')['units_sold'].mean().reset_index()
        figs=go.Figure(go.Bar(x=s['season'],y=s['units_sold'],marker_color=ACCENT))
        chart_box(base_layout(figs,'Average units sold by season',320))
