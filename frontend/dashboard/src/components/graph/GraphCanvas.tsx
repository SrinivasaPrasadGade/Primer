"use client";
import { useEffect, useRef } from "react";
import Graph from "graphology";
import Sigma from "sigma";
import styles from "@/styles/graph.module.css";
import { GraphData } from "@/lib/api";

// Node colours by entity type (doc §5.3). ip_address is added because the
// backend fraud-graph exposes that entity type; the doc's list omitted it.
const NODE_COLORS: Record<string, string> = {
    phone_number: "#3B82F6",
    bank_account: "#22C55E",
    upi_id: "#F59E0B",
    person: "#F97316",
    device: "#A855F7",
    ip_address: "#06B6D4",
    complaint: "#EF4444",
};

// Doc §5.3 types `data` as `any`; we use the real GraphData shape from lib/api.
export function GraphCanvas({ data, onNodeClick }: { data: GraphData | undefined; onNodeClick: (id: string) => void }) {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!containerRef.current || !data) return;

        const graph = new Graph();

        // Seed positions on a circle instead of pure random — random placement produces
        // the tangled "hairball" look; a circular seed gives ForceAtlas/Sigma a clean
        // starting point and reads far better for a small entity network.
        const uniqueNodes = data.nodes.filter((n, i, arr) => arr.findIndex((m) => m.id === n.id) === i);
        const count = uniqueNodes.length || 1;
        uniqueNodes.forEach((node, i) => {
            const angle = (2 * Math.PI * i) / count;
            graph.addNode(node.id, {
                label: node.display_label || node.entity_value || node.id,
                size: Math.max(8, Math.min(24, (node.risk_score || 10) / 4)),
                color: NODE_COLORS[node.entity_type] || "#666",
                x: Math.cos(angle) * 10,
                y: Math.sin(angle) * 10,
            });
        });

        // Add edges (guard against missing endpoints and parallel edges)
        data.edges.forEach((edge) => {
            if (graph.hasNode(edge.source_id) && graph.hasNode(edge.target_id) && !graph.hasEdge(edge.source_id, edge.target_id)) {
                graph.addEdge(edge.source_id, edge.target_id, {
                    label: edge.relationship,
                    size: Math.max(1, (edge.weight || 1) / 100),
                    color: "rgba(255,255,255,0.15)",
                });
            }
        });

        // Render with Sigma
        const renderer = new Sigma(graph, containerRef.current, {
            renderEdgeLabels: true,
            defaultNodeColor: "#666",
            defaultEdgeColor: "rgba(255,255,255,0.1)",
            labelColor: { color: "#F5F5F7" },
            labelSize: 12,
            minCameraRatio: 0.2,
            maxCameraRatio: 4,
        });

        renderer.on("clickNode", ({ node }) => onNodeClick(node));

        // Keep the canvas correctly sized/centred when its container resizes (window
        // resize, sidebar collapse, orientation change) — Sigma needs an explicit
        // refresh + camera reset, otherwise it renders at the stale initial size.
        const observer = new ResizeObserver(() => {
            renderer.refresh();
            renderer.getCamera().animatedReset();
        });
        observer.observe(containerRef.current);

        return () => {
            observer.disconnect();
            renderer.kill();
        };
    }, [data, onNodeClick]);

    return (
        <div className={styles.graphCanvasWrap}>
            <div ref={containerRef} className={styles.graphCanvas} />
            {(!data || data.nodes.length === 0) && (
                <div className={styles.graphEmpty}>Search an entity to explore its network.</div>
            )}
        </div>
    );
}
