import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Food Delivery Analytics Dashboard",
    layout="wide"
)

st.title("🍽 Food Delivery Analytics Dashboard")

# -----------------------------
# DATABASE CONNECTION
# -----------------------------

engine = create_engine(
    "mysql+pymysql://root:201721@127.0.0.1/food_analysis"
)

query = "SELECT * FROM online_food_finaldata"

df = pd.read_sql(query, engine)

# -----------------------------
# DATA PREPROCESSING
# -----------------------------

df["Order_Date"] = pd.to_datetime(df["Order_Date"])


# Convert 0 values → NaN so mean/median ignores them
zero_columns = [
    "Delivery_Time_Min",
    "Delivery_Rating",
    "Restaurant_Rating",
    "Distance_km"
]

df[zero_columns] = df[zero_columns].replace(0, pd.NA)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.header("Dashboard Filters")

city = st.sidebar.multiselect(
    "Select City",
    df["City"].dropna().unique(),
    default=df["City"].dropna().unique()
)

cuisine = st.sidebar.multiselect(
    "Select Cuisine",
    df["Cuisine_Type"].dropna().unique(),
    default=df["Cuisine_Type"].dropna().unique()
)

payment = st.sidebar.multiselect(
    "Select Payment Mode",
    df["Payment_Mode"].dropna().unique(),
    default=df["Payment_Mode"].dropna().unique()
)

df = df[
    (df["City"].isin(city)) &
    (df["Cuisine_Type"].isin(cuisine)) &
    (df["Payment_Mode"].isin(payment))
]

# -----------------------------
# KPI METRICS
# -----------------------------

st.subheader("📊 Key Business Metrics")

col1,col2,col3,col4,col5,col6 = st.columns(6)

total_orders = df.shape[0]
total_revenue = df["Order_Value"].sum()
avg_order_value = df["Order_Value"].mean()
avg_delivery_time = df["Delivery_Time_Min"].mean()
cancel_rate = (df["Order_Status"]=="Cancelled").mean()*100
avg_delivery_rating = df["Delivery_Rating"].mean()

col1.metric("Total Orders", total_orders)
col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col3.metric("Avg Order Value", f"₹{avg_order_value:.2f}")
col4.metric("Avg Delivery Time", f"{avg_delivery_time:.2f} min")
col5.metric("Cancellation Rate", f"{cancel_rate:.2f}%")
col6.metric("Avg Delivery Rating", f"{avg_delivery_rating:.2f}")

st.divider()

# -----------------------------
# SIDEBAR INSIGHT SELECTION
# -----------------------------

insight = st.sidebar.selectbox(
    "Select Insight",
    [
        "Customer & Order Analysis",
        "Revenue & Profit Analysis",
        "Delivery Performance",
        "Restaurant Performance",
        "Operational Insights"
    ]
)

# -----------------------------
# CUSTOMER ANALYSIS
# -----------------------------

if insight == "Customer & Order Analysis":

    st.header("Customer & Order Analysis")

    # Top spending customers
    top_customers = (
        df.groupby("Customer_ID")["Order_Value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_customers,
        x="Customer_ID",
        y="Order_Value",
        title="Top Spending Customers"
    )

    st.plotly_chart(fig,use_container_width=True)

    # Age group vs order value
    age_analysis = df.groupby("Age_Group")["Order_Value"].mean().reset_index()

    fig = px.bar(
        age_analysis,
        x="Age_Group",
        y="Order_Value",
        color="Age_Group",
        title="Age Group vs Average Order Value"
    )

    st.plotly_chart(fig,use_container_width=True)

    # Weekend vs weekday
    df["Order_Day_Type"] = df["Order_Date"].dt.dayofweek.apply(
        lambda x: "Weekend" if x>=5 else "Weekday"
    )

    pattern = df.groupby("Order_Day_Type")["Order_ID"].count().reset_index()

    fig = px.pie(
        pattern,
        names="Order_Day_Type",
        values="Order_ID",
        title="Weekend vs Weekday Orders"
    )

    st.plotly_chart(fig)

# -----------------------------
# REVENUE ANALYSIS
# -----------------------------

elif insight == "Revenue & Profit Analysis":

    st.header("Revenue & Profit Analysis")

    # Monthly revenue
    df["Month_Name"] = df["Order_Date"].dt.to_period("M").astype(str)

    monthly = df.groupby("Month_Name")["Order_Value"].sum().reset_index()

    fig = px.line(
        monthly,
        x="Month_Name",
        y="Order_Value",
        markers=True,
        title="Monthly Revenue Trend"
    )

    st.plotly_chart(fig,use_container_width=True)

    # Discount impact
    fig = px.scatter(
        df,
        x="Discount_Applied",
        y="Profit_Margin",
        color="City",
        title="Impact of Discount on Profit"
    )

    st.plotly_chart(fig,use_container_width=True)

    # Revenue by city
    city_rev = df.groupby("City")["Order_Value"].sum().reset_index()

    fig = px.bar(
        city_rev,
        x="City",
        y="Order_Value",
        title="Revenue by City"
    )

    st.plotly_chart(fig,use_container_width=True)

# -----------------------------
# DELIVERY PERFORMANCE
# -----------------------------

elif insight == "Delivery Performance":

    st.header("Delivery Performance")

    city_delivery = df.groupby("City")["Delivery_Time_Min"].mean().reset_index()

    fig = px.bar(
        city_delivery,
        x="City",
        y="Delivery_Time_Min",
        title="Average Delivery Time by City"
    )

    st.plotly_chart(fig,use_container_width=True)

    fig = px.scatter(
        df,
        x="Distance_km",
        y="Delivery_Time_Min",
        title="Distance vs Delivery Time"
    )

    st.plotly_chart(fig)

    fig = px.scatter(
        df,
        x="Delivery_Time_Min",
        y="Delivery_Rating",
        title="Delivery Rating vs Delivery Time"
    )

    st.plotly_chart(fig)

# -----------------------------
# RESTAURANT PERFORMANCE
# -----------------------------

elif insight == "Restaurant Performance":

    st.header("Restaurant Performance")

    top_rest = (
        df.groupby("Restaurant_Name")["Restaurant_Rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_rest,
        x="Restaurant_Name",
        y="Restaurant_Rating",
        title="Top Rated Restaurants"
    )

    st.plotly_chart(fig,use_container_width=True)

    cancel = (
        df[df["Order_Status"]=="Cancelled"]
        .groupby("Restaurant_Name")
        .size()
        .reset_index(name="Cancel_Count")
    )

    fig = px.bar(
        cancel,
        x="Restaurant_Name",
        y="Cancel_Count",
        title="Cancellation Rate by Restaurant"
    )

    st.plotly_chart(fig)

# -----------------------------
# -----------------------------
# OPERATIONAL INSIGHTS
# -----------------------------

elif insight == "Operational Insights":

    st.header("Operational Insights")

    # Payment Mode Preference
    payment_mode = df["Payment_Mode"].value_counts().reset_index()
    payment_mode.columns = ["Payment_Mode", "Count"]

    fig = px.pie(
        payment_mode,
        names="Payment_Mode",
        values="Count",
        title="Payment Mode Preference"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Cancellation Reason Analysis
    cancel_reason = df["Cancellation_Reason"].value_counts().reset_index()
    cancel_reason.columns = ["Cancellation_Reason", "Count"]

    fig = px.bar(
        cancel_reason,
        x="Cancellation_Reason",
        y="Count",
        title="Cancellation Reason Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)