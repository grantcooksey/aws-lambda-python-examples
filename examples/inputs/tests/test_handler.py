from http import HTTPStatus
import pytest

from inputs import app

# disable sleep
app.CONTEXT_SLEEP_TEST_SECONDS = 0


@pytest.fixture()
def lambda_event():
    return {
        'aws_lambda': 'is_cool'
    }


@pytest.fixture()
def lambda_context():
    return MockContext()


class MockContext:
    def __init__(self):
        self.log_stream_name = '2019/1/15/[$LATEST]b684e04267f11ba5'
        self.log_group_name = '/aws/lambda/test'
        self.aws_request_id = '1'
        self.memory_limit_in_mb = 128

    def get_remaining_time_in_millis(self):
        return 30000


def test_handler(lambda_event, lambda_context):
    response = app.lambda_handler(lambda_event, lambda_context)
    assert response['statusCode'] == HTTPStatus.OK.value
