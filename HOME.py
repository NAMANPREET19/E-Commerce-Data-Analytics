# This is a sample Python script.
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import sqlite3
st.set_page_config(
    page_title='E-Commerce Dashboard',
    page_icon="📊",
    layout="wide"
)

# TITLE
st.markdown("""
<h1 style="margin-bottom:0; color:#8FD6E1; text-align:center;
font-size:50px;
font-weight:bold;
text-shadow:
    0px 2px 4px rgba(0,0,0,0.2),
    0px 4px 8px rgba(0,0,0,0.1);">
📊 E-Commerce Analytics Dashboard
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
# dataset=st.file_uploader("UPLOAD DATASET TO WORK ON")
# bar=st.progress(0)
dataset="Sample - Superstore.csv"
data = pd.read_csv(dataset,encoding="latin1")
# if dataset is not None:
    # time.sleep(0.2)
    # time.sleep(0.2)
    # bar.progress(100)
    # df = pd.read_csv(dataset,encoding="latin1")
# Load CSV

# Create database
conn = sqlite3.connect("superstore.db")



data['Order Date']=pd.to_datetime(data['Order Date'])
data['Ship Date']=pd.to_datetime(data['Ship Date'])
order_date=pd.DatetimeIndex(data['Order Date'])
ship_date=pd.DatetimeIndex(data['Ship Date'])
data['Order Month']= data['Order Date'].dt.month
data['Order Year']=data['Order Date'].dt.year

st.sidebar.title('DEEP ANALYSIS')

st.header("Dataset Sample:")
st.write(data.sample(5))

# ADDING K P I
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("Total Sales",
              f"${data['Sales'].sum():,.0f}")

with col2:
    st.metric("Total Profit",
              f"${data['Profit'].sum():,.0f}")

with col3:
    st.metric("Orders",
              data['Order ID'].nunique())

with col4:
    margin=(data['Profit'].sum()/
            data['Sales'].sum())*100

    st.metric("Margin",
              f"{margin:.2f}%")


st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

[data-testid="metric-container"]{
    border:1px solid #262730;
    padding:20px;
    border-radius:10px;
    background:#111827;
}

</style>
""",unsafe_allow_html=True)


year=st.sidebar.selectbox('Yearly_Sales Analysis',['Overall','2014','2015','2016','2017'])

monthly_sales = data.groupby(['Order Year', 'Order Month'])['Sales'].sum()
subcat=data.groupby(['Category','Sub-Category'])['Sales'].sum()


st.markdown("""
<div style="margin:25px 0;">

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

<div style="
background:linear-gradient(135deg,#111827,#1f2937);
padding:18px;
border-radius:15px;
border:1px solid rgba(0,255,255,0.4);
box-shadow:
    0 0 15px rgba(0,255,255,0.2);
margin:10px 0;
">

<h2 style="
text-align:center;
margin:0;
color:white;">
📊 YEARLY_SALES ANALYSIS
</h2>

</div>

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

</div>
""", unsafe_allow_html=True)

if year=='2014':
    st.title('2014 Sales analysis')
    sale2014=monthly_sales.loc[2014]

    fig1=px.bar(
        x=sale2014.index,
        y=sale2014.values,
        title='2014 Sales by Month',
        labels={'x':'Month', 'y':'Sales'},
    )
    st.plotly_chart(fig1)

elif year=='2015':
    st.title('2015 Sales analysis')
    sale2015=monthly_sales.loc[2015]

    fig1=px.bar(
        x=sale2015.index,
        y=sale2015.values,
        title='2015 Sales by Month',
        labels={'x':'Month', 'y':'Sales'},
    )
    st.plotly_chart(fig1)
elif year=='2016':
    st.title('2016 Sales analysis')
    sale2016=monthly_sales.loc[2016]

    fig1=px.bar(
        x=sale2016.index,
        y=sale2016.values,
        title='2016 Sales by Month',
        labels={'x':'Month', 'y':'Sales'},
    )
    st.plotly_chart(fig1)
elif year=='2017':
    st.title('2017 Sales analysis')
    sale2017=monthly_sales.loc[2017]

    fig1=px.bar(
        x=sale2017.index,
        y=sale2017.values,
        title='2017 Sales by Month',
        labels={'x':'Month', 'y':'Sales'},
    )
    st.plotly_chart(fig1)

elif year=='Overall':
    st.title('Overall Sales analysis')
    monthly_sales = data.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()

    fig=px.line(
        monthly_sales,
        x='Order Month',
        y='Sales',
        color='Order Year',
        )

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Sales',
        hovermode='x unified'
    )
    st.plotly_chart(fig)


cat=st.sidebar.selectbox('Categorical_Sales Analysis',['Overall','Furniture','Office Supplies','Technology','All Sub-Categories'])
st.markdown("""
<div style="margin:25px 0;">

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

<div style="
background:linear-gradient(135deg,#111827,#1f2937);
padding:18px;
border-radius:15px;
border:1px solid rgba(0,255,255,0.4);
box-shadow:
    0 0 15px rgba(0,255,255,0.2);
margin:10px 0;
">

<h2 style="
text-align:center;
margin:0;
color:white;">
📊 CATEGORICAL_SALES ANALYSIS
</h2>

</div>

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

</div>
""", unsafe_allow_html=True)
if cat=='Overall':
    st.title('Overall Categorical_Sales analysis')
    st.write('Sales is in dollars')
    categorical_sales = data.groupby('Category')['Sales'].sum().reset_index()
    st.write(categorical_sales)
    fig = px.pie(
        categorical_sales,
        values='Sales',
        names='Category',
        title='Sales by Category'
    )

    fig.update_traces(
        textinfo='percent+label',
        pull=[0.03]*len(categorical_sales)  # slight separation effect
    )

    st.plotly_chart(fig, use_container_width=True)

if cat=='Furniture':
    st.title('Category: Furniture')
    Furniture = subcat.loc['Furniture'].reset_index()
    fig=px.pie(
        Furniture,
        values='Sales',
        names='Sub-Category',
        title='Sales by Furniture'
    )
    fig.update_traces(
        textinfo='percent+label',
        pull=[0.03]*len(Furniture)  # slight separation effect
    )
    st.plotly_chart(fig, use_container_width=True)


if cat=='Office Supplies':
    st.title('Category: Office Supplies')
    Office_Supplies = subcat.loc['Office Supplies'].reset_index()
    fig=px.pie(
        Office_Supplies,
        values='Sales',
        names='Sub-Category',
        title='Sales by Office_Supplies'
    )
    fig.update_traces(
        textinfo='percent+label',
        pull=[0.03]*len(Office_Supplies)  # slight separation effect
    )
    st.plotly_chart(fig, use_container_width=True)

if cat=='Technology':
    st.title('Category: Technology')
    Technology = subcat.loc['Technology'].reset_index()
    fig=px.pie(
        Technology,
        values='Sales',
        names='Sub-Category',
        title='Sales by Technology'
    )
    fig.update_traces(
        textinfo='percent+label',
        pull=[0.03]*len(Technology)  # slight separation effect
    )
    st.plotly_chart(fig, use_container_width=True)
if cat=='All Sub-Categories':
    st.title('All Sub-Categories')
    subcat_sales = data.groupby('Sub-Category')['Sales'].sum()
    fig = px.bar(
        subcat_sales,
        x=subcat_sales.index,
        y=subcat_sales.values,
        title='Sales by All Sub-Categories',
        labels={'x':'SUB-CATEGORIES','y':'SALES'},
    )

    st.plotly_chart(fig, use_container_width=True)


# BETTER UI BETWEEN LINES

st.markdown("""
<div style="margin:25px 0;">

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

<div style="
background:linear-gradient(135deg,#111827,#1f2937);
padding:18px;
border-radius:15px;
border:1px solid rgba(0,255,255,0.4);
box-shadow:
    0 0 15px rgba(0,255,255,0.2);
margin:10px 0;
">

<h2 style="
text-align:center;
margin:0;
color:white;">
📊 PROFIT ANALYSIS
</h2>

</div>

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

</div>
""", unsafe_allow_html=True)



profit=st.sidebar.selectbox('Profit Analysis',['Monthly_Profit','Profit By Category','Profit By Sub-Category'])
if profit=='Monthly_Profit':
    st.title('Monthly Profit')
    monthly = data.groupby([data['Order Year'], data['Order Month']])['Profit'].sum().reset_index()
    fig=px.line(
        monthly,
        x='Order Month',
        y='Profit',
        color='Order Year',
    )
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='profit',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

if profit=='Profit By Category':
    st.title('Profit By Category')
    categorical_profit = data.groupby('Category')['Profit'].sum()
    fig=px.bar(
        x=categorical_profit.index,
        y=categorical_profit.values,
        title='Profit by Category',
        labels={'x':'Category','y':'Profit'},
    )
    st.plotly_chart(fig, use_container_width=True)

if profit=='Profit By Sub-Category':
    st.title('Profit By Sub-Category')
    subcat_profit = data.groupby('Sub-Category')['Profit'].sum()
    fig = px.bar(
        x=subcat_profit.index,
        y=subcat_profit.values,
        title='Profit by Category',
        labels={'x': 'Category', 'y': 'Profit'},
    )
    st.plotly_chart(fig, use_container_width=True)



# Sales_vs_Profit=st.sidebar.selectbox('Sales_vs_Profit Analysis',['Categorical','Subcategorical','Consumer Segment'])
# if Sales_vs_Profit=='Categorical':
#     st.title('Categorical SalesVProfit Analysis')
#     categorical_profit = data.groupby('Category')['Profit'].sum().reset_index()
#     categorical_sales = data.groupby('Category')['Sales'].sum().reset_index()
#     cat = categorical_sales.merge(categorical_profit, how='inner', on='Category')
#     st.bar_chart(cat)
#
# if Sales_vs_Profit=='Subcategorical':
#     st.title('Subcategorical SalesVProfit Analysis')
#     subcat_profit = data.groupby('Sub-Category')['Profit'].sum().reset_index()
#     subcat_sales = data.groupby('Sub-Category')['Sales'].sum().reset_index()
#     subcat = subcat_sales.merge(subcat_profit, how='inner', on='Sub-Category')
#     st.line_chart(subcat)
#
# if Sales_vs_Profit=='Consumer Segment':
#     st.title('SalesVProfit Analysis By Consumer Segment')
#     seg = data.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
#     fig,ax=plt.subplots()
#     sns.lineplot(data=seg, x='Segment', y='Sales', hue=['Profit','Sales'], palette='Set1', ax=ax)
#     st.pyplot(fig)

btn=st.button('Sales to profit ratio')
if btn:
    seg = data.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    seg['sale to profit ratio'] = (seg['Sales'] / seg['Profit'])
    st.write(seg)




st.markdown("""
<div style="margin:25px 0;">

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

<div style="
background:linear-gradient(135deg,#111827,#1f2937);
padding:18px;
border-radius:15px;
border:1px solid rgba(0,255,255,0.4);
box-shadow:
    0 0 15px rgba(0,255,255,0.2);
margin:10px 0;
">

<h2 style="
text-align:center;
margin:0;
color:white;">
📊 PRODUCT ANALYSIS
</h2>

</div>

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

</div>
""", unsafe_allow_html=True)

query= """
SELECT "Product Name",SUM(Sales) AS TotalP
FROM Orders 
GROUP BY "Product Name"
ORDER BY TotalP DESC
LIMIT 10
"""

query2="""
SELECT "Product Name",SUM(Profit) AS TotalP
FROM Orders 
GROUP BY "Product Name"
ORDER BY TotalP DESC
LIMIT 10
"""
query3="""
SELECT
    "Product Name",
    SUM(Sales) AS Revenue,
    SUM(Profit) AS Profit
FROM Orders
GROUP BY "Product Name"
ORDER BY Revenue DESC
LIMIT 20;
"""

top_products=pd.read_sql(query, conn)
profit_products=pd.read_sql(query2, conn)
top_sales = pd.read_sql(query3, conn)

low_profit_products = top_sales.sort_values(
    by="Profit",
    ascending=True
)

fig=px.bar(
    top_products,
    x="Product Name",
    y="TotalP",
    title="Top 10 Products by REVENUE"
)

fig2=px.bar(
    profit_products,
    x="Product Name",
    y="TotalP",
    title="Top 10 Products by PROFIT"
)

fig3=px.bar(
    low_profit_products.head(10),
    x="Profit",
    y="Product Name",
    orientation="h",
    title="High Revenue Products with Low Profit",
    hover_data=["Revenue"]

)


tab1, tab2, tab3=st.tabs([
    "best selling products",
    "most profitable products",
    "high selling but low profit"
])

with tab1:
    st.plotly_chart(fig, use_container_width=True)
    product=top_products.iloc[0]["Product Name"]
    sale=top_products.iloc[0]["TotalP"]
    st.info(f"{product} is the best selling product generating a revenue of ${sale:,.2f} ")

with tab2:
    st.plotly_chart(fig2, use_container_width=True)
    product=profit_products.iloc[0]["Product Name"]
    sale=profit_products.iloc[0]["TotalP"]
    st.success(f"{product} is the most profitable product generating a profit of ${sale:,.2f} ")

with tab3:
    st.plotly_chart(fig3, use_container_width=True)
    product_name=low_profit_products.iloc[0]["Product Name"]
    st.warning(
        f"{product_name} generated high sales but resulted in a net loss."
    )

st.markdown("""
<div style="margin:25px 0;">

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

<div style="
background:linear-gradient(135deg,#111827,#1f2937);
padding:18px;
border-radius:15px;
border:1px solid rgba(0,255,255,0.4);
box-shadow:
    0 0 15px rgba(0,255,255,0.2);
margin:10px 0;
">

<h2 style="
text-align:center;
margin:0;
color:white;">
📊 REGIONAL ANALYSIS
</h2>

</div>

<hr style="
border:none;
height:3px;
background:linear-gradient(to right,
transparent,
#00ffff,
#00ffff,
transparent);
box-shadow:
    0 0 10px #00ffff,
    0 0 20px #00ffff;
">

</div>
""", unsafe_allow_html=True)


query="""
SELECT Region, SUM(Profit) AS Profit
FROM Orders 
GROUP BY Region
ORDER BY Profit DESC   
"""

query2="""
SELECT State, SUM(Profit) AS Profit
FROM Orders 
GROUP BY State
ORDER BY Profit DESC   
"""

query3="""
SELECT
    State,
    SUM(Profit) AS Profit
FROM Orders
GROUP BY State
HAVING SUM(Profit) < 0
ORDER BY Profit
"""
Region_profit=pd.read_sql(query, conn)
State_profit=pd.read_sql(query2, conn)
Loss_region=pd.read_sql(query3, conn)

fig = px.bar(
    Region_profit,
    x="Region",
    y="Profit",
    title="Profit by Region"
)
fig2=px.bar(
    State_profit.head(10),
    x="State",
    y="Profit",
    title="TOP 10 PROFIT MAKING STATES"
)
fig3=px.bar(
    Loss_region,
    x="State",
    y="Profit",
    title="LOSS MAKING STATES"
)
tab1, tab2, tab3=st.tabs([
    "Region-wise performance",
    "Profit Making States",
    "Loss-making states"
])

with tab1:
    st.subheader("These are the regions of united states")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.plotly_chart(fig3, use_container_width=True)




