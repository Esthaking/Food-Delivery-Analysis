🍽 Food Delivery Analytics Dashboard
📌 Project Overview

The Food Delivery Analytics Dashboard is a data analytics project designed to analyze food delivery operations and generate meaningful insights from raw order data.

This project involves data cleaning, data transformation, database integration, and visualization to understand customer behavior, revenue patterns, delivery performance, and operational efficiency.

The final output is an interactive dashboard built using Streamlit and connected to a MySQL database, allowing users to explore key business insights dynamically.

🎯 Project Objectives

The main objectives of this project are:

Analyze customer ordering behavior

Track revenue and profit trends

Evaluate delivery performance

Analyze restaurant ratings and cancellations

Provide operational insights for decision making

Build an interactive analytics dashboard for data exploration

🛠 Technologies Used
Technology	Purpose
Python	Data analysis and processing
Pandas	Data cleaning and transformation
MySQL	Database storage
SQLAlchemy	Database connection between Python and MySQL
Streamlit	Interactive dashboard development
Plotly	Data visualization
📊 Dataset Description

The dataset contains information related to food delivery operations including:

Order_ID – Unique identifier for each order

Customer_ID – Unique customer identifier

City – City where the order was placed

Cuisine_Type – Type of cuisine ordered

Order_Value – Total order amount

Delivery_Time_Min – Delivery time in minutes

Delivery_Rating – Customer rating for delivery service

Restaurant_Rating – Restaurant rating

Distance_km – Distance between restaurant and delivery location

Payment_Mode – Payment method used

Order_Status – Order completion or cancellation status

Cancellation_Reason – Reason for cancelled orders

Discount_Applied – Discount applied on the order

Profit_Margin – Profit margin for the order

📓 Notebook Explanation
1️⃣ FOOD_ANALYSIS_PROJECT.ipynb

This notebook performs the first level of data cleaning and preprocessing.

Tasks performed in this notebook:

Data exploration

Identifying missing values

Basic data cleaning

Standardizing column values

Preparing the dataset for further processing

This step ensures that the raw dataset becomes structured and ready for advanced cleaning.

2️⃣ online_F_A.ipynb

This notebook performs the second level of data cleaning and transformation.

Tasks performed:

Filling remaining missing values

Data formatting and transformation

Handling inconsistent data entries

Preparing the final cleaned dataset

After this stage, the dataset is ready to be stored in the MySQL database for further analysis.

🗄 Database Integration

The cleaned dataset is stored in a MySQL database.

Python connects to the database using SQLAlchemy.

Example connection code:

from sqlalchemy import create_engine

engine = create_engine(
"mysql+pymysql://username:password@localhost/database_name"
)

The data is then retrieved using SQL queries and loaded into a Pandas DataFrame.

📊 Streamlit Dashboard (app.py)

The app.py file contains the main application code for the dashboard.

It performs the following tasks:

Connects Python to MySQL Workbench

Retrieves cleaned data from the database

Performs additional preprocessing for analytics

Creates an interactive dashboard using Streamlit

Generates multiple analytical insights

📈 Dashboard Features

The dashboard provides interactive filters and analytical insights including:

City filter

Cuisine filter

Payment mode filter

Dynamic KPI metrics

Interactive charts and graphs

📊 Key Performance Indicators (KPIs)

The dashboard displays important business metrics such as:

Total Orders

Total Revenue

Average Order Value

Average Delivery Time

Cancellation Rate

Average Delivery Rating

These KPIs help quickly understand overall business performance.

🔍 Analytical Insights
Customer & Order Analysis

Top spending customers

Age group vs order value analysis

Weekend vs weekday ordering patterns

Revenue & Profit Analysis

Monthly revenue trends

Impact of discounts on profit margins

Revenue contribution by city

Delivery Performance

Average delivery time by city

Distance vs delivery time relationship

Delivery rating vs delivery time analysis

Restaurant Performance

Top-rated restaurants

Restaurant-wise cancellation analysis

Operational Insights

Payment mode preferences

Cancellation reason analysis
