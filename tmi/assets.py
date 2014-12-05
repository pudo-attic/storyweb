from flask.ext.assets import Bundle

from tmi.core import assets

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
