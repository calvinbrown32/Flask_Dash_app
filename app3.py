import os
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

project_root = os.path.dirname(__file__)
print(project_root)
#template_path = os.path.join(project_root, 'app/templates')
#app = Flask(__name__, template_folder=template_path)

# import dash
# app = dash.Dash(__name__)
# server = app.server


server = flask.Flask(__name__)
# app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp')
# app.layout = html.Div(children=[
#     html.H1(children='Dash App')])


##************************************
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp', external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
##*******************************************************

app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp2', external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


#
# @server.route('/')
# def index():
#     return '''
# <html>
# <div>
#     <h1>Flask App</h1>
# </div>
# </html>
# '''

@server.route('/data_test')
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



# file Upload


# @server.route('/file_input_test')
# def file_input():
#     """Renders the file input page"""
#      return render_template('file_input_test.html')


# @server.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(secure_filename(f.filename))
#         return 'file uploaded successfully'
#
#

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'rtf'}

UPLOAD_FOLDER = '/tmp'
#UPLOAD_FOLDER = '/Users/calvindechicago/Desktop'
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@server.route('/upload_site', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>'''


@server.route(f'{UPLOAD_FOLDER}/<filename>')
def uploaded_file(filename):
    return send_from_directory(server.config['UPLOAD_FOLDER'],
                               filename)


# @app.route('/upload')
# def upload_file():
#     return render_template('upload.html')
#

# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(secure_filename(f.filename))
#         return 'file uploaded successfully'



# if __name__== "__main__":
#     #app.run()
#     app.run_server(debug=True)


#
#
# server = flask.Flask(__name__)
# #app = dash.Dash(__name__, server=server)
# app = dash.Dash(__name__, server=server, url_base_pathname='/pathname')

# @server.route('/hello')
# def hello():
# #     return 'Hello, World!'
#
#
# @server.route('/plotly_dashboard')
# def render_dashboard():
#     return flask.redirect('/pathname')

#
# app = Flask(__name__)
#
# server = flask.Flask(__name__)
# app = dash.Dash(__name__, server=server)
#
# app.layout = html.Div(
# 	children=[
#             **stuff goes here**
# 	]
# )

#
@server.route('/')
def hello_world():
    """test_page_2.html"""
    return render_template('test_page_2.html', author = 'Calvin')
#
#
# @app.route('/test_page_2')
# def test_page_2():
#     """returns another test page to demonstrate how flask routing works"""
#     return render_template('/test_page_2.html')

@server.route('/test_page/<test_pg_num>')
def test_page(test_pg_num):
    """This flask route  demonstrates variable rules """
    return 'This is test page ' + str(test_pg_num)


if __name__ == '__main__':
    server.run(debug=True)

# @server.route('/data_test')
# def data_test():
#     """Tests a number of functions including downloading a csv file from my github, and
#     loading it to an html page"""
#
#     # Download and munge the crash data from Github account
#     url = 'http://calvinbrown32.github.io/Collisions.csv'
#     crash_data = pd.read_csv(url)
#   #  crash_data.set_index(['CASE_ID'], inplace=True)
#   #  crash_data.index.name = None
#     bike_crashes = crash_data.loc[crash_data.BICYCLE_ACCIDENT == 'Y']
#     ped_crashes = crash_data.loc[crash_data.PEDESTRIAN_ACCIDENT == 'Y']
#
#     return render_template('data_test.html', tables=[bike_crashes.to_html(classes='bike'), ped_crashes.to_html(classes='ped')],
#                            titles=['na', 'Bike Crashes', 'Ped Crashes'])

#
# @app.route('/plotly_chart')
# def plotly_chart():
#     url = 'http://calvinbrown32.github.io/Collisions.csv'
#     crash_data = pd.read_csv(url)
#     crash_data['crash_date'] = pd.to_datetime(crash_data['COLLISION_DATE'])
#     crash_data2 = crash_data[['crash_date', 'CASE_ID']]
#     date_crash_count = crash_data2.groupby('crash_date', as_index=False).agg({"CASE_ID": "count"})
#     date_crash_count.columns = ['crash_date', 'crash_count']
#
#     fig = px.bar(date_crash_count, x='crash_date', y='crash_count')
#     return render_template('plotly_chart.html', html.Div([dcc.Graph(id='graph',figure=fig)]))

# if __name__== "__main__":
#     #app.run()
#     app.run_server(debug=True)
#
# if __name__ == '__main__':
#     server.run(debug=True)


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

#Dash intro
#https://www.datacamp.com/community/tutorials/learn-build-dash-python

#AttributeError: ‘NoneType’ object has no attribute ‘traverse’
#https://community.plotly.com/t/multipage-app-trouble-after-updating-dash-components/6382/4


## CALVIN NOTES  -
# Flask and Dash Guide shows how we can embed a dash app within our flask app. This is preferable
# as flask is much more flexible than Dash.

# https://stackoverflow.com/questions/34457981/trying-to-run-flask-app-gives-address-already-in-use
# You can get the pid of all running processes having python keyword using the command:
#     ps -fA | grep python
# After getting the pid's use kill command as follows:
#     kill -9 pid
# After running above two commands now run the flask app, it will work fine

