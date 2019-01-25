import logging
import os
from urllib.parse import urlparse
from http import HTTPStatus
from psycopg2 import connect

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CONNECTION_TIMEOUT_IN_SECONDS = 10

DATABASE_URL = os.environ['DATABASE_URL']

QUERY = '''
SELECT c.id, c.model
FROM car c
LIMIT 5
'''


def lambda_handler(event, context):
    try:
        connection_params = urlparse(DATABASE_URL)
        conn = connect(
            user=connection_params.username,
            password=connection_params.password,
            host=connection_params.hostname,
            port=connection_params.port,
            dbname=connection_params.path[1:],  # Drop forward slash
            connect_timeout=CONNECTION_TIMEOUT_IN_SECONDS
        )
        cursor = conn.cursor()
        cursor.execute(QUERY)
        records = cursor.fetchall()
        conn.close()

        # do something with the data
        for record in records:
            print(record)

    except Exception as e:  # Catch all for easier error tracing in logs
        logger.error(e, exc_info=True)
        raise Exception('Error occurred during execution')  # notify aws of failure

    return {
        "statusCode": HTTPStatus.OK.value
    }
