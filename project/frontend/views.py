from frontend import app
#import requests

@app.route("/")
def hello():
        return 'Hello ' #+ '! request.url = ' + request.url
