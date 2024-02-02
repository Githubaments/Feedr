import streamlit as st
import pandas as pd
import plotly.express as px
import re
import json

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

# Streamlit interface
st.title("Order Analysis App")

# Text area for user to paste data
data = st.text_area("Paste your order data here:", height=300)

# Button to parse and analyze data
if st.button("Analyze Orders"):
    if data:
        try:
            # Parse the string of data into a list of dictionaries
            data = json.loads(data)

            # Convert the list of dictionaries into a DataFrame
            df = pd.DataFrame(data)

            # Perform DataFrame operations
            total_spend = df['total'].sum()
            st.write(f"Total Spend: {total_spend}")

            # Add more analysis and visualization as needed

        except json.JSONDecodeError as e:
            st.error(f"JSON parsing error: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please paste order data above.")
