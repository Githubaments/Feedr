import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Function to parse the text data
def parse_orders(text_data):
    # Regular expression pattern to match each order's details
    order_pattern = re.compile(
        r'(?P<Date>\d{2} Jan \d{2}) at (?P<Time>[\d: -]+ \(GMT\))\n'
        r'(?P<Status>\w+)\n'
        r'(?P<Meal>\w+)\n'
        r'(?P<DeliveryType>\w+)\n'
        r'(?P<Vendor>[\w ]+)\n'
        r'(?P<Item>1x [\w ]+[\w ]*)\n\n'  # Adjusted to capture leading '1x '
        r'(?P<Ingredients>(?:.*\n)*)'  # Non-greedy match for ingredients list
        r'(?P<Total>\d+\.\d+) credits\n\n'
        r'(?P<Subsidised>\d+\.\d+) credits',
        re.MULTILINE
    )
    
    # Find all matches in the text data
    matches = order_pattern.finditer(text_data)
    
    # Create a list of dictionaries from the matches
    orders = [match.groupdict() for match in matches]
    
    # Process each order to adjust data according to requirements
    for order in orders:
        order['Total'] = float(order['Total'])
        order['Subsidised'] = float(order['Subsidised'])
        order['Payment'] = order['Total'] - order['Subsidised']
        order['Ingredients'] = [ingredient.strip() for ingredient in order['Ingredients'].strip().split('\n') if ingredient.strip()]  # Split and strip each ingredient
        order['Item'] = order['Item'][3:]  # Remove leading '1x ' from Item
        
    # Convert the list of dictionaries to a pandas DataFrame and drop unnecessary columns
    df = pd.DataFrame(orders).drop(['Time', 'Status', 'Meal', 'DeliveryType'], axis=1)
    
    return df

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
