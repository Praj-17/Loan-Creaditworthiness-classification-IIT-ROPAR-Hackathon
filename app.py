import streamlit as st
import pandas as pd
from Archives.data_processing import clean_data, split_data
from Archives.model_training import get_models, train_and_evaluate_models
from Archives.visualisation import plot_model_comparison, plot_confusion_matrices

# Page config
st.set_page_config(page_title="Loan Risk Analyzer", layout="wide")

# Theme toggle
theme_mode = st.sidebar.radio("Select Theme", ("🌙 Dark", "🌞 Light"), index=0)

if theme_mode == "🌙 Dark":
    bg_color = "#0f1117"
    text_color = "#FFFFFF"
    button_color = "#444"
    success_text_color = "#FFFFFF"
else:
    bg_color = "#F8F4E1"
    text_color = "#000000"
    button_color = "#333333"
    success_text_color = "#000000"

# Custom CSS
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .stButton>button {{
            background-color: {button_color};
            color: white;
            font-size: 16px;
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            border: none;
        }}
        .stAlert.success {{
            background-color: #d4edda;
            color: {success_text_color} !important;
        }}
        div[data-testid="stAlertContainer"] p {{
            color: {success_text_color} !important;
        }}
    </style>
""", unsafe_allow_html=True)

# Sidebar title
st.sidebar.title("📁 Upload and Train")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload a preprocessed dataset (CSV)", type=["csv"])

# Default path
default_path = "Loan-Creaditworthiness-classification-main/data/Preprocessed/final.csv"

# Load dataset
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Custom dataset loaded successfully!")
else:
    try:
        df = pd.read_csv(default_path)
        st.sidebar.success("✅ Default dataset loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to load default dataset: {e}")
        df = None

# Training and output
if df is not None and st.sidebar.button("🚀 Train Models"):
    with st.spinner("Training in progress... Please wait ⏳"):
        df_cleaned = clean_data(df)
        X_train, X_test, y_train, y_test = split_data(df_cleaned, target_column='high_risk_applicant')
        models = get_models()
        results, predictions = train_and_evaluate_models(models, X_train, X_test, y_train, y_test)
        figs = plot_model_comparison(results)
        confusion_figs = plot_confusion_matrices(predictions)

    st.success("🎉 Training completed!")

    st.subheader("📊 Model Performance")
    for i in range(0, len(figs), 2):
        cols = st.columns(2)
        for j, fig in enumerate(figs[i:i+2]):
            cols[j].pyplot(fig)

    st.subheader("📉 Confusion Matrices")
    for i in range(0, len(confusion_figs), 2):
        cols = st.columns(2)
        for j, fig in enumerate(confusion_figs[i:i+2]):
            cols[j].pyplot(fig)
