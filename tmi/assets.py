from flask import Flask
from flask.ext.assets import Environment, Bundle

js_assets = Bundle(
    "js/app.js",
    #filters='uglifyjs',
    output='assets/app.js'
)

css_assets = Bundle(
    'style/app.less',
    filters='less',
    output='assets/style.css'
)

app = Flask(__name__)
assets = Environment(app)

assets.register('js', js_assets)
assets.register('css', css_assets)
