import streamlit as st
import pandas as pd

def parse_orders(text_data):
    # Initialize a list to hold all parsed orders
    parsed_orders = []

    # Split the input text into lines for processing
    lines = text_data.split('\n')

    # Temporary storage for the current order's details
    current_order = {}

    for line in lines:
        line = line.strip()
        if not line and current_order:  # End of an order
            # Add the current order to the list and reset for the next order
            parsed_orders.append(current_order)
            current_order = {}
        else:
            # Split the line into key-value pairs based on the first colon encountered
            parts = line.split(',', 1)
            if len(parts) == 2:
                key, value = parts[0], parts[1]

                # Assign values to the corresponding keys in the current_order dictionary
                if key in ['DATE', 'STATUS', 'MEAL', 'DELIVERY TYPE', 'VENDOR', 'ITEMS']:
                    current_order[key] = value
                elif 'credits' in line:
                    # Handle monetary values separately
                    if 'TOTAL' not in current_order:
                        current_order['TOTAL'] = float(value.split()[0])
                    else:
                        current_order['SUBSIDISED'] = float(value.split()[0])
                        # Calculate payment once both total and subsidised are known
                        current_order['PAYMENT'] = current_order['TOTAL'] - current_order['SUBSIDISED']

    # Ensure the last order is added if the loop ends without an empty line
    if current_order:
        parsed_orders.append(current_order)

    # Convert the list of orders into a DataFrame
    df = pd.DataFrame(parsed_orders)

    # Correcting column names and ensuring all expected columns are present
    expected_columns = ['DATE', 'STATUS', 'MEAL', 'DELIVERY TYPE', 'VENDOR', 'ITEMS', 'TOTAL', 'SUBSIDISED', 'PAYMENT']
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None  # Add missing columns with None values

    return df



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
