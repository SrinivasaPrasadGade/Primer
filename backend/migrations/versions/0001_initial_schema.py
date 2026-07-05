"""initial schema — all modules per backend_schema_document.md

Revision ID: 0001
Revises:
Create Date: 2026-07-06

"""
from typing import Sequence, Union

from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMAS = [
    "core",
    "scam_sentinel",
    "note_verify",
    "fraud_graph",
    "geo_intel",
    "citizen_shield",
    "knowledge_base",
    "qr_scans",
    "panic",
]

UPGRADE_SQL = """
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- core
-- ============================================================
CREATE SCHEMA IF NOT EXISTS core;

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

-- Seed demo users
INSERT INTO core.users (email, name, role, designation, jurisdiction, password_hash) VALUES
    ('yashi@primer.demo', 'Yashi', 'lea_officer', 'Inspector, Cyber Cell', 'Mumbai Suburban', '$2b$12$demo_hash_yashi'),
    ('srinivas@primer.demo', 'Srinivas', 'bank_manager', 'Branch Manager, SBI', 'Andheri West', '$2b$12$demo_hash_srinivas'),
    ('sumanth@primer.demo', 'Sumanth', 'citizen', 'Citizen', NULL, '$2b$12$demo_hash_sumanth');

-- ============================================================
-- scam_sentinel
-- ============================================================
CREATE SCHEMA IF NOT EXISTS scam_sentinel;

CREATE TABLE scam_sentinel.scam_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    caller_number   VARCHAR(20) NOT NULL,
    callee_number   VARCHAR(20) NOT NULL,
    call_start      TIMESTAMPTZ NOT NULL,
    call_end        TIMESTAMPTZ,
    call_duration_sec INTEGER,
    alert_level     VARCHAR(10) NOT NULL DEFAULT 'NONE'
                    CHECK (alert_level IN ('RED', 'AMBER', 'YELLOW', 'NONE')),
    overall_confidence DECIMAL(5,2),
    scam_type       VARCHAR(50),
    scam_phase      VARCHAR(30),
    signal_scores   JSONB NOT NULL DEFAULT '{}',
    spoofing_detected    BOOLEAN DEFAULT FALSE,
    real_originating_number VARCHAR(20),
    deepfake_detected    BOOLEAN DEFAULT FALSE,
    voice_synthetic_probability DECIMAL(5,2),
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

CREATE TABLE scam_sentinel.scam_script_corpus (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language        VARCHAR(10) NOT NULL,
    scam_type       VARCHAR(50) NOT NULL,
    title           VARCHAR(255) NOT NULL,
    content         TEXT NOT NULL,
    key_phrases     TEXT[],
    embedding       vector(384),
    times_matched   INTEGER NOT NULL DEFAULT 0,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- note_verify
-- ============================================================
CREATE SCHEMA IF NOT EXISTS note_verify;

CREATE TABLE note_verify.verifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES core.users(id),
    denomination    INTEGER NOT NULL,
    serial_number   VARCHAR(20),
    verdict         VARCHAR(20) NOT NULL
                    CHECK (verdict IN ('GENUINE', 'SUSPECT', 'COUNTERFEIT')),
    confidence      DECIMAL(5,2) NOT NULL,
    feature_analysis JSONB NOT NULL DEFAULT '{}',
    image_path      VARCHAR(500),
    annotated_image_path VARCHAR(500),
    scan_source     VARCHAR(50) DEFAULT 'mobile'
                    CHECK (scan_source IN ('mobile', 'web', 'scanner')),
    device_info     JSONB,
    location        GEOMETRY(Point, 4326),
    is_known_counterfeit BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_nv_user ON note_verify.verifications (user_id, created_at DESC);
CREATE INDEX idx_nv_verdict ON note_verify.verifications (verdict, created_at DESC);
CREATE INDEX idx_nv_location ON note_verify.verifications USING GIST (location);

CREATE TABLE note_verify.counterfeit_serials (
    serial_number   VARCHAR(20) PRIMARY KEY,
    denomination    INTEGER NOT NULL,
    first_detected  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    detection_count INTEGER NOT NULL DEFAULT 1,
    source          VARCHAR(100) DEFAULT 'system'
);

-- ============================================================
-- fraud_graph
-- ============================================================
CREATE SCHEMA IF NOT EXISTS fraud_graph;

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

CREATE TABLE fraud_graph.dossiers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_id      UUID REFERENCES fraud_graph.clusters(id),
    title           VARCHAR(500) NOT NULL,
    content_json    JSONB NOT NULL,
    pdf_path        VARCHAR(500),
    generated_by    UUID REFERENCES core.users(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- geo_intel
-- ============================================================
CREATE SCHEMA IF NOT EXISTS geo_intel;

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

-- ============================================================
-- citizen_shield
-- ============================================================
CREATE SCHEMA IF NOT EXISTS citizen_shield;

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

CREATE TABLE citizen_shield.chat_messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES citizen_shield.chat_sessions(id),
    role            VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
    content         TEXT NOT NULL,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_session ON citizen_shield.chat_messages (session_id, created_at);

-- ============================================================
-- knowledge_base
-- ============================================================
CREATE SCHEMA IF NOT EXISTS knowledge_base;

CREATE TABLE knowledge_base.patterns (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title           VARCHAR(255) NOT NULL,
    description     TEXT NOT NULL,
    scam_type       VARCHAR(50) NOT NULL,
    language        VARCHAR(10) DEFAULT 'en',
    key_indicators  TEXT[],
    example_scripts TEXT[],
    embedding       vector(384),
    times_matched   INTEGER NOT NULL DEFAULT 0,
    labeled_by      UUID REFERENCES core.users(id),
    verified        BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- qr_scans
-- ============================================================
CREATE SCHEMA IF NOT EXISTS qr_scans;

CREATE TABLE qr_scans.scan_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES core.users(id),
    qr_content      TEXT NOT NULL,
    content_type    VARCHAR(50) NOT NULL
                    CHECK (content_type IN ('upi_payment', 'url', 'bank_account', 'text', 'unknown')),
    destination_account VARCHAR(255),
    destination_url VARCHAR(1000),
    risk_level      VARCHAR(20) NOT NULL
                    CHECK (risk_level IN ('safe', 'caution', 'dangerous')),
    risk_score      INTEGER CHECK (risk_score BETWEEN 0 AND 100),
    complaint_count INTEGER DEFAULT 0,
    explanation     TEXT,
    flags           JSONB DEFAULT '[]',
    scanned_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- panic
-- ============================================================
CREATE SCHEMA IF NOT EXISTS panic;

CREATE TABLE panic.sos_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES core.users(id),
    caller_number   VARCHAR(20),
    call_duration_sec INTEGER,
    location        GEOMETRY(Point, 4326),
    emergency_contact_notified BOOLEAN DEFAULT FALSE,
    emergency_contact_number VARCHAR(20),
    fraud_report_generated BOOLEAN DEFAULT FALSE,
    fraud_report_path VARCHAR(500),
    device_info     JSONB,
    triggered_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

DOWNGRADE_SQL = "\n".join(
    f"DROP SCHEMA IF EXISTS {schema} CASCADE;" for schema in reversed(SCHEMAS)
)


def upgrade() -> None:
    op.execute(UPGRADE_SQL)


def downgrade() -> None:
    op.execute(DOWNGRADE_SQL)
