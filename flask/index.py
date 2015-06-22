__author__ = 'oier'

import json

from flask import Flask, make_response

app = Flask(__name__)

import seaborn as sns
import numpy as np
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import StringIO

from sklearn import linear_model




from models import InputForm, ValueSelector
from flask import Flask, render_template, request
from compute import compute, load_data, line_plot

@app.route('/')
def index():
    return 'Hello World!'

def form_values(request):
    data = load_data()
    form = ValueSelector(request)
    form.value.choices = [(k,i) for k,i in enumerate(data.columns)]
    return(form)


@app.route('/blood', methods=['GET', 'POST'])
def blood():
    form = form_values(request.form)
    if request.method == 'POST':# and form.validate():
        result = line_plot(form.value.data)
    else:
        print("False")
        result = None

    return render_template('plot.html',
                           form=form, result=result)

@app.route('/vib1', methods=['GET', 'POST'])
def vib1():
    #form = InputForm(request.form)
    form = form_values(request.form)
    if request.method == 'POST' and form.validate():
        result = compute(form.A.data, form.b.data,
                         form.w.data, form.T.data)
    else:
        result = None

    return render_template('view_plain.html',
                           form=form, result=result)


if __name__ == '__main__':
    app.run()