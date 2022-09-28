# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : proxyApi.py
from functools import wraps

from proxy_pool.storages import RedisHandle
from flask import Flask, jsonify, request
from werkzeug.wrappers import Response

from setting import API_HOST,API_PORT

app = Flask(__name__)
rh = RedisHandle()

class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JsonResponse, cls).force_type(response, environ)
app.response_class = JsonResponse

def front(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        type = request.args.get("type", "").lower()
        if type not in ['','http','https']: return "Please enter the correct type. e.g. type=http"
        return func(*args, **kwargs)
    return wrapper

api_list = [
    {"url": "/get", "params": "type: 'e.g. http'", "desc": "get all same type proxy"},
    {"url": "/random", "params": "type: 'e.g. http'", "desc": "get a high score random proxy"},
    {"url": "/delete", "params": "proxy: 'e.g. 127.0.0.1:8080'", "desc": "delete an unable proxy"},
    {"url": "/all", "params": "type: 'e.g. http'", "desc": "get all proxy from proxy pool"},
    {"url": "/count", "params": "type: 'e.g. http'", "desc": "return proxy count"}
]

@app.route('/')
def index():
    """
    Show api list
    :return:
    """
    return {'api': api_list}

@app.route('/get')
@front
def get():
    """
    Get all same type proxy
    :param type: type
    :return:
    """
    type = request.args.get("type", "").lower()
    return {'type': type, 'proxy': rh.get(type)}

@app.route('/random')
@front
def get_random():
    """
    Get a high score random proxy
    :param type: type
    :return:
    """
    type = request.args.get("type", "").lower()
    return {'proxy': rh.random(type)}

@app.route('/delete')
@front
def delete():
    return "No run for now"

@app.route('/all')
def get_all():
    """
    Get all proxy from proxy pool
    :return:
    """
    return {'type': 'all', 'proxy': rh.all()}

@app.route('/count')
@front
def get_count():
    """
    Get all proxy count or get all the same type proxy count
    :param type: type
    :return:
    """
    type = request.args.get("type", "").lower()
    return {'allCount': rh.all_count(), 'typeCount': rh.type_count(type)} if type else {'allCount': rh.all_count()}


def runFlask():
    app.run(host=API_HOST, port=API_PORT)


if __name__ == '__main__':
    runFlask()