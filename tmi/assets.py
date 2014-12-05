from flask.ext.assets import Environment, Bundle

from tmi.core import app

assets = Environment(app)

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

assets.register('js', js_assets)
assets.register('css', css_assets)
