---
name: b-trees
description: Use when reasoning about B-trees, external-memory indexes, disk-block search trees, 2-3-4 trees, B-tree height bounds, node splits, top-down insertion, deletion cases, or database/storage index choices.
license: MIT
---

# B-Trees

## Overview

B-trees are not just high-fanout binary search trees. They teach the external-memory index mindset: choose node size from the block-transfer model, keep height small by packing many ordered separator keys per node, and spend CPU inside a block to avoid extra disk or page accesses.

When applying this chapter in industrial contexts, answer both questions:

1. Is the bottleneck disk, SSD page, cache block, or CPU comparison work?
2. Which invariant prevents an insertion or deletion from needing to backtrack up the tree?

## Shared CLRS Conventions

Also follow the parent `clrs` skill for mathematical formatting, theorem preconditions, proof tone, and chapter-skill routing. Put formal bounds in display LaTeX blocks, not inline prose or Markdown table cells.

## When to Use

Use this skill for:

- B-trees, B-plus-trees, B-star-trees, external-memory indexes, database indexes, storage-engine pages, disk blocks, SSD page access, and high-fanout search trees.
- B-tree definition questions: minimum degree, key counts, child counts, sorted separator keys, equal leaf depth, and root exceptions.
- `B-TREE-SEARCH`, `B-TREE-CREATE`, `B-TREE-INSERT`, `B-TREE-SPLIT-CHILD`, `B-TREE-SPLIT-ROOT`, `B-TREE-INSERT-NONFULL`, and `B-TREE-DELETE` reasoning.
- Comparing B-trees with red-black trees, binary search trees, sorted arrays, hash tables, LSM trees, or platform ordered containers.
- 2-3-4 tree questions, including join and split exercises.
- Disk-access versus CPU-time accounting, including block read models and root residency.

Do not use this skill as the primary guide for:

- Exact lookup with no ordering, range scan, predecessor, successor, or storage-page need; prefer hash-table reasoning.
- In-memory ordered maps where a standard library tree, skip list, sorted vector, or cache-aware container already solves the problem.
- Production database implementation details not present in the chapter, such as concurrency control, write-ahead logging, crash recovery, prefix compression, B-link trees, or LSM compaction policy.
- B-plus-tree leaf-chain semantics unless the prompt explicitly asks for the variant; the chapter's base B-tree keeps satellite information with keys.

## First Decision: What Search Structure Fits?

| Need | Prefer | Why |
| --- | --- | --- |
| Disk or page-resident ordered data | B-tree or B-plus-tree family | Reduces expensive page transfers by increasing fanout. |
| In-memory ordered map with ordinary keys | Mature balanced ordered container | Textbook B-tree mechanics are not automatically faster than engineered containers. |
| Exact lookup only with no order | Hash table | Ordering and separator maintenance add cost without value. |
| Static sorted data with rare mutation | Sorted array plus binary search | Locality and simplicity may beat tree maintenance. |
| Write-heavy storage with batched updates | Consider LSM-style design | B-trees optimize point/range reads and page-local updates, not every write pattern. |
| Educational 2-3-4 tree reasoning | B-tree with minimum degree fixed to the smallest legal value | Splits, merges, and borrowing become concrete enough to trace by hand. |

Before accepting a B-tree proposal, ask:

1. Does the data live in blocks or pages where one access can fetch many keys?
2. Is the root or top levels resident in memory?
3. Is the dominant cost block transfers, cache misses, key comparison, or mutation write amplification?
4. What node capacity follows from key size, pointer size, satellite-data placement, and block size?
5. What duplicate-key and satellite-record policy does the implementation expose?
6. Does deletion need full textbook rebalancing, lazy deletion, or a storage-engine-specific policy?

## B-Tree Definition Checklist

State the definition before applying any theorem or operation:

- Each node stores a sorted list of keys and a boolean leaf flag.
- An internal node with a given number of keys has one more child pointer than keys.
- Keys in a node separate the key ranges of its children.
- All leaves have the same depth.
- Every nonroot node has a lower and upper key-count bound determined by the minimum degree.
- The root is special: a nonempty root must have at least one key, but it need not satisfy the nonroot lower bound.
- A full node is one whose key count reaches the upper bound.

Use display math for the exact node-capacity contract:

$$
t \ge 2
$$

$$
t - 1 \le \text{nonroot keys} \le 2t - 1
$$

$$
t \le \text{nonroot internal children} \le 2t
$$

The illegal minimum-degree trap is simple: if the minimum degree were one, nonroot nodes could have no keys, internal nodes would not be forced to branch, splitting and merging would degenerate, and the height bound would lose its useful growth base.

## Disk-Block Model and Production Translation

The chapter analyzes two costs separately:

- **Disk or block accesses:** calls that transfer a whole node-sized block between secondary storage and main memory.
- **CPU time:** comparisons, loops, shifts, and in-memory manipulation inside nodes.

The root convention matters: the root is assumed to be in main memory, so procedures do not perform `DISK-READ` on the root. Modified nodes, including a modified root, still require `DISK-WRITE`.

Use this production phrasing when a teammate says B-trees are faster because they are logarithmic: "The textbook B-tree advantage is not the asymptotic label alone. It trades more CPU work inside each page for fewer page transfers. If the workload is already in RAM and comparison or cache-line behavior dominates, a B-tree is not automatically better than an engineered ordered container."

For modern systems, translate "disk" into the dominant transfer unit: disk block, SSD page, database page, filesystem page, or cache line. Then verify that node size, fanout, and satellite-data placement match that unit.

## Height Bound and Counting Proof

Theorem 18.1 bounds worst-case height for a nonempty B-tree. State its preconditions first: nonempty tree, minimum degree at least two, all nonroot nodes respecting the lower key bound, and all leaves at the same depth.

$$
h \le \log_t \frac{n + 1}{2}
$$

Proof recipe:

1. Give the root the fewest legal keys.
2. Give every other node the fewest legal keys.
3. Minimize branching at each depth: the root has at least two children when the height is positive, and every later internal node has at least the minimum number of children.
4. Sum the minimum number of keys across depths.
5. Solve the resulting inequality for height.

The minimum-key count is:

$$
n \ge 1 + (t - 1)\sum_{i=1}^{h} 2t^{i-1}
$$

After simplification:

$$
n \ge 2t^h - 1
$$

Therefore the displayed height bound follows. The industrial lesson is that a larger fanout changes the logarithm base and cuts page transfers, but it does not remove CPU work inside pages or mutation costs.

The maximum number of keys at height is achieved when every node is full:

$$
n_{\max} = (2t)^{h+1} - 1
$$

## Operation Quick Reference

| Operation | Invariant move | Disk-access lesson | CPU lesson |
| --- | --- | --- | --- |
| Search | Choose the first separator not less than the key, or descend to the final child. | One downward path; root read is omitted by convention. | Linear scan inside node costs proportional to node capacity; binary search can reduce comparisons. |
| Create | Allocate an empty leaf root and write it. | Constant disk work. | Constant CPU work. |
| Split child | Split a full child around its median before descending. | Writes the old child, new child, and parent. | Shifts keys and pointers within bounded node capacity. |
| Insert | Split full nodes on the way down so recursion never enters a full node. | One pass downward with bounded reads and writes per level. | Per-level scan and shift work. |
| Delete | Ensure the child about to receive recursion has an extra key. | One pass downward except predecessor or successor replacement can write back through a saved pointer. | Borrow and merge cases require careful index movement. |

Reference costs for height-based operations:

$$
O(h) = O(\log_t n)
$$

With linear search inside nodes, the CPU cost form is:

$$
O(th) = O(t\log_t n)
$$

With binary search inside nodes, comparison work across the path becomes independent of the chosen minimum degree up to the overall tree size:

$$
O(\lg n)
$$

## Search Guidance

`B-TREE-SEARCH` generalizes binary search tree search from a two-way decision to a multiway decision.

Use this checklist:

1. Scan or binary-search the sorted keys in the current node.
2. If the key is found, return the node and key index.
3. If the current node is a leaf and the key was not found, return not found.
4. Otherwise read the selected child and recurse.

For production answers, separate the cost of comparing keys inside a page from the cost of fetching the page. Binary search inside a node may help CPU time, but it does not change the number of block accesses. For tiny nodes such as 2-3-4 tree nodes, a linear scan can still be the better engineering choice because branch prediction and cache behavior may dominate the asymptotic comparison count.

## Insertion: Split Before Descent

The insertion invariant is: never recurse into a full node. The algorithm enforces this by splitting any full child before descending to it.

Root split is the only way the tree grows taller:

1. If the root is full, allocate a new nonleaf root.
2. Make the old root the new root's first child.
3. Split that child.
4. Continue insertion into a nonfull root.

Child split mechanics:

1. Let the selected child be full.
2. Allocate a new sibling with the same leaf flag.
3. Move the greater keys, and the corresponding child pointers when internal, into the new sibling.
4. Leave the lesser keys in the old child.
5. Move the median key up into the parent.
6. Insert the new sibling pointer immediately after the old child.
7. Write every modified node.

Pressure-check the median count:

$$
(t - 1) + 1 + (t - 1) = 2t - 1
$$

That identity explains why splitting a full node produces two legal nonfull nodes and one promoted separator.

## Deletion: Extra Key Before Descent

Deletion is the chapter's easiest place to make off-by-one mistakes. The recursive descent invariant is stronger than ordinary B-tree validity: before recursion descends into a nonroot child, that child must have at least the minimum degree number of keys, not merely the usual nonroot minimum.

Ordinary validity permits:

$$
t - 1
$$

Deletion descent requires:

$$
t
$$

Case guide:

| Case | Situation | Required action | Why it is safe |
| --- | --- | --- | --- |
| Case 1 | The search reaches a leaf. | Delete the key if present; otherwise report not found. | The descent invariant ensured a nonroot leaf can lose one key and remain legal. |
| Case 2a | The key is in an internal node and the preceding child has an extra key. | Replace the key by its predecessor and delete that predecessor from the preceding child. | The predecessor path begins from a child safe for descent. |
| Case 2b | The key is in an internal node and the following child has an extra key. | Replace the key by its successor and delete that successor from the following child. | Symmetric to predecessor replacement. |
| Case 2c | The key is in an internal node and both adjacent children are minimal. | Merge preceding child, the key, and following child before attempting predecessor or successor deletion; then delete from the merged child. | The merged node is full, so recursive deletion is safe. |
| Case 3a | The key is not in the internal node; the target child is minimal but an immediate sibling has an extra key. | Rotate one key through the parent into the target child; move the sibling boundary key up. | The target child gains the extra key needed for descent. |
| Case 3b | The target child and immediate siblings are minimal. | Merge the target child with one sibling and move the separating parent key down. | The merged child is large enough for descent; the parent loses one key. |

Borrowing is not direct sibling-to-child key copying. A parent separator moves down into the deficient child, and the sibling boundary key moves up into the parent. If children are internal nodes, the corresponding boundary child pointer moves with the borrowed key range.

Root shrink rule: after a merge, if the root has no keys, delete the old root and make its only child the new root. This is the only way B-tree height decreases. If the root is a leaf and its last key is deleted, the tree becomes empty.

Common deletion review checks:

- Left sibling borrow uses the sibling's greatest key.
- Right sibling borrow uses the sibling's least key.
- Merge with the right sibling moves the parent separator between the two children into the merged node.
- After removing a parent key, also remove exactly one child pointer and shift later keys and pointers consistently.
- In an internal-node merge, append the sibling child pointers in key-range order and free or detach the removed sibling after the parent pointer array is repaired.
- Check boundary children before naming a left or right sibling.
- Do not recurse into a child with only the ordinary minimum number of keys.

## Choosing Node Capacity

When a prompt gives a block-read time model, minimize the product of height and per-node transfer time rather than maximizing fanout blindly. The chapter exercise model uses a transfer time of this shape:

$$
a + bt
$$

Search time is approximated by:

$$
\frac{\ln n}{\ln t}(a + bt)
$$

The optimum satisfies:

$$
bt(\ln t - 1) = a
$$

For the common exercise values:

$$
a = 5\text{ ms}
$$

$$
b = 10\text{ microseconds}
$$

The approximate solution is near:

$$
t \approx 128
$$

Do not present this as a universal storage-engine constant. It follows from the toy transfer-time model and ignores cache hierarchy, compression, write cost, concurrency, and real device behavior.

## Variants and 2-3-4 Trees

The smallest legal minimum degree gives 2-3-4 trees. Use them when a problem wants hand-traceable B-tree behavior or asks about absorbing red children into black nodes of a red-black tree.

2-3-4 tree facts:

- Internal nodes have two, three, or four children.
- Nodes have one, two, or three keys.
- Top-down insertion splits full nodes before descent.
- Deletion borrows or merges before descent using the same extra-key invariant.
- A red-black tree can be viewed as a 2-3-4 tree when each black node absorbs its red children; rotations and recolorings correspond to splitting, merging, or redistributing these multi-key nodes.

For join and split exercises:

1. Maintain subtree height as stored metadata and update it on structural changes; this does not change asymptotic search, insert, or delete costs.
2. To join two 2-3-4 trees with a separating key, descend the taller tree until the child height matches the shorter tree, splice in the separating key and shorter tree, then repair overflow on the way back or by local splits.
3. To split around a key, follow the search path, collect side subtrees and separator keys that fall left and right, then rebuild each side using repeated joins from the deepest collected subtrees upward so every join receives already-balanced inputs.
4. The join costs telescope because each join works across a height difference, and the sequence of height differences along one root-to-leaf path sums to the tree height.

## One Practical Design Pattern

For a page-resident ordered index with range scans and point lookups:

1. Start from a mature database, storage engine, filesystem, or library index unless the implementation is the product.
2. Decide whether the exposed structure is a B-tree, B-plus-tree, or another page-oriented index.
3. Size nodes from page size, key size, pointer size, payload placement, compression, and expected fill factor.
4. Keep root and hot upper levels cached when possible.
5. Use top-down split and borrow/merge invariants as review tools, even if the implementation uses variant-specific policies.
6. Measure page reads, writes, cache misses, range-scan locality, split frequency, merge frequency, and tail latency separately.
7. Treat textbook pseudocode as an invariant reference, not a complete concurrent crash-safe storage engine.

## Invariant and Proof Recipes

- **B-tree search correctness:** State the separator-key invariant. After comparing with keys in the current node, show that exactly one child range can contain the target if the key is not in the node.
- **Height bound:** Construct the sparsest legal tree for the requested height, count minimum keys by depth, and solve for height.
- **Split correctness:** Show the median key separates all keys left in the old child from all keys moved to the new sibling, and show both resulting children satisfy key-count bounds.
- **Insertion correctness:** Maintain the nonfull-descent invariant. Splitting before descent ensures the leaf that receives the new key has space.
- **Deletion correctness:** Maintain the extra-key descent invariant. Borrowing creates room before descent; merging creates a full child before descent; root shrink preserves the root exception.
- **2-3-4 join and split:** Use stored heights to align subtrees, then rely on local split repair. For split, decompose the search path into ordered side subtrees and separators, then join them back in height-compatible order.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Recommending textbook B-tree code for an in-memory latency service solely because the height is smaller | Separate disk/page access from CPU and cache behavior; require a block-transfer bottleneck. |
| Saying B-tree search is logarithmic without interpreting the logarithm base and minimum-degree preconditions | State the height theorem, root exception, and node key-count bounds. |
| Forgetting that the root is conventionally kept in memory | Count root reads differently from other node reads, but still write a modified root. |
| Treating deletion as BST deletion plus rebalancing | Use the exact extra-key descent invariant and cases 1, 2a, 2b, 2c, 3a, and 3b. |
| Borrowing directly from siblings during deletion | Move keys through the parent separator and move child pointers when nodes are internal. |
| Putting formulas in Markdown table cells or prose | Put all bounds and transfer-time expressions in display LaTeX blocks. |
| Treating 2-3-4 join and split as ordinary concatenation and slicing | Align heights, use separating keys, and repair local overflows with B-tree operations. |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| "A B-tree is always faster than a red-black tree because it has lower height." | It is faster when fewer block or page transfers dominate the extra per-node CPU and mutation work. |
| "The minimum degree can be one." | The minimum degree must be at least two or nonroot nodes can be empty and the height argument degenerates. |
| "Insertion splits after it reaches a full leaf." | Top-down insertion splits full nodes before descent so recursion never enters a full node. |
| "Deleting from an internal node means just swapping with predecessor." | Predecessor replacement is allowed only when the preceding child has enough keys; otherwise use successor or merge. |
| "A child with the usual minimum key count is safe for deletion descent." | Deletion descent requires one extra key before recursion unless the child is the root. |
| "B-plus-trees are the same as the chapter's B-trees." | B-plus-trees keep satellite records in leaves and use internal nodes primarily for routing; state the variant. |
| "Disk-access count and CPU time are one metric." | Count block transfers and in-node CPU work separately, then map them to the real bottleneck. |
| "A split or merge can ignore satellite data." | Whatever satellite information or pointer is associated with a key moves with that key. |

## Verification Pressure Tests

Use these prompts to check whether this skill is working:

1. "A teammate wants to replace an in-memory red-black tree with textbook B-tree code for p99 latency. Explain when this is and is not justified, including root residency, block transfers, CPU work, and the height theorem."
2. "Review B-tree deletion pseudocode. State the invariant before every recursive descent and explain cases 1, 2a, 2b, 2c, 3a, and 3b, including root shrink."
3. "Answer these B-tree exercises: why the minimum degree cannot be one, maximum keys at a given height, binary search within nodes, choosing node capacity from a block-read model, and 2-3-4 join/split. Keep formulas in display blocks."
4. "Trace an insertion that splits the root and later splits a full child. Explain why splitting is done before descent and why height grows at the top."
5. "Compare a B-tree, B-plus-tree, red-black tree, sorted array, hash table, and LSM tree for a storage workload with point lookup, range scan, inserts, deletes, and page-size constraints."

Static checks for this skill:

- `SKILL.md` lives at `clrs/b-trees/SKILL.md`.
- Frontmatter name is `b-trees` and description starts with `Use when`.
- The parent `clrs` skill lists this chapter skill.
- Formal bounds and transfer-time expressions are displayed in LaTeX blocks, not embedded in prose or Markdown table cells.
- The text distinguishes textbook B-tree mechanics from production storage-engine choices.
- Deletion guidance names the extra-key descent invariant and all required cases.
