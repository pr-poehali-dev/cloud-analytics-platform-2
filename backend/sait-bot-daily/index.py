import os
import json
import psycopg2
import psycopg2.extras
import requests
from datetime import datetime

def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], options=f"-c search_path={os.environ.get('MAIN_DB_SCHEMA', 'public')}")

def post_to_vk(text: str, photo_url: str = '') -> dict:
    token = os.environ.get('VK_USER_TOKEN', '')
    group_id = os.environ.get('VK_GROUP_ID', '')
    owner_id = f'-{group_id}'

    if photo_url:
        upload_resp = requests.get(
            'https://api.vk.com/method/photos.getWallUploadServer',
            params={'access_token': token, 'group_id': group_id, 'v': '5.199'}
        ).json()
        upload_url = upload_resp['response']['upload_url']
        img_data = requests.get(photo_url).content
        uploaded = requests.post(upload_url, files={'photo': ('photo.jpg', img_data, 'image/jpeg')}).json()
        save_resp = requests.get(
            'https://api.vk.com/method/photos.saveWallPhoto',
            params={'access_token': token, 'group_id': group_id, 'v': '5.199',
                    'photo': uploaded['photo'], 'server': uploaded['server'], 'hash': uploaded['hash']}
        ).json()
        photo_obj = save_resp['response'][0]
        attachments = f"photo{photo_obj['owner_id']}_{photo_obj['id']}"
        return requests.get(
            'https://api.vk.com/method/wall.post',
            params={'access_token': token, 'owner_id': owner_id, 'message': text, 'attachments': attachments, 'v': '5.199'}
        ).json()
    else:
        return requests.get(
            'https://api.vk.com/method/wall.post',
            params={'access_token': token, 'owner_id': owner_id, 'message': text, 'v': '5.199'}
        ).json()

def handler(event: dict, context) -> dict:
    """Автопубликация ежедневного поста в Telegram и ВКонтакте (cron-задача)."""
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, X-Cron-Secret', 'Access-Control-Max-Age': '86400'}, 'body': ''}

    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN_2', '')
    channel_id = os.environ.get('UG_DRIVER_CHANNEL_ID', '')

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cur.execute("SELECT * FROM bot_daily_posts WHERE is_used = false ORDER BY id ASC LIMIT 1")
        post = cur.fetchone()
        if not post:
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': False, 'message': 'Нет доступных постов'})}

        post = dict(post)
        text = f"{post['greeting']}\n\n{post['description']}"

        tg_status = 'error'
        if post.get('photo_url'):
            resp = requests.post(f'https://api.telegram.org/bot{bot_token}/sendPhoto',
                data={'chat_id': channel_id, 'caption': text, 'photo': post['photo_url'], 'parse_mode': 'HTML'})
        else:
            resp = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage',
                data={'chat_id': channel_id, 'text': text, 'parse_mode': 'HTML'})
        tg_result = resp.json()
        if tg_result.get('ok'):
            tg_status = 'sent'

        vk_status = 'skip'
        if os.environ.get('VK_USER_TOKEN'):
            vk_result = post_to_vk(text, post.get('photo_url', ''))
            vk_status = 'sent' if vk_result.get('response') else f"error: {vk_result}"

        cur.execute(
            "UPDATE bot_daily_posts SET is_used=true, last_sent_at=%s, last_tg_status=%s, last_vk_status=%s WHERE id=%s",
            (datetime.now(), tg_status, vk_status, post['id'])
        )
        conn.commit()

        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'ok': True, 'tg_status': tg_status, 'vk_status': vk_status, 'post_id': post['id']})}

    finally:
        cur.close()
        conn.close()
