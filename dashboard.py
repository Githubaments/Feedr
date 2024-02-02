import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Function to parse text data
def parse_order(text):
    # Regular expression to match the order data format
    pattern = re.compile(
        r'(\d{2} [A-Za-z]+ \d{2}) at (\d{2}:\d{2} - \d{2}:\d{2} \(GMT\))\n'
        r'(Closed)\n'
        r'(lunch)\n'
        r'(Delivery)\n'
        r'([A-Za-z ]+)\n'
        r'(\dx [A-Za-z ]+)\n\n'
        r'((?:.*\n)*?)'  # Non-greedy match for multiple lines of ingredients
        r'(\d+\.\d+) credits\n\n'
        r'(\d+\.\d+) credits'
    )

    orders = text.strip().split('\n\n\n')  # Splitting based on the pattern in provided data
    parsed_orders = []

    for order in orders:
        match = pattern.search(order)
        if match:
            date, time, status, meal, delivery_type, vendor, item, ingredients, total, subsidised = match.groups()
            ingredients = ingredients.strip().split('\n') if ingredients.strip() else []
            parsed_orders.append({
                'date': date.strip(),
                'time': time.strip(),
                'status': status.strip(),
                'meal': meal.strip(),
                'delivery_type': delivery_type.strip(),
                'vendor': vendor.strip(),
                'item': item.strip(),
                'ingredients': ingredients,
                'total': float(total.strip()),
                'subsidised': float(subsidised.strip())
            })

    return parsed_orders


# Streamlit interface
st.title("Order Analysis App")

# Text area for user to paste data
data = st.text_area("Paste your order data here:", height=300)

# Button to parse data
if st.button("Analyze Orders"):
    if data:
        df = parse_data(data)
        st.write(df)

        # Show stats using pandas
        total_spend = df['Total'].sum()
        st.write("Total Spend: ", total_spend)

        # Show a plot using plotly
        fig = px.bar(df, x='Vendor', y='Total', title="Total Spend by Vendor")
        st.plotly_chart(fig)

    else:
        st.error("Please paste order data above.")
