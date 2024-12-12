import requests
import pandas as pd
import streamlit as st

# API Token
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI3IiwianRpIjoiZjY1N2ZiZDk5ZDliZWEyMzdlMWQ3NTZkN2Q4MDViNWNlZDhlZDZhMDhkMTIzYTRlNmQxYTBjYjdjYTZhM2FmM2EyMWY2MTQ3MDUzYTNmMzciLCJpYXQiOjE3MzM5OTcxMzIuNjgyNzI4LCJuYmYiOjE3MzM5OTcxMzIuNjgyNzMsImV4cCI6MTc2ODIxMTUzMi42NzYyMDUsInN1YiI6IjE3MzYiLCJzY29wZXMiOltdfQ.RZOp4aR2WAjd12W1Gw_yma0fPmO9XVmIoHScVN6Qh7DW4lApjdJWjwniFFE4hoV55cBdMj05GgHuwKzh1pk3-aJoKhKKMyC3XAeMJI1W9kRvTDc0Yasmt2oO13BgzBGIg4nAEhKjnp58dXdBQVjM4f6mwWotmAXrpxAJsBKe0xPpDoy9wA6CePXLyAeSWKjr94d-To6noRieEqSz2KVOsF3rKJOwO-fA_7ZxdgEYJ_UBgh5his7SAiU48Kqh_3q5zRp58Eq_1SOO7Cgsm-GK3l6agnEgU5Zv6vlaNRq5IQoAcHXXr-VgIYRaGXLz6EJGqCySUoWoMTjRmsqUjDBaUzQ8n7dUhiGmdXEG4eNQkvAZBnG4ckliqvUgMm3d1chvG2mamirE782Btw0n__JMwYxwbAFl-rbTYffryr55RAn1SCEmCucqr7yUmgJQH4tn5XDHX461a0-Fh0BJik-YcxCaknGt6Ihw1BGn2EDYWmxg0wrTklCK40kv4au5ma94p-lb6sPBS95p4KXZ-Rcf9gqsLZ44KK-XwbWQPsDg7ZIkMg0wxbw86mAdBJL9YOgecHWMRliBefXfLdEatshh5435BHoPkx1q8yqEcm2WPsU93z2TWbhqEIGKQfExNrXOPWPDLlqTcWPQ133x4pb_UvqzBnG37dCQB6mKHIQ2-9Q"  # Replace with your actual API token

# Headers for the API Request
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# List of URLs to fetch data from
all_urls = [
    'https://app.tracezilla.com/api/v1/wooden-spoon/price-lists/purchase',
    'https://app.tracezilla.com/api/v1/wooden-spoon/price-lists/sales',
    'https://app.tracezilla.com/api/v1/wooden-spoon/recipes',
    'https://app.tracezilla.com/api/v1/wooden-spoon/skus',
    'https://app.tracezilla.com/api/v1/wooden-spoon/orders',
    'https://app.tracezilla.com/api/v1/wooden-spoon/invoices',
    'https://app.tracezilla.com/api/v1/wooden-spoon/partners'
]

# Function to fetch data for each URL with pagination
def fetch_data(url):
    all_data = []
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data['data'])
            # Check if there is a next page
            next_page = data['links'].get('next')
            if next_page:
                page += 1
            else:
                break
        else:
            st.error(f"Error fetching data from {url}: {response.status_code}")
            break
    return all_data

# Convert API data to a Pandas DataFrame
def process_data_to_dataframe(data):
    try:
        return pd.json_normalize(data)  # Flatten nested JSON if needed
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return None

# Streamlit App
st.title("Tracezilla Data Viewer")

# Loop through the URLs and fetch data for each one
for url in all_urls:
    st.subheader(f"Data from: {url}")
    
    # Fetch data for the current URL
    data = fetch_data(url)
    
    if data:
        # Convert data to DataFrame
        df = process_data_to_dataframe(data)
        
        if df is not None:
            # Display the table for the current dataset
            st.dataframe(df)  # Display interactive table

            # Add filter for customer partner or any field (example for filtering 'customer_partner.name')
            if 'customer_partner.name' in df.columns:
                customers = df['customer_partner.name'].dropna().unique()
                selected_customer = st.selectbox(f"Filter by Customer for {url}", options=["All"] + list(customers))

                if selected_customer != "All":
                    filtered_df = df[df['customer_partner.name'] == selected_customer]
                else:
                    filtered_df = df
                st.write(f"Showing results for: {selected_customer}")
                st.dataframe(filtered_df)

                # Export to CSV option
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label=f"Download CSV for {url}",
                    data=csv,
                    file_name=f"{url.split('/')[-1]}_data.csv",
                    mime="text/csv"
                )
            else:
                st.write("No customer partner name column found for filtering.")
        else:
            st.error(f"Failed to process data for {url}.")
    else:
        st.error(f"Failed to fetch data from {url}.")