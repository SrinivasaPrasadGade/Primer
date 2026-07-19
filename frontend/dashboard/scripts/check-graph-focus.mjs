/**
 * Behaviour check for the fraud-graph selection highlighting.
 *
 * Imports the real src/components/graph/graphFocus.ts — that module is
 * deliberately free of React, CSS and sigma runtime imports so it can be
 * exercised headlessly (sigma needs WebGL).
 *
 *     node --experimental-strip-types scripts/check-graph-focus.mjs
 */
import Graph from "graphology";
import { ACTIVE_EDGE, DIMMED_EDGE, DIMMED_NODE, focusEdge, focusNode } from "../src/components/graph/graphFocus.ts";

let pass = 0;
let fail = 0;

function check(name, got, want) {
    const ok = JSON.stringify(got) === JSON.stringify(want);
    if (ok) {
        pass++;
        console.log(`  PASS  ${name}`);
    } else {
        fail++;
        console.log(`  FAIL  ${name}\n          got ${JSON.stringify(got)}\n         want ${JSON.stringify(want)}`);
    }
}

// a—b—c—d. Selecting b focuses {a, b, c}; d and the c—d edge fall outside it.
const g = new Graph();
for (const n of ["a", "b", "c", "d"]) g.addNode(n, { size: 10, color: "#3B82F6", label: n });
const ab = g.addEdge("a", "b", { size: 2, color: "#fff", label: "transferred_to" });
const bc = g.addEdge("b", "c", { size: 2, color: "#fff", label: "transferred_to" });
const cd = g.addEdge("c", "d", { size: 2, color: "#fff", label: "owns" });

const node = (n) => g.getNodeAttributes(n);
const edge = (e) => g.getEdgeAttributes(e);

console.log("\nselection = 'b'  (neighbours a and c; d is outside the neighbourhood)");
{
    const r = focusNode(g, "b", "b", node("b"));
    check("selected node is enlarged and highlighted", [r.size, r.highlighted, r.forceLabel], [14.5, true, true]);
}
for (const n of ["a", "c"]) {
    const r = focusNode(g, "b", n, node(n));
    check(`neighbour '${n}' keeps its entity-type colour and shows its label`, [r.color, r.forceLabel], ["#3B82F6", true]);
}
{
    const r = focusNode(g, "b", "d", node("d"));
    check("non-neighbour 'd' is dimmed and loses its label", [r.color, r.label], [DIMMED_NODE, null]);
}
for (const [name, e] of [["a—b", ab], ["b—c", bc]]) {
    const r = focusEdge(g, "b", e, edge(e));
    check(`incident edge ${name} is brightened and thickened`, [r.color, r.size], [ACTIVE_EDGE, 3]);
}
{
    const r = focusEdge(g, "b", cd, edge(cd));
    check("distant edge c—d is dimmed and loses its label", [r.color, r.label], [DIMMED_EDGE, null]);
}

console.log("\nselection = null  (nothing picked — the default view)");
check("node attributes pass through untouched", focusNode(g, null, "a", node("a")), node("a"));
check("edge attributes pass through untouched", focusEdge(g, null, ab, edge(ab)), edge(ab));

console.log("\nselection = an id that is not in this graph  (stale after switching entity)");
check("node falls back to the unfocused view", focusNode(g, "gone", "a", node("a")), node("a"));
check("edge falls back to the unfocused view", focusEdge(g, "gone", ab, edge(ab)), edge(ab));

console.log(`\n${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
