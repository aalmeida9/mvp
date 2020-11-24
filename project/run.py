# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from werkzeug.serving import run_simple
#
# from frontend import create_app as app_frontend_create_app
# frontend = app_frontend_create_app()
#
# from bc import create_app as app_bc_create_app
# bc = app_bc_create_app()
#
#
# application = DispatcherMiddleware(
#     frontend, {
#     '/bc': bc
# })
#
# if __name__ == '__main__':
#     run_simple(
#         hostname='localhost',
#         port=5000,
#         application=application,
#         use_reloader=True,
#         use_debugger=True,
#         use_evalex=True)

from frontend import app

app.run(debug=True)
