import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Define a function to parse the text data
def parse_orders(text_data):
    # Define the regular expression pattern for the data structure
    order_pattern = re.compile(
        r'(?P<Date>\d{2} Jan \d{2}) at (?P<Time>[\d: -]+ \(GMT\))\n'
        r'(?P<Status>\w+)\n'
        r'(?P<Meal>\w+)\n'
        r'(?P<DeliveryType>\w+)\n'
        r'(?P<Vendor>[\w ]+)\n'
        r'(?P<Item>[\dx ]+[\w ]+)\n\n'
        r'(?P<Ingredients>(?:.+\n)*)'  # Non-greedy match for ingredients list
        r'(?P<Total>\d+\.\d+) credits\n\n'
        r'(?P<Subsidised>\d+\.\d+) credits',
        re.MULTILINE
    )
    
    # Find all matches in the text data
    matches = order_pattern.finditer(text_data)
    
    # Create a list of dictionaries from the matches
    orders = [match.groupdict() for match in matches]
    
    # Convert 'Total' and 'Subsidised' to numeric types and 'Ingredients' to lists
    for order in orders:
        order['Total'] = float(order['Total'])
        order['Subsidised'] = float(order['Subsidised'])
        order['Ingredients'] = order['Ingredients'].strip().split('\n') if order['Ingredients'].strip() else []
    
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
