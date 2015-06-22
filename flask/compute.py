__author__ = 'oier'

from numpy import exp, cos, linspace
import numpy as np
import matplotlib.pyplot as plt
import os, time, glob


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

def damped_vibrations(t, A, b, w):
    return A*exp(-b*t)*cos(w*t)

def compute(A, b, w, T, resolution=500):
    """Return filename of plot of the damped_vibration function."""
    t = linspace(0, T, resolution+1)
    u = damped_vibrations(t, A, b, w)
    plt.figure()  # needed to avoid adding curves in plot
    plt.plot(t, u)
    plt.title('A=%g, b=%g, w=%g' % (A, b, w))
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time since Jan 1, 1970 in filename in order make
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    return plotfile



def load_data():
    path = "/docs/cancer/blood"
    file = "Blood Samples.csv"
    file = os.path.join(path,file)
    data = pd.read_csv(file, sep =";")
    data["Fecha"] = [ datetime.strptime(i, "%m/%d/%Y")  for i in data["Fecha"] ]
    data = data.sort(columns="Fecha")
    return(data)

def model(x,y):
    clf = linear_model.LinearRegression()
    X = np.arange(len(x)).reshape(len(x),1)
    Y = y.reshape(len(y),1)
    line = clf.fit( X , Y ).predict(X)
    return(line)

def line_plot(col):
    print("col number:")
    print(col)

    data = load_data()
    #tratar datos
    colname = data.columns[col]

    m = data[colname]
    mask = (m.isnull() == False)
    y = data[colname][mask]
    x = data["Fecha"][mask]

    print("Y:")
    print(y)
    print("X:")
    print(x)
    #model
    line = model(x,y)

    print("line:")
    print(line)

    #Plotting
    plt.figure()
    plt.plot(y.values)
    plt.plot(np.arange(len(x)), line, c="r")
    plt.title(colname)
    labels = [ i.strftime("%Y/%m/%d") for i in x ]
    plt.xticks(range(y.size), labels, rotation=90)

    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time since Jan 1, 1970 in filename in order make
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)

    return plotfile


if __name__ == '__main__':
    print (line_plot(27))
    #print (compute(1, 0.1, 1, 20))