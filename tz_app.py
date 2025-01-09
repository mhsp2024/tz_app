import requests
import pandas as pd
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath('/path/to/tz_get_data_api'))


### import datasets :
from tz_get_data_api import df_recipes
# df_sku_merged, df_all_recipes_skus, df_order_inbounds_add, df_invoice_com, df_prices_sku, df_sku_prices

# recipes :df_recipes
# sku :df_sku_merged
# recipe and ingredients(sku) : df_all_recipes_skus
# production order inbounds : df_order_inbounds_add
# invoices : df_invoice_com
# sku prices : df_prices_sku
# latest sku prices : df_sku_prices

# Streamlit App
st.title("Tracezilla Data Viewer")

# Add filter for customer partner or any field (example for filtering 'name')
if 'name' in df_recipes.columns:
    # Get unique customer names
    customers = df_recipes['name'].dropna().unique()

    # Add a selectbox to filter by customer
    selected_customer = st.selectbox("Filter by Customer", options=["All"] + list(customers))

    # Filter the dataset based on the selected customer
    if selected_customer != "All":
        filtered_df = df_recipes[df_recipes['name'] == selected_customer]
    else:
        filtered_df = df_recipes

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

