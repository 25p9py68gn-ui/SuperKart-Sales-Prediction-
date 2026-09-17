import streamlit as st
import os
import requests

st.set_page_config(page_title="SuperKart Sales Predictor", page_icon="🛒")
st.title("SuperKart Product-Store Sales Predictor")
st.write("Enter product and store characteristics to estimate sales revenue.")

api_url = st.text_input(
    "Backend prediction endpoint",
value = os.getenv("API_URL", "http://localhost:7860/v1/predict")
)

product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
allocated_area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027, format="%.3f")
mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox(
    "Store Type",
    ["Food Mart", "Supermarket Type1", "Supermarket Type2", "Departmental Store"]
)
product_id_char = st.selectbox("Product ID Prefix", ["FD", "DR", "NC"])
store_age = st.number_input("Store Age (Years)", min_value=0, value=16)
product_category = st.selectbox(
    "Product Type Category", ["Perishables", "Non Perishables"]
)

if st.button("Predict Sales"):
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": sugar,
        "Product_Allocated_Area": allocated_area,
        "Product_MRP": mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": city_type,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age,
        "Product_Type_Category": product_category,
    }
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        prediction = response.json()["predicted_sales"]
        st.success(f"Predicted Sales Revenue: {prediction:,.2f}")
    except Exception as exc:
        st.error(f"Prediction request failed: {exc}")
