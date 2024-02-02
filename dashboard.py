import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Define a function to parse the text data
def parse_orders(text_data):
    orders = []
    current_order = {}
    lines = text_data.split('\n')
    for line in lines:
        if line.strip() == '':
            # End of an order, process and reset
            if current_order:
                orders.append(current_order)
                current_order = {}
        else:
            # Process line
            if ' at ' in line and 'GMT' in line:
                current_order['Date'] = line.split(' at ')[0]
            elif line in ['Closed', 'Open']:
                current_order['Status'] = line
            elif line in ['lunch', 'dinner']:
                current_order['Meal'] = line
            elif 'Delivery' in line:
                current_order['DeliveryType'] = line
            elif 'credits' in line:
                if 'Total' not in current_order:
                    current_order['Total'] = float(line.split()[0])
                else:
                    current_order['Subsidised'] = float(line.split()[0])
            else:
                # Assume this line is either Vendor, Item, or Ingredients
                if 'Vendor' not in current_order:
                    current_order['Vendor'] = line
                elif 'Item' not in current_order:
                    current_order['Item'] = line.replace('1x ', '')
                else:
                    # Append to ingredients
                    current_order.setdefault('Ingredients', []).append(line)
                    
    # Catch any order not followed by a blank line
    if current_order:
        orders.append(current_order)
    
    for order in orders:
        order['Payment'] = order.get('Total', 0) - order.get('Subsidised', 0)

    
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(orders).drop(['Time', 'Status', 'Meal', 'DeliveryType'], axis=1, errors='ignore')
    df['Payment'] = df['Total'] - df['Subsidised']
    df['Item'] = df['Item'].str.replace('1x ', '')

    return df

# Streamlit app interface
st.title("Lunch Order Analysis")

# Text area for user to paste data
data = st.text_area("Paste your order data here:", height=300)

# Button to parse and analyze data
if st.button("Analyze Orders"):
    if data:
        # Parse the text data into a DataFrame
        df = parse_orders(data)
        
        if not df.empty:
            # Display the DataFrame
            st.write(df)

            # Perform DataFrame operations
            total_spend = df['Total'].sum()
            st.write(f"Total Spend: {total_spend} credits")

            # Visualization example
            fig = px.bar(df, x='Vendor', y='Total', title='Total Spend by Vendor')
            st.plotly_chart(fig)
        else:
            st.error("Could not parse any orders from the provided data. Please check the format.")
    else:
        st.error("Please paste order data above.")
