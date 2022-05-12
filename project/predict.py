from flask import Blueprint, message_flashed, redirect, render_template, request, url_for, flash
import pandas as pd 
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
#import xgboost as xgb
import sklearn
from . import db
from .models import Result, Vecteurs

data = pd.read_csv('/home/wiem/Document/projet_final/data/banking.csv', sep=';')

predict = Blueprint('predict', __name__)
@predict.route('/predict')
def predictTemplate():
    return render_template('prediction.html')



@predict.route('/predict', methods=['POST'])
def predict_post():
    age = int( request.form.get('age')) 
    education = str(request.form.get('education'))
    job = str(request.form.get('job'))
    marital = str(request.form.get('marital_status'))
    default = str(request.form.get('default'))
    housing = str(request.form.get('housing_loan'))
    loan = str(request.form.get('personal_loan'))
    contact = str(request.form.get('contact'))
    month = str(request.form.get('month'))
    day= str(request.form.get('day_of_week'))
    duration = float(request.form.get('duration'))
    poutcome = str(request.form.get('poutcome'))
    campaign = 1
    pdays = 999
    previous =0
    varRate =1.1
    priceIdx =93.994
    confIdx = -36.4
    euribor3m = 4.857
    employed = 4963.6

    if age < 18 :
        flash('WARNING: Your client is not of legal age')
        
    userVecteur = Vecteurs(age=age,job=job, marital=marital, education=education, default=default, housing=housing,
                   loan=loan, contact=contact, month=month, day=day, duration=duration, 
                   campaign=campaign, pdays=pdays, previous=previous, poutcome=poutcome,
                   varRate=varRate, priceIdx=priceIdx, confIdx=confIdx, euribor3m=euribor3m, employed=employed)
    db.session.add(userVecteur)
    db.session.commit()

    
    features_columns = ['age', 'job', 'marital', 'education', 'default', 'housing',
                        'loan', 'contact', 'month', 'day_of_week', 'duration', 'campaign', 'pdays',
       'previous', 'poutcome', 'emp_var_rate', 'cons_price_idx',
       'cons_conf_idx', 'euribor3m', 'nr_employed']

    
    user=[age,job, marital, education, default, housing, loan, 
        contact, month, day, duration, campaign, pdays,
       previous, poutcome, varRate, priceIdx,
       confIdx, euribor3m, employed] 

    df_user = pd.DataFrame([user], columns = features_columns)

    filename = "/home/wiem/Document/projet_final/API/flask-app/project/preprocessor.sav"
    my_preprocessor= pickle.load(open(filename,"rb"))

    
    model_file = "/home/wiem/Document/projet_final/API/flask-app/project/preprocessor_aug.sav"
    model = pickle.load(open(model_file,"rb"))

    encoded_user = my_preprocessor.transform(df_user)
    
    user_prediction = model.predict(encoded_user)
    predict_proba = model.predict_proba(encoded_user)
    predict_proba_user = predict_proba[0][0]
    

    

    if predict_proba_user < 0.8 :
        flash("Results are not satisfiying")
        #return redirect(url_for('predict.predict_post'))
        
    
    new_result = Result(contenu=user_prediction[0], predictProba=predict_proba_user)
    db.session.add(new_result)
    db.session.commit()

    if user_prediction ==['no']: 
        message = "Your client will not subscribe a term deposit"
    else:
        message = "Your client will subscribe a term deposit"
        
    return render_template('result.html', value = message)