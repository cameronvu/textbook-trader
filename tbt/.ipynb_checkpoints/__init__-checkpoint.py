import os

from flask import Flask

'''
    This acts as the application factory for what will be our app, Textbook Trader
    This python file also sets up the directory as a package
'''

def create_app(test_config=None):
    # create and configure the app
    '''
        This function is responsible for creating an application instance of the Flask class
        The return is a Flask object called app
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import listing
    app.register_blueprint(listing.bp)
    app.add_url_rule('/', endpoint='index')

    
    return app

    

