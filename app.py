# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 18:58:22 2022

@author: debas
"""
import numpy as np
import pandas as pd
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, request, url_for, redirect, jsonify

app = Flask(__name__)
model  = load_model("fruit")
model1  = load_model("vegetable")

@app.route('/', methods=['GET','POST'])
def index():
    mytext =[]
    text = []
    plant =[]
    mypath=[]
    file_path=[]
    if request.method == "POST":
        f = request.files['image']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads',f.filename)
        f.save(file_path)
       
        img  = image.load_img(file_path, target_size = (128,128))
        x = image.img_to_array(img)
        x = np.expand_dims(x,axis=0)
        plant=request.form['plant']
        if(plant=="fruit"): 
            y = np.argmax(model.predict(x),axis=1)
            index  = ['Apple___Black_rot','Apple___healthy','Corn_(maize)___Northern_Leaf_Blight','Corn_(maize)___healthy','Peach___Bacterial_spot','Peach___healthy']
            df=pd.read_excel('precautions - fruits.xlsx')
            text = df.iloc[y[0]]['caution']
            print(df.iloc[y[0]]['caution'])
        else:
            y = np.argmax(model1.predict(x),axis=1)
            index  = ['Pepper,_bell___Bacterial_spot','Pepper,_bell___healthy','Potato___Early_blight','Potato___healthy','Potato___Late_blight','Tomato___Bacterial_spot','Tomato___Late_blight','Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot']
            df=pd.read_excel('precautions - veg.xlsx')
            text = df.iloc[y[0]]['caution']
    return render_template('home.html',mytext=text, mypath=file_path)

if __name__ == '__main__':
    app.run(debug=True)