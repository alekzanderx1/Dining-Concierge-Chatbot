Steps to download data from yelp and upload to Elasticsearch and DynamoDB:

	1. Create a Yelp fusion account and obtain API Key

	2. Use the Yelp API key to run "YelpDataDownload.py" script with appropriate category values to download data as json.

	3. Run "DynamoDBImport.py" to upload data to DynamoDB for each category.

	4. Run "ElasticsearchJSONGenerator.py" for each category to generate Elasticserach campatible JSON for data upload.

	5. Run the below command to upload json files generated above to elasticsearch - 

	curl -XPOST -u "username:password" "<ES_URL>/_bulk" --data-binary @categoryJSON.json -H "Content-Type: application/json"

