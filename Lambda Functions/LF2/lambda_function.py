import json
import boto3
import requests
from requests_aws4auth import AWS4Auth

esHost= '<ES_HOST>'
region = "us-east-1"
index = "restaurants"

def getdatafromDBTable(table, key):
    response = table.get_item(Key={'businessId':key}, TableName='yelp-restaurants')
    name=response['Item']['name']
    location=response['Item']['address']
    return '{} located at {}'.format(name,location)
    
def getRestaurantsfromES(cuisine):
    service = "es"
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    url = esHost + '/' + index + '/_search'
    query = {"query": {"match": {"category": cuisine }}}
    headers = { "Content-Type": "application/json" }
    res = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    res = res.text
    res = json.loads(res)
    res = res["hits"]["hits"]
    return res
    
def sendSESMail(message,email):
    ses_client = boto3.client('ses', region_name=region)
    response = ses_client.send_email(
        Source='syed.ahmad@nyu.edu',
        Destination={
            'ToAddresses': [email]
        },
        ReplyToAddresses=['syed.ahmad@nyu.edu'],
        Message={
            'Subject': {
                'Data': 'NYU Dining Recommendation Bot',
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': message,
                    'Charset': 'utf-8'
                },
                'Html': {
                    'Data': message,
                    'Charset': 'utf-8'
                }
            }
        }
    )
    
def lambda_handler(event, context):
    sqsUrl = "<SQS_URL>"
    sqs_client = boto3.client("sqs", region_name=region)
    response = sqs_client.receive_message(
        QueueUrl=sqsUrl,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10,
        AttributeNames=['All'],
        MessageAttributeNames=[
        'Name','Email','Cuisine','Location','NumberOfPeople','DiningDate','DiningTime'
        ]
    )
    numOfMessages = len(response.get('Messages', []))
    
    if numOfMessages > 0:
        for message in response.get("Messages", []):
            messageAttributes = message['MessageAttributes']
            # read parameters from event
            name = messageAttributes['Name']['StringValue']
            cuisine = messageAttributes['Cuisine']['StringValue']
            date = messageAttributes['DiningDate']['StringValue']
            time = messageAttributes['DiningTime']['StringValue']
            location = messageAttributes['Location']['StringValue']
            numPeople = messageAttributes['NumberOfPeople']['StringValue']
            # phone = messageAttributes['PhoneNumber']['StringValue']
            email = messageAttributes['Email']['StringValue']
        
            # call elastisearch to find random restaurants with given cuisine type
            elastisearchResults = getRestaurantsfromES(cuisine)
            
            # call dynamodb to elicit extra info for each restaurant identified
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('yelp-restaurants')
            restaurantDetails=[]
            count = 0
            for i in elastisearchResults:
                count += 1
                rid = i['_source']['RestaurantID']
                rest=getdatafromDBTable(table, rid)
                rest = str(count) + ". " + rest
                restaurantDetails.append(rest)
                # limiting number of suggestions to 5
                if count == 5:
                    break
            
            # prepare response for user
            responseToUser = "Hello {}! Here are my {} restaurant suggestions for {} people, for {} at {}:<br> ".format(str(name),str(cuisine),str(numPeople),str(date),str(time)) 
            responseToUser += ",<br> ".join(restaurantDetails)
            responseToUser += ".<br> Enjoy your meal!"
        
            sendSESMail(responseToUser,email)
            sqs_client.delete_message(
                QueueUrl= sqsUrl,
                ReceiptHandle=message['ReceiptHandle']
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully')
        }
    else:
         return {
            'statusCode': 200,
            'body': json.dumps('No messages present in SQS queue')
        }
