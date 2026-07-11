import { ReactNode } from "react";
import styles from "@/styles/layout.module.css";

export function PageHeader({ title, subtitle, actions }: { title: string; subtitle?: string; actions?: ReactNode }) {
    return (
        <div className={styles.pageHeader}>
            <div>
                <h1 className={styles.pageTitle}>{title}</h1>
                {subtitle && <p className={styles.pageSubtitle}>{subtitle}</p>}
            </div>
            {actions && <div className={styles.pageActions}>{actions}</div>}
        </div>
    );
}
