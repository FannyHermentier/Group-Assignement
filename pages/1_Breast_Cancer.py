import streamlit as st
import pickle
import pandas as pd

# This should be the first Streamlit command used in your app, and it should only be called once!
st.set_page_config(page_title="Breast Cancer Risk Prediction App 🩺", page_icon="🔍", layout="wide")

# Load the saved model and scaler
@st.cache_resource
def load_model_scaler():
    with open('pages/SVM_cancer.sav', 'rb') as model_file, open('pages/scaler.pkl', 'rb') as scaler_file:
        model = pickle.load(model_file)
        scaler = pickle.load(scaler_file)
    return model, scaler

model, scaler = load_model_scaler()

# Define a background image
background_image = "breast_cancer.jpg" 
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(background_image, width=300) 

# Page Title
st.title("Breast Cancer Risk Prediction App 🩺")

# Introduction
st.markdown("""
    Welcome to the Breast Cancer Risk Prediction App. This app uses a sophisticated machine learning model to 
    estimate the likelihood of breast cancer being benign or malignant based on clinical feature input. 
    Please input the relevant data below to receive a prediction.
""")

# Sidebar - About the model
st.sidebar.header("About the Model")
st.sidebar.info("""
    This model was trained on a comprehensive dataset of breast cancer cases, 
    using advanced machine learning techniques to ensure high accuracy and reliability.
""")

# Sidebar - Contact
st.sidebar.header("Need Assistance?")
st.sidebar.info("""
    If you require professional medical advice or assistance, 
    please contact a healthcare provider immediately.
""")

# Create a form for user input
with st.form("prediction_form"):
    st.subheader("Enter the clinical features of the tumor:")

    # Initialize input_data
    input_data = {}

    # Generate input fields based on feature ranges
    feature_ranges = {
        "mean texture": (9.71, 39.28),
        "mean perimeter": (43.79, 188.5),
        "mean smoothness": (0.05263, 0.1634),
        "mean concavity": (0.0, 0.4268),
        "mean symmetry": (0.106, 0.304),
        "perimeter error": (0.757, 21.98),
        "compactness error": (0.002252, 0.1354),
        "concavity error": (0.0, 0.396),
        "concave points error": (0.0, 0.05279),
        "worst texture": (12.02, 49.54),
        "worst perimeter": (50.41, 251.2),
        "worst smoothness": (0.07117, 0.2226),
        "worst compactness": (0.02729, 1.058),
        "worst concavity": (0.0, 1.252),
        "worst concave points": (0.0, 0.291),
        "worst symmetry": (0.1565, 0.6638),
        "worst fractal dimension": (0.05504, 0.2075),
    }

    # Use columns to create a better layout
    cols = st.columns(len(feature_ranges) // 3 + (len(feature_ranges) % 3 > 0))
    for index, (feature, (min_val, max_val)) in enumerate(feature_ranges.items()):
        with cols[index % len(cols)]:
            # Here we assign the value to input_data inside the loop
            input_data[feature] = st.number_input(f"{feature} ({min_val} - {max_val})", 
                                                  min_value=min_val, max_value=max_val, 
                                                  value=(min_val+max_val)/2, 
                                                  step=0.01,
                                                  key=feature)

    # Submit button for the form
    submit_button = st.form_submit_button("Predict")

# Process user input and provide a prediction
if submit_button:
    input_df = pd.DataFrame([input_data])
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)
    result = "Malignant" if prediction[0] == 0 else "Benign"

    # Display results with a custom message
    st.subheader(f"The prediction is: **{result}**")
    if result == "Malignant":
        st.snow()
        st.error("⚠️Please consult with a medical professional for further evaluation and guidance.")
    else:
        st.balloons()
        st.success("✅ The tumor is predicted to be benign. For peace of mind, please verify with a healthcare provider.")

# Additional Information
st.info("""
    #### How to use this app:
    - Fill out the clinical feature information on the left.
    - Click the 'Predict' button to see the prediction result.
    
    #### Disclaimer:
    - This application is not intended to be a substitute for professional medical advice, diagnosis, or treatment.
    - Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
""")


