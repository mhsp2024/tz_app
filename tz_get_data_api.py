import requests
import pandas as pd
import streamlit as st
import os

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



# sku prices
df_purchase = process_data_to_dataframe(fetch_data('https://app.tracezilla.com/api/v1/wooden-spoon/price-lists/purchase'))
price_listid= df_purchase['id']


def fetch_data_(url):
    all_data = []
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            # Ensure 'data' key exists
            if 'data' in data:
                all_data.extend(data['data'])  # Append data part of the response
            else:
                print(f"No 'data' key found on page {page}. Stopping.")
                break
            
            # Check for pagination
            if 'links' in data and data['links'].get('next'):
                page += 1
            else:
                break
        else:
            print(f"Error fetching data from {url}: {response.status_code}")
            break
    return all_data

# Collect all data parts
all_data_parts = []

for i in price_listid:
    url = f'https://app.tracezilla.com/api/v1/wooden-spoon/price-lists/purchase/{i}/prices'
#    print(f"Fetching data for Price List ID: {i}")
    
    try:
        data_part = fetch_data_(url)  # Fetch the "data" part
        all_data_parts.extend(data_part)  # Combine all data into a single list
    except Exception as e:
        print(f"Failed to fetch data for Price List ID {i}: {e}")

# Convert the combined data into a DataFrame
df_sku_prices = pd.DataFrame(all_data_parts)



# production orders
# production order id
df_pro_orders = process_data_to_dataframe(fetch_data('https://app.tracezilla.com/api/v1/wooden-spoon/orders/production'))
production_order_id = df_pro_orders['id']

def fetch_production_orders(base_url, api_token):
    all_orders = []  # To store all order data
    next_url = base_url
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    while next_url:
        response = requests.get(next_url, headers=headers)
        try:
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()  # Attempt to parse JSON
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response Text: {response.text}")
            break
        except ValueError as json_err:
            print(f"JSON parse error: {json_err}")
            print(f"Raw response: {response.text}")
            break

        # Append data from the current page
        all_orders.extend(data.get('data', []))

        # Move to the next page
        next_url = data.get('links', {}).get('next')

    return all_orders

# Base URL for the first page
base_url = "https://app.tracezilla.com/api/v1/wooden-spoon/orders/production?type%5Beq%5D=production&sortBy=created_at&sortDirection=asc&perPage=25&additional=budgets%2Corder_sub_total"

orders = fetch_production_orders(base_url,API_TOKEN)

df_orders = pd.json_normalize(orders)

# order inbounds

# Initialize lists
all_data_parts = []  # To store all successful data
failed_ids = []  # List to store IDs that failed
timeout_ids = []  # List to store IDs that failed due to timeout

# Main loop to fetch data for production orders
for i in production_order_id:
    url = f'https://app.tracezilla.com/api/v1/wooden-spoon/orders/production/{i}/inbound/lots?include=lot,sku,sku.files_count,sku.comments_count,lot.attribute_values,lot.traces,lot.dates,lot.traces_brought_forward,lot.traces_brought_forward.origin_lot,line_number&additional=lot_restrictions'
    try:
        data_part = fetch_data_(url)  # Fetch the "data" part
        all_data_parts.extend(data_part)  # Combine all data into a single list
    except requests.exceptions.Timeout:
        print(f"Timeout for Production Order ID {i}")
        timeout_ids.append(i)  # Collect IDs with timeout errors
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data for Production Order ID {i}: {e}")
        failed_ids.append(i)  # Collect other errors
        # Debugging: Check raw response
        try:
            response = requests.get(url, timeout=30)
        except Exception as debug_e:
            print(f"Could not fetch raw response for {i}: {debug_e}")

# Combine all data into a single DataFrame
df_order_inbounds_add = pd.DataFrame(all_data_parts)

print("Data fetching complete.")
print(f"Total records fetched: {len(df_order_inbounds_add)}")
print(f"Failed IDs: {len(failed_ids)}")
print(f"Timeout IDs: {len(timeout_ids)}")

processed_data = []

# Iterate through each row of the DataFrame
for _, row in df_order_inbounds_add.iterrows():
    sku = row['sku']  # Nested SKU details
    lot = row['lot']  # Nested lot details
    inbound_order_lot = lot.get('inbound_order_lot', {})  # Nested inbound_order_lot details
    order = inbound_order_lot.get('order', {})  # Nested order details within inbound_order_lot
    
    # Extract relevant fields
    processed_data.append({
        # Order Details
        "order_id": order.get('id'),
        "order_date": order.get('order_date'),
        "delivery_date": order.get('delivery_date'),
        "currency": order.get('currency'),
        
        # SKU Details
        "sku_id": sku.get('id'),
        "sku_code": sku.get('sku_code'),
        "global_name": sku.get('global_name'),
        "unit_of_measure": sku.get('unit_of_measure'),
        
        # Lot Details
        "lot_number_complete": lot.get('lot_number_complete'),
        "quantity_available": lot.get('quantity_available'),
        "unit": lot.get('unit'),
        "uom_conversion": lot.get('uom_conversion'),
        
        # Price Details
        "unit_price": inbound_order_lot.get('unit_price'),
        "line_price": inbound_order_lot.get('line_price'),
        "total_price": inbound_order_lot.get('total_price'),
    })

# Create a DataFrame
df_prices = pd.DataFrame(processed_data)


# order invoices

invoices = process_data_to_dataframe(fetch_data('https://app.tracezilla.com/api/v1/wooden-spoon/invoices'))

invoice_id = invoices['id']
data_part =[]
all_data_parts= []

for i in invoice_id:
    url = f'https://app.tracezilla.com/api/v1/wooden-spoon/invoices/{i}/lines-extract'
    try:
        data_part = fetch_data_(url)  # Fetch the "data" part
        all_data_parts.extend(data_part)  # Combine all data into a single list
    except Exception as e:
        print(f"Failed to fetch data for Price List ID {i}: {e}")

# Convert the combined data into a DataFrame
df_invoice = pd.DataFrame(all_data_parts)

df_invoice = df_invoice[df_invoice['category']=='sales_price']

df_invoice_com = df_invoice.merge(
    df_prices[['sku_id', 'sku_code', 'global_name']],
    on='sku_id',
    how='left')

df_prices_sku = df_invoice_com[[
    'order_id',
    'delivery_date',
    'sku_id',
    'sku_code',
    'global_name',
    'unit_price',
    'uom_conversion',
    'uoms_per_price_unit',
    'calculation',
    'quantity',
    'quantity_parcels',
    'base_unit',
    'quantity_uom'
]].rename(columns={'order_type_y': 'order_type'})

df_prices_sku = df_prices_sku.drop_duplicates()
df_prices_sku['price_uom'] = df_prices_sku['unit_price'] / df_prices_sku['uom_conversion']

