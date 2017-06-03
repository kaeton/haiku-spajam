#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set fileencoding=utf-8:

from flask import Flask

app = Flask(__name__)

@app.route("/") #トップディレクトリ / は別に使うため
def hello():
    return "{\"name\":\"goechan\"}"
    # return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
