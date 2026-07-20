"use client";
import { useState } from "react";
import { api, GraphNode } from "@/lib/api";
import styles from "@/styles/graph.module.css";

export function EntityPanel({
    node,
    clusterId,
    onViewMoneyFlow,
}: {
    node: GraphNode | null;
    clusterId: string | null;
    onViewMoneyFlow: (id: string) => void;
}) {
    const [busy, setBusy] = useState(false);
    const [dossierError, setDossierError] = useState<string | null>(null);

    async function handleGenerateDossier() {
        if (!clusterId) return;
        setBusy(true);
        setDossierError(null);
        try {
            // Generate first, then pull the PDF back down — the generate endpoint
            // returns a server-side path the browser can't reach on its own.
            await api.generateDossier(clusterId);
            const blob = await api.downloadDossier(clusterId);

            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = `dossier_${clusterId}.pdf`;
            link.click();
            URL.revokeObjectURL(url);
        } catch (err) {
            setDossierError(err instanceof Error ? err.message : "Could not generate the dossier.");
        } finally {
            setBusy(false);
        }
    }

    if (!node) {
        return <p className={styles.panelEmpty}>Click a node to inspect it.</p>;
    }

    return (
        <div className={styles.panel}>
            <span className={styles.panelType}>{node.entity_type.replace(/_/g, " ")}</span>
            <h3 className={styles.panelValue}>{node.display_label || node.entity_value}</h3>
            {node.risk_score !== undefined && (
                <p className={styles.panelRisk}>
                    Risk score: <strong>{node.risk_score}</strong>
                </p>
            )}
            <button className={styles.panelButton} onClick={() => onViewMoneyFlow(node.id)}>
                Trace Money Flow
            </button>

            {/* Dossiers are generated per cluster, so an entity outside one has nothing to export. */}
            <button
                className={styles.panelButton}
                onClick={handleGenerateDossier}
                disabled={!clusterId || busy}
                title={clusterId ? undefined : "This entity is not part of a detected cluster"}
            >
                {busy ? "Generating…" : "Generate Dossier"}
            </button>
            {!clusterId && <p className={styles.panelEmpty}>No cluster linked to this entity.</p>}
            {dossierError && <p className={styles.panelEmpty}>{dossierError}</p>}
        </div>
    );
}
