from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import json
import boto3
from botocore.exceptions import ClientError
print('Loading function')


def lambda_handler(event, context):
	invokelam=boto3.client("lambda",region_name="ap-south-1")
 #   #print("Received event: " + json.dumps(event, indent=2))
	message = event['Records'][0]['Sns']['Message']
	y = json.loads(message)
	acc=str(y["acc"])
	amnt=int(y["amnt"])
	print("This is " , type(amnt),type(acc))
	AccDb=boto3.resource("dynamodb")
	table=AccDb.Table("Accounts_uday")
	try:
		response = table.get_item(
			Key={
				"acc":acc
				}
				)
		item = response['Item']
		new_val=item['balance']+amnt
		response1 = table.update_item(
			Key={
				"acc":acc
				},
				UpdateExpression='SET balance = :val1',
				ExpressionAttributeValues={
					':val1': new_val
				}
			)
		response = table.get_item(
			Key={
				"acc":acc
			}
			)
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		item = response['Item']
	# print(response['balance'])
	url='http://******************/****/****' #Hidden for security purposes
	resp=requests.get(url)
	words=[]
	if resp.status_code==200: 
		print(resp)
		print("Successfully Accessed Web Page " + str(resp)) 
		resp=str(resp.content)
		words=resp.split(">")
		email=words[1].split('"')
		add=email[0].strip()
	else: 
		print(resp)
		print("Error while accessing webpage" + str(resp))
	print(add)
	print(type(add))
	payload={
		  "to": add,
		  "from": "udaysrivastava0@gmail.com",
		  "subject": "Hello Sir"+str(amnt)
			}
	resp=invokelam.invoke(FunctionName="smsTry",InvocationType="Event",Payload=json.dumps(payload))
