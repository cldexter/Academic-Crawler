# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: web.py
   Description: 网络界面，通过网络进行操作
   Author: Dexter Chen
   Date：2017-10-28
-------------------------------------------------
"""
from flask import Flask
from flask import render_template
from flask import request
import mongodb_handler as mh

app = Flask(__name__)


@app.route('/')
def hello():
    return "hello"


@app.route('/new/<number>')
def new(number):
    content = mh.read_content("cancer", "lung,cancer", int(number))
    return render_template('content_template.html', content = content)


if __name__ == '__main__':
    app.run()   