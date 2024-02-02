import streamlit as st
import pandas as pd
import re

def parse_orders(text_data):
    # Initialize an empty list to hold order dictionaries
    orders = []
    
    # Split the data into individual orders, assuming at least two newlines between orders
    orders_data = re.split(r'\n\n+', text_data.strip())
    
    for order_text in orders_data:
        lines = order_text.strip().split('\n')
        
        # Basic check to ensure there are enough lines for an order
        if len(lines) < 9:  # Minimum expected lines based on provided format
            continue  # Skip this order if it doesn't meet the expected structure
        
        # Extracting data with checks
        date = lines[0]
        vendor = lines[4]
        item = lines[5].replace('1x ', '') if lines[5].startswith('1x ') else lines[5]
        ingredients = lines[6:-2]  # Might be empty, which is fine
        
        # Safely extracting Total and Subsidised values
        try:
            total = float(lines[-2].split()[0])
            subsidised = float(lines[-1].split()[0])
        except (ValueError, IndexError):
            # If conversion fails or lines are missing, skip this order
            continue
        
        payment = total - subsidised
        
        orders.append({
            'Date': date,
            'Vendor': vendor,
            'Item': item,
            'Ingredients': ingredients,
            'Total': total,
            'Subsidised': subsidised,
            'Payment': payment
        })
    
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
