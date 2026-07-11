"use client";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { Badge } from "../shared/Badge";
import styles from "@/styles/dashboard.module.css";
import { ScamSession } from "@/lib/api";

export function LiveAlertFeed({ sessions }: { sessions: ScamSession[] }) {
    return (
        <div className={styles.alertFeed}>
            <span className={styles.sectionTitle}>Live Alert Feed</span>
            <div className={styles.alertList}>
                <AnimatePresence initial={false}>
                    {sessions.slice(0, 8).map((session) => (
                        <motion.div
                            key={session.id}
                            initial={{ opacity: 0, y: -12 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.3 }}
                        >
                            <Link href={`/scam/${session.id}`} className={styles.alertRow}>
                                <Badge level={session.alert_level} />
                                <span className={styles.alertPhone}>{session.caller_number}</span>
                                <span className={styles.alertType}>{session.scam_type}</span>
                                <span className={styles.alertConfidence}>{session.overall_confidence.toFixed(1)}%</span>
                            </Link>
                        </motion.div>
                    ))}
                </AnimatePresence>
                {sessions.length === 0 && <p className={styles.emptyState}>No active sessions yet.</p>}
            </div>
        </div>
    );
}
