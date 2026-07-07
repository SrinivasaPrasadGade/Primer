"""
Generates realistic demo seed data for Primer.
Matches the schema created by backend/migrations/versions/0001_initial_schema.py
(see backend_schema_document.md).

Run manually AFTER `alembic upgrade head` has created the schemas/tables —
this is NOT meant to run as a docker-entrypoint-initdb.d script, since those
scripts execute before the backend runs its Alembic migrations.

Usage:
    cd ml/data_generation
    python generate_seed.py
    psql $DATABASE_URL -f ../../backend/seed_data/01_seed.sql
"""
import json
import os
import random
import sys
import uuid

random.seed(42)

OUT = []


def emit(sql: str) -> None:
    OUT.append(sql.strip() + "\n")


def esc(value) -> str:
    """Escape a Python value for use inside a single-quoted SQL literal position."""
    return str(value).replace("'", "''")


def uid() -> str:
    return str(uuid.uuid4())


def pg_array(values) -> str:
    """Render a Python list as a Postgres TEXT[] literal."""
    inner = ",".join(f'"{esc(v)}"' for v in values)
    return "'{" + inner + "}'"


# ── Reference data ──────────────────────────────────────────────────────────

CITIES = {
    "Mumbai":    {"lat": (18.90, 19.28), "lon": (72.77, 72.98), "state": "Maharashtra", "weight": 0.30},
    "Delhi":     {"lat": (28.50, 28.78), "lon": (76.95, 77.35), "state": "Delhi",       "weight": 0.26},
    "Bangalore": {"lat": (12.85, 13.10), "lon": (77.50, 77.70), "state": "Karnataka",   "weight": 0.22},
    "Hyderabad": {"lat": (17.30, 17.50), "lon": (78.35, 78.55), "state": "Telangana",   "weight": 0.22},
}

SCAM_TYPES = {
    "digital_arrest":    0.35,
    "cbi_impersonation": 0.25,
    "customs_seizure":   0.20,
    "tax_evasion":       0.12,
    "bank_kyc":          0.08,
}

SCAM_PHASES = ["opening", "trust_building", "fear_induction", "payment_demand", "closing"]

CRIME_TYPES = ["digital_arrest", "upi_fraud", "ficn_seizure", "investment_scam", "phishing", "other"]

# geo_intel.incidents.crime_type has a CHECK constraint limited to CRIME_TYPES above,
# which doesn't line up 1:1 with SCAM_TYPES — map each scam_sessions.scam_type to the
# closest allowed crime_type for the cross-linked incidents (see LINKED_SESSION_COUNT).
SCAM_TYPE_TO_CRIME_TYPE = {
    "digital_arrest": "digital_arrest",
    "cbi_impersonation": "other",
    "customs_seizure": "other",
    "tax_evasion": "other",
    "bank_kyc": "phishing",
}

# Number of RED-alert scam_sessions cross-linked into the fraud graph (as a matching
# phone_number entity) and geo-intel map (as an incident with source_ref_id set), so
# the scam_sentinel -> fraud_graph -> geo_intel correlation path has real data to find.
LINKED_SESSION_COUNT = 25

HOUR_WEIGHTS = [1] * 6 + [3, 5, 8, 10, 10, 10, 8, 8, 5, 3, 2, 2, 1, 1, 1, 1, 1, 1]

TELECOM_PROVIDERS = ["Jio", "Airtel", "Vi", "BSNL"]

SCRIPT_TEMPLATES = [
    ("en", "digital_arrest", "Fake CBI Digital Arrest — Parcel Warning",
     "This is Officer {name} from CBI Mumbai. Your Aadhaar-linked parcel containing illegal "
     "substances has been intercepted at customs. You are under digital arrest. Do not disconnect "
     "this call or contact anyone, or a warrant will be issued for your arrest.",
     ["digital arrest", "do not disconnect", "warrant", "aadhaar linked", "customs intercepted"]),
    ("hi", "digital_arrest", "फर्जी सीबीआई डिजिटल गिरफ्तारी — पार्सल चेतावनी",
     "मैं सीबीआई मुंबई से अधिकारी {name} बोल रहा हूं। आपके आधार से जुड़े पार्सल में अवैध सामान मिला है। "
     "आप डिजिटल गिरफ्तारी में हैं। कॉल मत काटिए वरना गिरफ्तारी वारंट जारी होगा।",
     ["डिजिटल गिरफ्तारी", "कॉल मत काटिए", "वारंट", "आधार लिंक"]),
    ("en", "cbi_impersonation", "CBI Impersonation — FIR Threat",
     "We are calling from CBI Delhi headquarters. This is Inspector {name}. An FIR has been registered "
     "against your name in a money laundering case. To avoid immediate arrest, you must verify your "
     "bank account on this call.",
     ["FIR registered", "money laundering", "immediate arrest", "verify bank account"]),
    ("hi", "cbi_impersonation", "सीबीआई फर्जी कॉल — एफआईआर की धमकी",
     "हम सीबीआई दिल्ली मुख्यालय से बोल रहे हैं। मैं इंस्पेक्टर {name} बोल रहा हूं। आपके नाम पर मनी लॉन्ड्रिंग "
     "केस में एफआईआर दर्ज हुई है। गिरफ्तारी से बचने के लिए तुरंत अपना बैंक खाता सत्यापित करें।",
     ["एफआईआर दर्ज", "मनी लॉन्ड्रिंग", "तुरंत गिरफ्तारी", "बैंक खाता सत्यापित"]),
    ("en", "customs_seizure", "Customs Parcel Seizure Scam",
     "This is customs department Mumbai airport. This is Officer {name}. A parcel booked under your "
     "name has been seized, containing banned items and cash worth lakhs. Pay the customs penalty now "
     "to avoid FIR.",
     ["parcel seized", "customs penalty", "banned items", "pay now"]),
    ("hi", "customs_seizure", "सीमा शुल्क पार्सल जब्ती घोटाला",
     "यह मुंबई एयरपोर्ट सीमा शुल्क विभाग है। मैं अधिकारी {name} बोल रहा हूं। आपके नाम से बुक पार्सल जब्त हुआ है "
     "जिसमें प्रतिबंधित सामान है। एफआईआर से बचने के लिए अभी जुर्माना भरें।",
     ["पार्सल जब्त", "जुर्माना भरें", "प्रतिबंधित सामान", "एफआईआर से बचें"]),
    ("en", "tax_evasion", "Income Tax Department Threat Call",
     "This call is from the Income Tax Department, Investigation Wing. I am Officer {name}. "
     "Discrepancies worth several lakhs have been found in your recent filings. A non-bailable warrant "
     "is being prepared unless you settle the pending dues today via UPI.",
     ["income tax department", "non-bailable warrant", "settle dues", "pay via UPI"]),
    ("en", "bank_kyc", "Bank KYC Expiry Fraud",
     "Dear customer, this is {name} from the bank's verification team. Your bank account KYC will be "
     "blocked within 2 hours. Share the OTP sent to your phone immediately to keep your account active "
     "and avoid permanent suspension.",
     ["KYC will be blocked", "share the OTP", "account suspension", "keep account active"]),
    ("hi", "bank_kyc", "बैंक केवाईसी समाप्ति धोखाधड़ी",
     "प्रिय ग्राहक, मैं बैंक सत्यापन टीम से {name} बोल रहा हूं। आपके बैंक खाते का केवाईसी 2 घंटे में ब्लॉक हो "
     "जाएगा। खाता सक्रिय रखने के लिए तुरंत अपने फोन पर आया ओटीपी साझा करें।",
     ["केवाईसी ब्लॉक", "ओटीपी साझा करें", "खाता निलंबन"]),
]

KB_PATTERNS = [
    ("Digital Arrest Impersonation", "digital_arrest",
     "Scammer poses as CBI/police/customs official claiming the victim is under 'digital arrest' and "
     "must stay on video/voice call while transferring funds to 'safe government accounts'.",
     ["stay on call", "safe custody account", "aadhaar linked parcel", "video call surveillance"]),
    ("CBI/Police FIR Threat", "cbi_impersonation",
     "Caller claims an FIR or non-bailable warrant exists against the victim and demands urgent "
     "bank verification or payment to 'settle' the case.",
     ["FIR registered", "non-bailable warrant", "urgent verification"]),
    ("Customs/Courier Parcel Seizure", "customs_seizure",
     "Caller claims a parcel in the victim's name was seized at customs containing contraband, "
     "and demands a penalty payment to avoid prosecution.",
     ["parcel seized", "contraband found", "customs penalty"]),
    ("Fake Income Tax Notice", "tax_evasion",
     "Caller impersonates Income Tax officials citing discrepancies in filings and pressures the "
     "victim to pay 'pending dues' immediately via UPI.",
     ["tax discrepancy", "pending dues", "pay via UPI"]),
    ("KYC Expiry / Account Block", "bank_kyc",
     "SMS or call claims the victim's bank/UPI KYC will expire, requesting OTP or personal banking "
     "details to 'reactivate' the account.",
     ["KYC expiry", "share OTP", "reactivate account"]),
    ("Investment / Trading App Scam", "investment_scam",
     "Victim is lured into a fake trading app showing inflated returns, then blocked from "
     "withdrawing after depositing larger sums.",
     ["guaranteed returns", "fake trading app", "withdrawal blocked"]),
    ("Loan App Harassment", "loan_fraud",
     "Predatory loan apps extract contacts/photos during KYC then use them to harass and blackmail "
     "borrowers into paying inflated amounts.",
     ["instant loan approval", "contact list access", "harassment for repayment"]),
    ("QR Code / UPI Refund Scam", "upi_fraud",
     "Scammer sends a QR code disguised as a 'refund' request; scanning and entering UPI PIN "
     "actually authorizes an outgoing payment.",
     ["scan to receive refund", "enter UPI PIN to collect", "reverse QR trick"]),
    ("Job Offer Advance Fee Scam", "job_scam",
     "Fake recruiter offers a high-paying remote job and asks for 'registration' or 'training kit' "
     "fees upfront before disappearing.",
     ["work from home offer", "registration fee", "training kit payment"]),
    ("Sextortion / Video Call Blackmail", "sextortion",
     "Victim is lured into a compromising video call, recorded without consent, then blackmailed "
     "with threats to share the recording with contacts.",
     ["compromising video call", "recording threat", "share with contacts"]),
    ("Electricity Bill Disconnection Scam", "utility_scam",
     "SMS/call claims electricity connection will be disconnected tonight over unpaid dues, urging "
     "the victim to install a remote-access app to 'pay directly'.",
     ["bill disconnection tonight", "install remote app", "pay directly"]),
]


def weighted_choice(weights_dict):
    keys = list(weights_dict.keys())
    weights = list(weights_dict.values())
    return random.choices(keys, weights=weights)[0]


def city_point():
    city, cfg = weighted_choice({k: v["weight"] for k, v in CITIES.items()}), None
    cfg = CITIES[city]
    lat = round(random.uniform(*cfg["lat"]), 6)
    lon = round(random.uniform(*cfg["lon"]), 6)
    return city, cfg["state"], lat, lon


def rand_phone():
    return f"+91{random.randint(7000000000, 9999999999)}"


def rand_upi():
    handles = ["okaxis", "oksbi", "okhdfcbank", "ybl", "paytm"]
    return f"{random.randint(1000000000, 9999999999)}@{random.choice(handles)}"


def rand_account():
    return "".join(str(random.randint(0, 9)) for _ in range(11))


# ── core: demo users are inserted by the 0001 migration; look them up by email ──
YASHI = "(SELECT id FROM core.users WHERE email = 'yashi@primer.demo')"
SRINIVAS = "(SELECT id FROM core.users WHERE email = 'srinivas@primer.demo')"
SUMANTH_USER = "(SELECT id FROM core.users WHERE email = 'sumanth@primer.demo')"


# ── 1. scam_sentinel.scam_sessions (500: 20% RED / 40% AMBER / 40% YELLOW) ──
def gen_scam_sessions():
    """Returns the RED-alert sessions selected to be cross-linked into the fraud
    graph and geo-intel map (see gen_fraud_graph/gen_geo_incidents), so the
    scam_sentinel -> fraud_graph -> geo_intel correlation path
    (backend/app/services/correlation.py) has real matches to find in the demo."""
    emit("-- scam_sentinel.scam_sessions")
    levels = ["RED"] * 100 + ["AMBER"] * 200 + ["YELLOW"] * 200
    random.shuffle(levels)
    scam_keys = list(SCAM_TYPES.keys())
    scam_weights = list(SCAM_TYPES.values())
    linked_sessions = []

    for level in levels:
        confidence = {
            "RED": random.uniform(85, 99),
            "AMBER": random.uniform(60, 84),
            "YELLOW": random.uniform(30, 59),
        }[level]
        scam_type = random.choices(scam_keys, weights=scam_weights)[0]
        scam_phase = random.choice(SCAM_PHASES)
        duration = random.randint(180, 5400)
        # Anchor on when the call ENDED (not started) so call_start is always
        # further in the past — a call can never end in the future.
        hours_since_end = random.randint(1, 720)
        spoofed = random.random() > 0.55
        deepfake = random.random() > 0.7
        status = random.choices(
            ["active", "classified", "acknowledged", "investigating", "closed"],
            weights=[10, 25, 20, 20, 25],
        )[0]
        signals = json.dumps({
            "call_flow_match": {"score": round(random.uniform(0.7, 0.99), 2)},
            "number_spoofing": {"score": round(random.uniform(0.5, 0.95), 2)},
            "script_similarity": {"score": round(random.uniform(0.6, 0.98), 2)},
            "voice_synthetic": {"score": round(random.uniform(0.3, 0.85), 2)},
            "urgency_phrases": {"score": round(random.uniform(0.7, 1.0), 2)},
        })
        acknowledged = status in ("acknowledged", "investigating", "closed")
        session_id = uid()
        caller = rand_phone()
        callee = rand_phone()

        emit(f"""INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, call_end, call_duration_sec,
             alert_level, overall_confidence, scam_type, scam_phase, signal_scores,
             spoofing_detected, real_originating_number, deepfake_detected,
             voice_synthetic_probability, status, acknowledged_by, acknowledged_at)
            VALUES (
             '{session_id}', '{caller}', '{callee}',
             NOW() - interval '{hours_since_end} hours' - interval '{duration} seconds',
             NOW() - interval '{hours_since_end} hours',
             {duration}, '{level}', {confidence:.1f}, '{scam_type}', '{scam_phase}',
             '{signals}'::jsonb, {str(spoofed).lower()},
             {("'" + rand_phone() + "'") if spoofed else "NULL"},
             {str(deepfake).lower()}, {random.uniform(0.3, 0.9):.2f}, '{status}',
             {YASHI if acknowledged else "NULL"},
             {"NOW() - interval '" + str(random.randint(0, hours_since_end)) + " hours'" if acknowledged else "NULL"}
            );""")

        if level == "RED" and len(linked_sessions) < LINKED_SESSION_COUNT:
            linked_sessions.append(
                {"id": session_id, "caller": caller, "callee": callee, "scam_type": scam_type}
            )
    emit("")
    return linked_sessions


# ── 2. scam_sentinel.number_reputation (100) ────────────────────────────────
def gen_number_reputation():
    emit("-- scam_sentinel.number_reputation")
    numbers = set()
    while len(numbers) < 100:
        numbers.add(rand_phone())

    for phone in numbers:
        blacklisted = random.random() > 0.5
        risk = random.randint(70, 100) if blacklisted else random.randint(0, 60)
        scam_type = random.choice(list(SCAM_TYPES.keys())) if blacklisted else "NULL"
        emit(f"""INSERT INTO scam_sentinel.number_reputation
            (phone_number, risk_score, total_flags, total_complaints, is_blacklisted,
             primary_scam_type, telecom_provider, first_seen, last_flagged, metadata)
            VALUES (
             '{phone}', {risk}, {random.randint(0, 40) if blacklisted else random.randint(0, 3)},
             {random.randint(0, 50) if blacklisted else random.randint(0, 2)},
             {str(blacklisted).lower()},
             {("'" + scam_type + "'") if blacklisted else "NULL"},
             '{random.choice(TELECOM_PROVIDERS)}',
             NOW() - interval '{random.randint(30, 720)} days',
             {("NOW() - interval '" + str(random.randint(0, 60)) + " days'") if blacklisted else "NULL"},
             '{{}}'::jsonb
            );""")
    emit("")


# ── 3. scam_sentinel.scam_script_corpus (50) ────────────────────────────────
def gen_script_corpus():
    emit("-- scam_sentinel.scam_script_corpus")
    names = ["Sharma", "Verma", "Iyer", "Reddy", "Khan", "Rao", "Gupta"]
    # Every template now has a {name} placeholder, so each (template, name) combo
    # renders to distinct content. Sample combos without replacement so the
    # corpus never contains two byte-identical rows.
    combos = [(t, name) for t in range(len(SCRIPT_TEMPLATES)) for name in names]
    random.shuffle(combos)
    for t_idx, name in combos[:50]:
        lang, scam_type, title, content, phrases = SCRIPT_TEMPLATES[t_idx]
        rendered = content.replace("{name}", name)
        emit(f"""INSERT INTO scam_sentinel.scam_script_corpus
            (id, language, scam_type, title, content, key_phrases, times_matched, is_active)
            VALUES (
             '{uid()}', '{lang}', '{scam_type}', '{esc(title)}', '{esc(rendered)}',
             {pg_array(phrases)}, {random.randint(0, 200)}, TRUE
            );""")
    emit("")


# ── 4. note_verify.counterfeit_serials (20) ─────────────────────────────────
def gen_counterfeit_serials():
    emit("-- note_verify.counterfeit_serials")
    for denomination in [500] * 10 + [2000] * 10:
        prefix = random.choice(["3AQ", "7CF", "1XK", "9GH", "4LM"])
        serial = f"{prefix}{random.randint(100000, 999999)}"
        emit(f"""INSERT INTO note_verify.counterfeit_serials
            (serial_number, denomination, first_detected, detection_count, source)
            VALUES (
             '{serial}', {denomination}, NOW() - interval '{random.randint(1, 400)} days',
             {random.randint(1, 25)}, '{random.choice(["NCRP", "RBI Alert", "Bank Report", "system"])}'
            );""")
    emit("")


# ── 5. fraud_graph.entities + edges + clusters (200+ / 400+, 6 clusters) ───
def gen_fraud_graph(linked_sessions):
    emit("-- fraud_graph.clusters")
    cluster_ids = [uid() for _ in range(6)]
    # Named after cities in CITIES only — geo_incidents are plotted from that same
    # set, so a cluster referencing a city with no incidents on the map would look
    # broken in the demo.
    cluster_names = [
        "Mumbai Digital Arrest Ring",
        "Delhi CBI Impersonation Network",
        "Hyderabad Customs Scam Cell",
        "Bangalore UPI Mule Network",
        "Bangalore Tax Notice Syndicate",
        "Mumbai Loan App Harassment Cell",
    ]
    for cid, name in zip(cluster_ids, cluster_names):
        emit(f"""INSERT INTO fraud_graph.clusters
            (id, name, node_count, edge_count, estimated_loss, victim_count, status, detected_at)
            VALUES ('{cid}', '{esc(name)}', 30, 55, {random.uniform(500000, 8000000):.2f},
             {random.randint(8, 60)}, '{random.choice(["active", "monitoring", "dismantled"])}',
             NOW() - interval '{random.randint(5, 300)} days');""")
    emit("")

    emit("-- fraud_graph.entities")
    entity_ids_by_cluster = {cid: [] for cid in cluster_ids}
    entity_types = ["phone_number", "bank_account", "upi_id", "person", "device", "ip_address"]
    # fraud_graph.entities has UNIQUE (entity_type, entity_value) — "person" values
    # in particular are drawn from a small enough space (9000 combos) that plain
    # random.randint collides across ~280 entities, so track everything used.
    used_entity_values = set()

    def gen_entity_value(etype):
        while True:
            if etype == "phone_number":
                value = rand_phone()
            elif etype == "bank_account":
                value = rand_account()
            elif etype == "upi_id":
                value = rand_upi()
            elif etype == "person":
                value = f"Person_{random.randint(1000,9999)}"
            elif etype == "device":
                value = f"IMEI-{random.randint(100000000000000, 999999999999999)}"
            else:
                value = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
            if (etype, value) not in used_entity_values:
                used_entity_values.add((etype, value))
                return value

    # Distribute the RED-alert sessions to be cross-linked round-robin across
    # clusters, so each cluster gets a scam_sessions.caller_number as one of its
    # phone_number entities. That's the join key correlation.py's
    # _matched_entities() uses to walk a session into its fraud-graph cluster.
    linked_by_cluster = {cid: [] for cid in cluster_ids}
    for i, sess in enumerate(linked_sessions):
        linked_by_cluster[cluster_ids[i % len(cluster_ids)]].append(sess)
        used_entity_values.add(("phone_number", sess["caller"]))

    for cid in cluster_ids:
        n_entities = random.randint(35, 45)
        for _ in range(n_entities):
            etype = random.choices(entity_types, weights=[30, 20, 20, 15, 10, 5])[0]
            eid = uid()
            value = gen_entity_value(etype)

            entity_ids_by_cluster[cid].append((eid, etype))
            risk = random.randint(40, 100)
            emit(f"""INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('{eid}', '{etype}', '{esc(value)}', '{esc(value)}', {risk}, '{{}}'::jsonb,
                 '{cid}', NOW() - interval '{random.randint(10, 400)} days', NOW() - interval '{random.randint(0, 10)} days');""")

        for sess in linked_by_cluster[cid]:
            eid = uid()
            entity_ids_by_cluster[cid].append((eid, "phone_number"))
            emit(f"""INSERT INTO fraud_graph.entities
                (id, entity_type, entity_value, display_label, risk_score, properties, cluster_id, first_seen, last_seen)
                VALUES ('{eid}', 'phone_number', '{sess["caller"]}', '{sess["caller"]}', {random.randint(85, 100)},
                 '{{}}'::jsonb, '{cid}', NOW() - interval '{random.randint(10, 400)} days',
                 NOW() - interval '{random.randint(0, 3)} days');""")
    emit("")

    emit("-- fraud_graph.edges")
    relationships = ["called", "transferred_to", "uses_number", "owns_account",
                     "uses_device", "connected_from", "reported_by", "linked_to"]
    edges_generated = 0
    for cid in cluster_ids:
        members = entity_ids_by_cluster[cid]
        n_edges = random.randint(70, 90)
        for _ in range(n_edges):
            src, tgt = random.sample(members, 2)
            rel = random.choice(relationships)
            emit(f"""INSERT INTO fraud_graph.edges
                (id, source_id, target_id, relationship, weight, properties, first_seen, last_seen)
                VALUES ('{uid()}', '{src[0]}', '{tgt[0]}', '{rel}', {random.uniform(1, 25):.2f}, '{{}}'::jsonb,
                 NOW() - interval '{random.randint(1, 300)} days', NOW() - interval '{random.randint(0, 5)} days');""")
            edges_generated += 1
    emit(f"-- total edges generated: {edges_generated}")
    emit("")


# ── 6. geo_intel.incidents (550) ────────────────────────────────────────────
def gen_geo_incidents(linked_sessions):
    emit("-- geo_intel.incidents")

    # Cross-linked incidents: source_module/source_ref_id point back at a real
    # scam_sessions row, which is what correlation.py's _map_incidents() joins on.
    for sess in linked_sessions:
        city, state, lat, lon = city_point()
        crime_type = SCAM_TYPE_TO_CRIME_TYPE[sess["scam_type"]]
        severity = random.choices(["medium", "high", "critical"], weights=[20, 40, 40])[0]
        emit(f"""INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, source_ref_id, reported_at)
            VALUES (
             '{uid()}', '{crime_type}',
             '{esc(crime_type.replace("_", " ").title())} reported in {city}',
             'Correlated with an active scam_sentinel RED alert session.',
             ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326),
             '{state}', '{city}', '{random.randint(400000, 599999)}',
             '{severity}', {random.uniform(5000, 1500000):.2f},
             'scam_sentinel', '{sess["id"]}',
             NOW() - interval '{random.randint(1, 30)} days'
            );""")

    for _ in range(550 - len(linked_sessions)):
        city, state, lat, lon = city_point()
        crime_type = random.choice(CRIME_TYPES)
        severity = random.choices(["low", "medium", "high", "critical"], weights=[20, 40, 30, 10])[0]
        emit(f"""INSERT INTO geo_intel.incidents
            (id, crime_type, title, description, location, state, district, pin_code,
             severity, estimated_loss, source_module, reported_at)
            VALUES (
             '{uid()}', '{crime_type}',
             '{esc(crime_type.replace("_", " ").title())} reported in {city}',
             'Auto-generated demo incident for seed/demo purposes.',
             ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326),
             '{state}', '{city}', '{random.randint(400000, 599999)}',
             '{severity}', {random.uniform(5000, 1500000):.2f},
             '{random.choice(["scam_sentinel", "fraud_graph", "citizen_shield", "note_verify"])}',
             NOW() - interval '{random.randint(1, 365)} days'
            );""")
    emit("")


# ── 7. qr_scans.scan_results — flagged/dangerous (10) ───────────────────────
def gen_qr_flagged():
    emit("-- qr_scans.scan_results (flagged)")
    for _ in range(10):
        upi = rand_upi()
        emit(f"""INSERT INTO qr_scans.scan_results
            (id, user_id, qr_content, content_type, destination_account, risk_level,
             risk_score, complaint_count, explanation, flags)
            VALUES (
             '{uid()}', {SUMANTH_USER}, 'upi://pay?pa={upi}&am=1&cu=INR', 'upi_payment',
             '{upi}', 'dangerous', {random.randint(75, 99)}, {random.randint(3, 40)},
             'This UPI ID is linked to multiple fraud complaints and appears in the fraud graph as a known mule account.',
             '["linked_to_fraud_account", "high_complaint_count", "recently_created"]'::jsonb
            );""")
    emit("")


# ── 8. core.investigations + core.case_summaries (5) ────────────────────────
def gen_case_summaries():
    emit("-- core.investigations + core.case_summaries")
    cases = [
        ("Digital Arrest Fraud Ring — Andheri Cluster", "digital_arrest", "critical",
         "Multi-victim digital arrest scam impersonating CBI officials, funds routed through "
         "3 mule accounts before consolidation into a single UPI wallet."),
        ("CBI Impersonation Network — South Delhi", "cbi_impersonation", "high",
         "Coordinated CBI impersonation scam targeting retired government employees, using "
         "spoofed caller IDs matching real CBI office numbers."),
        ("Customs Seizure Scam — Hyderabad Courier Ring", "customs_seizure", "medium",
         "Courier/customs seizure scam operating from call centre with links to 40+ victim "
         "complaints across Telangana and Andhra Pradesh."),
        ("Income Tax Notice Fraud — Bangalore Tech Corridor", "tax_evasion", "high",
         "Fake Income Tax Investigation Wing calls targeting IT professionals, pressuring "
         "victims to settle fabricated dues via UPI within a fixed window."),
        ("Bank KYC Expiry Scam — Pune Retail Cluster", "bank_kyc", "medium",
         "OTP-harvesting KYC expiry scam targeting retail bank customers, with proceeds "
         "funnelled through a chain of newly opened mule accounts."),
    ]
    for title, ctype, priority, description in cases:
        inv_id = uid()
        emit(f"""INSERT INTO core.investigations
            (id, title, description, type, priority, status, assigned_to, estimated_amount,
             victim_count, tags, created_by)
            VALUES (
             '{inv_id}', '{esc(title)}', '{esc(description)}', '{ctype}', '{priority}',
             '{random.choice(["open", "active"])}', {YASHI}, {random.uniform(500000, 6000000):.2f},
             {random.randint(5, 60)}, {pg_array([ctype, "seed_demo"])}, {YASHI}
            );""")

        timeline = json.dumps([
            {"stage": "first_complaint_filed", "days_ago": random.randint(60, 90)},
            {"stage": "pattern_identified", "days_ago": random.randint(30, 59)},
            {"stage": "fraud_graph_cluster_confirmed", "days_ago": random.randint(10, 29)},
            {"stage": "investigation_opened", "days_ago": random.randint(1, 9)},
        ])
        suspects = json.dumps([
            {"role": "call_operator", "status": "unidentified"},
            {"role": "mule_account_holder", "status": "identified", "risk": "high"},
        ])
        related = json.dumps([f"NCRP-{random.randint(100000, 999999)}" for _ in range(3)])

        emit(f"""INSERT INTO core.case_summaries
            (id, investigation_id, summary_text, timeline_json, suspects_json, related_complaints,
             confidence_score, source_evidence, generated_by)
            VALUES (
             '{uid()}', '{inv_id}',
             '{esc(description)} Cross-referenced against the fraud graph and geo-intel modules, '
             'this case shows a consistent operational pattern with escalating victim counts over '
             'the last quarter.',
             '{timeline}'::jsonb, '{suspects}'::jsonb, '{related}'::jsonb,
             {random.uniform(70, 95):.2f}, {pg_array(["call_recording", "cdr_log", "fraud_graph_cluster"])},
             'gemini'
            );""")
    emit("")


# ── 9. knowledge_base.patterns (10+) ────────────────────────────────────────
def gen_kb_patterns():
    emit("-- knowledge_base.patterns")
    for title, scam_type, description, indicators in KB_PATTERNS:
        emit(f"""INSERT INTO knowledge_base.patterns
            (id, title, description, scam_type, language, key_indicators, example_scripts,
             times_matched, labeled_by, verified)
            VALUES (
             '{uid()}', '{esc(title)}', '{esc(description)}', '{scam_type}', 'en',
             {pg_array(indicators)}, {pg_array([description[:80]])},
             {random.randint(5, 300)}, {YASHI}, TRUE
            );""")
    emit("")


def main():
    emit("BEGIN;")
    emit("")
    linked_sessions = gen_scam_sessions()
    gen_number_reputation()
    gen_script_corpus()
    gen_counterfeit_serials()
    gen_fraud_graph(linked_sessions)
    gen_geo_incidents(linked_sessions)
    gen_qr_flagged()
    gen_case_summaries()
    gen_kb_patterns()
    emit("COMMIT;")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "..", "..", "backend", "seed_data", "01_seed.sql")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(OUT))
    print(f"Wrote {len(OUT)} SQL statement blocks to {os.path.normpath(out_path)}", file=sys.stderr)


if __name__ == "__main__":
    main()
