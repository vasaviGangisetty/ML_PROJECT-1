import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Assuming this import works in your local environment ---
from database.db_operations import get_all_customers

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Enterprise Analytics", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium-looking metric cards
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #4facfe;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATA LOADING & PREPARATION
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = get_all_customers()
    # Ensure churned is easily readable for charts (assuming 0/1 or True/False)
    if 'is_churned' in df.columns and df['is_churned'].dtype in ['int64', 'bool']:
        df['Churn Status'] = df['is_churned'].apply(lambda x: 'Churned' if x else 'Active')
    return df

df_raw = load_data()

# ---------------------------------------------------------
# 3. INTERACTIVE SIDEBAR FILTERS
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942269.png", width=60)
    st.header("⚙️ Global Filters")
    st.write("Drill down into specific customer segments.")

    # Age Filter
    min_age, max_age = int(df_raw['age'].min()), int(df_raw['age'].max())
    age_range = st.slider("Select Age Range:", min_age, max_age, (min_age, max_age))

    # Gender Filter
    genders = df_raw['gender'].unique().tolist()
    selected_genders = st.multiselect("Select Gender:", genders, default=genders)

    # Churn Filter
    churn_status = st.radio("Customer Status:", ["All", "Active", "Churned"])

# ---------------------------------------------------------
# 4. APPLY FILTERS
# ---------------------------------------------------------
df_filtered = df_raw[
    (df_raw['age'] >= age_range[0]) & 
    (df_raw['age'] <= age_range[1]) & 
    (df_raw['gender'].isin(selected_genders))
]

if churn_status != "All":
    df_filtered = df_filtered[df_filtered['Churn Status'] == churn_status]

# ---------------------------------------------------------
# 5. HEADER & DYNAMIC KPIs
# ---------------------------------------------------------
st.title("📈 Enterprise Overview Dashboard")
st.markdown("Monitor real-time customer behavior, revenue metrics, and retention strategies.")

if df_filtered.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your criteria.")
else:
    # Calculate global metrics to show deltas (comparisons)
    global_avg_income = df_raw['income'].mean()
    global_avg_spend = df_raw['spending_score'].mean()
    global_churn = df_raw['is_churned'].mean() * 100

    filtered_churn = df_filtered['is_churned'].mean() * 100

    st.markdown("### 📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("👥 Filtered Customers", f"{len(df_filtered):,}", f"{(len(df_filtered)/len(df_raw))*100:.1f}% of Total")
    col2.metric("💰 Avg Income", f"${df_filtered['income'].mean():,.0f}", f"${df_filtered['income'].mean() - global_avg_income:,.0f} vs Global")
    col3.metric("⭐ Avg Spending Score", f"{df_filtered['spending_score'].mean():.0f}/100", f"{df_filtered['spending_score'].mean() - global_avg_spend:.1f} vs Global")
    
    # Delta color inversion for churn (lower is better)
    col4.metric("⚠️ Segment Churn Rate", f"{filtered_churn:.1f}%", f"{filtered_churn - global_churn:.1f}% vs Global", delta_color="inverse")

    st.markdown("---")

    # ---------------------------------------------------------
    # 6. TABBED INTERACTIVE CHARTS
    # ---------------------------------------------------------
    tab1, tab2, tab3 = st.tabs(["📊 Demographics & Churn", "💸 Revenue & Engagement Clusters", "🔍 Deep Dive Data"])

    # --- TAB 1: Demographics ---
    with tab1:
        colA, colB = st.columns(2)
        with colA:
            # Upgraded Donut Chart
            fig_gender = px.pie(
                df_filtered, names='gender', 
                title="Customer Gender Distribution", 
                hole=0.4, 
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_gender.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='label+percent+value')
            fig_gender.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_gender, use_container_width=True)

        with colB:
            # Stacked Histogram showing Churn overlay on Age
            fig_age = px.histogram(
                df_filtered, x='age', color='Churn Status', nbins=20, 
                title="Age Distribution by Churn Status",
                color_discrete_map={"Active": "#2ecc71", "Churned": "#e74c3c"},
                marginal='box', barmode='stack'
            )
            fig_age.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", legend_title_text='')
            st.plotly_chart(fig_age, use_container_width=True)

    # --- TAB 2: Advanced Visuals ---
    with tab2:
        st.markdown("### 🎯 Value Segmentation")
        st.write("Understand how Income and Spending relate, sized by Total Lifetime Spend.")
        
        # Interactive Bubble Chart
        fig_scatter = px.scatter(
            df_filtered, x='income', y='spending_score', 
            color='Churn Status', size='total_spent', hover_name='customer_id',
            color_discrete_map={"Active": "#3498db", "Churned": "#e74c3c"},
            title="Income vs Spending Score (Bubble Size = Total Spent)",
            labels={"income": "Annual Income ($)", "spending_score": "Spending Score (0-100)"},
            opacity=0.7
        )
        fig_scatter.update_layout(plot_bgcolor="rgba(240,240,240,0.5)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- TAB 3: Data & Heatmap ---
    with tab3:
        colC, colD = st.columns([1, 1.5])
        
        with colC:
            st.markdown("### 🔥 Correlation Heatmap")
            corr_cols = ['age', 'income', 'spending_score', 'purchase_frequency', 'total_spent', 'is_churned']
            
            # Using Plotly Graph Objects for a highly polished heatmap
            corr_matrix = df_filtered[corr_cols].corr()
            fig_corr = px.imshow(
                corr_matrix, 
                text_auto=".2f", 
                color_continuous_scale="RdBu_r", 
                aspect="auto",
                zmin=-1, zmax=1
            )
            fig_corr.update_layout(margin=dict(l=0, r=0, b=0, t=30))
            st.plotly_chart(fig_corr, use_container_width=True)
            
        with colD:
            st.markdown("### 📋 Filtered Raw Data")
            st.write("Export or sort the current active segment.")
            
            # Use Streamlit's powerful interactive dataframe
            display_cols = ['customer_id', 'age', 'gender', 'income', 'spending_score', 'total_spent', 'Churn Status']
            
            st.dataframe(
                df_filtered[display_cols].style.applymap(
                    lambda x: 'background-color: #ffcccc' if x == 'Churned' else 'background-color: #ccffcc', 
                    subset=['Churn Status']
                ), 
                use_container_width=True, 
                height=350
            )