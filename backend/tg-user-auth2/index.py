import os
import json
import psycopg2
import psycopg2.extras
from datetime import datetime

def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], options=f"-c search_path={os.environ.get('MAIN_DB_SCHEMA', 'public')}")

def handler(event: dict, context) -> dict:
    """Логин Telegram user-аккаунта №2 (для слушателя исключённых). Управление сессией tg_user_session2."""
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, X-User-Id, X-Auth-Token, X-Session-Id', 'Access-Control-Max-Age': '86400'}, 'body': ''}

    method = event.get('httpMethod', 'GET')
    body = json.loads(event.get('body') or '{}')
    action = body.get('action', '')

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        if method == 'GET':
            cur.execute("SELECT id, phone, logged_in, user_info, updated_at FROM tg_user_session2 WHERE id = 1")
            row = cur.fetchone()
            r = dict(row) if row else {}
            for k, v in r.items():
                if isinstance(v, datetime):
                    r[k] = v.isoformat()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'session': r})}

        if action == 'send_code':
            phone = body.get('phone', '')
            api_id = int(os.environ.get('TG_API_ID', '0'))
            api_hash = os.environ.get('TG_API_HASH', '')

            from telethon.sync import TelegramClient
            from telethon.sessions import StringSession
            client = TelegramClient(StringSession(), api_id, api_hash)
            client.connect()
            result = client.send_code_request(phone)
            phone_code_hash = result.phone_code_hash
            client.disconnect()

            cur.execute("UPDATE tg_user_session2 SET phone=%s, phone_code_hash=%s, logged_in=false, updated_at=%s WHERE id=1",
                        (phone, phone_code_hash, datetime.now()))
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'phone_code_hash': phone_code_hash})}

        if action == 'confirm_code':
            phone = body.get('phone', '')
            code = body.get('code', '')
            password = body.get('password', '')

            cur.execute("SELECT phone_code_hash FROM tg_user_session2 WHERE id=1")
            row = cur.fetchone()
            phone_code_hash = row['phone_code_hash'] if row else ''

            api_id = int(os.environ.get('TG_API_ID', '0'))
            api_hash = os.environ.get('TG_API_HASH', '')

            from telethon.sync import TelegramClient
            from telethon.sessions import StringSession
            client = TelegramClient(StringSession(), api_id, api_hash)
            client.connect()
            try:
                client.sign_in(phone, code, phone_code_hash=phone_code_hash)
            except Exception as e:
                if '2FA' in str(e) or 'password' in str(e).lower():
                    client.sign_in(password=password)
                else:
                    raise

            session_string = client.session.save()
            me = client.get_me()
            user_info = {'id': me.id, 'first_name': me.first_name, 'username': me.username}
            client.disconnect()

            cur.execute("UPDATE tg_user_session2 SET session_string=%s, logged_in=true, user_info=%s, updated_at=%s WHERE id=1",
                        (session_string, json.dumps(user_info), datetime.now()))
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'user': user_info})}

        if action == 'logout':
            cur.execute("UPDATE tg_user_session2 SET session_string=NULL, logged_in=false, updated_at=%s WHERE id=1", (datetime.now(),))
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True})}

        return {'statusCode': 400, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': False, 'error': 'Unknown action'})}

    finally:
        cur.close()
        conn.close()
