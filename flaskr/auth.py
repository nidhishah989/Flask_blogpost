#### source link: https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
## this file is a blueprint of user table#########################
## this file is kind of view.py file , but only for user table.
## so, this file has all request route related to user table that application needs.
## user -authentication::: REGISTER, LOGIN ,and LOGOUT
"""
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint. 
Then the blueprint is registered with the application when it is available in the factory function.
"""
####################### IMPORT NEEDED MODULES ###################################
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
#############################################################################################
###################### CREATE BLUEPRINT : AUTH #############################################
"""This creates a Blueprint named 'auth'. 
Like the application object, the blueprint needs to know where it’s defined, so __name__ is passed as the second argument. 
The url_prefix will be prepended to all the URLs associated with the blueprint."""

bp = Blueprint('auth', __name__, url_prefix='/auth')
############################################################################################
######################## VIEWS FOR BLUEPRINT AUTH #######################################

#############----------------- REGISTER VIEW --------------------------##########
# This will be called on url: auth/register
# Will show the Html Form and get the username and password.
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':  # POST request will be set in HTML page
        username = request.form['username'] # get username from HTML Form ,name of field match to form name
        password = request.form['password'] # get password from HTML Form ,name of field match to form name
        # call database connection
        db = get_db()
        error = None
        # validation check for requred fields.
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # check the username already exists or not in database user table . sql query..
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered." # user already there.so it is error
        # if no error happend in above code, means the user need to be register by saving data into database table
        if error is None:
            db.execute(    # execute sql squery to save new user
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

#############----------------- LOGIN VIEW --------------------------##########
# This will be called on url: auth/login
# Will show the Html Form and get the username and password.
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username'] # get username from HTML Form ,name of field match to form name
        password = request.form['password'] # get password from HTML Form ,name of field match to form name
        # connect to database       
        db = get_db()
        error = None
        # check the username is present or not
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        # if username is not present, then error as incorrect username
        if user is None:
            error = 'Incorrect username.'
        #if username is there, check password is correct or not
        # here, password check is done secretly by check_password_hash function
        #if password not correct, then error as incorrect password
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        #if username and password are correct, start the session by user id,
        #user id is same id that store for user in database
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

#############----------------- LOAD_LOGGED_IN_USER VIEW --------------------------##########
#bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested. 
#load_logged_in_user checks if a user id is stored in the session and gets that user’s data from the database, 
#storing it on g.user, which lasts for the length of the request. 
#If there is no user id, or if the id doesn’t exist, g.user will be None.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
#############----------------- LOGOUT VIEW --------------------------##########
#To log out, you need to remove the user id from the session. 
#Then load_logged_in_user won’t load a user on subsequent requests.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
##############--------------DECORATOR------------------------##########
#DECORATOR: The function that will be called from other views or when it require without a url
# This decorator is used to check the user is logged in or not.
# if user logged in , then the decorator will go back to same url from where it was requested
#otherwise the decorator redirect the login page for further requests
# this will be called when user do any CRUD operation with blog
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
################################################################################################