# Nivedita — Frontend & Mobile (Mac M4 Air)

## **Primer — Developer Task Sheet**

| Field | Detail |
|---|---|
| **Owner** | Nivedita |
| **Machine** | MacBook Air M4 |
| **Role** | Web dashboard (Next.js), Citizen mobile app (React Native/Expo), all UI screens |
| **Stack** | Next.js 14, React, CSS Modules, Framer Motion, Mapbox, Sigma.js, React Native, Expo |
| **Companion Docs** | [UI/UX Design](ui_ux_design_document.md) · [App Flow](application_flow_document.md) · [TRD](technical_requirements_document.md) |

---

## 1. Machine Setup

### 1.1 Dev Tools

```bash
# Node.js 20 LTS
brew install node@20

# Expo CLI (for mobile)
npm install -g expo-cli

# iOS Simulator (Xcode from App Store)
# Android: Install Android Studio for emulator (optional — test on physical device)
```

### 1.2 Web Dashboard Setup

```bash
cd primer/frontend/dashboard

# Create Next.js project
npx -y create-next-app@latest ./ --ts --app --src-dir --no-tailwind --no-eslint --import-alias "@/*"

# Install dependencies
npm install swr framer-motion sigma graphology mapbox-gl recharts lucide-react
npm install -D @types/mapbox-gl
```

### 1.3 Mobile App Setup

```bash
cd primer/mobile

# Create Expo project
npx -y create-expo-app@latest ./ --template blank-typescript

# Install dependencies
npx expo install expo-camera expo-barcode-scanner react-native-maps
npm install @react-navigation/native @react-navigation/bottom-tabs react-native-screens react-native-safe-area-context
```

---

## 2. Web Dashboard — Screen List

| # | Screen | Route | Role | Priority |
|---|---|---|---|---|
| 1 | Login | `/login` | All | **P0** |
| 2 | Home Dashboard | `/` | LEA Officer | **P0** |
| 3 | Scam Sentinel — Live Monitor | `/scam` | LEA Officer | **P0** |
| 4 | Scam Session Detail | `/scam/[id]` | LEA Officer | **P0** |
| 5 | Note Verify — Dashboard | `/notes` | Bank Manager | **P0** |
| 6 | Fraud Graph Explorer | `/graph` | LEA Officer | **P0** |
| 7 | Geo Intel — Crime Map | `/geo` | LEA Officer | **P0** |
| 8 | AI Copilot | `/copilot` (or sidebar) | LEA Officer | **P0** |
| 9 | Case Summarizer | `/case` | LEA Officer | **P1** |
| 10 | Notifications | Dropdown | All | **P1** |

**Total: 10 screens.** Not 30+. Focus on making these 10 beautiful.

---

## 3. Project Structure (Dashboard)

```
frontend/dashboard/src/
├── app/
│   ├── layout.tsx          Root layout (navbar + sidebar)
│   ├── page.tsx            Home dashboard
│   ├── login/page.tsx      Login screen
│   ├── scam/
│   │   ├── page.tsx        Live Monitor
│   │   └── [id]/page.tsx   Session Detail
│   ├── notes/page.tsx      Note Verify Dashboard
│   ├── graph/page.tsx      Fraud Graph Explorer
│   ├── geo/page.tsx        Crime Map
│   ├── copilot/page.tsx    AI Copilot
│   └── case/page.tsx       Case Summarizer
│
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   └── PageHeader.tsx
│   ├── dashboard/
│   │   ├── StatCard.tsx
│   │   ├── ThreatLevel.tsx
│   │   └── LiveAlertFeed.tsx
│   ├── scam/
│   │   ├── SessionCard.tsx
│   │   ├── SignalBar.tsx
│   │   ├── SessionDetail.tsx
│   │   └── ExplainableAI.tsx
│   ├── graph/
│   │   ├── GraphCanvas.tsx
│   │   ├── EntityPanel.tsx
│   │   └── CopilotBar.tsx
│   ├── geo/
│   │   ├── CrimeMap.tsx
│   │   └── HeatmapLayer.tsx
│   ├── shared/
│   │   ├── Badge.tsx
│   │   ├── ConfidenceBar.tsx
│   │   ├── Card.tsx
│   │   ├── Drawer.tsx
│   │   └── LoadingSkeleton.tsx
│   └── copilot/
│       ├── ChatInterface.tsx
│       └── ChatMessage.tsx
│
├── hooks/
│   ├── useAuth.ts
│   ├── useWebSocket.ts
│   └── useApi.ts
│
├── lib/
│   ├── api.ts              API client (fetch wrapper)
│   └── constants.ts        API URLs, config
│
└── styles/
    ├── globals.css          Design tokens (from UI/UX doc §3)
    ├── layout.module.css
    ├── dashboard.module.css
    ├── scam.module.css
    ├── graph.module.css
    ├── geo.module.css
    └── copilot.module.css
```

---

## 4. Design Tokens — `globals.css`

Copy directly from [UI/UX Design Document §3](ui_ux_design_document.md). The full CSS variables block goes here.

```css
/* globals.css */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    /* Surfaces */
    --color-bg-primary: #0A0A0F;
    --color-layer-1: #111118;
    --color-layer-2: #16161F;
    --color-layer-3: #1C1C27;
    --color-layer-4: #222233;

    /* Text */
    --color-text-primary: #F5F5F7;
    --color-text-secondary: #AEAEB2;
    --color-text-tertiary: #636366;

    /* Borders */
    --color-border-subtle: rgba(255, 255, 255, 0.06);
    --color-border-default: rgba(255, 255, 255, 0.10);

    /* Accent */
    --accent-500: #3B82F6;
    --accent-600: #2563EB;

    /* Alerts */
    --color-red: #EF4444;
    --color-red-bg: rgba(239, 68, 68, 0.08);
    --color-red-border: rgba(239, 68, 68, 0.20);
    --color-amber: #F59E0B;
    --color-amber-bg: rgba(245, 158, 11, 0.08);
    --color-green: #22C55E;
    --color-green-bg: rgba(34, 197, 94, 0.08);

    /* Typography */
    --font-display: "Inter", -apple-system, sans-serif;
    --font-mono: "JetBrains Mono", monospace;

    /* Spacing */
    --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
    --space-6: 24px; --space-8: 32px;

    /* Radius */
    --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px;
    --radius-xl: 16px; --radius-full: 9999px;

    /* Shadows */
    --shadow-sm: 0 2px 8px rgba(0,0,0,0.12);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.20);
    --shadow-red: 0 4px 24px rgba(239,68,68,0.25);

    /* Easing */
    --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1.0);
    --ease-smooth: cubic-bezier(0.23, 1.0, 0.32, 1.0);

    /* Layout */
    --nav-height: 56px;
    --sidebar-width: 240px;
    --sidebar-collapsed: 64px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background: var(--color-bg-primary);
    color: var(--color-text-primary);
    font-family: var(--font-display);
    font-size: 14px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
}
```

---

## 5. Key Component Implementations

### 5.1 SessionCard (Scam Sentinel)

```tsx
// components/scam/SessionCard.tsx
"use client";
import { motion } from "framer-motion";
import styles from "@/styles/scam.module.css";
import { Badge } from "../shared/Badge";
import { ConfidenceBar } from "../shared/ConfidenceBar";

interface Session {
    id: string;
    caller_number: string;
    callee_number: string;
    alert_level: "RED" | "AMBER" | "YELLOW";
    overall_confidence: number;
    scam_type: string;
    call_duration_sec: number;
    deepfake_detected: boolean;
}

export function SessionCard({ session, onClick }: { session: Session; onClick: () => void }) {
    return (
        <motion.div
            className={`${styles.sessionCard} ${styles[session.alert_level.toLowerCase()]}`}
            onClick={onClick}
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease: [0.23, 1.0, 0.32, 1.0] }}
            whileHover={{ y: -2 }}
        >
            <div className={styles.cardHeader}>
                <Badge level={session.alert_level} />
                <span className={styles.scamType}>{session.scam_type}</span>
                {session.deepfake_detected && <Badge level="AMBER" label="AI Voice" />}
            </div>
            <div className={styles.cardBody}>
                <div className={styles.phoneRow}>
                    <span className={styles.phone}>{session.caller_number}</span>
                    <span className={styles.arrow}>→</span>
                    <span className={styles.phone}>{session.callee_number}</span>
                </div>
                <ConfidenceBar value={session.overall_confidence} />
            </div>
            <div className={styles.cardFooter}>
                <span className={styles.duration}>{formatDuration(session.call_duration_sec)}</span>
                <span className={styles.confidence}>{session.overall_confidence.toFixed(1)}%</span>
            </div>
        </motion.div>
    );
}
```

### 5.2 ExplainableAI (Signal Bars)

```tsx
// components/scam/ExplainableAI.tsx
"use client";
import { motion } from "framer-motion";
import styles from "@/styles/scam.module.css";

interface Signal {
    score: number;
    explanation: string;
}

export function ExplainableAI({ signals }: { signals: Record<string, Signal> }) {
    const signalNames: Record<string, string> = {
        call_flow_match: "Call Flow Match",
        number_spoofing: "Number Spoofing",
        script_similarity: "Script Similarity",
        voice_synthetic: "Deepfake Voice",
        urgency_phrases: "Urgency Phrases",
    };
    const signalIcons: Record<string, string> = {
        call_flow_match: "✔",
        number_spoofing: "✔",
        script_similarity: "✔",
        voice_synthetic: "⚠️",
        urgency_phrases: "✔",
    };

    return (
        <div className={styles.explainableAI}>
            <h3 className={styles.sectionTitle}>Explainable AI — Why This Was Flagged</h3>
            {Object.entries(signals).map(([key, signal], index) => (
                <motion.div
                    key={key}
                    className={styles.signalRow}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.06, duration: 0.4 }}
                >
                    <div className={styles.signalHeader}>
                        <span className={styles.signalIcon}>
                            {signal.score >= 0.7 ? signalIcons[key] : "⚠️"}
                        </span>
                        <span className={styles.signalName}>{signalNames[key]}</span>
                        <span className={styles.signalScore}>{(signal.score * 100).toFixed(0)}%</span>
                    </div>
                    <div className={styles.signalBar}>
                        <motion.div
                            className={styles.signalFill}
                            initial={{ width: 0 }}
                            animate={{ width: `${signal.score * 100}%` }}
                            transition={{ delay: index * 0.06 + 0.2, duration: 0.8, ease: [0.23, 1, 0.32, 1] }}
                            style={{
                                background: signal.score >= 0.85
                                    ? "var(--color-red)"
                                    : signal.score >= 0.6
                                    ? "var(--color-amber)"
                                    : "var(--accent-500)"
                            }}
                        />
                    </div>
                    <p className={styles.signalExplanation}>{signal.explanation}</p>
                </motion.div>
            ))}
        </div>
    );
}
```

### 5.3 GraphCanvas (Fraud Graph)

```tsx
// components/graph/GraphCanvas.tsx
"use client";
import { useEffect, useRef } from "react";
import Graph from "graphology";
import Sigma from "sigma";
import styles from "@/styles/graph.module.css";

const NODE_COLORS: Record<string, string> = {
    phone_number: "#3B82F6",
    bank_account: "#22C55E",
    upi_id: "#F59E0B",
    person: "#F97316",
    device: "#A855F7",
    complaint: "#EF4444",
};

export function GraphCanvas({ data, onNodeClick }: { data: any; onNodeClick: (id: string) => void }) {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!containerRef.current || !data) return;

        const graph = new Graph();

        // Add nodes
        data.nodes.forEach((node: any) => {
            graph.addNode(node.id, {
                label: node.display_label || node.entity_value,
                size: Math.max(8, (node.risk_score || 10) / 5),
                color: NODE_COLORS[node.entity_type] || "#666",
                x: Math.random() * 100,
                y: Math.random() * 100,
            });
        });

        // Add edges
        data.edges.forEach((edge: any) => {
            if (graph.hasNode(edge.source_id) && graph.hasNode(edge.target_id)) {
                graph.addEdge(edge.source_id, edge.target_id, {
                    label: edge.relationship,
                    size: Math.max(1, (edge.weight || 1) / 100),
                    color: "rgba(255,255,255,0.15)",
                });
            }
        });

        // Render with Sigma
        const renderer = new Sigma(graph, containerRef.current, {
            renderEdgeLabels: true,
            defaultNodeColor: "#666",
            defaultEdgeColor: "rgba(255,255,255,0.1)",
        });

        renderer.on("clickNode", ({ node }) => onNodeClick(node));

        return () => renderer.kill();
    }, [data, onNodeClick]);

    return <div ref={containerRef} className={styles.graphCanvas} />;
}
```

### 5.4 WebSocket Hook (Live Feed)

```tsx
// hooks/useWebSocket.ts
"use client";
import { useEffect, useRef, useState, useCallback } from "react";

export function useWebSocket<T>(url: string) {
    const [messages, setMessages] = useState<T[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const ws = useRef<WebSocket | null>(null);

    useEffect(() => {
        ws.current = new WebSocket(url);

        ws.current.onopen = () => setIsConnected(true);
        ws.current.onclose = () => {
            setIsConnected(false);
            // Auto-reconnect after 3 seconds
            setTimeout(() => {
                ws.current = new WebSocket(url);
            }, 3000);
        };
        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages(prev => [data, ...prev].slice(0, 100)); // Keep last 100
        };

        return () => ws.current?.close();
    }, [url]);

    return { messages, isConnected };
}
```

---

## 6. Mobile App — Screen List

| # | Screen | Tab | Priority |
|---|---|---|---|
| 1 | Home | Home | **P0** |
| 2 | Note Scanner | Scan | **P0** |
| 3 | Scan Result | Scan | **P0** |
| 4 | QR Scanner | Scan | **P0** |
| 5 | QR Result | Scan | **P0** |
| 6 | Number Check | Home | **P1** |
| 7 | AI Chat | Chat | **P0** |
| 8 | Panic SOS | (overlay) | **P0** |

### Mobile Project Structure

```
mobile/
├── App.tsx                 Navigation setup
├── screens/
│   ├── HomeScreen.tsx
│   ├── NoteScannerScreen.tsx
│   ├── ScanResultScreen.tsx
│   ├── QRScannerScreen.tsx
│   ├── QRResultScreen.tsx
│   ├── NumberCheckScreen.tsx
│   ├── ChatScreen.tsx
│   └── PanicScreen.tsx
├── components/
│   ├── Badge.tsx
│   ├── RiskCard.tsx
│   ├── FeatureGrid.tsx
│   └── ChatBubble.tsx
├── hooks/
│   └── useApi.ts
├── constants/
│   ├── colors.ts           Design tokens
│   └── api.ts              API URLs
└── assets/
    └── models/
        └── note_auth_net.tflite
```

### Mobile Navigation

```tsx
// App.tsx
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

const Tab = createBottomTabNavigator();

export default function App() {
    return (
        <NavigationContainer>
            <Tab.Navigator screenOptions={{
                tabBarStyle: { backgroundColor: "#0A0A0F", borderTopColor: "rgba(255,255,255,0.06)" },
                tabBarActiveTintColor: "#3B82F6",
                tabBarInactiveTintColor: "#636366",
            }}>
                <Tab.Screen name="Home" component={HomeScreen} />
                <Tab.Screen name="Scan" component={ScanNavigator} />
                <Tab.Screen name="Chat" component={ChatScreen} />
                <Tab.Screen name="Profile" component={ProfileScreen} />
            </Tab.Navigator>
        </NavigationContainer>
    );
}
```

---

## 7. API Client

```tsx
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
    private token: string | null = null;

    setToken(token: string) { this.token = token; }

    async fetch<T>(path: string, options: RequestInit = {}): Promise<T> {
        const res = await fetch(`${API_BASE}/api/v1${path}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
                ...options.headers,
            },
        });
        if (!res.ok) throw new Error(`API Error: ${res.status}`);
        return res.json();
    }

    // Scam Sentinel
    getScamSessions = (params?: string) => this.fetch(`/scam/sessions${params ? `?${params}` : ""}`);
    getScamSession = (id: string) => this.fetch(`/scam/sessions/${id}`);
    getScamStats = () => this.fetch("/scam/stats");

    // Note Verify
    verifyNote = (image: string) => this.fetch("/note/verify", { method: "POST", body: JSON.stringify({ image_base64: image }) });

    // Fraud Graph
    getEntity = (type: string, id: string) => this.fetch(`/graph/entity/${type}/${id}`);
    getCluster = (id: string) => this.fetch(`/graph/cluster/${id}`);

    // Geo Intel
    getHeatmap = (bounds: string) => this.fetch(`/geo/heatmap?bounds=${bounds}`);
    getIncidents = (bounds: string) => this.fetch(`/geo/incidents?bounds=${bounds}`);

    // AI Copilot
    askCopilot = (question: string) => this.fetch("/copilot/query", { method: "POST", body: JSON.stringify({ question }) });

    // QR Scanner
    scanQR = (content: string) => this.fetch("/qr/scan", { method: "POST", body: JSON.stringify({ qr_content: content }) });

    // Call Screening
    screenNumber = (phone: string) => this.fetch(`/screen/number/${phone}`);
}

export const api = new ApiClient();
```

---

## 8. Task Checklist (Phase 4: Nivedita)

### 1. Web Dashboard Shell & Core UI
- [x] Next.js project setup (App Router, CSS Modules)
- [x] `globals.css` with all design tokens
- [x] Login page (email + password → JWT)
- [x] Root layout: Navbar (glassmorphism) + Sidebar + main area
- [x] Home Dashboard: stat cards, threat level, mini map, live alert feed
- [x] Scam Sentinel: Live Monitor (session cards with RED/AMBER/YELLOW)
- [x] Scam Sentinel: Session Detail with Explainable AI signal bars
- [x] RED card pulse animation
- [x] Fraud Graph Explorer (Sigma.js canvas + entity detail panel)
- [x] Geo Intel: Mapbox crime map with heatmap + Prediction zone overlay
- [x] AI Copilot chat bar in graph view + full chat interface page
- [x] Case Summarizer: upload → result display
- [x] Note Verify: bank manager dashboard view
- [x] Notification dropdown

### 2. Mobile App Setup
- [x] Expo project setup
- [x] Mobile Home screen with feature grid
- [x] Mobile Note Scanner (camera integration)
- [x] Mobile QR Scanner screen (camera → decode → result)
- [x] Mobile Call Screening overlay (simulated incoming call)
- [x] Mobile Panic Button screen
- [x] Mobile AI Chat screen
- [x] Number Check screen

### 3. Integration & Demo Polish
- [x] All screens connected to live APIs
- [x] Loading skeletons everywhere
- [x] Error states (empty, offline, 404)
- [x] Animations smooth at 60fps
- [ ] Mobile tested on physical device
- [ ] Dashboard tested on external display / projector
- [ ] Demo rehearsal run-through
