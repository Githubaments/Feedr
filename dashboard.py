import streamlit as st
import pandas as pd

def find_subsudused(input_string):
    # Find the last index of the word "SUBSIDISED" in the string
    last_index = input_string.rfind("SUBSIDISED")
    
    # Check if "SUBSIDISED" is found in the string
    if last_index != -1:
        # Get everything after the last occurrence of "SUBSIDISED" (excluding "SUBSIDISED" itself)
        result = input_string[last_index + len("SUBSIDISED"):]
    else:
        result = input_string
    return result

def edit_df(df):
    df['Items'] = df['Items'].str.replace('1x ', '')
    df = df.drop(['Time', 'Status', 'Meal', 'Delivery Type'], axis=1, errors='ignore')
    df[['Total', 'Subsidised']] = df[['Total', 'Subsidised']].apply(pd.to_numeric, errors='coerce')
    df['Paid'] = df['Total'] - df['Subsidised'] 
    return df

def parse_orders(text_data):
    import re
    text_data = find_subsudused(text_data)
    # Splitting the input text into individual records
    records = re.split(r'\n(?=\d{2} \w+ \d{2})', text_data.strip())
    
    # Initialize an empty list to hold the parsed data
    data = []
    
    # Parsing each record
    for record in records:
        lines = record.strip().split('\n')
        date = lines[0].split(' at ')[0]
        status = lines[1]
        meal = lines[2]
        delivery_type = lines[3]
        vendor = lines[4]
        items_start_index = 5
        items_end_index = len(lines) - 3  # Items end before the last 3 lines which include the total and subsidised amounts
        items = ' '.join(lines[items_start_index:items_end_index])
        total = lines[-3].split(' ')[0]  # Assuming the total and subsidised amounts are always the last 3 lines
        subsidised = lines[-1].split(' ')[0]
    
        data.append([date, status, meal, delivery_type, vendor, items, total, subsidised])
    
    # Create a DataFrame
    columns = ['Date', 'Status', 'Meal', 'Delivery Type', 'Vendor', 'Items', 'Total', 'Subsidised']
    df = pd.DataFrame(data, columns=columns)

    return df




# Integration with Streamlit interface remains as previously described


# Streamlit app interface remains unchanged


# Streamlit interface
st.title("Lunch Order Analysis")

data = st.text_area("Paste your order data here:", height=300)

if st.button("Analyze Orders"):
    if data:
        df = parse_orders(data)
        df = edit_df(df)
        #df = df.dropna(subset=['Item'])
        if not df.empty:
            st.write("Parsed Orders:", df)
        else:
            st.error("Could not parse any orders from the provided data. Please check the format.")
    else:
        st.error("Please paste order data above.")
