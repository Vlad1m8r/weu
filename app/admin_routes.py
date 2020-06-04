from app.models import *
from app import db
from app import app
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_security import SQLAlchemyUserDatastore
from flask import render_template, flash, redirect, url_for, request
from flask_admin import AdminIndexView
from flask_admin import Admin


class Mix:
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        for role in current_user.roles:
            if role == 'admin':
                return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class AdminView(Mix, ModelView):
    pass


class HomeAdminView(Mix, AdminIndexView):
    pass


admin = Admin(app, name='WEU', template_mode='bootstrap3', index_view=HomeAdminView(), url="/")

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Thing, db.session))
