from flask import g, redirect, url_for, request
from wtforms import PasswordField, TextAreaField
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from tmi.core import app, db, app_name
from tmi.model import User, Card, Reference


class AppModelView(ModelView):
    
    def is_accessible(self):
        if g.user is None:
            return False
        if not g.user.is_active():
            return False
        if not g.user.is_admin:
            return False
        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))


class UserAdmin(AppModelView):
    column_list = [
        'email',
        'display_name',
        'active',
        'is_admin',
        'is_editor'
    ]
    column_exclude_list = ['password_hash']

    form_excluded_columns = [
        'password_hash',
        'blocks',
        'created_at',
        'updated_at',
        'active'
    ]

    column_labels = {
        'email': 'E-Mail',
        'is_admin': 'Administrator',
        'is_editor': 'Editor',
        'display_name': 'Name'
    }

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password = PasswordField('Password')
        return form_class

    def on_model_change(self, form, model, is_created):
        model.password = form.password.data


class CardAdmin(AppModelView):
    column_list = [
        'title',
        'category',
        'date'
    ]

    form_overrides = {
        'text': TextAreaField
    }
    
    form_excluded_columns = [
        'created_at',
        'updated_at'
    ]

    column_labels = {
        'text': 'Text'
    }

    def on_model_change(self, form, model, is_created):
        pass


class ReferenceAdmin(AppModelView):
    column_list = [
        'citation',
        'source'
    ]

    #form_overrides = {
    #    'text': TextAreaField
    #}
    
    form_excluded_columns = [
        'created_at',
        'updated_at'
    ]

    column_labels = {
        'source_url': 'Source Web Link',
        'url': 'Web Link'
    }

    def on_model_change(self, form, model, is_created):
        pass

admin = Admin(app, name=app_name)
admin.add_view(UserAdmin(User, db.session))
admin.add_view(CardAdmin(Card, db.session))
admin.add_view(ReferenceAdmin(Reference, db.session))
