from flask import Flask,request,jsonify, current_app,send_from_directory,send_file,abort,redirect,session,render_template,make_response
from flask_cors import CORS, cross_origin

from io import BytesIO
import json
import datetime,time
import os
import requests,urllib3,base64
import psycopg2
import psycopg2.extras
import hashlib

urllib3.disable_warnings()
app = Flask(__name__)
CORS(app)

def toJson(data,columns):
    results = []
    for row in data:
        results.append(dict(zip(columns, row)))
    return results