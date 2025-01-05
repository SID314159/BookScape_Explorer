# BookScape_Explorer
This project collects books data using Google Books API and gives cool Data analyses through Streamlit  
The sourcecode.py contains the entire python code

# What's Inside:
This project is split into 3 main functions + 1 streamlit section :
## 1. datclt() - Collects the books data using google books API
FEATURES:   
Editable list to add keywords anytime   
Easy control to set book count limit    
Prevents re-adding if a user passes existing keyword in streamlit   
Data transformation, cleaning and conversion to a neat pandas DataFrame   
Removes duplicates from the API returns

## 2. sql_upload() - Writes the transformed data (Pandas Dataframe) into a SQL database
FEATURES:     
Exception handling for sqlalchemy and pymysql to debug easily

## 3. dbcall() - Collects query from Streamlit Section and Retrives data from the SQL database     
FEATURES:    
Exception handling for pymysql to debug easily

## Streamlit Section - Enables user interaction with the backend through a web hosted UI containing 3 pages   
FEATURES:    
Users can initiate data collection for preset keywords on Page 1     
Users can get cool insights using preset analyses on Page2    
Users can pass their own keyword to collect additional related data       
Ability to easily add an additional analysis and its SQL query in the backend as it is defined as a dictionary     
Easy to perform or add operations over the data returned by dbcall() to display in Streamlit     


