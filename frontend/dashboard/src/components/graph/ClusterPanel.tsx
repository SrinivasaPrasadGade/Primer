"use client";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { api, ClusterDetail, ClusterEntity, DetectedCommunity } from "@/lib/api";
import styles from "@/styles/graph.module.css";

export function ClusterPanel({ onFocusEntity }: { onFocusEntity: (entity: ClusterEntity, clusterId: string) => void }) {
    const { user } = useAuth();
    const [communities, setCommunities] = useState<DetectedCommunity[] | null>(null);
    const [detail, setDetail] = useState<ClusterDetail | null>(null);
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Detection rewrites cluster assignments, so the backend restricts it to
    // lea_officer. Hiding it beats showing a button that always 403s.
    const canDetect = user?.role === "lea_officer";

    async function handleDetect() {
        setBusy(true);
        setError(null);
        setDetail(null);
        try {
            setCommunities(await api.detectCommunities());
        } catch (err) {
            setError(err instanceof Error ? err.message : "Community detection failed.");
        } finally {
            setBusy(false);
        }
    }

    async function handleInspect(clusterId: string) {
        setError(null);
        try {
            setDetail(await api.getCluster(clusterId));
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not load that cluster.");
        }
    }

    if (!canDetect) return null;

    return (
        <div className={styles.flowPanel}>
            <h4 className={styles.panelValue}>Communities</h4>
            <p className={styles.panelEmpty}>Group the graph into connected fraud clusters.</p>
            <button className={styles.panelButton} onClick={handleDetect} disabled={busy}>
                {busy ? "Detecting…" : "Detect Communities"}
            </button>

            {error && <p className={styles.panelEmpty}>{error}</p>}

            {communities?.length === 0 && <p className={styles.panelEmpty}>No clusters met the minimum size.</p>}

            {communities && communities.length > 0 && !detail && (
                <div className={styles.clusterList}>
                    {communities.map((c) => (
                        <button key={c.cluster_id} className={styles.clusterRow} onClick={() => handleInspect(c.cluster_id)}>
                            <span>{c.node_count} entities</span>
                            <span className={styles.clusterMeta}>{c.edge_count} links</span>
                        </button>
                    ))}
                </div>
            )}

            {detail && (
                <div className={styles.clusterList}>
                    <button className={styles.panelButton} onClick={() => setDetail(null)}>
                        ← Back to clusters
                    </button>
                    <p className={styles.panelRisk}>
                        <strong>{detail.cluster.name ?? "Cluster"}</strong> · {detail.cluster.status}
                    </p>
                    <p className={styles.clusterMeta}>
                        {detail.cluster.node_count} entities · {detail.cluster.edge_count} links · {detail.cluster.victim_count} victims
                    </p>
                    {detail.entities.map((e) => (
                        <button
                            key={e.id}
                            className={styles.clusterRow}
                            onClick={() => onFocusEntity(e, detail.cluster.id)}
                        >
                            <span>{e.display_label || e.entity_value}</span>
                            <span className={styles.clusterMeta}>{e.risk_score ?? "—"}</span>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
