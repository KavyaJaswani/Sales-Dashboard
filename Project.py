# DS PROJECT
# NAME-KAVYA
# ROLLNO.-101917179
# CSE7
# to run the file open command prompt,go to the directory where your project is present, and run the following code:
# streamlit run Project.py
# ******************************************************************************
#  to interact with excel we will use pandas a
import pandas as pd
# to create the web app we use streamlit library
import streamlit as st
# for vizualization, we will use plotly express
import plotly.express as px


# 1)setting up basic page
# ******************************************************************************
# Configures the default settings of the web app
st.set_page_config(
    page_title='Sales Dashboard',
    page_icon=":bar_chart:",
    layout="wide")

# 2) reading excel file
# ******************************************************************************
df=pd.read_excel(
#     io=path
    io='supermarkt_sales.xlsx',
#     when path is not given in io,engine is set ti identify io 
    engine='openpyxl',
#     what sheet out of excel file is to be chosen
    sheet_name='Sales',
#     what rows from the top are to be skipped
    skiprows=3,
#     what columns are to be taken
    usecols='B:R',
#     total number of rows to be read
    nrows=1000
)
# currently the Time columns is a python object,which means we have stored the time in string format,
# to get the time in hour, we first have to convert string to time format and then turn it into hour
df["hour"]=pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour 
# ******************************************************************************
# 3)creating a slidebar

#  we will add widges into the sidebar
st.sidebar.header("Fill Your Options Here :") 

# multiselect is one of the input widges which helps to select more than one option
# by default multiselect will select none of the options.
city =st.sidebar.multiselect(
      "Select the city :",
      options=df["City"].unique(),
 # by default multiselect will select none of the options.
      default=df["City"].unique(),
  )    

customer_type =st.sidebar.multiselect(
      "Select the customer_type :",
      options=df["Customer_type"].unique(),
      default=df["Customer_type"].unique()
  )  

gender =st.sidebar.multiselect(
      "Select the gender :",
      options=df["Gender"].unique(),
      default=df["Gender"].unique()
  )    

#   storing the data selected by users in a variable and filtering the same from the actual dataframe by using query method
df_selection=df.query(
    "City== @city & Customer_type==@customer_type & Gender==@gender"
)
# streamlit to implement: select and display only the options selected by users
st.dataframe(df_selection)

# ********************************************************************************
# ---MAINPAGE----

# DISPLAYINNG KPI(key performance indicator)S INSTEAD OF OUR DATAFRAME 
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI'S
# summing the Total column
total_sales=int(df_selection["Total"].sum())
# finding the mean of rating column
average_rating=round(df_selection["Rating"].mean(),1)
# multiplying star favicon with the average rating
star_rating = ":star:" * int(round(average_rating, 0))
# mean of total column and rounding off by 2
average_sale_by_transaction=round(df_selection["Total"].mean(),2)

col1,col2,col3=st.columns(3)

with col1:
    st.subheader("Total Sales:")
    st.subheader(f"INR ₹ {total_sales:,}")

with col2:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

with col3:
    st.subheader("Average Sales per Transaction")
    st.subheader(f"INR ₹ {average_sale_by_transaction}")
st.markdown("---")    

# **************************************************************************
# SALES BY PRODUCT LINE [BAR CHART]
# we summed the columns on the basis of "Product Line" and sorted the values in increasing values "Total" and then we only need "Total "column so we only showed it
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

# now using plotly express library to plot the data
fig_product_sales=px.bar(
    sales_by_product_line,
    x=sales_by_product_line.index,
    y='Total',
    title= "<b>Sales By Product Line</b>",
    color_discrete_sequence=["#AC3E31"]*len(sales_by_product_line),
    template="ggplot2",
)
st.plotly_chart(fig_product_sales)
# fig_product_sales.show()

# **********************************************************************************************
# SALES BY HOUR CHART
sales_by_hour=(
    df_selection.groupby(by=["hour"]).sum()[["Total"]].sort_values(by="Total")
)
fig_sales=px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales By Hour</b>",
    color_discrete_sequence=["#AC3E31"]*len(sales_by_product_line),
    template="ggplot2",
)
st.plotly_chart(fig_sales)