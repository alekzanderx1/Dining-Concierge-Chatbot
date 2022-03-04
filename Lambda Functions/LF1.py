import json
import random
import decimal 
import boto3
import logging
import datetime
from datetime import date,timedelta
import dateutil.parser
import time
import os
import math
import re


queue_url = '<QUEUE_URL>'
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def checkEmail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']
    
def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        if 'interpretedValue' in slots[slotName]['value']:
            return slots[slotName]['value']['interpretedValue']
        else:
            return slots[slotName]['value']['originalValue']
    else:
        return None    

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}

def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def sendmsgtosqs(intent_request):
    location = get_slot(intent_request,"location")
    cuisineType = get_slot(intent_request, 'cuisine')
    date = get_slot(intent_request, 'date')
    time = get_slot(intent_request, 'time')
    numPeople = get_slot(intent_request, 'peopleCount')
    name = get_slot(intent_request, 'name')
    email = get_slot(intent_request, 'email')
    
    # Sending the data to sqs queue
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageGroupId="dining_bot",
        MessageDeduplicationId="dining_dupli",
        MessageAttributes = {
            'Cuisine': {
                'DataType': 'String',
                'StringValue': str(cuisineType)
            },
            'Location': {
                'DataType': 'String',
                'StringValue': str(location)
            },
            'Name': {
                'DataType': 'String',
                'StringValue': str(name)
            },
            'Email': {
                'DataType': 'String',
                'StringValue': str(email)
            },
            'NumberOfPeople': {
                'DataType': 'String',
                'StringValue': str(numPeople)
            },
            'DiningDate': {
                'DataType': 'String',
                'StringValue': str(date)
            },
            'DiningTime': {
                'DataType': 'String',
                'StringValue': str(time)
            }
        },
        MessageBody= 'User request information from Lex'
    )

def buildValidationMessage(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot
        }
    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

def delegate(session_attributes,slots):
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate'
            },
            'intent':{
                "name": "DiningSuggestionsIntent",
                'slots':slots
            }
        }
    }

def validateSlots(location,cuisineType,date,time,numPeople,name,email):
    locs = ['nyc','manhattan','new york']
    if location is not None and location.lower() not in locs:
        return buildValidationMessage(False,
                                       'location',
                                       'We are not supporting services in {}. Please enter neighborhood in Manhattan'.format(location))
    
    cuisines=['indian','mexican','japanese','french','cafes','italian']
    if cuisineType is not None and cuisineType.lower() not in cuisines:
        return buildValidationMessage(False,
                                       'cuisine',
                                       'We are not supporting services for {} food. Please chose among Indian, Mexican, Japanese, French, Cafes, and Italian'.format(cuisineType))
    
    if date is not None:
        if not isValidDate(date):
            return buildValidationMessage(False, 'date', 'Invalid date! Sample input format: Today')
        elif datetime.datetime.strptime(date, '%Y-%m-%d').date() < datetime.date.today():
            return buildValidationMessage(False, 'date', 'The day has already passed ;)  Please enter a valid date.')
    if numPeople is not None:
        if int(numPeople) <=0 or int(numPeople)>10:
            return buildValidationMessage(False,'peopleCount',"We can only accommodate 0-10 people! Please enter again.")
    if time is not None:
        if len(time) != 5:
            return buildValidationMessage(False, 'time', "Invalid time! Enter in proper format(eg 02:00 PM)")
        if datetime.datetime.strptime(date, '%Y-%m-%d').date() == datetime.date.today():
            if (int(time[0:2])<=(datetime.datetime.now().hour)):
                return buildValidationMessage(False, 'time', "Invalid time! Enter Time after the present time")
        for i in range(len(time)):
            if i == 2:
                if time[i] != ":":
                    return buildValidationMessage(False, 'time', "Invalid time! Enter in proper format(eg 02:00 PM)")
            else:
                if not time[i].isalnum():
                    return buildValidationMessage(False, 'time', "Invalid time!Enter in proper format(eg 02:00 PM)")

        hour, minute = time.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            return buildValidationMessage(False, 'time', "Invalid time!")
    
    if email is not None:
        if not checkEmail(email):
            return buildValidationMessage(False, 'phoneNumber', "Please enter a valid Email address!")
            
            
    return buildValidationMessage(True, None, None)

def isValidDate(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False
        
def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan') 

def elicitSlot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionState':{
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit
                },
            'intent':{
                    'name': intent_name,
                    'slots': slots
                }
            
            
        },
        'messages':[message],
    }
    
def DiningSuggestionsIntent(intent_request):
    session_attributes = get_session_attributes(intent_request)
    location = get_slot(intent_request,"location")
    cuisineType = get_slot(intent_request, 'cuisine')
    date = get_slot(intent_request, 'date')
    time = get_slot(intent_request, 'time')
    numPeople = get_slot(intent_request, 'peopleCount')
    name = get_slot(intent_request, 'name')
    email = get_slot(intent_request, 'email')
    
    if intent_request['invocationSource'] == 'DialogCodeHook':
        slots = get_slots(intent_request)
        validationResultForSlots = validateSlots(location,cuisineType,date,time,numPeople,name,email)
        
        if not validationResultForSlots['isValid']:
                slots[validationResultForSlots['violatedSlot']] = None
                print(validationResultForSlots['violatedSlot'])
                return elicitSlot(session_attributes,
                                        intent_request['interpretations'][0]['intent']['name'],
                                        slots,
                                        validationResultForSlots['violatedSlot'],
                                        validationResultForSlots['message'])
    
        return delegate(session_attributes, get_slots(intent_request))
   
    sendmsgtosqs(intent_request)
    return close(intent_request, 
                    session_attributes,
                    'Fulfilled',
                    {'contentType': 'PlainText',
                    'content': 'Thank you! You will receive recommendations to the Email: {} later.'.format(email)}) 

def GreetingIntent(intent_request):
    session_attributes = get_session_attributes(intent_request)
    message =  {
            'contentType': 'PlainText',
            'content': "Hi! How Can I Help you?"
        }
    return elicitIntent(session_attributes, message)   
    
def ThankYouIntent(intent_request):
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    return close(
        intent_request,
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Happy to help. Have a great day!'
        }
    )
    
def elicitIntent(session_attributes, message):
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitIntent',
            }
        },
        'messages': [message]
    }
    
def dispatch(intent_request):
    response = None
    print(intent_request)
    intent_name = intent_request['interpretations'][0]['intent']['name']
    if intent_name == 'DiningSuggestionsIntent':
        return DiningSuggestionsIntent(intent_request)
    elif intent_name == 'ThankYouIntent':
        return ThankYouIntent(intent_request)
    elif intent_name == 'GreetingIntent':
        return GreetingIntent(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')

def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    response = dispatch(event)
    return response