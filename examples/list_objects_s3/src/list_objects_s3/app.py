import logging
import os
from http import HTTPStatus
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ['S3_BUCKET']


def lambda_handler(event, context):
    try:
        logger.info(f'Calling out to {S3_BUCKET} bucket to list objects')
        s3_client = boto3.client('s3')

        # Get all the objects from the bucket. Max 1000
        objects_in_bucket = s3_client.list_objects(Bucket=S3_BUCKET)

        logger.info('Found {} objects in the bucket. Printing a sample...'.format(len(objects_in_bucket['Contents'])))

        for key in objects_in_bucket['Contents'][:5]:
            logger.info('Found {} in bucket'.format(key['Key']))

    except Exception as e:  # Catch all for easier error tracing in logs
        logger.error(e, exc_info=True)
        raise Exception('Error occurred during execution')  # notify aws of failure

    return {
        "statusCode": HTTPStatus.OK.value
    }
