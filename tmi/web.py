from flask import render_template, redirect, request, url_for, g
from flask.ext.login import login_required, login_user
from flask.ext.login import logout_user, current_user
from restpager import Pager

from tmi.core import app
from tmi.model import User
from tmi.forms import LoginForm
from tmi.util import obj_or_404
from tmi.model.search import search_cards


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def home():
    q = {
        "query": {
            "match_all": {}
        },
        "sort": [
            {"date": {"order": "desc"}}, '_score'
        ]
    }
    pager = Pager(search_cards(q))
    return render_template("index.html", pager=pager)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            form.email.errors.append("Invalid user name or password")
        else:
            login_user(user, remember=True)
            return redirect(request.args.get("next") or url_for("home"))
    return render_template("login.html", form=form)
    

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
