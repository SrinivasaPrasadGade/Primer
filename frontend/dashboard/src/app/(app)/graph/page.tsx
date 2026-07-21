"use client";
import { FormEvent, useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { GraphCanvas } from "@/components/graph/GraphCanvas";
import { EntityPanel } from "@/components/graph/EntityPanel";
import { ClusterPanel } from "@/components/graph/ClusterPanel";
import { MoneyFlowPanel } from "@/components/graph/MoneyFlowPanel";
import { CopilotBar } from "@/components/graph/CopilotBar";
import { LoadingSkeleton } from "@/components/shared/LoadingSkeleton";
import { useApi } from "@/hooks/useApi";
import { api, ClusterEntity, GraphSearchResult, MoneyFlowEdge } from "@/lib/api";
import styles from "@/styles/graph.module.css";

export default function FraudGraphExplorer() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<GraphSearchResult[]>([]);
    const [selected, setSelected] = useState<GraphSearchResult | null>(null);
    const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
    const [moneyFlow, setMoneyFlow] = useState<{ nodeId: string; edges: MoneyFlowEdge[] } | null>(null);
    const [searchError, setSearchError] = useState<string | null>(null);

    const { data: graphData, error: graphError, isLoading } = useApi(
        selected ? `graph-entity-${selected.entity_type}-${selected.entity_value}` : null,
        () => api.getEntity(selected!.entity_type, selected!.entity_value)
    );

    async function handleSearch(e: FormEvent) {
        e.preventDefault();
        if (!query.trim()) return;
        setSearchError(null);
        try {
            const found = await api.searchGraph(query);
            setResults(found);
            if (found.length === 0) setSearchError("No matching entities found.");
        } catch (err) {
            setSearchError(err instanceof Error ? err.message : "Search failed");
        }
    }

    async function handleViewMoneyFlow(nodeId: string) {
        try {
            const flow = await api.getMoneyFlow(nodeId);
            setMoneyFlow({ nodeId, edges: flow });
        } catch {
            setMoneyFlow({ nodeId, edges: [] });
        }
    }

    // Focusing an entity from a cluster carries its cluster_id across, so the
    // dossier action stays available on the entity panel.
    function handleFocusClusterEntity(entity: ClusterEntity, clusterId: string) {
        setSelected({
            id: entity.id,
            entity_type: entity.entity_type,
            entity_value: entity.entity_value,
            display_label: entity.display_label,
            risk_score: entity.risk_score,
            cluster_id: clusterId,
        });
        setResults([]);
        setSelectedNodeId(null);
        setMoneyFlow(null);
    }

    function handleNodeClick(nodeId: string) {
        // GraphCanvas sends "" when the officer clicks empty canvas to deselect.
        setSelectedNodeId(nodeId || null);
        setMoneyFlow(null);
    }

    const selectedNode = graphData?.nodes.find((n) => n.id === selectedNodeId) ?? null;
    const phoneNumberNodes = graphData?.nodes.filter((n) => n.entity_type === "phone_number") ?? [];

    return (
        <>
            <PageHeader title="Fraud Graph Explorer" subtitle="Interactive entity network across phones, accounts, and devices" />

            <div className={styles.layout}>
                <div className={styles.canvasWrap}>
                    <form className={styles.searchBar} onSubmit={handleSearch}>
                        <input
                            className={styles.searchInput}
                            placeholder="Search phone number, UPI ID, bank account…"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <button className={styles.searchButton} type="submit">
                            Search
                        </button>
                    </form>

                    {/* Phone numbers are the majority of nodes in a cluster and make the
                        canvas unreadable if every one prints its own label — pick one here
                        instead; the canvas only shows the label for whichever is selected. */}
                    {phoneNumberNodes.length > 0 && (
                        <select
                            className={styles.numberSelect}
                            value={selectedNodeId ?? ""}
                            onChange={(e) => handleNodeClick(e.target.value)}
                        >
                            <option value="">Select a phone number…</option>
                            {phoneNumberNodes.map((n) => (
                                <option key={n.id} value={n.id}>
                                    {n.display_label || n.entity_value}
                                </option>
                            ))}
                        </select>
                    )}

                    {searchError && <p style={{ color: "var(--color-text-tertiary)", fontSize: 12 }}>{searchError}</p>}

                    {results.length > 0 && !selected && (
                        <div className={styles.searchResults}>
                            {results.map((r) => (
                                <button
                                    key={r.id}
                                    className={styles.searchResultRow}
                                    onClick={() => {
                                        setSelected(r);
                                        setResults([]);
                                    }}
                                >
                                    <span>{r.display_label || r.entity_value}</span>
                                    <span>{r.entity_type}</span>
                                </button>
                            ))}
                        </div>
                    )}

                    {isLoading ? (
                        <LoadingSkeleton height={420} />
                    ) : graphError ? (
                        <div className={styles.graphCanvas} style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                            <p style={{ color: "var(--color-text-tertiary)", fontSize: 13 }}>
                                {graphError instanceof Error ? graphError.message : "Entity not found."}
                            </p>
                        </div>
                    ) : (
                        <GraphCanvas data={graphData} onNodeClick={handleNodeClick} selectedNodeId={selectedNodeId} />
                    )}

                    <CopilotBar />
                </div>

                <div>
                    <EntityPanel node={selectedNode} clusterId={selected?.cluster_id ?? null} onViewMoneyFlow={handleViewMoneyFlow} />
                    {moneyFlow && <MoneyFlowPanel edges={moneyFlow.edges} nodeId={moneyFlow.nodeId} />}
                    <ClusterPanel onFocusEntity={handleFocusClusterEntity} />
                </div>
            </div>
        </>
    );
}
