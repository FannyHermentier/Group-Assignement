import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os

# Streamlit page configuration
st.set_page_config(page_title="Chest X-Ray Pneumonia Detection", page_icon=":hospital:", layout="wide")

# Load the pre-trained model from the .h5 file
model_path = os.path.join("pages", "ANN_ChestXRay_model.h5")
model = tf.keras.models.load_model(model_path)

# Header Image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("chest.jpg", use_column_width=True)

# Title and Introduction
st.title("Chest X-Ray Pneumonia Detection App")
st.markdown("This app predicts whether pneumonia is present in a chest X-ray image.")

# Sidebar
st.sidebar.title("About the App")
st.sidebar.info(
    "This is a Chest X-Ray Pneumonia Detection App using a trained neural network model. "
    "Upload a chest X-ray image, and it will predict whether pneumonia is present."
)
st.sidebar.title("Need Assistance?")
st.sidebar.info("""
    If you have health concerns or symptoms, please consult a healthcare professional immediately.
""")

# File uploader
uploaded_file = st.file_uploader("Upload a chest X-ray image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded X-Ray Image", use_column_width=True)
    
    # Preprocess the uploaded image
    img = image.load_img(uploaded_file, target_size=(150, 150))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    
    # Make predictions
    prediction = model.predict(img)
    
    # Display results with a custom message
    if prediction > 0.5:
        st.error("⚠️ Prediction: Pneumonia Detected. Please consult with a medical professional for further evaluation and guidance.")
    else:
        st.success("✅ Prediction: No Pneumonia Detected. However, for peace of mind, please verify with a healthcare provider.")
        st.balloons()

# Footer
st.markdown("---")
st.markdown(
    "© 2023 Chest X-Ray Pneumonia Detection App by IE University Students."
)

# Additional styling
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-image: linear-gradient(#d6e0f0, #f7f7f7);
    }
    </style>
    """, unsafe_allow_html=True)
