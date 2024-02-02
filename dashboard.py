import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Function to parse text data
def parse_data(data):
    orders = data.strip().split('\n\n\n')  # Adjust the split based on the actual data
    pattern = re.compile(r'Your Regex Here')

    # List to hold all orders
    all_orders = []

    # Process each order
    for order in orders:
        match = pattern.match(order)
        if match:
            all_orders.append(match.groups())

    # Convert to a DataFrame if all_orders is not empty
    if all_orders:
        df = pd.DataFrame(all_orders, columns=['Date', 'Time', 'Status', 'Meal', 'DeliveryType', 'Vendor', 'Item', 'Ingredients', 'Total', 'Subsidised'])
        # Convert 'Total' and 'Subsidised' to numeric types
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
        df['Subsidised'] = pd.to_numeric(df['Subsidised'], errors='coerce')
        return df
    else:
        # Return an empty DataFrame if no orders were parsed
        return pd.DataFrame()

# Then, in your Streamlit app, you would use it like this:
if st.button("Analyze Orders"):
    if data:
        df = parse_data(data)
        if not df.empty:
            st.write(df)
            total_spend = df['Total'].sum()
            st.write("Total Spend: ", total_spend)
            # Other analysis and plotting code...
        else:
            st.error("No orders were parsed. Please check the data format.")



# Streamlit interface
st.title("Order Analysis App")

# Text area for user to paste data
data = st.text_area("Paste your order data here:", height=300)

# Button to parse data
if st.button("Analyze Orders"):
    if data:
        df = parse_order(data)
        st.write(df)

        # Show stats using pandas
        total_spend = df['Total'].sum()
        st.write("Total Spend: ", total_spend)

        # Show a plot using plotly
        fig = px.bar(df, x='Vendor', y='Total', title="Total Spend by Vendor")
        st.plotly_chart(fig)

    else:
        st.error("Please paste order data above.")
