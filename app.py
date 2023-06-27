import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

#Funciones de apoyo

def PrimaryPredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 2)
    loaded_model = pickle.load(open("pickles/primary.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]  

def HeadshotPredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 3)
    loaded_model = pickle.load(open("pickles/headshots.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/primary')
def primary():
    return render_template('primary.html')

@app.route('/headshots')
def headshots():
    return render_template('headshots.html')

@app.route('/result_p',methods = ['POST'])
def result_p():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        data = to_predict_list = list(map(int, to_predict_list))
        try:
            to_predict_list = list(map(float, to_predict_list))
            result = PrimaryPredictor(to_predict_list)
            if int(result)==0:
                prediction='Pistola'
            elif int(result)==1:
                prediction='SMG'
            elif int(result)==2:
                prediction='Heavy Machine Gun'
            elif int(result)==3:
                prediction='AR'
            elif int(result)==4:
                prediction='Sniper'
            else:
                prediction=f'Cuchillo'
        except ValueError:
            prediction=f'Error en el formato de los datos{data}'

        return render_template("result_p.html", prediction=prediction)

@app.route('/result_h',methods = ['POST'])
def result_h():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        data = to_predict_list = list(map(float, to_predict_list))
        try:
            to_predict_list = list(map(float, to_predict_list))
            result = HeadshotPredictor(to_predict_list)
            prediction = result
        except ValueError:
            prediction=f'Error en el formato de los datos{data}'

        return render_template("result_h.html", prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)