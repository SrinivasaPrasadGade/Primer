export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export const API_V1 = `${API_BASE}/api/v1`;
const WS_SCAM_LIVE_BASE = `${API_V1.replace(/^http/, "ws")}/scam/ws/live`;

/**
 * The live feed is auth-guarded, and a browser can't attach an Authorization
 * header to a WebSocket handshake — so the token goes in the query string.
 * Returns null when there's no token yet, which callers use to skip connecting.
 */
export function wsScamLiveUrl(token: string | null): string | null {
    return token ? `${WS_SCAM_LIVE_BASE}?token=${encodeURIComponent(token)}` : null;
}

export const TOKEN_STORAGE_KEY = "primer_token";
export const USER_STORAGE_KEY = "primer_user";

export type UserRole = "lea_officer" | "bank_manager" | "citizen";

export interface AuthUser {
    id: string;
    email: string;
    name: string;
    role: UserRole;
    designation?: string;
    jurisdiction?: string;
}
