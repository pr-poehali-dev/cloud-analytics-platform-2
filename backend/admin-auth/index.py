import os
import json

def handler(event: dict, context) -> dict:
    """Аутентификация администратора. Поддерживает scope=posts для раздела постов."""
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, X-User-Id, X-Auth-Token, X-Session-Id', 'Access-Control-Max-Age': '86400'}, 'body': ''}

    body = json.loads(event.get('body') or '{}')
    scope = body.get('scope', 'admin')
    login = body.get('login', '')
    password = body.get('password', '')

    if scope == 'posts':
        valid_login = os.environ.get('POSTS_LOGIN', '')
        valid_password = os.environ.get('POSTS_PASSWORD', '')
    else:
        valid_login = os.environ.get('ADMIN_LOGIN', '')
        valid_password = os.environ.get('ADMIN_PASSWORD', '')

    if login == valid_login and password == valid_password:
        import secrets
        token = secrets.token_hex(32)
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'ok': True, 'token': token, 'scope': scope})
        }

    return {
        'statusCode': 401,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'ok': False, 'error': 'Неверный логин или пароль'})
    }
