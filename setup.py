###############################################################################################
####################### WHY SETUP.py and MANIFEST.in ???? ##################################
#Making your project installable means that you can build a distribution file and install that in another environment,
#This makes deploying your project the same as installing any other library, 
#so you’re using all the standard Python tools to manage everything.
#############################################################################################
############## WHAT IS IN SETUP.py ??? #####################################################
""" packages tells Python what package directories (and the Python files they contain) to include. 
find_packages() finds these directories automatically so you don’t have to type them out. 
To include other files, such as the static and templates directories, include_package_data is set.
 Python needs another file named MANIFEST.in to tell what this other data is."""

 #############################################################################
 #########for MANIFEST.IN FILE COMMENTS ####################################
 #This tells Python to copy everything in the static and templates directories, 
 #and the schema.sql file, but to exclude all bytecode files.
 #############################################################################

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

#################for tests ########################
# [tool:pytest]
# testpaths = tests

# [coverage:run]
# branch = True
# source =
#     flaskr