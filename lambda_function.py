import boto3
import json
from botocore.exceptions import ClientError
def lambda_handler(event, context):
  AccDb=boto3.resource("dynamodb")
  table=AccDb.Table("Accounts_uday")
  acc=str(event["acc"])
  response = table.get_item(
  	Key={
  		"acc":acc
  		}
  		)
  item=response['Item']
  if response.get('Item')==None:
    return("Invalid account number!!! RETRY!!!")
    print("Exiting")
    exit()
  else:
      return("Your Balance is",item["balance"])