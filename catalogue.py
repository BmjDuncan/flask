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

@app.route('/Video/<video>')
def video_page(video):
    if 'loggedin' in session:
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
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    url = "http://35.195.173.196/myflix/users"
    response=requests.get(url)
    jResp=response.json()
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists
        account={}
        for i in jResp:
            if (i['username']==username and i['password']==password): 
                account={'username':username}
                
        # If account exists in accounts table in out database
        try:
            # Create session data, we can access this data in other routes
            session['username'] = account['username']
            session['loggedin'] = True
            # Redirect to cat page
            return redirect(url_for('cat'))
        except:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/cat')
def cat_page():  
    if 'loggedin' in session:
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
        html="<h1>Your Videos</h1>"
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
                            html=html+'<img src="http://34.79.49.178/pics/'+thumb+'" width="50" height="50">'
                            html=html+"</a>"
                            html=html+'</div>'
            html=html+'</div>'
        return html
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port="80")
