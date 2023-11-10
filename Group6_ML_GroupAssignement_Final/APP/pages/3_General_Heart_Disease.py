import streamlit as st
import pickle
import pandas as pd

# Load the saved model from the pickle file
with open("pages/xgboost_heart_disease_model.sav", "rb") as file:
    model = pickle.load(file)

# Streamlit page configuration
st.set_page_config(page_title="Heart Disease Risk Prediction", page_icon=":heart:", layout="wide")

# Define a function to predict heart disease risk
def predict_heart_disease_risk(Age, Sex, BP, Cholesterol, FBS_over_120, EKG_results, Max_HR, Exercise_angina, ST_depression, Slope_of_ST, Number_of_vessels_fluro, Thallium, Chest_pain_type_2, Chest_pain_type_3, Chest_pain_type_4):
    input_data = {
        'Age': Age,
        'Sex': Sex,
        'BP': BP,
        'Cholesterol': Cholesterol,
        'FBS over 120': FBS_over_120,
        'EKG results': EKG_results,
        'Max HR': Max_HR,
        'Exercise angina': Exercise_angina,
        'ST depression': ST_depression,
        'Slope of ST': Slope_of_ST,
        'Number of vessels fluro': Number_of_vessels_fluro,
        'Thallium': Thallium,
        'Chest pain type_2': Chest_pain_type_2,
        'Chest pain type_3': Chest_pain_type_3,
        'Chest pain type_4': Chest_pain_type_4
    }
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    return prediction[0]

# Header Image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("heart.jpg", use_column_width=True)

# Title and Introduction
st.title("Heart Disease Risk Prediction")
st.markdown("## Estimate the risk of heart disease based on your health factors.")

# Sidebar
st.sidebar.title("About the App")
st.sidebar.info("""
    This app uses a trained xgboost model to estimate the risk of heart disease based on various input features such as age, sex, blood pressure, cholesterol levels, and more.
""")
st.sidebar.title("Need Assistance?")
st.sidebar.info("""
    If you require professional medical advice or assistance, 
    please contact a healthcare provider immediately.
""")

# Input fields
st.subheader("Your Details")
Age = st.slider("Age (21-77)", 21, 77, 40)
Sex = st.radio("Sex", ("Female", "Male"))
Sex = 1 if Sex == "Male" else 0
BP = st.slider("Blood Pressure (mm Hg)", 94, 200, 120)
Cholesterol = st.slider("Cholesterol", 126, 564, 200)

st.subheader("Medical Information")
FBS_over_120 = st.checkbox("Fasting Blood Sugar > 120 mg/dl")
EKG_results = st.selectbox("EKG Results", ("Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"))
EKG_results = {"Normal": 0, "ST-T Wave Abnormality": 1, "Left Ventricular Hypertrophy": 2}[EKG_results]
Max_HR = st.slider("Maximum Heart Rate", 71, 202, 150)
Exercise_angina = st.checkbox("Exercise-Induced Angina")
ST_depression = st.slider("ST Depression", 0.0, 6.2, 2.0)

st.subheader("ST Segment")
Slope_of_ST = st.selectbox("Slope of ST Segment", ("Upsloping", "Flat", "Downsloping"))
Slope_of_ST = {"Upsloping": 1, "Flat": 2, "Downsloping": 3}[Slope_of_ST]
Number_of_vessels_fluro = st.slider("Number of Vessels Colored by Flourosopy (0-3)", 0, 3, 0)
Thallium = st.slider("Thallium", 3, 7, 3)

st.subheader("Chest Pain Types")
st.markdown("Indicate if you have one or more of the following chest pains:")
Chest_pain_type_2 = st.checkbox("Atypical Angina")
Chest_pain_type_3 = st.checkbox("Non-Anginal Pain")
Chest_pain_type_4 = st.checkbox("Asymptomatic")

# Prediction button
if st.button("Predict Heart Disease Risk"):
    result = predict_heart_disease_risk(Age, Sex, BP, Cholesterol, FBS_over_120, EKG_results, Max_HR, Exercise_angina, ST_depression, Slope_of_ST, Number_of_vessels_fluro, Thallium, Chest_pain_type_2, Chest_pain_type_3, Chest_pain_type_4)
    result_text = "High" if result == 1 else "Low"
    if result == 1:
        st.error(f"Risk of Heart Disease: {result_text}")
        st.write("⚠️ You may consider consulting a healthcare professional for further evaluation and advice.")
        st.markdown("For more information on heart disease prevention and risk management, you can visit [YourHealthcareWebsite](https://medlineplus.gov/ency/article/002203.htm).")
    else:
        st.success(f"Risk of Heart Disease: {result_text}")
        st.balloons()
        st.write(" ✅ You appear to be at a low risk of heart disease. However, it's essential to maintain a healthy lifestyle and consult with a healthcare professional for regular check-ups and guidance.")   

# Footer
st.markdown("---")
st.markdown(
    "© 2023 Heart Disease Risk Prediction App by IE University students."
)