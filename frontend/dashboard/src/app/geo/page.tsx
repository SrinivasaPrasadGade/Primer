"use client";
import { useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { CrimeMap } from "@/components/geo/CrimeMap";
import { useApi } from "@/hooks/useApi";
import { api, GeoIncident } from "@/lib/api";
import styles from "@/styles/geo.module.css";

const DEFAULT_BOUNDS = "72.77,18.89,72.99,19.27";

export default function GeoIntelMap() {
    const [bounds, setBounds] = useState(DEFAULT_BOUNDS);
    const [selectedIncident, setSelectedIncident] = useState<GeoIncident | null>(null);

    const { data: heatmap } = useApi(`geo-heatmap-${bounds}`, () => api.getHeatmap(bounds));
    const { data: incidents } = useApi(`geo-incidents-${bounds}`, () => api.getIncidents(bounds));
    const { data: predictions } = useApi(`geo-predictions-${bounds}`, () => api.getPredictions(bounds));

    return (
        <>
            <PageHeader title="Geo Intel — Crime Map" subtitle="Live crime heatmap with hotspot predictions" />

            <div className={styles.layout}>
                <CrimeMap
                    heatmap={heatmap ?? []}
                    incidents={incidents ?? []}
                    predictions={predictions ?? []}
                    onBoundsChange={setBounds}
                    onIncidentClick={setSelectedIncident}
                />

                <div className={styles.sidebar}>
                    {selectedIncident ? (
                        <div className={styles.incidentCard}>
                            <p className={styles.incidentTitle}>{selectedIncident.title}</p>
                            <p className={styles.incidentMeta}>{selectedIncident.crime_type}</p>
                            <p className={styles.incidentMeta}>Severity: {selectedIncident.severity}</p>
                            <p className={styles.incidentMeta}>Est. loss: ₹{selectedIncident.estimated_loss}</p>
                            <p className={styles.incidentMeta}>{selectedIncident.description}</p>
                        </div>
                    ) : (
                        <div className={styles.incidentCard}>
                            <p className={styles.incidentMeta}>Click a red pin on the map to see incident details.</p>
                        </div>
                    )}
                    <div className={styles.incidentCard}>
                        <p className={styles.incidentTitle}>Predicted Hotspots</p>
                        <p className={styles.incidentMeta}>{(predictions ?? []).length} zone(s) in current view</p>
                    </div>
                </div>
            </div>
        </>
    );
}
