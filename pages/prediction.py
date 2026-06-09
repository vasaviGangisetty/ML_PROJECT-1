import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# --- Assuming these imports match your actual backend ---
from utils.helpers import load_all_models
from utils.preprocessing import preprocess_input

# ---------------------------------------------------------
# 1. PAGE CONFIG & PREMIUM CSS
# ---------------------------------------------------------
st.set_page_config(page_title="AI Prediction Engine", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    /* Premium Form Styling */
    div[data-testid="stForm"] {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Profile Card */
    .profile-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-left: 4px solid #4facfe;
        border-radius: 12px;
        padding: 20px;
        color: #f8fafc;
        box-shadow: 2px 4px 15px rgba(0,0,0,0.2);
    }
    .profile-metric {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 8px 0;
        font-size: 0.95rem;
    }
    .profile-metric:last-child {
        border-bottom: none;
    }
    .metric-label { color: #94a3b8; }
    .metric-value { font-weight: 600; color: #e2e8f0; }

    /* Action Badges */
    .badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-safe { background-color: rgba(46, 204, 113, 0.2); color: #4ade80; border: 1px solid #4ade80; }
    .badge-warn { background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #fbbf24; }
    .badge-risk { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #f87171; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. MODEL LOADING
# ---------------------------------------------------------
scaler, le, _, rf, _ = load_all_models()

# ---------------------------------------------------------
# 3. HEADER
# ---------------------------------------------------------
st.title("🔮 AI Prediction Sandbox")
st.markdown("<p style='color: #94a3b8;'>Input custom customer parameters below to run a live simulation against the Random Forest Neural Engine.</p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. INTERACTIVE FORM
# ---------------------------------------------------------
with st.form("pred_form"):
    st.markdown("### 🛠️ Configure Customer Profile")
    
    col_demo, col_behav = st.columns(2)
    
    with col_demo:
        st.markdown("#### 👤 Demographics")
        age = st.slider("Age", 18, 100, 35)
        gender = st.selectbox("Gender", ["Male", "Female"])
        income = st.number_input("Annual Income ($)", 10000, 200000, 65000, step=5000)
        
    with col_behav:
        st.markdown("#### 🛒 Behavioral Metrics")
        score = st.slider("Spending Score (1-100)", 1, 100, 45)
        freq = st.number_input("Purchases (Last 12 Months)", 1, 100, 12)
        spent = st.number_input("Total Lifetime Spent ($)", 100, 20000, 2500, step=100)
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("⚡ Run AI Analysis Sequence", use_container_width=True)

# ---------------------------------------------------------
# 5. AI PROCESSING & RESULTS
# ---------------------------------------------------------
if submit:
    # --- Simulated Boot Sequence ---
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("⚙️ Normalizing input features...")
    time.sleep(0.3)
    progress_bar.progress(30)
    
    status_text.text("🧠 Running Random Forest Classification Trees...")
    time.sleep(0.4)
    progress_bar.progress(70)
    
    status_text.text("📊 Compiling probability matrices...")
    time.sleep(0.3)
    progress_bar.progress(100)
    
    status_text.empty()
    progress_bar.empty()
    st.toast("AI Analysis Complete!", icon="✅")
    
    st.markdown("---")
    
    # --- Actual AI Prediction ---
    X_input = preprocess_input(scaler, le, age, gender, income, score, freq, spent)
    pred = rf.predict(X_input)[0]
    prob = rf.predict_proba(X_input)[0][1] * 100  # Probability of Churn
    
    # Determine Status & Assign Proper RGBA Colors for the Plot
    if prob >= 70:
        badge_class = "badge-risk"
        status_text = "CRITICAL CHURN RISK"
        color = "#ef4444"
        fill_color = "rgba(239, 68, 68, 0.25)" # Fixed RGBA format
        strategy = "Immediate intervention required. Deploy a high-value retention offer (e.g., 20% discount or free premium upgrade)."
    elif prob >= 40:
        badge_class = "badge-warn"
        status_text = "MODERATE FLIGHT RISK"
        color = "#f59e0b"
        fill_color = "rgba(245, 158, 11, 0.25)" # Fixed RGBA format
        strategy = "Customer is wavering. Add them to an automated re-engagement drip campaign showcasing new product features."
    else:
        badge_class = "badge-safe"
        status_text = "HIGHLY RETAINED (SAFE)"
        color = "#2ecc71"
        fill_color = "rgba(46, 204, 113, 0.25)" # Fixed RGBA format
        strategy = "Customer exhibits high loyalty. Optimal target for upselling premium tiers and referral programs."

    # --- RESULTS LAYOUT ---
    st.markdown(f"<h2>AI Verdict: <span class='badge {badge_class}'>{status_text}</span></h2>", unsafe_allow_html=True)
    
    colA, colB, colC = st.columns([1.2, 1, 1.2])
    
    # 1. GAUGE CHART
    with colA:
        st.markdown("### 🎯 Churn Probability")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            number={'suffix': "%", 'font': {'size': 40, 'color': color}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': color, 'thickness': 0.25},
                'bgcolor': "rgba(255,255,255,0.05)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 40], 'color': "rgba(46, 204, 113, 0.1)"},
                    {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.1)"},
                    {'range': [70, 100], 'color': "rgba(239, 68, 68, 0.1)"}
                ],
                'threshold': {'line': {'color': color, 'width': 4}, 'thickness': 0.75, 'value': prob}
            }
        ))
        fig_gauge.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
        st.plotly_chart(fig_gauge, use_container_width=True)

    # 2. BEAUTIFUL PROFILE CARD
    with colB:
        st.markdown("### 📋 Profile Scan")
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-metric"><span class="metric-label">Age</span><span class="metric-value">{age}</span></div>
            <div class="profile-metric"><span class="metric-label">Gender</span><span class="metric-value">{gender}</span></div>
            <div class="profile-metric"><span class="metric-label">Income</span><span class="metric-value">${income:,}</span></div>
            <div class="profile-metric"><span class="metric-label">Spend Score</span><span class="metric-value">{score}/100</span></div>
            <div class="profile-metric"><span class="metric-label">Frequency</span><span class="metric-value">{freq} / yr</span></div>
            <div class="profile-metric"><span class="metric-label">LTV (Spent)</span><span class="metric-value">${spent:,}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    # 3. RADAR CHART (Customer DNA)
    with colC:
        st.markdown("### 🧬 Customer DNA")
        # Normalize values to a 0-100 scale purely for the visual radar chart
        radar_vals = [
            (age/100)*100, 
            min((income/150000)*100, 100), 
            score, 
            min((freq/50)*100, 100), 
            min((spent/10000)*100, 100)
        ]
        categories = ['Age', 'Income', 'Spend Score', 'Frequency', 'Total Spent']
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=radar_vals + [radar_vals[0]], # Close the circle
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor=fill_color, # FIXED ERROR: Replaced hex with valid rgba string
            line=dict(color=color, width=2)
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)"),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")
            ),
            showlegend=False,
            height=280,
            margin=dict(l=30, r=30, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#94a3b8"}
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- AI STRATEGY RECOMMENDATION ---
    st.info(f"💡 **AI Recommended Strategy:** {strategy}")