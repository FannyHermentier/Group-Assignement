import streamlit as st
import pandas as pd
from joblib import load

# Set page configuration
st.set_page_config(page_title="Stroke Risk Predictor", layout="wide", page_icon=":brain:")

# Load the pre-trained model and the preprocessing pipeline
model = load('pages/rf_model.sav')  # Update the path as needed
preprocessing = load('pages/preprocessing.joblib')

# Define a function to make predictions
def predict_stroke_risk(input_data):
    processed_data = preprocessing.transform(pd.DataFrame([input_data]))
    prediction = model.predict(processed_data)[0]
    return prediction

# Header Image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("stroke.jpg", use_column_width=True)

# Header and Introduction
st.title("🧠 Stroke Risk Prediction App")
st.markdown("## Estimate your risk of having a stroke based on health factors.")

# Sidebar
st.sidebar.title("About the App")
st.sidebar.info(
    "This app uses a machine learning model to estimate the risk of stroke. "
    "Fill out the information below and hit 'Predict' to see your results."
)
st.sidebar.title("Need Assistance?")
st.sidebar.info(
    "If you require professional medical advice or assistance, "
    "please contact a healthcare provider immediately."
)

# Input form
with st.form(key='prediction_form'):
    st.subheader("Input Information")
    gender = st.radio("Gender", ("Male", "Female", "Other"), horizontal=True)
    age = st.slider("Age", 0, 100, 50)
    hypertension = st.radio("Hypertension", ("No", "Yes"), horizontal=True)
    heart_disease = st.radio("Heart disease", ("No", "Yes"), horizontal=True)
    married = st.radio("Married", ("No", "Yes"), horizontal=True)
    work_type = st.selectbox("Work type", ("Children", "Govt_job", "Never_worked", "Private", "Self-employed"))
    residence_type = st.radio("Residence type", ("Rural", "Urban"), horizontal=True)
    avg_glucose_level = st.number_input("Average Glucose Level", 0.0, 500.0, 100.0, 0.1)
    smoking_status = st.selectbox("Smoking Status", ("Formerly smoked", "Never smoked", "Smokes", "Unknown"))
    
    submit_button = st.form_submit_button("Predict")

# Prediction logic
if submit_button:
    input_data = {
        'gender': gender,
        'age': age,
        'hypertension': 1 if hypertension == "Yes" else 0,
        'heart_disease': 1 if heart_disease == "Yes" else 0,
        'ever_married': married,
        'work_type': work_type,
        'Residence_type': residence_type,
        'avg_glucose_level': avg_glucose_level,
        'smoking_status': smoking_status
    }
    
    prediction = predict_stroke_risk(input_data)
    
    col1, col2, col3 = st.columns(3)
    with col2:  # Centering the output
        if prediction == 1:
            st.error("⚠️ High Stroke Risk")
            st.markdown("### Consult a healthcare professional for further evaluation and advice.")
            st.markdown("[Learn More About Stroke Prevention](https://www.stroke.org/en/about-stroke/stroke-prevention)")
        else:
            st.success("✅ Low Stroke Risk")
            st.balloons()
            st.markdown("### Continue to maintain a healthy lifestyle.")

# Footer
st.markdown("---")
st.markdown(
    "© 2023 Stroke Risk Prediction App by IE University Students. "
    "Data from [Kaggle](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset)."
)
  