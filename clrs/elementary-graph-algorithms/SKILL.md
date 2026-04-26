---
name: elementary-graph-algorithms
description: Use when representing graphs or solving graph-search problems with adjacency lists, adjacency matrices, breadth-first search, depth-first search, topological sorting, strongly connected components, edge classification, reachability, articulation points, bridges, biconnected components, or Euler tours.
license: MIT
---

# Elementary Graph Algorithms

## Overview

Graph-search answers must bind the representation contract to the invariant being used. Breadth-first search is a layer and shortest-unweighted-path argument; depth-first search is an interval, ancestor, and finish-time argument; topological sorting and strongly connected components are finish-time applications, not just traversal recipes.

## Shared CLRS Conventions

- Follow the parent `clrs` skill for mathematical formatting: every expression, bound, inequality, or recurrence goes in a display LaTeX block, never in prose, tables, headings, or inline code spans.
- Use CLRS graph notation and theorem numbers when they clarify the proof.
- State whether the graph is directed or undirected before classifying edges or claiming reachability.
- State the representation before giving a running time.
- Treat adjacency-list order as an input-order detail: it can change discovery order and predecessor trees, but not breadth-first distances.

## When to Use

Use this skill for:

- Choosing adjacency lists, adjacency matrices, or augmented adjacency structures.
- Breadth-first search for unweighted single-source shortest paths, layers, reachability, and breadth-first trees.
- Depth-first search for timestamp intervals, ancestor reasoning, edge classification, cycle detection, articulation points, bridges, and biconnected components.
- Topological sorting of directed acyclic graphs.
- Strongly connected components using the two-pass transpose algorithm.
- Euler-tour existence in directed graphs and reachability questions that reduce to component condensation.

Do not use it as the main skill for weighted shortest paths, minimum spanning trees, maximum flow, matching, or dynamic graph maintenance unless the immediate task is the representation or the initial traversal invariant.

## Quick Reference

| Problem shape | Use | Required precondition | Main proof hook |
| --- | --- | --- | --- |
| Sparse graph traversal | Adjacency lists | Neighbor iteration dominates | Scan each list once |
| Dense edge-existence queries | Adjacency matrix | Vertices have stable indices | Constant edge lookup, quadratic storage |
| Unweighted shortest paths from one source | Breadth-first search | Unit edge cost or edge count metric | Layer monotonicity |
| Ancestors, descendants, and cycle witnesses | Depth-first search | Fixed vertex and adjacency iteration order for exact forest | Parenthesis and white-path theorems |
| Linear order of prerequisites | Topological sort | Directed acyclic graph | Decreasing finish times |
| Mutual reachability classes | Strongly connected components | Directed graph | Component finish-time ordering on the transpose |
| Undirected cut vertices and bridges | Depth-first low values | Connected component considered with tree and back edges | Subtree escape to a proper ancestor |

## Representation Decision

Use adjacency lists when traversal or sparse storage is central. The storage bound is below.

$$
\Theta(V+E)
$$

For directed graphs, list lengths sum to the number of edges. For undirected graphs, list lengths sum to twice the number of edges. Scanning all edges is linear in the representation.

Use adjacency matrices when edge-existence queries dominate and quadratic storage is acceptable. The storage and row-scan cost are below.

$$
\Theta(V^2)
$$

For undirected graphs, the matrix is symmetric; storing only one triangle is an implementation choice, not a change in the model. For weighted graphs, entries may store weights and reserve a sentinel such as NIL, zero, or infinity for absent edges only when that sentinel cannot be confused with a real weight.

Use hash-backed or sorted adjacency containers when edge-existence queries must be faster than scanning a list. Name the tradeoff explicitly: extra memory, weaker iteration locality, possible loss of deterministic adjacency order, hash adversary assumptions, and the need to preserve edge attributes. Balanced trees or sorted vectors may be better when deterministic order or range-like scans matter.

For production workloads that need both fast edge-existence queries and fast deterministic neighbor scans, consider a hybrid representation: an ordered neighbor list or vector for iteration plus a per-vertex lookup index for membership. State the synchronization cost and memory overhead explicitly. If external vertex ids arrive on the hot path, include the external-id resolution map in the lookup cost and failure modes.

Store vertex and edge attributes in the representation that matches the caller's identity model: parallel arrays for dense stable vertex ids, object fields for owned vertex records, maps for external ids, or edge records when parallel edges or edge identity matters.

## Breadth-First Search

Use breadth-first search when the distance measure is the number of edges on an unweighted path from a source. It works on directed and undirected graphs.

Core state:

- WHITE vertices are undiscovered.
- GRAY vertices are discovered and waiting in the queue.
- BLACK vertices have had their adjacency list scanned.
- The source has distance zero and NIL predecessor.
- Unreachable vertices keep infinite distance and NIL predecessor.

With adjacency lists, breadth-first search runs in the bound below.

$$
\Theta(V+E)
$$

With an adjacency matrix, each dequeued vertex requires scanning a full row, so the traversal uses the bound below.

$$
\Theta(V^2)
$$

### Invariant Checklist

When explaining or using breadth-first search, include these facts:

1. The queue contains exactly the gray vertices at the loop test.
2. The queue contains vertices from at most two consecutive distance layers.
3. Enqueued distances are monotone by Corollary 20.4.
4. Each tree edge sets a newly discovered vertex one layer deeper than its predecessor.
5. Lemma 20.1 supplies the edge relaxation inequality for true unweighted distances.
6. Lemma 20.2 says computed distances are upper bounds until Theorem 20.5 proves equality for all reachable vertices.
7. Lemma 20.6 says the predecessor subgraph is a breadth-first tree.

Affirmative queue wording: next-layer vertices may be enqueued while current-layer vertices remain in the queue. FIFO order places them behind the remaining current-layer vertices, which is why processing stays layer-monotone. Do not say all vertices in the next layer wait until the entire current layer has finished before being enqueued.

### Order-Dependence Rule

Distances are independent of adjacency-list order. Discovery order and the predecessor tree can change with adjacency-list order. If the task asks for a unique tree, require a specified neighbor order or a deterministic tie-breaker.

### Breadth-First Edge Classification

For undirected breadth-first search:

- Tree edges go to the next layer.
- Cross edges connect vertices in the same layer or adjacent layers.
- Back and forward edge categories from depth-first search do not appear.

For directed breadth-first search:

- Tree edges go to the next layer.
- Forward edges do not appear under the depth-first classification idea.
- Cross edges can point within the same layer, to the next layer, or to an earlier layer within the permitted breadth-first distance constraint.
- Back edges can point to an ancestor or earlier layer; they do not invalidate shortest-path distances.

## Depth-First Search

Use depth-first search when the answer depends on nesting, ancestors, finishing order, cycle witnesses, or decomposing an undirected graph by low values.

With adjacency lists, depth-first search runs in the bound below.

$$
\Theta(V+E)
$$

Core state:

- WHITE vertices are undiscovered.
- GRAY vertices are active on the recursion stack.
- BLACK vertices are finished.
- Each vertex receives one discovery time and one finish time.
- The predecessor subgraph is a depth-first forest.

### Theorem Hooks

- The parenthesis theorem, Theorem 20.7, says two vertex intervals are disjoint or one strictly contains the other. Containment is the ancestor relation.
- Corollary 20.8 turns strict interval nesting into proper-descendant reasoning.
- The white-path theorem, Theorem 20.9, says a vertex becomes a descendant exactly when a white path from the newly discovered ancestor exists at discovery time.
- In undirected graphs, Theorem 20.10 says every depth-first edge is tree or back; forward and cross edges do not occur.

### Directed Edge Classification

Classify an edge by the target color at exploration time first:

| Target color when explored | Classification rule |
| --- | --- |
| WHITE | Tree edge. No exception. |
| GRAY | Back edge to an active ancestor; self-loops are back edges. |
| BLACK | Forward or cross edge; use timestamps to distinguish. |

Use interval rules when timestamps are known.

Tree or forward edge:

$$
u.d < v.d < v.f < u.f
$$

Back edge:

$$
v.d \le u.d < u.f \le v.f
$$

Cross edge:

$$
v.d < v.f < u.d < u.f
$$

RED flag: an explored WHITE target is never a cross edge. If the prompt suggests a non-tree edge to a WHITE target, correct the premise.

## Topological Sort

Use topological sort only for directed acyclic graphs. The algorithm is:

1. Run depth-first search.
2. Put each vertex at the front of the output list when it finishes.
3. Return vertices in decreasing finish-time order.

The running time with adjacency lists is below.

$$
\Theta(V+E)
$$

Proof recipe:

- First check acyclicity. Lemma 20.11 says a directed graph is acyclic exactly when depth-first search produces no back edges.
- For a cycle proof, choose the first discovered vertex on the cycle; the remaining cycle path is white at that moment, so the white-path theorem forces a descendant and then a back edge.
- For Theorem 20.12, inspect each directed edge when it is explored. The target cannot be gray in a directed acyclic graph. If the target is white, it becomes a descendant and finishes first. If it is black, it has already finished. Either way, the source finishes later.

Do not claim every edge target becomes a descendant during the source's visit. A black target is already finished; the finish-time inequality still holds, but the descendant explanation does not apply.

## Strongly Connected Components

A strongly connected component is a maximal set of vertices that are mutually reachable. The transpose graph reverses every directed edge and preserves the component partition. With adjacency lists, the transpose can be built in linear time in the representation.

Algorithm:

1. Run depth-first search on the original graph and record finish times.
2. Build the transpose graph.
3. Run depth-first search on the transpose, considering vertices in decreasing first-pass finish time.
4. Output each second-pass depth-first tree as one strongly connected component.

The total running time with adjacency lists is below.

$$
\Theta(V+E)
$$

Proof recipe:

- Contract components into the component graph.
- Lemma 20.13 says the component graph is acyclic: if a path returned to the first component, the two components would be one component.
- Define a component's discovery time as its earliest first-pass discovery and its finish time as its latest first-pass finish.
- Lemma 20.14 gives the finish-time ordering for component edges in the original graph.

$$
f(C') > f(C)
$$

- Corollary 20.15 turns that ordering around in the transpose to prevent the next second-pass search from leaking into an unvisited component.
- Theorem 20.16 follows by induction over the second-pass trees: the root's component is still white, every vertex in that component is reachable in the transpose, and every outgoing transpose edge to another component leads only to a component already assigned.

Avoid source-versus-sink handwaving. If you use those words, tie them back to the first-pass component finish-time order and the no-leakage argument in the transpose.

## Advanced Depth-First Applications

### Articulation Points

In a connected undirected graph, the depth-first root is an articulation point exactly when it has at least two children in the depth-first tree.

A nonroot vertex is an articulation point exactly when it has a child subtree with no back edge to a proper ancestor of that vertex. Use low values to express the test.

For a child subtree rooted at a child, the articulation condition is below.

$$
\text{child.low} \ge \text{vertex.d}
$$

### Bridges

A bridge is an edge that lies on no simple cycle. For a tree edge from a parent to a child, the bridge condition is below.

$$
\text{child.low} > \text{parent.d}
$$

### Biconnected Components

Maintain an edge stack during depth-first search. When an articulation boundary is detected, pop edges up to the boundary tree edge; those popped edges form one biconnected component. Nonbridge edges partition into biconnected components, while bridges stand alone as single-edge components when components are defined over edges.

### Euler Tours in Directed Graphs

For a strongly connected directed graph, an Euler tour exists exactly when every vertex has equal indegree and outdegree. Find the tour by repeatedly following unused outgoing edges to form cycles and splicing cycles into the current tour, as in Hierholzer-style traversal. The edge-processing time is linear when unused outgoing edges are removed or advanced by cursor.

### Reachability Labels on Component Graphs

For problems asking for a minimum reachable label or representative, first condense strongly connected components into a directed acyclic graph. Compute component answers in reverse topological order, combining each component's own label with answers from outgoing neighbors.

## Answer Template

When answering a graph-search problem, use this order:

1. State graph direction, representation, and whether weights matter.
2. Choose the algorithm and name the precondition that makes it valid.
3. State the invariant or theorem hook.
4. Give the running time in a display block after naming the representation.
5. Name what is order-dependent and what is invariant under adjacency-list order.
6. Include production caveats for representation choices, ids, attributes, and adversarial lookup assumptions.

## Replayable Pressure Pattern

Use this small directed graph to test edge classification and finish-time reasoning. Vertices are considered in alphabetical order, and each adjacency list is in the order shown.

```
A: B, C
B: D
C: D
D: B
E: C
```

Required reasoning:

- The first WHITE target reached from a vertex is a tree edge.
- The edge from `D` to `B` is back because `B` is gray while `D` is active.
- The edge from `C` to `D` is cross if `D` has already finished before `C` explores it.
- The second depth-first tree rooted at `E` can create a cross edge to an already finished component of the forest.

Use this pattern to catch the false claim that a WHITE target can be a cross edge, and to catch answers that classify BLACK targets without timestamps.

## RED Pressure Failures This Skill Prevents

- Treating a WHITE target in depth-first search as a possible cross edge.
- Classifying BLACK targets without interval or discovery-order reasoning.
- Saying undirected depth-first search has forward or cross edges.
- Claiming every topological-sort edge target becomes a descendant.
- Explaining strongly connected components only with vague source or sink language instead of the finish-time component argument.
- Forgetting that adjacency-matrix breadth-first search scans rows and therefore has quadratic traversal cost.
- Treating breadth-first predecessor trees as unique when adjacency-list order is unspecified.
- Choosing hash-backed adjacency lists without naming memory, determinism, iteration locality, and adversarial hashing tradeoffs.
- Leaking inline formulas in CLRS answers, especially inside tables.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Giving a running time before naming the representation | State adjacency lists, adjacency matrix, or augmented adjacency structure first |
| Using breadth-first search for weighted shortest paths | Switch to an algorithm whose preconditions match the weights |
| Treating predecessor trees as unique | Say distances are stable, parents are order-dependent |
| Calling a WHITE depth-first target cross | WHITE target means tree edge |
| Using a gray target in topological sort | A gray target is a back edge, so the graph is not a directed acyclic graph |
| Explaining strongly connected components by intuition only | Use component finish-time order and transpose no-leakage |
| Putting formulas in table cells | Keep tables verbal and put formulas in display blocks nearby |

## Verification Pressure Tests

- Ask for breadth-first search on a graph with two different neighbor orders. The answer must keep distances fixed while allowing different parents.
- Ask for directed depth-first edge classification with WHITE, GRAY, and BLACK targets. The answer must say WHITE means tree and must use intervals for BLACK targets.
- Ask why decreasing finish time topologically sorts a directed acyclic graph. The answer must handle both WHITE and BLACK target cases.
- Ask why the second pass of the strongly connected components algorithm cannot leak into a different unvisited component. The answer must cite the component finish-time ordering and transpose argument.
- Ask whether an adjacency matrix is appropriate for a sparse production graph with frequent edge-existence queries. The answer must weigh memory against lookup needs and mention augmented adjacency alternatives.
- Ask for a production representation with sparse graph storage, frequent membership tests, deterministic full-neighbor scans, weighted edges, and external vertex ids. The answer must discuss hybrid list-plus-lookup designs, synchronization cost, id resolution, and edge records.
- Ask for an answer under the parent CLRS formatting rule. The answer must not place formulas in prose, headings, tables, or inline code spans.

## Static Checks

- Frontmatter name matches the directory slug.
- Description begins with `Use when` and names concrete triggers.
- The parent `clrs` router has a bullet for this chapter skill.
- Bounds and inequalities appear only in display LaTeX blocks.
- Tables contain verbal guidance, not formula expressions.
- The skill contains no narrative session log or source-conversion diary.
- Scan generated answers for inline math delimiters, asymptotic expressions in prose, inequalities in code spans, and formulas inside table cells before accepting GREEN results.
