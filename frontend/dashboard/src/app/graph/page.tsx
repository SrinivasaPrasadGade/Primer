"use client";
import { FormEvent, useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { GraphCanvas } from "@/components/graph/GraphCanvas";
import { EntityPanel } from "@/components/graph/EntityPanel";
import { CopilotBar } from "@/components/graph/CopilotBar";
import { LoadingSkeleton } from "@/components/shared/LoadingSkeleton";
import { useApi } from "@/hooks/useApi";
import { ArrowDownLeft, ArrowUpRight } from "lucide-react";
import { api, GraphSearchResult, MoneyFlowEdge } from "@/lib/api";
import styles from "@/styles/graph.module.css";

function formatAmount(n: number): string {
    return "₹" + Math.round(n).toLocaleString("en-IN");
}

function MoneyFlowPanel({ flow }: { flow: MoneyFlowEdge[] }) {
    if (flow.length === 0) {
        return <p className={styles.flowEmpty}>No money-flow transfers traced from this entity.</p>;
    }
    const outflow = flow.filter((e) => e.direction === "outflow");
    const inflow = flow.filter((e) => e.direction === "inflow");
    const totalOut = outflow.reduce((s, e) => s + e.amount, 0);
    const totalIn = inflow.reduce((s, e) => s + e.amount, 0);

    return (
        <div className={styles.flowPanel}>
            <div className={styles.flowSummary}>
                <div className={styles.flowStat}>
                    <span className={styles.flowOutLabel}>Out</span>
                    <span>{formatAmount(totalOut)}</span>
                </div>
                <div className={styles.flowStat}>
                    <span className={styles.flowInLabel}>In</span>
                    <span>{formatAmount(totalIn)}</span>
                </div>
            </div>
            {flow.map((edge) => {
                const out = edge.direction === "outflow";
                return (
                    <div key={edge.id} className={styles.flowRow}>
                        <span className={out ? styles.flowIconOut : styles.flowIconIn}>
                            {out ? <ArrowUpRight size={14} /> : <ArrowDownLeft size={14} />}
                        </span>
                        <span className={styles.flowPath}>
                            {edge.from_entity} → {edge.to_entity}
                        </span>
                        <span className={styles.flowHop}>hop {edge.hop}</span>
                        <span className={styles.flowAmount}>{formatAmount(edge.amount)}</span>
                    </div>
                );
            })}
        </div>
    );
}

export default function FraudGraphExplorer() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<GraphSearchResult[]>([]);
    const [selected, setSelected] = useState<GraphSearchResult | null>(null);
    const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
    const [moneyFlow, setMoneyFlow] = useState<MoneyFlowEdge[] | null>(null);
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
            setMoneyFlow(flow);
        } catch {
            setMoneyFlow([]);
        }
    }

    const selectedNode = graphData?.nodes.find((n) => n.id === selectedNodeId) ?? null;

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
                        <GraphCanvas data={graphData} onNodeClick={setSelectedNodeId} />
                    )}

                    <CopilotBar context={selectedNode?.entity_value ?? selectedNode?.display_label ?? null} />
                </div>

                <div>
                    <EntityPanel node={selectedNode} onViewMoneyFlow={handleViewMoneyFlow} />
                    {moneyFlow && (
                        <MoneyFlowPanel flow={moneyFlow} />
                    )}
                </div>
            </div>
        </>
    );
}
