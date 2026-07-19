import { API_V1, AuthUser, TOKEN_STORAGE_KEY } from "./constants";

const DEFAULT_TIMEOUT_MS = 30_000;
// LLM-backed endpoints do real work per request and are legitimately slower.
const AI_TIMEOUT_MS = 90_000;

export class ApiError extends Error {
    status: number;
    constructor(status: number, detail: string) {
        super(detail);
        this.status = status;
    }
}

function qs(params: Record<string, string | number | boolean | undefined | null>): string {
    const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== "");
    if (entries.length === 0) return "";
    return "?" + entries.map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`).join("&");
}

class ApiClient {
    private token: string | null = null;

    setToken(token: string | null) {
        this.token = token;
        if (typeof window === "undefined") return;
        if (token) window.localStorage.setItem(TOKEN_STORAGE_KEY, token);
        else window.localStorage.removeItem(TOKEN_STORAGE_KEY);
    }

    loadToken() {
        if (typeof window === "undefined") return null;
        this.token = window.localStorage.getItem(TOKEN_STORAGE_KEY);
        return this.token;
    }

    getToken() {
        return this.token;
    }

    private async request<T>(path: string, options: RequestInit & { timeoutMs?: number } = {}): Promise<T> {
        // Without a deadline a stalled request leaves the caller's `loading` state
        // set forever, which reads as a spinner that never resolves.
        const { timeoutMs = DEFAULT_TIMEOUT_MS, ...init } = options;
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), timeoutMs);

        let res: Response;
        try {
            res = await fetch(`${API_V1}${path}`, {
                ...init,
                signal: controller.signal,
                headers: {
                    "Content-Type": "application/json",
                    ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
                    ...init.headers,
                },
            });
        } catch (err) {
            if (err instanceof DOMException && err.name === "AbortError") {
                throw new ApiError(408, `Request timed out after ${Math.round(timeoutMs / 1000)}s. The server may be unreachable.`);
            }
            throw err;
        } finally {
            clearTimeout(timer);
        }
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

    private get<T>(path: string) {
        return this.request<T>(path, { method: "GET" });
    }
    private post<T>(path: string, body?: unknown, timeoutMs?: number) {
        return this.request<T>(path, {
            method: "POST",
            body: body !== undefined ? JSON.stringify(body) : undefined,
            timeoutMs,
        });
    }

    // Auth
    login = (email: string, password: string) =>
        this.post<{ access_token: string; token_type: string; user: AuthUser }>("/auth/login", { email, password });
    me = () => this.get<AuthUser>("/auth/me");

    // Scam Sentinel
    getScamSessions = (params?: { alert_level?: string; status?: string; limit?: number; offset?: number }) =>
        this.get<ScamSession[]>(`/scam/sessions${qs(params ?? {})}`);
    getScamSession = (id: string) => this.get<ScamSessionDetail>(`/scam/sessions/${id}`);
    classifyScamSession = (id: string) => this.post(`/scam/sessions/${id}/classify`);
    acknowledgeScamSession = (id: string) => this.post(`/scam/sessions/${id}/acknowledge`);
    getNumberReputation = (phone: string) => this.get(`/scam/numbers/${encodeURIComponent(phone)}`);
    flagNumber = (phone: string, alert_level: string) =>
        this.post(`/scam/numbers/${encodeURIComponent(phone)}/flag`, { alert_level });
    getScamStats = () => this.get<ScamStats>("/scam/stats");

    // Note Verify
    verifyNote = (payload: {
        image_base64: string;
        denomination?: number;
        serial_number?: string;
        scan_source?: "mobile" | "web" | "scanner";
        lat?: number;
        lng?: number;
    }) => this.post<NoteVerifyResult>("/note/verify", payload);
    getNoteHistory = (limit?: number) => this.get<NoteHistoryEntry[]>(`/note/history${qs({ limit })}`);
    getNoteStats = () => this.get<NoteStats>("/note/stats");
    getNoteSerial = (serial: string) => this.get(`/note/serials/${encodeURIComponent(serial)}`);

    // Fraud Graph
    getEntity = (type: string, value: string, depth = 2) =>
        this.get<GraphData>(`/graph/entity/${type}/${encodeURIComponent(value)}${qs({ depth })}`);
    getCluster = (id: string) => this.get(`/graph/cluster/${id}`);
    getMoneyFlow = (entityId: string) => this.get<MoneyFlowEdge[]>(`/graph/money-flow/${entityId}`);
    searchGraph = (query: string, limit = 20) => this.post<GraphSearchResult[]>(`/graph/search`, { query, limit });
    generateDossier = (clusterId: string) => this.post<{ pdf_path: string }>(`/graph/dossier/${clusterId}`);
    detectCommunities = (minClusterSize = 3) =>
        this.post(`/graph/communities/detect${qs({ min_cluster_size: minClusterSize })}`);

    // Geo Intel
    getHeatmap = (bounds: string, type?: string, days?: number) =>
        this.get<HeatmapCell[]>(`/geo/heatmap${qs({ bounds, type, days })}`);
    getIncidents = (bounds: string, type?: string, limit?: number) =>
        this.get<GeoIncident[]>(`/geo/incidents${qs({ bounds, type, limit })}`);
    getPredictions = (bounds: string, predictionDate?: string) =>
        this.get<HotspotPrediction[]>(`/geo/predictions${qs({ bounds, prediction_date: predictionDate })}`);
    // Scores a grid of points with the hotspot model, one DB round trip per point —
    // legitimately slower than a normal request.
    generatePredictions = (bounds: string, type?: string, gridKm?: number, riskThreshold?: number) =>
        this.post<HotspotPrediction[]>(
            `/geo/predictions/generate${qs({ bounds, type, grid_km: gridKm, risk_threshold: riskThreshold })}`,
            undefined,
            AI_TIMEOUT_MS,
        );
    getGeoStats = () => this.get("/geo/stats");

    // Citizen Shield
    citizenChat = (message: string, sessionId?: string | null) =>
        this.post<{ session_id: string; reply: string }>("/citizen/chat", { message, session_id: sessionId ?? null });
    getCitizenChatHistory = (sessionId: string) => this.get(`/citizen/chat/${sessionId}/history`);
    closeCitizenChat = (sessionId: string) => this.post(`/citizen/chat/${sessionId}/close`);
    numberCheck = (phone: string) => this.get(`/citizen/number-check/${encodeURIComponent(phone)}`);

    // Extra features
    askCopilot = (question: string) =>
        this.post<{
            available?: boolean;
            answer: string;
            data: unknown[];
            sources: string[];
            query_executed: { tool: string; args: Record<string, unknown> }[];
        }>(
            "/copilot/query",
            { question },
            AI_TIMEOUT_MS,
        );
    scanQR = (qrContent: string) => this.post("/qr/scan", { qr_content: qrContent });
    summarizeCase = (entityType: string, entityValue: string, investigationId?: string | null) =>
        this.post<CaseSummary>(
            "/case/summarize",
            { entity_type: entityType, entity_value: entityValue, investigation_id: investigationId ?? null },
            AI_TIMEOUT_MS,
        );
    triggerPanic = (payload: {
        caller_number?: string;
        call_duration_sec?: number;
        location?: { lat: number; lng: number };
        emergency_contact_number?: string;
    }) => this.post("/panic/trigger", payload);
    screenNumber = (phone: string) => this.get(`/screen/number/${encodeURIComponent(phone)}`);
}

export interface SignalScore {
    score: number;
    explanation: string;
}

export interface ScamSession {
    id: string;
    caller_number: string;
    callee_number: string;
    alert_level: "RED" | "AMBER" | "YELLOW";
    overall_confidence: number;
    scam_type: string;
    call_duration_sec: number;
    deepfake_detected: boolean;
    status?: string;
    created_at?: string;
}

export interface ScamSessionDetail extends ScamSession {
    signal_scores: Record<string, SignalScore>;
}

export interface ScamStats {
    total_sessions?: number;
    red_count?: number;
    amber_count?: number;
    yellow_count?: number;
    /** Sessions still awaiting classification. */
    active_count?: number;
    /** Sessions an officer has closed out. */
    closed_count?: number;
    avg_confidence?: number;
    [key: string]: unknown;
}

export interface NoteVerifyResult {
    id: string;
    verdict: "GENUINE" | "SUSPECT" | "COUNTERFEIT";
    confidence: number;
    denomination: number;
    serial_number: string | null;
    scan_source: string;
    is_known_counterfeit: boolean;
    feature_analysis: Record<string, number>;
    created_at: string;
}

export interface NoteHistoryEntry {
    id: string;
    denomination: number;
    serial_number: string | null;
    verdict: "GENUINE" | "SUSPECT" | "COUNTERFEIT";
    confidence: number;
    scan_source: string;
    created_at: string;
}

export interface NoteStats {
    total_scans: number;
    genuine_count: number;
    suspect_count: number;
    counterfeit_count: number;
}

export interface GraphNode {
    id: string;
    entity_type: string;
    entity_value?: string;
    display_label?: string;
    risk_score?: number;
}

export interface GraphEdge {
    source_id: string;
    target_id: string;
    relationship: string;
    weight?: number;
}

export interface GraphData {
    nodes: GraphNode[];
    edges: GraphEdge[];
}

export interface GraphSearchResult {
    id: string;
    entity_type: string;
    entity_value: string;
    display_label: string | null;
    risk_score: number | null;
    cluster_id: string | null;
}

export interface CaseSummary {
    id: string;
    investigation_id: string | null;
    summary_text: string;
    timeline_json: Array<{ date?: string; event?: string; [key: string]: unknown }>;
    suspects_json: Array<{ identifier?: string; name?: string; role?: string; [key: string]: unknown }>;
    related_complaints: string[];
    confidence_score: number;
    source_evidence: string[];
    generated_by: string;
    created_at: string;
}

export interface HeatmapCell {
    lng: number;
    lat: number;
    intensity: number;
    crime_type: string;
}

export interface GeoIncident {
    id: string;
    crime_type: string;
    title: string;
    description: string;
    lng: number;
    lat: number;
    severity: string;
    estimated_loss: number;
    reported_at: string;
}

export interface HotspotPrediction {
    id: string;
    prediction_date: string;
    crime_type: string;
    lng: number;
    lat: number;
    radius_km: number;
    risk_score: number;
    model_version: string;
}

export interface MoneyFlowEdge {
    id: string;
    source_id: string;
    target_id: string;
    amount: number;
    first_seen: string;
    from_entity: string;
    from_type: string;
    to_entity: string;
    to_type: string;
}

export const api = new ApiClient();
