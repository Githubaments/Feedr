import streamlit as st
import pandas as pd

def parse_orders(text_data):
    orders = []
    current_order = {}
    for line in text_data.split('\n'):
        line = line.strip()
        if not line:  # Blank line indicates the end of an order
            if current_order:  # Add the current order if it exists
                # Ensure 'Total' and 'Subsidised' are present
                current_order.setdefault('Total', 0.0)
                current_order.setdefault('Subsidised', 0.0)
                orders.append(current_order)
                current_order = {}
        else:
            # Process each line to extract order details
            # Assuming a simplified format here for demonstration; adjust as needed
            if 'DATE' in line:
                # This is where you'd normally parse the date, but it's skipped for simplicity
                pass
            elif 'credits' in line:
                value = float(line.split()[0])
                if 'Total' not in current_order:
                    current_order['Total'] = value
                else:
                    current_order['Subsidised'] = value
            else:
                # Additional parsing logic for other fields
                pass
    
    # Don't forget to add the last order if the input doesn't end with a blank line
    if current_order:
        current_order.setdefault('Total', 0.0)
        current_order.setdefault('Subsidised', 0.0)
        orders.append(current_order)
    
    df = pd.DataFrame(orders)
    
    # Compute 'Payment' only if 'Total' and 'Subsidised' columns are present
    if 'Total' in df.columns and 'Subsidised' in df.columns:
        df['Payment'] = df['Total'] - df['Subsidised']
    else:
        df['Payment'] = 0.0  # Or set to an appropriate default or error value
    
    return df

# Streamlit app interface remains unchanged


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
