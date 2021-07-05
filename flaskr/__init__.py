# this file is used to setup the application 
#with configuration, registration, and other setup

#we use <application factory> function to tell server which 
#folder is a package of this application

import os
from flask import Flask

#this function is <application factory>
def create_app(test_config=None):
    #create and configure the app
    #following line create flask instance
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #Load the instance config, if it exits, when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)
    
    #ensure the instace folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    return app