import os
import json
import psycopg2
import psycopg2.extras
import requests
from datetime import datetime

def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], options=f"-c search_path={os.environ.get('MAIN_DB_SCHEMA', 'public')}")

def handler(event: dict, context) -> dict:
    """Автопубликация сторис в Telegram раз в 48 часов через business-аккаунт."""
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, X-Cron-Secret', 'Access-Control-Max-Age': '86400'}, 'body': ''}

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cur.execute("SELECT * FROM bot_stories WHERE is_used = false ORDER BY id ASC LIMIT 1")
        story = cur.fetchone()
        if not story:
            cur.execute("UPDATE bot_stories SET is_used = false")
            conn.commit()
            cur.execute("SELECT * FROM bot_stories ORDER BY id ASC LIMIT 1")
            story = cur.fetchone()

        if not story:
            return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'ok': False, 'message': 'Нет сторис для публикации'})}

        story = dict(story)
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN_2', '')
        business_id = os.environ.get('TELEGRAM_BUSINESS_CONNECTION_ID', '')

        video_data = requests.get(story['video_url']).content
        resp = requests.post(
            f'https://api.telegram.org/bot{bot_token}/sendVideoNote',
            data={'business_connection_id': business_id},
            files={'video_note': ('story.mp4', video_data, 'video/mp4')}
        )
        result = resp.json()

        status = 'sent' if result.get('ok') else f"error: {result.get('description', '')}"
        cur.execute(
            "UPDATE bot_stories SET is_used=true, last_sent_at=%s, last_status=%s WHERE id=%s",
            (datetime.now(), status, story['id'])
        )
        conn.commit()

        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'ok': result.get('ok', False), 'status': status, 'story_id': story['id']})}

    finally:
        cur.close()
        conn.close()
