import requests
import pandas as pd
import streamlit as st
import sys
import os

# recipes :df_recipes
# sku :df_sku_merged
# recipe and ingredients(sku) : df_all_recipes_skus
# production order inbounds : df_order_inbounds_add
# invoices : df_invoice_com
# sku prices : df_prices_sku
# latest sku prices : df_sku_prices


########################################
# here we make connection to tz_get_data_api and get the datasets we need for visualizations
# But the problem is, it takes too long to fetch data from api, causing the generation of 
# website almost impossible
### need to find a way to speed up the process of loading data from api

########################################
## get data in a seperate .py file then import datasets
# Add the path to tz_get_data_api.py
# sys.path.append(os.path.abspath('/path/to/tz_get_data_api'))

#from tz_get_data_api import (
#    df_recipes,
#    df_sku_merged,
#    df_all_recipes_skus,
#    df_order_inbounds_add,
#    df_invoice_com,
#    df_prices_sku)

#######################################

# the above part needs to be fixed, now use two datasets to build up the sample website first

# API_TOKEN = st.secrets["API_TOKEN"]
API_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI3IiwianRpIjoiMjIyZTM5OGE4YzA5M2M2NmMyNzIwNDFjZTQzNWY2ZDczYzc4YTE4YWE1ZDk2ZmRlYzE3MjJlYjAxMzdkNTJjMDYzYTJkMzUzMGQxYzIxYzQiLCJpYXQiOjE3MTU4MDgwOTguNzM1NzMxLCJuYmYiOjE3MTU4MDgwOTguNzM1NzM0LCJleHAiOjE3NDczNDQwOTguNzMzMzI0LCJzdWIiOiIxNzM2Iiwic2NvcGVzIjpbXX0.vVtqcEP_JPKp6co5rmnZErB7ZGmSSjxpkxdVIdUWGjRHSTUEXHQfZ9nByfagaPCaQa5CGohcROWqU9vBowDOt1m-1xnYx_7N-hzBG7WqVtXTXHSPzeqXkNVXllYuaJ7LS8lFIEotSE3G2iHPz_evdiHHpFmQqsfnU2NL3RgfHtyj_5WRBtEYlTh8tKP-gR-RhRN8b6LDtObKN_nLwpcivpSqTp5Gybxez02mpjbVxjwit6tYWYqAvFUnt2Z_E5ZsCuAFPpayngOsPa-Tupfyuv03Z-ZLl3PRzxWd-udjUj05YacNP0zFXghrnsaE_z1SI2xWhbREyp37y65ZkSGs_UJoTwMTFRTMs322iw8tIB_2LCeBtEh4gmCqQ3YmeMhT9LFU7AAX4DNmPInyCmr3XXe7MDs0Uh2Pv_pxEdaO_awZJi0fZHNrotscSw9VcwWbR_03lBPvzETvtInCNo3yNPyc2z8C-f_q7aV9fPJNBOe7m2DprOpjfZEvy2Oa6B3qav8ImQRRY9gnX1OToH4awLyIaJNsfHGvWbgzqBZUXkEms7YiehqjiSfuGgoNuUiisG5-D8OwVrGc68QhnBK9_EdJYHxFM28AOAgxVfaoqULRNNfrnGvI07E7cPoBb7n83w13w9CvIxgdm2BYfV3rB668oVlkGhusYVNOWVBUgBI"

# Headers for the API Request
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

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
    

# get recipes and sku
df_recipes = process_data_to_dataframe(fetch_data('https://app.tracezilla.com/api/v1/wooden-spoon/recipes'))

# recipe and ingredient

def fetch_data_(url):
    all_data = []
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            # Ensure 'data' key exists in the response
            if 'data' in data:
                all_data.extend(data['data'])
            else:
                #print(f"No 'data' key found on page {page}. Stopping.")
                break
            
            # Check for pagination 'links' key safely
            if 'links' in data and data['links'].get('next'):
                page += 1
            else:
                # Stop if 'links' or 'next' key is not present
                #print("No more pages to fetch.")
                break
        else:
            print(f"Error fetching data from {url}: {response.status_code}")
            break
    return all_data

# Get list of Recipes Consumes, build up dataset of recipe and ingredients

all_recipes_data = []

# Loop through all recipe IDs
for recipe_id in df_recipes['id']:
    url = f'https://app.tracezilla.com/api/v1/wooden-spoon/recipes/{recipe_id}/consumes'    
    # Fetch data for the current recipe
    try:
        skus = fetch_data_(url)
        for sku in skus:
            sku['recipe_id'] = recipe_id  # Add recipe_id to each SKU for context
            all_recipes_data.append(sku)
    except Exception as e:
        print(f"Failed to fetch data for Recipe ID {recipe_id}: {e}")

# Convert the collected data into a DataFrame
df_all_recipes_skus = pd.DataFrame(all_recipes_data)




#####################################

# Streamlit App
st.title("Tracezilla Data Viewer")

# Sidebar to select dataset
dataset_name = st.sidebar.selectbox(
    "Select Dataset",
    options=["Recipes", "Recipes and ingredients"]
)

# Display the selected dataset
if dataset_name == "Recipes":
    st.header("Recipe Dataset")
    selected_df = df_recipes
    # filter, with download button
    if 'name' in selected_df.columns:
        # Get unique names
        names = selected_df['name'].dropna().unique()
        # Add a selectbox
        selected = st.selectbox("Filter by Recipe name", options=["All"] + list(names))
        # Filter the dataset based on the selected name
        if selected != "All":
            filtered_df = selected_df[selected_df['name'] == selected]
        else:
            filtered_df = selected_df
        # Display the filtered dataset
        st.write(f"Showing results for: {selected}")
        st.dataframe(filtered_df)
        # Convert the filtered dataset to CSV
        csv = filtered_df.to_csv(index=False)
        # Add a download button to export the dataset as CSV
        st.download_button(
            label="Download Filtered Dataset as CSV",
            data=csv,
            file_name="filtered_dataset.csv",
            mime="text/csv"
        )
    else:
        # Display a message if the 'name' column is not found
        st.write("The 'name' column is not found in the dataset. Please check the data.")

elif dataset_name == "Recipes and ingredients":
    st.header("Recipes and ingredients")
    selected_df = df_all_recipes_skus
    # filter, with download button
    # Filter by "global_name" with string input
    if 'recipe_id' in selected_df.columns:
        # Get unique names
        names = selected_df['recipe_id'].dropna().unique()
        # Add a selectbox to filter by customer
        selected = st.selectbox("Filter by Recipe name", options=["All"] + list(names))
        # Filter the dataset based on the selected customer
        if selected != "All":
            filtered_df = selected_df[selected_df['recipe_id'] == selected]
        else:
            filtered_df = selected_df
        # Display the filtered dataset
        st.write(f"Showing results for: {selected}")
        st.dataframe(filtered_df)
        # Convert the filtered dataset to CSV
        csv = filtered_df.to_csv(index=False)
        # Add a download button to export the dataset as CSV
        st.download_button(
            label="Download Filtered Dataset as CSV",
            data=csv,
            file_name="filtered_dataset.csv",
            mime="text/csv"
        )
    else:
        # Display a message if the 'global_name' column is not found
        st.write("The 'global_name' column is not found in the dataset. Please check the data.")
       
# Display the filtered dataset
#st.dataframe(selected_df)


