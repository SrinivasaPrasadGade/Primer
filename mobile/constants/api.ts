export const API_BASE = process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000";
export const API_V1 = `${API_BASE}/api/v1`;

// MVP demo auth: the citizen mobile app has no login screen (see task sheet),
// so it signs in as the seeded citizen demo user on launch.
export const DEMO_CITIZEN_EMAIL = "sumanth@primer.demo";
export const DEMO_CITIZEN_PASSWORD = "Primer@2026";

export const TOKEN_STORAGE_KEY = "primer_mobile_token";
// Persisting the chat session id is what lets an interrupted conversation be
// restored from /citizen/chat/{id}/history after the app is reopened.
export const CHAT_SESSION_STORAGE_KEY = "primer_mobile_chat_session";
