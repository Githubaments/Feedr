import streamlit as st
import pandas as pd
import re

def split_into_orders(text_data):
    # Split on two newline characters, which seems to be the consistent separator between orders
    return re.split(r'\n\n+', text_data.strip())

def parse_orders(text_data):
    # Split the entire input into lines
    lines = text_data.strip().split('\n')
    
    # Initialize variables for processing
    orders = []
    current_order = {}
    reading_ingredients = False
    
    for line in lines:
        if line.strip() == '' and current_order:  # End of an order
            # Finalize the current order
            orders.append(current_order)
            current_order = {}  # Reset for the next order
            reading_ingredients = False
        elif 'DATE' in line:  # Indicates the start of an order
            reading_ingredients = False  # Reset flag
        elif ' at ' in line and 'GMT' in line:  # Date line
            current_order['Date'] = line.split(' at ')[0]
        elif 'credits' in line:
            if 'Total' not in current_order:
                current_order['Total'] = float(line.split()[0])
            else:
                current_order['Subsidised'] = float(line.split()[0])
                current_order['Payment'] = current_order['Total'] - current_order['Subsidised']
        elif line.startswith('1x '):
            current_order['Item'] = line[3:]  # Remove '1x ' prefix
            reading_ingredients = True
            current_order['Ingredients'] = []
        elif reading_ingredients:
            current_order['Ingredients'].append(line)
        elif line in ['Closed', 'lunch', 'Delivery']:  # Status, Meal, DeliveryType lines
            # These lines indicate specific fields, but if they are consistent, you might not need to store them
            continue
        else:
            # Vendor or other fields not explicitly handled above
            current_order['Vendor'] = line
    
    # Add the last order if the loop ends without adding it
    if current_order:
        orders.append(current_order)
    
    return pd.DataFrame(orders)

# Streamlit interface code remains the same


def parse_orders(text_data):
    orders_text = split_into_orders(text_data)
    orders = [parse_order(order_text) for order_text in orders_text if parse_order(order_text) is not None]
    return pd.DataFrame(orders)

# Streamlit app interface
st.title("Lunch Order Analysis")

data = st.text_area("Paste your order data here:", height=300)

if st.button("Analyze Orders"):
    if data:
        df = parse_orders(data)
        if not df.empty:
            st.write("Parsed Orders:", df)
            
            # Visualization: Total Spend by Vendor
            fig = px.bar(df, x='Vendor', y='Payment', title='Total Payment by Vendor')
            st.plotly_chart(fig)
        else:
            st.error("Could not parse any orders from the provided data. Please check the format.")
    else:
        st.error("Please paste order data above.")
