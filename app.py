import numpy as np
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


with open('https://diabetesprojectfinal.s3.amazonaws.com/model/diabetes_model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/diabetes', methods=['POST'])
def diabetes():
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

    prediction = model.predict(form_data)
    probability = model.predict_proba(form_data)[0, 1]

    return render_template('result.html', prediction=prediction[0], probability=probability)


@app.route('/hear_attack')
def heart_attack():
    return render_template('heart_attack.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
