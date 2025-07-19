
import streamlit as st

# PASSWORD PROTECTION
def check_password():
    def password_entered():
        if st.session_state["password"] == "sepsis2025":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don’t store the password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        st.error("❌ Incorrect password")
        return False
    else:
        return True

# Block access unless correct password is entered
if not check_password():
    st.stop()


import streamlit as st
import joblib
import pandas as pd

# Load your trained model
model = joblib.load("lactate_model_streamlit.pkl")  # Update this name if needed

st.title("AI-Powered Lactate Risk Stratification")
st.write("Enter patient data to predict risk level:")

# Input fields
age = st.number_input("Age", min_value=18, max_value=100, value=65)
lactate = st.number_input("Lactate (mmol/L)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
hr = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=85)
sbp = st.number_input("Systolic BP (mmHg)", min_value=50, max_value=200, value=110)
dbp = st.number_input("Diastolic BP (mmHg)", min_value=30, max_value=120, value=70)

# Comorbidities as checkboxes
st.write("Check all comorbidities that apply:")
diabetes = st.checkbox("Diabetes")
hypertension = st.checkbox("Hypertension")
kidney_failure = st.checkbox("Kidney Failure")
heart_failure = st.checkbox("Heart Failure")

# Build input for model
comorb_values = [
    int(diabetes),
    int(heart_failure),
    int(hypertension),
    int(kidney_failure)
]
none_val = int(not any(comorb_values))
input_data = [age, lactate, hr, sbp, dbp] + comorb_values + [none_val]

expected_columns = [
    "Age", "Lactate (mmol/L)", "Heart Rate (bpm)", "Systolic BP (mmHg)", "Diastolic BP (mmHg)",
    "Diabetes", "Heart Failure", "Hypertension", "Kidney Failure", "None"
]

df = pd.DataFrame([input_data], columns=expected_columns)

if st.button("Predict Risk Level"):
    prediction = model.predict(df)[0]
    risk_levels = {
        0: "Low risk – stable",
        1: "Moderate risk – monitor closely",
        2: "High risk – likely septic shock"
    }
    st.success(f"Predicted Risk Level: **{risk_levels[prediction]}**")