import streamlit as st
import plotly.graph_objects as go
from database.db_operations import get_all_customers
from utils.helpers import load_all_models

st.set_page_config(page_title="E-Commerce Recommendations", layout="wide")

st.title("🛒 Smart E-Commerce Recommendations")
st.write("Find similar customers and recommend products based on their purchasing power and budget, similar to a Flipkart/Amazon search filter.")

# Load data and models
df = get_all_customers()
scaler, le, _, _, knn = load_all_models()

# ---------------------------------------------------------
# 1. FLIPKART-STYLE SEARCH & FILTER UI
# ---------------------------------------------------------
st.markdown("### 🔍 Search & Filter")
col1, col2 = st.columns(2)

with col1:
    cust_id = st.selectbox("1. Select Target Customer ID:", df['customer_id'].tolist())

with col2:
    # Flipkart-style Budget Filter
    max_budget = st.slider("2. Filter Lookalikes by Max Budget ($ Total Spent):", 
                           min_value=int(df['total_spent'].min()), 
                           max_value=int(df['total_spent'].max()), 
                           value=int(df['total_spent'].max()))

# ---------------------------------------------------------
# 2. AI KNN PROCESSING
# ---------------------------------------------------------
if st.button("🚀 Search for Lookalikes & Products", type="primary", use_container_width=True):
    
    # Preprocess Data
    X = df[['age', 'gender', 'income', 'spending_score', 'purchase_frequency', 'total_spent']].copy()
    X['gender_encoded'] = le.transform(X['gender'])
    expected_features = ['age', 'gender_encoded', 'income', 'spending_score', 'purchase_frequency', 'total_spent']
    X_scaled = scaler.transform(X[expected_features])
    
    target_idx = df[df['customer_id'] == cust_id].index[0]
    target_scaled = X_scaled[target_idx].reshape(1, -1)
    
    # Find Top 10 lookalikes to allow for filtering
    distances, indices = knn.kneighbors(target_scaled, n_neighbors=11)
    match_indices = indices[0][1:]
    
    # Get the raw dataframe of matches
    lookalikes_df = df.iloc[match_indices].copy()
    
    # APPLY THE E-COMMERCE BUDGET FILTER
    filtered_lookalikes = lookalikes_df[lookalikes_df['total_spent'] <= max_budget]
    
    if filtered_lookalikes.empty:
        st.warning("No lookalikes found within this budget. Try increasing the budget filter!")
    else:
        st.markdown("---")
        
        # ---------------------------------------------------------
        # 3. DYNAMIC PRODUCT RECOMMENDATION ENGINE
        # ---------------------------------------------------------
        # Calculate average spending score of the filtered lookalikes
        avg_score = filtered_lookalikes['spending_score'].mean()
        
        # Suggest products based on how much the matched customers spend
        if avg_score >= 70:
            tier = "Premium / Luxury"
            products = ["Apple MacBook Pro", "Sony PlayStation 5", "Rolex Submariner", "Samsung 4K OLED TV"]
        elif avg_score >= 40:
            tier = "Mid-Range / Popular"
            products = ["Nike Air Max Sneakers", "Dyson Vacuum", "Apple AirPods Pro", "Kindle Paperwhite"]
        else:
            tier = "Budget / Value"
            products = ["Basic Phone Case", "Cotton T-Shirt 3-Pack", "Desk Organizer", "Water Bottle"]

        st.markdown("### 🛍️ Suggested Products to Pitch")
        st.info(f"**Customer Buying Tier:** {tier} (Based on Lookalike spending behavior)")
        st.success(f"**Top Recommended Products:** {', '.join(products)}")

        # ---------------------------------------------------------
        # 4. TABLES & GRAPHS
        # ---------------------------------------------------------
        st.markdown("### 📋 Filtered Lookalike Customers")
        st.write("These customers match the target profile and fall within your selected budget.")
        display_cols = ['customer_id', 'age', 'gender', 'income', 'spending_score', 'total_spent']
        st.dataframe(filtered_lookalikes[display_cols].style.highlight_max(subset=['spending_score'], color='lightgreen'), use_container_width=True)

        st.markdown("### 📊 Target vs. Top Match Metrics")
        
        # Compare Target against the closest match that passed the budget filter
        best_match_data = filtered_lookalikes.iloc[0]
        target_data = df.iloc[target_idx]

        colA, colB, colC = st.columns(3)
        
        with colA:
            fig_income = go.Figure(data=[
                go.Bar(name='Target', x=['Income ($)'], y=[target_data['income']], marker_color='#2ca02c'),
                go.Bar(name='Best Match', x=['Income ($)'], y=[best_match_data['income']], marker_color='#1f77b4')
            ])
            fig_income.update_layout(barmode='group', margin=dict(t=30, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig_income, use_container_width=True)

        with colB:
            fig_spent = go.Figure(data=[
                go.Bar(name='Target', x=['Total Spent ($)'], y=[target_data['total_spent']], marker_color='#2ca02c'),
                go.Bar(name='Best Match', x=['Total Spent ($)'], y=[best_match_data['total_spent']], marker_color='#1f77b4')
            ])
            fig_spent.update_layout(barmode='group', margin=dict(t=30, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig_spent, use_container_width=True)
            
        with colC:
            fig_score = go.Figure(data=[
                go.Bar(name='Target', x=['Spend Score'], y=[target_data['spending_score']], marker_color='#2ca02c'),
                go.Bar(name='Best Match', x=['Spend Score'], y=[best_match_data['spending_score']], marker_color='#1f77b4')
            ])
            fig_score.update_layout(barmode='group', margin=dict(t=30, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig_score, use_container_width=True)