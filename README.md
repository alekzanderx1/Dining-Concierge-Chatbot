# Dining Concierge Chatbot

This is serverless, microservice-driven web application built and deployed on AWS. The chatbot sends users restaurant suggestions to their Email given a set of preferences provided through conversation. 


- Example interaction:

	Bot: Hi there, I'm your personal Concierge. How can I help?
	
	User: Hello
	
	Bot: Hi there, how can I help?
	
	User: I need some restaurant suggestions.
	
	Bot: Hello! May I know your name?
	
	User: James
	
	Bot: Awesome James! Can I know number of people joining you?
	
	User: 2
	
	Bot: What type of Cuisine do you wanna try James?
	
	User: Japanese
	
	Bot: A few more to go. What date?
	
	User: Today
	
	Bot: What time?
	
	User: 7 pm
	
	Bot: All set! Can I have your Email Tejas to send my finding on?
	
	User: james@gmail.com
	
	Bot: Thank you! I will send some recommendations to the Email: james@gmail.com later.
	
	User: Thank you!
	
	Bot: You’re welcome.
	
	(a few minutes later)
	
	User gets the following Email:
	
	“Hello Jammes! Here are my Japanese restaurant suggestions for 2 people, for today at 7 pm: 
	
	1. Sushi Nakazawa, located at 23 Commerce St, 
	
	2. Jin Ramen, located at 3183 Broadway,
	
	3. Nikko, located at 1280 Amsterdam Ave. 
	
	Enjoy your meal!”

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

