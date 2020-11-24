from flask import Flask, request

import requests

app = Flask(__name__)

@app.route('/')
def main():
    return 'test'

#test functionality for getting/posting info to/from Ryu
@app.route('/test', methods =['GET', 'POST'])
def test():
    if request.method == 'POST' :
        return 'POST'
    else:
        return 'GET'
