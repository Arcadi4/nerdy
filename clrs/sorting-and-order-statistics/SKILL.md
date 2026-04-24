---
name: sorting-and-order-statistics
description: Use when choosing or analyzing CLRS sorting, heaps, priority queues, linear-time integer/distribution sorting, quicksort, selection, medians, quantiles, top-k, or order-statistic algorithms under practical engineering constraints.
license: MIT
---

# Sorting and Order Statistics

## Overview

Use sorting and selection as engineering tools, not reflexes. The core move is to identify the exact order information required, then choose the weakest ordering primitive that satisfies it under the real key, stability, memory, and adversary constraints.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style.

## When to Use

- You need to sort records, select a percentile, maintain top-k, merge sorted streams, or implement a priority queue.
- A prompt involves heaps, heapsort, quicksort, counting sort, radix sort, bucket sort, medians, quantiles, or ith order statistics.
- A comparison-sort lower bound seems relevant, or a proposed linear-time sort depends on integer keys, digits, or distribution assumptions.
- An implementation must preserve satellite data, stability, handles, index maps, or large-payload locality.

Do **not** use this skill merely because output should appear sorted in a UI. Use the platform's ordinary sort unless algorithm choice, asymptotics, stability, or data-structure behavior matters.

## First Decision: How Much Order Do You Need?

| Need | Prefer | Why |
| --- | --- | --- |
| General ordered records | Library sort, stable sort if ties matter | Production sorts are engineered for cache, duplicates, depth limits, and language semantics |
| Stable order by small dense integer key | Counting sort or radix sort | Beats comparison sorting only because key values can index counts or digits |
| Dynamic repeated min/max | Binary heap priority queue | Maintains partial order, not full sorted order |
| Merge k sorted streams | Min-heap of stream heads | Gives total cost based on k, not total stream count as a sort key |
| Single rank, median, percentile threshold | Selection or `nth_element` | Full sorting pays for order you will discard |
| Top-k unsorted | Size-k heap or selection threshold | Choose by k size, streaming needs, and memory |
| Top-k sorted | Select threshold, partition top-k, then sort only k | Avoids sorting the cold majority |
| Worst-case linear rank guarantee | Median-of-medians SELECT | Usually a fallback or proof tool because constants are high |

Before accepting a sort proposal, ask:

1. Is the output required to be fully ordered, or only partitioned around a rank or key?
2. Are equal-key records required to preserve input order?
3. Are keys comparison-only, bounded integers, fixed-width digits, or drawn from a known distribution?
4. Is moving the record payload expensive enough to sort pointers, indices, or references instead?
5. Can the input be adversarial, highly duplicated, already sorted, skewed, or streaming?

## Comparison Sorting Boundary

For comparison sorts on distinct keys, the decision-tree lower bound is:

$$
\Omega(n\lg n)
$$

because all permutations must remain possible leaves. This lower bound does **not** apply when the algorithm uses key values as array indices, digit values, or distribution positions. Whenever an answer claims linear sorting, state which non-comparison assumption paid for it.

## Practical Sorting Choices

| Algorithm family | Use when | Avoid or qualify when |
| --- | --- | --- |
| Insertion sort | Small arrays, nearly sorted runs, final cutoff inside engineered sorts | Large arbitrary inputs; worst case is quadratic |
| Merge sort or stable library sort | Stability is required and extra memory is acceptable | In-place memory is mandatory |
| Heapsort | In-place worst-case comparison bound is more important than constants/cache behavior | You want the fastest ordinary production sort |
| Quicksort partitioning | Teaching, `nth_element`, partition-based selection, or controlled internal implementation | Hand-rolled textbook quicksort in production |
| Counting sort | Integer key domain is small or remapped densely; stability matters | Key range is huge or sparse relative to input |
| Radix sort | Large batches of fixed-width primitive keys, IDs, or strings with stable digit passes | Memory bandwidth, allocation, or complex comparators dominate |
| Bucket sort | Distribution is validated and bucket boundaries are chosen from probability mass | Skew is unknown; worst-case guarantees matter |

Industrial default: use a mature library sort unless a property above clearly beats it. If implementing quicksort-like code, protect against duplicates with 3-way partitioning, protect against fixed bad input orders with randomized or sampled pivots, use a small-array insertion cutoff, and add a depth-limited fallback for worst-case executions. Random pivoting changes which inputs are predictably bad; it does not make worst cases impossible, and it does not by itself fix equal-key collapse. Tail recursion elimination only protects the stack if the smaller side is recursed into and the larger side is iterated.

## Stability, Satellite Data, and Payload Movement

Sorting keys in CLRS usually means sorting records. In production, keys travel with satellite data.

- If equal keys must retain arrival, timestamp, or file order, require a stable algorithm or explicitly add a stable tie-breaker.
- If records have large payloads, prefer sorting indices, pointers, row IDs, or compact key-reference pairs, then gather or stream the payload once.
- Counting sort is stable when placement processes input from the end while decrementing prefix counts; stable bucket construction preserves order by appending to buckets in input order.
- Radix sort needs a stable digit sort; without stability, later digit passes destroy earlier digit order.
- Bucket sort's average linear claim depends on distribution assumptions; counting sort's linear claim depends on key-range assumptions, not uniformity.

## Heaps and Mutable Priority Queues

A heap is a partial order for repeated extrema. It is the right abstraction for schedulers, event simulation, Dijkstra-like algorithms, k-way merge, streaming top-k, and dynamic priorities.

Binary heap facts:

- Root is min or max depending on orientation.
- Leaves occupy the second half of the array.
- `heapify` assumes child subtrees are already heaps and moves one bad node downward.
- Building a heap bottom-up is linear because most nodes are near leaves; do not multiply every node by the root height.

| Heap operation | Cost | Implementation note |
| --- | --- | --- |
| Peek min or max | Constant | Read the root without changing the heap |
| Insert | Logarithmic | Append, then bubble up |
| Extract min or max | Logarithmic | Move the last element to the root, then heapify down |
| Increase or decrease key | Logarithmic | Choose direction from heap orientation and priority change |
| Build heap bottom-up | Linear | Start at the last internal node and heapify downward |

Mutable priority queue checklist:

1. Store a map from external handle or job ID to heap index.
2. Every array swap must update both affected map entries in the same helper.
3. Reject duplicate live IDs, or define update semantics explicitly.
4. On extraction or cancellation, delete the removed ID from the map and invalidate stale handles.
5. After moving the last heap element into a hole, compare with its parent and best child to choose bubble-up or heapify-down. If uncertain, perform the direction that fixes the violated local relation, then assert the heap property in debug builds.
6. For a min-heap, a numerically smaller priority bubbles up; a numerically larger priority heapifies down. Reverse this for max-heaps.

Do not expose raw indices as durable handles unless they carry generation/version checks. Stale handles cause silent scheduler corruption.

## Selection and Order Statistics

The ith order statistic is the ith smallest element. Selection does not need to order all pairs, so the sorting lower bound does not apply.

Use this workflow:

1. Translate the requested percentile, median, threshold, or top-k into a rank convention.
2. If only the threshold is needed, use selection or a library `nth_element`/partition primitive.
3. If the top-k values are needed but not sorted, use a size-k heap for streaming data or selection plus partition for batch data.
4. If sorted top-k output is needed, sort only the selected k elements.
5. If adversarial worst-case linear time matters, use median-of-medians as a fallback, not as the everyday fastest path.

Quickselect partitions around a pivot and recurses only into the side containing the desired rank. Its expected time is linear with random pivots, but worst case is quadratic. Median-of-medians spends linear work to choose a pivot that leaves at most a constant fraction of the input alive, giving worst-case linear time with larger constants.

Useful CLRS-derived patterns:

- Simultaneous min and max: compare items in pairs, then compare the smaller to the current min and the larger to the current max.
- Largest k sorted: full sort is simple, heap extraction costs based on k, selection plus sorting k is often best for batch data when k is small.
- k quantiles: recursively select pivots to split ranks.
- Median or weighted median minimizes one-dimensional absolute deviation; for Manhattan distance in two dimensions, solve the coordinates independently.

## Linear-Time Sorting Preconditions

| Claim | Required precondition | Failure mode |
| --- | --- | --- |
| Counting sort is linear | Key range size is acceptable after remapping | Huge sparse range burns memory |
| Counting sort is stable | Placement scans input in reverse or otherwise preserves equal-key order | Records with equal keys reorder |
| Radix sort is linear | Fixed digit count and stable digit sort with manageable digit range | Unstable pass corrupts prior digits |
| Bucket sort is average linear | Inputs are independent and approximately uniform after any transform | Skew collapses into one bucket |
| Selection is linear expected | Randomized or robust pivot strategy; only rank/partition is needed | Full sorted order still requires more work |

When assumptions are empirical, validate and monitor them. A nightly job using bucket boundaries should record bucket-size skew; a radix pass should be justified by actual key width and memory bandwidth; a counting sort should check that the count array is small enough for cache and memory.

## Invariant and Proof Recipes

- **Heapify:** Assume child subtrees are heaps; prove the only possible violation follows the moved node downward until the parent-child relation holds.
- **Build heap:** Loop downward from the last internal node; invariant says every later node is already the root of a heap.
- **Partition:** Name the regions less than, equal to, greater than, unknown, and pivot. The proof is the maintenance of those regions, not the pivot folklore.
- **Randomized quicksort analysis:** Define pair indicators. Two elements are compared only if one is the first pivot chosen from their rank interval; sum probabilities by linearity of expectation.
- **Counting sort stability:** Prefix counts identify final slots for each key; scanning from the end assigns equal keys from right to left so earlier records land earlier.
- **Selection:** Track the rank of the pivot within the current subarray and translate the target rank when recursing into the right side.
- **Median-of-medians:** Show enough elements are guaranteed below and above the pivot, then solve the shrink recurrence rather than claiming the pivot is exactly central.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Choosing textbook quicksort for stable 16-bit record sorting because it is in-place | Prefer stable counting/radix-style sorting or reference sorting; quicksort is unstable and moves payloads too much |
| Saying bucket sort needs uniform region codes for a dense integer key job | Counting sort needs a bounded key range, not uniformity; bucket sort needs distribution assumptions |
| Sorting all telemetry samples for a percentile and top-k | Select the percentile threshold and use heap or selection for top-k; sort only the top-k if ordered output is needed |
| Claiming p95 and top-k can always be solved in one ordinary streaming pass | Streaming top-k is easy with a heap; exact percentile generally needs stored data, sketches, multiple passes, or a selection-capable batch |
| Updating heap array swaps without map updates | Centralize swap-with-index-update and invalidate removed handles |
| Applying heapify in the wrong direction after priority changes | For min-heaps, smaller priority bubbles up and larger priority moves down; inspect both local relations after arbitrary removal |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Treating quicksort as the practical lesson of the chapter | Extract partition balance, randomization, duplicate handling, adversarial input, and library-sort judgment |
| Applying the comparison-sort lower bound to counting or radix sort | State that these algorithms use key values, not only comparisons |
| Forgetting satellite data | Decide whether to move records, references, or compact key-reference pairs |
| Ignoring stability | Make equal-key order a first-class requirement when records, timestamps, or radix passes are involved |
| Using a heap as a complete sorted order | A heap gives repeated extrema and partial order; extracting all elements is a sort |
| Assuming randomized algorithms remove worst cases | They remove fixed-input dependence under the random model; worst-case executions still exist |
| Trusting average bucket performance without monitoring skew | Validate distribution and choose fallback behavior |

## Verification Pressure Tests

Use these to check future answers:

1. **Stable dense-key records:** For many large records with a small integer key and required tie order, the answer should reject textbook quicksort and discuss stable counting/radix/reference movement.
2. **Percentile and top-k:** For a large telemetry batch needing p95 and top-k, the answer should avoid full sorting unless a complete order is actually required.
3. **Mutable heap handles:** For a scheduler heap with arbitrary cancellation, the answer should require map updates on every swap and stale-handle defenses.
4. **Linear-time claim:** For counting, radix, or bucket sort, the answer should name the exact assumption that escapes the comparison lower bound.
