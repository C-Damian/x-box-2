import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("posted_tips")

#add posted tip from main.py to dynamoDB
def add_posted_tip(tip: dict):
    table.put_item(Item=tip)