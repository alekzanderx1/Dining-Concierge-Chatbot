import json
import random
import boto3


def lambda_handler(event, context):
    requestmsg = ''
    for msg in event['messages']:
        requestmsg += msg['unstructured']['text']
    client = boto3.client('lexv2-runtime')
    response = client.recognize_text(
    botId='UTAGENYFXA',
    botAliasId='GUUA7YGJ5M',
    localeId='en_US',
    sessionId="test_session_1",
    text=requestmsg)

    return {
        'statusCode': 200,
        'messages':[{
            "type":'unstructured',
            "unstructured":{
                    'text': response['messages'][0]['content']
                }
            }]
        }