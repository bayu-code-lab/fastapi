import boto3
import settings
import json

async def send_message(data):
    sqs = boto3.client(
        'sqs',region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    response = sqs.send_message( QueueUrl='{}{}'.format(settings.CONSUMER_BASE_URL,'_notification'), DelaySeconds=0, MessageBody=json.dumps(data))
