import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Define a function to parse the text data
def parse_orders(text_data):
    # Regular expression pattern to capture order details
    order_pattern = re.compile(
        r'(?P<Date>\d{2} Jan \d{2}) at (?P<Time>[\d: -]+ \(GMT\))\n'
        r'(?P<Status>\w+)\n'
        r'(?P<Meal>\w+)\n'
        r'(?P<DeliveryType>\w+)\n'
        r'(?P<Vendor>[^\n]+)\n'
        r'(?P<Item>[\dx ]+[^\n]+)\n\n'  # Adjusted to handle items more flexibly
        r'(?P<Ingredients>(?:.*\n)*)'  # Capture ingredients, handling multiple lines
        r'(?P<Total>\d+\.\d+) credits\n\n'
        r'(?P<Subsidised>\d+\.\d+) credits',
        re.MULTILINE | re.DOTALL  # Match across multiple lines
    )
    
    matches = order_pattern.finditer(text_data)
    orders = []
    
    for match in matches:
        order = match.groupdict()
        order['Total'] = float(order['Total'])
        order['Subsidised'] = float(order['Subsidised'])
        order['Ingredients'] = order['Ingredients'].strip().split('\n') if order['Ingredients'].strip() else []
        orders.append(order)
    
    if orders:
        df = pd.DataFrame(orders)
        df.drop(['Time', 'Status', 'Meal', 'DeliveryType'], axis=1, errors='ignore', inplace=True)
        df['Payment'] = df['Total'] - df['Subsidised']
        df['Item'] = df['Item'].str.replace('1x ', '', regex=False)
        return df
    else:
        return pd.DataFrame()

# Streamlit app interface
st.title("Lunch Order Analysis")

data = st.text_area("Paste your order data here:", height=300)

if st.button("Analyze Orders"):
    if data:
        df = parse_orders(data)
        if not df.empty:
            st.write("Parsed Orders:", df)
            
            # Visualization: Total Spend by Vendor
            fig = px.bar(df, x='Vendor', y='Total', color='Vendor', title='Total Spend by Vendor')
            st.plotly_chart(fig)
            
            # Additional analysis as needed
            total_spend = df['Total'].sum()
            st.write(f"Total Spend: {total_spend} credits")
        else:
            st.error("Could not parse any orders from the provided data. Please check the format.")
    else:
        st.error("Please paste order data above.")
