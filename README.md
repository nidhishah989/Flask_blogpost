# Flask_blogpost
# source link:
[link] https://flask.palletsprojects.com/en/2.0.x/tutorial/

# Project Detail:
  This project is about users and their blogs
   Database: sqlite3
   modules required to run this application: Python, Flask( other required one install with Flask)
   main part: _init_py : for setting of application, database connection, importing schema of database, importing the blueprints with view and decorator functions.

# file structure for templates:
   the templates main folder
   base.html for further inheritance
   two folders : 
              1) auth (named base on blueprint name) (include html files related views functions in that blueprint)
              2) blog (named base on blueprint name) (include html files related views functions in that blueprint)

# INSTALL APP AS PACKAGE:
   pip install -e . (SETUP.PY and MANIFEST.in)

# EXTRA WORK FOR FUTURE:
    -- A detail view to show a single post. Click a post’s title to go to its page.
    -- Like / unlike a post.
    -- Comments.
    -- Tags. Clicking a tag shows all the posts with that tag.
    -- A search box that filters the index page by name.
    -- Paged display. Only show 5 posts per page.
    -- Upload an image to go along with a post.
    -- Format posts using Markdown.
    -- An RSS feed of new posts.
