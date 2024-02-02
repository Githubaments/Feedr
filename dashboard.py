import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Function to parse the text data
def parse_orders(text_data):
    # Split the data on two or more newlines to account for varying gaps between orders
    orders_data = re.split(r'\n\n+', text_data.strip())
    
    # Define the regular expression pattern to capture the details of each order
    order_pattern = re.compile(
        r'(?P<Date>\d{2} Jan \d{2}) at (?P<Time>[\d: -]+ \(GMT\))\n'
        r'(?P<Status>\w+)\n'
        r'(?P<Meal>\w+)\n'
        r'(?P<DeliveryType>\w+)\n'
        r'(?P<Vendor>[^\n]+)\n'  # Use a more generic capture for Vendor to handle spaces and letters
        r'(?P<Item>[^\n]+)\n'  # Similarly, capture the item more broadly
        r'(?P<Ingredients>(?:.*\n)*?)'  # Non-greedy match for potentially multiple ingredients
        r'(?P<Total>\d+\.\d+) credits\n\n'
        r'(?P<Subsidised>\d+\.\d+) credits',
        re.DOTALL  # Allows '.' to match newlines, accommodating multi-line Ingredients
    )
    
    orders = []
    
    for order_text in orders_data:
        match = order_pattern.search(order_text)
        if match:
            order = match.groupdict()
            order['Total'] = float(order['Total'])
            order['Subsidised'] = float(order['Subsidised'])
            order['Payment'] = order['Total'] - order['Subsidised']
            order['Item'] = order['Item'].replace('1x ', '')  # Remove '1x ' prefix from Item
            order['Ingredients'] = order['Ingredients'].strip().split('\n') if order['Ingredients'].strip() else []
            orders.append(order)
    
    # Convert the list of dictionaries to a pandas DataFrame
    if orders:
        df = pd.DataFrame(orders)
        # Drop unnecessary columns if present
        df.drop(['Time', 'Status', 'Meal', 'DeliveryType'], axis=1, errors='ignore', inplace=True)
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no orders were matched


# Streamlit interface
st.title("Lunch Order Analysis")

# Text area for the user to paste data
data = st.text_area("Paste your order data here:", height=300)

# Button to parse and analyze data
if st.button("Analyze Orders"):
    if data:
        # Parse the text data into a DataFrame
        df = parse_orders(data)
        
        if not df.empty:
            # Display the DataFrame
            st.write(df)

            # Visualization example: Total Spend by Vendor
            fig = px.bar(df, x='Vendor', y='Payment', title='Total Payment by Vendor')
            st.plotly_chart(fig)
        else:
            st.error("Could not parse any orders from the provided data. Please check the format.")
    else:
        st.error("Please paste order data above.")
