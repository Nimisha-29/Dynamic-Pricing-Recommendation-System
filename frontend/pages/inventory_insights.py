import plotly.graph_objects as go
import streamlit as st
from backend.pricing_rules import get_final_recommended_price
from components import chart_box, status_text
from styles import NAVY, GREEN, RED, AMBER, ACCENT


def render(ctx):
    df=ctx['df']
    st.markdown('<div class="section-kicker">Stock intelligence</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Inventory Insights</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-copy">See where current stock and demand conditions create pressure to increase, hold or discount prices.</div>',unsafe_allow_html=True)
    latest=df['date'].max(); snap=df[df['date']==latest].copy()
    actions=[]; prices=[]
    for _,row in snap.iterrows():
        fp,act,_=get_final_recommended_price(base_price=row['base_price'],cost_price=row['cost_price'],competitor_price=row['competitor_price'],opening_stock=row['opening_stock'],units_sold=row['units_sold'],demand_level=row['demand_level'])
        actions.append(act); prices.append(round(fp,2))
    snap['action']=actions; snap['recommended_price']=prices; snap['price_delta']=(snap['recommended_price']-snap['current_price']).round(2); snap['margin_pct']=((snap['recommended_price']-snap['cost_price'])/snap['cost_price']*100).round(1)
    k1,k2,k3,k4=st.columns(4)
    with k1: st.metric('Discount',f"{(snap.action=='Discount').sum()}")
    with k2: st.metric('Increase',f"{(snap.action=='Increase').sum()}")
    with k3: st.metric('Hold',f"{(snap.action=='Hold').sum()}")
    with k4: st.metric('Average margin',f"{snap.margin_pct.mean():.1f}%")
    colors={'Discount':RED,'Increase':GREEN,'Hold':AMBER}
    fig=go.Figure()
    fig.add_trace(go.Bar(name='Opening stock',x=snap['product_name'],y=snap['opening_stock'],marker_color='rgba(89,100,217,.28)'))
    fig.add_trace(go.Bar(name='Closing stock',x=snap['product_name'],y=snap['closing_stock'],marker_color=[colors.get(a,ACCENT) for a in snap['action']]))
    fig.update_layout(
        barmode='group',
        height=430,
        paper_bgcolor='#FFFDF9',
        plot_bgcolor='#FFFDF9',
        font={'color':NAVY,'family':'Inter, Arial, sans-serif'},
        title={'text':'Current stock by product','font':{'color':NAVY,'size':17,'family':'Inter, Arial, sans-serif'},'x':0.01,'xanchor':'left'},
        xaxis={'tickangle':-35,'gridcolor':'#E5DED2','tickfont':{'color':NAVY,'size':11},'title':{'font':{'color':NAVY,'size':12}},'linecolor':'#C8C0B4'},
        yaxis={'title':'Units','gridcolor':'#E5DED2','tickfont':{'color':NAVY,'size':11},'title':{'font':{'color':NAVY,'size':12}},'linecolor':'#C8C0B4'},
        legend={'bgcolor':'rgba(255,253,249,.92)','font':{'color':NAVY,'size':12}},
        margin={'t':55,'b':85,'l':58,'r':20}
    )
    chart_box(fig)
    table=snap[['product_name','category','demand_level','opening_stock','closing_stock','units_sold','current_price','recommended_price','price_delta','margin_pct','action']].rename(columns={'product_name':'Product','category':'Category','demand_level':'Demand','opening_stock':'Open Stock','closing_stock':'Close Stock','units_sold':'Sold','current_price':'Current (₹)','recommended_price':'Recommended (₹)','price_delta':'Change (₹)','margin_pct':'Margin %','action':'Action'})
    st.dataframe(table,use_container_width=True,height=500,hide_index=True)
