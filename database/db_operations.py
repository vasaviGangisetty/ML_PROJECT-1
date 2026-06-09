import sqlite3
import pandas as pd

# I have REMOVED @st.cache_data here so Streamlit is FORCED 
# to read the live database and find the new 'favorite_product' column!
def get_all_customers():
    conn = sqlite3.connect("database/customer_analytics.db")
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    return df