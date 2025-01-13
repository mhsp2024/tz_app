# tz_app

### tracezilla_get_data.ipynb & tz_get_data_api.py
collect data from api, with descriptions in .ipynb
This script gets data about recipe, ingredient, price, etc from tracezilla api. 

### tz_app.py 
This script is about the settings of streamlit app.
When I tried to combine code for data collection with this part, it took too long to successfully create the website. So now I only use two datasets as a sample.

In order to solve the problem of low speed, I tried to seperate fetching data in one scipt and import the datasets into another one for creating a website, but it still takes time and needs further build-ups. This attempt is stored in branch tz_app_test. I think we need other plans to speed up data collection and processing, such as moving this part to another platform before putting the result datasets into streamlit. now it runs all over everytime we open the website.

