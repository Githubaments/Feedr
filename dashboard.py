import streamlit as st
import pandas as pd
import re

def split_into_orders(text_data):
    # Split on two newline characters, which seems to be the consistent separator between orders
    return re.split(r'\n\n+', text_data.strip())

def parse_order(order_text):
    # Adjusted regex pattern to capture the structure of an individual order
    order_pattern = re.compile(
        r'(?P<Date>\d{2} Jan \d{2}) at (?P<Time>[\d: -]+ \(GMT\))\n'
        r'(?P<Status>\w+)\n'
        r'(?P<Meal>\w+)\n'
        r'(?P<DeliveryType>\w+)\n'
        r'(?P<Vendor>[^\n]+)\n'
        r'(?P<Item>1x [^\n]+)\n'  # Assuming '1x ' prefix is consistent
        r'(?P<Ingredients>(?:.*\n)*?)'  # Non-greedy match for ingredients list
        r'(?P<Total>\d+\.\d+) credits\n'
        r'(?P<Subsidised>\d+\.\d+) credits',
        re.DOTALL  # Allows '.' to match across multiple lines for Ingredients
    )
    match = order_pattern.search(order_text)
    if match:
        order = match.groupdict()
        order['Total'] = float(order['Total'])
        order['Subsidised'] = float(order['Subsidised'])
        order['Payment'] = order['Total'] - order['Subsidised']
        order['Ingredients'] = [ingredient for ingredient in order['Ingredients'].strip().split('\n') if ingredient]
        order['Item'] = order['Item'].replace('1x ', '')
        return order
    else:
        return None

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
