import joblib
import streamlit as st

@st.cache_resource # This fixes memory errors and speeds up the app
def load_all_models():
    scaler = joblib.load('saved_models/scaler.pkl')
    le = joblib.load('saved_models/label_encoder.pkl')
    kmeans = joblib.load('saved_models/segment_model.pkl')
    rf = joblib.load('saved_models/churn_model.pkl')
    knn = joblib.load('saved_models/knn_model.pkl')
    return scaler, le, kmeans, rf, knn