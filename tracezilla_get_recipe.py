### recipes
# df_recipes

### sku
# df_sku_merged

import requests
import pandas as pd
import streamlit as st
import os

API_TOKEN = st.secrets["API_TOKEN"]

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




df_recipes = process_data_to_dataframe(fetch_data('https://app.tracezilla.com/api/v1/wooden-spoon/recipes'))


df_skus = process_data_to_dataframe(fetch_data('https://app.tracezilla.com/api/v1/wooden-spoon/skus'))

# Merge df_skus with selected columns from df_recipes
df_sku_merged = pd.merge(
    df_skus, 
    df_recipes[['id', 'number', 'name', 'ref', 'description','active']],  # Include relevant columns
    left_on='auto_recipe_id', 
    right_on='id',
    how='left',
    suffixes=('', '_recipe')  # Avoid column name conflicts
)

# Drop the duplicate 'id' column created after the merge (from df_recipes)
df_sku_merged = df_sku_merged.drop(columns=['id_recipe'])
# Rename 'id' column to 'sku_id'
df_sku_merged = df_sku_merged.rename(columns={'id': 'sku_id'})
df_sku_merged = df_sku_merged.rename(columns={'name': 'recipe_name'})


