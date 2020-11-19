from flask import Flask, request
#config: https://exploreflask.com/en/latest/configuration.html

app = Flask(__name__)

from frontend import views
