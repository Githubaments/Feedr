import streamlit as st
import pandas as pd

def parse_orders(text_data):
    # Initialize variables for processing
    orders = []
    current_order = {}
    lines = text_data.split('\n')

    for line in lines:
        line = line.strip()
        if not line:  # Checks for empty lines indicating possible end of an order
            if current_order:  # If there's an order being processed, add it to the list
                orders.append(current_order)
                current_order = {}  # Reset for the next order
        elif 'DATE' in line or 'STATUS' in line or 'MEAL' in line or 'DELIVERY TYPE' in line:
            # Skip these lines or handle accordingly
            continue
        else:
            # Parse the line based on known formats, assuming ':' is a delimiter
            parts = line.split(':')
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else None

            if key in ['Total', 'Subsidised']:
                current_order[key] = float(value.split()[0]) if value else 0.0
            else:
                current_order[key] = value

    # Handling the last order in case there's no trailing newline
    if current_order:
        orders.append(current_order)

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(orders)

    # Post-processing DataFrame
    if not df.empty:
        df['Payment'] = df['Total'] - df['Subsidised']
        df['Item'] = df['Item'].str.replace('1x ', '', regex=False)  # Clean up item names

    return df

# Streamlit interface
st.title("Lunch Order Analysis")

data = st.text_area("Paste your order data here:", height=300)

if st.button("Analyze Orders"):
    if data:
        df = parse_orders(data)
        if not df.empty:
            st.write("Parsed Orders:", df)
        else:
            st.error("Could not parse any orders from the provided data. Please check the format.")
    else:
        st.error("Please paste order data above.")
