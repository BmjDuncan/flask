from datetime import *
import time
import sys

import json
import requests
# First we set our credentials

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)
app.debug = True

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

@app.route('/')
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

                        html=html+'<h3>'+name+'</h3>'
                        ServerIP=request.host.split(':')[0]
                        html=html+'<a href="http://'+ServerIP+'/Video/'+uuid+'">'
                        html=html+'<img src="http://34.79.49.178/pics/'+thumb+'">'
                        html=html+"</a>"

    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0',port="80")
