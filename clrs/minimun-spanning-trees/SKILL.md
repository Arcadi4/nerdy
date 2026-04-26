---
name: minimun-spanning-trees
description: Use when solving, proving, implementing, or reviewing minimum spanning tree problems, including safe edges, cuts, light edges, Kruskal, Prim, union-find, priority queues, bottleneck trees, second-best trees, or MST update questions.
license: MIT
---

# Minimum Spanning Trees

## Overview

Minimum-spanning-tree answers should not justify greedy choices by weight intuition alone. They must identify the maintained forest, the cut or cycle that certifies the next edge, and the data-structure contract that makes the stated bound real.

**Core principle:** prove an edge is safe by a cut-and-paste exchange, then implement the greedy rule with the representation that actually exposes the needed light edge.

## Shared Formatting Conventions

- Follow the parent `clrs` skill for mathematical formatting: every expression, inequality, objective, or asymptotic bound goes in a display LaTeX block, never in prose, tables, headings, or inline code spans.
- This rule applies to production comparison tables too: table cells may say "same comparison bound," "near-linear disjoint-set term," or "the textbook Fibonacci-heap bound," but the actual symbolic bounds must appear in display blocks outside the table.
- Use `greedy-algorithms` for the general exchange-proof discipline, `elementary-graph-algorithms` for graph representation contracts, and `data-structures-for-disjoint-sets` for union-find details.
- State that the graph is connected and undirected before using minimum-spanning-tree theorems. If it is disconnected, switch to a minimum spanning forest.
- State the graph representation before giving a running time.
- Preserve tie behavior: equal-weight light edges can yield different minimum spanning trees with the same total weight.

## When to Use

Use this skill for:

- Minimum spanning trees, minimum spanning forests, network-design trees, and wiring-style connection problems.
- Safe-edge, cut, light-edge, cycle, bottleneck, and exchange arguments.
- Kruskal's algorithm, Prim's algorithm, Boruvka-style contraction, or MST preprocessing.
- Updating an existing minimum spanning tree after one edge weight changes or one vertex is added.
- Comparing union-find, binary-heap priority queues, Fibonacci heaps, adjacency lists, and adjacency matrices for MST implementations.
- Second-best minimum spanning tree questions and max-edge-on-tree-path reasoning.

Do not use this skill for shortest paths, maximum flow, matching, or general dynamic graph connectivity unless the immediate question is how those problems differ from minimum spanning trees.

## Quick Reference

| Problem shape | Use | Required contract | Proof hook |
| --- | --- | --- | --- |
| Need to add one edge to a partial MST forest | Safe-edge rule | Current edge set is contained in some MST | Light edge crossing a cut that respects the forest |
| Need a certificate that a greedy edge is legal | Cut property | Cut is chosen before or independently of the candidate edge and respects the accepted set | Exchange an existing crossing edge out of an MST |
| Need Kruskal's next edge | Global sorted edge scan | Union-find exactly represents current forest components | Component corollary |
| Need Prim's next edge | Tree-to-outside priority queue | Keys record cheapest edge from the grown tree to each outside vertex | Component corollary for the current tree |
| Need to reject an edge on a cycle | Cycle max-edge rule | A concrete cycle is present in the graph | Remove a maximum edge from the cycle |
| Need to update after a non-tree edge decreases | Add the edge, inspect the old tree path, possibly swap | Existing MST and path maximum are available | Cycle exchange |
| Need production implementation advice | Choose by graph shape and library support | Memory, handles, total ordering, and update support are specified | Same greedy proof, different engineering risk |

Keep symbolic definitions outside the table. The usual input model is below.

$$
G=(V,E)
$$

The objective is below.

$$
w(T)=\sum_{(u,v)\in T} w(u,v)
$$

## Safe Edges and the Cut Rule

A set of accepted edges is safe to maintain when it is a subset of at least one minimum spanning tree. Generic MST algorithms start with the empty set and repeatedly add an edge that preserves this property.

Core definitions:

- A cut partitions the vertices into two sides.
- An edge crosses a cut when its endpoints are on opposite sides.
- A cut respects the accepted set when no accepted edge crosses it.
- A light edge crossing a cut is an edge whose weight is minimum among crossing edges; ties are allowed.

The theorem-use checklist:

1. Confirm the graph is connected and undirected.
2. Confirm the accepted set is already contained in some MST.
3. Choose a cut that respects the accepted set.
4. Identify a light crossing edge for that cut.
5. Conclude that adding that edge is safe.

The cut theorem is below.

$$
\text{If } A \text{ is contained in some MST, the cut respects } A,
\text{ and } e \text{ is light across the cut, then } e \text{ is safe for } A.
$$

Proof recipe:

1. Let an MST contain the accepted set.
2. If the light edge is already in that MST, stop.
3. Otherwise add the light edge; it creates a cycle on the old tree path between its endpoints.
4. The old path must contain some edge crossing the same cut.
5. That crossing edge is not in the accepted set because the cut respects the accepted set.
6. Remove that old crossing edge and keep the light edge.
7. The replacement does not increase total weight, so the new tree is also an MST and contains the accepted set plus the new edge.

Use the component corollary when the accepted set is a forest. For a component of the forest, the cut consisting of that component versus all other vertices respects the accepted set. A light edge connecting that component to a different component is safe.

## Cut Converse Trap

Do not reverse the cut theorem. A safe edge crossing a respecting cut need not be light for that cut.

Replayable counterexample:

- Vertices are named `a`, `b`, `c`, and `d`.
- Edge weights are listed below.

$$
w(a,b)=1,\quad w(b,c)=2,\quad w(b,d)=3,\quad w(c,d)=3,\quad w(a,c)=5
$$

- The accepted set contains the single edge below.

$$
A=\{(a,b)\}
$$

- Use the cut with one side containing `a` and `b`, and the other side containing `c` and `d`.
- The cut respects the accepted set because the accepted edge stays on one side.
- The crossing edge below is light.

$$
(b,c)
$$

- The crossing edge below is safe but not light.

$$
(b,d)
$$

Why safe: the edge set below is a minimum spanning tree.

$$
\{(a,b),(b,c),(b,d)\}
$$

Its total weight is the same as the alternative tree below.

$$
\{(a,b),(b,c),(c,d)\}
$$

Therefore the heavier crossing edge can be safe even though a lighter crossing edge exists.

## Cycle and Max-Edge Rule

Use the cycle rule to reject edges, update trees, and reason about non-tree edges.

If an edge is a maximum-weight edge on a cycle, then some MST avoids that edge. If it is the unique maximum edge on the cycle, no MST contains it.

Proof recipe:

1. Suppose a spanning tree contains the cycle's maximum edge.
2. Removing that edge disconnects the tree into two components.
3. The rest of the cycle contains another edge crossing the same induced cut.
4. Add that other edge to reconnect the tree.
5. The replacement does not increase total weight, and strictly improves the tree when the removed edge is uniquely heavier.

Do not claim every non-MST edge is globally heavy. The useful fact is path-relative: for a non-tree edge, compare it with the maximum edge on the unique tree path between its endpoints.

## Kruskal's Algorithm

Use Kruskal when sorting edges is acceptable and a simple, robust implementation matters. The accepted set is a forest over all vertices.

Pseudocode pattern:

```text
KRUSKAL(G, w):
    A = empty set
    for each vertex v:
        MAKE-SET(v)
    sort edges by nondecreasing weight
    for each edge (u, v) in sorted order:
        if FIND-SET(u) != FIND-SET(v):
            add (u, v) to A
            UNION(u, v)
    return A
```

Invariant checklist:

1. Union-find sets are exactly the connected components of the current forest.
2. An edge whose endpoints are already in the same set would create a cycle and must be skipped.
3. The first scanned edge connecting two different components is light among all remaining edges connecting those two forest components to something outside at the moment it is accepted.
4. The component corollary makes that accepted edge safe.
5. Stop once the accepted set contains the right number of tree edges; continuing only scans rejected cycle edges.

With union by rank and path compression, the disjoint-set operations contribute the near-linear bound below over the whole run.

$$
O(E\alpha(V))
$$

Sorting dominates under the comparison model.

$$
O(E\lg V)
$$

Implementation contracts:

- Edge weights need a total preorder; define deterministic tie-breaking only for reproducible output, not correctness.
- Parallel edges are allowed if the representation preserves edge identity.
- Union-find representatives are equality tokens, not semantic component labels.
- The graph must be connected for a spanning tree; otherwise Kruskal returns a minimum spanning forest.
- If integer weights have a small bounded range, specialized sorting can improve the sorting term, but only when the range and memory budget are real.

## Prim's Algorithm

Use Prim when the graph is naturally available as adjacency lists from a growing tree, or when storing and sorting the whole edge list is less attractive. The accepted set is always one tree rooted at an arbitrary start vertex.

Core state:

- Each outside vertex has a key: the cheapest known edge from the current tree to that vertex.
- Each outside vertex has a parent pointer naming the tree vertex that realizes its key.
- The priority queue contains exactly the vertices not yet in the tree.
- Extracting the minimum-key vertex adds the parent edge to the tree, except for the root.

Pseudocode pattern:

```text
PRIM(G, w, r):
    for each vertex u:
        u.key = infinity
        u.parent = NIL
    r.key = 0
    Q = all vertices keyed by key
    while Q is not empty:
        u = EXTRACT-MIN(Q)
        for each neighbor v of u:
            if v is still in Q and w(u, v) < v.key:
                v.parent = u
                v.key = w(u, v)
                DECREASE-KEY(Q, v)
```

Invariant checklist:

1. Vertices outside the queue are exactly the grown tree.
2. For every queued vertex with a parent, its key is the weight of a light edge connecting it to the grown tree among edges seen so far from the grown tree.
3. The extracted vertex is incident on a light edge crossing the cut between the grown tree and the queued vertices.
4. Updating neighbors after extraction restores the key invariant.

With a binary heap and adjacency lists, the total running time is below.

$$
O(E\lg V)
$$

With a Fibonacci heap, the textbook amortized bound is below.

$$
O(E+V\lg V)
$$

With an adjacency matrix and simple array keys, the dense-graph implementation can run in the bound below.

$$
O(V^2)
$$

Implementation contracts:

- A real decrease-key operation needs handles or an index map from vertices to heap positions. A standard library heap without decrease-key usually needs lazy duplicate entries plus stale-entry checks, changing constants and memory behavior.
- Queue membership must be testable when relaxing adjacency edges.
- Fibonacci heaps are an asymptotic teaching tool; production code usually prefers binary heaps, pairing heaps, specialized indexed heaps, or library graph routines unless profiling justifies the complexity.
- Adjacency lists give the stated edge-scan bound; adjacency matrices change neighbor scanning costs.

## Choosing Kruskal or Prim in Practice

Prefer Kruskal when:

- Edges already arrive as a batch edge list.
- Sorting fits memory and is well-optimized by the platform.
- The graph is sparse or medium-sized and implementation risk matters.
- You need simple deterministic testing around union-find and sorted edges.

Prefer Prim when:

- The graph is already adjacency-list based and vertex-centric.
- The graph is dense enough that scanning adjacency structures is natural.
- You can use an indexed priority queue or a matrix implementation with predictable storage.
- You need to grow from a root for integration reasons, while remembering that the MST cost does not depend on the root.

Do not recommend textbook Fibonacci heaps by default in production. Extract the chapter lesson instead: reducing decrease-key cost matters only when the workload actually performs many successful key decreases and when the implementation's constants, memory locality, and maintenance cost are acceptable.

When writing a production comparison table, keep the time column verbal. Put the concrete bounds immediately before or after the table as display blocks. A safe comparison table uses entries such as "comparison-sort dominated," "indexed-heap dominated," and "amortized textbook bound," not symbolic notation.

## Dynamic MST Update Patterns

### Decreasing a Tree Edge

If the weight of an edge already in an MST decreases, the same tree remains an MST. Proof: every alternative tree's relative cost cannot improve against a tree that contains the discounted edge; the tree's total weight only decreases.

### Decreasing a Non-Tree Edge

Add the changed edge to the old MST. It creates one cycle consisting of the new edge plus the old tree path between its endpoints. Remove a maximum-weight edge from the old tree path if the changed edge is lighter than that path maximum; otherwise keep the old tree.

Algorithm:

1. Find the unique path between the changed edge's endpoints in the old tree.
2. Find a maximum-weight edge on that path.
3. If the changed edge is lighter than that maximum path edge, swap them.
4. Otherwise return the old tree.

A single update can be handled by a tree search in the bound below.

$$
O(V)
$$

For many updates, preprocess for max-edge-on-path queries using an appropriate tree data structure; state the update and query model before claiming a faster bound.

### Adding a New Vertex

When a new vertex and its incident edges are added to a graph with a known MST, attach the new vertex using its minimum-weight incident edge, then consider whether additional incident edges can improve the old tree by cycle exchanges. A safe simple answer is to run the non-tree-edge decrease/addition check for each incident edge after initially connecting the vertex; advanced answers may use dynamic tree structures.

## Second-Best Minimum Spanning Tree

For distinct edge weights, the MST is unique, but the second-best tree can be found by one-edge exchange.

Recipe:

1. Compute the MST.
2. For every non-tree edge, find the maximum-weight edge on the unique tree path between its endpoints.
3. The candidate tree adds the non-tree edge and removes that path maximum.
4. Choose the candidate with the smallest positive increase in total weight.

The exchange delta is below.

$$
\Delta = w(e)-w(f)
$$

Here the first edge is a non-tree edge and the second edge is the maximum edge on the corresponding tree path. Put the formula in display form when using it in answers.

## Bottleneck Spanning Trees

Every minimum spanning tree is a bottleneck spanning tree: if the largest edge in an MST were not minimum possible, replacing with a spanning tree of smaller bottleneck would contradict the cut or Kruskal threshold view.

Decision rule for a candidate bottleneck value:

1. Keep only edges whose weight is at most the candidate value.
2. Test whether the resulting graph is connected.
3. If connected, a spanning tree exists using no larger edge; otherwise no such tree exists.

This gives a clean way to reason about bottleneck problems separately from total MST weight.

## Answer Template

When solving an MST prompt, structure the answer as follows:

1. **Model:** connected undirected graph, weight assumptions, representation, and whether ties matter.
2. **Invariant:** accepted edge set is a forest contained in some MST, or a single Prim tree with priority-queue keys.
3. **Safe-edge certificate:** name the cut, component, or cycle exchange that justifies the chosen edge.
4. **Algorithm:** give the steps only after the proof hook is clear.
5. **Complexity:** state the data structure and representation before the bound.
6. **Production translation:** call out handles, memory, sorting, queue membership, total ordering, and library alternatives when implementation is requested.

## RED Pressure Failures This Skill Prevents

| Failure mode | What goes wrong | Skill countermeasure |
| --- | --- | --- |
| Reversing the cut theorem | Claims every safe crossing edge must be light | Includes a replayable counterexample with accepted set, cut, safe edge, and lighter edge |
| Vague dynamic update | Says to rerun Kruskal or swaps without proof | Forces the add-edge cycle and max-path exchange argument |
| Fibonacci heap overrecommendation | Treats the asymptotic bound as a production default | Requires handles, amortized-cost, locality, and maintenance contracts |
| Missing queue contracts in Prim | Gives the textbook bound with a standard heap lacking decrease-key | Requires vertex handles or lazy stale-entry policy |
| Formula leaks in tables | Puts objectives and bounds inline | Keeps tables verbal and moves formulas to display blocks |
| Production table leakage | Puts Kruskal, Prim, or Fibonacci-heap bounds directly in comparison cells | Requires verbal time labels in tables and display blocks adjacent to the table |
| Tie confusion | Assumes MST uniqueness without distinct weights | States that ties can produce multiple MSTs and safe light edges |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Saying the lowest global edge is always the whole proof | It belongs to some MST, but each later step needs a cut or component certificate |
| Treating arbitrary clusters as Kruskal components | Components must be induced by the accepted forest |
| Applying the cut theorem to a cut crossed by accepted edges | The cut must respect the accepted set |
| Claiming the converse of the cut theorem | Safe crossing edges need not be light for that cut |
| Removing the new edge in a non-tree-edge update | Remove a maximum edge from the old tree path if a swap improves the tree |
| Claiming Prim and Dijkstra are the same | Prim keys are cheapest incident tree edges; Dijkstra keys are path-distance estimates |
| Forgetting disconnected inputs | Return a minimum spanning forest or report that no spanning tree exists |
| Hiding edge identity | Parallel edges and original-edge references matter for contractions and MST-REDUCE-style preprocessing |

## Verification Pressure Tests

Use these prompts to verify the skill changes future answers:

1. **Cut converse trap:** Give a graph, accepted set, respecting cut, safe edge, and lighter crossing edge that disproves the converse of the cut theorem.
2. **Dynamic update:** Given an MST and a decreased non-tree edge, produce the path-maximum swap algorithm, proof, and single-update running time.
3. **Production choice:** For a million-edge graph, choose among Kruskal, binary-heap Prim, and Fibonacci-heap Prim while naming memory, sorting, decrease-key, and union-find contracts.
4. **Formatting fidelity:** Distinguish cut property, component corollary, and cycle rule in a table whose cells contain only prose, then put theorem formulas and bounds in display blocks.
5. **Second-best tree:** Explain why checking every non-tree edge plus the maximum edge on its tree path suffices.

## Static Checks

- Frontmatter `name` matches the requested directory slug `minimun-spanning-trees`.
- Description starts with "Use when" and names MST triggers, not the workflow.
- Parent `clrs/SKILL.md` has a routing bullet for this chapter skill.
- All formulas, objectives, and asymptotic bounds appear in display LaTeX blocks.
- Markdown tables contain verbal guidance only.
- Production comparison tables use verbal time labels, with symbolic bounds outside the table.
- The skill is not a narrative chapter summary or session log.
- The chapter-specific facts stay here rather than in the parent router.
