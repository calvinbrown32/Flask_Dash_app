import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, request, send_from_directory, flash, session
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

project_root = os.path.dirname(__file__)
print(project_root)
template_path = os.path.join(project_root, 'app/templates')
# app = Flask(__name__, template_folder=template_path)


# import dash
# app = dash.Dash(__name__)
# server = app.server


server = flask.Flask(__name__)
# app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp')
# app.layout = html.Div(children=[
#     html.H1(children='Dash App')])

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'rtf'}

UPLOAD_FOLDER = '/tmp'
#UPLOAD_FOLDER = '/Users/calvindechicago/Desktop'
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
server.config['UPLOAD_EXTENSIONS'] = ['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.rtf', '.csv']



@server.route('/')
def hello_world():
    """test_page_2.html"""
    return render_template('test_page_2.html', author = 'Calvin')
##************************************
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp/', external_stylesheets=external_stylesheets)

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

app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp2/', external_stylesheets=external_stylesheets)

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
#============================================

#===========================================================
app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp_tims/', external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

url = 'http://calvinbrown32.github.io/Collisions.csv'
crash_data = pd.read_csv(url)
#  crash_data.set_index(['CASE_ID'], inplace=True)
#  crash_data.index.name = None
bike_crashes = crash_data.loc[crash_data.BICYCLE_ACCIDENT == 'Y']
ped_crashes = crash_data.loc[crash_data.PEDESTRIAN_ACCIDENT == 'Y']

#Create table of total crashes by year
df_bike = bike_crashes['ACCIDENT_YEAR'].value_counts().reset_index()
df_bike.columns = ['ACCIDENT_YEAR', 'total']


fig = px.bar(df_bike, x="ACCIDENT_YEAR", y="total", barmode="group")

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

#============================================




@server.route('/test_page/<test_pg_num>')
def test_page(test_pg_num):
    """This flask route  demonstrates variable rules """
    return 'This is test page ' + str(test_pg_num)

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@server.route('/upload_site', methods=['GET', 'POST'])
def upload_file1():
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


#===============================================
# UPLOAD SITE V2
# FROM: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
#===============================================

@server.route('/upload_site2')
def upload_file2():
    files = os.listdir(server.config['UPLOAD_FOLDER'])
    return render_template('/file_upload2.html', files=files)

@server.route('/upload_site2', methods=['GET', 'POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in server.config['UPLOAD_EXTENSIONS']:
            return "This type of file is not permitted", 400
        uploaded_file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
    return '', 204


@server.route(f'{UPLOAD_FOLDER}/<filename>')
def uploaded_file(filename):
    return send_from_directory(server.config['UPLOAD_FOLDER'],
                               filename)

#===============================================
# Trying to Print out uploaded file list
# https://stackoverflow.com/questions/49385103/return-list-of-previously-uploaded-files-back-to-flask
# https://stackoverflow.com/questions/19911106/flask-file-upload-limit
# URL FOR EXPLANATION
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#===============================================
@server.route("/uploaded_files2", methods=["POST"])
def uploaded_files():
    uploaded_files = flask.request.files.getlist("file[]")
    print(uploaded_files)
    return ""

@server.route('/upload_site3', methods=['GET', 'POST'])
def upload_files2():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in server.config['UPLOAD_EXTENSIONS']:
            return "This type of file is not permitted", 400
        if filename != '':
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
            session['filenames'] = filenames
    return render_template('uploaded_files.html', filenames=filenames)


@server.route('/uploaded_files2')
def uploaded_files2():
    return render_template('uploaded_files2.html', content=session['filenames'])


if __name__ == '__main__':
    server.run(debug=True)

