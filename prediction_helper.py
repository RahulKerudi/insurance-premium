from joblib import load
import pandas as pd


prediction_columns = load('artifacts/prediction_columns.joblib')
model_young = load('artifacts/model_young.joblib')
model_rest = load('artifacts/model_rest.joblib')
scaler_young = load('artifacts/scaler_young.joblib')
scaler_rest = load('artifacts/scaler_rest.joblib')


def get_normalized_score(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }
    diseases = medical_history.lower().split(' & ')
    min_val, max_val = 0, 14
    score = 0
    for disease in diseases:
        score += risk_scores[disease]
    normalized = (score - min_val) / (max_val - min_val)

    return normalized


def col_scaling(age, df):
    if age<=25:
        scale_obj = scaler_young['scaler']
        scale_cols = scaler_young['cols_to_scale']
    else:
        scale_obj = scaler_rest['scaler']
        scale_cols = scaler_rest['cols_to_scale']

    df['income_level'] = 0
    df[scale_cols] = scale_obj.transform(df[scale_cols])
    df.drop('income_level',axis=1,inplace=True)

    return df


def preprocessing(input_dict):
    insurance_plan_encode = {'Bronze':1, 'Silver':2, 'Gold':3}
    df = pd.DataFrame(0,columns=prediction_columns,index=[0])
    for key, value in input_dict.items():
        if key == 'Age':
            df['age'] = value
        elif key == 'No of Dependants':
            df['number_of_dependants'] = value
        elif key == 'Income in Lakhs':
            df['income_lakhs'] = value
        elif key == 'Genetical Risk':
            df['genetical_risk'] = value
        elif key == 'Gender' and value == 'Male':
            df['gender_Male'] = 1
        elif key == 'Marital Status' and value == 'Unmarried':
            df['marital_status_Unmarried'] = 1
        elif key == 'Region':
            if value == 'Northwest':
                df['region_Northwest'] = 1
            elif value == 'Southeast':
                df['region_Southeast'] = 1
            elif value == 'Southwest':
                df['region_Southwest'] = 1
        elif key == 'BMI Category':
            if value == 'Obesity':
                df['bmi_category_Obesity'] = 1
            elif value == 'Overweight':
                df['bmi_category_Overweight'] = 1
            elif value == 'Underweight':
                df['bmi_category_Underweight'] = 1
        elif key == 'Smoking Status':
            if value == 'Occasional':
                df['smoking_status_Occasional'] = 1
            elif value == 'Regular':
                df['smoking_status_Regular'] = 1
        elif key == 'Employment Status':
            if value == 'Salaried':
                df['employment_status_Salaried'] = 1
            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1
        elif key == 'Insurance Plan':
            df['insurance_plan'] = insurance_plan_encode.get(value,1)
        elif key == 'Medical History':
            df['normalized_risk_score'] = get_normalized_score(value)

    df = col_scaling(input_dict['Age'],df)
    return df

def predict(input_dict):
    df = preprocessing(input_dict)
    if input_dict['Age']<=25:
        model = model_young
    else:
        model = model_rest

    return int(model.predict(df))


