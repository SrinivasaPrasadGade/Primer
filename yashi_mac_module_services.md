# Yashi — Module Services & Business Logic (Mac M3 Pro)

## **Primer — Developer Task Sheet**

| Field | Detail |
|---|---|
| **Owner** | Yashi |
| **Machine** | MacBook Pro M3 |
| **Role** | Module business logic: signal scoring, graph queries, PostGIS ops, NLU, QR risk, KB similarity |
| **Stack** | Python 3.12, SQLAlchemy, sentence-transformers, FAISS, PostGIS, Jinja2, WeasyPrint |
| **Companion Docs** | [TRD](technical_requirements_document.md) · [Backend Schema](backend_schema_document.md) · [Srinivas Doc](srinivas_mac_core_backend.md) |

---

## 1. Role Clarification — Yashi vs Srinivas

```
Srinivas (API Layer):  HTTP handlers, request validation, auth checks, response formatting
Yashi (Logic Layer):   Signal scoring, graph algorithms, spatial queries, NLU, risk assessment

Srinivas calls Yashi's service functions.
```

**Example:**

```python
# Srinivas writes: backend/app/routers/scam_sentinel.py
@router.get("/sessions/{id}")
async def get_session(id: UUID, db=Depends(get_db)):
    return await scam_service.get_session_detail(db, id)  # ← calls Yashi's code

# Yashi writes: backend/app/services/scam_sentinel.py
async def get_session_detail(db, session_id: UUID):
    session = await db.get(ScamSession, session_id)
    session.signal_explanations = generate_signal_explanations(session.signal_scores)
    return session
```

All of Yashi's code lives in `backend/app/services/`.

---

## 2. Machine Setup

```bash
# Python 3.12
brew install python@3.12

# Project setup
cd primer/backend
source .venv/bin/activate  # Use same venv as Srinivas

# Additional packages Yashi needs (add to requirements.txt)
pip install sentence-transformers faiss-cpu geoalchemy2 shapely langdetect
```

---

## 3. Service Files — What Yashi Writes

```
backend/app/services/
├── scam_sentinel.py      Scam session processing, signal scoring, alert classification
├── note_verify.py        Currency feature analysis, serial lookup
├── fraud_graph.py        Graph queries (recursive CTEs), community detection, money flow
├── geo_intel.py          PostGIS heatmap queries, hotspot integration
├── citizen_shield.py     Gemini chat prompts, language detection, risk assessment
├── copilot.py            NL query parsing, function calling, result formatting
├── qr_scanner.py         QR content parsing, UPI/URL risk assessment
├── case_summary.py       Evidence extraction, Gemini summarisation prompts
├── knowledge_base.py     Pattern similarity search, embedding management
└── dossier.py            PDF generation (Jinja2 + WeasyPrint)
```

---

## 4. Module 1 — Scam Sentinel (Signal Scoring)

### 4.1 Signal Score Computation

```python
# backend/app/services/scam_sentinel.py
from dataclasses import dataclass

@dataclass
class SignalResult:
    score: float          # 0.0 to 1.0
    explanation: str      # Human-readable reason

async def compute_signal_scores(session_data: dict) -> dict:
    """Compute all signal scores for a scam session.
    Returns dict of signal_name → {score, explanation}
    Used by Explainable AI to show why a session was flagged.
    """
    signals = {}

    # Signal 1: Call Flow Pattern Match
    signals["call_flow_match"] = await match_call_flow_pattern(session_data)

    # Signal 2: Number Spoofing Detection
    signals["number_spoofing"] = detect_number_spoofing(session_data)

    # Signal 3: Script Similarity (uses sentence-transformers)
    signals["script_similarity"] = await compute_script_similarity(
        session_data.get("transcript_text", "")
    )

    # Signal 4: Voice Synthetic Probability (from ML model output)
    signals["voice_synthetic"] = SignalResult(
        score=session_data.get("voice_synthetic_probability", 0),
        explanation=generate_voice_explanation(session_data)
    )

    # Signal 5: Urgency Phrase Detection
    signals["urgency_phrases"] = detect_urgency_phrases(
        session_data.get("transcript_text", "")
    )

    return {name: {"score": round(s.score, 2), "explanation": s.explanation}
            for name, s in signals.items()}

def classify_alert_level(overall_confidence: float) -> str:
    """RED ≥ 85%, AMBER 60-84%, YELLOW < 60%"""
    if overall_confidence >= 0.85:
        return "RED"
    elif overall_confidence >= 0.60:
        return "AMBER"
    return "YELLOW"
```

### 4.2 Script Similarity (Sentence-Transformers + FAISS)

```python
# backend/app/services/scam_sentinel.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load once at startup
_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
_corpus_index = None
_corpus_texts = []

async def load_script_corpus(db):
    """Load scam script corpus from DB into FAISS index."""
    global _corpus_index, _corpus_texts
    scripts = await db.execute(select(ScamScriptCorpus).where(ScamScriptCorpus.is_active == True))
    _corpus_texts = [s.content for s in scripts.scalars()]
    embeddings = _model.encode(_corpus_texts, normalize_embeddings=True)
    _corpus_index = faiss.IndexFlatIP(384)
    _corpus_index.add(embeddings.astype(np.float32))

async def compute_script_similarity(text: str) -> SignalResult:
    """Compare text against known scam scripts."""
    if not text or _corpus_index is None:
        return SignalResult(score=0.0, explanation="No transcript available")

    embedding = _model.encode([text], normalize_embeddings=True).astype(np.float32)
    scores, indices = _corpus_index.search(embedding, k=3)
    top_score = float(scores[0][0])
    top_match_idx = int(indices[0][0])

    return SignalResult(
        score=max(0, min(1, top_score)),
        explanation=f"Matches template #{top_match_idx + 1} — seen {_corpus_texts[top_match_idx][:50]}..."
    )

URGENCY_PHRASES = {
    "en": ["arrest warrant", "immediate transfer", "fir against you", "money laundering",
           "supreme court order", "digital arrest", "aadhaar linked", "account frozen"],
    "hi": ["गिरफ्तारी वारंट", "तुरंत ट्रांसफर", "आपके खिलाफ FIR", "मनी लॉन्ड्रिंग",
           "सुप्रीम कोर्ट का आदेश", "डिजिटल अरेस्ट", "आधार लिंक", "अकाउंट फ्रीज"]
}

def detect_urgency_phrases(text: str) -> SignalResult:
    """Detect urgency/coercion phrases in call transcript."""
    if not text:
        return SignalResult(score=0.0, explanation="No transcript available")

    text_lower = text.lower()
    found = [p for lang_phrases in URGENCY_PHRASES.values() for p in lang_phrases if p in text_lower]

    if not found:
        return SignalResult(score=0.0, explanation="No urgency phrases detected")

    score = min(1.0, len(found) * 0.15 + 0.4)
    return SignalResult(
        score=score,
        explanation=f"Detected: {', '.join(found[:3])}"
    )
```

---

## 5. Module 2 — Fraud Graph (PostgreSQL-based)

### 5.1 Graph Queries

```python
# backend/app/services/fraud_graph.py
from sqlalchemy import text

async def get_entity_neighbourhood(db, entity_type: str, entity_value: str, depth: int = 2):
    """Get N-hop neighbourhood of an entity using recursive CTE."""
    query = text("""
        WITH RECURSIVE hops AS (
            SELECT e.id, e.entity_type, e.entity_value, e.risk_score,
                   e.display_label, e.properties, e.cluster_id, 0 AS depth
            FROM fraud_graph.entities e
            WHERE e.entity_type = :type AND e.entity_value = :value

            UNION ALL

            SELECT e2.id, e2.entity_type, e2.entity_value, e2.risk_score,
                   e2.display_label, e2.properties, e2.cluster_id, h.depth + 1
            FROM hops h
            JOIN fraud_graph.edges eg ON (eg.source_id = h.id OR eg.target_id = h.id)
            JOIN fraud_graph.entities e2 ON (
                e2.id = CASE WHEN eg.source_id = h.id THEN eg.target_id ELSE eg.source_id END
            )
            WHERE h.depth < :depth
        )
        SELECT DISTINCT ON (id) * FROM hops;
    """)
    result = await db.execute(query, {"type": entity_type, "value": entity_value, "depth": depth})
    nodes = [dict(row._mapping) for row in result]

    # Get edges between found nodes
    node_ids = [n["id"] for n in nodes]
    edges_query = text("""
        SELECT e.*, 
               s.entity_value as source_label, t.entity_value as target_label
        FROM fraud_graph.edges e
        JOIN fraud_graph.entities s ON e.source_id = s.id
        JOIN fraud_graph.entities t ON e.target_id = t.id
        WHERE e.source_id = ANY(:ids) AND e.target_id = ANY(:ids)
    """)
    edges_result = await db.execute(edges_query, {"ids": node_ids})
    edges = [dict(row._mapping) for row in edges_result]

    return {"nodes": nodes, "edges": edges}

async def get_money_flow(db, entity_id: str):
    """Trace money flow through accounts connected to an entity."""
    query = text("""
        SELECT e.source_id, e.target_id, e.relationship, e.weight as amount,
               s.entity_value as from_entity, t.entity_value as to_entity,
               s.entity_type as from_type, t.entity_type as to_type
        FROM fraud_graph.edges e
        JOIN fraud_graph.entities s ON e.source_id = s.id
        JOIN fraud_graph.entities t ON e.target_id = t.id
        WHERE e.relationship = 'transferred_to'
        AND (e.source_id IN (
            SELECT id FROM fraud_graph.entities WHERE cluster_id = (
                SELECT cluster_id FROM fraud_graph.entities WHERE id = :entity_id
            )
        ))
        ORDER BY e.first_seen
    """)
    result = await db.execute(query, {"entity_id": entity_id})
    return [dict(row._mapping) for row in result]
```

### 5.2 Simple Community Detection (Label Propagation)

```python
# backend/app/services/fraud_graph.py
async def detect_communities(db):
    """Simple label propagation for community detection.
    Not as sophisticated as Neo4j GDS, but works for demo.
    """
    # Fetch all edges
    edges = await db.execute(text("SELECT source_id, target_id FROM fraud_graph.edges"))
    
    # Build adjacency list
    from collections import defaultdict
    graph = defaultdict(set)
    for row in edges:
        graph[str(row.source_id)].add(str(row.target_id))
        graph[str(row.target_id)].add(str(row.source_id))

    # Union-Find for connected components
    parent = {}
    def find(x):
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x, y):
        parent[find(x)] = find(y)

    for node, neighbours in graph.items():
        for neighbour in neighbours:
            union(node, neighbour)

    # Group into clusters
    clusters = defaultdict(list)
    for node in graph:
        clusters[find(node)].append(node)

    return {k: v for k, v in clusters.items() if len(v) >= 3}  # Min 3 nodes = cluster
```

---

## 6. Module 3 — Geo Intel (PostGIS Queries)

```python
# backend/app/services/geo_intel.py
from sqlalchemy import text

async def get_heatmap_data(db, bounds: dict, crime_type: str = None, days: int = 7):
    """Aggregate incidents into grid cells for heatmap visualisation."""
    query = text("""
        SELECT
            ST_X(location) as lng,
            ST_Y(location) as lat,
            COUNT(*) as intensity,
            crime_type
        FROM geo_intel.incidents
        WHERE reported_at >= NOW() - :days * INTERVAL '1 day'
        AND ST_Within(location, ST_MakeEnvelope(:west, :south, :east, :north, 4326))
        GROUP BY ST_SnapToGrid(location, 0.01), crime_type
        ORDER BY intensity DESC
    """)
    params = {**bounds, "days": days}
    result = await db.execute(query, params)
    return [dict(row._mapping) for row in result]

async def get_incident_pins(db, bounds: dict, crime_type: str = None, limit: int = 500):
    """Get individual incident pins for map display."""
    query = text("""
        SELECT id, crime_type, title, description,
               ST_X(location) as lng, ST_Y(location) as lat,
               severity, estimated_loss, reported_at
        FROM geo_intel.incidents
        WHERE ST_Within(location, ST_MakeEnvelope(:west, :south, :east, :north, 4326))
        ORDER BY reported_at DESC
        LIMIT :limit
    """)
    result = await db.execute(query, {**bounds, "limit": limit})
    return [dict(row._mapping) for row in result]
```

---

## 7. Extra Features Logic

### 7.1 QR Scanner — Risk Assessment

```python
# backend/app/services/qr_scanner.py
import re
from urllib.parse import urlparse

async def assess_qr_risk(db, qr_content: str) -> dict:
    """Parse QR content, identify type, check against fraud databases."""

    # Detect content type
    if qr_content.startswith("upi://"):
        return await assess_upi_qr(db, qr_content)
    elif qr_content.startswith("http"):
        return await assess_url_qr(db, qr_content)
    else:
        return {"risk_level": "safe", "content_type": "text", "explanation": "Plain text QR code"}

async def assess_upi_qr(db, upi_string: str) -> dict:
    """Check UPI payment QR against fraud database."""
    # Parse UPI: upi://pay?pa=xyz@ybl&pn=Name&am=1000
    params = dict(re.findall(r'(\w+)=([^&]+)', upi_string))
    upi_id = params.get("pa", "")

    # Check if UPI ID is in fraud graph
    entity = await db.execute(text("""
        SELECT e.*, COUNT(eg.id) as connection_count
        FROM fraud_graph.entities e
        LEFT JOIN fraud_graph.edges eg ON e.id = eg.source_id OR e.id = eg.target_id
        WHERE e.entity_type = 'upi_id' AND e.entity_value = :upi
        GROUP BY e.id
    """), {"upi": upi_id})
    entity = entity.first()

    if entity and entity.risk_score >= 70:
        return {
            "risk_level": "dangerous",
            "content_type": "upi_payment",
            "destination_account": upi_id,
            "risk_score": entity.risk_score,
            "complaint_count": entity.connection_count,
            "explanation": f"Known fraud account with {entity.connection_count} linked complaints"
        }
    elif entity and entity.risk_score >= 30:
        return {
            "risk_level": "caution",
            "content_type": "upi_payment",
            "destination_account": upi_id,
            "risk_score": entity.risk_score,
            "complaint_count": entity.connection_count,
            "explanation": "Some suspicious activity linked to this account"
        }
    return {
        "risk_level": "safe",
        "content_type": "upi_payment",
        "destination_account": upi_id,
        "risk_score": 0,
        "complaint_count": 0,
        "explanation": "No known issues with this account"
    }
```

### 7.2 AI Copilot — Query Parsing

```python
# backend/app/services/copilot.py
from app.services.gemini_client import generate

COPILOT_SYSTEM = """You are an AI investigation assistant for the Primer fraud intelligence platform.
You help law enforcement officers query across fraud databases.
When the user asks a question, determine which function to call and with what parameters.
Always be precise and cite the data source."""

async def process_query(db, question: str) -> dict:
    """Process natural language query from officer.
    Uses Gemini function calling to convert NL → structured DB query.
    """
    # For MVP: pattern match common queries, fallback to Gemini
    question_lower = question.lower()

    if "complaints linked to" in question_lower or "complaints for" in question_lower:
        # Extract entity from question
        entity = extract_entity_from_question(question)
        results = await search_complaints_by_entity(db, entity)
        return format_copilot_response(question, results)

    elif "victims contacted by" in question_lower:
        phone = extract_phone_from_question(question)
        results = await find_victims_of_number(db, phone)
        return format_copilot_response(question, results)

    elif "total loss" in question_lower:
        entity = extract_entity_from_question(question)
        results = await calculate_total_loss(db, entity)
        return format_copilot_response(question, results)

    else:
        # Fallback: send to Gemini for general analysis
        response = await generate(
            prompt=f"Officer asks: {question}\n\nProvide a helpful analysis.",
            system_instruction=COPILOT_SYSTEM
        )
        return {"answer": response, "data": [], "sources": ["gemini"]}
```

### 7.3 Case Summarizer

```python
# backend/app/services/case_summary.py
from app.services.gemini_client import generate
import json

SUMMARIZER_PROMPT = """You are a forensic case analyst. Given the following evidence,
generate a structured case summary in JSON format with these fields:
- summary: 2-3 sentence executive summary
- timeline: array of {date, event} objects in chronological order
- suspects: array of {identifier, type, role, risk_score} objects
- related_complaints: array of complaint IDs
- confidence_score: 0-100 score of how confident you are in the analysis

Evidence:
{evidence}

Respond ONLY with valid JSON."""

async def generate_case_summary(evidence_text: str, complaint_ids: list = None) -> dict:
    """Generate structured case summary using Gemini."""
    response = await generate(
        prompt=SUMMARIZER_PROMPT.format(evidence=evidence_text),
        system_instruction="You are a forensic case analyst. Output only valid JSON."
    )
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"summary": response, "timeline": [], "suspects": [], "confidence_score": 50}
```

### 7.4 Knowledge Base — Similarity Search

```python
# backend/app/services/knowledge_base.py
async def find_similar_patterns(db, description: str, top_k: int = 5) -> list:
    """Find similar fraud patterns using vector similarity.
    Uses pgvector for similarity search.
    """
    embedding = _model.encode([description], normalize_embeddings=True)[0]

    query = text("""
        SELECT id, title, description, scam_type, key_indicators,
               1 - (embedding <=> :embedding::vector) as similarity
        FROM knowledge_base.patterns
        WHERE verified = true
        ORDER BY embedding <=> :embedding::vector
        LIMIT :k
    """)
    result = await db.execute(query, {"embedding": embedding.tolist(), "k": top_k})
    return [dict(row._mapping) for row in result]

async def add_pattern(db, title: str, description: str, scam_type: str, labeled_by: str):
    """Analyst labels a new pattern → embed → store."""
    embedding = _model.encode([description], normalize_embeddings=True)[0]

    await db.execute(text("""
        INSERT INTO knowledge_base.patterns (title, description, scam_type, embedding, labeled_by)
        VALUES (:title, :description, :scam_type, :embedding::vector, :labeled_by)
    """), {
        "title": title, "description": description,
        "scam_type": scam_type, "embedding": embedding.tolist(),
        "labeled_by": labeled_by
    })
    await db.commit()
```

---

## 8. Dossier PDF Generation

```python
# backend/app/services/dossier.py
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

env = Environment(loader=FileSystemLoader("app/templates"))

async def generate_dossier(db, cluster_id: str, officer_id: str) -> str:
    """Generate a PDF evidence dossier for a fraud cluster."""
    # Gather data
    cluster = await get_cluster_data(db, cluster_id)
    nodes = await get_cluster_entities(db, cluster_id)
    edges = await get_cluster_edges(db, cluster_id)
    timeline = await get_cluster_timeline(db, cluster_id)

    # Render template
    template = env.get_template("dossier.html")
    html_content = template.render(
        cluster=cluster,
        nodes=nodes,
        edges=edges,
        timeline=timeline,
        generated_at=datetime.now().isoformat(),
        generated_by=officer_id,
    )

    # Generate PDF
    output_path = f"uploads/dossiers/dossier_{cluster_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
    HTML(string=html_content).write_pdf(output_path)

    # Store reference in DB
    await db.execute(text("""
        INSERT INTO fraud_graph.dossiers (cluster_id, title, content_json, pdf_path, generated_by)
        VALUES (:cluster_id, :title, :content, :pdf_path, :officer_id)
    """), {
        "cluster_id": cluster_id,
        "title": f"Dossier — {cluster['name']}",
        "content": json.dumps({"nodes": len(nodes), "edges": len(edges)}),
        "pdf_path": output_path,
        "officer_id": officer_id
    })
    await db.commit()
    return output_path
```

---

## 9. Task Checklist (Phase 2: Yashi)

### 1. Scam Sentinel & Graph Logic
- [ ] Scam Sentinel: signal scoring (all 5 signals)
- [ ] Scam Sentinel: urgency phrase detection (Hindi + English)
- [ ] Scam Sentinel: script similarity (sentence-transformers + FAISS)
- [ ] Scam Sentinel: alert level classification
- [ ] Number reputation scoring algorithm
- [ ] Fraud Graph: entity neighbourhood query (recursive CTE)
- [ ] Fraud Graph: community detection (union-find)
- [ ] Fraud Graph: money flow tracing

### 2. Geo Intel & Citizen Shield Logic
- [ ] Geo Intel: PostGIS heatmap aggregation
- [ ] Geo Intel: incident pins query
- [ ] Geo Intel: hotspot prediction integration
- [ ] Citizen Shield: Gemini prompt templates (fraud advisor)
- [ ] Citizen Shield: language detection (langdetect)
- [ ] Knowledge Base: similarity search + pattern labeling

### 3. Extra Features Logic
- [ ] AI Copilot: query parsing + DB query generation
- [ ] QR Scanner: UPI parsing + risk assessment
- [ ] QR Scanner: URL domain reputation check
- [ ] Case Summarizer: evidence extraction + Gemini prompts
- [ ] Dossier: PDF template + generation logic
- [ ] Deepfake voice: inference wrapper for model output
- [ ] Integration testing: all services work with Srinivas's routers
- [ ] Performance: ensure graph queries < 2s for 100 nodes
