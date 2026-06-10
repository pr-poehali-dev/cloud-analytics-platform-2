-- ============================================================
-- Миграция для НОВОГО проекта: модуль «Посты в канал»
-- ============================================================

-- Основные посты в Telegram-канал
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL DEFAULT '',
    text TEXT NOT NULL,
    photo_url TEXT DEFAULT '',
    video_note_url TEXT DEFAULT '',
    button_text TEXT DEFAULT '',
    button_url TEXT DEFAULT '',
    button2_text TEXT DEFAULT '',
    button2_url TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'draft',
    chats TEXT NOT NULL DEFAULT 'main',
    scheduled_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,
    telegram_message_id BIGINT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Ежедневные посты бота (Telegram + ВК)
CREATE TABLE IF NOT EXISTS bot_daily_posts (
    id SERIAL PRIMARY KEY,
    photo_url TEXT NOT NULL,
    greeting TEXT NOT NULL,
    description TEXT NOT NULL,
    is_used BOOLEAN DEFAULT false,
    scheduled_date DATE,
    last_tg_status TEXT,
    last_vk_status TEXT,
    last_vk_user_status TEXT,
    last_sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT now()
);

-- Видео-сторис
CREATE TABLE IF NOT EXISTS bot_stories (
    id SERIAL PRIMARY KEY,
    video_url TEXT NOT NULL,
    caption TEXT NOT NULL DEFAULT '',
    is_used BOOLEAN DEFAULT false,
    last_sent_at TIMESTAMP,
    last_status TEXT,
    created_at TIMESTAMP DEFAULT now()
);

-- Исключённые водители
CREATE TABLE IF NOT EXISTS excluded_drivers (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    username TEXT,
    first_name TEXT,
    detected_at TIMESTAMP DEFAULT now(),
    message_sent BOOLEAN DEFAULT false,
    message_sent_at TIMESTAMP,
    send_status TEXT,
    source_msg_id BIGINT,
    resend_queued BOOLEAN DEFAULT false,
    resend_status TEXT,
    resend_at TIMESTAMP,
    access_hash BIGINT,
    is_unreachable BOOLEAN NOT NULL DEFAULT false
);

-- Настройки слушателя исключённых (одна строка, id=1)
CREATE TABLE IF NOT EXISTS excluded_settings (
    id INTEGER PRIMARY KEY DEFAULT 1,
    enabled BOOLEAN DEFAULT false,
    message_template TEXT NOT NULL DEFAULT '',
    photo_url TEXT DEFAULT '',
    button_text TEXT DEFAULT '',
    button_url TEXT DEFAULT '',
    source_chat TEXT DEFAULT '',
    source_msg_id BIGINT DEFAULT 0,
    last_checked_msg_id BIGINT DEFAULT 0,
    last_run_at TIMESTAMP,
    loop_token TEXT,
    loop_heartbeat TIMESTAMP,
    active_session SMALLINT DEFAULT 2,
    humanize_enabled BOOLEAN DEFAULT true
);
INSERT INTO excluded_settings (id) VALUES (1) ON CONFLICT (id) DO NOTHING;

-- Сессии Telegram user-аккаунтов
CREATE TABLE IF NOT EXISTS tg_user_session (
    id INTEGER PRIMARY KEY DEFAULT 1,
    phone TEXT,
    phone_code_hash TEXT,
    session_string TEXT,
    logged_in BOOLEAN DEFAULT false,
    user_info JSONB,
    updated_at TIMESTAMP DEFAULT now()
);
INSERT INTO tg_user_session (id) VALUES (1) ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS tg_user_session2 (
    id INTEGER PRIMARY KEY DEFAULT 1,
    phone TEXT,
    phone_code_hash TEXT,
    session_string TEXT,
    logged_in BOOLEAN DEFAULT false,
    user_info JSONB,
    updated_at TIMESTAMP DEFAULT now()
);
INSERT INTO tg_user_session2 (id) VALUES (1) ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS tg_user_session3 (
    id INTEGER PRIMARY KEY DEFAULT 1,
    phone TEXT,
    phone_code_hash TEXT,
    session_string TEXT,
    logged_in BOOLEAN DEFAULT false,
    user_info JSONB,
    updated_at TIMESTAMP DEFAULT now()
);
INSERT INTO tg_user_session3 (id) VALUES (1) ON CONFLICT (id) DO NOTHING;

-- Пул user-аккаунтов Telegram
CREATE TABLE IF NOT EXISTS tg_user_accounts (
    id SERIAL PRIMARY KEY,
    label TEXT NOT NULL,
    phone TEXT,
    session_string TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT false,
    is_banned BOOLEAN NOT NULL DEFAULT false,
    daily_invites_used INTEGER NOT NULL DEFAULT 0,
    daily_reset_date DATE NOT NULL DEFAULT CURRENT_DATE,
    last_used_at TIMESTAMP,
    warmup_last_invite_date DATE,
    needs_warmup BOOLEAN NOT NULL DEFAULT true,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- Business-подключения Telegram
CREATE TABLE IF NOT EXISTS business_connections (
    id SERIAL PRIMARY KEY,
    connection_id TEXT NOT NULL,
    user_id BIGINT,
    username TEXT,
    is_enabled BOOLEAN DEFAULT true,
    can_reply BOOLEAN DEFAULT false,
    raw JSONB,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Глобальные настройки
CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL DEFAULT '',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);