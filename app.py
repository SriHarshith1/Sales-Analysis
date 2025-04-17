import pandas as pd
import plotly.express as px
import streamlit as st 


# Setting page configs
st.set_page_config(page_title = 'Sales Dashboard',
                   page_icon = ':bar_chart:',
                   layout = 'wide')

@st.cache_data

def get_data_from_excel():
    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
    )

    # Convert 'Time' column (datetime.time) to hour integer
    df['hour'] = df['Time'].apply(lambda t: t.hour if pd.notnull(t) else None)

    return df

df = get_data_from_excel()


# --- SIDERBAR---


st.sidebar.header("Customize Your View")

# City Selection

city = st.sidebar.multiselect(
    "Select the city :",
    options = df['City'].unique(),
    default = df['City'].unique()
)

# Customer Types

customer = st.sidebar.multiselect(
    "Select the type of customer :",
    options = df['Customer_type'].unique(),
    default = df['Customer_type'].unique()
)

#Gender Selection

Gender = st.sidebar.multiselect(
    "Select the type of customer :",
    options = df['Gender'].unique(),
    default = df['Gender'].unique()
)


df_selection = df.query(
    "City == @city & Customer_type == @customer & Gender == @Gender"
)

# ---Main Page---
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


# Top KPI's

total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(),1)
star_rating = ":star:"* int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection['Total'].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales :")
    st.subheader(f"US $ {total_sales:} ")
    
with middle_column:
    st.subheader("Average Rating :")
    st.subheader(f"{average_rating} {star_rating}")
    
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f" $ {average_sale_by_transaction}")

st.markdown('----')

# SALES BY PRODUCT LINE [BAR CHART]

sales_by_product_line = (
    df_selection.groupby(by = ['Product line']).sum([['Total']]).sort_values(by = "Total")
)

fig_product_sales =  px.bar(
    sales_by_product_line,
    x= 'Total',
    y = sales_by_product_line.index,
    orientation= 'h',
    title = "<b> Sales by Product Line </b>",
    color_discrete_sequence= ['#008388']* len(sales_by_product_line),
    template="plotly_white" 
    
)
# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
