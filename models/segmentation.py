def get_segment(kmeans_model, input_scaled):
    return kmeans_model.predict(input_scaled)[0]