# coding: utf-8
from flask import Flask

import sae

app = Flask(__name__)
app.debug = False


@app.route('/generate_204', methods=('GET', 'POST', 'OPTIONS', 'DELETE', 'PUT', ))
def android_portal():
    return '', 204


@app.route('/', methods=('GET', 'POST', 'OPTIONS', ))
def index():
    return 'lo', 200


application = sae.create_wsgi_app(app)
