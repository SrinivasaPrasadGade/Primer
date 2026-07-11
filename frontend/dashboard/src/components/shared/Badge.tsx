import styles from "./shared.module.css";

type Level = "RED" | "AMBER" | "YELLOW" | "GREEN";

export function Badge({ level, label }: { level: Level; label?: string }) {
    return <span className={`${styles.badge} ${styles[level.toLowerCase()]}`}>{label ?? level}</span>;
}
