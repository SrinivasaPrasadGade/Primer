import { GraphNode } from "@/lib/api";
import styles from "@/styles/graph.module.css";

export function EntityPanel({ node, onViewMoneyFlow }: { node: GraphNode | null; onViewMoneyFlow: (id: string) => void }) {
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
        </div>
    );
}
