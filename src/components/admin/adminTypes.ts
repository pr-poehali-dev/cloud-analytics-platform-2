// URLs бэкенд-функций (новый проект)
export const API_URLS = {
  adminAuth:       "https://functions.poehali.dev/8b8a2dac-5db3-41f5-83ed-01e01fd910d2",
  adminPosts:      "https://functions.poehali.dev/1e13ce61-a559-4007-99da-1e06d675990f",
  adminBotPosts:   "https://functions.poehali.dev/2b96994a-6d5c-41bf-ade3-c563f1dfabf2",
  saitBotDaily:    "https://functions.poehali.dev/c6089fab-3f7b-4988-bfb5-9ca38278df99",
  adminBotStories: "https://functions.poehali.dev/ec60a8b1-27ee-4a4b-bad0-d26b3d8a3f30",
  storiesCron:     "https://functions.poehali.dev/ab907d44-fb79-4f80-8244-8dd0b61290ae",
  excludedWatcher: "https://functions.poehali.dev/2936d419-f1b3-4a26-8603-1cd6f5233771",
  tgUserAuth:      "https://functions.poehali.dev/a8ca9420-5401-4d13-b212-869df4bf44ce",
  tgUserAuth2:     "https://functions.poehali.dev/4d894c1d-b7b0-4380-9865-5adea5e69e62",
  uploadVideo:     "https://functions.poehali.dev/bd26b062-6d55-453f-902a-503ef4f75586",
} as const;

// Типы постов
export type PostStatus = "draft" | "published" | "scheduled";

export interface Post {
  id: number;
  title: string;
  text: string;
  photo_url: string;
  video_note_url: string;
  button_text: string;
  button_url: string;
  button2_text: string;
  button2_url: string;
  status: PostStatus;
  chats: string;
  scheduled_at: string | null;
  published_at: string | null;
  telegram_message_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface BotDailyPost {
  id: number;
  photo_url: string;
  greeting: string;
  description: string;
  is_used: boolean;
  scheduled_date: string | null;
  last_tg_status: string | null;
  last_vk_status: string | null;
  last_sent_at: string | null;
  created_at: string;
}

export interface BotStory {
  id: number;
  video_url: string;
  caption: string;
  is_used: boolean;
  last_sent_at: string | null;
  last_status: string | null;
  created_at: string;
}

export interface ExcludedDriver {
  id: number;
  user_id: number | null;
  username: string | null;
  first_name: string | null;
  detected_at: string;
  message_sent: boolean;
  message_sent_at: string | null;
  send_status: string | null;
  is_unreachable: boolean;
}

export interface ExcludedSettings {
  id: number;
  enabled: boolean;
  message_template: string;
  photo_url: string;
  button_text: string;
  button_url: string;
  source_chat: string;
  active_session: number;
  humanize_enabled: boolean;
}
