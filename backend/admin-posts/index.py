import os
import json
import psycopg2
import psycopg2.extras
from datetime import datetime

def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], options=f"-c search_path={os.environ.get('MAIN_DB_SCHEMA', 'public')}")

def handler(event: dict, context) -> dict:
    """CRUD постов в Telegram-канал: получение, создание, обновление, удаление, публикация."""
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, X-User-Id, X-Auth-Token, X-Session-Id', 'Access-Control-Max-Age': '86400'}, 'body': ''}

    method = event.get('httpMethod', 'GET')
    params = event.get('queryStringParameters') or {}
    body = json.loads(event.get('body') or '{}')

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        action = params.get('action') or body.get('action', '')

        if method == 'GET':
            status_filter = params.get('status', '')
            if status_filter:
                cur.execute("SELECT * FROM posts WHERE status = %s ORDER BY created_at DESC", (status_filter,))
            else:
                cur.execute("SELECT * FROM posts ORDER BY created_at DESC")
            rows = cur.fetchall()
            result = []
            for row in rows:
                r = dict(row)
                for k, v in r.items():
                    if isinstance(v, datetime):
                        r[k] = v.isoformat()
                result.append(r)
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'posts': result})}

        if method == 'POST' and action == 'create':
            cur.execute(
                """INSERT INTO posts (title, text, photo_url, video_note_url, button_text, button_url, button2_text, button2_url, status, chats, scheduled_at)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
                (body.get('title',''), body.get('text',''), body.get('photo_url',''), body.get('video_note_url',''),
                 body.get('button_text',''), body.get('button_url',''), body.get('button2_text',''), body.get('button2_url',''),
                 body.get('status','draft'), body.get('chats','main'), body.get('scheduled_at'))
            )
            new_id = cur.fetchone()['id']
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'id': new_id})}

        if method == 'PUT' and action == 'update':
            post_id = body.get('id')
            cur.execute(
                """UPDATE posts SET title=%s, text=%s, photo_url=%s, video_note_url=%s, button_text=%s, button_url=%s,
                   button2_text=%s, button2_url=%s, status=%s, chats=%s, scheduled_at=%s, updated_at=now()
                   WHERE id=%s""",
                (body.get('title',''), body.get('text',''), body.get('photo_url',''), body.get('video_note_url',''),
                 body.get('button_text',''), body.get('button_url',''), body.get('button2_text',''), body.get('button2_url',''),
                 body.get('status','draft'), body.get('chats','main'), body.get('scheduled_at'), post_id)
            )
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True})}

        if method == 'DELETE':
            post_id = params.get('id') or body.get('id')
            cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
            conn.commit()
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True})}

        if method == 'POST' and action == 'publish':
            import requests as req
            post_id = body.get('id')
            cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
            post = dict(cur.fetchone())

            bot_token = os.environ.get('UG_INFO_BOT_TOKEN_NEW', '')
            channel_id = os.environ.get('UG_DRIVER_CHANNEL_ID', '')

            send_params = {'chat_id': channel_id, 'parse_mode': 'HTML'}
            buttons = []
            if post.get('button_text') and post.get('button_url'):
                buttons.append([{'text': post['button_text'], 'url': post['button_url']}])
            if post.get('button2_text') and post.get('button2_url'):
                buttons.append([{'text': post['button2_text'], 'url': post['button2_url']}])
            if buttons:
                send_params['reply_markup'] = json.dumps({'inline_keyboard': buttons})

            if post.get('photo_url'):
                send_params['caption'] = post['text']
                send_params['photo'] = post['photo_url']
                resp = req.post(f'https://api.telegram.org/bot{bot_token}/sendPhoto', data=send_params)
            else:
                send_params['text'] = post['text']
                resp = req.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=send_params)

            tg_result = resp.json()
            if tg_result.get('ok'):
                msg_id = tg_result['result']['message_id']
                cur.execute("UPDATE posts SET status='published', published_at=now(), telegram_message_id=%s, updated_at=now() WHERE id=%s", (msg_id, post_id))
                conn.commit()
                return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': True, 'message_id': msg_id})}
            else:
                return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': False, 'error': tg_result.get('description', 'Telegram error')})}

        return {'statusCode': 400, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': False, 'error': 'Unknown action'})}

    finally:
        cur.close()
        conn.close()
