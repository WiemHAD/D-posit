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
from .models import Result, Info


predict = Blueprint('predict', __name__)
@predict.route('/predict')
def predictTemplate():
    return render_template('prediction.html')



@predict.route('/predict', methods=['POST'])
def predict_post():
    age = int( request.form.get('age'))  
    job = str(request.form.get('job'))
    marital = str(request.form.get('marital_status'))
    default = str(request.form.get('default'))
    housing = str(request.form.get('housing_loan'))
    contact = str(request.form.get('contact'))
    month = str(request.form.get('month'))
    day = str(request.form.get('day'))
    duration = int(request.form.get('duration'))
    education = "basic.4y"
    loan = "no"
    poutcome = 'nonexistent'
    campaign = 1
    pdays = 999
    previous =0
    emp_var_rate =1.1
    cons_price_idx =93.994
    cons_conf_idx = -36.4
    euribor3m = 4.857
    nr_employed = 4963.6


    # newinfo = Info(age,job,marital, default , housing,contact,month,day,duration,education,loan)
    # db.session.add(newinfo)
    # db.session.commit()


    if age > 18 :
        flash('Votre age est superieur a 18')

    
    features_columns = ['age', 'job', 'marital', 'education', 'default', 'housing',
                        'loan', 'contact', 'month', 'day_of_week', 'duration', 'campaign', 'pdays',
       'previous', 'poutcome', 'emp.var.rate', 'cons.price.idx',
       'cons.conf.idx', 'euribor3m', 'nr.employed']
    
    user=[age,job, marital, education, default, housing, loan, 
        contact, month, day, duration, campaign, pdays,
       previous, poutcome, emp_var_rate, cons_price_idx,
       cons_conf_idx, euribor3m, nr_employed] 
    
    df_user = pd.DataFrame([user], columns = features_columns)
    
    #reshaped_array = user_df.reshape(1,-1)

    filename = "preprocessor2.sav"
    
    my_preprocessor= pickle.load(open(filename,"rb"))
    #user_fit = my_preprocessor.fit(reshaped_array)
    user_prediction = my_preprocessor.predict(df_user)
    
    new_result = Result(contenu=user_prediction[0])
    db.session.add(new_result)
    db.session.commit()
    print('************************************')
    print(Result.query.all())
    print('************************************')
    
    if user_prediction ==['no']: 
        message = "Le client ne souscrira pas de produit d'épargne"
    else:
        message = "le client souscrira un produit d'épargne"
        
    return render_template('result.html', value = message)