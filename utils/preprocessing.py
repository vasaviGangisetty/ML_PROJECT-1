import numpy as np

def preprocess_input(scaler, le, age, gender, income, score, freq, spent):
    gen_enc = le.transform([gender])[0]
    data = np.array([[age, gen_enc, income, score, freq, spent]])
    return scaler.transform(data)