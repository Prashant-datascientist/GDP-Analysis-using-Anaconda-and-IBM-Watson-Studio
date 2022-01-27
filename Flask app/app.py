from flask import Flask, render_template, request # Flask is a application
# used to run/serve our application
# request is used to access the file which is uploaded by the user in out application
# render_template is used for rendering the html pages
import pickle # pickle is used for serializing and de-serializing Python object structures


app=Flask(__name__) # our flask app

@app.route('/') # rendering the html template
def home():
    return render_template('home.html')
@app.route('/predict') # rendering the html template
def index() :
    return render_template("index.html")

@app.route('/data_predict', methods=['GET','POST']) # route for our prediction
def predict():
    
    # loading model which we saved
    model = pickle.load(open('gdp.pkl', 'rb'))
 
    data = [[x for x in request.form.values()]]    
    
    prediction= model.predict(data)[0]
    print(prediction)
    
    return render_template('gdp_pred.html', prediction=prediction)

if __name__ == '__main__':
    app.run()