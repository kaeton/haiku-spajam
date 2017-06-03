#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set fileencoding=utf-8:

import requests
import boto3

session = boto3.Session(profile_name='default')
rek = session.client('rekognition')

resp = requests.get('http://natgeo.nikkeibp.co.jp/atcl/news/16/b/040700074/01.jpg?__scale=w:400,h:452&_sh=09c09109e0')
#resp = requests.get('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEpvRc3Td6OFWApLfYBdMgJ9SGbKpfIrhyTJxmScxF_s1LP28Ihg')
imgbytes = resp.content

rekresp = rek.detect_labels(Image={'Bytes': imgbytes})

print(rekresp)
