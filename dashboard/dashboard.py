import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load cleaned data
df = pd.read_csv('https://raw.githubusercontent.com/rismaamaliyah/EDA-Bike-Sharing/main/dashboard/all_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Title
st.title("Bike Sharing Dashboard")

# Sidebar
with st.sidebar:
    st.image("https://plus.unsplash.com/premium_photo-1678718713393-2b88cde9605b?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YmlrZXxlbnwwfHwwfHx8MA%3D%3D")

    # Data range slider
    start_date = st.date_input("Start Date", df['Date'].min())
    end_date = st.date_input("End Date", df['Date'].max())

# Filter data
filtered_df = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))]

# Display daily rentals
total_rentals = filtered_df['Total Count'].sum()
total_registered = filtered_df['Registered Count'].sum()
total_casual = filtered_df['Casual Count'].sum()

lowest_rental_day = filtered_df['Total Count'].idxmin()
highest_rentals_day = filtered_df['Total Count'].idxmax()
avg_rentals_per_day = filtered_df['Total Count'].mean()

st.header("Daily Rentals")

col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", total_rentals)
col2.metric("Registered", total_registered)
col3.metric("Casual", total_casual)

col4, col5, col6 = st.columns(3)
col4.metric(label="Lowest Rentals Day", value=f"{lowest_rental_day}")
col5.metric(label="Highest Rentals Day", value=f"{highest_rentals_day}")
col6.metric(label="Average Rentals per Day", value=f"{avg_rentals_per_day:.2f}")

# Display bike usage pattern per hour & per day
st.header('Bike Usage Pattern')

col7, col8 = st.columns(2)

with col7: 
    st.subheader("per Hour")
    hourly_data = filtered_df.groupby('Hour')[['Casual Count', 'Registered Count', 'Total Count']].mean().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(x='Hour', y='Total Count', data=hourly_data, label='Total Count', color='b', ax=ax)
    sns.lineplot(x='Hour', y='Casual Count', data=hourly_data, label='Casual Count', color='g', ax=ax)
    sns.lineplot(x='Hour', y='Registered Count', data=hourly_data, label='Registered Count', color='r', ax=ax)
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Total Bike Rentals')
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

with col8: 
    st.subheader("per Day")
    daily_data = filtered_df.groupby('Weekday')[['Casual Count', 'Registered Count', 'Total Count']].mean().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(x='Weekday', y='Total Count', data=daily_data, label='Total Count', color='b', ax=ax)
    sns.lineplot(x='Weekday', y='Casual Count', data=daily_data, label='Casual Count', color='g', ax=ax)
    sns.lineplot(x='Weekday', y='Registered Count', data=daily_data, label='Registered Count', color='r', ax=ax)
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Total Bike Rentals')
    ax.set_xticklabels(daily_data['Weekday'])
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Display relationship between temperature, humidity, wind speed, and bike rentals
st.header('Relationship Between Temperature, Humidity, Wind Speed, and Bike Rentals')
col9, col10, col11 = st.columns(3)

with col9:
    st.subheader("Temperature and Bike Rentals")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Temperature', y='Total Count', data=filtered_df, ax=ax)
    ax.set_xlabel('Temperature (%)')
    ax.set_ylabel('Total Bike Rentals')
    plt.tight_layout()
    st.pyplot(fig)
    
with col10:
    st.subheader("Humidity and Bike Rentals")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Humidity', y='Total Count', data=filtered_df, ax=ax)
    ax.set_xlabel('Humidity (%)')
    ax.set_ylabel('Total Bike Rentals')
    plt.tight_layout()
    st.pyplot(fig)

with col11:
    st.subheader("Wind Speed and Bike Rentals")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Wind Speed', y='Total Count', data=filtered_df, ax=ax)
    ax.set_title('Relationship Between Wind Speed and Total Bike Rentals')
    ax.set_xlabel('Wind Speed (%)')
    ax.set_ylabel('Total Bike Rentals')
    plt.tight_layout()
    st.pyplot(fig)

# Calculate average users per cluster
cluster_analysis = filtered_df.groupby('Cluster')['Total Count'].mean()

# Determine the cluster with the highest average
highest_mean_cluster = cluster_analysis.idxmax()
highest_mean_value = cluster_analysis.max()

# Metric Display for clusters with the most users
st.header('Binning Analysis')
st.metric(label="Cluster with Highest Avg Users:", value=f"Cluster {highest_mean_cluster}", delta=f"{highest_mean_value:.2f}")

st.caption(f"Copyright © 2024 [Risma Amaliyah Mahmudah](https://www.linkedin.com/in/rismaamaliyah/)")
