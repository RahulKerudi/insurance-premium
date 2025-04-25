import streamlit as st
from prediction_helper import predict


st.title('Healthcare Premium Prediction')

categorical_columns = {
    'gender':['Male', 'Female'],
    'region':['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'marital_status':['Unmarried', 'Married'],
    'bmi_category':['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'smoking_status':['No Smoking', 'Regular', 'Occasional', 'Smoking=0', 'Does Not Smoke',
     'Not Smoking'],
    'employment_status':['Salaried', 'Self-Employed', 'Freelancer'],
    'medical_history':['Diabetes', 'High blood pressure', 'No Disease',
     'Diabetes & High blood pressure', 'Thyroid', 'Heart disease',
     'High blood pressure & Heart disease', 'Diabetes & Thyroid',
     'Diabetes & Heart disease'],
    'insurance_plan':['Bronze', 'Silver', 'Gold']
}


row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input('Age',min_value=18,max_value=100,step=1)
with row1[1]:
    no_of_dependants = st.number_input('No of Dependants',min_value=0,step=1)
with row1[2]:
    income_lakhs = st.number_input('Income in Lakhs',min_value=0,step=1)

with row2[0]:
    genetical_risk = st.number_input('Genetical Risk',min_value=0,step=1)
with row2[1]:
    gender = st.selectbox('Gender',categorical_columns['gender'])
with row2[2]:
    region = st.selectbox('Region',categorical_columns['region'])

with row3[0]:
    marital_status = st.selectbox('Marital Status',categorical_columns['marital_status'])
with row3[1]:
    bmi_category = st.selectbox('BMI Category',categorical_columns['bmi_category'])
with row3[2]:
    smoking_status = st.selectbox('Smoking Status',categorical_columns['smoking_status'])

with row4[0]:
    employment_status = st.selectbox('Employment Status',categorical_columns['employment_status'])
with row4[1]:
    medical_history = st.selectbox('Medical History',categorical_columns['medical_history'])
with row4[2]:
    insurance_plan = st.selectbox('Insurance Plan',categorical_columns['insurance_plan'])


input_dict = {
    'Age':age,
    'No of Dependants':no_of_dependants,
    'Income in Lakhs':income_lakhs,
    'Genetical Risk':genetical_risk,
    'Gender':gender,
    'Region':region,
    'Marital Status':marital_status,
    'BMI Category':bmi_category,
    'Smoking Status':smoking_status,
    'Employment Status':employment_status,
    'Medical History':medical_history,
    'Insurance Plan':insurance_plan
}



if st.button('Predict'):
    prediction = predict(input_dict)
    st.success(f'Predicted Premium Amount is: ₹ {prediction}')
