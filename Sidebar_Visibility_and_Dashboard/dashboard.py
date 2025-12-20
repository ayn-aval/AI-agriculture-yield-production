import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# ================================
# Load Data
# ================================
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "Datasets", "Crops_data.csv")
MODELS_DIR = os.path.join(BASE_DIR, "Models")


df = pd.read_csv(DATA_PATH)


# ================================
# Sidebar Navigation
# ================================
st.sidebar.title("🌾 AI Agriculture Yield Dashboard")
page = st.sidebar.radio(
    "Go to", ["Overview", "Data Insights", "Trends", "Leaderboard", "Crop Comparison", "Predictions", "Upload & Explore CSV"]
)

# ================================
# Overview
# ================================
if page == "Overview":
    st.title("📊 Cultivating Insights, Growing Predictions  🌱")
    st.markdown(
        """
        Welcome to the **AI Agriculture Yield Prediction App** 🌾  
        This dashboard helps visualize and predict crop yields with an intuitive UI.  
        Use the sidebar to navigate between sections.
        
        This project uses **Machine Learning & Data Science** to analyze and predict crop yields, 
        empowering researchers, students, and farmers with better insights. 🚜🌾
        """
    )
    st.info("💡 Tip: Hover over info icons ℹ️ to understand features!")
    
    # --- Contributors Section ---
    st.subheader("GSSoC’25")


    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**👩‍💻 Project Admin**")
        st.write("[Nupur Madaan](https://github.com/nupurmadaan04)")

    with col2:
        st.markdown("**🙋‍♀️ Contributor**")
        st.write("[Sakshi Srivastava](https://github.com/Sakshi-Srivastava19)")

    st.success("✨ Proudly built as part of **GSSoC’25 Open Source Program**")
# ================================
# Data Insights
# ================================
elif page == "Data Insights":
    st.title("📊 Data Insights")

    crop_sel = st.selectbox(
        "Select a Crop 🌾",
        ["RICE","WHEAT","MAIZE","SORGHUM","PEARL MILLET","BARLEY","CHICKPEA","SESAMUM","GROUNDNUT",
         "PIGEONPEA","RAPSEED & MUSTARD","SUNFLOWER","SAFFLOWER","CASTOR","LINSEED","SOYABEAN","OIL SEEDS",
         "SUGARCANE","COTTON"]
    )
    crop_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
    crop_state = st.sidebar.selectbox("Select State", sorted(df["State Name"].unique()))
    crop_metrics = st.sidebar.radio("Metric", ["Area","Yield","Production"])

    df1 = df[(df["Year"] == crop_year) & (df["State Name"] == crop_state)]

    area_col = f"{crop_sel} AREA (1000 ha)"
    yield_col = f"{crop_sel} YIELD (Kg per ha)"
    production_col = f"{crop_sel} PRODUCTION (1000 tons)"

    if crop_metrics == "Area":
        col = area_col
    elif crop_metrics == "Yield":
        col = yield_col
    else:
        col = production_col

    st.markdown("Your farming insights are ready! 📊")
    fig = px.bar(
        df1, x="Dist Name", y=col,
        title=f"{crop_sel} - {crop_metrics} in {crop_state} ({crop_year})",
        color_discrete_sequence=["#e07a5f"]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Summary metrics
    total_area = df1[area_col].sum()
    total_yield = df1[yield_col].mean()
    total_production = df1[production_col].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Area", f"{total_area:,.0f} (1000 ha)")
    col2.metric("Avg Yield", f"{total_yield:,.0f} kg/ha")
    col3.metric("Total Production", f"{total_production:,.0f} tons")
# ✅ Download filtered dataset
    st.subheader("💾 Download Filtered Data")
    csv_data = df1.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv_data,
        file_name=f"{crop_sel}_{crop_state}_{crop_year}.csv",
        mime="text/csv",
    )

# ================================
# Trends Over Time
# ================================
elif page == "Trends":
    st.title("📈 Crop Trends Over Time")

    crop_sel = st.selectbox("Select Crop 🌾", df.columns[df.columns.str.contains("YIELD")].str.replace(" YIELD (Kg per ha)", ""))
    crop_state = st.sidebar.selectbox("Select State", sorted(df["State Name"].unique()))
    metric = st.sidebar.radio("Metric", ["Area", "Yield", "Production"])

    area_col = f"{crop_sel} AREA (1000 ha)"
    yield_col = f"{crop_sel} YIELD (Kg per ha)"
    production_col = f"{crop_sel} PRODUCTION (1000 tons)"

    col = yield_col if metric == "Yield" else area_col if metric == "Area" else production_col
    trend_df = df[df["State Name"] == crop_state]

    fig_trend = px.line(
        trend_df, x="Year", y=col, color="Dist Name",
        title=f"{crop_sel} {metric} Trend in {crop_state}", markers=True
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# ================================
# Leaderboard
# ================================
elif page == "Leaderboard":
    st.title("🏆 Top 5 Districts")

    crop_sel = st.selectbox("Select Crop 🌾", df.columns[df.columns.str.contains("YIELD")].str.replace(" YIELD (Kg per ha)", ""))
    crop_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
    crop_state = st.sidebar.selectbox("Select State", sorted(df["State Name"].unique()))
    metric = st.sidebar.radio("Metric", ["Area", "Yield", "Production"])

    area_col = f"{crop_sel} AREA (1000 ha)"
    yield_col = f"{crop_sel} YIELD (Kg per ha)"
    production_col = f"{crop_sel} PRODUCTION (1000 tons)"

    col = yield_col if metric == "Yield" else area_col if metric == "Area" else production_col
    df1 = df[(df["Year"] == crop_year) & (df["State Name"] == crop_state)]

    top5 = df1.sort_values(by=col, ascending=False).head(5)
    st.table(top5[["Dist Name", col]])

# ================================
# Crop Comparison
# ================================
elif page == "Crop Comparison":
    st.title("🌾 Compare Crops")

    crop_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
    crop_state = st.sidebar.selectbox("Select State", sorted(df["State Name"].unique()))

    multi_crops = st.multiselect(
        "Select Crops to Compare",
        df.columns[df.columns.str.contains("YIELD")].str.replace(" YIELD (Kg per ha)", "")
    )

    df1 = df[(df["Year"] == crop_year) & (df["State Name"] == crop_state)]

    if multi_crops:
        compare_data = {}
        for c in multi_crops:
            compare_data[c] = df1[f"{c} YIELD (Kg per ha)"].mean()

        compare_df = pd.DataFrame.from_dict(compare_data, orient="index", columns=["Avg Yield"])
        st.bar_chart(compare_df)

# ================================
# Predictions (AI Model)
# ================================
# Predictions Page
elif page == "Predictions":
    st.title("🤖 Yield Predictions")

    try:
        model = joblib.load(os.path.join(MODELS_DIR, "rf_model.pkl"))
        scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    except FileNotFoundError:
        st.error("⚠️ Model files not found. Please ensure Models/ contains rf_model.pkl and scaler.pkl")
        st.stop()

    # Inputs
    rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0)
    fertilizer = st.number_input("🧪 Fertilizer (kg/ha)", min_value=0)
    area = st.number_input("🌍 Area (hectares)", min_value=0)
    temperature = st.number_input("🌡️ Temperature (°C)", min_value=-10.0)

    if st.button("🔮 Predict Yield for Rice"):
        try:
            # Adjust feature order as per training
            features = [[rainfall, fertilizer, area, temperature]]
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0]

            st.success(f"✅ Estimated Yield: **{prediction:.2f} tonnes**")
        except Exception as e:
            st.error(f"⚠️ Prediction failed: {e}")
    

# ================================
# Upload & Explore CSV
# ================================
elif page == "Upload & Explore CSV":
    st.title("📂 Upload & Explore Your Dataset")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        user_df = pd.read_csv(uploaded_file)

        st.subheader("🔎 Quick Glance at Data")
        st.dataframe(user_df.head(), use_container_width=True)

        st.subheader("📈 Interactive Charts")
        numeric_cols = user_df.select_dtypes(include="number").columns

        if len(numeric_cols) >= 2:
            x_axis = st.selectbox("Choose X-axis", numeric_cols, key="upload_x")
            y_axis = st.selectbox("Choose Y-axis", numeric_cols, key="upload_y")

            fig = px.scatter(
                user_df, x=x_axis, y=y_axis, trendline="ols",
                title=f"Scatter Plot: {x_axis} vs {y_axis}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Not enough numeric columns for visualization.")

        # ✅ Add download option
        st.subheader("💾 Download Processed Data")
        csv_data = user_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="processed_data.csv",
            mime="text/csv",
        )
    else:
        st.info("Please upload a CSV file to explore.")
