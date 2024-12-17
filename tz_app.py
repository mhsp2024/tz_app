import requests
import pandas as pd
import streamlit as st

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI3IiwianRpIjoiMjIyZTM5OGE4YzA5M2M2NmMyNzIwNDFjZTQzNWY2ZDczYzc4YTE4YWE1ZDk2ZmRlYzE3MjJlYjAxMzdkNTJjMDYzYTJkMzUzMGQxYzIxYzQiLCJpYXQiOjE3MTU4MDgwOTguNzM1NzMxLCJuYmYiOjE3MTU4MDgwOTguNzM1NzM0LCJleHAiOjE3NDczNDQwOTguNzMzMzI0LCJzdWIiOiIxNzM2Iiwic2NvcGVzIjpbXX0.vVtqcEP_JPKp6co5rmnZErB7ZGmSSjxpkxdVIdUWGjRHSTUEXHQfZ9nByfagaPCaQa5CGohcROWqU9vBowDOt1m-1xnYx_7N-hzBG7WqVtXTXHSPzeqXkNVXllYuaJ7LS8lFIEotSE3G2iHPz_evdiHHpFmQqsfnU2NL3RgfHtyj_5WRBtEYlTh8tKP-gR-RhRN8b6LDtObKN_nLwpcivpSqTp5Gybxez02mpjbVxjwit6tYWYqAvFUnt2Z_E5ZsCuAFPpayngOsPa-Tupfyuv03Z-ZLl3PRzxWd-udjUj05YacNP0zFXghrnsaE_z1SI2xWhbREyp37y65ZkSGs_UJoTwMTFRTMs322iw8tIB_2LCeBtEh4gmCqQ3YmeMhT9LFU7AAX4DNmPInyCmr3XXe7MDs0Uh2Pv_pxEdaO_awZJi0fZHNrotscSw9VcwWbR_03lBPvzETvtInCNo3yNPyc2z8C-f_q7aV9fPJNBOe7m2DprOpjfZEvy2Oa6B3qav8ImQRRY9gnX1OToH4awLyIaJNsfHGvWbgzqBZUXkEms7YiehqjiSfuGgoNuUiisG5-D8OwVrGc68QhnBK9_EdJYHxFM28AOAgxVfaoqULRNNfrnGvI07E7cPoBb7n83w13w9CvIxgdm2BYfV3rB668oVlkGhusYVNOWVBUgBI"

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
