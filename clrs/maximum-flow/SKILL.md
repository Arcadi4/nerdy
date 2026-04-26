---
name: maximum-flow
description: Use when solving, proving, implementing, or reviewing flow-network problems, including maximum flow, residual networks, augmenting paths, cuts, Ford-Fulkerson, Edmonds-Karp, bipartite matching reductions, vertex capacities, multiple sources and sinks, or min-cut certificates.
license: MIT
---

# Maximum Flow

## Overview

Use this skill to decide whether a problem is really a flow model, a cut certificate, an augmenting-path algorithm question, or a matching reduction before naming an algorithm.

**Core principle:** a maximum-flow answer is correct only when the model preserves capacity constraints, conservation, residual cancellation, and the cut certificate that proves optimality.

## Shared CLRS Conventions

- Follow the parent `clrs` skill for mathematical formatting: every formula, inequality, asymptotic bound, and symbolic expression belongs in a display LaTeX block.
- Use chapter-specific theorem names here, and keep shared graph traversal mechanics in `elementary-graph-algorithms`.
- State the graph direction, source and sink convention, capacity domain, and whether integrality matters before using Ford-Fulkerson, Edmonds-Karp, or a matching reduction.
- Keep tables verbal. Put capacities, residual definitions, and running times in display blocks near the table instead of inside table cells.

## When to Use

Use this skill when a task involves:

- modeling transport, assignment, disjoint paths, escape routes, image segmentation-style cuts, or feasibility through capacities;
- proving a flow is maximum or extracting a minimum cut from a residual network;
- choosing or analyzing Ford-Fulkerson, Edmonds-Karp, capacity scaling, or push-relabel-style production alternatives;
- reducing bipartite matching, vertex capacities, multiple sources, multiple sinks, or antiparallel directed edges to ordinary single-source single-sink flow;
- reviewing an implementation that maintains residual edges, reverse edges, bottlenecks, or integer-flow assumptions.

Do not use this skill merely because a graph is directed. If the task is shortest paths, reachability, strongly connected components, spanning trees, or topological order without capacities and conservation, route to `elementary-graph-algorithms`, `shortest-paths`, or `minimun-spanning-trees` as appropriate instead.

## First Decision

| Situation | First move | Watch for |
| --- | --- | --- |
| Ordinary source-to-sink capacity question | Define the flow network and requested output | Forgetting conservation or the direction of cut capacity |
| Antiparallel edges, many sources, many sinks, or vertex limits | Normalize the network before analyzing algorithms | Claiming value preservation without mapping flows both ways |
| Need proof of optimality | Extract or name a cut certificate | Skipping saturated-forward and zero-reverse facts |
| Integer capacities and small optimal value | Basic Ford-Fulkerson may be acceptable for analysis | Value-dependent running time and bad path choices |
| Need a polynomial guarantee independent of value | Use Edmonds-Karp or another strongly bounded method | Calling arbitrary augmenting paths polynomial without assumptions |
| Bipartite matching | Build the unit-capacity flow network | Conflating max-flow min-cut with the integrality theorem |
| Large production workload | Prefer mature max-flow libraries and push-relabel-style methods | Hand-rolling textbook pseudocode without profiling or adversarial tests |

Use the bounds below when the algorithm choice matters.

$$
O(E\,|f^*|)
$$

$$
O(VE^2)
$$

## Output Contract Checklist

Before giving the final answer, check each item that applies:

- Name the original problem and the transformed flow problem.
- State whether capacities are real-valued, rational, integer-valued, or unit capacities.
- Identify the source set, sink set, supersource, supersink, and any split vertices.
- Say whether the answer needs a maximum value, a full flow, a minimum cut, a matching, or a feasibility certificate.
- For a reduction, give a mapping from original solutions to flows and from flows back to original solutions.
- For a proof, include capacity constraints, conservation, residual reachability, and cut equality.
- For an algorithm, state the augmenting-path rule and the assumption behind the running time.
- For implementation advice, describe reverse-edge bookkeeping and the production alternative if textbook code is not the right deliverable.

## Flow Network Model

A flow network is a directed graph with a source, a sink, nonnegative capacities, no self-loops, and no antiparallel edges in the textbook model. Every vertex is assumed to lie on a source-to-sink path after irrelevant vertices are removed.

A flow obeys the capacity constraint.

$$
0 \le f(u,v) \le c(u,v)
$$

It also obeys conservation at every ordinary vertex.

$$
\sum_{u \in V} f(u,v) = \sum_{w \in V} f(v,w)
$$

The flow value is the net flow out of the source.

$$
|f| = \sum_{v \in V} f(s,v) - \sum_{v \in V} f(v,s)
$$

For answers under the parent formatting rule, refer to these as the capacity constraint, conservation law, and source net-flow value rather than repeating formulas inline.

## Normalization and Modeling Reductions

### Antiparallel directed edges

If both directions appear between two vertices, split one of the two directed edges. Replace the chosen edge by a two-edge path through a new vertex, and give both new edges the original capacity. State which direction you split; either direction preserves the maximum value, so choose the direction that keeps the transformed instance easiest to explain or matches the prompt's construction order.

Preservation proof recipe:

1. Any old flow through the split edge becomes equal flow through both new edges.
2. Any new feasible flow must send equal flow through both new edges by conservation at the inserted vertex.
3. Therefore feasible values and maximum values are unchanged.
4. The transformation adds one vertex and one extra edge per split edge.

### Multiple sources and sinks

For many sources, add a supersource with edges to the original sources. For many sinks, add a supersink with edges from the original sinks. Always state the capacity choice for these added edges. If the original sources and sinks are unconstrained, use a safe nonbinding capacity such as the sum of outgoing original capacities or a symbolic infinite capacity. If the prompt intentionally encodes supplies or demands, use those exact capacities instead.

If the prompt has exact supplies or exact demands, do not merely say “infinite capacity.” Use the required supply or demand edge capacities and verify that the computed maximum flow reaches the total required amount.

### Vertex capacities

Split each capacity-limited vertex into an input copy and an output copy. Incoming edges enter the input copy, outgoing edges leave the output copy, and the connecting edge enforces the vertex limit.

If source or sink throughput is also limited, split it too. If the source and sink are exempt from the vertex-capacity rule, say so explicitly.

### Escape, disjoint paths, and separator variants

For edge-disjoint paths, use unit edge capacities. For vertex-disjoint paths, split vertices and use unit capacity on the internal split edge. For grid escape problems, connect each cell to its neighbors with the relevant unit capacities, connect starting cells to the supersource, connect exits to the supersink, and test whether the flow value reaches the number of agents.

### Cut variants

For an edge whose membership in a minimum cut is being tested, force or forbid that edge through capacity changes or contraction only after stating which cut problem is being solved. For a global directed minimum cut, do not pretend one source-to-sink run is enough unless the source and sink are fixed by the problem.

## Residual Networks and Augmentation

The residual network represents how the current flow can still change. Forward residual capacity means unused capacity on an original edge. Reverse residual capacity means cancellable positive flow.

$$
c_f(u,v) = c(u,v) - f(u,v)
$$

$$
c_f(v,u) = f(u,v)
$$

An augmenting path is a source-to-sink path in the residual network. Its bottleneck is the smallest residual capacity on the path.

$$
c_f(p) = \min\{c_f(u,v) : (u,v) \text{ lies on } p\}
$$

Augmenting increases original-edge flow on forward residual edges and decreases original-edge flow on reverse residual edges.

$$
f(u,v) \leftarrow f(u,v) + c_f(p)
$$

$$
f(u,v) \leftarrow f(u,v) - c_f(p)
$$

Implementation review checklist:

- Store each residual edge with a pointer or index to its reverse partner.
- Update both directions atomically on every augmentation.
- Never interpret a reverse residual edge as a real edge in the original problem unless the original edge exists separately.
- Keep original capacity and current residual capacity distinct in names.
- Use integer types only when the maximum possible accumulated flow fits them.

## Cut Certificates and Max-Flow Min-Cut

When the residual network has no augmenting path, the minimum cut certificate is obtained by reachability from the source in the residual network. Let the source-reachable side be the source side of the cut, and let all other vertices be the sink side.

Proof recipe:

1. The sink is not reachable, so this is a valid source-sink cut.
2. Every original edge from the source side to the sink side is saturated. Otherwise that edge would have positive forward residual capacity and would make the sink-side endpoint reachable.
3. Every original edge from the sink side to the source side carries zero flow. Otherwise the reverse residual edge would go from the source side to the sink side and make that sink-side endpoint reachable.
4. Net flow across this cut equals the flow value by the cut-flow lemma.
5. Saturation and zero reverse flow make the net flow equal the cut capacity.
6. Since every flow is bounded above by every cut capacity, equality proves both maximum flow and minimum cut.

Use the theorem equivalence below as the concise certificate structure.

$$
f \text{ is maximum}
\quad\Longleftrightarrow\quad
G_f \text{ has no augmenting path}
\quad\Longleftrightarrow\quad
|f| \text{ equals the capacity of some cut}
$$

Common proof trap: if an original edge goes from the sink side back to the source side and carries positive flow, the residual edge goes from the source side to the sink side. That is what contradicts the sink-side vertex being unreachable from the source.

## Ford-Fulkerson and Edmonds-Karp

Basic Ford-Fulkerson:

1. Initialize all flows to zero.
2. Build or query the residual network.
3. Find any augmenting path.
4. Augment by the bottleneck.
5. Stop when no augmenting path remains.
6. Extract the reachable-set cut if a certificate is required.

For integer capacities, every augmentation increases the value by at least one unit. The value-dependent bound is below.

$$
O(E\,|f^*|)
$$

With irrational capacities and adversarial augmenting-path choices, the method may fail to terminate. With poor integer path choices, it can take many augmentations even when a better path choice exists.

Edmonds-Karp is Ford-Fulkerson with breadth-first search shortest augmenting paths. Its proof hinges on residual shortest-path distances never decreasing and on each edge becoming critical only a bounded number of times. The strongly polynomial bound is below.

$$
O(VE^2)
$$

Capacity scaling chooses augmenting paths with large residual capacity first. Use it when the prompt explicitly asks for scaling or when the largest capacity parameter is part of the analysis.

$$
O(E^2 \log C)
$$

Production judgment: for large or performance-sensitive max-flow instances, prefer a maintained library and consider push-relabel implementations. The transferable idea from the chapter is not “hand-roll Ford-Fulkerson”; it is how residual cancellation, augmenting certificates, and cut duality make the solution auditable.

## Bipartite Matching Reduction

For a bipartite graph, direct every original matching edge from the left side to the right side. Add a source connected to every left vertex and a sink connected from every right vertex. Give every edge unit capacity.

A matching becomes an integer-valued flow by sending one unit along each selected left-to-right edge and through the corresponding source and sink edges. An integer-valued flow becomes a matching by selecting exactly the left-to-right edges carrying positive flow. Unit capacities ensure no vertex is selected more than once.

Use the integrality theorem for the flow-to-matching step: Ford-Fulkerson with integer capacities produces an integer-valued maximum flow. Rational or real capacities alone are not enough for this extraction claim unless the problem has been converted to an equivalent integer-capacity network. Then use max-flow optimality to conclude maximum cardinality.

Do not justify the extraction only by max-flow min-cut. The cut theorem proves optimality of the flow value; integrality is what makes the flow readable as a matching.

The basic Ford-Fulkerson running time for this constructed network follows because each augmentation increases the matching size by one and the matching size is bounded by the number of vertices.

$$
O(VE)
$$

If the graph has isolated vertices, remove them or say that the edge-count simplification assumes every vertex has at least one incident edge.

## Worked Answer Pattern

When asked to solve or review a maximum-flow problem, use this structure:

1. **Model:** name vertices, directed edges, source, sink, capacities, and any normalizing transformations.
2. **Preservation:** map original feasible solutions to flows and map flows back to original feasible solutions.
3. **Algorithm:** choose the augmenting-path rule or library based on capacity domain and required bound.
4. **Certificate:** provide either residual reachability cut or matching extraction.
5. **Complexity:** state the graph size after transformation and the algorithm bound under its assumptions.
6. **Implementation risk:** call out reverse-edge bookkeeping, integer overflow, or production library preference when relevant.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Listed antiparallel, supersource, and split-vertex transformations without proving preservation | Map feasible flows in both directions and account for added vertices and edges |
| Ignored whether source and sink participate in vertex capacities | State whether they are split or exempt |
| Extracted a residual reachable-set cut but gave a vague optimality proof | Prove saturated forward edges, zero reverse edges, cut-flow equality, and weak duality |
| Described backward zero-flow contradiction in the wrong direction | Say positive backward original flow creates a residual edge from the source side to the sink side |
| Reduced bipartite matching to flow but conflated theorem roles | Use integrality to extract the matching and max-flow optimality to prove cardinality |
| Claimed running times without algorithm assumptions | Tie each bound to arbitrary Ford-Fulkerson, Edmonds-Karp, scaling, or the unit-capacity matching construction |
| Leaked formulas in prose or table cells | Put all formulas and bounds in display LaTeX blocks |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Treating reverse residual edges as original edges | Reverse residual capacity represents cancellable flow |
| Saying no augmenting path means no local improvement only | Use the max-flow min-cut theorem to turn it into a global certificate |
| Counting cut capacity in both directions | Cut capacity counts only original edges from the source side to the sink side |
| Forgetting negative contribution of sink-side-to-source-side flow in net cut flow | Include zero-reverse proof when deriving equality |
| Applying integer-flow extraction to noninteger capacities | Require integer capacities and an integral-flow algorithm result before reading a combinatorial object from a flow |
| Promising basic Ford-Fulkerson is polynomial without capacity assumptions | Use Edmonds-Karp or another strongly bounded method for a capacity-independent guarantee |
| Hand-rolling textbook algorithms in production by default | Prefer mature libraries unless the task is educational, small, or requires a custom auditable implementation |
| Giving a matching reduction for a non-bipartite graph | Use a matching algorithm appropriate to the graph class instead |

## Verification Pressure Tests

Use these prompts to test whether the skill changes behavior:

1. A network has antiparallel edges, three sources, two sinks, and a vertex capacity on every ordinary vertex. Ask for an ordinary max-flow transformation, size accounting, and proof that the maximum value is preserved.
2. Ford-Fulkerson terminates with no augmenting path. Ask for a minimum-cut certificate and a proof that explicitly handles forward crossing edges and backward crossing edges.
3. A bipartite graph is reduced to max flow. Ask which theorem makes the extracted matching valid, which theorem proves optimality, and why the running time is value-bounded.
4. A production service needs high-throughput max flow on large graphs with integer capacities. Ask whether to implement textbook Ford-Fulkerson and what chapter insight remains useful if the answer is no.
5. A response must include a decision table and complexity bounds under the parent CLRS formatting rules. Reject any formula in a table cell, heading, inline code span, or prose sentence.
6. A vertex-disjoint paths problem names the source and sink as exempt from vertex limits. Check that the transformation splits only the constrained vertices and explains the exemption.
7. A residual graph contains a reverse edge across the proposed cut. Ask what original-flow fact it represents and which reachability contradiction it would create.

## Static Checks

Before declaring the skill complete:

- Confirm this file lives at `clrs/maximum-flow/SKILL.md`.
- Confirm frontmatter has `name`, `description`, and `license`, with the name matching the directory slug.
- Confirm the parent `clrs/SKILL.md` routes to `maximum-flow`.
- Inspect headings and tables for formulas; formulas must appear only in display LaTeX blocks.
- Check that RED failures are represented in `## RED Pressure Failures This Skill Prevents`.
- Check that the skill distinguishes textbook Ford-Fulkerson mechanics from production max-flow implementation judgment.
- Check that no session narrative, source-processing story, or authoring log appears in the skill.
- Check that chapter-specific theorem details stay here instead of in the parent router.
