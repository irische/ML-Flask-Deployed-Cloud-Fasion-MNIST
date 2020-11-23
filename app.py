# Import Required Libraries

# Load librariesfrom flask 
from flask import Flask,render_template,request,send_file,send_from_directory,jsonify, redirect, url_for
#import pandas as pd
import numpy as np
from PIL import Image, ImageFilter


#import keras
import tensorflow as tf
# from matplotlib import pyplot as plt

from numpy import loadtxt
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
#from tensorflow.python.keras import losses

    
# instantiate flask 
app = Flask(__name__,static_folder='static',template_folder='templates')

#Define a directory of image
app.config["IMAGE_UPLOADS"] = "/uploads"
# load the model, and pass in the custom metric function

loaded_cnn_model = load_model("cnn_model.h5")
loaded_cnn_model.summary()

# For the root '/' we need to define a function in which we are rendering the template of index.html as default
# This rendering template is done if it get's any GET Request

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='GET':
        return render_template('index.html')

    if request.method=='POST':
        action = request.form['action']
        if action == 'classify':
            print(url_for('classify'))

            return redirect(url_for('classify'))


# For the root '/predict' we need to define a function named predict
# This function will take values from the ajax request and performs the prediction
# By getting response from flask to ajax it will display the response to the result field
# This whole above process occurs when request method is POST
# This rendering template is index.html if it get's any GET Request

@app.route('/classify',methods=['POST','GET'])
def classify():
    # if request.method=='GET':
    #     return redirect(url_for("main"))
    if request.method=='POST':
        print("CLASSIFY POST")
        print(request.url)
        print(url_for('index'))
        if request.files:
            print("Got image!")
            image = request.files['inputImage']
            im_grey = Image.open(image).convert('L')
            grey = np.array(im_grey)
            #grey.resize(28,28)
            #print(grey)
            #print(grey.shape)
            pixel_array = resizeTo(im_grey)
            print(pixel_array)
            print(pixel_array.shape)

            print("Start Predicting")
            label = loaded_cnn_model.predict(pixel_array)
            print(getLabel(label))



            # pixel_array = [(255 - x) * 1.0 / 255.0 for x in pixel_array]
            # pixel_array = np.array(pixel_array)
            # #X = np.random.random((28, 28))
            # plt.axis('off')
            # plt.close()
            # plt.imshow(pixel_array.reshape((28,28)))
            # #plt.imshow(pixel_array, cmap="gray")
            # plt.savefig('MNIST_IMAGE.png')#save MNIST image
            # plt.show()
            # plt.axis('off')
            # plt.close()

            print("IMAGE is here")
            return render_template('classify.html')

        print("POST METHOD ")
        if "back" in request.form:
            return redirect(url_for('index'))
    
    # # Predicting the label for the features collected
    # label=loaded_cnn_model.predict([features])
    
    # Returning the response to ajax	
def getLabel(a):
    labels = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]
    maxValue = max(a[0])
    for i in range(a[0].size):
        if a[0][i] == maxValue:
            return labels[i]
#Resize image to be 28x28 grayscale
def resizeTo(im):

    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255))
    print(width)
    print(height)

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
        if (nheight == 0):  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight) / 2), 0))  # calculate horizontal position
        newImage.paste(img, (4, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Height becomes 20 pixels.
        nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth) / 2), 0))  # caculate vertical pozition
        newImage.paste(img, (wleft, 4))  # paste resized image on white canvas


    pixels = np.array(newImage)
    pixels = pixels/255.0
    # pixel_array = [(255 - x) * 1.0 / 255.0 for x in pixel_array]
    # pixels = [(255 - x) * 1.0 / 255.0 for x in pixels]
    print("Result")

    n = pixels.size
    result = np.ones((n,1))

    #pixels = np.append(result, pixels)
    #all_data = np.concatenate((pixels, ones), 1)
    #pixels = np.hstack((ones,pixels))
    pixels = pixels.reshape(1, 28, 28, 1)

    print(pixels.shape)
    print(pixels)

    #plt.imshow()
    return pixels
    
# It is the starting point of code
if __name__=='__main__':
  # We need to run the app to run the server
  app.run(host='0.0.0.0',port=8080)
  # app.run(debug=True)