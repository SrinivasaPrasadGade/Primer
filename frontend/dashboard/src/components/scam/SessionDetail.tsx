"use client";
import { Badge } from "@/components/shared/Badge";
import { Card } from "@/components/shared/Card";
import { ConfidenceBar } from "@/components/shared/ConfidenceBar";
import { ExplainableAI } from "./ExplainableAI";
import { ScamSessionDetail } from "@/lib/api";
import styles from "@/styles/scam.module.css";

const STATUS_LABEL: Record<string, string> = {
    active: "Awaiting classification",
    classified: "Classified — not yet acknowledged",
    acknowledged: "Acknowledged",
    investigating: "Under investigation",
    closed: "Closed",
};

export function SessionDetail({
    session,
    onAcknowledge,
    onReclassify,
    pendingAction = null,
    actionError = null,
}: {
    session: ScamSessionDetail;
    onAcknowledge: () => void;
    onReclassify: () => void;
    pendingAction?: "acknowledge" | "reclassify" | null;
    actionError?: string | null;
}) {
    const status = session.status ?? "active";
    // Acknowledging twice is a no-op server-side; showing it as already done is the
    // only on-screen evidence the first click had any effect.
    const isAcknowledged = status === "acknowledged";
    const busy = pendingAction !== null;

    return (
        <div className={styles.detailGrid}>
            <Card>
                <div className={styles.detailHeader}>
                    <Badge level={session.alert_level} />
                    <span>{session.scam_type}</span>
                    {session.deepfake_detected && <Badge level="AMBER" label="AI Voice" />}
                </div>
                <ConfidenceBar value={session.overall_confidence} />
                <p style={{ marginTop: 8, fontFamily: "var(--font-mono)", fontSize: 12 }}>
                    Confidence: {session.overall_confidence.toFixed(1)}% · Duration: {session.call_duration_sec}s
                </p>

                <p className={`${styles.statusPill} ${isAcknowledged ? styles.statusPillDone : ""}`}>
                    {STATUS_LABEL[status] ?? status}
                </p>

                <div className={styles.actionRow}>
                    <button
                        className={`${styles.actionButton} ${styles.actionButtonPrimary}`}
                        onClick={onAcknowledge}
                        disabled={busy || isAcknowledged}
                    >
                        {pendingAction === "acknowledge"
                            ? "Acknowledging…"
                            : isAcknowledged
                              ? "Acknowledged"
                              : "Acknowledge"}
                    </button>
                    <button className={styles.actionButton} onClick={onReclassify} disabled={busy}>
                        {pendingAction === "reclassify" ? "Re-running…" : "Re-run Classification"}
                    </button>
                </div>

                {actionError && (
                    <p role="alert" className={styles.actionError}>
                        {actionError}
                    </p>
                )}
            </Card>

            <Card>
                <ExplainableAI signals={session.signal_scores ?? {}} />
            </Card>
        </div>
    );
}
