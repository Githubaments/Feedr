import streamlit as st
import pandas as pd

def parse_orders(text_data):
    orders = []
    current_order = {'Ingredients': []}  # Initialize with an empty 'Ingredients' list
    credits_counter = 0  # Counter to differentiate between Total and Subsidised

    for line in text_data.split('\n'):
        line = line.strip()

        # Reset for new order
        if not line:
            if current_order:
                # Ensure the last order is added
                orders.append(current_order)
                current_order = {'Ingredients': []}
                credits_counter = 0  # Reset counter for the next order
            continue

        if 'DATE' in line or 'STATUS' in line or 'MEAL' in line or 'DELIVERY TYPE' in line:
            # These lines can be parsed for additional order details if necessary
            pass
        elif 'credits' in line:
            value = float(line.split()[0])
            if credits_counter == 0:  # First occurrence
                current_order['Total'] = value
                credits_counter += 1
            else:  # Second occurrence
                current_order['Subsidised'] = value
                # Calculate Payment now that we have both values
                current_order['Payment'] = current_order['Total'] - current_order['Subsidised']
        elif line.startswith('1x '):  # Item line found
            current_order['Item'] = line[3:]  # Remove '1x ' prefix
        elif 'at' in line and 'GMT' in line:  # Date and time line
            # Assuming the date is always at the start of the order
            current_order['Date'] = line.split(' at ')[0]
        else:
            # Assuming the line before items start is always the Vendor
            if 'Vendor' not in current_order:
                current_order['Vendor'] = line
            else:
                # All other lines before the 'Total' are considered as ingredients
                current_order['Ingredients'].append(line)

    # Add the last order if it wasn't added
    if current_order and 'Total' in current_order and 'Subsidised' in current_order:
        orders.append(current_order)

    return pd.DataFrame(orders)




# Integration with Streamlit interface remains as previously described


# Streamlit app interface remains unchanged


# Streamlit interface
st.title("Lunch Order Analysis")

data = st.text_area("Paste your order data here:", height=300)

if st.button("Analyze Orders"):
    if data:
        df = parse_orders(data)
        #df = df.dropna(subset=['Item'])
        if not df.empty:
            st.write("Parsed Orders:", df)
        else:
            st.error("Could not parse any orders from the provided data. Please check the format.")
    else:
        st.error("Please paste order data above.")
