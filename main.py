# This is a sample Python script.
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import time

st.title('E-COMMERCE SALES ANALYSIS')
# dataset=st.file_uploader("UPLOAD DATASET TO WORK ON")
# bar=st.progress(0)
dataset="Sample - Superstore.csv"
data = pd.read_csv(dataset,encoding="latin1")
# if dataset is not None:
    # time.sleep(0.2)
    # time.sleep(0.2)
    # bar.progress(100)
    # df = pd.read_csv(dataset,encoding="latin1")

data['Order Date']=pd.to_datetime(data['Order Date'])
data['Ship Date']=pd.to_datetime(data['Ship Date'])
order_date=pd.DatetimeIndex(data['Order Date'])
ship_date=pd.DatetimeIndex(data['Ship Date'])
data['Order Month']= data['Order Date'].dt.month
data['Order Year']=data['Order Date'].dt.year

st.sidebar.title('DEEP ANALYSIS')

st.header("Dataset Sample:")
st.write(data.sample(5))
year=st.sidebar.selectbox('Yearly_Sales Analysis',['Overall','2014','2015','2016','2017'])

monthly_sales = data.groupby(['Order Year', 'Order Month'])['Sales'].sum()
subcat=data.groupby(['Category','Sub-Category'])['Sales'].sum()


if year=='2014':
    st.title('2014 Sales analysis')
    st.bar_chart(monthly_sales.loc[2014])

elif year=='2015':
    st.title('2015 Sales analysis')
    st.bar_chart(monthly_sales.loc[2015])
elif year=='2016':
    st.title('2016 Sales analysis')
    st.bar_chart(monthly_sales.loc[2016])
elif year=='2017':
    st.title('2017 Sales analysis')
    st.bar_chart(monthly_sales.loc[2017])
elif year=='Overall':
    st.title('Overall Sales analysis')
    monthly_sales = data.groupby(['Order Month', 'Order Year'])['Sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly_sales, x='Order Month', y='Sales', hue='Order Year', palette='Set1', ax=ax)

    ax.set_xticks(monthly_sales['Order Month'].unique())
    ax.set_title("Monthly Sales by Year")
    st.pyplot(fig)


cat=st.sidebar.selectbox('Categorical_Sales Analysis',['Overall','Furniture','Office Supplies','Technology','All Sub-Categories'])
if cat=='Overall':
    st.title('Overall Categorical_Sales analysis')
    st.write('Sales is in dollars')
    categorical_sales = data.groupby('Category')['Sales'].sum().reset_index()
    st.dataframe(categorical_sales)
    fig,ax=plt.subplots(figsize=(8, 3))
    ax.pie(categorical_sales['Sales'], labels=categorical_sales['Category'], autopct='%0.1f%%', shadow=True)
    ax.set_title("Sales by Category")
    st.pyplot(fig)

if cat=='Furniture':
    st.title('Category: Furniture')
    Furniture = subcat.loc['Furniture'].reset_index()
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.pie(Furniture['Sales'], labels=Furniture['Sub-Category'], autopct='%0.1f%%')
    ax.set_title('Furniture Sales')
    st.pyplot(fig)


if cat=='Office Supplies':
    st.title('Category: Office Supplies')
    Office_Supplies = subcat.loc['Office Supplies'].reset_index()
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.pie(Office_Supplies['Sales'], labels=Office_Supplies['Sub-Category'], autopct='%0.1f%%')
    ax.set_title('Office_Supplies Sales')
    st.pyplot(fig)

if cat=='Technology':
    st.title('Category: Technology')
    Technology = subcat.loc['Technology'].reset_index()
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.pie(Technology['Sales'], labels=Technology['Sub-Category'], autopct='%0.1f%%')
    ax.set_title('Technology Sales')
    st.pyplot(fig)

if cat=='All Sub-Categories':
    st.title('All Sub-Categories')
    subcat_sales = data.groupby('Sub-Category')['Sales'].sum()
    st.bar_chart(subcat_sales)

profit=st.sidebar.selectbox('Profit Analysis',['Monthly_Profit','Profit By Category','Profit By Sub-Category'])
if profit=='Monthly_Profit':
    st.title('Monthly Profit')
    monthly = data.groupby([data['Order Year'], data['Order Month']])['Profit'].sum().reset_index()
    fig,ax=plt.subplots()
    sns.lineplot(data=monthly, x='Order Month', y='Profit', hue='Order Year', palette='Dark2',ax=ax)
    ax.set_xticks(monthly['Order Month'])
    st.pyplot(fig)

if profit=='Profit By Category':
    st.title('Profit By Category')
    categorical_profit = data.groupby('Category')['Profit'].sum()
    st.bar_chart(categorical_profit)

if profit=='Profit By Sub-Category':
    st.title('Profit By Sub-Category')
    subcat_profit = data.groupby('Sub-Category')['Profit'].sum()
    st.bar_chart(subcat_profit)


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




