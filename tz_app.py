def fetch_data(url):
    all_data = []
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}", headers=headers)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Check if the content is in JSON format
            try:
                data = response.json()  # Attempt to parse as JSON
                all_data.extend(data['data'])
                
                # Check if there is a next page
                next_page = data['links'].get('next')
                if next_page:
                    page += 1
                else:
                    break
            except ValueError:
                # Handle case where response is not JSON
                st.error(f"Error: Response from {url} is not in valid JSON format.")
                st.write("Response content:")
                st.text(response.text)  # Display raw response content for debugging
                break
        else:
            st.error(f"Error fetching data from {url}: {response.status_code}")
            st.write("Response content:")
            st.text(response.text)  # Display raw response content for debugging
            break
    return all_data
