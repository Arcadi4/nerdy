---
name: clrs
description: Use when working with CLRS, Introduction to Algorithms by Cormen, Leiserson, Rivest, and Stein, including algorithm design, data structures, asymptotic analysis, recurrences, proof style, or textbook-grounded algorithm explanations.
license: MIT
---

# Introduction to Algorithms

## When to Use

Use this skill when you need to understand, implement, or analyze an algorithm-intensive problem, choose an algorithmic technique, reason about a sophisticated data structure, or answer a CLRS-style exercise.

## CLRS Skill Selection

1. Identify the problem being solved and the CLRS concept it most closely matches.
2. If the user mentions a chapter topic directly, load the matching chapter skill.
3. If the topic is inferred rather than named, map the problem to likely CLRS techniques before choosing a chapter skill.
4. Use chapter skills for chapter-specific facts, examples, theorem details, and common traps.
5. Keep the index skill for shared CLRS answer style and routing; do not store chapter-specific algorithms or theorem catalogs here.

Current chapter skills:

- `characterizing-running-times`: asymptotic notation, running-time bounds, growth-rate comparisons, and loop-bound reasoning.
- `divide-and-conquer`: recurrences, recursion trees, substitution, Master theorem, Akra-Bazzi, and divide-and-conquer matrix multiplication.
- `elementary-data-structures`: dynamic sets, arrays, matrices, stacks, queues, linked lists, sentinels, rooted trees, representation invariants, and pointer/locality tradeoffs.
- `elementary-graph-algorithms`: graph representations, adjacency lists, adjacency matrices, breadth-first search, depth-first search, topological sorting, strongly connected components, edge classification, reachability, articulation points, bridges, biconnected components, and Euler tours.
- `data-structures-for-disjoint-sets`: disjoint sets, union-find, linked-list and forest representations, weighted union, union by rank, path compression, connected components, offline minimum, and offline LCA.
- `hash-tables`: direct addressing, chaining, open addressing, universal hashing, load factors, deletion behavior, probe bounds, and cache-aware dictionary design.
- `b-trees`: external-memory search trees, disk-block indexes, B-tree height bounds, node splitting, top-down insertion, deletion rebalancing, and 2-3-4 tree join/split reasoning.
- `augmenting-data-structures`: augmented red-black trees, order-statistic trees, rank/select queries, interval trees, overlap search, maintained metadata, and augmentation theorem preconditions.
- `binary-search-trees`: ordered dynamic sets, predecessor and successor navigation, BST deletion and transplant, red-black rotations and balancing invariants, and production ordered-container choices.
- `dynamic-programming`: optimal substructure, overlapping subproblems, memoization, bottom-up tables, reconstruction, rod cutting, matrix-chain multiplication, LCS, optimal BSTs, and DP production tradeoffs.
- `amortized-algorithms`: aggregate analysis, accounting credits, potential functions, multipop stacks, binary counters, dynamic tables, resizing policies, and amortized-versus-average-case traps.
- `greedy-algorithms`: greedy-choice property, exchange arguments, activity selection, fractional knapsack, Huffman coding, offline caching, and greedy-versus-DP traps.
- `minimun-spanning-trees`: minimum spanning trees, safe edges, cut and cycle properties, Kruskal's algorithm, Prim's algorithm, bottleneck trees, second-best trees, and MST update reasoning.
- `probabilistic-analysis-and-randomized-algorithms`: probabilistic analysis, indicator random variables, randomized algorithms, random permutations, balls-and-bins, birthday paradox, streaks, and online hiring.
- `parallel-algorithms`: fork-join task parallelism, spawn and sync, serial projections, trace DAGs, work/span analysis, greedy scheduling, slackness, determinacy races, parallel loops, matrix multiplication, parallel merge sort, reductions, scans, stencils, and randomized parallel algorithms.
- `linear-programming`: linear-programming formulations, standard form, feasibility and boundedness, simplex intuition, graph and flow LPs, duality, weak and strong duality, Farkas certificates, complementary slackness, and integer-LP caveats.
- `matrix-operations`: linear systems, LU and LUP decomposition, pivoting, matrix inversion, symmetric positive-definite matrices, Schur complements, least-squares approximation, normal equations, pseudoinverses, tridiagonal systems, and numerical-stability tradeoffs.
- `polynomials-and-fft`: polynomial representations, point-value evaluation and interpolation, complex roots of unity, DFT and inverse DFT, FFT, convolution, FFT circuits, and modular exactness caveats.
- `shortest-paths`: single-source and all-pairs shortest paths, relaxation, negative edges and cycles, Bellman-Ford, DAG paths, Dijkstra, Floyd-Warshall, Johnson, difference constraints, transitive closure, arbitrage, and path reconstruction.
- `maximum-flow`: flow networks, residual networks, augmenting paths, cuts, Ford-Fulkerson, Edmonds-Karp, min-cut certificates, bipartite matching reductions, vertex capacities, and flow-model transformations.
- `matchings-in-biparite-graphs`: bipartite matching, augmenting paths, Hopcroft-Karp, stable marriage, Gale-Shapley, Hungarian assignment, feasible labels, equality subgraphs, and matching-specific proof certificates.
- `online-algorithms`: competitive analysis, online/offline comparisons, elevator and ski-rental hedging, move-to-front list update, online caching, randomized marking, and adversary models.
- `sorting-and-order-statistics`: heaps, priority queues, sorting choice, stability, linear-time sorting preconditions, selection, medians, quantiles, and top-k decisions.

## Mathematical Formatting

Always put mathematical expressions in display LaTeX blocks. Do not put formulas in inline code spans, inline math, or plain prose. Notation names such as O-notation, Theta-notation, or little-omega can appear in prose, but any expression, inequality, limit, recurrence, or growth comparison must be displayed as a block.

This applies to the entire response, including headings, scratch work, examples, thresholds, ratios, and explanatory narration. If a sentence would contain symbols such as variables, powers, inequalities, limits, or fractions, split the expression into a display block and refer to it from prose as "the expression above" or "the bound below." Do not leak scratch-work formulas in prose before the polished answer.

Start directly with the polished answer. Do not include planning paragraphs, scratch-work narration, or "I am checking" preambles; those are common places where formulas accidentally escape display blocks.

Never place formulas in Markdown headings. Use prose headings such as "First claim" or "Little-o check," then put the formula below the heading in a display block.

Forbidden patterns:

- A heading that embeds a formula.
- A prose sentence that embeds a ratio, limit, threshold, recurrence, or asymptotic relation.
- An inline code span that contains a formula or inequality.

Safe pattern:

```markdown
## First claim

The claim is true.

$$
\frac{f(n)}{g(n)} \to 0
$$

Therefore the first expression is little-o of the second expression.
```

## General CLRS Conventions

- State which case, model, or quantity is being analyzed before giving a bound or theorem result.
- Ground answers in CLRS terminology and theorem names when relevant; cite theorem numbers when the chapter skill provides them.
- Check theorem preconditions before applying a named result.
- Prefer precise tight bounds when justified, and say when only an upper or lower bound has been shown.
- Keep chapter-specific worked examples, algorithms, proof recipes, and common mistakes in the relevant chapter skill.
