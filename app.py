from flask import Flask, request, jsonify
import pandas as pd
import joblib
import io

superkart_api = Flask(__name__)
model = joblib.load("superkart_model.joblib")

FEATURES = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]

@superkart_api.get("/")
def health():
    return jsonify({"status": "SuperKart Sales Prediction API is running"})

@superkart_api.post("/v1/predict")
def predict():
    try:
        payload = request.get_json(force=True)
        input_df = pd.DataFrame([payload])[FEATURES]
        prediction = float(model.predict(input_df)[0])
        return jsonify({"predicted_sales": round(prediction, 2)})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

@superkart_api.post("/v1/predictbatch")
def predict_batch():
    try:
        uploaded_file = request.files["file"]
        batch_df = pd.read_csv(io.BytesIO(uploaded_file.read()))
        predictions = model.predict(batch_df[FEATURES])
        result = {str(i): round(float(v), 2) for i, v in enumerate(predictions)}
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860)
