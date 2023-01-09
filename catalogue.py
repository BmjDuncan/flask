from datetime import *
import time
import sys
from db import *
import json
import requests
import mysql
# First we set our credentials

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)
app.debug = True

cnx = mysql.connector.connect(user='root', password='dacjd156n.',host='localhost', port='3306')
cursor = cnx.cursor()
create_database(cnx,cursor)

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

@app.route('/register', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']

        cnx = mysql.connector.connect(user='root', password='dacjd156n.',host='some-mysql')
        cursor = cnx.cursor()
        insert_user(cnx,cursor,username,password)

        return redirect(url_for('login'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="80")
