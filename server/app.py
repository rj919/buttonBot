__author__ = 'rcj1492'
__created__ = '2016.06'
__license__ = 'MIT'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# construct flask app object
from flask import Flask, request, jsonify, render_template
flask_args = {
    'import_name': __name__
}
app = Flask(**flask_args)

# initialize logging and debugging
import logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)
app.config['ASSETS_DEBUG'] = False

# construct request deconstructor
from time import time
from server.methods.request_handler import requestDeconstructor

# construct botClient
from server.bot import botClient
import json
bot_kwargs = {
    'message_schema': json.loads(open('models/messages-model.json').read()),
    'case_schema': json.loads(open('models/case-fields-model.json').read()),
    'question_sequence': json.loads(open('models/question-sequence.json').read())
}
bot_kwargs['request_schema'] = {
    'schema': {
        'report_id': '78145cklsf',
        'case_fields': bot_kwargs['case_schema']['schema'],
        'message_history': [
            bot_kwargs['message_schema']['schema']
        ]
    }
}
bot_kwargs['response_schema'] = {
    'schema': {
        'report_id': '78145cklsf',
        'case_fields': bot_kwargs['case_schema']['schema'],
        'outgoing_messages': [
            bot_kwargs['message_schema']['schema']
        ]
    }
}
case_bot = botClient(**bot_kwargs)

@app.route('/')
def dashboard_page():
    return render_template('dashboard.html'), 200

@app.route('/api/<interface_type>/<form_type>', methods=['POST'])
def api_endpoint(interface_type='', form_type=''):
    response_dict = {
        'status': 'success',
        'interface': interface_type,
        'form': form_type
    }
    # request architecture for pygmy depends upon interface
    # form schema for bot depends upon form type
    return jsonify(response_dict), 200

@app.route('/api/<request_resource>', methods=['POST'])
def api_request(request_resource=''):
    response_dict = {
        'status': 'success',
        'dt': time(),
        'details': {}
    }
    if request_resource == 'analyze':
        request_details = requestDeconstructor(request, bot_kwargs['request_schema'])
        if not request_details:
            response_dict['status'] = 'error'
        else:
            response_dict['details'] = request_details
            del response_dict['details']['message_history']
            response_dict['details']['outgoing_messages'] = []
    elif request_resource == 'response':
        response_dict['details'] = case_bot.responseModel.schema
    else:
        response_dict['details'] = case_bot.requestModel.schema
    return jsonify(response_dict), 200

@app.errorhandler(404)
def page_not_found(error):
    # app.logger.debug(error)
    return render_template('404.html'), 404

if __name__ == '__main__':
    config_args = {
        'host': '0.0.0.0',
        'port': 5000
    }
    app.run(**config_args)

