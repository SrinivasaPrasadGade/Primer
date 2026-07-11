"use client";
import { useEffect, useRef } from "react";
import Graph from "graphology";
import Sigma from "sigma";
import styles from "@/styles/graph.module.css";
import { GraphData } from "@/lib/api";

const NODE_COLORS: Record<string, string> = {
    phone_number: "#3B82F6",
    bank_account: "#22C55E",
    upi_id: "#F59E0B",
    person: "#F97316",
    device: "#A855F7",
    ip_address: "#06B6D4",
    complaint: "#EF4444",
};

export function GraphCanvas({ data, onNodeClick }: { data: GraphData | undefined; onNodeClick: (id: string) => void }) {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!containerRef.current || !data) return;

        const graph = new Graph();

        data.nodes.forEach((node) => {
            if (graph.hasNode(node.id)) return;
            graph.addNode(node.id, {
                label: node.display_label || node.entity_value || node.id,
                size: Math.max(6, (node.risk_score ?? 10) / 5),
                color: NODE_COLORS[node.entity_type] || "#666",
                x: Math.random() * 100,
                y: Math.random() * 100,
            });
        });

        data.edges.forEach((edge) => {
            if (graph.hasNode(edge.source_id) && graph.hasNode(edge.target_id) && !graph.hasEdge(edge.source_id, edge.target_id)) {
                graph.addEdge(edge.source_id, edge.target_id, {
                    label: edge.relationship,
                    size: Math.max(1, (edge.weight ?? 1) / 100),
                    color: "rgba(255,255,255,0.15)",
                });
            }
        });

        const renderer = new Sigma(graph, containerRef.current, {
            renderEdgeLabels: true,
            defaultNodeColor: "#666",
            defaultEdgeColor: "rgba(255,255,255,0.1)",
        });

        renderer.on("clickNode", ({ node }) => onNodeClick(node));

        return () => renderer.kill();
    }, [data, onNodeClick]);

    return <div ref={containerRef} className={styles.graphCanvas} />;
}
