import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Function to parse text data
def parse_data(data):
    # Split the data by double newlines
    orders = data.strip().split('\n\n')
    
    # Define the pattern to extract information
    pattern = re.compile(r'Your Regular Expression Here')

    # List to hold all orders
    all_orders = []

    # Process each order
    for order in orders:
        match = pattern.search(order)
        if match:
            all_orders.append(match.groups())
    
    # Convert to a DataFrame
    columns = ['Date', 'Time', 'Status', 'Meal', 'DeliveryType', 'Vendor', 'Items', 'Ingredients', 'Total', 'Subsidised']
    df = pd.DataFrame(all_orders, columns=columns)
    
    # Convert Total and Subsidised to numeric
    df['Total'] = pd.to_numeric(df['Total'])
    df['Subsidised'] = pd.to_numeric(df['Subsidised'])
    
    return df

# Streamlit interface
st.title("Order Analysis App")

# Text area for user to paste data
data = st.text_area("Paste your order data here:", height=300)

# Button to parse data
if st.button("Analyze Orders"):
    if data:
        df = parse_data(data)
        st.write(df)

        # Show stats using pandas
        total_spend = df['Total'].sum()
        st.write("Total Spend: ", total_spend)

        # Show a plot using plotly
        fig = px.bar(df, x='Vendor', y='Total', title="Total Spend by Vendor")
        st.plotly_chart(fig)

    else:
        st.error("Please paste order data above.")
