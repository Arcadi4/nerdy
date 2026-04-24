---
name: augmenting-data-structures
description: Use when augmenting balanced trees or dynamic sets with maintained metadata, order-statistic trees, interval trees, rank/select queries, overlap search, red-black-tree augmentation theorems, or production choices around custom indexed structures.
license: MIT
---

# Augmenting Data Structures

## Overview

Augmenting a data structure is not "add a cached field and hope." The reusable move is to choose a base structure whose ordinary operations already fit the access pattern, add metadata whose dependencies are local enough to maintain, prove mutation updates preserve it, and only then design new queries that safely exploit it.

For production use, treat the textbook structures as proof patterns and API design warnings. Prefer mature ordered containers, database range indexes, exclusion constraints, or tested libraries unless the custom metadata and workload justify owning rotations, deletion, concurrency, persistence, and rebuild logic.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style. Keep identities, inequalities, bounds, and recurrence-like claims in display LaTeX blocks rather than inline prose.

## When to Use

Use this skill for:

- Designing or reviewing augmented dynamic sets, especially red-black trees with per-node metadata.
- Order-statistic trees, `OS-SELECT`, `OS-RANK`, select-by-rank, rank-by-handle, inversion counting, Josephus-style rank deletion, or multiset rank APIs.
- Interval trees, interval overlap search, booking conflict detection, rectangle sweep-line active sets, or endpoint-overlap reasoning.
- Applying the red-black-tree augmentation theorem and checking whether a candidate attribute is locally maintainable.
- Explaining why rotations can update metadata locally and why some metadata depends on ancestors instead.

Do **not** use this skill merely because code contains cached fields. Use ordinary implementation judgment unless the cache is maintained across dynamic-set mutations and participates in asymptotic query behavior or proof obligations.

## The Four-Step Augmentation Method

Use this as the default design and review checklist:

1. **Choose the underlying structure.** It should already support the ordering, search, insertion, deletion, and traversal pattern needed by the application.
2. **Choose the extra information.** Define exactly what each field means, including sentinel or empty-subtree values.
3. **Verify maintainability.** Show how every modifying operation updates the field without breaking the claimed bound, especially rotations and deletion moves.
4. **Develop the new operations.** Prove the query uses the metadata safely; do not assume pruning is safe because it is intuitive.

If any step is vague, stop. The augmentation is not ready for implementation review.

## First Decision: Should This Be a Custom Augmented Tree?

| Need | Prefer | Reason |
| --- | --- | --- |
| Exact lookup only | Hash table or existing dictionary | Augmented order adds complexity without value. |
| Ordered iteration plus rank/select | Existing order-statistic container if available; otherwise balanced tree with subtree counts | Rank needs maintained subtree cardinalities and duplicate semantics. |
| Time booking conflicts | Database constraint, range index, or interval library before custom tree | Transactions, persistence, and boundary semantics are often harder than overlap search. |
| One-off static interval queries | Sort, sweep line, segment tree, or static interval index | Dynamic deletion and rotations may be unnecessary. |
| Educational proof or specialized in-memory index | Custom augmented balanced tree | Only when invariants, tests, concurrency, and maintenance ownership are explicit. |
| External-memory or storage-engine index | B-tree-like or database-native structure | Pointer red-black trees do not model page, disk, or cache behavior. |

Before approving custom code, require explicit answers for interval openness, duplicate keys, object handles, iterator invalidation, concurrent writers, persistence, rebuilds after corruption, and test coverage for stale metadata.

For interval trees specifically, duplicate low endpoints require a deterministic secondary ordering or bucket policy. Equal low endpoints can be ordered by high endpoint plus stable identifier, stored in a per-low bucket, or represented by handles that define identity outside the comparator.

## Augmentation Theorem for Red-Black Trees

Theorem 17.1 applies when a node's augmented attribute can be computed in constant time from the node itself and its children, including their augmented attributes. Then insertion and deletion can maintain the attribute without changing the asymptotic red-black-tree bounds.

Use this theorem only after checking:

1. The attribute's definition is per subtree, not per root-to-node path unless ancestor data is explicitly maintained elsewhere.
2. The value at a node depends only on that node and its two children.
3. The sentinel or empty-child value is defined.
4. Rotations invalidate only the nodes whose child sets change, or any propagation remains bounded by the tree height and the constant number of rotations.
5. Deletion's moved node and all ancestors on changed paths are handled.

Examples that satisfy the local condition:

- Subtree size for order-statistic trees.
- Maximum high endpoint in an interval subtree.
- Black-height, when represented from descendants and node color. Define the sentinel black-height convention first, then compute a node's value from one child black-height plus the node's color, relying on the red-black equal-black-height invariant.
- Any associative inorder aggregate that can be combined from left aggregate, node payload, and right aggregate.

Examples that do not satisfy the theorem directly:

- Node depth, because it depends on ancestors and rotations can change depths for many descendants.
- Global rank stored directly in every node, because inserting a new minimum can change many ranks.
- Metadata whose value depends on sibling, parent, or external global state unless an additional proof bounds updates.

## Order-Statistic Trees

An order-statistic tree is a red-black tree with a subtree-size field at each node. The sentinel's size is zero, and every internal node satisfies the identity below.

$$
x.\mathrm{size}=x.\mathrm{left}.\mathrm{size}+x.\mathrm{right}.\mathrm{size}+1
$$

This metadata supports two different query shapes:

| Query | Input contract | Core move |
| --- | --- | --- |
| Select by rank | Tree root and a one-based rank within the subtree | Compare the target rank with the left-subtree size plus one. |
| Rank by node | A tree and a node handle already in the tree | Start with the node's local rank and climb to the root, adding skipped left subtrees when moving up from a right child. |

For select, at a node compute the rank of that node within its own subtree.

$$
r=x.\mathrm{left}.\mathrm{size}+1
$$

Then go left, return the node, or go right with the target rank reduced by the local rank.

For rank, initialize with the node's local rank. While climbing to the root, add the parent and the parent's left subtree exactly when the climb comes from a right child.

### Duplicate-Key Discipline

Do not say `rank(key)` is well-defined in a multiset unless the API defines which equal key is meant. The textbook node-rank operation takes a node pointer, and with duplicate keys the rank is the node's position in inorder traversal, not a unique property of the key value.

Production choices include:

- `rank(handle)`: caller identifies the exact node or iterator.
- `rank_lower_bound(key)`: count elements strictly below the key.
- `rank_upper_bound(key)`: count elements at or below the key.
- Compound ordering by key plus stable tie-breaker.
- One node per key with a multiplicity count and explicit within-bucket offset rules.

Concrete API patterns:

```text
select(index) -> handle
rank(handle) -> index of that exact element
count_less_than(key) -> lower-bound rank
count_at_most(key) -> upper-bound rank
insert(key, value) -> handle with stable tie-breaker or bucket offset
```

Choose one policy before writing tests. Searching by key and then calling node-rank is ambiguous if search may return any duplicate.

### Maintaining Subtree Size

Insertion increments the size field on the downward search path and gives the new node size one. Rotation repair changes only local child sets, so update the two rotated nodes in dependency order.

For a left rotation around the old parent, the new parent inherits the old parent's subtree size, and the old parent recomputes from its children.

Deletion decrements sizes along the changed path from the lowest moved or removed position toward the root, then handles fixup rotations the same way. The important review point is not the exact pseudocode line number; it is that every structural path change and every rotation has a metadata update rule.

## Interval Trees

An interval tree stores intervals in a red-black tree ordered by low endpoint. Each node also stores the maximum high endpoint among all intervals in its subtree. The empty subtree value must be below every valid high endpoint or be represented as a sentinel-safe minimum.

$$
x.\mathrm{max}=\max\{x.\mathrm{int}.\mathrm{high},x.\mathrm{left}.\mathrm{max},x.\mathrm{right}.\mathrm{max}\}
$$

Closed intervals overlap when both endpoint comparisons succeed.

$$
i.\mathrm{low}\le i'.\mathrm{high}\quad\text{and}\quad i'.\mathrm{low}\le i.\mathrm{high}
$$

If using open or half-open intervals, rewrite the overlap predicate and all boundary tests before implementing. Booking systems often use half-open intervals so adjacent bookings do not conflict.

### Interval Search Rule

At node `x`, if the query does not overlap `x.int`, go left exactly when the left subtree is nonempty and its maximum high endpoint reaches the query's low endpoint. Otherwise go right.

The safe-right proof is simple: if the left subtree is empty or its maximum high endpoint is before the query's low endpoint, every interval in the left subtree ends before the query starts, so none overlaps.

The safe-left proof is the common trap. If the algorithm goes left and the left subtree contains no overlapping interval, it still does not miss a right-subtree overlap:

1. Choose a witness interval in the left subtree whose high endpoint equals the stored left-subtree maximum.
2. Since that interval does not overlap the query, interval trichotomy puts the query strictly to its left by high endpoint.
3. Because the tree is ordered by low endpoint, every right-subtree interval starts no earlier than the current node's low endpoint, which is no earlier than the left interval's low endpoint.
4. Therefore every right-subtree interval starts after the query ends, so none overlaps.

When proving correctness, name all three ingredients: interval trichotomy, existence of an interval attaining the left maximum, and BST ordering by low endpoint. Omitting any one usually turns the proof into hand-waving.

Compact contradiction template:

1. Assume some right-subtree interval overlaps the query.
2. Use low-endpoint ordering to place the current node's low endpoint at or before the query's high endpoint.
3. Pick the left-subtree witness whose high endpoint reaches the query's low endpoint.
4. Since the witness does not overlap the query, trichotomy forces the query to end before the witness starts.
5. Low-endpoint ordering then puts every right-subtree interval after the query, contradicting the assumed overlap.

The later recursive outcome in the left subtree is not part of the pruning decision. The pruning proof is local to the node where the branch choice is made.

### Interval API and Production Boundaries

Before using an interval tree for real booking, calendars, reservations, or VLSI geometry, define:

- Closed, open, or half-open interval semantics.
- Whether zero-length intervals are valid.
- Endpoint normalization for timestamps, time zones, daylight saving transitions, and precision.
- Whether the query needs any overlap, all overlaps, the earliest-low overlap, exact interval lookup, or maximum-overlap point.
- How delete, update, reschedule, and batch import maintain the maximum endpoint metadata. Treat reschedule as delete plus insert unless the implementation has a proved in-place update path.
- How concurrent insertions avoid race conditions between search and commit. If conflict search and insertion are not one transaction or one lock-protected critical section, the structure is not sufficient for booking correctness.
- How persistence, crash recovery, and rebuilds restore both the base tree and the augmented metadata after partial writes or corrupted state.

Go/no-go rubric for custom interval trees:

- **Go** only when the workload is truly dynamic, in-memory latency matters, interval semantics are stable, the team can test rotations and deletion paths, and library/database options fail a documented requirement.
- **No-go** when correctness depends on transactions, cross-process persistence, ad hoc rebuilds, complex calendar normalization, or operational ownership the team cannot staff.
- **Prefer database or library** when a range index, exclusion constraint, geometry index, or maintained ordered container provides the same conflict rule with less bespoke metadata maintenance.

Minimum acceptance tests for a production-bound interval tree:

1. Empty tree, single node, and root replacement on delete.
2. Boundary-touching intervals under the chosen openness convention.
3. Nested intervals, identical intervals, equal low endpoints, and equal high endpoints.
4. Insert and delete sequences that force both left and right rotations.
5. Reschedule and batch-update paths compared against delete plus insert semantics.
6. Randomized operation sequences checked against a brute-force interval list.
7. Concurrency or transaction tests for simultaneous non-conflicting and conflicting bookings.
8. Rebuild or recovery tests that recompute augmented metadata from persisted base records.

## Common Extension Patterns

| Problem | Augmentation idea | Trap |
| --- | --- | --- |
| Count inversions in an array | Insert elements into an order-statistic tree and count prior larger elements | Define duplicate policy before counting. |
| Josephus permutation | Maintain remaining people by rank and repeatedly select/delete by modular rank | Indices shift after deletion; use subtree sizes rather than array deletion. |
| List all overlapping intervals | Repeatedly search and delete temporarily, or recursively prune subtrees using maximum endpoints | Restoring mutations and duplicate intervals must be safe. |
| Rectangle overlap with sweep line | Sweep by horizontal edge events and keep active vertical intervals in an interval tree | Event ordering must handle containment and boundary semantics. |
| Point of maximum interval overlap | Store endpoint deltas and augment prefix-sum information | Tie-breaking and endpoint openness change counts. |
| Minimum gap in a dynamic set | Maintain subtree minimum, maximum, and minimum adjacent gap | The gap depends on boundary values crossing child and parent regions. |

## Invariant and Proof Recipes

For an augmented red-black tree:

1. State the base BST or red-black invariant separately from the augmented invariant.
2. Define the sentinel value.
3. Show the augmented value is computed from children and local node data.
4. Show insertion/deletion update changed ancestor paths.
5. Show each rotation recomputes affected nodes in dependency order.
6. Only then analyze the new query.

For order-statistic queries:

1. Convert the desired rank convention to a node-handle, lower-bound, upper-bound, or tie-broken key contract.
2. Use left-subtree size to count inorder predecessors.
3. For upward rank, add skipped regions only when moving up from a right child.
4. State the height-bound dependency on the balanced tree.

For interval search:

1. State the interval overlap predicate and boundary convention.
2. State that the tree is ordered by low endpoint.
3. State that the maximum endpoint is a subtree aggregate.
4. Prove safe right using the maximum endpoint.
5. Prove safe left using interval trichotomy plus low-endpoint ordering.

## RED Pressure Failures This Skill Prevents

Baseline agents often know the names `OS-SELECT`, `OS-RANK`, and interval trees. This skill exists to prevent subtler failures:

- Treating a cached field as a valid augmentation without checking local dependence.
- Claiming depth is covered by the augmentation theorem even though it depends on ancestors.
- Implementing `rank(key)` for duplicates without defining lower-bound, upper-bound, handle, tie-breaker, or bucket semantics.
- Proving interval-search correctness with intuition but omitting interval trichotomy or the low-endpoint ordering argument.
- Forgetting that interval trees as presented use closed intervals and that production booking often wants half-open intervals.
- Updating metadata on insert but not on deletion moves, rotations, reschedules, or rebuilds.
- Recommending a hand-rolled tree when a library ordered container, database range index, transaction, or exclusion constraint is safer.
- Leaking formulas into prose or tables in CLRS-style answers instead of using display math.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| "Theorem 17.1 proves any per-node metadata is cheap." | Check whether the node value depends only on local node and child information. |
| "Store global rank in each node." | Store subtree size; global ranks change too broadly under insertion. |
| "Search key then rank the result." | Safe only with distinct keys or deterministic duplicate semantics. |
| "Rotations preserve the tree, so metadata is fine." | Rotations preserve inorder order, but augmented fields whose child sets changed must be recomputed. |
| "Interval search can go left because max says maybe." | Prove safe pruning; the right subtree is excluded only by trichotomy plus low-endpoint ordering. |
| "Closed versus half-open intervals is a detail." | It changes overlap at boundaries and can change booking correctness. |
| "The logarithmic query justifies custom infrastructure." | Include update, delete, concurrency, persistence, tests, and library/database alternatives in the decision. |

## Verification Pressure Tests

Use these prompts to check whether this skill is working:

1. "A teammate wants to store black-height and depth in every red-black-tree node and cites the augmentation theorem. Which field qualifies and why?"
2. "Design `rank(key)` for a production ordered multiset. Explain why node-rank is not the same as key-rank with duplicates."
3. "Prove the left-branch case of interval search without hand-waving. Name the exact facts that exclude the right subtree."
4. "Review a proposed hand-rolled interval tree for booking conflicts. What semantics, maintenance rules, tests, and alternatives must be checked?"
5. "Given an augmented tree proposal, apply the four-step method and reject the design if metadata update rules for deletion and rotations are missing."
6. "Explain how to update subtree size or maximum endpoint after a rotation without changing the inorder sequence."

Static checks for this skill:

- `SKILL.md` lives at `clrs/augmenting-data-structures/SKILL.md`.
- Frontmatter name is `augmenting-data-structures`, description starts with `Use when`, and license is `MIT`.
- The parent `clrs` skill lists this chapter skill.
- Formal identities, overlap predicates, and bounds appear in display LaTeX blocks rather than inline prose or table cells.
- The text distinguishes textbook mechanism from production deployment judgment.
