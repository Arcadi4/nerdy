---
name: data-structures-for-disjoint-sets
description: Use when disjoint sets, union-find, dynamic connectivity, connected components, weighted union, union by rank, path compression, inverse Ackermann bounds, linked-list set representations, offline minimum, or offline LCA reasoning appears.
license: MIT
---

# Data Structures for Disjoint Sets

## Overview

Use this skill to keep disjoint-set answers honest about representatives, handles, sequence bounds, and offline metadata. The key behavior change is to separate the abstract partition contract from representation choices: linked lists, forests, rank, path compression, and application-specific metadata all have different invariants.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting and proof tone. In this chapter skill, operation names such as `MAKE-SET`, `UNION`, and `FIND-SET` may appear in code spans, but all mathematical bounds and symbolic definitions must be displayed in LaTeX blocks, not placed in prose, headings, inline code, or Markdown tables.

## When to Use

Use this skill for:

- Union-find or disjoint-set APIs, including `makeSet`, `find`, `union`, and `sameComponent`.
- Dynamic connectivity where edges only accumulate and components are queried.
- Explaining why a representative is arbitrary unless the API explicitly stores separate canonical metadata.
- Comparing linked-list and forest representations.
- Analyzing weighted union, union by rank, path compression, and inverse-Ackermann amortized bounds.
- Offline algorithms that use disjoint sets as a bookkeeping layer: connected components, offline minimum, depth determination with pseudodistances, and Tarjan offline lowest common ancestors.

Do not use it for fully dynamic graph connectivity with deletions, online minimum extraction, or online LCA queries unless the answer explicitly says the chapter technique is not sufficient by itself.

## Quick Reference

| Topic | Use it to decide | Required contract |
| --- | --- | --- |
| Abstract disjoint sets | Whether the problem only needs partition membership | `FIND-SET` returns a stable representative only while the set is unchanged |
| Connected components | Whether edges are only added before queries | Initialize every vertex, union endpoints, compare representatives |
| Linked-list sets | Whether constant-time find is worth expensive unions | Every element has a back-pointer to the set object |
| Weighted union on lists | Whether sequence cost matters more than one union | Append the shorter list to the longer list and update moved back-pointers |
| Disjoint-set forests | Whether tree roots can represent sets | Parent pointers form rooted trees; roots point to themselves |
| Union by rank | Whether tree growth is controlled without path compression | Rank is history metadata and only increases on equal-rank root links |
| Path compression | Whether repeated finds should flatten search paths | `FIND-SET` rewrites parents on the path to the root |
| Offline minimum | Whether the full operation sequence is known | Process keys in increasing order through insertion-block sets |
| Offline LCA | Whether all tree queries are known before DFS | Answer a pair only when the other endpoint is black |

Use these bounds when the stated representation and heuristics match.

Linked-list simple union can take quadratic total time over the adversarial sequence:

$$
\Theta(n^2)
$$

Weighted union on linked lists gives the sequence bound:

$$
O(m + n \lg n)
$$

Union by rank alone on forests gives the sequence bound:

$$
O(m \lg n)
$$

Union by rank with path compression gives the sequence bound:

$$
O(m\alpha(n))
$$

## API and Representative Contracts

Always state the partition contract before the implementation:

1. `MAKE-SET(x)` creates a singleton set and requires that `x` is not already present.
2. `FIND-SET(x)` requires that `x` already belongs to a set and returns the current representative of that set.
3. `UNION(x, y)` merges the two sets containing `x` and `y`; it is a no-op when they are already in the same set.
4. `SAME-COMPONENT(u, v)` is true exactly when the representatives returned by `FIND-SET` are identical.

The representative is a set identifier, not a semantic minimum, maximum, first insertion, display label, or leader. If a production API needs the smallest vertex ID, tenant ID, canonical account, or newest timestamp, store that value as separate metadata on the representative and maintain it during `UNION`; do not infer it from union by rank or path compression.

### Production Review Checklist

- Does the caller own element handles, dense IDs, or a map from application objects to nodes?
- Is the operation sequence insertion-only, or are deletions required?
- Is the requested representative semantic or merely an equality token?
- Are duplicate `MAKE-SET`, unknown-element `FIND-SET`, and same-set `UNION` specified?
- Is concurrent mutation possible, and if so, is synchronization outside the data structure contract?

## Linked-List Representation

Use linked lists to explain the back-pointer cost model, not as the default production implementation.

Representation:

- Each set object stores `head`, `tail`, and optionally `length`.
- Each element object stores the member value, `next`, and a back-pointer to its set object.
- `FIND-SET` follows the element's back-pointer.
- `UNION` appends one list to the other and updates every moved element's back-pointer.

The adversarial simple-union sequence must name which list moves. A bad sequence repeatedly appends the growing list into a singleton, so the moved-list sizes are:

$$
1, 2, 3, \ldots, n - 1
$$

Therefore the total number of back-pointer updates is:

$$
\sum_{i=1}^{n-1} i = \Theta(n^2)
$$

Weighted union fixes the sequence by always appending the shorter list to the longer list. An element's back-pointer changes only when the size of its containing set at least doubles, so any one element is moved at most:

$$
\lceil \lg n \rceil
$$

This improves the whole operation sequence even though one `UNION` can still move many elements.

## Forest Representation

Use disjoint-set forests when implementing union-find unless the prompt has a reason to discuss linked lists.

Core pseudocode pattern:

```text
MAKE-SET(x):
    x.p = x
    x.rank = 0

UNION(x, y):
    LINK(FIND-SET(x), FIND-SET(y))

LINK(x, y):
    if x == y:
        return x
    if x.rank > y.rank:
        y.p = x
        return x
    x.p = y
    if x.rank == y.rank:
        y.rank = y.rank + 1
    return y

FIND-SET(x):
    if x != x.p:
        x.p = FIND-SET(x.p)
    return x.p
```

Rank is not current height after path compression. Treat rank as historical upper-bound metadata that supports `LINK` decisions and the amortized proof. Nonroot ranks freeze; root ranks increase only on equal-rank links.

Required rank properties:

- Along any simple path toward a root, ranks strictly increase.
- Parent ranks monotonically increase over time.
- A node's rank never decreases.
- Path compression changes parents, not ranks.

## Invariant and Proof Recipes

### Weighted-Union List Proof

To prove the sequence bound, charge cost to elements whose back-pointers are updated.

1. An element moves only when its set is appended to another set.
2. Under weighted union, the destination set has size at least as large as the moved set.
3. After each move, the moved element belongs to a set at least twice as large as before.
4. Since no set grows beyond the total number of elements, each element moves logarithmically many times.

### Rank-Only Forest Proof

For union by rank without path compression, show that rank bounds height and that a rank increase requires two roots of equal rank. This gives logarithmic-height trees and logarithmic finds.

### Combined Heuristic Proof

For union by rank with path compression, do not replace the chapter proof with a generic "trees get flat" argument. Use the chapter-specific potential-method vocabulary:

- Define an inverse-Ackermann level for positive-rank nonroots.
- Track `level(x)` from the rank of `x.p` relative to Ackermann thresholds.
- Track `iter(x)` as the number of applications needed at the node's level to pass the parent rank.
- Assign zero potential to roots and rank-zero nodes.
- Assign bounded positive potential to nonroot positive-rank nodes.
- During `FIND-SET`, path compression raises parent ranks enough to pay for most traversed nodes through potential decrease.

The practical message can say the bound is effectively constant for real systems, but the formal statement remains inverse-Ackermann amortized time, not literal constant time.

## Worked Pattern: Offline Minimum

Use this pattern to prevent the common but wrong "segment minimum bubbling" explanation.

Given a known sequence of inserts and extracts, partition the inserts into the blocks below, where each extract follows the corresponding insertion block.

$$
I_1, I_2, \ldots, I_m, I_{m+1}
$$

Create a disjoint set for each block that still exists. Process inserted keys in increasing key order, not operation order.

For each key in increasing order:

1. Find the current block set containing the key.
2. If the block is not the final block, store the key as that block's extracted answer.
3. Destroy the current block set by unioning it with the next existing set to the right.
4. Make the representative metadata point to that next existing block index.

The representative metadata is a block index and successor pointer, not the minimum element in a live segment. This is an offline algorithm: it depends on knowing all inserted keys and all extract positions before the loop starts.

## Application Patterns

### Connected Components

For an undirected graph, initialize every vertex with `MAKE-SET`, union endpoints for each edge, then answer component equality by comparing representatives. Do not promise support for edge deletion; this chapter's DSU pattern handles incremental connectivity.

### Depth Determination with Path Compression

When maintaining depths in a forest with compressed paths, store a pseudodistance field that can be accumulated and rewritten during `FIND-SET`. The trap is updating only parent pointers and losing the distance contribution from skipped ancestors.

### Tarjan Offline Lowest Common Ancestors

Use one DFS over the rooted tree and answer only offline query pairs.

Pattern:

```text
LCA(u):
    MAKE-SET(u)
    FIND-SET(u).ancestor = u
    for each child v of u:
        LCA(v)
        UNION(u, v)
        FIND-SET(u).ancestor = u
    color[u] = BLACK
    for each query {u, v}:
        if color[v] == BLACK:
            answer {u, v} with FIND-SET(v).ancestor
```

The `ancestor` field is metadata stored on the representative after each union. The representative itself may be arbitrary; the algorithm is correct because the metadata is reset after each child union and because queries are answered only when the other endpoint has finished.

## RED Pressure Failures This Skill Prevents

- Claiming a union-find representative is the smallest vertex ID just because components need canonical labels.
- Calling `FIND-SET` true constant time when the precise result is amortized inverse-Ackermann time under both heuristics.
- Giving the linked-list quadratic example without saying the growing list is the moved list.
- Saying weighted union improves every individual `UNION`; it improves the sequence bound, not the worst single append.
- Inventing an offline-minimum algorithm based on segment minima, adjacent bubbling, or online extraction.
- Treating rank as current height after path compression or recomputing rank from the compressed tree.
- Giving a generic potential proof and omitting `level(x)` and `iter(x)` from the chapter analysis.
- Passing a proof-fidelity review by covering only the linked-list half while skipping rank, compression, and potential-method details.
- Leaking mathematical expressions into Markdown table cells or inline prose while explaining bounds.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Representative means smallest, first, or semantic leader | Representative is an equality token unless separate metadata is maintained |
| `UNION` receives roots and arbitrary elements interchangeably | Public `UNION` should call `FIND-SET`; low-level `LINK` receives roots |
| Path compression alone justifies the full bound | The chapter's strongest bound needs both union by rank and path compression |
| Rank is size or current height | Rank is historical upper-bound metadata used for linking and proof |
| Linked-list weighted union is always fast per operation | A single append can still be linear; the sequence is controlled |
| Offline minimum is a heap simulation | It is a key-order sweep over insertion-block sets and successor blocks |
| Tarjan LCA answers as soon as one endpoint is discovered | Answer only when the other endpoint is black |
| Proof review covers only linked-list unions | A complete chapter proof review must also cover rank monotonicity, path compression, `level(x)`, and `iter(x)` |
| Formula appears in a quick-reference table | Keep table cells verbal and place formulas in display blocks nearby |

## Verification Pressure Tests

Ask future agents to pass these checks after loading this skill:

1. Design a graph component service that asks for smallest-ID component labels. The answer must separate DSU representatives from canonical-label metadata and must state the formal amortized bound in a display block.
2. Analyze linked-list `UNION` without weighted union. The answer must replay the sequence where the growing list is appended into a singleton and must count moved back-pointers.
3. Explain weighted union on lists. The answer must say each moved element's containing set at least doubles and must not claim every `UNION` is logarithmic.
4. Describe offline minimum. The answer must partition inserts into blocks, process keys in increasing order, destroy the current block set, and union with the next existing block.
5. Explain Tarjan offline LCA. The answer must use black nodes, representative `ancestor` metadata, and post-child union reset.
6. Review a rank/path-compression proof. The answer must mention rank monotonicity, frozen nonroot ranks, `level(x)`, `iter(x)`, and display all formulas outside tables and prose. A response that only analyzes linked-list unions fails this pressure test.

Static checks for this skill:

- Frontmatter has `name`, `description`, and `license`.
- The description starts with "Use when" and contains searchable triggers for disjoint sets, union-find, connected components, rank, path compression, inverse Ackermann, offline minimum, and offline LCA.
- All mathematical expressions are in display LaTeX blocks, never headings, inline prose, inline code, or Markdown tables.
- The chapter-specific algorithms stay in this child skill; the parent `clrs` skill only routes to it.
- No construction-history narrative appears.
- No supporting files are required.
