"use client";
import { useState } from "react";
import { Badge } from "@/components/shared/Badge";
import { Card } from "@/components/shared/Card";
import { ConfidenceBar } from "@/components/shared/ConfidenceBar";
import { ExplainableAI } from "./ExplainableAI";
import { ScamSessionDetail } from "@/lib/api";
import styles from "@/styles/scam.module.css";

export function SessionDetail({
    session,
    onAcknowledge,
    onReclassify,
}: {
    session: ScamSessionDetail;
    onAcknowledge: () => Promise<void>;
    onReclassify: () => Promise<void>;
}) {
    const [ackBusy, setAckBusy] = useState(false);
    const [reBusy, setReBusy] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const acknowledged = session.status === "acknowledged";

    async function run(fn: () => Promise<void>, setBusy: (v: boolean) => void) {
        setError(null);
        setBusy(true);
        try {
            await fn();
        } catch (err) {
            setError(err instanceof Error ? err.message : "Action failed");
        } finally {
            setBusy(false);
        }
    }

    return (
        <div className={styles.detailGrid}>
            <Card>
                <div className={styles.detailHeader}>
                    <Badge level={session.alert_level} />
                    <span>{session.scam_type}</span>
                    {session.deepfake_detected && <Badge level="AMBER" label="AI Voice" />}
                    {session.status && (
                        <span className={styles.statusPill} data-status={session.status}>
                            {session.status}
                        </span>
                    )}
                </div>
                <ConfidenceBar value={session.overall_confidence} />
                <p style={{ marginTop: 8, fontFamily: "var(--font-mono)", fontSize: 12 }}>
                    Confidence: {session.overall_confidence.toFixed(1)}% · Duration: {session.call_duration_sec}s
                </p>
                <div className={styles.actionRow}>
                    <button
                        className={`${styles.actionButton} ${styles.actionButtonPrimary}`}
                        onClick={() => run(onAcknowledge, setAckBusy)}
                        disabled={ackBusy || acknowledged}
                    >
                        {acknowledged ? "✓ Acknowledged" : ackBusy ? "Acknowledging…" : "Acknowledge"}
                    </button>
                    <button
                        className={styles.actionButton}
                        onClick={() => run(onReclassify, setReBusy)}
                        disabled={reBusy}
                    >
                        {reBusy ? "Re-running…" : "Re-run Classification"}
                    </button>
                </div>
                {error && <p className={styles.actionError}>{error}</p>}
            </Card>

            <Card>
                <ExplainableAI signals={session.signal_scores ?? {}} />
            </Card>
        </div>
    );
}
