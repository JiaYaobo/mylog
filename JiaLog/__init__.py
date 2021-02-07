from flask import Flask, render_template
from JiaLog.settings import config
from JiaLog.blueprints.home import home_bp
from JiaLog.blueprints.auth import auth_bp
from JiaLog.blueprints.admin import admin_bp
from JiaLog.blueprints.note import note_bp
from JiaLog.commands import register_commands
from JiaLog.extensions import db, boostrap, ckeditor, mail, moment, login_manager, pagedown, csrf
from JiaLog.models import Admin, Category, Comment
from flask_login import current_user
import click, os


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
        app = Flask('JiaLog', template_folder='templates')
        app.config.from_object(config[config_name])
        register_blueprints(app)
        register_extensions(app)
        register_template_context(app)
        register_shell_context(app)
        register_errors(app)
        register_commands(app)
        return app


def register_extensions(app):
    boostrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    pagedown.init_app(app)
    csrf.init_app(app)



def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(note_bp, url_prefix='/note')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, unread_comments=unread_comments)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500

