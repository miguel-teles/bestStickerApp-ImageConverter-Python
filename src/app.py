import base64
import json
from io import BytesIO

from PIL import Image, UnidentifiedImageError


def lambda_handler(event, context):
    try:
        body = event.get('body')
        if body is None:
            raise ValueError("Request body is required")

        return convertImage(json.loads(event.get('body')).get('originalImageBase64'))
    except ValueError as ex:
        return respondError(400, str(ex))
    except UnidentifiedImageError as ex:
        return respondError(400, 'Invalid base64 image')
    except Exception as ex:
        return respondError(500, str(ex))


def convertImage(base64_image):
    if base64_image is None:
        raise ValueError("Request image is required")
    if type(base64_image) is not str:
        raise ValueError("Request image has to be a string")

    bytes_original_image = base64.b64decode(base64_image)
    original_image = Image.open(BytesIO(bytes_original_image))

    f = BytesIO()
    original_image.save(f, 'webp')
    webp_base64 = base64.b64encode(f.getvalue()).decode('utf-8')

    return respondSuccess(webp_base64)


def respondError(status_code, message):
    return {
        "statusCode": status_code,
        "body": json.dumps({
            "status": status_code,
            "message": message
        })
    }


def respondSuccess(webp_image):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "webpImageBase64": webp_image
        })
    }
