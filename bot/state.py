import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("x-bot-state")

#add posted tip to dynamoDB
def add_posted_tip(tip: dict):
    table.put_item(Item=tip)