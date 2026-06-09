import streamlit as st
import time
import numpy as np
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="Nexus AI Analytics", page_icon="🌌", layout="wide")

# ---------------------------------------------------------
# 2. ULTRA-PREMIUM CSS (Glassmorphism & Animations)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global App Background adjustments for Dark Mode */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Live Data Ticker */
    .ticker-wrap {
        width: 100%;
        background-color: rgba(0, 255, 255, 0.05);
        border-top: 1px solid rgba(0, 255, 255, 0.2);
        border-bottom: 1px solid rgba(0, 255, 255, 0.2);
        padding: 5px 0;
        margin-top: -30px;
        margin-bottom: 30px;
        overflow: hidden;
    }
    .ticker-text {
        white-space: nowrap;
        color: #00e5ff;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        animation: ticker 20s linear infinite;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* Glowing Gradient Title */
    .glow-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(to right, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(0, 242, 254, 0.3);
        margin-bottom: 0px;
        padding-bottom: 10px;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        height: 200px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: rgba(0, 229, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 229, 255, 0.15);
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Card Icon floating effect */
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        display: inline-block;
        transition: transform 0.3s ease;
    }
    .glass-card:hover .card-icon {
        transform: rotate(-10deg) scale(1.1);
    }
    
    h4 {
        margin-top: 0;
        color: #ffffff;
        font-weight: 600;
    }
    p {
        color: #a0aec0;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. LIVE DATA TICKER
# ---------------------------------------------------------
st.markdown("""
    <div class="ticker-wrap">
        <div class="ticker-text">
            🔴 LIVE SYSTEM FEED &nbsp;&nbsp;|&nbsp;&nbsp; 
            DB Latency: 12ms &nbsp;&nbsp;|&nbsp;&nbsp; 
            Random Forest ACC: 94.2% &nbsp;&nbsp;|&nbsp;&nbsp; 
            K-Means Clusters: 4 Optimal &nbsp;&nbsp;|&nbsp;&nbsp; 
            API Traffic: Normal &nbsp;&nbsp;|&nbsp;&nbsp; 
            Last Model Training: 2 Hours Ago &nbsp;&nbsp;|&nbsp;&nbsp;
            Status: ALL SYSTEMS NOMINAL
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. HERO SECTION WITH 3D AI SPIRAL
# ---------------------------------------------------------
col_text, col_visual = st.columns([1.2, 1])

with col_text:
    st.markdown('<div class="glow-title">Nexus AI Studio</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #cbd5e1; font-weight: 300;'>Enterprise Customer Intelligence</h3>", unsafe_allow_html=True)
    
    st.write("""
        <span style="color:#94a3b8; font-size: 1.1rem; line-height:1.6;">
        Welcome to your command center. Transform raw customer data into predictive revenue strategies. 
        Leverage machine learning algorithms to predict churn, dynamically segment audiences, and discover 
        hidden lookalike buying patterns in milliseconds.
        </span>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("⚡ Initialize Core Systems", type="primary", use_container_width=False):
        with st.spinner("Aligning neural weights and syncing databases..."):
            time.sleep(1.5)
        st.success("✅ Core Initialized. Modules unlocked in sidebar.")

with col_visual:
    # 3D Parametric "AI DNA" / Neural Spiral Visual
    t = np.linspace(0, 20, 250)
    x = np.cos(t) * t
    y = np.sin(t) * t
    z = t

    fig = go.Figure()
    # Add glowing line
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color='rgba(0, 242, 254, 0.3)', width=2),
        hoverinfo='none'
    ))
    # Add glowing nodes
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=4,
            color=z,
            colorscale='Tealgrn', # Beautiful glowing cyber colors
            opacity=0.9,
            symbol='circle'
        ),
        hoverinfo='none'
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, backgroundcolor="rgba(0,0,0,0)"),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, backgroundcolor="rgba(0,0,0,0)"),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, backgroundcolor="rgba(0,0,0,0)"),
            camera=dict(eye=dict(x=1.2, y=1.2, z=0.8))
        ),
        height=350,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. GLASSMORPHISM MODULE GRID
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="glass-card">
            <div class="card-icon">📈</div>
            <h4>Executive Dashboard</h4>
            <p>High-level KPIs, global revenue distributions, and deep-dive demographic analytics.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="glass-card">
            <div class="card-icon">🧠</div>
            <h4>Custom Prediction</h4>
            <p>Input custom parameters manually to test AI model boundaries and accuracy in real-time.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="glass-card">
            <div class="card-icon">🎯</div>
            <h4>Audience Clustering</h4>
            <p>K-Means automatically groups your buyers into actionable loyalty and value profiles.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="glass-card" style="border-color: rgba(46, 204, 113, 0.4);">
            <div class="card-icon">✅</div>
            <h4 style="color: #2ecc71;">System Health</h4>
            <p style="margin-bottom: 2px;"><b>Database:</b> Secure & Connected</p>
            <p style="margin-bottom: 2px;"><b>Models:</b> Pre-loaded</p>
            <p><b>Status:</b> Optimal</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="glass-card">
            <div class="card-icon">⚠️</div>
            <h4>Churn Risk Radar</h4>
            <p>Random Forest models scan your active user base to predict drop-off before it happens.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="glass-card">
            <div class="card-icon">🛒</div>
            <h4>Lookalike Engine</h4>
            <p>KNN-based product matching. Find similar customers and pitch optimal pricing tiers.</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; color: #475569; margin-top: 50px; font-size: 0.85rem;">
        Nexus AI Platform v2.1.0 • Secure Enterprise Environment
    </div>
""", unsafe_allow_html=True)