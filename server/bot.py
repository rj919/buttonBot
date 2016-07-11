__author__ = 'rcj1492'
__created__ = '2016.07'
__license__ = 'MIT'

from textblob import TextBlob
from jsonmodel.validators import jsonModel
from time import time

class botClient(object):

    def __init__(self, message_schema, case_schema, request_schema, response_schema, question_sequence):

        self.messageModel = jsonModel(message_schema)
        self.caseModel = jsonModel(case_schema)
        self.requestModel = jsonModel(request_schema)
        self.responseModel = jsonModel(response_schema)
        self.questions = question_sequence

    def analyze(self, **kwargs):

        outgoing_messages = []

        case_fields = self.caseModel.ingest(**{})
        message_history = []
        report_id = ''
        for key, value in kwargs.items():
            if key == 'case_fields':
                case_fields = value
            elif key == 'message_history':
                message_history = value
            elif key == 'report_id':
                report_id = value

    # construct a sequence for questions based upon model declaration
        outer_sequence = []
        outer_seq_order = []
        civilian_sequence = []
        civilian_seq_order = []
        officer_sequence = []
        officer_seq_order = []
        incident_sequence = []
        incident_seq_order = []

        for key, value in self.caseModel.schema.items():
            component_key = '.%s' % key
            outer_sequence.append(component_key)
            if isinstance(value, list):
                component_key = '%s[0]' % component_key
                element_dict = self.caseModel.schema[key][0]
            else:
                element_dict = self.caseModel.schema[key]
            for k, v in element_dict.items():
                sub_component_key = '%s.%s' % (component_key, k)
                if key == 'civilians':
                    civilian_sequence.append(sub_component_key)
                elif key == 'officers':
                    officer_sequence.append(sub_component_key)
                elif key == 'incident':
                    incident_sequence.append(sub_component_key)

        seq_list = [ outer_sequence, officer_sequence, civilian_sequence, incident_sequence ]
        order_list = [ outer_seq_order, officer_seq_order, civilian_seq_order, incident_seq_order ]

        for i in range(len(seq_list)):
            for j in range(len(seq_list[i])):
                component_criteria = self.caseModel.keyMap[seq_list[i][j]]
                seq_position = None
                if 'field_metadata' in component_criteria.keys():
                    if 'sequence_order' in component_criteria['field_metadata'].keys():
                        seq_position = component_criteria['field_metadata']['sequence_order']
                if isinstance(seq_position, int):
                    order_list[i].append(seq_position)
                else:
                    order_list[i].append(len(seq_list[i]))

        from copy import deepcopy
        seq_copy = deepcopy(seq_list)
        for i in range(len(seq_copy)):
            ordered_list = []
            sort_list = sorted(zip(order_list[i],seq_copy[i]))
            for (y,x) in sort_list:
                ordered_list.append(x)
            for j in range(len(seq_list[i])):
                seq_list[i][j] = ordered_list[j]

        # print(incident_sequence)

    # retrieve report completion data from memory (or create)
        from labpack.platforms.localhost_client import localhostClient
        localHost = localhostClient()
        report_path = './data'
        report_key_map = {}
        report_list = localHost.find(query_filters=[ {'.file_name': { 'must_contain': [ report_id ] } } ], query_root=report_path)
        if report_list:
            file_path = report_list[0]
            file_data = open(file_path, 'rt')
            report_key_map = json.loads(file_data.read())
        metadata_fields = {
            'completion_status': '',
            'completion_time': 0,
            'active_field': False
        }
        if not report_key_map:
            for key, value in self.caseModel.keyMap.items():
                report_key_map[key] = value
                if 'field_metadata' not in report_key_map[key].keys():
                    report_key_map[key]['field_metadata'] = {}
                    for k, v in metadata_fields.items():
                        report_key_map[key]['field_metadata'][k] = v
                for k, v in metadata_fields.items():
                    if k not in report_key_map[key]['field_metadata'].keys():
                        report_key_map[key]['field_metadata'][k] = v
            file_path = '%s/%s.json' % (report_path, report_id)
            file_data = json.dumps(report_key_map).encode('utf-8')
            with open(file_path, 'wb') as f:
                f.write(file_data)
                f.close()

        print(report_key_map)

        def message_builder(seq_list, report_key_map, case_fields):
            new_message = {
                'dt': time(),
                'sender': 'ombotsman'
            }
            new_message = self.messageModel.ingest(**new_message)
            for i in seq_list[0]:
                if report_key_map[i]['value_datatype'] == 'list':
                    if not self.caseModel._walk(i, case_fields):
                        new_message['text'] = report_key_map[i]['field_metadata']['initial_question']
                        return new_message

                    elif not report_key_map[i]['field_metadata']['completion_status']:
                        new_message['text'] = report_key_map[i]['field_metadata']['followup_question']
                        return new_message
            return new_message

        outgoing_messages.append(message_builder(seq_list, report_key_map, case_fields))

        print(outgoing_messages)
        # print(case_fields)
        # print(message_history)



        return outgoing_messages, case_fields

if __name__ == '__main__':
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
    bot = botClient(**bot_kwargs)
    nlp_request = json.loads(open('models/nlp-request.json').read())
    test_civilian = nlp_request['details']['case_fields']['civilians'][0]
    test_description = nlp_request['details']['case_fields']['incident']['description']
    test_officer = nlp_request['details']['case_fields']['officers'][0]
    test_kwargs = nlp_request['details']
    bot.analyze(**test_kwargs)
    # print(bot.caseModel.keyMap)
    # print(bot.questions)