/**
 * Selection styling for the fraud-graph canvas.
 *
 * Kept out of GraphCanvas.tsx so this logic is reachable without importing
 * React, CSS modules or sigma — sigma needs WebGL, so anything that imports it
 * cannot run under a headless test.
 */
import type Graph from "graphology";
import type { Attributes } from "graphology-types";
import type { EdgeDisplayData, NodeDisplayData } from "sigma/types";

/** Applied to everything outside the selected node's immediate neighbourhood. */
export const DIMMED_NODE = "#333A47";
export const DIMMED_EDGE = "rgba(255,255,255,0.04)";
export const ACTIVE_EDGE = "rgba(96,165,250,0.6)";

/**
 * Selection styling for one node.
 *
 * Draws focus by dimming everything outside the selected node's immediate
 * neighbourhood rather than by recolouring the selection itself: entity-type
 * colour is the graph's primary encoding, so overriding it on the focused node
 * would cost more information than the highlight adds.
 */
// Phone numbers are the densest, most repetitive label on the canvas — with
// a full cluster on screen they stack into unreadable text. They're picked
// from the dropdown instead, so the canvas only prints one once it's
// selected (or a neighbour of the selection).
const LABEL_HIDDEN_BY_DEFAULT = new Set(["phone_number"]);

export function focusNode(
    graph: Graph,
    selected: string | null,
    node: string,
    attrs: Attributes,
): Partial<NodeDisplayData> {
    const hideByDefault = LABEL_HIDDEN_BY_DEFAULT.has(attrs.entityType as string);
    // A selection naming a node that isn't in this graph (a stale id left over
    // from the previously inspected entity) must fall back to the unfocused
    // view rather than dimming every node at once.
    if (!selected || !graph.hasNode(selected)) {
        return hideByDefault ? { ...attrs, label: null } : attrs;
    }
    if (node === selected) {
        return { ...attrs, size: (attrs.size ?? 1) * 1.45, highlighted: true, forceLabel: true, zIndex: 2 };
    }
    if (graph.areNeighbors(selected, node)) {
        return { ...attrs, forceLabel: true, zIndex: 1 };
    }
    return { ...attrs, color: DIMMED_NODE, label: null, zIndex: 0 };
}

/** Selection styling for one edge. See {@link focusNode}. */
export function focusEdge(
    graph: Graph,
    selected: string | null,
    edge: string,
    attrs: Attributes,
): Partial<EdgeDisplayData> {
    if (!selected || !graph.hasNode(selected)) return attrs;
    if (graph.hasExtremity(edge, selected)) {
        return { ...attrs, color: ACTIVE_EDGE, size: (attrs.size ?? 1) + 1, zIndex: 1 };
    }
    // Drop the label too — dimmed edges keeping full-strength text is the main
    // source of visual noise on a dense cluster.
    return { ...attrs, color: DIMMED_EDGE, label: null, zIndex: 0 };
}
