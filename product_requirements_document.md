# Product Requirements Document (PRD)

## **Primer — AI-Powered Digital Public Safety Intelligence Platform**

| Field | Detail |
|---|---|
| **Document Version** | 2.0 — Hackathon MVP |
| **Date** | 5 July 2026 |
| **Classification** | Hackathon Submission |
| **Theme** | Smart Cities · Public Safety · Digital Trust · Geospatial Law Enforcement |

---

## 1. Executive Summary

**Primer** is an AI-powered Digital Public Safety Intelligence Platform that shifts India's cybercrime response from **reactive investigation to real-time threat neutralisation**. For this hackathon MVP, we demonstrate five core intelligence modules plus **eight differentiating features** — all working together as a unified system.

### What We're Demonstrating

```
┌─────────────────────────────────────────────────────────────────┐
│  CORE MODULES                                                    │
│  ─────────────                                                   │
│  1. Scam Sentinel    — Live digital arrest scam detection        │
│  2. Note Verify      — Camera-based counterfeit currency check   │
│  3. Fraud Graph      — Visual fraud network mapping              │
│  4. Geo Intel        — Crime heatmap + hotspot prediction        │
│  5. Citizen Shield   — AI chat bot for citizens                  │
│                                                                   │
│  EXTRA FEATURES (Differentiators)                                │
│  ─────────────────────────────────                               │
│  6. AI Investigation Copilot    — NL queries across all data     │
│  7. QR Code Scanner             — Instant QR risk assessment     │
│  8. Deepfake Voice Detector     — AI-generated speech flagging   │
│  9. Explainable AI              — Full reasoning for every flag  │
│  10. AI Case Summarizer         — Auto-generate case briefs      │
│  11. Adaptive Fraud KB          — Self-updating scam database    │
│  12. Panic Button (Silent SOS)  — Stealth fraud reporting        │
│  13. Pre-Answer Call Screening  — Block scams before pickup      │
└─────────────────────────────────────────────────────────────────┘
```

### Core Value Proposition

| Stakeholder | Without Primer | With Primer |
|---|---|---|
| **Law Enforcement** | Post-facto FIR filing; siloed data | Real-time alerts; cross-jurisdictional graph intelligence; AI copilot for investigation |
| **Financial Institutions** | Manual FICN detection | Camera-based counterfeit detection in < 3 seconds |
| **Citizens** | No guidance during active scam | Pre-answer call screening, QR safety check, panic button, multilingual AI advisor |

### Judging Criteria Alignment

| Criteria | Weight | How Primer Scores |
|---|---|---|
| **Innovation** | 25% | Panic Button (silent SOS), Pre-Answer Call Screening, AI Investigation Copilot, Adaptive Fraud KB — features that don't exist in any current Indian law enforcement tool |
| **Business Impact** | 25% | Intervenes *during* scam calls (not after); quantifiable: ₹1,776 Cr annual losses addressable; citizen self-protection via QR scanner |
| **Technical Excellence** | 20% | Multi-signal Explainable AI, Graph Neural Networks, Computer Vision, Speech AI, Agentic AI fusion — all with audit trails |
| **Scalability** | 15% | Clean API-first design, event-driven architecture, containerised services, horizontal scaling path |
| **User Experience** | 15% | Apple-inspired dark UI, < 300ms interactions, multilingual support, zero-training citizen app |

---

## 2. Problem Statement

### The Scale of the Crisis

| Metric | Value | Source |
|---|---|---|
| Cybercrime complaints (2023) | **1.14 million** | MHA / I4C |
| Year-on-Year growth | **+60%** | MHA |
| "Digital arrest" scam losses (Jan–Sep 2024) | **₹1,776 crore** | MHA Press Brief |
| FICN notes detected (FY 2024–25) | **Record high** (₹500 denomination) | RBI Annual Report |
| Average victim response time | **72+ hours** post-incident | NCRB |

### Why Existing Solutions Fail

| Existing Approach | Gap |
|---|---|
| NCRP Portal (cybercrime.gov.in) | Complaint *after* victimisation; no real-time intervention |
| Bank fraud monitoring | Blind to social engineering call flows |
| Telecom DND / spam filters | Cannot detect live scam sessions or AI-spoofed voices |
| Manual FICN detection | Fails against high-quality ₹500 fakes |

### Primer's Opportunity

The convergence of **Computer Vision, Graph AI, NLP/LLMs, Geospatial Intelligence, Speech AI, and Agentic AI** makes it feasible to operate across the *entire kill chain* of digital fraud — from the moment a spoofed call is initiated to prosecution support.

---

## 3. Target Users & Demo Personas

| Demo User | Role | Modules They Access |
|---|---|---|
| **Yashi** | LEA Officer (Inspector, Cyber Cell) | Full dashboard: Scam Sentinel, Fraud Graph, Geo Intel, AI Copilot, Case Summarizer |
| **Srinivas** | Bank Manager (SBI branch) | Note Verify scanner, counterfeit history, FICN analytics |
| **Sumanth** | Citizen (mobile app user) | QR scanner, pre-answer call screening, panic button, AI chat, note scanner |

---

## 4. Module Requirements (MVP Scope)

### Module 1 — Scam Sentinel (Digital Arrest Detection)

**What it does:** Detects active "digital arrest" scam sessions by analysing call metadata, number reputation, script patterns, and voice characteristics — flagging them in real-time.

**MVP User Stories:**

| ID | As a... | I want to... | Priority |
|---|---|---|---|
| US-1.1 | LEA Officer (Yashi) | See a live dashboard of flagged scam sessions in my jurisdiction | **P0** |
| US-1.2 | LEA Officer (Yashi) | View confidence scores with explainable AI breakdown for each flag | **P0** |
| US-1.3 | System | Detect AI-generated/deepfake voices in call sessions | **P0** |
| US-1.4 | System | Screen incoming calls and show risk level BEFORE the citizen answers | **P0** |

**MVP Functional Scope:**
- Multi-signal classifier: call flow patterns + number reputation + script matching + voice analysis
- Three alert levels: **RED** (≥ 85% confidence), **AMBER** (60–84%), **YELLOW** (< 60%)
- Explainable AI output: every flag shows contributing signals with individual scores
- Pre-answer call screening: check number against DB, show risk to citizen before they pick up

**Technologies:** NLP/LLMs (script matching), Speech AI (voice spoofing detection), Agentic AI (multi-signal fusion)

---

### Module 2 — Note Verify (Counterfeit Currency Detection)

**What it does:** Camera-based AI that analyses currency note photos and returns GENUINE / SUSPECT / COUNTERFEIT with per-feature scores.

**MVP User Stories:**

| ID | As a... | I want to... | Priority |
|---|---|---|---|
| US-2.1 | Bank Manager (Srinivas) | Scan a note with phone camera and get instant verdict | **P0** |
| US-2.2 | Citizen (Sumanth) | Check if a note I received is genuine using the app | **P0** |
| US-2.3 | Bank Manager (Srinivas) | See per-feature analysis (watermark, thread, microprint) | **P0** |

**MVP Functional Scope:**
- Camera-guided capture with quality validation (blur, lighting, framing)
- Multi-feature analysis: watermark, security thread, microprint, intaglio, serial number
- On-device inference (TFLite, < 3 seconds on mid-range phone)
- Serial number OCR + known-counterfeit database lookup

**Technologies:** Computer Vision (EfficientNet-based classifier), Edge AI (TFLite on-device)

---

### Module 3 — Fraud Graph (Network Intelligence)

**What it does:** Visualises connections between fraud entities (phones, accounts, devices, people) as an interactive network graph — revealing fraud rings and money trails.

**MVP User Stories:**

| ID | As a... | I want to... | Priority |
|---|---|---|---|
| US-3.1 | LEA Officer (Yashi) | Enter a phone number/account and see its fraud connections as a graph | **P0** |
| US-3.2 | LEA Officer (Yashi) | Ask the AI Copilot "Show all complaints linked to this UPI" | **P0** |
| US-3.3 | LEA Officer (Yashi) | Generate an evidence package with graph, timeline, and suspects | **P0** |

**MVP Functional Scope:**
- Interactive graph visualisation (D3.js/Sigma.js)
- Entity search: phone, account, UPI, case ID
- Community detection: auto-cluster related entities
- Money flow tracing: visual Sankey diagram
- AI Copilot: natural language queries across graph data

**Technologies:** Graph AI & Network Analysis (community detection, centrality), Agentic AI (copilot queries)

---

### Module 4 — Geo Intel (Crime Pattern Intelligence)

**What it does:** Maps fraud incidents geographically with heatmaps and predicts future hotspots.

**MVP User Stories:**

| ID | As a... | I want to... | Priority |
|---|---|---|---|
| US-4.1 | LEA Officer (Yashi) | View a real-time heatmap of cybercrime incidents | **P0** |
| US-4.2 | LEA Officer (Yashi) | See predicted hotspots for the next 7 days | **P1** |

**MVP Functional Scope:**
- Interactive crime map (Mapbox) with incident pins and heatmap overlay
- Time-range filtering (24h / 7d / 30d)
- Hotspot prediction layer (ML-based, next 7 days)
- Cross-module overlay: scam call origins + FICN seizure locations

**Technologies:** Geospatial Intelligence (PostGIS, Mapbox), spatiotemporal ML

---

### Module 5 — Citizen Shield (AI Advisor)

**What it does:** AI chatbot accessible via mobile app that helps citizens assess fraud risk and report incidents.

**MVP User Stories:**

| ID | As a... | I want to... | Priority |
|---|---|---|---|
| US-5.1 | Citizen (Sumanth) | Describe a suspicious call and get instant risk assessment | **P0** |
| US-5.2 | Citizen (Sumanth) | Check a phone number against known scam databases | **P0** |
| US-5.3 | Citizen (Sumanth) | Get guided help in Hindi/English/regional language | **P1** |

**MVP Functional Scope:**
- Chat interface powered by Gemini API with fraud-domain context
- Number lookup against reputation database
- Multilingual support (Hindi + English minimum, extensible)
- Guided complaint filing assistance

**Technologies:** NLP/LLMs (Gemini API), multilingual NLU

---

## 5. Extra Feature Requirements

### Feature 6 — AI Investigation Copilot

**What:** Officers ask natural-language questions and the AI searches across all connected datasets.

**Examples:**
- "Show all complaints linked to this UPI"
- "Find victims contacted by this number"
- "What's the total loss from cluster CL-2026-00891?"

**MVP Scope:** Text-based chat in the dashboard. Gemini API processes the query, converts to structured DB queries, returns formatted results.

**Technology:** Agentic AI, LLM function calling, structured query generation

---

### Feature 7 — QR Code Scanner

**What:** Citizen scans any QR code. AI checks destination account, complaint history, suspicious patterns, and domain reputation.

**Output:**
- ✅ Safe — No known issues
- ⚠️ Caution — Some suspicious patterns
- 🚫 Dangerous — Known fraud account / malicious URL

**MVP Scope:** Camera-based QR scanner in mobile app → decode → check against fraud DB → show risk verdict.

**Technology:** Computer Vision (QR decoding via ML Kit/zxing), database lookups

---

### Feature 8 — Deepfake Voice Detector

**What:** Analyses voice characteristics to detect AI-generated/synthetic speech. Flags calls where the caller claims to be an authority figure but uses AI-generated voice.

**MVP Scope:** Upload audio clip → spectral analysis → synthetic probability score with explanation.

**Technology:** Speech AI (LCNN on mel-spectrograms, ASVspoof-trained)

---

### Feature 9 — Explainable AI

**What:** Every detection shows its full reasoning chain.

**Example output:**
```
Detected because:
✔ Caller number spoofed (confidence: 88%)
✔ Urgency phrases detected: "arrest warrant", "immediate transfer"
✔ Fake police identity claimed
✔ Same script seen 240 times in database
✔ Destination account flagged in 14 prior complaints
```

**MVP Scope:** Every Scam Sentinel alert and Note Verify result includes signal-level breakdown with individual confidence scores.

**Technology:** Model interpretability, feature attribution, structured output

---

### Feature 10 — AI Case Summarizer

**What:** Officers upload evidence (complaints, call logs, transaction records). AI generates a structured case brief.

**Output:**
- Executive summary
- Chronological timeline
- Suspected individuals and roles
- Related complaints
- Confidence score

**MVP Scope:** Upload text/files → Gemini API generates structured summary → display in dashboard.

**Technology:** LLMs (Gemini API), document parsing, structured output generation

---

### Feature 11 — Adaptive Fraud Knowledge Base

**What:** When analysts encounter new scam patterns, they label them. The system suggests similar existing cases and auto-categorises without full model retraining.

**MVP Scope:** Analyst labels a session → system finds top-5 similar cases via embedding similarity → stores new pattern → future detections use the expanded corpus.

**Technology:** Vector embeddings (sentence-transformers), similarity search, incremental learning

---

### Feature 12 — Panic Button (Silent SOS)

**What:** If a citizen realises they're on a scam call but can't hang up, they press the power button 3 times. The app silently:
- Records the caller number
- Saves call details
- Alerts an emergency contact
- Prepares a fraud report

The scammer doesn't know anything happened.

**MVP Scope:** Demonstrate via app button (simulated power-button trigger) → show silent background actions → display generated report.

**Technology:** OS accessibility APIs, background services, silent notification dispatch

---

### Feature 13 — Pre-Answer Call Screening

**What:** AI screens incoming calls BEFORE the user answers.

**UX Flow:**
```
Incoming Call: 9876543210
Checking...

⚠️ High Scam Risk
Known Fraud Number

[Reject]  [Answer Anyway]
```

**MVP Scope:** Demonstrate with simulated incoming call → number lookup → risk verdict overlay → user choice.

**Technology:** CallKit (iOS) / CallScreeningService (Android), number reputation API

---

## 6. Technologies Used

| Technology | Where Used |
|---|---|
| **Computer Vision** | Counterfeit detection (NoteAuthNet), deepfake video analysis, QR scanning |
| **Graph AI & Network Analysis** | Fraud ring mapping, community detection, centrality analysis, money flow tracing |
| **NLP / LLMs** | Scam script matching, AI Copilot, Case Summarizer, Citizen Shield chatbot, Explainable AI narratives |
| **Geospatial Intelligence** | Crime heatmaps, hotspot prediction, patrol optimisation |
| **Speech AI** | Deepfake voice detection, voice pattern classification |
| **Agentic AI** | Multi-source intelligence fusion, AI Copilot query orchestration, cross-module correlation |
| **Edge AI** | On-device currency scanning (TFLite), QR code processing |
| **Vector Search** | Adaptive Knowledge Base similarity matching, scam script corpus |

---

## 7. Evaluation Metrics (Demo-Ready)

| Metric | Target | How We Demonstrate |
|---|---|---|
| Counterfeit detection accuracy (₹500) | ≥ 95% | Live scan demo with genuine + fake notes |
| Digital arrest scam detection precision | ≥ 90% | Simulated scam session → real-time flag |
| Fraud network detection lead time | < 5 minutes from first complaint | Show graph building in real-time |
| False positive rate (citizen tools) | ≤ 2% | QR scanner + call screening demo with clean numbers |
| Explainability coverage | 100% of flags have reasoning | Every alert shows signal breakdown |
| AI Copilot query accuracy | ≥ 85% relevant results | Live NL query demo |
| Pre-answer screening latency | < 2 seconds | Simulated incoming call demo |

---

## 8. Out of Scope (Post-Hackathon)

These are **not** in the MVP but are noted as scalability paths:

- Full RBAC with MFA and WebAuthn
- IVR (voice call) bot integration
- WhatsApp Business API integration
- Telecom operator API integration (real CDR streaming)
- NCRP portal integration
- Court-admissible evidence packaging (IEA §65B compliance)
- Multi-tenancy (multiple states/agencies)
- ATM/counting machine SDK integration
- Real-time call interception
- International intelligence sharing (STIX 2.1)
