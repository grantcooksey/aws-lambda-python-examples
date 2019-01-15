import logging
import time
from http import HTTPStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CONTEXT_SLEEP_TEST_SECONDS = 1


def lambda_handler(event, context):
    try:
        logger.info('Starting input lambda function call')

        print('Event: {}'.format(event))

        print("Log stream name:", context.log_stream_name)
        print("Log group name:", context.log_group_name)
        print("Request ID:", context.aws_request_id)
        print("Mem. limits(MB):", context.memory_limit_in_mb)
        # Code will execute quickly, so we add a 1 second intentional delay so you can see that in time remaining value.
        print("Time remaining (MS):", context.get_remaining_time_in_millis())
        print("Sleeping for 1 sec now")
        time.sleep(CONTEXT_SLEEP_TEST_SECONDS)
        print("Time remaining (MS):", context.get_remaining_time_in_millis())

    except Exception as e:  # Catch all for easier error tracing in logs
        logger.error(e, exc_info=True)
        raise Exception('Error occurred during execution')  # notify aws of failure

    return {
        "statusCode": HTTPStatus.OK.value
    }
