"use client";
import { motion } from "framer-motion";
import styles from "@/styles/scam.module.css";
import { SignalScore } from "@/lib/api";

const signalNames: Record<string, string> = {
    call_flow_match: "Call Flow Match",
    number_spoofing: "Number Spoofing",
    script_similarity: "Script Similarity",
    voice_synthetic: "Deepfake Voice",
    urgency_phrases: "Urgency Phrases",
};

const signalIcons: Record<string, string> = {
    call_flow_match: "✔",
    number_spoofing: "✔",
    script_similarity: "✔",
    voice_synthetic: "⚠️",
    urgency_phrases: "✔",
};

export function SignalBar({ signalKey, signal, index }: { signalKey: string; signal: SignalScore; index: number }) {
    return (
        <motion.div
            className={styles.signalRow}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.06, duration: 0.4 }}
        >
            <div className={styles.signalHeader}>
                <span className={styles.signalIcon}>{signal.score >= 0.7 ? signalIcons[signalKey] : "⚠️"}</span>
                <span className={styles.signalName}>{signalNames[signalKey] ?? signalKey}</span>
                <span className={styles.signalScore}>{(signal.score * 100).toFixed(0)}%</span>
            </div>
            <div className={styles.signalBar}>
                <motion.div
                    className={styles.signalFill}
                    initial={{ width: 0 }}
                    animate={{ width: `${signal.score * 100}%` }}
                    transition={{ delay: index * 0.06 + 0.2, duration: 0.8, ease: [0.23, 1, 0.32, 1] }}
                    style={{
                        background:
                            signal.score >= 0.85 ? "var(--color-red)" : signal.score >= 0.6 ? "var(--color-amber)" : "var(--accent-500)",
                    }}
                />
            </div>
            <p className={styles.signalExplanation}>{signal.explanation}</p>
        </motion.div>
    );
}
