"use client";
import { useEffect, useMemo, useRef } from "react";
import Graph from "graphology";
import Sigma from "sigma";
import { focusEdge, focusNode } from "./graphFocus";
import circular from "graphology-layout/circular";
import forceAtlas2 from "graphology-layout-forceatlas2";
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

const EDGE_MIN_WIDTH = 1;
const EDGE_MAX_WIDTH = 6;


/**
 * Edge `weight` is a rupee amount, so it can't be used as a pixel width
 * directly. Map the observed range onto EDGE_MIN..EDGE_MAX instead; amounts in
 * a cluster are heavily skewed, so rank on log scale.
 */
function edgeWidthScale(weights: number[]) {
    const logs = weights.map((w) => Math.log10(Math.max(1, w)));
    const lo = Math.min(...logs);
    const hi = Math.max(...logs);
    return (weight: number) => {
        if (!Number.isFinite(lo) || hi === lo) return EDGE_MIN_WIDTH + 1;
        const raw = (Math.log10(Math.max(1, weight)) - lo) / (hi - lo);
        const t = Math.min(1, Math.max(0, raw)); // a weight outside the sampled range must not invert the width
        return EDGE_MIN_WIDTH + t * (EDGE_MAX_WIDTH - EDGE_MIN_WIDTH);
    };
}

function buildGraph(data: GraphData) {
    const graph = new Graph();

    // Add nodes (guard against duplicate ids — graphology throws otherwise)
    data.nodes.forEach((node) => {
        if (graph.hasNode(node.id)) return;
        graph.addNode(node.id, {
            label: node.display_label || node.entity_value || node.id,
            size: Math.max(8, (node.risk_score || 10) / 5),
            color: NODE_COLORS[node.entity_type] || "#666",
        });
    });

    const widthOf = edgeWidthScale(data.edges.map((e) => e.weight || 1));

    // Add edges (guard against missing endpoints and parallel edges)
    data.edges.forEach((edge) => {
        if (graph.hasNode(edge.source_id) && graph.hasNode(edge.target_id) && !graph.hasEdge(edge.source_id, edge.target_id)) {
            graph.addEdge(edge.source_id, edge.target_id, {
                label: edge.relationship,
                size: widthOf(edge.weight || 1),
                color: "rgba(255,255,255,0.15)",
            });
        }
    });

    // ForceAtlas2 needs distinct starting coordinates; seed on a circle, then
    // let the layout pull connected entities into clusters.
    if (graph.order > 0) {
        circular.assign(graph);
        if (graph.order > 1) {
            forceAtlas2.assign(graph, {
                iterations: 200,
                settings: { ...forceAtlas2.inferSettings(graph), barnesHutOptimize: graph.order > 200 },
            });
        }
    }

    return graph;
}


// Doc §5.3 types `data` as `any`; we use the real GraphData shape from lib/api.
export function GraphCanvas({
    data,
    onNodeClick,
    selectedNodeId = null,
}: {
    data: GraphData | undefined;
    onNodeClick: (id: string) => void;
    selectedNodeId?: string | null;
}) {
    const containerRef = useRef<HTMLDivElement>(null);
    const rendererRef = useRef<Sigma | null>(null);

    // Read by the reducers on every repaint. Held in a ref rather than a
    // dependency so changing the selection repaints the existing renderer
    // instead of rebuilding the graph and re-running ForceAtlas2 — which would
    // throw away the layout and make the canvas jump on every click.
    const selectedRef = useRef<string | null>(selectedNodeId);

    // SWR hands back a fresh object on every revalidation. Rebuilding (and
    // re-running the layout) on identity alone makes the graph jump for no
    // reason, so key the work on the actual node/edge content.
    const signature = useMemo(() => {
        if (!data) return null;
        return JSON.stringify({
            n: data.nodes.map((x) => [x.id, x.risk_score, x.entity_type]),
            e: data.edges.map((x) => [x.source_id, x.target_id, x.relationship, x.weight]),
        });
    }, [data]);

    // Keep the latest handler reachable without making it an effect dependency.
    const onNodeClickRef = useRef(onNodeClick);
    useEffect(() => {
        onNodeClickRef.current = onNodeClick;
    }, [onNodeClick]);

    const dataRef = useRef(data);
    dataRef.current = data;

    useEffect(() => {
        const container = containerRef.current;
        const current = dataRef.current;
        if (!container || !current || signature === null) return;

        const graph = buildGraph(current);

        const renderer = new Sigma(graph, container, {
            renderEdgeLabels: true,
            defaultNodeColor: "#666",
            defaultEdgeColor: "rgba(255,255,255,0.1)",
            // Sigma throws if the container measures 0 at construction, which
            // happens while the flex parent is still settling. The observer
            // below corrects the size as soon as it is real.
            allowInvalidContainer: true,

            nodeReducer: (node, attrs) => focusNode(graph, selectedRef.current, node, attrs),
            edgeReducer: (edge, attrs) => focusEdge(graph, selectedRef.current, edge, attrs),
        });

        rendererRef.current = renderer;

        renderer.on("clickNode", ({ node }) => onNodeClickRef.current(node));
        // Clicking empty canvas clears the selection, which is the only way back
        // to the unfocused view once a node has been picked.
        renderer.on("clickStage", () => onNodeClickRef.current(""));

        // Sigma sizes itself from the container at construction. The container
        // is a flex child of a vh-based parent, so it changes size well after
        // mount — without this the canvas keeps its first measurement.
        // resize() re-measures but does not repaint, hence scheduleRender().
        const observer = new ResizeObserver(() => {
            renderer.resize();
            renderer.scheduleRender();
        });
        observer.observe(container);

        return () => {
            observer.disconnect();
            renderer.kill();
            rendererRef.current = null;
        };
    }, [signature]);

    // Repaint through the reducers when the selection changes. refresh() re-runs
    // them against the existing layout, so nothing moves.
    useEffect(() => {
        selectedRef.current = selectedNodeId;
        rendererRef.current?.refresh({ skipIndexation: true });
    }, [selectedNodeId, signature]);

    return <div ref={containerRef} className={styles.graphCanvas} />;
}
