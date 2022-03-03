# Dining Concierge Chatbot

This is serverless, microservice-driven web application built and deployed on AWS. The chatbot sends users restaurant suggestions to their Email given a set of preferences provided through conversation. 


- Example interaction:

	User: Hello
	Bot: Hi there, how can I help?
	User: I need some restaurant suggestions.
	Bot: Great. I can help you with that. What city or city area are you looking to dine in?
	User: Manhattan
	Bot: Got it, Manhattan. What cuisine would you like to try?
	User: Japanese
	Bot: Ok, how many people are in your party?
	User: Two
	Bot: A few more to go. What date?
	User: Today
	Bot: What time?
	User: 7 pm, please
	Bot: Great. Lastly, I need your email so I can send you my findings.
	User: email@email.com
	Bot: You’re all set. Expect my suggestions shortly! Have a good day.
	User: Thank you!
	Bot: You’re welcome.
	(a few minutes later)
	User gets the following Email:
	“Hello! Here are my Japanese restaurant suggestions for 2 people, for today at 7 pm: 1.
	Sushi Nakazawa, located at 23 Commerce St, 2. Jin Ramen, located at 3183 Broadway,
	3. Nikko, located at 1280 Amsterdam Ave. Enjoy your meal!”

- AWS Services used:

	- S3
	- API Gateway
	- Lambda
	- Lex V2
	- SQS
	- SES
	- OpenSearch
	- DynamoDB
	- EventBridge
	- IAM

