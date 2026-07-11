"use client";
import { motion } from "framer-motion";
import { Badge } from "../shared/Badge";
import { ConfidenceBar } from "../shared/ConfidenceBar";
import styles from "@/styles/scam.module.css";
import { ScamSession } from "@/lib/api";

function formatDuration(seconds: number) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
}

export function SessionCard({ session, onClick }: { session: ScamSession; onClick: () => void }) {
    const isRed = session.alert_level === "RED";
    return (
        <motion.div
            className={`${styles.sessionCard} ${styles[session.alert_level.toLowerCase()]}`}
            onClick={onClick}
            initial={{ opacity: 0, y: -20 }}
            animate={isRed ? { opacity: 1, y: 0, boxShadow: ["0 0 0 rgba(239,68,68,0)", "0 0 24px rgba(239,68,68,0.35)", "0 0 0 rgba(239,68,68,0)"] } : { opacity: 1, y: 0 }}
            transition={isRed ? { duration: 2, repeat: Infinity, ease: "easeInOut" } : { duration: 0.4, ease: [0.23, 1.0, 0.32, 1.0] }}
            whileHover={{ y: -2 }}
        >
            <div className={styles.cardHeader}>
                <Badge level={session.alert_level} />
                <span className={styles.scamType}>{session.scam_type}</span>
                {session.deepfake_detected && <Badge level="AMBER" label="AI Voice" />}
            </div>
            <div className={styles.cardBody}>
                <div className={styles.phoneRow}>
                    <span className={styles.phone}>{session.caller_number}</span>
                    <span className={styles.arrow}>→</span>
                    <span className={styles.phone}>{session.callee_number}</span>
                </div>
                <ConfidenceBar value={session.overall_confidence} />
            </div>
            <div className={styles.cardFooter}>
                <span className={styles.duration}>{formatDuration(session.call_duration_sec)}</span>
                <span className={styles.confidence}>{session.overall_confidence.toFixed(1)}%</span>
            </div>
        </motion.div>
    );
}
