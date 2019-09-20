from unittest import mock
import httpretty
import requests
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
from rest_framework.test import APITestCase
from django.conf import settings
from rest_framework import status

from apps.iot_client import AWSIoTClient, AWSIoTError
from tests.utils import mocked_rpc_response


class FakeBotoAWSRequestsAuth(BotoAWSRequestsAuth):
    def __init__(self, *args, **kwargs):
        pass

    def get_aws_request_headers_handler(self, r):
        return {}


class AWSSetUpCase(APITestCase):
    """
    Ensure API endpoints have correct permissions and return appropriate errors or data
    """

    def setUp(self):
        settings.IOT_THING_INTEGRATION = True
        settings.IOT_AWS_HOST = 'not-really-aws.com'
        settings.IOT_GATEWAY_STAGE = 'test'

    def test_init(self):
        aws_iot_client = AWSIoTClient()

        self.assertEqual(aws_iot_client.session.auth.aws_host, settings.IOT_AWS_HOST)
        self.assertEqual(aws_iot_client.session.auth.aws_region, 'us-east-1')
        self.assertEqual(aws_iot_client.session.auth.service, 'execute-api')
        self.assertEqual(aws_iot_client.session.auth.aws_secret_access_key, None)
        self.assertIn('content-type', aws_iot_client.session.headers)
        self.assertEqual(aws_iot_client.session.headers['content-type'], 'application/json')


@mock.patch('apps.iot_client.BotoAWSRequestsAuth', FakeBotoAWSRequestsAuth)
class AWSTestWithMocked(APITestCase):
    def setUp(self):
        settings.IOT_THING_INTEGRATION = True
        settings.IOT_AWS_HOST = 'not-really-aws.com'
        settings.IOT_GATEWAY_STAGE = 'test'

    def test_get(self):
        aws_iot_client = AWSIoTClient()

        # Call without connection return the 503 Error
        with mock.patch.object(requests.Session, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError(mock.Mock(status=503), 'not found')
            try:
                aws_iot_client._get('test_method')
                self.fail("Should have thrown AWS Error")
            except AWSIoTError as aws_error:
                self.assertEqual(aws_error.status_code, 503)

        with mock.patch.object(requests.Session, 'get') as mock_get:
            mock_get.return_value = mocked_rpc_response({
                "error": {
                    "code": 1337,
                    "message": "Error from AWS Server",
                },
            })
            try:
                aws_iot_client._get('test_method')
            except AWSIoTError as aws_error:
                self.assertEqual(aws_error.status_code, 500)
                self.assertIn('Error from AWS Server', aws_error.detail)

            mock_get.return_value = mocked_rpc_response({
                "error": {
                    "code": 404,
                    "message": "Error from AWS Server",
                },
            }, code=404)

            try:
                aws_iot_client._get('test_method')
            except AWSIoTError as aws_error:
                self.assertEqual(aws_error.status_code, 500)
                self.assertIn('Error from AWS Server', aws_error.detail)

            mock_get.side_effect = KeyError('Generic Exception')

            try:
                aws_iot_client._get('test_method')
            except AWSIoTError as aws_error:
                self.assertEqual(aws_error.status_code, 500)

    def test_call(self):
        aws_iot_client = AWSIoTClient()

        # Call without connection return the 503 Error
        with mock.patch.object(requests.Session, 'post') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError(mock.Mock(status=503), 'not found')

            try:
                aws_iot_client._call('post', 'test_method')
                self.fail("Should have thrown AWS Error")
            except AWSIoTError as aws_error:
                self.assertEqual(aws_error.status_code, 503)

        with mock.patch.object(requests.Session, 'post') as mock_post:
            mock_post.return_value = mocked_rpc_response({
                "error": {
                    "code": 404,
                    "message": "Error from AWS Server",
                },
            }, code=404)
            try:
                aws_iot_client._call('post', 'test_method')
            except AWSIoTError as aws_error:
                self.assertEqual(aws_error.status_code, 500)
                self.assertIn('Error from AWS Server', aws_error.detail)

            mock_post.return_value = mocked_rpc_response({
                "message": {
                    "code": 404,
                    "message": "Error from AWS Server",
                },
            }, code=404)
            try:
                aws_iot_client._call('post', 'test_method')
            except AWSIoTError as aws_error:
                self.assertEqual(aws_error.status_code, 500)
                self.assertIn('Error from AWS Server', aws_error.detail)

            mock_post.return_value = mocked_rpc_response({
                "fail": {
                    "code": 404,
                    "message": "Error from AWS Server",
                },
            }, code=404)
            try:
                aws_iot_client._call('post', 'test_method')
            except AWSIoTError as aws_error:
                self.assertEqual(aws_error.status_code, 500)
                self.assertIn('Error from AWS Server', aws_error.detail)

            mock_post.return_value = mocked_rpc_response({
                "success": {
                    "message": "Success from AWS Server",
                },
            }, code=404)
            try:
                aws_iot_client._call('patch', 'test_method')
            except AWSIoTError as aws_error:
                self.assertEqual(aws_error.status_code, 500)
                self.assertIn('Invalid HTTP Method', aws_error.detail)