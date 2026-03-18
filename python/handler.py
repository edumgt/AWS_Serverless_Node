import json


def hello(event, context):
    """AWS Lambda handler for a simple Hello World HTTP endpoint."""
    query_params = event.get("queryStringParameters") or {}
    name = query_params.get("name", "World")

    body = {"message": f"Hello, {name}!", "language": "Python"}

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
