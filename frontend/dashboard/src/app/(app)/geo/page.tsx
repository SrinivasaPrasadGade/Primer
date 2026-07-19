"use client";
import { useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { CrimeMap } from "@/components/geo/CrimeMap";
import { useApi } from "@/hooks/useApi";
import { useAuth } from "@/hooks/useAuth";
import { api, GeoIncident } from "@/lib/api";
import styles from "@/styles/geo.module.css";

const DEFAULT_BOUNDS = "72.77,18.89,72.99,19.27";

export default function GeoIntelMap() {
    const [bounds, setBounds] = useState(DEFAULT_BOUNDS);
    const [selectedIncident, setSelectedIncident] = useState<GeoIncident | null>(null);
    const [generating, setGenerating] = useState(false);
    const [generateError, setGenerateError] = useState<string | null>(null);
    const { user } = useAuth();

    const { data: heatmap } = useApi(`geo-heatmap-${bounds}`, () => api.getHeatmap(bounds));
    const { data: incidents } = useApi(`geo-incidents-${bounds}`, () => api.getIncidents(bounds));
    const {
        data: predictions,
        isLoading: predictionsLoading,
        mutate: mutatePredictions,
    } = useApi(`geo-predictions-${bounds}`, () => api.getPredictions(bounds));

    // Predictions are only ever read here; nothing else in the app invokes the
    // generator, so the table stays empty until someone runs it for a viewport.
    const canGenerate = user?.role === "lea_officer";

    async function handleGenerate() {
        setGenerating(true);
        setGenerateError(null);
        try {
            await api.generatePredictions(bounds);
            await mutatePredictions();
        } catch (err) {
            setGenerateError(err instanceof Error ? err.message : "Failed to generate predictions");
        } finally {
            setGenerating(false);
        }
    }

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
                        <p className={styles.incidentMeta}>
                            {predictionsLoading ? "Loading…" : `${(predictions ?? []).length} zone(s) in current view`}
                        </p>

                        {!predictionsLoading && (predictions ?? []).length === 0 && (
                            <p className={styles.incidentMeta}>
                                No forecast has been run for this area yet.
                                {!canGenerate && " Ask an LEA officer to run one."}
                            </p>
                        )}

                        {canGenerate && (
                            <button className={styles.generateButton} onClick={handleGenerate} disabled={generating}>
                                {generating ? "Running model…" : "Run forecast for this view"}
                            </button>
                        )}

                        {generateError && (
                            <p role="alert" className={styles.incidentMeta} style={{ color: "var(--color-red)" }}>
                                {generateError}
                            </p>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
}
