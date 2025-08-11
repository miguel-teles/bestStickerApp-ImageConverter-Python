import base64
import json
from io import BytesIO

import pytest
from PIL import Image

from src import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": open('base64Image.json').read(),
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }


def test_lambda_function(apigw_event):
    response = app.lambda_handler(apigw_event, None)

    assert response["statusCode"] == 200
    body = json.loads(response.get('body'))
    assert body.get('webpImageBase64') != None

    base64_webp_image = base64.b64decode(body.get('webpImageBase64'))
    Image.open(BytesIO(base64_webp_image)).show()
    assert response is not None

    response = app.lambda_handler({"body": "{warmup:true}"}, None)
    assert response["statusCode"] == 200



def test_lambda_function_invalid_base64():
    webp_image = app.lambda_handler({'abcs': ''}, {})

    assert webp_image.get('body') is not None
    assert webp_image.get('statusCode') is not 200

    assert 'message' in webp_image.get('body')
    assert 'status' in webp_image.get('body')

    webp_image = app.lambda_handler({"body": None}, {})
    assert webp_image.get('body') is not None
    assert webp_image.get('statusCode') is not 200

    assert 'message' in webp_image.get('body')
    assert 'status' in webp_image.get('body')
