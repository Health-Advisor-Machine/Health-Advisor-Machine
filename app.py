import boto3
import numpy as np
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

s3 = boto3.client('s3')
# Download the file from S3
bucket_name = 'diabetesprojectfinal'
s3.download_file(bucket_name, 'model/heart_attack_model.pkl', 'model/heart_attack_model.pkl')
s3.download_file(bucket_name, 'model/diabetes_model.pkl', 'model/diabetes_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


with open('model/diabetes_model.pkl', 'rb') as f:
    model1 = pickle.load(f)


@app.route('/diabetes_results', methods=['POST'])
def diabetes_results():
    # Get form data from user input
    gender = int(request.form['gender'])
    age = int(request.form['age'])
    hypertension = int(request.form['hypertension'])
    heart_disease = int(request.form['heart_disease'])
    smoking_history = int(request.form['smoking_history'])
    bmi = int(request.form['bmi'])
    hba1c_level = int(request.form['HbA1c_level'])
    blood_glucose_level = int(request.form['blood_glucose_level'])

    form_data = np.array([[gender, age, hypertension, heart_disease, smoking_history, bmi, hba1c_level,
                           blood_glucose_level]])

    prediction = model1.predict(form_data)
    probability = model1.predict_proba(form_data)[0, 1]

    return render_template('diabetes_results.html', prediction=prediction[0], probability=probability)


@app.route('/heart_attack')
def heart_attack():
    return render_template('heart_attack.html')

with open('model/heart_attack_model.pkl', 'rb') as file:
    model2 = pickle.load(file)

@app.route('/hear_attack_results', methods=['POST'])
def heart_attack_results():
    # Get form data from user input
    age = int(request.form['Age'])
    sex = int(request.form['Sex'])
    cp = int(request.form['Chest Pain Type'])
    trtbps = int(request.form['Resting Blood Pressure'])
    chol = int(request.form['Cholesterol'])
    fbs = int(request.form['Fasting Blood Sugar'])
    restecg = int(request.form['Rest ECG'])
    thalachh = int(request.form['Max Heart Rate'])
    exng = int(request.form['Exercise Induced Angina'])
    oldpeak = int(request.form['ST Depression'])
    slp = int(request.form['Slope'])
    caa = int(request.form['Num Major Vessels'])
    thall = int(request.form['Thalassemia'])

    form_data = np.array([[age, sex, cp, trtbps, chol, fbs, restecg, thalachh,
                           exng, oldpeak, slp, caa, thall]])

    prediction = model2.predict(form_data)
    probability = model2.predict_proba(form_data)[0, 1]

    return render_template('heart_attack_results.html', prediction=prediction[0], probability=probability)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
