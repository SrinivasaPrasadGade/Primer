"use client";
import { ChangeEvent, useRef, useState } from "react";
import { Upload, FileText } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/shared/Card";
import { LoadingSkeleton } from "@/components/shared/LoadingSkeleton";
import { api, CaseSummary } from "@/lib/api";
import styles from "@/styles/dashboard.module.css";

const ENTITY_TYPES = ["phone_number", "bank_account", "upi_id", "person", "device", "ip_address", "complaint"];

// Pull the strongest identifier out of an uploaded case/complaint file. The
// backend summarises by entity (it extracts evidence from the DB), so we detect
// the entity from the file's text and hand that to /case/summarize.
function detectEntity(text: string): { type: string; value: string } | null {
    const upi = text.match(/[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}/);
    if (upi) return { type: "upi_id", value: upi[0] };
    // Phone numbers are stored E.164 (+91XXXXXXXXXX); stripping the "+" and country
    // code here produced a lookup that never matched, so every case came back empty.
    const phone = text.match(/(?:\+?91[\s-]?)?[6-9]\d{9}/);
    if (phone) {
        const digits = phone[0].replace(/\D/g, "");
        return { type: "phone_number", value: `+91${digits.slice(-10)}` };
    }
    const account = text.match(/\b\d{9,18}\b/);
    if (account) return { type: "bank_account", value: account[0] };
    return null;
}

export default function CaseSummarizerPage() {
    const inputRef = useRef<HTMLInputElement>(null);
    const [fileName, setFileName] = useState<string | null>(null);
    const [entityType, setEntityType] = useState(ENTITY_TYPES[0]);
    const [entityValue, setEntityValue] = useState("");
    const [summary, setSummary] = useState<CaseSummary | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleFile(e: ChangeEvent<HTMLInputElement>) {
        const file = e.target.files?.[0];
        if (!file) return;
        setError(null);
        setSummary(null);
        setFileName(file.name);
        const text = await file.text();
        const detected = detectEntity(text);
        if (detected) {
            setEntityType(detected.type);
            setEntityValue(detected.value);
        } else {
            setEntityValue("");
            setError("No phone / UPI / account identifier found in the file — enter one manually below.");
        }
    }

    async function handleSummarize() {
        if (!entityValue.trim()) return;
        setLoading(true);
        setError(null);
        try {
            const result = await api.summarizeCase(entityType, entityValue.trim());
            setSummary(result);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to generate summary");
        } finally {
            setLoading(false);
        }
    }

    return (
        <>
            <PageHeader title="Case Summarizer" subtitle="Upload a case file to generate an AI investigation dossier" />

            <Card>
                <div className={styles.caseUpload}>
                    <button className={styles.caseUploadZone} onClick={() => inputRef.current?.click()}>
                        <Upload size={24} />
                        <span>{fileName ? "Replace case file" : "Upload a case / complaint file"}</span>
                        <span className={styles.caseUploadHint}>.txt, .json, .csv, .log</span>
                    </button>
                    <input ref={inputRef} type="file" accept=".txt,.json,.csv,.log,text/*" hidden onChange={handleFile} />

                    {fileName && (
                        <div className={styles.caseFileRow}>
                            <FileText size={16} />
                            <span>{fileName}</span>
                        </div>
                    )}

                    {fileName && (
                        <div className={styles.caseForm}>
                            <select className={styles.caseSelect} value={entityType} onChange={(e) => setEntityType(e.target.value)}>
                                {ENTITY_TYPES.map((t) => (
                                    <option key={t} value={t}>
                                        {t.replace(/_/g, " ")}
                                    </option>
                                ))}
                            </select>
                            <input
                                className={styles.caseInput}
                                placeholder="Detected entity — edit if needed"
                                value={entityValue}
                                onChange={(e) => setEntityValue(e.target.value)}
                            />
                            <button className={styles.caseSubmit} onClick={handleSummarize} disabled={loading || !entityValue.trim()}>
                                {loading ? "Summarizing…" : "Summarize"}
                            </button>
                        </div>
                    )}
                </div>
            </Card>

            {error && <p style={{ color: "var(--color-amber)", fontSize: 13, marginTop: 16 }}>{error}</p>}

            {loading && (
                <div style={{ marginTop: 24 }}>
                    <LoadingSkeleton height={300} />
                </div>
            )}

            {summary && !loading && (
                <div style={{ marginTop: 24 }}>
                    <Card>
                        {summary.confidence_score === 0 && (
                            <p role="alert" style={{ color: "var(--color-red)", fontSize: 13, marginBottom: 12 }}>
                                AI summarization did not run — the evidence was recorded but not analysed. Treat the
                                text below as incomplete, not as a finding.
                            </p>
                        )}
                        <p className={styles.caseSummaryText}>{summary.summary_text}</p>
                        <p style={{ fontSize: 12, color: "var(--color-text-tertiary)", marginBottom: 24 }}>Confidence: {summary.confidence_score}%</p>

                        {summary.timeline_json.length > 0 && (
                            <div className={styles.caseSection}>
                                <p className={styles.caseSectionTitle}>Timeline</p>
                                {summary.timeline_json.map((item, i) => (
                                    <div key={i} className={styles.caseTimelineRow}>
                                        <span style={{ color: "var(--color-text-tertiary)", fontFamily: "var(--font-mono)" }}>{item.date}</span>
                                        <span>{item.event}</span>
                                    </div>
                                ))}
                            </div>
                        )}

                        {summary.suspects_json.length > 0 && (
                            <div className={styles.caseSection}>
                                <p className={styles.caseSectionTitle}>Suspects</p>
                                {summary.suspects_json.map((s, i) => (
                                    <div key={i} className={styles.caseSuspectRow}>
                                        {/* The summarizer emits `identifier`; older records used `name`. */}
                                        <span>{s.identifier ?? s.name ?? "—"}</span>
                                        <span style={{ color: "var(--color-text-tertiary)" }}>{s.role}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </Card>
                </div>
            )}
        </>
    );
}
