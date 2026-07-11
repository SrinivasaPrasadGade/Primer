import styles from "./shared.module.css";

export function ConfidenceBar({ value }: { value: number }) {
    const color = value >= 85 ? "var(--color-red)" : value >= 60 ? "var(--color-amber)" : "var(--accent-500)";
    return (
        <div className={styles.confidenceBar}>
            <div className={styles.confidenceFill} style={{ width: `${Math.min(100, Math.max(0, value))}%`, background: color }} />
        </div>
    );
}
