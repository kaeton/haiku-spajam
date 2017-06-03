#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set fileencoding=utf-8:

from flask import Flask, request
from flask import json
import requests
import boto3
app = Flask(__name__)

@app.route("/") #トップディレクトリ / は別に使うため
 #def hello():
 #    # return "{\"name\":\"goechan\"}"
 #    return "<h1 style='color:blue'>Hello There!</h1>"
def hello():
    return '<form action="/getAttribute" method="GET"><input name="url"><input type="submit" value="Search"></form>'

@app.route("/getAttribute")
def echo(): 
    session = boto3.Session(profile_name='default')
    rek = session.client('rekognition')
    
    resp = requests.get(request.args.get('url', ''))
    #resp = requests.get('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEpvRc3Td6OFWApLfYBdMgJ9SGbKpfIrhyTJxmScxF_s1LP28Ihg')
    imgbytes = resp.content
    
    # return "You said: " + request.args.get('text', '')
    rekresp = rek.detect_labels(Image={'Bytes': imgbytes})
    
    # print(rekresp)
    # return "You said: " + request.args.get('text', '')
    return str(rekresp)

@app.route("/uploadImage", methods = ['POST'])
def getImage():
    f = open('upload_sample.png', 'wb')
    f.write(request.data)
    return 'written data!\n'


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
