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

# the above part needs to be fixed, now we use sample datasets 
# to build up the website first
import pandas as pd
import streamlit as st

# Generate two example datasets

# Dataset: df_recipes
df_recipes = pd.DataFrame({
    "id": [1, 2, 3],
    "number": [101, 102, 103],
    "name": ["Recipe A", "Recipe B", "Recipe C"],
    "ref": ["REF001", "REF002", "REF003"],
    "description": ["Description A", "Description B", "Description C"],
    "reference_consume_id": [None, 1, 2],
    "preferred_interval": [30, 45, 60],
    "master_resource_id": [None, 101, 102],
    "replacement_id": [None, None, 1],
    "replaced_from": [None, None, None],
    "units_per_hour": [50, 60, 70],
    "fixed_minutes": [15, 10, 20],
    "active": [True, True, False],
    "created_at": ["2023-01-01", "2023-01-02", "2023-01-03"],
    "updated_at": ["2023-02-01", "2023-02-02", "2023-02-03"]
})

# Dataset: df_prices_sku
df_prices_sku = pd.DataFrame({
    "order_id": [1, 2, 3],
    "delivery_date": ["2023-03-01", "2023-03-02", "2023-03-03"],
    "sku_id": [501, 502, 503],
    "sku_code": ["SKU001", "SKU002", "SKU003"],
    "global_name": ["Name1", "Name2", "Name3"],
    "unit_price": [15.0, 20.0, 18.0],
    "uom_conversion": [1, 1, 1],
    "uoms_per_price_unit": [10, 20, 15],
    "calculation": ["calc1", "calc2", "calc3"],
    "quantity": [100, 200, 150],
    "quantity_parcels": [10, 20, 15],
    "base_unit": ["kg", "kg", "kg"],
    "quantity_uom": ["kg", "kg", "kg"],
    "price_uom": ["USD", "USD", "USD"]
})

#####################################

# Streamlit App
st.title("Tracezilla Data Viewer")

# Sidebar to select dataset
dataset_name = st.sidebar.selectbox(
    "Select a Dataset",
    options=["recipes", "sku prices"]
)

# Display the selected dataset
if dataset_name == "recipes":
    st.header("Recipes Dataset")
    selected_df = df_recipes
    # filter, with download button
    if 'name' in selected_df.columns:
        # Get unique customer names
        customers = selected_df['name'].dropna().unique()
        # Add a selectbox to filter by customer
        selected_customer = st.selectbox("Filter by Customer", options=["All"] + list(customers))
        # Filter the dataset based on the selected customer
        if selected_customer != "All":
            filtered_df = selected_df[selected_df['name'] == selected_customer]
        else:
            filtered_df = selected_df
        # Display the filtered dataset
        st.write(f"Showing results for: {selected_customer}")
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

elif dataset_name == "sku prices":
    st.header("Prices SKU Dataset")
    selected_df = df_prices_sku
    # filter, with download button
    # Filter by "global_name" with string input
    if 'global_name' in selected_df.columns:
        # Add a text input box for filtering by global_name
        filter_string = st.text_input("Filter by Global Name", "")

        # Filter the dataset based on the input string
        if filter_string:
            filtered_df = selected_df[selected_df['global_name'].str.contains(filter_string, case=False, na=False)]
        else:
            filtered_df = selected_df

        # Display the filtered dataset
        st.write(f"Showing results for global_name containing: '{filter_string}'")
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
st.dataframe(selected_df)

