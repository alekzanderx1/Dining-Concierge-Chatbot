import json
from dynamodb_json import json_util as json2
import boto3
from datetime import datetime
from decimal import Decimal

session = boto3.Session(
    aws_access_key_id="<ACCESS_KEY>",
    aws_secret_access_key="<SECRET_KEY>"
)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('yelp-restaurants') # update table name accordingly

keys_to_preserve = ["name","rating","review_count"]

# Read the JSON file
with open('mexican.json') as json_data: # update input file name based on category
	items = json.load(json_data)
	result = []
	for item in items:
		res = {}
		for key in keys_to_preserve:
			res[key] = str(item[key])
		res['zipcode'] = item['location']['zip_code']
		res['address'] = " ".join(item['location']['display_address'])
		res['insertedAtTimestamp'] = str(datetime.now())
		res['businessId'] = item['id']
		result.append(res)	

	for item in result:
		table.put_item(Item=item)