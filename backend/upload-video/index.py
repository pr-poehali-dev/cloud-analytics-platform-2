import os
import json
import base64
import boto3
import uuid
from datetime import datetime

def handler(event: dict, context) -> dict:
    """Загрузка видео-кружка в S3 и возврат CDN URL."""
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, X-User-Id, X-Auth-Token, X-Session-Id', 'Access-Control-Max-Age': '86400'}, 'body': ''}

    body = json.loads(event.get('body') or '{}')
    file_data = body.get('file_data', '')
    file_name = body.get('file_name', f'video_{uuid.uuid4().hex}.mp4')
    content_type = body.get('content_type', 'video/mp4')

    if not file_data:
        return {'statusCode': 400, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': False, 'error': 'file_data is required'})}

    video_bytes = base64.b64decode(file_data)

    s3 = boto3.client(
        's3',
        endpoint_url='https://bucket.poehali.dev',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

    key = f'videos/{datetime.now().strftime("%Y%m")}/{uuid.uuid4().hex}_{file_name}'
    s3.put_object(Bucket='files', Key=key, Body=video_bytes, ContentType=content_type)

    cdn_url = f"https://cdn.poehali.dev/projects/{os.environ['AWS_ACCESS_KEY_ID']}/bucket/{key}"

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'ok': True, 'url': cdn_url, 'key': key})
    }
