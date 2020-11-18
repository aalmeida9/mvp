from flask import Flask, request

def create_app():
    app_name = 'frontend'
    print('app_name = {}'.format(app_name))

    # create app
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/")
    def hello():
        return 'Hello ' + app_name + '! request.url = ' + request.url
    
    # return app
    return app
