__author__ = 'oier'


from wtforms import Form, FloatField, validators, SelectField, SelectMultipleField
from math import pi
from compute import load_data

class InputForm(Form):
    A = FloatField(
        label='amplitude (m)', default=1.0,
        validators=[validators.InputRequired()])
    b = FloatField(
        label='damping factor (kg/s)', default=0,
        validators=[validators.InputRequired()])
    w = FloatField(
        label='frequency (1/s)', default=2*pi,
        validators=[validators.InputRequired()])
    T = FloatField(
        label='time interval (s)', default=18,
        validators=[validators.InputRequired()])


data = load_data()
my_choices = [(k,i) for k,i in enumerate(data.columns)]

class ValueSelector(Form):
    value = SelectField(u'Plotting value', choices=my_choices)
    plot_type = SelectMultipleField(u'Plot type', choices=[(0, 'line'), (1, 'boxplot')])

