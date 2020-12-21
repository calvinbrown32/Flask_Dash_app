import os
import pandas as pd
from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


project_root = os.path.dirname(__file__)

print(project_root)
#template_path = os.path.join(project_root, 'app/templates')
#app = Flask(__name__, template_folder=template_path)


app = Flask(__name__)

@app.route('/')
def hello_world():
    """returns hello world"""
    return render_template('test_page_2.html', author = 'Calvin')


@app.route('/test_page_2')
def test_page_2():
    """returns another test page to demonstrate how flask routing works"""
    return render_template('/test_page_2.html')

@app.route('/test_page/<test_pg_num>')
def test_page(test_pg_num):
    """This flask route  demonstrates variable rules """
    return 'This is test page ' + str(test_pg_num)

@app.route('/data_test')
def data_test():
    """Tests a number of functions including downloading a csv file from my github, and
    loading it to an html page"""

    # Download and munge the crash data from Github account
    url = 'http://calvinbrown32.github.io/Collisions.csv'
    crash_data = pd.read_csv(url)
  #  crash_data.set_index(['CASE_ID'], inplace=True)
  #  crash_data.index.name = None
    bike_crashes = crash_data.loc[crash_data.BICYCLE_ACCIDENT == 'Y']
    ped_crashes = crash_data.loc[crash_data.PEDESTRIAN_ACCIDENT == 'Y']

    return render_template('data_test.html', tables=[bike_crashes.to_html(classes='bike'), ped_crashes.to_html(classes='ped')],
                           titles=['na', 'Bike Crashes', 'Ped Crashes'])


@app.route('/plotly_chart')
def plotly_chart():
    url = 'http://calvinbrown32.github.io/Collisions.csv'
    crash_data = pd.read_csv(url)
    crash_data['crash_date'] = pd.to_datetime(crash_data['COLLISION_DATE'])
    crash_data2 = crash_data[['crash_date', 'CASE_ID']]
    date_crash_count = crash_data2.groupby('crash_date', as_index=False).agg({"CASE_ID": "count"})
    date_crash_count.columns = ['crash_date', 'crash_count']

    fig = px.bar(date_crash_count, x='crash_date', y='crash_count')
    return render_template('plotly_chart.html', html.Div([dcc.Graph(id='graph',figure=fig)]))

if __name__== "__main__":
    app.run()
    #app.run_server(debug=True)


# Steps to creating a Python App / Module
# Create new directory where the app/module will sit
# $mkdir
# Create and activate virtual environment
# $virtualenv venv
# Install desired/necessary libraries
# Find virtual env python instance → use: $ ls venv
# Activate $ . venv/bin/activate
# Run Flask APP
# $flask run
# print out states:
# WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead. * Debug mode: off
#  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
#
# navigate to http://127.0.0.1:5000/ in web browser

#to deactivate virtual environment, simply type 'deactivate' in console

#
#
# Flask Tutorial
# https://www.youtube.com/watch?v=7M1MaAPWnYg&list=PLB5jA40tNf3vX6Ue_ud64DDRVSryHHr1h&index=1

#HTTP methods GET and POST tutorial
#https://www.youtube.com/watch?v=9MHYHgh4jYc

#
# TUTORIAL - TABLES TO PAGE
# https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
#
# BASIC FLASK APP
# https://opensource.com/article/18/4/flask

#python group by and aggregation tutorial
#https://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/

# Flask and Plotly App
# https://www.youtube.com/watch?v=yPSbJSblrvw

# Flask and Dash Tutorial - Flat Iron
# https://www.youtube.com/watch?v=MpFHXZqho7g

# Flask and Dash Guide
#https://hackersandslackers.com/plotly-dash-with-flask/

#Flask and Dash
#https://stackoverflow.com/questions/45845872/running-a-dash-app-within-a-flask-app

#Flask and Dash - plotly community
#https://community.plotly.com/t/run-a-dash-app-inside-a-flask-app/10331/2

