__author__ = 'rcj1492'
__created__ = '2016.07'
__license__ = 'MIT'

from textblob import TextBlob
from jsonmodel.validators import jsonModel

class botClient(object):

    def __init__(self, message_schema, case_schema, request_schema, response_schema, question_sequence):

        self.messageModel = jsonModel(message_schema)
        self.caseModel = jsonModel(case_schema)
        self.requestModel = jsonModel(request_schema)
        self.responseModel = jsonModel(response_schema)
        self.questions = question_sequence

    def analyze(self, **kwargs):

        outgoing_messages = []
        case_fields = {}

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
            'case_fields': bot_kwargs['case_schema']['schema'],
            'message_history': [
                bot_kwargs['message_schema']['schema']
            ]
        }
    }
    bot_kwargs['response_schema'] = {
        'schema': {
            'case_fields': bot_kwargs['case_schema']['schema'],
            'outgoing_messages': [
                bot_kwargs['message_schema']['schema']
            ]
        }
    }
    bot = botClient(**bot_kwargs)
    # print(bot.caseModel.keyMap)
    # print(bot.questions)
    details = {
        "case_fields": {
                           "civilians": [
                               {
                                   "birth_date": "",
                                   "business_phone": "",
                                   "city": "New York City",
                                   "complaintant_or_not": True,
                                   "email_address": "rcjames@gmail.com",
                                   "first_name": "Richard",
                                   "gender": "",
                                   "home_phone": "2123476574",
                                   "last_name": "James",
                                   "mobile_carrier": "Verizon",
                                   "mobile_phone": "9178565357",
                                   "permission_to_text": True,
                                   "race": "",
                                   "relation_to_victim": "",
                                   "sexual_orientation": "",
                                   "state": "",
                                   "street_address": "32 Gansevoort St",
                                   "victim_or_not": True,
                                   "witness_or_not": True,
                                   "zip_code": "10014"
                               }
                           ],
                           "incident": {
                               "borough": "",
                               "date": "",
                               "description": "I was waiting outside Penn Station to meet a friend, when an officer approached me and asked for my ID. I told him I wasn't doing anything illegal and he began to intimidate me and invade my personal space. He eventually started swearing and screaming obscenities at me before my friend arrived and we left.",
                               "location": "Outside Penn Station on 8th Ave",
                               "media": [
                                   "https://ombotsman.bot/3dnc9J"
                               ]
                           },
                           "officers": [
                               {
                                   "car_marked": "",
                                   "car_number": "2855",
                                   "description": "White male, mid-40's with salt and pepper hair, around 6'2\" and medium build.",
                                   "first_name": "Jerry",
                                   "foot_or_car": "",
                                   "last_name": "Seinfeld",
                                   "license_plate_number": "749111",
                                   "plainclothes_or_uniform": "",
                                   "precinct_command": "13th",
                                   "race": "",
                                   "rank": "",
                                   "role": "Instigator of incident - he was the one who began intimidating and cursing me out.",
                                   "sex": "",
                                   "shield_number": "6386",
                                   "subject_or_witness": ""
                               }
                           ]
                       },
        "message_history": [
            {
                "dt": 14000000,
                "media": "",
                "options": [
                    "skip"
                ],
                "sender": "id",
                "text": "",
                "url": ""
            }
        ]
    }
    validated = bot.requestModel.ingest(**details)
    print(bot.requestModel.schema)