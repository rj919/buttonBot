__author__ = 'rcj1492'
__created__ = '2016.06'
__license__ = 'MIT'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, session, jsonify, url_for, render_template
flask_args = {
    'import_name': __name__
}
app = Flask(**flask_args)

@app.route('/')
def dashboard_page():
    return render_template('dashboard.html'), 200

@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404

if __name__ == '__main__':
    config_args = {
        'host': '0.0.0.0',
        'port': 5000
    }
    app.run(**config_args)

