import sqlite3
import pandas as pd
import os

os.makedirs('database', exist_ok=True)
db_path = "database/customer_analytics.db"

def setup_db():
    # 1. DELETE THE OLD DB TO FORCE THE NEW COLUMNS
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Old database deleted.")

    # 2. CREATE FRESH DB
    conn = sqlite3.connect(db_path)
    
    # 3. PUSH CSV TO DB
    df = pd.read_csv('dataset/customer_data.csv')
    df.to_sql('customers', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
    print("✅ New database built successfully with 'favorite_product'!")

if __name__ == "__main__":
    setup_db()