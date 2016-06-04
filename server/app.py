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

