# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 15:11:26 2022

@author: prash
"""
from flask import Flask, render_template, request
import requests
import os

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "YSMb-8yIZSGqqtutyiYVVP62U2dnnE4ptLQg2ZOeuABx"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app=Flask(__name__) # our flask app

@app.route('/') # rendering the html template
def home():
    return render_template('home.html')
@app.route('/predict') # rendering the html template
def index() :
    return render_template("index.html")

@app.route('/data_predict', methods=['GET','POST']) # route for our prediction
def predict():
    input_feature=[float(x) for x in request.form.values() ]  
    #features_values=[np.array(input_feature)]

    payload_scoring = {"input_data":[{"fields":["Population", "Area_sq_mi",
       "Pop_Density_per_sq_mi", "Coastline_coast_or_area_ratio",
       "Net_migration", "Infant_mortality_per_1000_births",
       "Literacy",
       "Arable", "Crops",
       "Deathrate", "Agriculture", "Industry", "Service", "Region_label",
       'Climate_label'],"values":[input_feature]}]}


    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f7369421-0013-4093-87d4-75bd441a04a9/predictions?version=2022-01-27', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions=response_scoring.json()
    output = predictions['predictions'][0]['values'][0][0]
    
    #print(output)
     # predictions using the loaded model file
    #prediction=model.predict(x)  
    #print("Prediction is:",prediction)
     # showing the prediction results in a UI
    #prediction = (output)
    return render_template("gdp_pred.html",pred=output)
if __name__=="__main__":
    
    # app.run(host='0.0.0.0', port=8000,debug=True)    # running the app
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=False,use_reloader=False)
