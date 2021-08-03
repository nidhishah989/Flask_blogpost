# source link: https://flask.palletsprojects.com/en/2.0.x/tutorial/database/
#################################################
# this file is to set the database connection
# the sqlite3 database is already in python. so not require other connection as other database require,
# any operation and queries will run through this database connection.
# when the work is done the connection is close
# usually, with web application. this connection used while hnadling the request 
# and close before respond send
#################################################################################################
# import database support module. for each database is different
import sqlite3
import click
# g : it is a special object to store the data that accessed through many function when a request initiated
#     so, for each request, data in g is different.
# current_app: is another special object that points to the Flask application handling the request.
from flask import current_app, g
from flask.cli import with_appcontext
#########################################################################################################################
################################### Database Connection Setup #####################################################
# whenever the request needs database connection get_db() called. 
# if the db connection is done for a request , and again called , the same connection will be used instead of making new
def get_db():
    # basically check db is connected for that g object or not. if not than connect it, otherwise return same db connection
    if 'db' not in g:
        # sqlite3.connect(): establishes a connection to the file pointed at by the DATABASE configuration key
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row: tells the connection to return rows that behave like dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db

# this function get call to close the connection to db once the request work is done.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

######################################################################################################
######################## Initiate database tables with schema file ###################################
# this function will be call to create the database tables that are created in the schema.sql file
# this function called with command line init-db ...see the init_db_command() function below.
def init_db():
    # call the get_db() function here, so, the database connection setup for further process of creating tables
    db = get_db()
    # now current_app and open_resource will find the schema.sql file, will be stored in f
    # open_resources: helps to find the location of schema.sql cause after deployment you will not sure where the file is
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# as we know click is to run command-line commands, here the command will be init-db
@click.command('init-db')
@with_appcontext
# this will call inti_db() function and send message to user as database is set. after getting a commnad init-db from user
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    # send a message in cmd window
    click.echo('Initialized the database.')

# this function will register the functions close_db and init_db_command with application
#the function paramter should be an instance of Flask , 
#but we are using application factory, so we don't have instance, for that we are using 'app' as parameter
def init_app(app):
    '''app.teardown_appcontext() ::tells Flask to call that function when cleaning up after returning the response.
       app.cli.add_command()::  adds a new command that can be called with the flask command.'''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
#################################################################################################################