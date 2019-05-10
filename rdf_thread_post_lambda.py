import json
import boto3
import sys


def lambda_handler(event, context):
    # Get the values from the request body
    title = event["title"]
    votes = event["votes"]
    thread_creation_time = event["thread_creation_time"]
    insert_day = event["insert_day"]
    url = event["url"]
    mp3_url = event["mp3_url"]
    db_id = event["db_id"]

    # Set the SNS topic ARN
    SNS_ARN_TOPIC = "arn:aws:sns:us-east-1:[your_ARN]"

    # Insert into DynamoDB rdf table
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    rdf_table = dynamodb.Table('rdf_dynamo_table')

    try:
        response = rdf_table.put_item(
            Item={
                'title': title,
                'votes': votes,
                'thread_creation_time': thread_creation_time,
                'insert_day': insert_day,
                'url': url,
                'mp3_url': mp3_url,
                'db_id': db_id
            }
        )
        print("Item successfully added:")
        print(json.dumps(response))

    except ClientError as e:
        print(e.response['Error']['Message'])
        sys.exit(1)

    # Send SNS topic to notify Polly to create mp3 file out of title
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn=SNS_ARN_TOPIC,
        Subject=title,
        Message=url
    )

    return response["ResponseMetadata"]["HTTPStatusCode"]
