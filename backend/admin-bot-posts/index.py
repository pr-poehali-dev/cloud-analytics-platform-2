import os
import json
import psycopg2
import psycopg2.extras
from datetime import datetime

def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], options=f"-c search_path={os.environ.get('MAIN_DB_SCHEMA', 'public')}")

def handler(event: dict, context) -> dict:
    """CRUD ежедневных постов бота @ug_sait_bot (Telegram + ВКонтакте)."""
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
            cur.execute("SELECT * FROM bot_daily_posts ORDER BY id DESC")
            rows = cur.fetchall()
            result = []
            for row in rows:
                r = dict(row)
                for k, v in r.items():
                    if isinstance(v, datetime):
                        r[k] = v.isoformat()
                    elif hasattr(v, 'isoformat'):
                        r[k] = v.isoformat()
                result.append(r)
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'posts': result})}

        if method == 'POST' and action == 'create':
            cur.execute(
                "INSERT INTO bot_daily_posts (photo_url, greeting, description) VALUES (%s, %s, %s) RETURNING id",
                (body.get('photo_url', ''), body.get('greeting', ''), body.get('description', ''))
            )
            new_id = cur.fetchone()['id']
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'id': new_id})}

        if method == 'PUT' and action == 'update':
            cur.execute(
                "UPDATE bot_daily_posts SET photo_url=%s, greeting=%s, description=%s, is_used=%s WHERE id=%s",
                (body.get('photo_url',''), body.get('greeting',''), body.get('description',''), body.get('is_used', False), body.get('id'))
            )
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True})}

        if method == 'DELETE':
            post_id = params.get('id') or body.get('id')
            cur.execute("DELETE FROM bot_daily_posts WHERE id = %s", (post_id,))
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True})}

        return {'statusCode': 400, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': False, 'error': 'Unknown action'})}

    finally:
        cur.close()
        conn.close()
