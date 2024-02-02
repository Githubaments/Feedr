import streamlit as st
import pandas as pd
import re

def parse_orders(text_data):
    # Split the data into individual orders more reliably
    orders_data = text_data.strip().split('\n\n\n')  # Adjust based on your actual data delimiter
    
    # Initialize an empty list to hold order dictionaries
    orders = []
    
    # Loop over each order data block
    for order_text in orders_data:
        # Splitting each order's text by newlines
        lines = order_text.strip().split('\n')
        
        # Parsing each part of the order
        order = {
            'Date': lines[0],
            'Status': lines[1],
            'Meal': lines[2],
            'DeliveryType': lines[3],
            'Vendor': lines[4],
            'Item': lines[5].replace('1x ', ''),  # Remove '1x ' from item name
            'Ingredients': lines[6:-2],  # Assuming ingredients are always before the last two lines
            'Total': float(lines[-2].split()[0]),  # Assuming the second last line is Total
            'Subsidised': float(lines[-1].split()[0])  # Assuming the last line is Subsidised
        }
        order['Payment'] = order['Total'] - order['Subsidised']  # Calculate Payment
        
        # Adding the parsed order to the list
        orders.append(order)
    
    # Convert the list of order dictionaries to a DataFrame
    df = pd.DataFrame(orders)
    
    return df

# Streamlit app interface
st.title("Order Analysis")

data = st.text_area("Paste your order data here:", height=300)

if st.button("Analyze Orders"):
    if data:
        df = parse_orders(data)
        if not df.empty:
            st.write("Parsed Orders:", df)
            # You can further analyze or visualize the DataFrame `df` here as needed
        else:
            st.error("Could not parse any orders from the provided data. Please check the format.")
    else:
        st.error("Please paste order data above.")
