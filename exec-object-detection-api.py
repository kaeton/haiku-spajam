#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set fileencoding=utf-8:

import requests
import boto3

# session = boto3.Session(profile_name='default')
# sns = session.client('sns')
# sns.publish(PhoneNumber='+15558675309', Message='Hello from boto')
# rek = session.client('rekognition')
#
# with open('trump.jpg', 'rb') as f:
#     imgbytes = f.read()
#
# # imgfile.close()
#
# # imgobj = {'Bytes': imgbytes}
# # imgattrs = ['ALL']
#
# rekresp = rek.detect_labels(Image={'Bytes': imgbytes})

session = boto3.Session(profile_name='default')
rek = session.client('rekognition')

resp = requests.get('http://stash.compciv.org/2017/obama.jpg')
imgbytes = resp.content

rekresp = rek.detect_faces(Image={'Bytes': imgbytes},
                           Attributes=['ALL'])
