import boto3
import json
from botocore.exceptions import ClientError
def lambda_handler(event, context):
  AccDb=boto3.resource("dynamodb")
  table=AccDb.Table("Accounts_uday")
  acc=str(event["acc"])
  amnt=int(event["amnt"])
  response = table.get_item(
  	Key={
  		"acc":acc
  		}
  		)
  if response.get('Item')==None:
    return("Invalid account number!!! RETRY!!!")
    print("Exiting")
    exit()
  topicArn="arn:aws:sns:ap-south-1:813806477503:transaction_uday"
  snsClient=boto3.client("sns",region_name="ap-south-1")
  publish_object={"acc":event["acc"],"amnt":event["amnt"]}
  response=snsClient.publish(
  TopicArn=topicArn,
  Message=json.dumps(publish_object),
  Subject="transaction_details",
  MessageAttributes={"TransactionType":{"DataType":"String","StringValue":"Transfer"}}
  )
  return("Transaction is Successful")