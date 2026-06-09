def predict_churn(rf_model, input_scaled):
    prediction = rf_model.predict(input_scaled)[0]
    probability = rf_model.predict_proba(input_scaled)[0][1] * 100
    return prediction, probability