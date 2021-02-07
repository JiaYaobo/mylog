from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_pagedown import PageDown

boostrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()
pagedown = PageDown()


@login_manager.user_loader
def load_user(user_id):
    from JiaLog.models import Admin
    user = Admin.query.get(int(user_id))
    return user