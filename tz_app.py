import requests
import streamlit as st

# API URL and Token
API_URL = "https://app.tracezilla.com/api/v1/wooden-spoon/orders/sales"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI3IiwianRpIjoiZjY1N2ZiZDk5ZDliZWEyMzdlMWQ3NTZkN2Q4MDViNWNlZDhlZDZhMDhkMTIzYTRlNmQxYTBjYjdjYTZhM2FmM2EyMWY2MTQ3MDUzYTNmMzciLCJpYXQiOjE3MzM5OTcxMzIuNjgyNzI4LCJuYmYiOjE3MzM5OTcxMzIuNjgyNzMsImV4cCI6MTc2ODIxMTUzMi42NzYyMDUsInN1YiI6IjE3MzYiLCJzY29wZXMiOltdfQ.RZOp4aR2WAjd12W1Gw_yma0fPmO9XVmIoHScVN6Qh7DW4lApjdJWjwniFFE4hoV55cBdMj05GgHuwKzh1pk3-aJoKhKKMyC3XAeMJI1W9kRvTDc0Yasmt2oO13BgzBGIg4nAEhKjnp58dXdBQVjM4f6mwWotmAXrpxAJsBKe0xPpDoy9wA6CePXLyAeSWKjr94d-To6noRieEqSz2KVOsF3rKJOwO-fA_7ZxdgEYJ_UBgh5his7SAiU48Kqh_3q5zRp58Eq_1SOO7Cgsm-GK3l6agnEgU5Zv6vlaNRq5IQoAcHXXr-VgIYRaGXLz6EJGqCySUoWoMTjRmsqUjDBaUzQ8n7dUhiGmdXEG4eNQkvAZBnG4ckliqvUgMm3d1chvG2mamirE782Btw0n__JMwYxwbAFl-rbTYffryr55RAn1SCEmCucqr7yUmgJQH4tn5XDHX461a0-Fh0BJik-YcxCaknGt6Ihw1BGn2EDYWmxg0wrTklCK40kv4au5ma94p-lb6sPBS95p4KXZ-Rcf9gqsLZ44KK-XwbWQPsDg7ZIkMg0wxbw86mAdBJL9YOgecHWMRliBefXfLdEatshh5435BHoPkx1q8yqEcm2WPsU93z2TWbhqEIGKQfExNrXOPWPDLlqTcWPQ133x4pb_UvqzBnG37dCQB6mKHIQ2-9Q"  # Replace with your actual API token

# Headers for the API Request
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Fetch Sales Orders from the API
def fetch_sales_orders():
    params = {
        "sortBy": "created_at",
        "sortDirection": "asc",
        "include": "customer_partner",
        "additional": "order_sub_total"
    }
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching sales orders: {e}")
        return None

# Streamlit App
st.title("Tracezilla Sales Orders Viewer")

# Fetch data
sales_orders = fetch_sales_orders()

# Display the data in Streamlit
if sales_orders:
    st.subheader("Sales Orders")
    # Display raw JSON
    st.json(sales_orders)

    # Display as a table if data is a list of dictionaries
    if isinstance(sales_orders, list):
        st.subheader("Sales Orders Table")
        st.write(sales_orders)  # Automatically renders tabular data
else:
    st.error("Failed to fetch sales orders.")
