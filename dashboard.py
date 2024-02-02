import streamlit as st
import pandas as pd

def parse_orders(text_data):
    # Split the data into blocks for each order
    order_blocks = text_data.strip().split('\n\n\n')
    
    # Initialize a list to hold all parsed orders
    parsed_orders = []
    
    for block in order_blocks:
        lines = block.split('\n')
        order = {}
        
        # Assuming the first line always contains the date and time
        order['Date'] = lines[0].split(' at ')[0]
        
        # Direct assignments based on the structure
        order['Status'] = lines[1]
        order['Meal'] = lines[2]
        order['DeliveryType'] = lines[3]
        order['Vendor'] = lines[4]
        order['Item'] = lines[5].lstrip('1x ')
        
        # Ingredients are variable; capture until we hit a line with "credits"
        ingredients_index = 6
        ingredients = []
        while 'credits' not in lines[ingredients_index]:
            ingredients.append(lines[ingredients_index])
            ingredients_index += 1
        
        order['Ingredients'] = ingredients
        
        # The next lines after ingredients are Total and Subsidised
        order['Total'] = float(lines[ingredients_index].split()[0])
        order['Subsidised'] = float(lines[ingredients_index + 2].split()[0])  # Assuming an empty line between
        
        # Calculate Payment
        order['Payment'] = order['Total'] - order['Subsidised']
        
        parsed_orders.append(order)
    
    return pd.DataFrame(parsed_orders)


# Streamlit app interface remains unchanged


# Streamlit interface
st.title("Lunch Order Analysis")

data = st.text_area("Paste your order data here:", height=300)

if st.button("Analyze Orders"):
    if data:
        df = parse_orders(data)
        df = df.dropna(subset=['Item'])
        if not df.empty:
            st.write("Parsed Orders:", df)
        else:
            st.error("Could not parse any orders from the provided data. Please check the format.")
    else:
        st.error("Please paste order data above.")
