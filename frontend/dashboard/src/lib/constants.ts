export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export const API_V1 = `${API_BASE}/api/v1`;
export const WS_SCAM_LIVE = `${API_V1.replace(/^http/, "ws")}/scam/ws/live`;

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
