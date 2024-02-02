import streamlit as st
import pandas as pd

def parse_orders(text_data):
    # Initialize variables for processing
    orders = []
    current_order = {'Ingredients': []}  # Initialize with an empty 'Ingredients' list
    ingredients_reading_mode = False

    lines = text_data.split('\n')

    for line in lines:
        line = line.strip()

        if not line:  # Blank line, indicating either the end of an order or ingredients list
            if ingredients_reading_mode:  # If it was reading ingredients, it continues to the next line
                ingredients_reading_mode = False
            elif current_order:  # End of an order, add it to the list and reset
                # Ensure 'Total' and 'Subsidised' are present
                current_order.setdefault('Total', 0.0)
                current_order.setdefault('Subsidised', 0.0)
                current_order['Payment'] = current_order['Total'] - current_order['Subsidised']
                orders.append(current_order)
                current_order = {'Ingredients': []}  # Reset for the next order
            continue

        # Start capturing ingredients after the 'Item' line
        if ingredients_reading_mode:
            current_order['Ingredients'].append(line)
            continue

        # Detect line content and fill the current_order dictionary accordingly
        if 'at' in line and 'GMT' in line:  # Date line found
            current_order['Date'] = line.split(' at ')[0]
        elif 'credits' in line:  # Total or Subsidised line found
            value = float(line.split()[0])
            if 'Total' not in current_order:
                current_order['Total'] = value
            else:
                current_order['Subsidised'] = value
        elif line.startswith('1x '):  # Item line found, next lines will be ingredients
            current_order['Item'] = line[3:]  # Remove '1x ' prefix
            ingredients_reading_mode = True  # Next lines are ingredients until a blank line
        else:
            # This simple example assumes the first unknown line after 'Date' is 'Vendor'
            # Adjust this logic based on your actual data structure
            if 'Vendor' not in current_order:
                current_order['Vendor'] = line

    # Capture the last order if the text doesn't end with a blank line
    if current_order and not ingredients_reading_mode:
        current_order.setdefault('Total', 0.0)
        current_order.setdefault('Subsidised', 0.0)
        current_order['Payment'] = current_order['Total'] - current_order['Subsidised']
        orders.append(current_order)

    return pd.DataFrame(orders)

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
