import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- Assuming these imports work in your local environment ---
from database.db_operations import get_all_customers
from utils.helpers import load_all_models

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI E-Commerce Recommender", 
    page_icon="🛒", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better looking metric cards
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MOCK PRODUCT DATABASE (Simulating a real catalog)
# ---------------------------------------------------------
@st.cache_data
def get_product_catalog():
    return pd.DataFrame([
        {"id": "P01", "name": "Apple MacBook Pro 16\"", "category": "Electronics", "price": 2499, "tier": "Premium", "rating": 4.9, "img": "💻"},
        {"id": "P02", "name": "Sony PlayStation 5", "category": "Gaming", "price": 499, "tier": "Premium", "rating": 4.8, "img": "🎮"},
        {"id": "P03", "name": "Rolex Submariner Watch", "category": "Accessories", "price": 8500, "tier": "Premium", "rating": 4.9, "img": "⌚"},
        {"id": "P04", "name": "Samsung 4K OLED TV", "category": "Electronics", "price": 1200, "tier": "Premium", "rating": 4.7, "img": "📺"},
        {"id": "P05", "name": "Nike Air Max Sneakers", "category": "Fashion", "price": 150, "tier": "Mid-Range", "rating": 4.5, "img": "👟"},
        {"id": "P06", "name": "Dyson V11 Vacuum", "category": "Home", "price": 400, "tier": "Mid-Range", "rating": 4.6, "img": "🧹"},
        {"id": "P07", "name": "Apple AirPods Pro", "category": "Electronics", "price": 249, "tier": "Mid-Range", "rating": 4.8, "img": "🎧"},
        {"id": "P08", "name": "Kindle Paperwhite", "category": "Electronics", "price": 130, "tier": "Mid-Range", "rating": 4.7, "img": "📱"},
        {"id": "P09", "name": "Basic Phone Case", "category": "Accessories", "price": 15, "tier": "Value", "rating": 4.2, "img": "📱"},
        {"id": "P10", "name": "Cotton T-Shirt 3-Pack", "category": "Fashion", "price": 25, "tier": "Value", "rating": 4.3, "img": "👕"},
        {"id": "P11", "name": "Mesh Desk Organizer", "category": "Office", "price": 20, "tier": "Value", "rating": 4.1, "img": "🗂️"},
        {"id": "P12", "name": "Insulated Water Bottle", "category": "Accessories", "price": 18, "tier": "Value", "rating": 4.6, "img": "💧"},
    ])

# Load data and models
df = get_all_customers()
scaler, le, _, _, knn = load_all_models()
catalog_df = get_product_catalog()

# ---------------------------------------------------------
# SIDEBAR: SEARCH & FILTER UI
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3144/3144456.png", width=60)
    st.header("Search Parameters")
    
    cust_id = st.selectbox("🎯 Target Customer ID:", df['customer_id'].tolist())
    
    st.divider()
    st.subheader("🛒 Product Filters")
    st.write("Set the budget constraints for recommendations:")
    
    max_product_price = st.slider(
        "Max Product Price ($):", 
        min_value=10, 
        max_value=10000, 
        value=3000, 
        step=50
    )
    
    st.divider()
    st.subheader("👥 Lookalike Filters")
    min_match = st.slider("Minimum Match Confidence (%)", 50, 100, 75)

# ---------------------------------------------------------
# MAIN DASHBOARD HEADER
# ---------------------------------------------------------
st.title("🛍️ Smart E-Commerce Recommender")
st.markdown("Leverage AI to find Lookalike Audiences and surface highly relevant products based on purchasing power.")

# ---------------------------------------------------------
# TARGET CUSTOMER PROFILE (KPIs)
# ---------------------------------------------------------
target_idx = df[df['customer_id'] == cust_id].index[0]
target_data = df.iloc[target_idx]

st.subheader(f"Customer Profile: `{cust_id}`")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Age & Gender", f"{target_data['age']} yrs, {target_data['gender']}")
col2.metric("Annual Income", f"${target_data['income']:,.0f}")
col3.metric("Spending Score", f"{target_data['spending_score']}/100")
col4.metric("Lifetime Value (Total Spent)", f"${target_data['total_spent']:,.2f}")

st.divider()

# ---------------------------------------------------------
# AI KNN PROCESSING
# ---------------------------------------------------------
with st.spinner("Analyzing millions of data points to find lookalikes..."):
    # Preprocess Data safely
    X = df[['age', 'gender', 'income', 'spending_score', 'purchase_frequency', 'total_spent']].copy()
    X['gender_encoded'] = le.transform(X['gender'])
    expected_features = ['age', 'gender_encoded', 'income', 'spending_score', 'purchase_frequency', 'total_spent']
    X_scaled = scaler.transform(X[expected_features])
    
    target_scaled = X_scaled[target_idx].reshape(1, -1)
    
    # Find Top 20 lookalikes to allow for filtering
    distances, indices = knn.kneighbors(target_scaled, n_neighbors=21)
    match_indices = indices[0][1:]
    match_distances = distances[0][1:]
    
    # Convert distances to a pseudo "Match Percentage" (Realistic UI feature)
    # Lower distance = Higher Match %. Assuming scaled data distances generally fall between 0 and 5.
    match_percentages = np.clip(100 - (match_distances * 15), 0, 100).round(1)
    
    # Build Lookalikes DataFrame
    lookalikes_df = df.iloc[match_indices].copy()
    lookalikes_df['match_confidence'] = match_percentages
    
    # Filter by user-defined confidence
    filtered_lookalikes = lookalikes_df[lookalikes_df['match_confidence'] >= min_match]

if filtered_lookalikes.empty:
    st.warning("⚠️ No lookalikes found meeting the minimum match confidence. Try lowering the threshold in the sidebar.")
else:
    # ---------------------------------------------------------
    # TABS FOR CLEANER UI
    # ---------------------------------------------------------
    tab1, tab2, tab3 = st.tabs(["🎁 AI Product Recommendations", "👥 Lookalike Audience Insights", "📊 Data Analysis"])
    
    # ---------------------------------------------------------
    # TAB 1: DYNAMIC PRODUCT RECOMMENDATION ENGINE
    # ---------------------------------------------------------
    with tab1:
        avg_score = filtered_lookalikes['spending_score'].mean()
        avg_income = filtered_lookalikes['income'].mean()
        
        # Determine Purchasing Tier
        if avg_score >= 70 and avg_income > 60000:
            tier = "Premium"
            color = "gold"
        elif avg_score >= 40:
            tier = "Mid-Range"
            color = "silver"
        else:
            tier = "Value"
            color = "#cd7f32" # Bronze
            
        st.markdown(f"### Target Buying Tier: **<span style='color:{color}'>{tier}</span>**", unsafe_allow_html=True)
        st.caption(f"Based on a lookalike average spending score of {avg_score:.1f} and income of ${avg_income:,.0f}.")
        
        # Filter product catalog by Tier AND Sidebar Price Budget
        recommended_products = catalog_df[
            (catalog_df['tier'] == tier) & 
            (catalog_df['price'] <= max_product_price)
        ].sort_values(by='rating', ascending=False)
        
        if recommended_products.empty:
            st.info("No products match this tier within the selected price budget. Try increasing the Max Product Price.")
        else:
            st.write("#### ✨ Top Picks For This Customer:")
            # Display products as e-commerce "cards" using columns
            cols = st.columns(min(len(recommended_products), 4))
            for i, (_, row) in enumerate(recommended_products.head(4).iterrows()):
                with cols[i]:
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; padding:15px; border-radius:10px; text-align:center; background-color:white; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                        <h1 style="font-size:3rem; margin:0;">{row['img']}</h1>
                        <h5 style="margin-top:10px; color:#333; font-size:16px;">{row['name']}</h5>
                        <p style="color:#888; margin-bottom:5px;">{row['category']}</p>
                        <h4 style="color:#2ca02c; margin:0;">${row['price']}</h4>
                        <p style="font-size:12px; margin-top:5px;">{'⭐' * int(row['rating'])} {row['rating']}/5.0</p>
                    </div>
                    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TAB 2: LOOKALIKE AUDIENCE
    # ---------------------------------------------------------
    with tab2:
        st.markdown("### 📋 Similar Customers Database")
        st.write("These customers show similar purchasing behaviors and demographics.")
        
        display_cols = ['customer_id', 'match_confidence', 'age', 'gender', 'income', 'spending_score', 'total_spent']
        
        # Format the dataframe to look like a real reporting tool
        styled_df = filtered_lookalikes[display_cols].style\
            .format({"match_confidence": "{:.1f}%", "income": "${:,.0f}", "total_spent": "${:,.2f}"})\
            .background_gradient(subset=['match_confidence'], cmap='Greens')
            
        st.dataframe(styled_df, use_container_width=True, height=300)

    # ---------------------------------------------------------
    # TAB 3: ANALYTICS & GRAPHS
    # ---------------------------------------------------------
    with tab3:
        best_match_data = filtered_lookalikes.iloc[0]
        
        st.markdown("### 📊 Target vs. Best Match Comparison")
        
        colA, colB = st.columns([1.5, 2])
        
        with colA:
            # Replaced 3 separate bar charts with one unified Grouped Bar Chart
            features = ['Income ($)', 'Total Spent ($)', 'Spend Score (x100)']
            
            # Multiply spend score by 100 purely so it's visible on the same axis as dollars
            target_vals = [target_data['income'], target_data['total_spent'], target_data['spending_score']*100]
            best_match_vals = [best_match_data['income'], best_match_data['total_spent'], best_match_data['spending_score']*100]
            
            fig_compare = go.Figure(data=[
                go.Bar(name='Target Customer', x=features, y=target_vals, marker_color='#1f77b4'),
                go.Bar(name='Best Match Customer', x=features, y=best_match_vals, marker_color='#ff7f0e')
            ])
            fig_compare.update_layout(
                barmode='group', 
                margin=dict(t=30, b=0, l=0, r=0), 
                height=350,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_compare, use_container_width=True)
            
        with colB:
            # E-commerce Scatter Plot (Income vs Spending Score) showing clusters
            # We plot the whole dataset, highlight the target, and highlight lookalikes
            df['Type'] = 'Other Customers'
            df.loc[filtered_lookalikes.index, 'Type'] = 'Lookalikes'
            df.loc[target_idx, 'Type'] = 'Target Customer'
            
            # Sort so Target is drawn last (on top)
            df_plot = df.sort_values(by='Type')
            
            color_map = {'Other Customers': 'lightgrey', 'Lookalikes': '#2ca02c', 'Target Customer': '#d62728'}
            
            fig_scatter = px.scatter(
                df_plot, x='income', y='spending_score', color='Type',
                color_discrete_map=color_map,
                hover_data=['customer_id'],
                title="Customer Clustering: Income vs. Spending Score"
            )
            
            # Make the target customer dot much larger
            fig_scatter.update_traces(marker=dict(size=8), selector=dict(name='Other Customers'))
            fig_scatter.update_traces(marker=dict(size=12, symbol='star'), selector=dict(name='Lookalikes'))
            fig_scatter.update_traces(marker=dict(size=18, symbol='star', line=dict(width=2, color='black')), selector=dict(name='Target Customer'))
            
            fig_scatter.update_layout(margin=dict(t=40, b=0, l=0, r=0), height=350)
            st.plotly_chart(fig_scatter, use_container_width=True)