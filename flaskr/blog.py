#### source link: https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
## this file is a blueprint of blog table#########################
## this file is kind of view.py file , but only for blog table.
## so, this file has all request route related to blog table that application needs.
## Application: CRUD FOR Blogs with showing all bogs with creator user
"""
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint. 
Then the blueprint is registered with the application when it is available in the factory function.
"""
####################### IMPORT NEEDED MODULES ###################################
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required # import this function from auth.py, so can call in blog apps 
from flaskr.db import get_db

#############################################################################################
###################### CREATE BLUEPRINT : AUTH #############################################
"""This creates a Blueprint named 'auth'. 
Like the application object, the blueprint needs to know where it’s defined, so __name__ is passed as the second argument. 
The url_prefix is not present here, so all view function will be called with same url instead of blog/function_url"""

bp = Blueprint('blog', __name__)
############################################################################################
######################## VIEWS FOR BLUEPRINT Blog #######################################

######################---------- VIew: index: for showing list of blogs---------------####
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(   # join sql
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

################## -----------Create: for creating the blog--------------------###
### user need to be logged in to create blog------------###
@bp.route('/create', methods=('GET', 'POST'))
@login_required # this make sure the user is logged in by calling the login_requred function from auth
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

##############----------------INTERNAL FUNCTION: GET_POST------------------##############
### this function will be called from update and delete blog view
### to make sure that login user is the author of this post or not
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

############-----------------------UPDATE VIEW FUNCTION--------------####################
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required # this make sure the user is logged in by calling the login_requred function from auth
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)
########################---------------DELETE BLOG VIEW ------------------###################
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required # this make sure the user is logged in by calling the login_requred function from auth
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
 