"use client";
import Link from "next/link";
import { CrimeMap } from "@/components/geo/CrimeMap";
import { useApi } from "@/hooks/useApi";
import { api } from "@/lib/api";
import styles from "@/styles/dashboard.module.css";

const DEFAULT_BOUNDS = "72.77,18.89,72.99,19.27";

const noop = () => {};

export function MiniMap() {
    const { data: heatmap } = useApi("mini-heatmap", () => api.getHeatmap(DEFAULT_BOUNDS));
    const { data: incidents } = useApi("mini-incidents", () => api.getIncidents(DEFAULT_BOUNDS));

    return (
        <div className={styles.miniMap}>
            <div className={styles.miniMapHeader}>
                <span className={styles.sectionTitle}>Crime Map</span>
                <Link href="/geo" className={styles.miniMapLink}>
                    View full map →
                </Link>
            </div>
            <CrimeMap
                heatmap={heatmap ?? []}
                incidents={incidents ?? []}
                predictions={[]}
                onBoundsChange={noop}
                onIncidentClick={noop}
                interactive={false}
                zoom={10}
                style={{ minHeight: 200, height: 200 }}
            />
        </div>
    );
}
