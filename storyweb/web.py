from flask import render_template

from storyweb.core import app


@app.route('/')
def home():
    return render_template("index.html")
