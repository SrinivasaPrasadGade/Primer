"use client";
import { ChangeEvent, useRef, useState } from "react";
import { Upload } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/shared/Card";
import { StatCard } from "@/components/dashboard/StatCard";
import { LoadingSkeleton } from "@/components/shared/LoadingSkeleton";
import { useApi } from "@/hooks/useApi";
import { api, NoteVerifyResult } from "@/lib/api";
import styles from "@/styles/dashboard.module.css";

const VERDICT_CLASS: Record<string, string> = {
    GENUINE: styles.verdictGenuine,
    SUSPECT: styles.verdictSuspect,
    COUNTERFEIT: styles.verdictCounterfeit,
};

function fileToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result as string);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

export default function NoteVerifyDashboard() {
    const [latest, setLatest] = useState<NoteVerifyResult | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);
    const [uploadError, setUploadError] = useState<string | null>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    const { data: stats, isLoading: statsLoading, mutate: mutateStats } = useApi("note-stats", () => api.getNoteStats());
    const { data: history, isLoading: historyLoading, mutate: mutateHistory } = useApi("note-history", () => api.getNoteHistory(10));

    async function handleFile(e: ChangeEvent<HTMLInputElement>) {
        const file = e.target.files?.[0];
        if (!file) return;
        setUploadError(null);
        const base64 = await fileToBase64(file);
        setPreview(base64);
        setSubmitting(true);
        try {
            const result = await api.verifyNote({ image_base64: base64, scan_source: "web" });
            setLatest(result);
            mutateStats();
            mutateHistory();
        } catch (err) {
            setUploadError(err instanceof Error ? err.message : "Verification failed");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <>
            <PageHeader title="Note Verify" subtitle="Camera-based counterfeit currency detection" />

            <div className={styles.statGrid}>
                {statsLoading ? (
                    Array.from({ length: 4 }).map((_, i) => <LoadingSkeleton key={i} height={78} />)
                ) : (
                    <>
                        <StatCard label="Total Scans" value={stats?.total_scans ?? 0} />
                        <StatCard label="Genuine" value={stats?.genuine_count ?? 0} tone="green" />
                        <StatCard label="Suspect" value={stats?.suspect_count ?? 0} tone="amber" />
                        <StatCard label="Counterfeit" value={stats?.counterfeit_count ?? 0} tone="red" />
                    </>
                )}
            </div>

            <div className={styles.notesGrid}>
                <Card>
                    <div className={styles.notesUpload}>
                        {preview ? (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img src={preview} alt="Note preview" className={styles.notesUploadPreview} />
                        ) : (
                            <div className={styles.notesUploadPlaceholder}>
                                <Upload size={28} />
                                <span>Upload a currency note photo</span>
                            </div>
                        )}
                        <button className={styles.notesUploadButton} onClick={() => inputRef.current?.click()} disabled={submitting}>
                            {submitting ? "Analyzing…" : "Choose Image"}
                        </button>
                        <input ref={inputRef} type="file" accept="image/*" hidden onChange={handleFile} />
                        {uploadError && <p className={styles.notesError}>{uploadError}</p>}
                    </div>
                </Card>

                <Card>
                    {latest ? (
                        <>
                            <p className={`${styles.notesVerdict} ${VERDICT_CLASS[latest.verdict]}`}>{latest.verdict}</p>
                            <p style={{ fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 16 }}>
                                Confidence {latest.confidence.toFixed(1)}% · ₹{latest.denomination}
                            </p>
                            {Object.entries(latest.feature_analysis).map(([name, score]) => (
                                <div key={name} className={styles.notesFeatureRow}>
                                    <span>{name.replace(/_/g, " ")}</span>
                                    <span style={{ fontFamily: "var(--font-mono)" }}>{(score * 100).toFixed(0)}%</span>
                                </div>
                            ))}
                        </>
                    ) : (
                        <p style={{ color: "var(--color-text-tertiary)", fontSize: 13 }}>
                            Upload a note image to see the verdict and Explainable AI feature breakdown.
                        </p>
                    )}
                </Card>
            </div>

            <div style={{ marginTop: 32 }}>
                <h3 className={styles.sectionTitle} style={{ marginBottom: 16 }}>
                    Recent Scans
                </h3>
                {historyLoading ? (
                    <LoadingSkeleton height={120} />
                ) : (
                    (history ?? []).map((entry) => (
                        <div key={entry.id} className={styles.notesHistoryRow}>
                            <span className={VERDICT_CLASS[entry.verdict]}>{entry.verdict}</span>
                            <span>₹{entry.denomination}</span>
                            <span style={{ flex: 1, color: "var(--color-text-tertiary)" }}>{entry.scan_source}</span>
                            <span style={{ fontFamily: "var(--font-mono)" }}>{entry.confidence.toFixed(1)}%</span>
                        </div>
                    ))
                )}
            </div>
        </>
    );
}
