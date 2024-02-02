import streamlit as st
import pandas as pd

def parse_orders(text_data):
    # Initialize variables for processing
    orders = []
    current_order = {}
    lines = text_data.strip().split('\n')
    
    # Helper function to reset the current order and prepare for the next
    def reset_current_order():
        return {'Ingredients': []}
    
    # Indicators of the current section being processed
    process_next_line_as_vendor = False
    
    for line in lines:
        line = line.strip()
        
        if not line:  # Blank line indicates the end of a section or order
            if current_order:  # End of an order
                orders.append(current_order)
                current_order = reset_current_order()
                process_next_line_as_vendor = False  # Reset the indicator
            continue
        
        # Using flags to identify what to do with each line
        if process_next_line_as_vendor:
            current_order['Vendor'] = line
            process_next_line_as_vendor = False  # Reset the flag
            continue
        
        # Identifying sections based on known prefixes or patterns
        if 'DATE' in line:
            # Skip the DATE line or parse it if you need the date
            pass
        elif 'at' in line and 'GMT' in line:  # This line contains the date and time
            current_order['Date'] = line.split(' at ')[0]
        elif 'Delivery' in line:  # The line before the vendor
            process_next_line_as_vendor = True
        elif line.startswith('1x '):  # Marks the beginning of items
            current_order['Item'] = line[3:]  # Remove '1x ' prefix
        elif 'credits' in line:
            # Assuming the Total and Subsidised are always at the end
            if 'Total' not in current_order:
                current_order['Total'] = float(line.split()[0])
            else:
                current_order['Subsidised'] = float(line.split()[0])
        else:
            # Handle ingredients and other details as needed
            current_order.setdefault('Ingredients', []).append(line)
    
    # Don't forget to add the last order if it ends without a trailing newline
    if current_order:
        orders.append(current_order)
    
    # Calculate Payment for each order
    for order in orders:
        total = order.get('Total', 0.0)
        subsidised = order.get('Subsidised', 0.0)
        order['Payment'] = total - subsidised
    
    return pd.DataFrame(orders)

# Integration with Streamlit interface remains as previously described


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
