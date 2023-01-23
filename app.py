from flask import *  
import pickle
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
#from skimage.transform import resize
import numpy as np
import pandas as pd
import cv2 


app = Flask(__name__) 
import os 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=["POST","GET"])
def getImage():
    if request.method == 'POST':
        result = request.files['file']
        result.save(result.filename)
        pred = predict(result.filename)
        print(pred)
        os.remove(result.filename)
    return render_template('index.html')+ '''<div style='
    font-family: "Roboto", sans-serif;
  font-variant: small-caps;
  line-height: 1;
  color: #454cad;
  margin-bottom: 0;
   margin: 0;
   position: absolute;
   top: 80%;
   left: 50%;
   transform: translate(-50%, -50%);
}'><h1 style='font-size: 30px;'>Our Model predicts this image as ''' + pred + '.</h1></div>'

def predict(file):
    Class=['Car', 'AirPlane']
    model = pickle.load(open('carplane.pkl','rb'))
    img = cv2.imread(file,0)
    image=cv2.resize(img,(128,128))
    image = image.reshape(1,-1)
    print(image.shape)
    pred = model.predict(image)
    return Class[pred[0]]
   

if __name__ == '__main__':
    app.run(debug=True)