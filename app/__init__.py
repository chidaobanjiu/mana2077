from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from flask_simplemde import SimpleMDE
from flask_admin import Admin
from controller.views import CustomView, CustomModelView, PostView


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
simplemde = SimpleMDE()
admin = Admin()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    simplemde.init_app(app)

    """Create the app instance via factory-method"""
    admin.init_app(app)
    """register view function 'CustomModelView' into Flask-Admin"""
    admin.add_view(CustomView(name='back home'))
    """import models here because models' import db from __init__"""
    from .models import User, Post, Role, Tag, Comment, Permission
    """register view function 'CustomModelView' into Flask-Admin"""
    admin.add_view(
        PostView(Post, db.session, name='Post'))
    models = [Role, Tag, User]
    for model in models:
        admin.add_view(
            CustomModelView(model, db.session, category='Models'))


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
