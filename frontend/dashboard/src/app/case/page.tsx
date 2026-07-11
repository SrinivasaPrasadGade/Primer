"use client";
import { FormEvent, useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/shared/Card";
import { LoadingSkeleton } from "@/components/shared/LoadingSkeleton";
import { api, CaseSummary } from "@/lib/api";
import styles from "@/styles/dashboard.module.css";

const ENTITY_TYPES = ["phone_number", "bank_account", "upi_id", "person", "device", "ip_address", "complaint"];

export default function CaseSummarizerPage() {
    const [entityType, setEntityType] = useState(ENTITY_TYPES[0]);
    const [entityValue, setEntityValue] = useState("");
    const [summary, setSummary] = useState<CaseSummary | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();
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
            <PageHeader title="Case Summarizer" subtitle="AI-generated investigation dossier for any entity" />

            <form className={styles.caseForm} onSubmit={handleSubmit}>
                <select className={styles.caseSelect} value={entityType} onChange={(e) => setEntityType(e.target.value)}>
                    {ENTITY_TYPES.map((t) => (
                        <option key={t} value={t}>
                            {t.replace(/_/g, " ")}
                        </option>
                    ))}
                </select>
                <input
                    className={styles.caseInput}
                    placeholder="Entity value (e.g. phone number, UPI ID)…"
                    value={entityValue}
                    onChange={(e) => setEntityValue(e.target.value)}
                />
                <button className={styles.caseSubmit} type="submit" disabled={loading}>
                    {loading ? "Summarizing…" : "Summarize"}
                </button>
            </form>

            {error && <p style={{ color: "var(--color-red)", fontSize: 13 }}>{error}</p>}

            {loading && <LoadingSkeleton height={300} />}

            {summary && !loading && (
                <Card>
                    <p className={styles.caseSummaryText}>{summary.summary_text}</p>
                    <p style={{ fontSize: 12, color: "var(--color-text-tertiary)", marginBottom: 24 }}>
                        Confidence: {summary.confidence_score}%
                    </p>

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
                                    <span>{s.name}</span>
                                    <span style={{ color: "var(--color-text-tertiary)" }}>{s.role}</span>
                                </div>
                            ))}
                        </div>
                    )}
                </Card>
            )}
        </>
    );
}
