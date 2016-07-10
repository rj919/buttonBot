__author__ = 'rcj1492'
__created__ = '2016.07'
__license__ = 'MIT'

from textblob import TextBlob
from jsonmodel.validators import jsonModel

class botClient(object):

    def __init__(self, message_schema, case_schema, request_schema, response_schema):

        self.messageModel = jsonModel(message_schema)
        self.caseModel = jsonModel(case_schema)
        self.requestModel = jsonModel(request_schema)
        self.responseModel = jsonModel(response_schema)

    def analyze(self, **kwargs):

        outgoing_messages = []
        case_fields = {}

        return outgoing_messages, case_fields

if __name__ == '__main__':
    import json
    message_schema = json.loads(open('models/messages-model.json').read())
    case_schema = json.loads(open('models/case-fields-model.json').read())
    request_schema = {
        'schema': {
            'case_fields': case_schema['schema'],
            'message_history': [
                message_schema['schema']
            ]
        }
    }
    response_schema = {
        'schema': {
            'case_fields': case_schema['schema'],
            'outgoing_messages': [
                message_schema['schema']
            ]
        }
    }
    bot = botClient(message_schema, case_schema, request_schema, response_schema)
    print(bot.caseModel.keyMap)