#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set fileencoding=utf-8:

from flask import Flask, request
from flask import json
import requests
import boto3
import json
import csv
import re
import random

app = Flask(__name__)

@app.route("/") #トップディレクトリ / は別に使うため
def hello():
    return '<form action="/getAttribute" method="GET"><input name="url"><input type="submit" value="Search"></form>'

def createHaiku(labellist):
    uselabel = labellist.copy()
    data = []
    upperdata = []
    middledata = []
    downdata = []

    for l in open('upper.csv').readlines():
        upperdata.append(l.rstrip('\r\n'))

    for l in open('middle.csv').readlines():
        middledata.append(l.rstrip('\r\n'))

    for l in open('down.csv').readlines():
        downdata.append(l.rstrip('\r\n'))

    data.append(upperdata)
    data.append(middledata)
    data.append(downdata)

    upperText = ""
    middleText = ""
    downText = ""
    for label in upperdata:
        for ulabel in uselabel:
            matchOB = re.match(ulabel, label)
            if matchOB != 'None':
                uselabel.remove(ulabel)
                upperText = label

    for label in middledata:
        for ulabel in uselabel:
            matchOB = re.match(ulabel, label)
            if matchOB != 'None':
                uselabel.remove(ulabel)
                middleText = label

    for label in downdata:
        for ulabel in uselabel:
            matchOB = re.match(ulabel, label)
            if matchOB != 'None':
                uselabel.remove(ulabel)
                downText = label

    if upperText=="":
        randint = random.randint(0,random.randint(0,len(upperdata)-1))
        upperText = upperdata[randint]

    if middleText=="":
        randint = random.randint(0,random.randint(0,len(middledata)-1))
        middleText = middledata[randint]

    if downText=="":
        randint = random.randint(0,random.randint(0,len(downdata)-1))
        downText = downdata[randint]

    return upperText+middleText+downText

@app.route("/getAttribute")
def echo(): 
    session = boto3.Session(profile_name='default')
    rek = session.client('rekognition')
    
    resp = requests.get(request.args.get('url', ''))
    #resp = requests.get('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEpvRc3Td6OFWApLfYBdMgJ9SGbKpfIrhyTJxmScxF_s1LP28Ihg')
    imgbytes = resp.content
    
    # return "You said: " + request.args.get('text', '')
    rekresp = rek.detect_labels(Image={'Bytes': imgbytes})
    en_namearr = rekresp['Labels']
    translated_labelarr = []
    label_arr = [x['Name'] for x in en_namearr]
    for label in label_arr:
        # translated_labelarr.append(requests.get('https://www.googleapis.com/language/translate/v2?key=AIzaSyALNfiZm9wC0VHwmRBBZS2ldc5f6gYXr-0&target=ja&q=' + label).text)
        # response = json.loads(requests.get('https://www.googleapis.com/language/translate/v2?key=AIzaSyALNfiZm9wC0VHwmRBBZS2ldc5f6gYXr-0&target=ja&q=' + label).text)
        response_text = requests.get('https://www.googleapis.com/language/translate/v2?key=AIzaSyALNfiZm9wC0VHwmRBBZS2ldc5f6gYXr-0&target=ja&q=' + label).text
        response = json.loads(response_text)
        data = response['data']#['translations']['translatedText']
        translation = data['translations']
        # return str(translation)
        m = re.search(r"Text\'\:\s\S*\s", str(translation))
        ja_label = re.search(r"\'\S*\'", str(m.group(0)))

        # ja_label = translation['translatedText']
        translated_labelarr.append(ja_label.group(0))
        # translated_labelarr.append(ja_label)

    # print(rekresp)
    # return "You said: " + request.args.get('text', '')
    # return requests.get('https://www.googleapis.com/language/translate/v2?key=AIzaSyALNfiZm9wC0VHwmRBBZS2ldc5f6gYXr-0&target=ja&q=Hello').text
    # return str(rekresp['Labels'])
    # return str(translated_labelarr)
    return createHaiku(translated_labelarr)

@app.route("/uploadImage", methods = ['POST'])
def getImage():
    f = open('upload_sample.png', 'wb')
    f.write(request.data)
    return 'written data!\n'


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
