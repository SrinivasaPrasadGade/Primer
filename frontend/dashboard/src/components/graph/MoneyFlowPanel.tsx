import { MoneyFlowEdge } from "@/lib/api";
import styles from "@/styles/graph.module.css";

const inr = new Intl.NumberFormat("en-IN", { maximumFractionDigits: 0 });

function roleOf(edges: MoneyFlowEdge[], nodeId: string) {
    const sends = edges.some((e) => e.source_id === nodeId);
    const receives = edges.some((e) => e.target_id === nodeId);
    if (sends && receives) return "Intermediary";
    if (sends) return "Sender";
    if (receives) return "Receiver";
    return "Not on a transfer";
}

export function MoneyFlowPanel({ edges, nodeId }: { edges: MoneyFlowEdge[]; nodeId: string }) {
    if (edges.length === 0) {
        return <p className={styles.panelEmpty}>No transfers recorded in this cluster.</p>;
    }

    const total = edges.reduce((sum, e) => sum + (e.amount ?? 0), 0);

    return (
        <div className={styles.flowPanel}>
            <div className={styles.flowHeader}>
                <span className={styles.panelType}>Cluster money flow</span>
                <span className={styles.flowRole}>{roleOf(edges, nodeId)}</span>
            </div>
            <p className={styles.flowSummary}>
                {edges.length} transfer{edges.length === 1 ? "" : "s"} · ₹{inr.format(total)} total
            </p>

            <ol className={styles.flowList}>
                {edges.map((edge) => {
                    const out = edge.source_id === nodeId;
                    const incoming = edge.target_id === nodeId;
                    return (
                        <li
                            key={edge.id}
                            className={`${styles.flowRow} ${out || incoming ? styles.flowRowActive : ""}`}
                        >
                            <span className={styles.flowEntities}>
                                <span className={out ? styles.flowSelf : undefined}>{edge.from_entity}</span>
                                {" → "}
                                <span className={incoming ? styles.flowSelf : undefined}>{edge.to_entity}</span>
                            </span>
                            <span className={styles.flowAmount}>₹{inr.format(edge.amount ?? 0)}</span>
                        </li>
                    );
                })}
            </ol>
        </div>
    );
}
