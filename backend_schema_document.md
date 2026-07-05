# Backend Schema Document

## **Primer — AI-Powered Digital Public Safety Intelligence Platform**

| Field | Detail |
|---|---|
| **Document Version** | 2.0 — Hackathon MVP |
| **Date** | 5 July 2026 |
| **Database** | PostgreSQL 16 + PostGIS + pgvector (single instance) |
| **Companion Documents** | [PRD](product_requirements_document.md) · [TRD](technical_requirements_document.md) |

---

## 1. Data Architecture — MVP

### 1.1 Single-Database Strategy

Everything lives in **one PostgreSQL instance** with schema namespacing. No Neo4j, no TimescaleDB, no Elasticsearch, no Weaviate, no MinIO.

| What Production Uses | MVP Replacement |
|---|---|
| Neo4j (graph) | PostgreSQL adjacency tables + recursive CTEs |
| TimescaleDB (time-series) | PostgreSQL with timestamp indexes |
| Elasticsearch (search) | PostgreSQL `tsvector` full-text search |
| Weaviate (vectors) | pgvector extension or in-memory FAISS |
| MinIO (object storage) | Local filesystem (`/uploads/`) |
| Redis (cache) | Redis 7 single instance (kept — too useful to drop) |

### 1.2 Schema Overview

```
primer (database)
├── core.*              — Users, auth, investigations, notifications
├── scam_sentinel.*     — Scam sessions, alerts, number reputation
├── note_verify.*       — Currency verifications, serial registry
├── fraud_graph.*       — Entities, edges, clusters (replaces Neo4j)
├── geo_intel.*         — Incidents with PostGIS coordinates
├── citizen_shield.*    — Chat sessions, messages
├── knowledge_base.*    — Adaptive fraud patterns
├── qr_scans.*          — QR code scan results
└── panic.*             — Silent SOS events
```

---

## 2. Schema: `core` — Platform Foundation

```sql
CREATE SCHEMA IF NOT EXISTS core;

-- ── Users (3 demo roles: lea_officer, bank_manager, citizen) ──
CREATE TABLE core.users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) NOT NULL UNIQUE,
    name            VARCHAR(255) NOT NULL,
    role            VARCHAR(50) NOT NULL
                    CHECK (role IN ('lea_officer', 'bank_manager', 'citizen')),
    designation     VARCHAR(100),
    jurisdiction    VARCHAR(200),
    password_hash   TEXT NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed demo users
INSERT INTO core.users (email, name, role, designation, jurisdiction, password_hash) VALUES
    ('yashi@primer.demo', 'Yashi', 'lea_officer', 'Inspector, Cyber Cell', 'Mumbai Suburban', '$2b$12$demo_hash_yashi'),
    ('srinivas@primer.demo', 'Srinivas', 'bank_manager', 'Branch Manager, SBI', 'Andheri West', '$2b$12$demo_hash_srinivas'),
    ('sumanth@primer.demo', 'Sumanth', 'citizen', 'Citizen', NULL, '$2b$12$demo_hash_sumanth');

-- ── Investigations (cross-module cases) ──
CREATE TABLE core.investigations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    type            VARCHAR(50) NOT NULL DEFAULT 'mixed',
    priority        VARCHAR(20) NOT NULL DEFAULT 'medium'
                    CHECK (priority IN ('critical', 'high', 'medium', 'low')),
    status          VARCHAR(30) NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open', 'active', 'closed')),
    assigned_to     UUID REFERENCES core.users(id),
    estimated_amount DECIMAL(15,2),
    victim_count    INTEGER DEFAULT 0,
    tags            TEXT[],
    created_by      UUID NOT NULL REFERENCES core.users(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Case Summaries (AI-generated) ──
CREATE TABLE core.case_summaries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    investigation_id UUID REFERENCES core.investigations(id),
    summary_text    TEXT NOT NULL,
    timeline_json   JSONB NOT NULL DEFAULT '[]',
    suspects_json   JSONB NOT NULL DEFAULT '[]',
    related_complaints JSONB NOT NULL DEFAULT '[]',
    confidence_score DECIMAL(5,2),
    source_evidence TEXT[],
    generated_by    VARCHAR(50) DEFAULT 'gemini',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Notifications ──
CREATE TABLE core.notifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES core.users(id),
    module          VARCHAR(50) NOT NULL,
    severity        VARCHAR(20) NOT NULL DEFAULT 'info'
                    CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
    title           VARCHAR(500) NOT NULL,
    body            TEXT NOT NULL,
    is_read         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON core.notifications (user_id, is_read, created_at DESC);

-- ── Audit Log (simplified — append-only) ──
CREATE TABLE core.audit_log (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor_id        UUID,
    action          VARCHAR(100) NOT NULL,
    module          VARCHAR(50),
    resource_type   VARCHAR(100),
    resource_id     VARCHAR(255),
    details         JSONB
);

CREATE INDEX idx_audit_timestamp ON core.audit_log (timestamp DESC);
```

---

## 3. Schema: `scam_sentinel` — Digital Arrest Detection

```sql
CREATE SCHEMA IF NOT EXISTS scam_sentinel;

-- ── Scam Sessions ──
CREATE TABLE scam_sentinel.scam_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Call Metadata
    caller_number   VARCHAR(20) NOT NULL,
    callee_number   VARCHAR(20) NOT NULL,
    call_start      TIMESTAMPTZ NOT NULL,
    call_end        TIMESTAMPTZ,
    call_duration_sec INTEGER,
    
    -- Classification
    alert_level     VARCHAR(10) NOT NULL DEFAULT 'NONE'
                    CHECK (alert_level IN ('RED', 'AMBER', 'YELLOW', 'NONE')),
    overall_confidence DECIMAL(5,2),
    scam_type       VARCHAR(50),
    scam_phase      VARCHAR(30),
    
    -- Explainable AI — signal breakdown
    signal_scores   JSONB NOT NULL DEFAULT '{}',
    -- Example: {
    --   "call_flow_match": { "score": 0.94, "explanation": "Matches digital arrest pattern" },
    --   "number_spoofing": { "score": 0.88, "explanation": "CLI mismatch detected" },
    --   "script_similarity": { "score": 0.91, "explanation": "Matches template #47 (CBI impersonation)" },
    --   "voice_synthetic": { "score": 0.73, "explanation": "Spectral anomalies in 2-4kHz range" },
    --   "urgency_phrases": { "score": 0.96, "explanation": "Detected: arrest warrant, immediate transfer" }
    -- }
    
    -- Spoofing
    spoofing_detected    BOOLEAN DEFAULT FALSE,
    real_originating_number VARCHAR(20),
    
    -- Voice Analysis
    deepfake_detected    BOOLEAN DEFAULT FALSE,
    voice_synthetic_probability DECIMAL(5,2),
    
    -- Status
    status          VARCHAR(20) NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'classified', 'acknowledged', 'investigating', 'closed')),
    acknowledged_by UUID REFERENCES core.users(id),
    acknowledged_at TIMESTAMPTZ,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ss_alert ON scam_sentinel.scam_sessions (alert_level, created_at DESC);
CREATE INDEX idx_ss_caller ON scam_sentinel.scam_sessions (caller_number);
CREATE INDEX idx_ss_callee ON scam_sentinel.scam_sessions (callee_number);

-- ── Number Reputation ──
CREATE TABLE scam_sentinel.number_reputation (
    phone_number    VARCHAR(20) PRIMARY KEY,
    risk_score      INTEGER NOT NULL DEFAULT 0 CHECK (risk_score BETWEEN 0 AND 100),
    total_flags     INTEGER NOT NULL DEFAULT 0,
    total_complaints INTEGER NOT NULL DEFAULT 0,
    is_blacklisted  BOOLEAN NOT NULL DEFAULT FALSE,
    primary_scam_type VARCHAR(50),
    telecom_provider VARCHAR(100),
    first_seen      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_flagged    TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}',
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Scam Script Corpus (for matching) ──
CREATE TABLE scam_sentinel.scam_script_corpus (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language        VARCHAR(10) NOT NULL,
    scam_type       VARCHAR(50) NOT NULL,
    title           VARCHAR(255) NOT NULL,
    content         TEXT NOT NULL,
    key_phrases     TEXT[],
    embedding       vector(384),          -- pgvector: sentence-transformer embedding
    times_matched   INTEGER NOT NULL DEFAULT 0,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 4. Schema: `note_verify` — Counterfeit Currency

```sql
CREATE SCHEMA IF NOT EXISTS note_verify;

-- ── Verifications ──
CREATE TABLE note_verify.verifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES core.users(id),
    
    -- Note Info
    denomination    INTEGER NOT NULL,
    serial_number   VARCHAR(20),
    
    -- Result
    verdict         VARCHAR(20) NOT NULL
                    CHECK (verdict IN ('GENUINE', 'SUSPECT', 'COUNTERFEIT')),
    confidence      DECIMAL(5,2) NOT NULL,
    
    -- Per-feature analysis (Explainable AI)
    feature_analysis JSONB NOT NULL DEFAULT '{}',
    -- Example: {
    --   "watermark": { "status": "pass", "score": 0.98 },
    --   "security_thread": { "status": "pass", "score": 0.95 },
    --   "microprint": { "status": "fail", "score": 0.23 },
    --   "intaglio": { "status": "pass", "score": 0.91 },
    --   "colour_shift": { "status": "warn", "score": 0.61 },
    --   "serial_known": { "status": "fail", "score": 0.0, "note": "Known counterfeit serial" }
    -- }
    
    -- Metadata
    image_path      VARCHAR(500),
    annotated_image_path VARCHAR(500),
    scan_source     VARCHAR(50) DEFAULT 'mobile'
                    CHECK (scan_source IN ('mobile', 'web', 'scanner')),
    device_info     JSONB,
    location        GEOMETRY(Point, 4326),      -- PostGIS point
    
    is_known_counterfeit BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_nv_user ON note_verify.verifications (user_id, created_at DESC);
CREATE INDEX idx_nv_verdict ON note_verify.verifications (verdict, created_at DESC);
CREATE INDEX idx_nv_location ON note_verify.verifications USING GIST (location);

-- ── Known Counterfeit Serial Registry ──
CREATE TABLE note_verify.counterfeit_serials (
    serial_number   VARCHAR(20) PRIMARY KEY,
    denomination    INTEGER NOT NULL,
    first_detected  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    detection_count INTEGER NOT NULL DEFAULT 1,
    source          VARCHAR(100) DEFAULT 'system'
);
```

---

## 5. Schema: `fraud_graph` — Network Intelligence (PostgreSQL-based)

Instead of Neo4j, we model the graph in PostgreSQL with entities and edges.

```sql
CREATE SCHEMA IF NOT EXISTS fraud_graph;

-- ── Entities (nodes in the graph) ──
CREATE TABLE fraud_graph.entities (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type     VARCHAR(50) NOT NULL
                    CHECK (entity_type IN ('phone_number', 'bank_account', 'upi_id',
                                           'person', 'device', 'ip_address', 'complaint')),
    entity_value    VARCHAR(255) NOT NULL,
    display_label   VARCHAR(255),
    risk_score      INTEGER DEFAULT 0 CHECK (risk_score BETWEEN 0 AND 100),
    properties      JSONB DEFAULT '{}',
    cluster_id      UUID,
    first_seen      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT uq_entity UNIQUE (entity_type, entity_value)
);

CREATE INDEX idx_entity_type ON fraud_graph.entities (entity_type, entity_value);
CREATE INDEX idx_entity_cluster ON fraud_graph.entities (cluster_id);

-- ── Edges (relationships between entities) ──
CREATE TABLE fraud_graph.edges (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id       UUID NOT NULL REFERENCES fraud_graph.entities(id),
    target_id       UUID NOT NULL REFERENCES fraud_graph.entities(id),
    relationship    VARCHAR(50) NOT NULL
                    CHECK (relationship IN ('called', 'transferred_to', 'uses_number',
                                            'owns_account', 'uses_device', 'connected_from',
                                            'reported_by', 'linked_to')),
    weight          DECIMAL(10,2) DEFAULT 1.0,
    properties      JSONB DEFAULT '{}',
    first_seen      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_edge_source ON fraud_graph.edges (source_id);
CREATE INDEX idx_edge_target ON fraud_graph.edges (target_id);
CREATE INDEX idx_edge_rel ON fraud_graph.edges (relationship);

-- ── Clusters (fraud rings) ──
CREATE TABLE fraud_graph.clusters (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255),
    node_count      INTEGER NOT NULL DEFAULT 0,
    edge_count      INTEGER NOT NULL DEFAULT 0,
    estimated_loss  DECIMAL(15,2) DEFAULT 0,
    victim_count    INTEGER DEFAULT 0,
    status          VARCHAR(30) NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'monitoring', 'dismantled')),
    detected_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Dossiers (generated evidence packages) ──
CREATE TABLE fraud_graph.dossiers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_id      UUID REFERENCES fraud_graph.clusters(id),
    title           VARCHAR(500) NOT NULL,
    content_json    JSONB NOT NULL,       -- structured dossier content
    pdf_path        VARCHAR(500),          -- generated PDF file path
    generated_by    UUID REFERENCES core.users(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Graph Queries Using Recursive CTEs

```sql
-- 2-hop neighbourhood of an entity
WITH RECURSIVE hops AS (
    -- Seed: the starting entity
    SELECT e.id, e.entity_type, e.entity_value, e.risk_score, 0 AS depth
    FROM fraud_graph.entities e
    WHERE e.entity_type = 'phone_number' AND e.entity_value = '+919876543210'
    
    UNION ALL
    
    -- Expand: follow edges up to 2 hops
    SELECT e2.id, e2.entity_type, e2.entity_value, e2.risk_score, h.depth + 1
    FROM hops h
    JOIN fraud_graph.edges eg ON (eg.source_id = h.id OR eg.target_id = h.id)
    JOIN fraud_graph.entities e2 ON (e2.id = CASE WHEN eg.source_id = h.id THEN eg.target_id ELSE eg.source_id END)
    WHERE h.depth < 2
)
SELECT DISTINCT * FROM hops;
```

---

## 6. Schema: `geo_intel` — Geospatial Intelligence

```sql
CREATE SCHEMA IF NOT EXISTS geo_intel;

-- ── Crime Incidents ──
CREATE TABLE geo_intel.incidents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    crime_type      VARCHAR(50) NOT NULL
                    CHECK (crime_type IN ('digital_arrest', 'upi_fraud', 'ficn_seizure',
                                          'investment_scam', 'phishing', 'other')),
    title           VARCHAR(500),
    description     TEXT,
    location        GEOMETRY(Point, 4326) NOT NULL,
    state           VARCHAR(100),
    district        VARCHAR(100),
    pin_code        VARCHAR(10),
    severity        VARCHAR(20) DEFAULT 'medium',
    estimated_loss  DECIMAL(15,2),
    source_module   VARCHAR(50),
    source_ref_id   UUID,
    reported_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_incidents_location ON geo_intel.incidents USING GIST (location);
CREATE INDEX idx_incidents_type ON geo_intel.incidents (crime_type, reported_at DESC);
CREATE INDEX idx_incidents_time ON geo_intel.incidents (reported_at DESC);

-- ── Hotspot Predictions ──
CREATE TABLE geo_intel.predictions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prediction_date DATE NOT NULL,
    crime_type      VARCHAR(50),
    center_point    GEOMETRY(Point, 4326) NOT NULL,
    radius_km       DECIMAL(5,2) NOT NULL,
    risk_score      INTEGER CHECK (risk_score BETWEEN 0 AND 100),
    model_version   VARCHAR(50),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_predictions_date ON geo_intel.predictions (prediction_date, risk_score DESC);
```

---

## 7. Schema: `citizen_shield` — Citizen AI Advisor

```sql
CREATE SCHEMA IF NOT EXISTS citizen_shield;

-- ── Chat Sessions ──
CREATE TABLE citizen_shield.chat_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES core.users(id),
    language        VARCHAR(10) DEFAULT 'en',
    status          VARCHAR(20) DEFAULT 'active'
                    CHECK (status IN ('active', 'closed', 'escalated')),
    risk_assessment VARCHAR(20),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at        TIMESTAMPTZ
);

-- ── Chat Messages ──
CREATE TABLE citizen_shield.chat_messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES citizen_shield.chat_sessions(id),
    role            VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
    content         TEXT NOT NULL,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_session ON citizen_shield.chat_messages (session_id, created_at);
```

---

## 8. Schema: `knowledge_base` — Adaptive Fraud Knowledge Base

```sql
CREATE SCHEMA IF NOT EXISTS knowledge_base;

-- ── Fraud Patterns ──
CREATE TABLE knowledge_base.patterns (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title           VARCHAR(255) NOT NULL,
    description     TEXT NOT NULL,
    scam_type       VARCHAR(50) NOT NULL,
    language        VARCHAR(10) DEFAULT 'en',
    key_indicators  TEXT[],
    example_scripts TEXT[],
    embedding       vector(384),          -- sentence-transformer embedding for similarity
    times_matched   INTEGER NOT NULL DEFAULT 0,
    labeled_by      UUID REFERENCES core.users(id),
    verified        BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Similarity search: find patterns similar to a new one
-- SELECT * FROM knowledge_base.patterns
-- ORDER BY embedding <-> $1::vector
-- LIMIT 5;
```

---

## 9. Schema: `qr_scans` — QR Code Scanner

```sql
CREATE SCHEMA IF NOT EXISTS qr_scans;

CREATE TABLE qr_scans.scan_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES core.users(id),
    qr_content      TEXT NOT NULL,
    content_type    VARCHAR(50) NOT NULL
                    CHECK (content_type IN ('upi_payment', 'url', 'bank_account', 'text', 'unknown')),
    
    -- Extracted data
    destination_account VARCHAR(255),
    destination_url VARCHAR(1000),
    
    -- Risk assessment
    risk_level      VARCHAR(20) NOT NULL
                    CHECK (risk_level IN ('safe', 'caution', 'dangerous')),
    risk_score      INTEGER CHECK (risk_score BETWEEN 0 AND 100),
    complaint_count INTEGER DEFAULT 0,
    explanation     TEXT,
    flags           JSONB DEFAULT '[]',
    
    scanned_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 10. Schema: `panic` — Silent SOS / Panic Button

```sql
CREATE SCHEMA IF NOT EXISTS panic;

CREATE TABLE panic.sos_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES core.users(id),
    
    -- Call info captured silently
    caller_number   VARCHAR(20),
    call_duration_sec INTEGER,
    
    -- Location
    location        GEOMETRY(Point, 4326),
    
    -- Actions taken
    emergency_contact_notified BOOLEAN DEFAULT FALSE,
    emergency_contact_number VARCHAR(20),
    fraud_report_generated BOOLEAN DEFAULT FALSE,
    fraud_report_path VARCHAR(500),
    
    -- Device info
    device_info     JSONB,
    
    triggered_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 11. Redis Key Design (Simplified)

```
# Number reputation cache (fast lookups for call screening)
num:rep:{phone}          → JSON { risk_score, flags, is_blacklisted }   TTL: 1 hour

# User sessions
session:{user_id}        → JWT token                                     TTL: 24 hours

# Dashboard stats cache
stats:dashboard:{jurisdiction}  → JSON { active_alerts, ficn_today... } TTL: 60 seconds

# Rate limiting
rate:{user_id}:{endpoint}      → counter                                TTL: 60 seconds
```

---

## 12. Seed Data for Demo

The demo requires pre-loaded data to look impressive:

```sql
-- 1. 50+ scam sessions (mix of RED/AMBER/YELLOW)
-- 2. 20+ phone numbers with reputation scores
-- 3. 100+ fraud graph entities with edges forming 3-4 visible clusters
-- 4. 200+ geo incidents spread across Mumbai, Delhi, Bangalore
-- 5. 10+ known counterfeit serial numbers
-- 6. 30+ scam script templates (Hindi + English)
-- 7. 5+ QR codes linked to flagged accounts
-- 8. 3+ pre-generated case summaries
```

A `seed.sql` file will be created to populate all of this on `docker compose up`.
