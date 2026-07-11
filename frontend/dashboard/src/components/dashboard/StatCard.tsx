import { ReactNode } from "react";
import styles from "@/styles/dashboard.module.css";

export function StatCard({ label, value, icon, tone = "default" }: { label: string; value: ReactNode; icon?: ReactNode; tone?: "default" | "red" | "amber" | "green" }) {
    return (
        <div className={`${styles.statCard} ${styles[`tone-${tone}`]}`}>
            <div className={styles.statHeader}>
                <span className={styles.statLabel}>{label}</span>
                {icon}
            </div>
            <span className={styles.statValue}>{value}</span>
        </div>
    );
}
