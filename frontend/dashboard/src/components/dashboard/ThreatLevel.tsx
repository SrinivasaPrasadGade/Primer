import styles from "@/styles/dashboard.module.css";

export function ThreatLevel({ redCount, amberCount, yellowCount }: { redCount: number; amberCount: number; yellowCount: number }) {
    const total = Math.max(1, redCount + amberCount + yellowCount);
    const level = redCount > 5 ? "Critical" : redCount > 0 ? "Elevated" : amberCount > 0 ? "Guarded" : "Normal";
    const levelTone = redCount > 5 ? "red" : redCount > 0 ? "amber" : amberCount > 0 ? "amber" : "green";

    return (
        <div className={styles.threatLevel}>
            <div className={styles.threatHeader}>
                <span className={styles.sectionTitle}>Threat Level</span>
                <span className={`${styles.threatBadge} ${styles[`badge-${levelTone}`]}`}>{level}</span>
            </div>
            <div className={styles.threatBar}>
                <div className={styles.threatSegmentRed} style={{ width: `${(redCount / total) * 100}%` }} />
                <div className={styles.threatSegmentAmber} style={{ width: `${(amberCount / total) * 100}%` }} />
                <div className={styles.threatSegmentYellow} style={{ width: `${(yellowCount / total) * 100}%` }} />
            </div>
            <div className={styles.threatLegend}>
                <span>{redCount} Red</span>
                <span>{amberCount} Amber</span>
                <span>{yellowCount} Yellow</span>
            </div>
        </div>
    );
}
