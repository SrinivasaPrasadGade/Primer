"use client";
import { ChangeEvent, useRef, useState } from "react";
import { Upload, FileText } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/shared/Card";
import { LoadingSkeleton } from "@/components/shared/LoadingSkeleton";
import { api, CaseSummary } from "@/lib/api";
import styles from "@/styles/dashboard.module.css";

export default function CaseSummarizerPage() {
    const inputRef = useRef<HTMLInputElement>(null);
    const [file, setFile] = useState<File | null>(null);
    const [summary, setSummary] = useState<CaseSummary | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    function handleFile(e: ChangeEvent<HTMLInputElement>) {
        const selected = e.target.files?.[0];
        if (!selected) return;
        setError(null);
        setSummary(null);
        setFile(selected);
    }

    async function handleSummarize() {
        if (!file) return;
        setLoading(true);
        setError(null);
        try {
            // Send the file verbatim — the server summarises its text directly.
            const result = await api.summarizeCaseFile(file);
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
                        <span>{file ? "Replace case file" : "Upload a case / complaint file"}</span>
                        <span className={styles.caseUploadHint}>.txt, .json, .csv, .log</span>
                    </button>
                    <input ref={inputRef} type="file" accept=".txt,.json,.csv,.log,text/*" hidden onChange={handleFile} />

                    {file && (
                        <div className={styles.caseFileRow}>
                            <FileText size={16} />
                            <span>{file.name}</span>
                        </div>
                    )}

                    {file && (
                        <div className={styles.caseForm}>
                            <button className={styles.caseSubmit} onClick={handleSummarize} disabled={loading}>
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
                                        <span>{s.name}</span>
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
