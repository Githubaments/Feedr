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

# Analysis and visualization function
def analyze_and_visualize(df):
    import plotly.express as px

    vendor_counts_sorted = df.groupby(['Vendor', 'Year']).size().reset_index(name='Order Count').sort_values(by='Order Count', ascending=False)

    fig_vendor_counts = px.bar(vendor_counts_sorted, x='Vendor', y='Order Count', color='Year', 
                           title="Top Vendors by Order Count, Split by Year", 
                           text='Year', category_orders={"Vendor": vendor_counts_sorted['Vendor']})

    fig_vendor_counts.update_layout(xaxis_title="Vendor", yaxis_title="Order Count")

    st.plotly_chart(fig_vendor_counts, use_container_width=True)

    
    # Calculating totals
    total_sum = df['Total'].sum()
    subsidised_sum = df['Subsidised'].sum()
    paid_sum = df['Paid'].sum()

    # Displaying totals
    st.write(f"Total Sum: {total_sum}")
    st.write(f"Subsidised Sum: {subsidised_sum}")
    st.write(f"Paid Sum: {paid_sum}")

    # Visualization for Most Popular Vendors by Order Count, split by year
    fig_vendor_counts = px.bar(df, x='Vendor', color='Year', title="Top Vendors by Order Count, Split by Year",
                               labels={"count": "Order Count"}, text='Year')
    fig_vendor_counts.update_layout(xaxis_title="Vendor", yaxis_title="Order Count")

    # Visualization for Most Popular Vendors by Total Paid, split by year
    vendor_totals_by_year = df.groupby(['Vendor', 'Year'])['Total'].sum().reset_index()
    fig_vendor_totals = px.bar(vendor_totals_by_year, x='Vendor', y='Total', color='Year', 
                               title="Vendors by Total Paid, Split by Year")
    fig_vendor_totals.update_layout(xaxis_title="Vendor", yaxis_title="Total Paid")

    # Visualization for Top 5 Dishes, split by year
    # Note: Adjusting the approach to identify top dishes by year might require more specific handling
    top_dishes_by_year = df.groupby(['Items', 'Year']).size().reset_index(name='counts')
    top_dishes_by_year_sorted = top_dishes_by_year.sort_values(by='counts', ascending=False).head(5)
    fig_top_dishes = px.bar(top_dishes_by_year_sorted, x='Items', y='counts', color='Year', 
                            title="Top 5 Dishes by Count, Split by Year")
    fig_top_dishes.update_layout(xaxis_title="Dish", yaxis_title="Count")

    # Displaying visualizations
    st.plotly_chart(fig_vendor_counts, use_container_width=True)
    st.plotly_chart(fig_vendor_totals, use_container_width=True)
    st.plotly_chart(fig_top_dishes, use_container_width=True)


    # Group by month and vendor, then count unique occurrences
    vendor_counts_by_time = df.groupby([df['Year'], 'Vendor']).size().reset_index(name='Counts')
    vendor_counts_by_time    
    fig = px.line(vendor_counts_by_time, x='Year', y='Counts', color='Vendor', 
                  title='Vendor Order Counts Over Time',
                  labels={'Counts': 'Number of Orders'})
    fig.update_layout(xaxis_title='Time', yaxis_title='Number of Orders', xaxis=dict(tickformat="%b %Y"))
    st.plotly_chart(fig, use_container_width=True)

    return

def load_data():
    data = st.text_area("Paste your order data here:", height=300)
    return data

# Streamlit interface
st.title("Lunch Order Analysis")
data = load_data()

df = parse_orders(data)
df = edit_df(df)
df['Year'] = df['Date'].str.split(' ').apply(lambda x: x[2])
unique_years = df['Year'].unique()
unique_years.sort()  # Optional: sort the years
        
selected_years = st.multiselect('Select Years:', options=unique_years, default=unique_years)
        
df = df[df['Year'].isin(selected_years)]
analyze_and_visualize(df)
if not df.empty:
    st.write("Parsed Orders:", df)
else:
    st.error("Could not parse any orders from the provided data. Please check the format.")

