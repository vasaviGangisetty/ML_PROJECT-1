import pandas as pd
import numpy as np
import os

os.makedirs('dataset', exist_ok=True)

np.random.seed(42)
n_customers = 1000

data = {
    'customer_id': range(1, n_customers + 1),
    'age': np.random.randint(18, 70, n_customers),
    'gender': np.random.choice(['Male', 'Female'], n_customers),
    'income': np.random.randint(30000, 150000, n_customers),
    'spending_score': np.random.randint(1, 100, n_customers),
    'purchase_frequency': np.random.randint(1, 50, n_customers),
    'total_spent': np.round(np.random.uniform(100, 5000, n_customers), 2),
}
df = pd.DataFrame(data)

# Logic for Churn (High risk if low frequency & low spending)
df['is_churned'] = np.where((df['purchase_frequency'] < 10) & (df['spending_score'] < 30), 1, 0)
# Add slight randomness
df['is_churned'] = np.where(np.random.rand(n_customers) < 0.1, np.random.choice([0, 1]), df['is_churned'])

df.to_csv('dataset/customer_data.csv', index=False)
print("✅ dataset/customer_data.csv generated!")