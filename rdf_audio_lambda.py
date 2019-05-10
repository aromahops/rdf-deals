import boto3
import os
from contextlib import closing
from boto3.dynamodb.conditions import Key, Attr
import re


def lambda_handler(event, context):
    # Set values
    SPEAKER_VOICE = 'Joanna'
    VOICE_FORMAT = 'mp3'
    S3_RDF_BUCKET = "[YOUR_S3_BUCKET]"

    # Get the SNS message passed by the rdf_post_thread lambda function
    url = event["Records"][0]["Sns"]["Message"]  # Get the SNS message

    # Query the specified row in dynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    rdf_table = dynamodb.Table("rdf_dynamo_table")
    rdf_thread = rdf_table.query(
        KeyConditionExpression=Key('url').eq(url)
    )

    title = rdf_thread["Items"][0]["title"]
    alphanumeric_title = re.sub(r'\W+', '', title)

    # synthesize the rdf title into an mp3 voice file
    polly = boto3.client('polly', region_name='us-east-1')

    try:
        response = polly.synthesize_speech(
            VoiceId=SPEAKER_VOICE,
            OutputFormat=VOICE_FORMAT,
            Text=title
        )
    except (BotoCoreError, ClientError) as e:
        print(e)
        sys.exit(1)

    # Write mp3 file to temp directory in Lambda
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            mp3_directory_file = os.path.join("/tmp/", alphanumeric_title)
            try:
                with open(mp3_directory_file, "wb") as mp3file:
                    mp3file.write(response["AudioStream"].read())
                    mp3file.close()
            except IOError as e:
                print(e)
                sys.exit(1)
    else:
        print("No audio to stream")
        sys.exit(1)

    # Save to S3
    s3 = boto3.client('s3')

    try:
        s3.upload_file(mp3_directory_file,
                       S3_RDF_BUCKET,
                       alphanumeric_title + ".mp3")

    except(BotoCoreError, ClientError) as e:
        print("uploading file to s3 failed: " + e)
        sys.exit(1)

    s3_mp3_url = "https://s3.amazonaws.com/" + S3_RDF_BUCKET + \
                 "/" + alphanumeric_title + ".mp3"

    # Updates the mp3 url in DynamoDB after polly synthesizes text
    response = rdf_table.update_item(
        Key={'url': url},
        UpdateExpression="set mp3_url = :mp3_val",
        ExpressionAttributeValues={':mp3_val': s3_mp3_url}
    )

    return response["ResponseMetadata"]["HTTPStatusCode"]
