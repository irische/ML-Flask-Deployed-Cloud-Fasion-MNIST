# Import Required Libraries

# Load libraries
from flask import Flask, jsonify, request
#import pandas as pd
import numpy as np

#import keras
import tensorflow as tf
from tf.keras.models import load_model
from tf.keras.utils import CustomObjectScope
from tf.keras.initializers import glorot_uniform
#from tensorflow.python.keras import losses

    
# instantiate flask 
app = Flask(__name__,static_folder='static',template_folder='templates')

# load the model, and pass in the custom metric function

loaded_cnn_model = tf.keras.models.load_model("cnn_model")

# For the root '/' we need to define a function in which we are rendering the template of index.html as default
# This rendering template is done if it get's any GET Request

@app.route('/',methods=['POST','GET'])
def main():
  if request.method=='GET':
    return render_template('index.html')

# For the root '/predict' we need to define a function named predict
# This function will take values from the ajax request and performs the prediction
# By getting response from flask to ajax it will display the response to the result field
# This whole above process occurs when request method is POST
# This rendering template is index.html if it get's any GET Request

@app.route('/classify',methods=['POST','GET'])
def classify():
  if request.method=='GET':
    return render_template('index.html')
  if request.method=='POST':
    if request.files:
        print("Got image!")
        image = request.files["inputImage"]
    print("POST METHOD ")
    
    # # Predicting the label for the features collected
    # label=loaded_cnn_model.predict([features])
    
    # Returning the response to ajax	
    return 0
    
# It is the starting point of code
if __name__=='__main__':
  # We need to run the app to run the server
  app.run(debug=False)