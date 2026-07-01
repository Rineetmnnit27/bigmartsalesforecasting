import streamlit as st
import pandas as pd
import joblib

# ==========================================
# Load Pipeline
# ==========================================

pipeline = joblib.load("sales_pipeline (2).pkl")

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="BigMart Sales Prediction",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 BigMart Sales Prediction")
st.markdown("Predict the sales of a product in a BigMart outlet.")

st.divider()

# ==========================================
# Product Information
# ==========================================

st.subheader("📦 Product Information")

item_identifier = st.text_input(
    "Item Identifier",
    value="FDA15"
)

item_weight = st.number_input(
    "Item Weight",
    min_value=0.0,
    value=12.5
)

item_fat_content = st.selectbox(
    "Item Fat Content",
    [
        "Low Fat",
        "Regular",
        "LF",
        "low fat",
        "reg"
    ]
)

item_visibility = st.number_input(
    "Item Visibility",
    min_value=0.0,
    value=0.05,
    format="%.4f"
)

item_type = st.selectbox(
    "Item Type",
    [
        "Dairy",
        "Soft Drinks",
        "Meat",
        "Fruits and Vegetables",
        "Household",
        "Baking Goods",
        "Snack Foods",
        "Frozen Foods",
        "Breakfast",
        "Health and Hygiene",
        "Hard Drinks",
        "Canned",
        "Breads",
        "Starchy Foods",
        "Others",
        "Seafood"
    ]
)

item_mrp = st.number_input(
    "Item MRP",
    min_value=0.0,
    value=150.0
)

# ==========================================
# Outlet Information
# ==========================================

st.subheader("🏬 Outlet Information")

outlet_identifier = st.selectbox(
    "Outlet Identifier",
    [
        "OUT010",
        "OUT013",
        "OUT017",
        "OUT018",
        "OUT019",
        "OUT027",
        "OUT035",
        "OUT045",
        "OUT046",
        "OUT049"
    ]
)

outlet_establishment_year = st.selectbox(
    "Outlet Establishment Year",
    [
        1985,
        1987,
        1997,
        1998,
        1999,
        2002,
        2004,
        2007,
        2009
    ]
)

outlet_size = st.selectbox(
    "Outlet Size",
    [
        "Small",
        "Medium",
        "High"
    ]
)

outlet_location_type = st.selectbox(
    "Outlet Location Type",
    [
        "Tier 1",
        "Tier 2",
        "Tier 3"
    ]
)

outlet_type = st.selectbox(
    "Outlet Type",
    [
        "Grocery Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Supermarket Type3"
    ]
)

# ==========================================
# Prediction
# ==========================================

if st.button("Predict Sales"):

    outlet_age = 2026 - outlet_establishment_year

    if item_identifier.startswith("FD"):
        item_category = "Food"

    elif item_identifier.startswith("DR"):
        item_category = "Drinks"

    else:
        item_category = "Non-Consumable"

    if item_category == "Non-Consumable":
        item_fat_content = "Non-Edible"

    sample = pd.DataFrame({

        "Item_Weight":[item_weight],

        "Item_Visibility":[item_visibility],

        "Item_MRP":[item_mrp],

        "Outlet_Establishment_Year":[outlet_establishment_year],

        "Outlet_Age":[outlet_age],

        "Item_Fat_Content":[item_fat_content],

        "Item_Type":[item_type],

        "Outlet_Identifier":[outlet_identifier],

        "Outlet_Size":[outlet_size],

        "Outlet_Location_Type":[outlet_location_type],

        "Outlet_Type":[outlet_type],

        "Item_Category":[item_category]

    })

    prediction = pipeline.predict(sample)[0]

    st.success(f"### Predicted Sales: ₹ {prediction:,.2f}")

    st.metric(
        label="Estimated Sales",
        value=f"₹ {prediction:,.2f}"
    )