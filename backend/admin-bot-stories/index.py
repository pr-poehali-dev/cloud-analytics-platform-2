import os
import json
import psycopg2
import psycopg2.extras
from datetime import datetime

def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], options=f"-c search_path={os.environ.get('MAIN_DB_SCHEMA', 'public')}")

def handler(event: dict, context) -> dict:
    """CRUD управления видео-сторис для Telegram."""
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, X-User-Id, X-Auth-Token, X-Session-Id', 'Access-Control-Max-Age': '86400'}, 'body': ''}

    method = event.get('httpMethod', 'GET')
    params = event.get('queryStringParameters') or {}
    body = json.loads(event.get('body') or '{}')
    action = params.get('action') or body.get('action', '')

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        if method == 'GET':
            cur.execute("SELECT * FROM bot_stories ORDER BY id DESC")
            rows = cur.fetchall()
            result = []
            for row in rows:
                r = dict(row)
                for k, v in r.items():
                    if isinstance(v, datetime):
                        r[k] = v.isoformat()
                result.append(r)
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'stories': result})}

        if method == 'POST' and action == 'create':
            cur.execute(
                "INSERT INTO bot_stories (video_url, caption) VALUES (%s, %s) RETURNING id",
                (body.get('video_url', ''), body.get('caption', ''))
            )
            new_id = cur.fetchone()['id']
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'id': new_id})}

        if method == 'PUT' and action == 'update':
            cur.execute(
                "UPDATE bot_stories SET video_url=%s, caption=%s, is_used=%s WHERE id=%s",
                (body.get('video_url',''), body.get('caption',''), body.get('is_used', False), body.get('id'))
            )
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True})}

        if method == 'DELETE':
            story_id = params.get('id') or body.get('id')
            cur.execute("DELETE FROM bot_stories WHERE id = %s", (story_id,))
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True})}

        return {'statusCode': 400, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': False, 'error': 'Unknown action'})}

    finally:
        cur.close()
        conn.close()
