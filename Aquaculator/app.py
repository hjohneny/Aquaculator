from asyncio.windows_events import NULL
from asyncio.windows_utils import pipe
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
import sklearn
from flask import jsonify
from datetime import date

tilapiamodel = pickle.load(open('TilapiaPriceDecisionTree.pkl', 'rb'))
yieldmodel = pickle.load(open('Yield_DecisionTree.pkl', 'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/tilapia_price")
def tilapia_price():
    return render_template('tilapia-price.html')

@app.route("/yield_cal")
def yield_cal():
    return render_template('yield-cal.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/predict_tilapia', methods=['POST'])
def predict_tilapia_price():
    Price_USD = float(request.form.get('Price_USD'))
    Exchange = float(request.form.get('Exchange'))

    #Tilapia price prediction
    tilapiaresult = tilapiamodel.predict(np.array([Price_USD, Exchange]).reshape(1,2))
    tilapiaoutput = np.round(tilapiaresult, 2)
    return render_template('tilapia-price.html', tilapiaresult="Predicted Tilapia Price per Kilo For Given Value:  RM: {} ".format(tilapiaoutput))

@app.route('/predict_yield', methods=['POST'])
def predict_yield_cal():
    Type = request.form.get('Type')
    Initial_Cost = float(request.form.get('Initial_Cost'))
    Maintenance_Cost = float(request.form.get('Maintenance_Cost'))
    Duration_Months = int(request.form.get('Duration_Months'))
    Tank_L = request.form.get('Tank_L')
    
    # yield prediction

    yieldvalue = pd.DataFrame([[Tank_L, Type, Initial_Cost, Maintenance_Cost, Duration_Months]], 
                    columns=['Tank_L', 'Type', 'Initial_Cost', 'Maintenance_Cost', 'Duration_Months'])
    prediction = yieldmodel.predict(yieldvalue)[0]
        
    yieldoutput = float(round(prediction))
    CBA = (yieldoutput * 1.5)/((Maintenance_Cost * Duration_Months)+Initial_Cost)

    if yieldoutput < 0:
        return render_template('yield-cal.html', prediction="Sorry insert valid value.")
    elif CBA < 1:
        return render_template('yield-cal.html', prediction="Predicted Yield after {} month(S): RM {} a month. CBA ratio: {}...Not profitable!".format(Duration_Months, yieldoutput, round(CBA, 2)))
    elif CBA > 1:
        return render_template('yield-cal.html', prediction="Predicted Yield after {} month(S): RM {} a month. CBA ratio: {}...Profitable. Please proceed with your project.".format(Duration_Months, yieldoutput, round(CBA, 2)))

if __name__ == '__main__':
    app.run(debug=True)