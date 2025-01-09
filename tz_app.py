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

# Add filter for customer partner or any field (example for filtering 'customer_partner.name')
if 'name' in df_recipes.columns:
    customers = df_recipes['name'].dropna().unique()
    selected_customer = st.selectbox(f"Filter by Customer for {url}", options=["All"] + list(customers))

    if selected_customer != "All":
        filtered_df = df_recipes[df_recipes['name'] == selected_customer]
    else:
        filtered_df = df_recipes
    st.write(f"Showing results for: {selected_customer}")
    st.dataframe(filtered_df)

    # Export to CSV option
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label=f"Download CSV for {url}",
        data=csv,
        file_name=f"{url.split('/')[-1]}_data.csv",
        mime="text/csv")
else:
    st.write("No customer partner name column found for filtering.")
