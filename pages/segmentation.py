import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

# --- Assuming these imports match your actual backend ---
from database.db_operations import get_all_customers
from utils.helpers import load_all_models

# ---------------------------------------------------------
# 1. PAGE CONFIG & PREMIUM CSS
# ---------------------------------------------------------
st.set_page_config(page_title="AI Segmentation Studio", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* Glowing Title */
    .glow-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #b224ef 0%, #7579ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    /* Glassmorphism KPI Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s ease, border-color 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: #7579ff;
    }
    .card-title {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .card-value {
        font-size: 2rem;
        font-weight: bold;
        color: #f8fafc;
        margin: 10px 0;
    }
    
    /* Custom UI Badges */
    .cluster-badge {
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATA LOADING & AI PROCESSING
# ---------------------------------------------------------
df = get_all_customers()
scaler, le, kmeans, _, _ = load_all_models()

with st.spinner("Aligning K-Means Centroids..."):
    time.sleep(0.5) # Simulate processing for UI feel

# AI Processing safely
X = df[['age', 'gender', 'income', 'spending_score', 'purchase_frequency', 'total_spent']].copy()
X['gender_encoded'] = le.transform(X['gender'])
expected_features = ['age', 'gender_encoded', 'income', 'spending_score', 'purchase_frequency', 'total_spent']
X_scaled = scaler.transform(X[expected_features])

df['Cluster'] = kmeans.predict(X_scaled).astype(str)

# Map clusters to business-friendly names with Emojis
cluster_map = {
    '0': '🥉 Budget Buyers', 
    '1': '👑 High Rollers', 
    '2': '💖 Loyalists', 
    '3': '🚶 Occasional'
}
df['Cluster Name'] = df['Cluster'].map(cluster_map).fillna("Other")

# ---------------------------------------------------------
# 3. HEADER & KPI DASHBOARD
# ---------------------------------------------------------
st.markdown('<div class="glow-title">🎯 AI Audience Segmentation</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; margin-bottom: 30px;'>K-Means Clustering dynamically grouping your customers across 6 dimensions into actionable personas.</p>", unsafe_allow_html=True)

# Calculate dynamic cluster metrics
total_cust = len(df)
top_cluster = df['Cluster Name'].mode()[0]
avg_spent = df['total_spent'].mean()
high_rollers_count = len(df[df['Cluster Name'] == '👑 High Rollers'])

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'<div class="glass-card"><div class="card-title">Total Base Formatted</div><div class="card-value">{total_cust:,}</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="glass-card"><div class="card-title">Largest Segment</div><div class="card-value" style="font-size: 1.5rem;">{top_cluster}</div></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="glass-card"><div class="card-title">Global Avg LTV</div><div class="card-value">${avg_spent:,.0f}</div></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="glass-card" style="border-top: 3px solid gold;"><div class="card-title">VIP Accounts Identified</div><div class="card-value" style="color: gold;">{high_rollers_count}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. VISUALIZATIONS: 3D MAP & DONUT CHART
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["🌌 3D Universe Map", "📊 Segment Breakdown"])

color_sequence = ['#00E5FF', '#FF007F', '#B300FF', '#00FF66']

with tab1:
    st.markdown("### 🌐 The Customer Galaxy")
    st.write("Drag to rotate and scroll to zoom. The size of the sphere represents their purchase frequency.")
    
    # Advanced 3D Scatter Plot
    fig_3d = px.scatter_3d(
        df, x='age', y='income', z='spending_score', 
        color='Cluster Name', size='purchase_frequency', 
        hover_name='customer_id',
        color_discrete_sequence=color_sequence,
        opacity=0.85
    )
    fig_3d.update_layout(
        scene=dict(
            xaxis=dict(title='Age', backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title='Income ($)', backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(title='Spend Score', backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, b=0, t=0),
        height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="white"))
    )
    st.plotly_chart(fig_3d, use_container_width=True)

with tab2:
    colA, colB = st.columns([1, 1.2])
    
    with colA:
        st.markdown("#### Audience Distribution")
        # Donut Chart for Segment Sizes
        fig_donut = px.pie(
            df, names='Cluster Name', 
            hole=0.5, 
            color_discrete_sequence=color_sequence
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='label+value')
        fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, height=400)
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with colB:
        st.markdown("#### Segment Profiles & Strategy")
        st.info("**👑 High Rollers**: High income, high spenders. *Strategy: Exclusive early access & premium upselling.*")
        st.success("**💖 Loyalists**: High frequency, average spend. *Strategy: Reward points & subscription boxes.*")
        st.warning("**🥉 Budget Buyers**: Low income, price-sensitive. *Strategy: Flash sales, discount codes, bundles.*")
        st.error("**🚶 Occasional**: Low frequency, low spend. *Strategy: Re-engagement drip campaigns.*")

st.markdown("---")

# ---------------------------------------------------------
# 5. INTERACTIVE DATABASE TABLE
# ---------------------------------------------------------
st.markdown("### 📋 AI Segment Directory")
st.write("Browse and export the assigned clusters for your marketing team.")

col_filter, _ = st.columns([1, 2])
with col_filter:
    # Interactive filtering!
    selected_segment = st.selectbox("🔍 Filter by Segment:", ["View All"] + list(cluster_map.values()))

# Filter Logic
if selected_segment != "View All":
    filtered_df = df[df['Cluster Name'] == selected_segment]
else:
    filtered_df = df

columns_to_display = ['customer_id', 'Cluster Name', 'age', 'gender', 'income', 'spending_score', 'total_spent']

# Gorgeous Dataframe Styling
styled_df = filtered_df[columns_to_display].style\
    .format({"income": "${:,.0f}", "total_spent": "${:,.2f}"})\
    .applymap(lambda x: f"background-color: rgba(255, 0, 127, 0.1); color: #FF007F" if 'High Rollers' in str(x) else '', subset=['Cluster Name'])\
    .applymap(lambda x: f"background-color: rgba(0, 229, 255, 0.1); color: #00E5FF" if 'Budget' in str(x) else '', subset=['Cluster Name'])\
    .applymap(lambda x: f"background-color: rgba(0, 255, 102, 0.1); color: #00FF66" if 'Loyalists' in str(x) else '', subset=['Cluster Name'])

st.dataframe(styled_df, use_container_width=True, height=400)