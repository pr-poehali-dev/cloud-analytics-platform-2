import os
import json
import psycopg2
import psycopg2.extras
from datetime import datetime

def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], options=f"-c search_path={os.environ.get('MAIN_DB_SCHEMA', 'public')}")

def handler(event: dict, context) -> dict:
    """Авто-сообщения исключённым водителям: чтение настроек, сохранение водителей, отправка сообщений."""
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, X-User-Id, X-Auth-Token, X-Session-Id', 'Access-Control-Max-Age': '86400'}, 'body': ''}

    method = event.get('httpMethod', 'GET')
    params = event.get('queryStringParameters') or {}
    body = json.loads(event.get('body') or '{}')
    action = params.get('action') or body.get('action', '')

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        if method == 'GET' and action == 'settings':
            cur.execute("SELECT * FROM excluded_settings WHERE id = 1")
            row = cur.fetchone()
            r = dict(row) if row else {}
            for k, v in r.items():
                if isinstance(v, datetime):
                    r[k] = v.isoformat()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'settings': r})}

        if method == 'GET' and action == 'list':
            cur.execute("SELECT * FROM excluded_drivers ORDER BY detected_at DESC LIMIT 200")
            rows = cur.fetchall()
            result = []
            for row in rows:
                r = dict(row)
                for k, v in r.items():
                    if isinstance(v, datetime):
                        r[k] = v.isoformat()
                result.append(r)
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'drivers': result})}

        if method == 'PUT' and action == 'settings':
            cur.execute(
                """UPDATE excluded_settings SET enabled=%s, message_template=%s, photo_url=%s,
                   button_text=%s, button_url=%s, source_chat=%s, active_session=%s, humanize_enabled=%s
                   WHERE id=1""",
                (body.get('enabled', False), body.get('message_template', ''), body.get('photo_url', ''),
                 body.get('button_text', ''), body.get('button_url', ''), body.get('source_chat', ''),
                 body.get('active_session', 2), body.get('humanize_enabled', True))
            )
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True})}

        if method == 'POST' and action == 'add_driver':
            cur.execute(
                """INSERT INTO excluded_drivers (user_id, username, first_name, access_hash)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (body.get('user_id'), body.get('username'), body.get('first_name'), body.get('access_hash'))
            )
            new_id = cur.fetchone()['id']
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'id': new_id})}

        if method == 'DELETE':
            driver_id = params.get('id') or body.get('id')
            cur.execute("DELETE FROM excluded_drivers WHERE id = %s", (driver_id,))
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True})}

        return {'statusCode': 400, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': False, 'error': 'Unknown action'})}

    finally:
        cur.close()
        conn.close()
