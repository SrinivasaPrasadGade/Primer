import { useCallback, useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { API_V1, DEMO_CITIZEN_EMAIL, DEMO_CITIZEN_PASSWORD, TOKEN_STORAGE_KEY } from "../constants/api";

export class ApiError extends Error {
    status: number;
    constructor(status: number, detail: string) {
        super(detail);
        this.status = status;
    }
}

class ApiClient {
    private token: string | null = null;
    private loginPromise: Promise<string> | null = null;

    private async request<T>(path: string, options: RequestInit = {}, requireAuth = true): Promise<T> {
        if (requireAuth && !this.token) await this.ensureLoggedIn();

        const res = await fetch(`${API_V1}${path}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
                ...options.headers,
            },
        });
        if (!res.ok) {
            let detail = res.statusText;
            try {
                const body = await res.json();
                detail = body.detail ?? detail;
            } catch {
                // no JSON body
            }
            throw new ApiError(res.status, detail);
        }
        if (res.status === 204) return undefined as T;
        return res.json();
    }

    async ensureLoggedIn(): Promise<string> {
        if (this.token) return this.token;
        if (this.loginPromise) return this.loginPromise;

        this.loginPromise = (async () => {
            const cached = await AsyncStorage.getItem(TOKEN_STORAGE_KEY);
            if (cached) {
                this.token = cached;
                return cached;
            }
            const res = await fetch(`${API_V1}/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: DEMO_CITIZEN_EMAIL, password: DEMO_CITIZEN_PASSWORD }),
            });
            if (!res.ok) throw new ApiError(res.status, "Unable to sign in as demo citizen");
            const data = await res.json();
            this.token = data.access_token;
            await AsyncStorage.setItem(TOKEN_STORAGE_KEY, data.access_token);
            return data.access_token as string;
        })();

        try {
            return await this.loginPromise;
        } finally {
            this.loginPromise = null;
        }
    }

    private get<T>(path: string, requireAuth = true) {
        return this.request<T>(path, { method: "GET" }, requireAuth);
    }
    private post<T>(path: string, body?: unknown, requireAuth = true) {
        return this.request<T>(path, { method: "POST", body: body !== undefined ? JSON.stringify(body) : undefined }, requireAuth);
    }

    // `denomination` is required, and constrained to the values the API accepts.
    // NoteAuthNet scores authenticity only — it has no denomination head — so the
    // backend takes this from the caller and rejects anything else with a 422.
    // Optional here would push that failure to runtime.
    verifyNote = (payload: { image_base64: string; denomination: NoteDenomination; scan_source?: "mobile" | "web" | "scanner"; lat?: number; lng?: number }) =>
        this.post<NoteVerifyResult>("/note/verify", payload);

    scanQR = (qrContent: string) => this.post<QRScanResult>("/qr/scan", { qr_content: qrContent });

    numberCheck = (phone: string) => this.get<NumberCheckResult>(`/citizen/number-check/${encodeURIComponent(phone)}`, false);
    screenNumber = (phone: string) => this.get<ScreenNumberResult>(`/screen/number/${encodeURIComponent(phone)}`);

    citizenChat = (message: string, sessionId?: string | null) =>
        this.post<CitizenChatResponse>("/citizen/chat", { message, session_id: sessionId ?? null });

    triggerPanic = (payload: {
        caller_number?: string;
        call_duration_sec?: number;
        location?: { lat: number; lng: number };
        emergency_contact_number?: string;
    }) => this.post<PanicResult>("/panic/trigger", payload);

    me = () => this.get<AuthUser>("/auth/me");
}

export interface AuthUser {
    id: string;
    email: string;
    name: string;
    role: string;
    designation?: string;
    jurisdiction?: string;
}

/** Mirrors the `Literal[...]` on NoteVerifyRequest.denomination in the backend. */
export const NOTE_DENOMINATIONS = [10, 20, 50, 100, 200, 500, 2000] as const;
export type NoteDenomination = (typeof NOTE_DENOMINATIONS)[number];

export interface NoteVerifyResult {
    id: string;
    verdict: "GENUINE" | "SUSPECT" | "COUNTERFEIT";
    confidence: number;
    denomination: number;
    feature_analysis: Record<string, number>;
    is_known_counterfeit: boolean;
}

export interface QRScanResult {
    id: string;
    qr_content: string;
    content_type: string;
    destination_account: string | null;
    destination_url: string | null;
    risk_level: string;
    risk_score: number;
    complaint_count: number;
    explanation: string;
    flags: string[];
    scanned_at: string;
}

export interface NumberCheckResult {
    phone: string;
    risk_score: number;
    is_blacklisted: boolean;
    message?: string;
    total_flags?: number;
    total_complaints?: number;
}

// The backend's first-turn response (no session_id in the request) returns the new
// session's identifier as `id`; every subsequent turn returns it as `session_id`.
export interface CitizenChatResponse {
    id?: string;
    session_id?: string;
    reply: string;
    risk_assessment?: string;
}

// Field names mirror the /panic/trigger response exactly. They previously did not
// (`id`/`fraud_report_path` vs the API's `report_id`/`fraud_report_url`), so every
// read of them was silently undefined.
export interface PanicResult {
    report_id: string;
    // Stays false until something actually sends a notification; `on_file` only
    // means a number was supplied.
    emergency_contact_notified: boolean;
    emergency_contact_on_file: boolean;
    fraud_report_generated: boolean;
    fraud_report_url: string | null;
    triggered_at: string;
}

export interface ScreenNumberResult {
    risk_level: string;
    risk_score: number;
    flags: string[];
    recommendation: string;
}

export const api = new ApiClient();

// Generic on-demand fetch hook for screens that load data on mount.
export function useApi<T>(fetcher: () => Promise<T>, deps: unknown[] = []) {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const run = useCallback(() => {
        setLoading(true);
        setError(null);
        fetcher()
            .then(setData)
            .catch((err) => setError(err instanceof Error ? err.message : "Something went wrong"))
            .finally(() => setLoading(false));
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, deps);

    useEffect(() => {
        run();
    }, [run]);

    return { data, loading, error, refetch: run };
}
