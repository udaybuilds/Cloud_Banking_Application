import boto3
import json
import random
from botocore.exceptions import ClientError
def lambda_handler(event, context):
    otp = random.randint(100000,999999)
    invokelam=boto3.client("lambda",region_name="ap-south-1")
    AccDb=boto3.resource("dynamodb")
    table=AccDb.Table("Accounts_uday")
    acc=str(event["acc"])
    response = table.get_item(
    Key={
    "acc":acc
    }
    )
    if response.get('Item')==None:
        return(1)
        print("Exiting")
        exit()
    item=response['Item']
    number=item["no"]
    payload={
          "target": str(number),
          "type": "sms",
          "message": str(otp),
          "region": "ap-south-1"
        }
    print(type(payload["target"]),payload["target"])
    resp=invokelam.invoke(FunctionName="sending-otp-cloudfront-Uday",InvocationType="Event",Payload=json.dumps(payload))
    print(type(otp))
    return(otp)