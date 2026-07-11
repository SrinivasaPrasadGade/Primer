"use client";
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
    onAcknowledge: () => void;
    onReclassify: () => void;
}) {
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
                <div className={styles.actionRow}>
                    <button className={`${styles.actionButton} ${styles.actionButtonPrimary}`} onClick={onAcknowledge}>
                        Acknowledge
                    </button>
                    <button className={styles.actionButton} onClick={onReclassify}>
                        Re-run Classification
                    </button>
                </div>
            </Card>

            <Card>
                <ExplainableAI signals={session.signal_scores ?? {}} />
            </Card>
        </div>
    );
}
