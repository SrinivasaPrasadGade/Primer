# Application Flow Document

## **Primer — AI-Powered Digital Public Safety Intelligence Platform**

| Field | Detail |
|---|---|
| **Document Version** | 2.0 — Hackathon MVP |
| **Date** | 5 July 2026 |
| **Companion Documents** | [PRD](product_requirements_document.md) · [TRD](technical_requirements_document.md) |

---

## 1. Platform Entry Points

```mermaid
graph TB
    subgraph "Entry Points"
        WEB["🖥️ Web Dashboard<br/>localhost:3000<br/>(LEA Officer, Bank Manager)"]
        APP["📱 Citizen Mobile App<br/>Expo (Android/iOS)<br/>(Citizens)"]
    end

    subgraph "Web Dashboard Modules"
        WEB --> HOME["Home / Overview"]
        HOME --> M1["Scam Sentinel"]
        HOME --> M2["Note Verify"]
        HOME --> M3["Fraud Graph"]
        HOME --> M4["Geo Intel"]
        HOME --> M5["AI Copilot"]
        HOME --> M6["Case Summarizer"]
    end

    subgraph "Citizen App Features"
        APP --> SCAN["📸 Scan Note"]
        APP --> QR["🔲 QR Scanner"]
        APP --> CHECK["🔍 Check Number"]
        APP --> CHAT["💬 Chat with AI"]
        APP --> PANIC["🆘 Panic Button"]
        APP --> SCREEN["📞 Call Screening"]
    end
```

---

## 2. Demo Roles & Access

| Screen | Yashi (LEA Officer) | Srinivas (Bank Manager) | Sumanth (Citizen) |
|---|---|---|---|
| Home Dashboard | ✅ Full | ✅ Limited | ❌ |
| Scam Sentinel | ✅ Full | ❌ | ❌ |
| Note Verify | ✅ Analytics | ✅ Full (scan + history) | ❌ |
| Fraud Graph | ✅ Full | ❌ | ❌ |
| Geo Intel | ✅ Full | ❌ | ❌ |
| AI Copilot | ✅ Full | ❌ | ❌ |
| Case Summarizer | ✅ Full | ❌ | ❌ |
| Mobile App | ❌ | ❌ | ✅ Full |

---

## 3. Authentication Flow

```mermaid
graph TD
    A["User visits dashboard<br/>or opens app"] --> B{"Existing token?"}
    B -->|Valid JWT| C["Redirect to Home"]
    B -->|No / Expired| D["Login Screen"]
    
    D --> E["Enter email + password"]
    E --> F{"Valid?"}
    F -->|No| G["❌ Invalid credentials"]
    G --> D
    F -->|Yes| H["Issue JWT (24h expiry)"]
    H --> C

    C --> I{"Role?"}
    I -->|lea_officer| J["Full Dashboard"]
    I -->|bank_manager| K["Note Verify Dashboard"]
    I -->|citizen| L["Mobile App Home"]
```

No MFA, no onboarding wizard, no account lockout for MVP.

---

## 4. Flow 1 — Home Dashboard (LEA Officer)

```
┌──────────────────────────────────────────────────────────────────────┐
│  🛡️ Primer     [🔍 Search number, account...]     [🔔 3]  [👤 Yashi]│
├────────────┬─────────────────────────────────────────────────────────┤
│            │                                                         │
│  📊 Home ● │  Good Morning, Yashi                                   │
│            │  Mumbai Suburban Cyber Cell · Last 24 hours             │
│  🚨 Scam   │                                                        │
│  Sentinel  │  ┌─────────┬─────────┬─────────┬─────────┐            │
│            │  │ 🚨 47   │ 💵 12   │ 🕸️ 3    │ 📍 891  │            │
│  💵 Note   │  │ Active  │ FICN    │ Fraud   │ Total   │            │
│  Verify    │  │ Scam    │ Flagged │ Clusters│ Incidents│           │
│            │  │ Alerts  │ Today   │ Found   │ (24h)   │            │
│  🕸️ Fraud  │  └─────────┴─────────┴─────────┴─────────┘            │
│  Graph     │                                                         │
│            │  ┌────────────────────────────────────────────┐         │
│  🗺️ Geo    │  │  📊 THREAT LEVEL: ELEVATED                │         │
│  Intel     │  │  ▰▰▰▰▰▰▰▰▱▱  78/100                     │         │
│            │  │  Primary driver: Digital arrest scam surge │         │
│  🤖 AI     │  └────────────────────────────────────────────┘         │
│  Copilot   │                                                         │
│            │  ┌──────────────────┐  ┌──────────────────────┐        │
│  📋 Case   │  │  LIVE ALERT FEED │  │  CRIME MAP (MINI)    │        │
│  Summary   │  │  ────────────────│  │  [Interactive Map]    │        │
│            │  │  🔴 14:23 RED    │  │  [Open Full Map →]   │        │
│            │  │  Digital arrest  │  └──────────────────────┘        │
│            │  │  +91-98XX..      │                                   │
│            │  │  [View Details]  │                                   │
│            │  └──────────────────┘                                   │
└────────────┴─────────────────────────────────────────────────────────┘
```

---

## 5. Flow 2 — Scam Sentinel (Live Monitor)

```mermaid
graph TD
    A["Navigate to Scam Sentinel"] --> B["Live Session Feed<br/>(WebSocket auto-updates)"]
    
    B --> C["Session cards show:<br/>• Alert level 🔴/🟡/🟢<br/>• Caller ↔ Callee numbers<br/>• Duration (live counter)<br/>• Confidence score<br/>• Explainable AI signals"]
    
    C --> D{"Click session?"}
    D -->|Yes| E["Session Detail Drawer"]
    
    E --> F["Explainable AI Tab"]
    F --> G["Signal bars:<br/>✔ Call Flow Match: 94%<br/>✔ Number Spoofing: 88%<br/>✔ Script Similarity: 91%<br/>✔ Voice Synthetic: 73%<br/>✔ Urgency Phrases: 96%"]
    
    E --> H["Actions Tab"]
    H --> I["Acknowledge Alert"]
    H --> J["Flag Number"]
    H --> K["Create Investigation"]
```

### Scam Session Detail Screen

```
┌──────────────────────────────────────────────────────────────────────┐
│  ← Back to Live Monitor                                             │
│                                                                      │
│  Session: SSN-2026-07-05-14234                    Status: 🔴 ACTIVE │
│                                                                      │
│  Caller: +91-9876-XXXXX4 (Spoofed ⚠️)    Callee: +91-7890-XXXXX7  │
│  Duration: 00:15:22 (live)                                           │
│                                                                      │
│  EXPLAINABLE AI — WHY THIS WAS FLAGGED               CONFIDENCE     │
│  ─────────────────────────────────────              ┌────────────┐  │
│                                                      │   91.5%    │  │
│  ✔ Call Flow Match        ▰▰▰▰▰▰▰▰▰▱  94%         │   HIGH     │  │
│    "Matches digital arrest pattern (CBI variant)"    │   RISK     │  │
│                                                      └────────────┘  │
│  ✔ Number Spoofing        ▰▰▰▰▰▰▰▰▱▱  88%                        │
│    "CLI mismatch: presented as +91, origin Myanmar"                  │
│                                                                      │
│  ✔ Script Similarity      ▰▰▰▰▰▰▰▰▰▱  91%                        │
│    "Matches template #47 — seen 240 times"                           │
│                                                                      │
│  ⚠️ Deepfake Voice        ▰▰▰▰▰▰▰▱▱▱  73%                        │
│    "Spectral anomalies in 2-4kHz; possible AI synthesis"             │
│                                                                      │
│  ✔ Urgency Phrases        ▰▰▰▰▰▰▰▰▰▰  96%                        │
│    "Detected: arrest warrant, immediate transfer, FIR"               │
│                                                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                │
│  │ ✅ Acknowledge│ │ 🚫 Flag     │ │ 📋 Create    │                │
│  │              │ │ Number       │ │ Investigation│                │
│  └──────────────┘ └──────────────┘ └──────────────┘                │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 6. Flow 3 — Note Verify (Currency Scanner)

### 6.1 Mobile App — Scan Flow

```mermaid
graph TD
    A["User taps '💵 Scan Note'"] --> B["Camera opens with<br/>guided overlay frame"]
    B --> C["Quality check<br/>(blur, lighting, framing)"]
    
    C --> D{"Quality OK?"}
    D -->|Blurry| E["⚠️ 'Hold steady'"]
    D -->|Dark| F["⚠️ 'Need more light'"]
    E --> C
    F --> C
    
    D -->|Good| G["📸 Auto-capture"]
    G --> H["⏳ Analysing... (1-3s)"]
    H --> I{"Verdict?"}
    
    I -->|GENUINE| J["✅ Green screen<br/>Confidence: 96%"]
    I -->|SUSPECT| K["⚠️ Yellow screen<br/>'Scan the back'"]
    I -->|COUNTERFEIT| L["🚫 Red screen<br/>Confidence: 94%"]
    
    J --> M["Feature breakdown<br/>(expandable)"]
    K --> M
    L --> M
    
    L --> N["Action: Report + Location"]
```

### 6.2 Result Screen

```
┌─────────────────────────────────────┐
│  ← Scan Result                      │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │  [Annotated note image with    │ │
│  │   problem areas highlighted]   │ │
│  └─────────────────────────────────┘ │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │  🚫  COUNTERFEIT DETECTED       │ │
│  │  Denomination: ₹500             │ │
│  │  Confidence: 94.2%              │ │
│  │  Serial: 2AB 012345             │ │
│  │  ⚠️ Known in counterfeit DB    │ │
│  └─────────────────────────────────┘ │
│                                      │
│  Feature Analysis               [▾] │
│  ✅ Watermark         Pass  98%      │
│  ✅ Security Thread   Pass  95%      │
│  ❌ Microprint        FAIL  23%      │
│  ✅ Intaglio Print    Pass  91%      │
│  ⚠️ Colour Shift     Warn  61%      │
│  ❌ Serial Number     Known FICN     │
│                                      │
│  ┌──────────┐  ┌──────────────────┐  │
│  │ 📸 Scan  │  │ 📍 Report This   │  │
│  │ Back     │  │ Note             │  │
│  └──────────┘  └──────────────────┘  │
└─────────────────────────────────────┘
```

---

## 7. Flow 4 — Fraud Graph Explorer

```mermaid
graph TD
    A["Navigate to Fraud Graph"] --> B["Search entity:<br/>phone / account / UPI"]
    
    B --> C{"Found?"}
    C -->|No| D["❌ Not found"]
    C -->|Yes| E["Interactive Graph<br/>(2-hop neighbourhood)"]
    
    E --> F{"User action?"}
    F -->|Click node| G["Node detail panel<br/>(risk score, connections)"]
    F -->|Expand node| H["Load +1 hop neighbours"]
    F -->|Ask AI Copilot| I["Natural language query"]
    F -->|Generate dossier| J["PDF evidence package"]
    
    I --> K["AI processes query →<br/>structured DB query →<br/>formatted results"]
```

### Graph Explorer Screen

```
┌──────────────────────────────────────────────────────────────────────┐
│  Fraud Graph > Explorer                                              │
│  Search: [+91-9876543210       🔍]  Depth: [2 hops ▾]              │
│                                                                      │
│  ┌────────────────────────────────────────┬───────────────────────┐  │
│  │                                        │  ENTITY DETAIL        │  │
│  │       INTERACTIVE GRAPH CANVAS        │  ──────────────        │  │
│  │                                        │                       │  │
│  │            ●━━━●                       │  📱 +91-9876543210    │  │
│  │           ╱     ╲                      │  Risk: 🔴 92/100     │  │
│  │         ●        ●━━━●                 │  Flags: 14            │  │
│  │        ╱╲       ╱    ╲                 │  Cluster: CL-0891     │  │
│  │      ●   ●    ●       ●                │                       │  │
│  │                                        │  Connections:          │  │
│  │  Legend:                               │  • 8 accounts          │  │
│  │  ● Phone  ● Account  ● Person         │  • 23 calls            │  │
│  │  ━ Called  ━ Transferred  ━ Uses       │  • 3 devices           │  │
│  │                                        │                       │  │
│  │  [Zoom +] [Zoom -] [Fit] [Layout ▾]  │  [🕸️ Expand]         │  │
│  │                                        │  [📋 Add to Case]    │  │
│  │                                        │  [📄 Generate Dossier]│  │
│  └────────────────────────────────────────┴───────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────────┐│
│  │  🤖 AI Copilot: "Show all complaints linked to this UPI"       ││
│  │  ──────────────────────────────────────────────                  ││
│  │  Found 7 complaints linked to xyz@ybl:                          ││
│  │  • NCRP-2026-4421 (₹2.3L, digital arrest, 2026-06-28)         ││
│  │  • NCRP-2026-4398 (₹1.1L, digital arrest, 2026-06-25)         ││
│  │  • ... [View All]                                                ││
│  └──────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────┘
```

---

## 8. Flow 5 — Geo Intel (Crime Map)

```mermaid
graph TD
    A["Navigate to Geo Intel"] --> B["Interactive Map loads<br/>(Mapbox, full screen)"]
    
    B --> C["Display layers:<br/>• Incident pins (colour-coded)<br/>• Heatmap overlay<br/>• Prediction zones"]
    
    C --> D{"User action?"}
    D -->|Click pin| E["Incident detail popup"]
    D -->|Toggle layer| F["Show/hide: scam, ficn, fraud"]
    D -->|Time filter| G["24h / 7d / 30d / 90d"]
    D -->|View predictions| H["Predicted hotspot circles<br/>for next 7 days"]
```

---

## 9. Flow 6 — AI Investigation Copilot

```mermaid
graph TD
    A["Officer opens AI Copilot<br/>(sidebar or dedicated screen)"] --> B["Chat interface"]
    
    B --> C["Officer types:<br/>'Find victims contacted<br/>by +91-9876543210'"]
    
    C --> D["Gemini API processes query"]
    D --> E["Converts to structured<br/>DB queries"]
    E --> F["Executes across:<br/>• scam_sentinel.scam_sessions<br/>• fraud_graph.entities<br/>• geo_intel.incidents"]
    
    F --> G["Returns formatted results:<br/>• 14 victims found<br/>• Total loss: ₹18.7L<br/>• Across 3 districts<br/>• Timeline: Mar-Jul 2026"]
    
    G --> H["Officer can:<br/>[View on Graph] [View on Map]<br/>[Create Investigation]"]
```

---

## 10. Flow 7 — QR Code Scanner (Citizen App)

```mermaid
graph TD
    A["Citizen taps '🔲 Scan QR'"] --> B["Camera opens with<br/>QR frame overlay"]
    
    B --> C["QR decoded"]
    C --> D{"Content type?"}
    
    D -->|UPI payment| E["Extract: UPI ID,<br/>amount, payee name"]
    D -->|URL| F["Extract: domain,<br/>full URL"]
    D -->|Other| G["Show raw content"]
    
    E --> H["Check against<br/>fraud database"]
    F --> H
    
    H --> I{"Risk level?"}
    I -->|Safe| J["✅ No known issues<br/>Account clean"]
    I -->|Caution| K["⚠️ Suspicious patterns<br/>3 complaints found"]
    I -->|Dangerous| L["🚫 Known fraud account<br/>14 complaints, blacklisted"]
    
    K --> M["Show details:<br/>• Complaint count<br/>• Risk score<br/>• Last reported date"]
    L --> M
```

### QR Scan Result Screen

```
┌─────────────────────────────────────┐
│  ← QR Scan Result                    │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │  🚫  DANGEROUS                   │ │
│  │  ───────────────                 │ │
│  │  UPI: fraud@ybl                  │ │
│  │  Payee: "Government Fine Dept"   │ │
│  │  Amount: ₹49,999                 │ │
│  └─────────────────────────────────┘ │
│                                      │
│  Risk Assessment:                    │
│  • 14 fraud complaints filed         │
│  • Account blacklisted since Jun 12  │
│  • Linked to digital arrest scam     │
│  • Risk Score: 96/100                │
│                                      │
│  ┌──────────────────────────────────┐│
│  │  🚫  DO NOT PAY                  ││
│  │  This is a known fraud account   ││
│  └──────────────────────────────────┘│
│                                      │
│  ┌──────────┐  ┌──────────────────┐  │
│  │ Report   │  │ 📞 Call 1930     │  │
│  │ This QR  │  │ (Helpline)       │  │
│  └──────────┘  └──────────────────┘  │
└─────────────────────────────────────┘
```

---

## 11. Flow 8 — Panic Button (Silent SOS)

```mermaid
graph TD
    A["Citizen on a scam call<br/>realises it's fraud<br/>but can't hang up"] --> B["Presses power button 3x<br/>(or taps SOS in app)"]
    
    B --> C["App SILENTLY activates"]
    C --> D["Records caller number"]
    C --> E["Saves call details"]
    C --> F["Alerts emergency contact<br/>(silent SMS)"]
    C --> G["Prepares fraud report"]
    
    D --> H["Scammer doesn't<br/>know anything happened"]
    E --> H
    F --> H
    G --> H
    
    H --> I["After call ends:<br/>User sees full report<br/>ready to submit to police"]
```

### Panic Activation Screen (Invisible to Scammer)

```
┌─────────────────────────────────────┐
│                                      │
│  [Normal phone screen — no visible   │
│   indication to the caller]          │
│                                      │
│  ─── Background Actions ───          │
│  ✅ Number recorded: +91-9876543210  │
│  ✅ Call details saved               │
│  ✅ Emergency contact notified       │
│  ✅ Fraud report prepared            │
│                                      │
│  [After call ends, notification:]    │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │  🛡️ Primer Protected You        │ │
│  │                                  │ │
│  │  Your SOS was activated during  │ │
│  │  the call. We've prepared a     │ │
│  │  fraud report.                  │ │
│  │                                  │ │
│  │  [View Report] [Submit to 1930] │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## 12. Flow 9 — Pre-Answer Call Screening

```mermaid
graph TD
    A["Incoming call:<br/>+91-9876543210"] --> B["Primer checks number<br/>against reputation DB"]
    
    B --> C{"Risk level?"}
    
    C -->|Low risk| D["Normal ring<br/>No intervention"]
    
    C -->|Medium risk| E["⚠️ Overlay:<br/>'Possible scam'<br/>[Answer] [Reject]"]
    
    C -->|High risk| F["🚫 Overlay:<br/>'Known Fraud Number'<br/>[Reject] [Answer Anyway]"]
    
    E --> G{"User choice?"}
    F --> G
    
    G -->|Answer| H["Call connects<br/>(Panic button ready)"]
    G -->|Reject| I["Call blocked<br/>Number flagged"]
```

### Call Screening Overlay

```
┌─────────────────────────────────────┐
│                                      │
│           Incoming Call              │
│                                      │
│         9876543210                    │
│                                      │
│         Checking...                  │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │  ⚠️ HIGH SCAM RISK              │ │
│  │  ─────────────────               │ │
│  │  Known Fraud Number              │ │
│  │  • 14 complaints filed           │ │
│  │  • Linked to digital arrest scam │ │
│  │  • Risk Score: 92/100            │ │
│  └─────────────────────────────────┘ │
│                                      │
│  ┌──────────┐  ┌──────────────────┐  │
│  │  🚫      │  │  📞 Answer       │  │
│  │  Reject  │  │  Anyway          │  │
│  └──────────┘  └──────────────────┘  │
└─────────────────────────────────────┘
```

---

## 13. Flow 10 — AI Case Summarizer

```mermaid
graph TD
    A["Officer opens Case Summarizer"] --> B["Upload evidence:<br/>• Complaint text<br/>• Call logs<br/>• Transaction records"]
    
    B --> C["Gemini API processes<br/>all evidence"]
    
    C --> D["Generated Output:"]
    D --> E["📝 Summary:<br/>Organised digital arrest scam<br/>targeting retirees in Thane"]
    D --> F["📅 Timeline:<br/>Jun 15: First contact<br/>Jun 16: Video call (CBI)<br/>Jun 17: ₹3.2L transferred"]
    D --> G["👤 Suspects:<br/>+91-9876... (primary)<br/>xyz@ybl (mule account)"]
    D --> H["🔗 Related Cases:<br/>NCRP-4421, NCRP-4398"]
    D --> I["📊 Confidence: 87%"]
    
    E --> J["[Download PDF] [Add to Investigation]"]
```

---

## 14. Demo Walkthrough Script (5 minutes)

This is the recommended demo flow for judges:

```
Minute 0:00 — Login as Yashi (LEA Officer)
  → Dashboard with live stats, threat level, mini map

Minute 0:30 — Scam Sentinel
  → Show live RED alert → click → Explainable AI breakdown
  → "This is WHY we flagged it" — signal bars with explanations

Minute 1:30 — AI Copilot
  → Type: "Find all victims contacted by +91-9876543210"
  → Show cross-module results

Minute 2:00 — Fraud Graph
  → Click through to graph → show fraud ring cluster
  → Generate evidence dossier

Minute 2:30 — Geo Intel
  → Show crime heatmap → prediction layer

Minute 3:00 — Switch to Sumanth (Citizen App)
  → QR Scanner: scan a fraudulent QR → show 🚫 DANGEROUS
  → Note Scanner: scan a counterfeit → show 🚫 COUNTERFEIT with features
  → Pre-Answer Call Screening: incoming call → HIGH RISK overlay

Minute 4:00 — Panic Button
  → Simulate: on a scam call → SOS triggered silently
  → Show generated fraud report

Minute 4:30 — Case Summarizer (back to Yashi)
  → Upload evidence → AI generates summary + timeline + suspects

Minute 5:00 — Closing
  → "Primer: From reactive to predictive. Real-time. Explainable. India-first."
```
