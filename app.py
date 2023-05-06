import boto3
import numpy as np
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)



# Down load pickle files from S3. Only use when needed, so we don't have to run everytime.
# s3 = boto3.client('s3')
# # Download the file from S3
# bucket_name = 'diabetesprojectfinal'
# s3.download_file(bucket_name, 'model/heart_attack_model.pkl', 'model/heart_attack_model.pkl')
# s3.download_file(bucket_name, 'model/diabetes_model.pkl', 'model/diabetes_model.pkl')

# Load Pickles
with open('model/diabetes_model.pkl', 'rb') as f:
    model1 = pickle.load(f)
with open('model/heart_attack_model.pkl', 'rb') as file:
    model2 = pickle.load(file)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


@app.route('/diabetes_results', methods=['POST'])
def diabetes_results():
    # Get form data from user input
    gender = int(request.form['gender'])
    if gender == 0:
        female = 1
        male = 0
    else:
        male = 1
        female = 0
    smoking_history = int(request.form['smoking_history'])
    if smoking_history == 0:
        never = 1
        no_info = 0
        current = 0
        former = 0
        ever = 0
    elif smoking_history == 1:
        never = 0
        no_info = 1
        current = 0
        former = 0
        ever = 0
    elif smoking_history == 2:
        never = 0
        no_info = 0
        current = 1
        former = 0
        ever = 0
    elif smoking_history == 3:
        never = 0
        no_info = 0
        current = 0
        former = 1
        ever = 0
    elif smoking_history == 4:
        never = 0
        no_info = 0
        current = 0
        former = 0
        ever = 1
    age = int(request.form['age'])
    hypertension = int(request.form['hypertension'])
    heart_disease = int(request.form['heart_disease'])
    bmi = float(request.form['bmi'])
    hba1c_level = float(request.form['HbA1c_level'])
    blood_glucose_level = int(request.form['blood_glucose_level'])

    form_data = np.array([[female, male, never, no_info, current, former, ever, age,
                           hypertension, heart_disease, bmi, hba1c_level, blood_glucose_level]])

    prediction = model1.predict(form_data)
    probability = model1.predict_proba(form_data)[0, 1]

    return render_template('diabetes_results.html', prediction=prediction[0], probability=probability)


@app.route('/heart_attack')
def heart_attack():
    return render_template('heart_attack.html')


@app.route('/hear_attack_results', methods=['POST'])
def heart_attack_results():
    # Get form data from user input
    age = int(request.form['age'])
    sex = int(request.form['sex'])
    cp = int(request.form['cp'])
    trtbps = int(request.form['trtbps'])
    chol = int(request.form['chol'])
    fbs = int(request.form['fbs'])
    restecg = int(request.form['restecg'])
    thalachh = int(request.form['thalachh'])
    exng = int(request.form['exng'])
    oldpeak = int(request.form['oldpeak'])
    slp = int(request.form['slp'])
    caa = int(request.form['caa'])
    thall = int(request.form['thall'])

    form_data = np.array([[age, sex, cp, trtbps, chol, fbs, restecg, thalachh,
                           exng, oldpeak, slp, caa, thall]])

    prediction = model2.predict(form_data)
    probability = model2.predict_proba(form_data)[0, 1]

    return render_template('heart_attack_results.html', prediction=prediction[0], probability=probability)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060, debug=True)
