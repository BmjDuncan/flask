from datetime import *
import time
import sys
import json
import requests
import mysql
import mysql.connector
import MySQLdb.cursors
import re
# First we set our credentials

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_mysqldb import MySQL
app = Flask(__name__)
app.debug = True

app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 35.195.173.196
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'goose'
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_PORT']=3306

# Intialize MySQL
mysql = MySQL(app)

@app.route('/Video/<video>')
def video_page(video):
    print (video)
    url = 'http://34.76.74.49/myflix/videos?filter={"video.uuid":"'+video+'"}'
    headers = {}
    payload = json.dumps({ })
    print (request.endpoint)
    response = requests.get(url)
    print (url)
    if response.status_code != 200:
      print("Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message']))
      return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
    jResp = response.json()
    print (type(jResp))
    print (jResp)
    for index in jResp:
        for key in index:
           if (key !="_id"):
              print (index[key])
              for key2 in index[key]:
                  print (key2,index[key][key2])
                  if (key2=="Name"):
                      video=index[key][key2]
                  if (key2=="file"):
                      videofile=index[key][key2]
                  if (key2=="pic"):
                      pic=index[key][key2]
    return render_template('video.html', name=video,file=videofile,pic=pic)

@app.route('/cat')
def cat_page():
    url = "http://34.76.74.49/myflix/videos"
    url2="http://34.76.74.49/myflix/categories"
    response2=requests.get(url2)
    jResp2=response2.json()

    headers = {}
    payload = json.dumps({ })

    response = requests.get(url)
    #print (response)
    # exit if status code is not ok
    print (response)
    print (response.status_code)
    if response.status_code != 200:
      print("Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message']))
      return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
    jResp = response.json()
    print (type(jResp))
    html="<h1> Your Videos</h1>"
    for cat in jResp2:
        html=html+'<div style="display:flex">'
        html=html+'<h2>'+cat["category"].title()+'</h2>'
        for index in jResp:
        #print (json.dumps(index))
            #print ("----------------")
            for key in index:

                if (key !="_id"):
                    if cat["category"] in index[key]["category"]:
                        name=index[key]["Name"]
                        thumb=index[key]["thumb"]
                        uuid=index[key]["uuid"]
                        html=html+'<div style="margin-right:10px;">'
                        html=html+'<p style="text-align:center;">'+name.title()+'<p>'
                        ServerIP=request.host.split(':')[0]
                        html=html+'<a href="http://'+ServerIP+'/Video/'+uuid+'">'
                        html=html+'<img src="http://34.79.49.178/pics/'+thumb+'">'
                        html=html+"</a>"
                        html=html+'</div>'
        html=html+'</div>'
    return html

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="80")
