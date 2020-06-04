from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
# from flask_admin import AdminIndexView
# from flask_login import current_user
# from flask import redirect, url_for


app = Flask(__name__)
app.config.from_object(Config)

# class HomeAdminView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.roles[0].name == 'admin'
#
#     def inaccessible_callback(self, **kwargs):
#         return redirect(url_for('index'))
# admin = Admin(app, name='WEU', template_mode='bootstrap3', url="/chika")

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)


from app import routes, models, errors, admin_routes

