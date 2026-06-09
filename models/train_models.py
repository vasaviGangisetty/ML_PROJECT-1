import pandas as pd
import joblib
import os
import sqlite3
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors

os.makedirs('saved_models', exist_ok=True)

conn = sqlite3.connect("database/customer_analytics.db")
df = pd.read_sql_query("SELECT * FROM customers", conn)
conn.close()

le = LabelEncoder()
df['gender_encoded'] = le.fit_transform(df['gender'])

# Notice we DO NOT train on 'favorite_product', we only use it for business logic later
features = ['age', 'gender_encoded', 'income', 'spending_score', 'purchase_frequency', 'total_spent']
X = df[features]
y = df['is_churned']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, 'saved_models/scaler.pkl')
joblib.dump(le, 'saved_models/label_encoder.pkl')

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10).fit(X_scaled)
joblib.dump(kmeans, 'saved_models/segment_model.pkl')

rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_scaled, y)
joblib.dump(rf, 'saved_models/churn_model.pkl')

knn = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(X_scaled)
joblib.dump(knn, 'saved_models/knn_model.pkl')

print("✅ All Models Trained and Saved!")