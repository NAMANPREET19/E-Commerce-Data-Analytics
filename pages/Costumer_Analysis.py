import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import sqlite3

conn = sqlite3.connect("superstore.db")
dataset="Sample - Superstore.csv"
data = pd.read_csv(dataset,encoding="latin1")


data['Order Date']=pd.to_datetime(data['Order Date'])
data['Ship Date']=pd.to_datetime(data['Ship Date'])
order_date=pd.DatetimeIndex(data['Order Date'])
ship_date=pd.DatetimeIndex(data['Ship Date'])
data['Order Month']= data['Order Date'].dt.month
data['Order Year']=data['Order Date'].dt.year


query="""
SELECT "Customer Name", SUM(Sales) as Revenue
FROM Orders
GROUP BY "Customer Name"
ORDER BY Revenue Desc
LIMIT 20
"""

query2="""
SELECT "Customer Name", SUM(Profit) AS Profits
FROM Orders
GROUP BY "Customer Name"
ORDER BY Profits Desc
LIMIT 20 
"""

# repeat costumers
query3="""
SELECT "Customer Name", COUNT(*) AS Total
FROM Orders
GROUP BY "Customer Name" 
Having COUNT(*)>1
ORDER BY Total Desc
"""

# one time customer
query4 = """
SELECT
    "Customer Name"
FROM Orders
GROUP BY "Customer Name"
HAVING COUNT(*) = 1
"""

one_time_customers = pd.read_sql(query, conn)
top_customers = pd.read_sql(query, conn)
profit_cstmr= pd.read_sql(query2, conn)
repeat_customers=pd.read_sql(query3, conn)
onetime_customers=pd.read_sql(query4, conn)
repeat_count = len(repeat_customers)
one_time_count = len(one_time_customers)
pie_df = pd.DataFrame({
    "Customer Type": ["Repeat", "One-Time"],
    "Count": [repeat_count, one_time_count]
})


st.markdown("""
<h1 style="margin-bottom:0; color:#8FD6E1; text-align:center;
font-size:50px;
font-weight:bold;
text-shadow:
    0px 2px 4px rgba(0,0,0,0.2),
    0px 4px 8px rgba(0,0,0,0.1);">
📊 Costumer Analysis
</h1>

<p style="
font-size:16px;
color:#808080;
text-align:center;
">
Explore sales trends, profit insights, and business performance metrics
</p>
""", unsafe_allow_html=True)

st.divider()
# costumer segmentation
max_date = data['Order Date'].max()
rfm = data.groupby('Customer ID').agg({
    'Order Date': lambda x : (max_date-x.max()).days ,

    'Order ID':'nunique',
     'Sales':'sum'
})

rfm.columns = [
    'Recency',
    'Frequency',
    'Monetary'
]

rfm.reset_index(inplace=True)

rfm['M_Score'] = pd.qcut(
    rfm['Monetary'],
    4,
    labels=[1,2,3,4]
)

rfm['F_Score'] = pd.qcut(
    rfm['Frequency'].rank(method='first'),
    4,
    labels=[1,2,3,4]
)

rfm['R_Score'] = pd.qcut(
    rfm['Recency'],
    4,
    labels=[4,3,2,1]
)
# Recent customers get higher score.

def segment(i):
    if(
        i['M_Score']>=3
        and i['F_Score']>=3
        and i['R_Score']==4
    ):
        return "VIP"
    elif(
        i['F_Score'] >= 3
    ):
        return "LOYAL"
    elif(
        i['R_Score'] == 1
    ):
        return "RISK"
    else:
        return "REGULAR"

rfm['Segment'] = rfm.apply(
    segment,
    axis=1
)

st.write(rfm.head(7))

segment_count=rfm['Segment'].value_counts().reset_index()
segment_revenue=rfm.groupby('Segment')['Monetary'].sum().reset_index()

col1,col2 = st.columns(2)
with col1:
    figc = px.pie(
        segment_count,
        names="Segment",
        values="count",
        title="Customer Segment Distribution"
    )
    figc.update_traces(
        textinfo='percent+label'
    )

    st.plotly_chart(figc, use_container_width=True)

with col2:
    figd = px.bar(
        segment_revenue,
        x='Segment',
        y='Monetary',
        title='Revenue by Customer Segment',
        text_auto=True
    )

    st.plotly_chart(figd, use_container_width=True)



fig = px.bar(
    top_customers,
    y="Revenue",
    x="Customer Name",

    title="Top 20 Customers by Revenue"
)

fig2 = px.bar(
    profit_cstmr,
    y="Profits",
    x="Customer Name",

    title="Top 20 Customers by Profit"
)

fig3=px.pie(
    pie_df,
    names="Customer Type",
    values="Count",
    title="Repeat vs One-Time Customers"

)
# kpi cards
tab1, tab2, tab3 = st.tabs([
    "most revenue generators",
    "most profit generators",
    "Repeat vs one-time customers "
])
with tab1:
    st.plotly_chart(fig, use_container_width=True)
    customer = top_customers.iloc[0]["Customer Name"]
    revenue = top_customers.iloc[0]["Revenue"]

    st.info(f"{customer} drove the most revenue with ${revenue:,.2f} in sales")
with tab2:
    st.plotly_chart(fig2, use_container_width=True)
    customer = profit_cstmr.iloc[0]["Customer Name"]
    Profit = profit_cstmr.iloc[0]["Profits"]

    st.info(f"{customer} drove the most profit of ${Profit:,.2f} ")
with tab3:
    st.plotly_chart(fig3, use_container_width=True)
