"use client";
import styles from "@/styles/scam.module.css";
import { SignalScore } from "@/lib/api";
import { SignalBar } from "./SignalBar";

export function ExplainableAI({ signals }: { signals: Record<string, SignalScore> }) {
    return (
        <div className={styles.explainableAI}>
            <h3 className={styles.sectionTitle}>Explainable AI — Why This Was Flagged</h3>
            {Object.entries(signals).map(([key, signal], index) => (
                <SignalBar key={key} signalKey={key} signal={signal} index={index} />
            ))}
        </div>
    );
}
