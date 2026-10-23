from flask import *
import joblib
import numpy as np
from datetime import datetime
import data.TestModel
import os

from views import preprocess

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/user')
def user():
    return render_template("user.html")


@user_bp.route('/user_home',  methods=['POST', 'GET'])
def admin_home():
    msg = ''
    if request.form['user'] == 'user' and request.form['pwd'] == 'user':
        return render_template("predict.html")
    else:
        msg = 'Incorrect username / password !'
    return render_template('user.html', msg=msg)



def getParameters():
    parameters = (request.form['addr'])
    print(parameters)

    return parameters

@user_bp.route('/predict',  methods=['POST', 'GET'])
def predict():
    print("hi1")
    parameters = []

    if request.method == 'POST':
        file_name = "final_predictions.csv"
        print(os.path.isfile(file_name) and preprocess()=="valid")
        if os.path.isfile(file_name):
            print(f"{file_name} exists.")
            msg = "Predictions generated successfully!!"
        else:
            print(f"{file_name} does not exist.")
            msg = "Predictions could not be generated!!"

        return render_template('result.html', msg=msg)

    else:
        return render_template('predict.html')

@user_bp.route('/userlogout')
def userlogout():
    return render_template("home.html")