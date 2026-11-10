import os
from html import escape

import boto3
from botocore.config import Config


s3 = boto3.client(
    "s3",
    endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
    config=Config(s3={"addressing_style": "path"}),
)


def handler(event, context):
    params = event.get("queryStringParameters") or {}
    name = (params.get("imie") or "").strip()
    if not name:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": "Podaj imię w adresie, na przykład: ?imie=Ola",
        }

    obj = s3.get_object(Bucket=os.environ["TEMPLATE_BUCKET"], Key="template.html")
    template = obj["Body"].read().decode("utf-8")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": template.replace("{{IMIE}}", escape(name)),
    }
