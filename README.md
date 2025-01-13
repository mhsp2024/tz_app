# tz_app

### tracezilla_get_data.ipynb & tz_get_data_api.py
collect data from api, with descriptions in .ipynb
This script gets data about recipe, ingredient, price, etc from tracezilla api. 

### tz_app.py 
This script is about the settings of streamlit app.
When I tried to combine code for data collection with this part, it took too long to successfully create the website. So now I only use two datasets as a sample. if you want to test the app with everything, just copy all the code in tz_get_data_api.py and put them in tz_app.py before the part for streamlit app.

In order to solve the problem of low speed, I tried to seperate fetching data in one scipt and import the datasets into another one for creating a streamlit app, but it still takes a lot of time and doesn't work well. This attempt is stored in branch tz_app_test. I think we need other plans to speed up data collection and processing, such as moving this part to another platform, or applying effective data processing tools before putting the result datasets into streamlit. now it runs all over everytime we refresh the website.

Possible solution: store data into sql database and update on a regular basis. Extract datasets from database for generating streamlit website. This way we don't need to run the entire data collection part.
