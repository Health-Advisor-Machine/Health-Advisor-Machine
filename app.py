import time
import boto3
import numpy as np
from flask import Flask, render_template, request, flash
import pickle

app = Flask(__name__)
app.secret_key = 'TRUNG TRAN'

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
    feet = int(request.form['feet'])
    inches = int(request.form['inches'])
    weight = int(request.form['weight'])
    # calculate BMI
    height_m = (feet * 0.3048) + (inches * 0.0254)
    weight_kg = weight * 0.45359237
    bmi = round(weight_kg / (height_m ** 2), 1)
    hba1c_level = float(request.form['HbA1c_level'])
    blood_glucose_level = int(request.form['blood_glucose_level'])
    # Important to check feature's orders
    form_data = np.array([[female, male, never, no_info, current, former, ever, age,
                           hypertension, heart_disease, bmi, hba1c_level, blood_glucose_level]])

    prediction = model1.predict(form_data)
    probability = model1.predict_proba(form_data)[0, 1]

    return render_template('diabetes_results.html', prediction=prediction[0], probability=probability)


@app.route('/heart_attack')
def heart_attack():
    return render_template('heart_attack.html')


@app.route('/heart_attack_results', methods=['POST'])
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
    oldpeak = float(request.form['oldpeak'])
    slp = int(request.form['slp'])
    caa = int(request.form['caa'])
    thall = int(request.form['thall'])

    form_data = np.array([[age, sex, cp, trtbps, chol, fbs, restecg, thalachh,
                           exng, oldpeak, slp, caa, thall]])

    prediction = model2.predict(form_data)
    probability = model2.predict_proba(form_data)[0, 1]

    return render_template('heart_attack_results.html', prediction=prediction[0], probability=probability)


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = 'final_comments'
# COMMAND IN CLI TO DOWNLOAD FROM DYNAMODB
# aws dynamodb scan --table-name comments --output json --query "Items[*]" > json/comments.json

# Check if table already exists
existing_tables = list(dynamodb.tables.all())
if any(table.name == table_name for table in existing_tables):
    table = dynamodb.Table(table_name)
else:
    # Create comments table
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'comment_id',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'comment_id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    # Wait for table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)


@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html')


@app.route('/feedback', methods=['POST'])
def add_feedback():
    name = request.form['name']
    rating = request.form['rating']
    comment = request.form['comment']

    # Add comment to DynamoDB table
    table.put_item(
        Item={
            'comment_id': str(time.time()),
            'name': name,
            'rating': rating,
            'comment': comment
        }
    )
    flash('Thank you for your comment! It was saved on DynamoDB')
    return render_template('feedback.html')


@app.route('/craziness')
def craziness():
    return render_template("craziness.html")


@app.route('/craziness_results', methods=['POST'])
def craziness_results():
    choice = request.form['developer']
    if choice == "0":
        message = "YOU ARE CRAZY!"
    else:
        message = "ARE YOU CRAZY?"

    return render_template("craziness_results.html", message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060, debug=True)
