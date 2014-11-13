from flask import g, redirect, url_for, request
from wtforms import PasswordField
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from storyweb.core import app, db, app_name
from storyweb.model import User


class AppModelView(ModelView):
    
    def is_accessible(self):
        if g.user is not None and g.user.is_active():
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))


class UserAdmin(AppModelView):
    column_list = [
        'email',
        'display_name',
        'active'
    ]
    column_exclude_list = ['password_hash']

    form_excluded_columns = [
        'password_hash',
        'active'
    ]

    column_labels = {
        'email': 'E-Mail',
        'display_name': 'Name'
    }

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password = PasswordField('Password')
        return form_class

    def on_model_change(self, form, model):
        model.password = form.password.data


admin = Admin(app, name=app_name)
admin.add_view(UserAdmin(User, db.session))
