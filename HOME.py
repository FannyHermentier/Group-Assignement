import streamlit as st

# Streamlit page configuration
st.set_page_config(page_title="Medical Diagnosis App", page_icon="🏥", layout="wide")

# Header Image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("picture.jpg", use_column_width=True)  # Replace with the path to your image

# Title and Introduction
st.title("Welcome to the Medical Diagnosis App! 👩‍⚕️🏥")
st.markdown("Explore our advanced medical diagnosis tools for a quick and efficient analysis.")

# Main Content with Highlight Boxes
st.markdown("""
        ### Available Diagnoses:
    <ul>
        <li><a href="#breast-cancer-detection" style="text-decoration: none; color: #000;">Breast Cancer Detection</a></li>
        <li><a href="#stroke-risk-detection" style="text-decoration: none; color: #000;">Stroke Risk Detection</a></li>
        <li><a href="#heart-disease-detection" style="text-decoration: none; color: #000;">Heart Disease Detection</a></li>
        <li><a href="#pneumonia-detection" style="text-decoration: none; color: #000;">Pneumonia Detection</a></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### How to Use:")
st.info("""
    - Choose a diagnosis from the sidebar.
    - Upload relevant data or images for diagnosis.
    - Receive instant diagnosis results.
""")

st.markdown("### About the App:")
st.warning("""
    - We utilize advanced machine learning models for accurate diagnoses.
    - Your health and well-being are our top priorities.
""")

st.markdown("### Want to Learn More?")
st.success("""
    - Visit our [official website](https://www.sanidad.gob.es/en/home.htm) for more information.
    - Engage with our community on [forums](https://www.ie.edu/) and share your feedback.
    - Trust the Medical Diagnosis App for expert guidance on your health matters.
""")

# Footer
st.markdown("---")
st.markdown(
    "© 2023 Medical Diagnosis App by IE University Students."
)

# Additional styling for the page
st.markdown("""
    <style>
    .st-eb {
        border: 2px solid #f63366;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
