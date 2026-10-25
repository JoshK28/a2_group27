# import flask - from 'package' import 'Class'
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# local AI search for loading models
encoder = None
if os.getenv('AI_SEARCH_ENABLED', '1') == '1':
      from sentence_transformers import SentenceTransformer

      try:
          encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', local_files_only=True)
      except Exception:
          encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    # Should be set to false in a production environment
    app.debug = False
    app.secret_key = 'somesecretkey'
    # set the app configuration data 
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sitedata.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ db_path
    # initialise db with flask app
    db.init_app(app)

    Bootstrap5(app)
    
    # initialise the login manager
    login_manager = LoginManager()
    
    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    # Importing inside the create_app function avoids circular references
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
       return db.session.scalar(db.select(User).where(User.id==user_id))

    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import events
    app.register_blueprint(events.event_bp)

    # Show 404 error page when event can't be found.
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    # Show 500 error page when something breaks on server
    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template('500.html'),500
    
    return app