---
name: shortest-paths
description: Use when solving, proving, implementing, or reviewing weighted shortest-path problems, including single-source or all-pairs shortest paths, relaxation, negative edges or cycles, Dijkstra, Bellman-Ford, DAG paths, Floyd-Warshall, Johnson, difference constraints, transitive closure, arbitrage, or graph-path reductions.
license: MIT
---

# Shortest Paths

## Overview

Shortest-path answers are decision problems before they are algorithm names. First identify the path model, weight assumptions, graph representation, negative-cycle semantics, and whether the caller needs distances, predecessor trees, actual paths, or cycle witnesses.

**Core principle:** choose the algorithm whose preconditions match the weights and graph shape, prove correctness with relaxation, dynamic-programming decomposition, or reweighting, then state the production contract for representation, sentinels, overflow, and reconstruction.

## Shared CLRS Conventions

- Follow the parent `clrs` skill for mathematical formatting: every expression, inequality, recurrence, path weight, and asymptotic bound goes in a display LaTeX block, never in prose, headings, tables, or inline code spans.
- Use `elementary-graph-algorithms` for graph representation basics, breadth-first search on unweighted graphs, depth-first search, topological sorting, and transitive-reachability prerequisites.
- State whether the graph is directed or undirected before choosing a shortest-path algorithm. A negative undirected edge creates an immediate negative cycle under the directed-edge model unless the problem defines a different semantics.
- State the representation before giving a running time. Adjacency lists fit single-source and Johnson-style sparse algorithms; adjacency matrices fit dense all-pairs dynamic programs.
- Do not announce that you are reading this skill or applying a checklist. Deliver the polished answer directly.

## When to Use

Use this skill for:

- Weighted single-source shortest paths, single-destination reductions, single-pair questions, and all-pairs shortest paths.
- Choosing among breadth-first search, DAG shortest paths, Bellman-Ford, Dijkstra, Floyd-Warshall, Johnson, repeated single-source runs, or min-plus matrix products.
- Negative-edge and negative-cycle questions, including which vertices have finite distance, infinite distance, or unbounded-below distance.
- Relaxation invariants, predecessor subgraphs, shortest-path trees, path reconstruction, and output verification.
- Difference constraints, arbitrage detection, reliability paths, critical paths in acyclic project networks, bitonic-path exercises, and other graph-path reductions.
- Production reviews where the textbook algorithm must be translated into an API contract, library choice, graph representation, memory budget, or cycle-reporting behavior.

Do **not** use this skill as the main tool for unweighted graph traversal unless the task asks how breadth-first search is a shortest-path algorithm. Do not use it for minimum spanning trees, maximum flow, matching, or longest simple paths in general graphs unless the prompt asks why a shortest-path proof does not transfer.

## First Decision: Match the Model Before Naming the Algorithm

| Problem shape | Use | Required precondition | Main proof hook |
| --- | --- | --- | --- |
| Unweighted shortest paths from one source | Breadth-first search | Edge count is the metric | Layer monotonicity |
| Weighted directed acyclic graph | Topological-order relaxation | Graph is acyclic | Shortest path follows topological order |
| Negative edges from one source | Bellman-Ford | No relevant negative cycle for finite answers | Path-relaxation property |
| Nonnegative edges from one source | Dijkstra | Every edge weight is nonnegative | Extract-min finalization |
| Dense all-pairs shortest paths | Floyd-Warshall | No negative cycles for finite distances | Allowed-intermediate dynamic program |
| Sparse all-pairs with negative edges | Johnson | Bellman-Ford finds no negative cycle | Potential reweighting preserves path order |
| Need reachability only | Transitive closure | Boolean paths, not weights | Boolean intermediate-vertex dynamic program |
| Pairwise bound feasibility | Difference-constraint graph | Constraints are difference bounds | Triangle inequality plus negative-cycle contradiction |
| Multiplicative gain cycle | Negative logarithm reduction | Rates are positive | Product above one becomes negative cycle |
| Critical path in an acyclic network | Longest path in a DAG | Project graph is acyclic | Reverse comparison or negate weights |

Keep symbolic bounds outside the table. Common running-time labels are below.

$$
\Theta(V+E)
$$

$$
O(VE)
$$

$$
O((V+E)\lg V)
$$

$$
\Theta(V^3)
$$

$$
O(V^2\lg V+VE)
$$

## Output Contract Checklist

Before answering or implementing, pin down:

1. **Distance domain:** finite real values, infinity for unreachable vertices, and unbounded-below markers for vertices affected by reachable negative cycles.
2. **Path output:** value only, one shortest path, all shortest paths, predecessor tree per source, predecessor matrix, or negative-cycle witness.
3. **Tie behavior:** shortest paths and predecessor trees need not be unique; deterministic output requires a tie-breaker.
4. **Graph representation:** adjacency lists, adjacency matrix, edge list, or hybrid lookup structure.
5. **Sentinels:** distinguish absent edges from zero-weight edges, infinity from large finite values, and unbounded-below from ordinary finite negative values.
6. **Arithmetic safety:** potentials, distance additions, and logarithm transforms must not silently overflow, underflow, or lose required ordering.

## Relaxation Framework

Single-source algorithms maintain an estimate and predecessor for each vertex. Initialization sets every estimate to infinity and every predecessor to NIL, then sets the source estimate to zero. Relaxation of an edge updates the target only when the path through the edge improves the current estimate.

The relaxation inequality is below.

$$
v.d > u.d + w(u,v)
$$

The update is below.

$$
v.d = u.d + w(u,v)
$$

The predecessor update is below.

$$
v.\pi = u
$$

Use these proof hooks:

- **Triangle inequality:** for any edge, the true shortest-path weight to the target is at most the true shortest-path weight to the source plus the edge weight.
- **Upper-bound property:** estimates never drop below true shortest-path weights; once an estimate becomes exact, it remains exact.
- **No-path property:** an unreachable vertex keeps infinity.
- **Convergence property:** if the predecessor on a shortest path already has the correct estimate, relaxing the next edge makes the target correct forever.
- **Path-relaxation property:** relaxing the edges of a shortest path in order makes the destination estimate correct, regardless of other interleaved relaxations.
- **Predecessor-subgraph property:** once all reachable estimates are exact, predecessor edges form a shortest-paths tree rooted at the source.

For subpath proofs, decompose a shortest path into prefix, middle subpath, and suffix. If the middle subpath were not shortest, replacing it by a lighter subpath would improve the whole path and contradict optimality.

## Negative-Cycle Semantics

Shortest-path weights are well-defined only for destinations not downstream of a reachable negative-weight cycle. Distinguish four cases:

- If a vertex is unreachable from the source, its distance is infinity even when it lies on a negative cycle disconnected from the source.
- If a vertex is reachable from the source and no reachable negative cycle can reach it, its shortest-path weight is finite.
- If a reachable negative cycle can reach a vertex, the shortest-path weight is unbounded below.
- If the task is all-pairs, apply the same reachability condition separately for each source and destination pair.

Use the marker below only for vertices downstream of a reachable negative cycle.

$$
-\infty
$$

Do not reconstruct ordinary predecessor paths through unbounded-below vertices. Predecessor chains may cycle or fail to represent a finite shortest path. If the API reports affected vertices, propagate the marker from vertices relaxed on the detection pass to all vertices reachable from them.

## Bellman-Ford

Use Bellman-Ford for single-source shortest paths with negative edges and for negative-cycle detection reachable from the source.

Algorithm:

1. Initialize estimates and predecessors from the source.
2. Repeat the edge-relaxation pass enough times for every edge of any simple shortest path to have appeared in order.
3. Scan every edge once more.
4. If any edge can still relax, report a reachable negative-weight cycle.
5. Otherwise, the estimates and predecessor tree are correct for all reachable vertices.

The pass count for simple shortest paths is below.

$$
|V|-1
$$

The standard edge-list running time is below.

$$
O(VE)
$$

Correctness uses path relaxation: when no reachable negative cycle affects a destination, some simple shortest path has at most the number of edges above, so repeated full passes eventually relax its edges in order. The final scan proves there is no reachable negative cycle because a cycle whose every edge refuses relaxation cannot have negative total weight after summing the edge inequalities.

Implementation notes:

- Early termination after a pass with no changes is safe.
- To output one negative cycle, follow predecessor pointers from a relaxable vertex enough times to enter the cycle, then walk predecessors until the vertex repeats.
- To mark unbounded-below vertices, start from vertices still relaxable after the main passes and search forward in the original graph.
- Bellman-Ford returning failure means a negative cycle reachable from the chosen source; it is not a generic proof that every vertex has unbounded-below distance.

## DAG Shortest and Longest Paths

Use topological-order relaxation for weighted directed acyclic graphs, including graphs with negative edges. Cycles are absent, so negative cycles are impossible.

Algorithm:

1. Topologically sort the graph.
2. Initialize estimates and predecessors from the source.
3. Process vertices in topological order.
4. Relax every outgoing edge of each processed vertex once.

The running time with adjacency lists is below.

$$
\Theta(V+E)
$$

The proof is the path-relaxation property plus the fact that every path in a directed acyclic graph respects topological order. For critical paths or project scheduling, either negate weights and run shortest paths in the acyclic graph, or initialize longest-path estimates to negative infinity and reverse the relaxation comparison.

## Dijkstra

Use Dijkstra only when every edge weight is nonnegative, or when a specialized problem has been proven to preserve the extract-min finalization invariant. The ordinary algorithm finalizes vertices in nondecreasing estimate order and relaxes outgoing edges from each extracted vertex.

Required invariant:

1. The finalized set contains only vertices whose estimates equal true shortest-path weights.
2. The priority queue contains all unfinalized vertices keyed by their current estimates.
3. Extracting the minimum-key vertex is safe because a shortest path to it cannot become cheaper through an unfinalized vertex when every edge is nonnegative.

The array-based bound is below.

$$
O(V^2+E)
$$

The binary-heap bound is below.

$$
O((V+E)\lg V)
$$

The Fibonacci-heap bound is below.

$$
O(V\lg V+E)
$$

Do not use Dijkstra merely because there is only one negative edge. A later negative edge can make a previously finalized vertex cheaper, and the algorithm will silently return a plausible wrong answer. If an exercise asks about a special source-only negative-outgoing case, prove why the negative edge cannot point from an unfinalized region back into a finalized one before relying on Dijkstra-style finalization.

Production notes:

- Binary heaps with duplicate stale entries are often simpler than true decrease-key; state the stale-entry policy.
- Fibonacci heaps are usually a theorem-bound reference, not a default production implementation.
- Integer weights with small ranges may justify buckets or radix-style queues only when range, memory, and monotonicity assumptions are real.
- If path output is required, store predecessors during successful relaxations.

## All-Pairs Dynamic Programs

Use adjacency matrices for dense all-pairs algorithms. The matrix entry for a missing edge is infinity; diagonal entries are zero unless the problem explicitly asks to diagnose negative cycles.

### Min-Plus Path-Length Dynamic Program

The path-length dynamic program lets an entry store the best path using at most a bounded number of edges. Its recurrence is a min-plus matrix product: ordinary addition becomes minimization, ordinary multiplication becomes addition, zero is the multiplicative identity, and infinity is the additive identity.

Base case:

$$
l_{ij}^{(0)}=\begin{cases}0&\text{if }i=j,\\ \infty&\text{otherwise.}\end{cases}
$$

Recurrence:

$$
l_{ij}^{(r)}=\min_{1\le k\le n}\left(l_{ik}^{(r-1)}+w_{kj}\right)
$$

With no negative cycles, simple shortest paths use at most the number of edges below.

$$
n-1
$$

The slow version computes each edge budget in sequence and runs in:

$$
\Theta(n^4)
$$

Repeated squaring uses min-plus associativity and runs in:

$$
\Theta(n^3\lg n)
$$

This method is mostly useful for understanding the dynamic-programming structure or for specialized min-plus acceleration, not as the everyday dense APSP default.

### Floyd-Warshall

Use Floyd-Warshall for dense all-pairs shortest paths when the graph may have negative edges but no negative cycles. The state allows only intermediate vertices drawn from a growing prefix of the vertex order.

Base matrix:

$$
D^{(0)}=W
$$

Recurrence:

$$
d_{ij}^{(k)}=\min\left(d_{ij}^{(k-1)},\ d_{ik}^{(k-1)}+d_{kj}^{(k-1)}\right)
$$

The running time is below.

$$
\Theta(n^3)
$$

The in-place version uses only the distance matrix and the space below, because the recurrence for phase k can overwrite entries without invalidating that phase.

$$
\Theta(n^2)
$$

Detect a negative cycle by inspecting the final diagonal. A negative diagonal entry means some vertex can reach itself with negative total weight.

For paths, maintain a predecessor matrix or a split matrix. If a shorter route through the current intermediate vertex improves the distance, set the predecessor of the destination on the new path to the predecessor from the intermediate vertex to that destination. When equality occurs, keep or change the predecessor only according to a declared tie policy.

## Johnson for Sparse All-Pairs Shortest Paths

Use Johnson for sparse all-pairs shortest paths with negative edges and no negative cycles. It combines one Bellman-Ford run with one Dijkstra run from each original vertex.

Algorithm:

1. Add a fresh artificial source with zero-weight edges to every original vertex.
2. Run Bellman-Ford from the artificial source.
3. If Bellman-Ford reports a negative cycle, abort and report that all-pairs shortest paths are not well-defined.
4. Use the Bellman-Ford distances as vertex potentials.
5. Reweight every original edge using those potentials.
6. Run Dijkstra from each original vertex on the reweighted graph.
7. Convert each reweighted distance back to the original distance.
8. Store a predecessor row from each Dijkstra run if paths are required.

The reweighting formula is below.

$$
\widehat{w}(u,v)=w(u,v)+h(u)-h(v)
$$

The path telescoping identity is below.

$$
\widehat{w}(p)=w(p)+h(v_0)-h(v_k)
$$

The conversion back to original distances is below.

$$
d(u,v)=\widehat{d}(u,v)+h(v)-h(u)
$$

The Fibonacci-heap bound is below.

$$
O(V^2\lg V+VE)
$$

The binary-heap bound is below.

$$
O(VE\lg V)
$$

Why it works:

- The artificial source makes every potential finite, even when the original graph is not strongly connected.
- Triangle inequality from Bellman-Ford makes every reweighted edge nonnegative.
- For fixed endpoints, every path receives the same endpoint-dependent shift, so path ordering and shortest-path identity are preserved.
- Cycle weights are unchanged by telescoping, so negative cycles are preserved and detected before Dijkstra runs.

Wrong shortcuts to reject:

- Do not run Dijkstra from every source on the original graph when any negative edge remains.
- Do not use an arbitrary original source for potentials; unreachable vertices would create unusable infinite potentials.
- Do not subtract the global minimum edge weight from every edge; paths with different numbers of edges shift by different amounts.
- Do not store only the distance matrix when the caller asked for actual paths.
- Do not skip Bellman-Ford because negative cycles are merely “not expected.”

## Difference Constraints

Use this reduction for systems where each constraint bounds the difference between two variables. It is a feasibility reduction, not a general linear-programming solver.

Constraint form:

$$
x_j-x_i\le b_k
$$

Equivalent upper-bound form:

$$
x_j\le x_i+b_k
$$

Create the edge below.

$$
(v_i,v_j)\text{ with weight }b_k
$$

Add an artificial source with zero-weight edges to every variable vertex, run Bellman-Ford, and interpret success as a feasible assignment.

The assignment is below.

$$
x_i=\delta(v_0,v_i)
$$

The proof of feasibility is the triangle inequality on each constraint edge. The proof of infeasibility sums constraints around a negative cycle: the left sides telescope to zero while the right sides sum to a negative value, a contradiction.

Adding the same constant to every variable preserves feasibility because every difference is unchanged. If all bounds are integers, the shortest-path assignment from integer edge weights is integral. If the prompt asks for equalities, model each equality as two opposite inequalities.

## Transitive Closure and Reachability

Use transitive closure when the question asks whether a path exists, not what it weighs. The Floyd-Warshall analogue replaces minimization and addition with boolean OR and AND.

Base relation:

$$
t_{ij}^{(0)}=1\quad\text{if }i=j\text{ or }(i,j)\in E
$$

Recurrence:

$$
t_{ij}^{(k)}=t_{ij}^{(k-1)}\lor\left(t_{ik}^{(k-1)}\land t_{kj}^{(k-1)}\right)
$$

For sparse adjacency-list graphs, running breadth-first or depth-first search from each vertex may be a better representation-level choice. For dynamic edge insertions, update only pairs whose old reachability can now pass through the inserted edge.

## Reduction Patterns

| Problem | Reduction | Required caution |
| --- | --- | --- |
| Single destination | Reverse all edges and run single-source from the destination | Preserve directed edge semantics |
| Reliability path | Turn products into sums with logarithms | Probabilities must be positive and path ordering must be preserved |
| Arbitrage | Turn exchange-rate products into cycle weights | A profitable product becomes a negative cycle |
| Critical path | Longest path in a directed acyclic graph | General longest simple path is not the same problem |
| Box nesting | Sort dimensions and build an acyclic dominance graph | Strict nesting and dimension order must be explicit |
| Minimum mean cycle | Dynamic program by exact edge count | Average cycle objective is not ordinary shortest path |
| Bitonic shortest paths | Exploit sorted unique edge weights and bitonic promise | Do not assume arbitrary shortest paths are bitonic |

For arbitrage with positive exchange rates, use the transform below and report the negative cycle as the trade loop.

$$
w(u,v)=-\lg r(u,v)
$$

## Path Reconstruction

Distances alone do not produce paths. Choose reconstruction metadata deliberately:

- For single-source algorithms, a predecessor pointer per vertex reconstructs one path from the source to a reachable destination.
- For all-pairs algorithms, a predecessor matrix stores the predecessor of each destination on a path from each source.
- For Floyd-Warshall, a split matrix storing an intermediate vertex can recursively reconstruct the path instead of storing predecessors.
- For Johnson, store each Dijkstra predecessor row in original vertex names; the reweighted graph preserves the shortest-path structure.
- For unreachable destinations, predecessors remain NIL and path printing must report no path.
- For unbounded-below destinations, path printing must not chase predecessor cycles as if they were finite shortest paths.

Shortest-path trees need not be unique. Adjacency order, priority-queue tie behavior, and equality-handling in dynamic programs can change predecessor choices while preserving distances.

## Answer Template

When solving a shortest-path prompt, structure the answer as follows:

1. **Model:** directed or undirected graph, weighted or unweighted metric, representation, and whether negative edges or cycles are possible.
2. **Output:** distances only, paths, predecessor tree or matrix, reachability matrix, or cycle witness.
3. **Algorithm choice:** name the algorithm only after stating the precondition that makes it valid.
4. **Invariant or recurrence:** relaxation invariant, topological path order, extract-min finalization, intermediate-vertex dynamic program, or potential reweighting.
5. **Negative-cycle semantics:** say which vertices or pairs are finite, unreachable, or unbounded below.
6. **Complexity:** state representation and priority-queue choice before the displayed bound.
7. **Production contract:** sentinels, overflow, tie behavior, path reconstruction, memory shape, and library-vs-handrolled judgment.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Choosing the right headline algorithm but leaking inline formulas and table formulas | Keep tables verbal and move all symbolic expressions to display LaTeX blocks |
| Saying Bellman-Ford handles negative cycles without downstream reachability semantics | Mark only vertices reachable from a reachable negative cycle as unbounded below |
| Treating unreachable vertices on unrelated negative cycles as unbounded below | Keep them at infinity for that source |
| Recommending Dijkstra when only one edge is negative | Reject Dijkstra unless a special invariant is proven |
| Storing only all-pairs distances when paths are requested | Store predecessor rows, predecessor matrix, or split matrix |
| Explaining Johnson with a vague reweighting intuition | Include the artificial source, finite potentials, nonnegative reweighted edges, telescoping identity, and distance conversion |
| Using an arbitrary original source for Johnson potentials | Add a fresh source with zero-weight edges to every vertex |
| Subtracting the global minimum edge weight to remove negative edges | Reject it because path lengths with different edge counts shift differently |
| Mapping difference constraints with uncertainty about edge direction | Create the edge from the subtracted variable to the bounded variable |
| Proving difference-constraint infeasibility only by intuition | Sum constraints around the negative cycle and show the telescoping contradiction |
| Forgetting constant-shift and integer-solution facts for difference constraints | State that adding a constant preserves feasibility and integer bounds yield integer distances |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Using breadth-first search for weighted paths | Use breadth-first search only when edge count or unit weight is the metric |
| Using Dijkstra with negative edges | Use Bellman-Ford, DAG relaxation, or Johnson reweighting when preconditions fit |
| Saying any negative cycle invalidates every shortest-path answer | Check reachability from the source and reachability from the cycle to the destination |
| Assuming shortest paths are always simple | Remove cycles only when no relevant negative cycle exists; zero cycles can be removed without changing weight |
| Treating predecessor subgraphs as arbitrary shortest-path choices | Predecessors produced by relaxation have stronger acyclicity properties when no reachable negative cycle exists |
| Ignoring equality tie behavior in predecessor updates | Declare whether equal alternatives keep old predecessors or replace them |
| Calling Floyd-Warshall sparse-friendly | It is a dense matrix dynamic program unless the graph size and simplicity justify it |
| Calling Johnson path-preserving without proof | Use the endpoint-constant telescoping argument |
| Forgetting the artificial source in difference constraints or Johnson | Add it so every variable or vertex is reachable and potentials are finite |
| Returning values when the prompt asks for paths | Add reconstruction metadata and edge-case behavior |

## Red Flags

Stop and repair the answer if it contains any of these:

- An inline formula, inequality, recurrence, asymptotic bound, or path-weight expression in prose, a heading, a table cell, or an inline code span.
- Dijkstra recommended before all edge weights are confirmed nonnegative.
- “Negative cycle” reported without saying reachable from which source and which destinations are affected.
- Johnson described without the fresh artificial source or without converting distances back.
- Floyd-Warshall selected for a sparse production graph without justifying the memory and cubic-time tradeoff.
- A path-output answer with no predecessor, split, or parent metadata.
- A difference-constraint edge direction not derived from the upper-bound form.
- A complexity bound stated before graph representation and priority-queue choice.

## Verification Pressure Tests

Use these prompts to verify the skill changes future answers:

1. **Sparse all-pairs with negative edges:** For a sparse directed graph with negative edges, no expected negative cycles, and required path reconstruction, choose the algorithm, state preconditions, reject shortcuts, and keep formulas out of tables and prose.
2. **Negative-cycle reachability:** From a source that reaches one negative cycle but not another, classify ordinary reachable vertices, vertices downstream of the reachable cycle, and vertices unreachable from the source.
3. **Dijkstra trap:** Give a graph with one negative edge where Dijkstra finalizes a vertex too early, then explain why the nonnegative-edge proof fails.
4. **Difference constraints:** Convert a bound on one variable difference into a graph edge, run Bellman-Ford from the artificial source, and prove infeasibility by summing a negative cycle.
5. **Dense all-pairs reconstruction:** Use Floyd-Warshall with a predecessor or split matrix, state negative-diagonal detection, and specify equality-tie behavior.
6. **Reduction judgment:** Detect arbitrage via a logarithm transform, or solve critical paths in a directed acyclic graph, while refusing to generalize to arbitrary longest simple paths.
7. **Formatting fidelity:** Produce a shortest-path decision table whose cells contain only prose, then put every formal expression and bound in display LaTeX blocks outside the table.

## Static Checks

- `SKILL.md` lives at `clrs/shortest-paths/SKILL.md`.
- Frontmatter name is `shortest-paths`, description starts with `Use when`, and license is `MIT`.
- The parent `clrs` router has a bullet for this chapter skill.
- The skill references the parent `clrs` conventions instead of duplicating the full parent style contract.
- Markdown tables contain verbal guidance only; symbolic formulas and bounds appear in display LaTeX blocks outside tables.
- Headings use generalized concept names rather than source-branded chapter labels.
- The text distinguishes textbook mechanisms from production judgment about libraries, memory, sentinels, overflow, and reconstruction.
- RED failures are represented as explicit corrections, and verification prompts pressure the same failure modes.
