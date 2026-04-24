---
name: greedy-algorithms
description: Use when solving or proving greedy algorithms, including activity selection, fractional knapsack, Huffman coding, offline caching, exchange arguments, greedy-choice property, optimal substructure, or deciding whether dynamic programming is required instead.
license: MIT
---

# Greedy Algorithms

## Overview

Greedy algorithms are not justified by intuition that a local choice "seems good." They require a proof that one locally best choice can be part of some global optimum, and that the remaining work is a smaller problem of the same kind.

**Core principle:** name the greedy choice, prove it is safe by exchange or transformation, then prove the residual subproblem combines with that choice to form an optimum.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style. Keep recurrences, costs, inequalities, and asymptotic bounds in display LaTeX blocks rather than inline prose.

When giving examples or pressure-test answers, do not write interval notation, set notation, objective functions, asymptotic bounds, capacities, or inequalities inline. Introduce them in prose, then put the notation in a display block.

## When to Use

- A prompt asks for a greedy algorithm, a proof of greedy correctness, an exchange argument, or a counterexample to a proposed greedy rule.
- The problem asks for maximizing compatible activities, fractional knapsack value, prefix-free Huffman codes, or offline cache hits with a known request sequence.
- You need to compare greedy with dynamic programming or explain why a locally attractive rule fails.
- A production question involves scheduling intervals, priority-queue merging, compression codes, cache replacement policies, or canonical coin systems.

Do **not** use this skill merely because an algorithm makes choices. If the choice must be made after comparing solved subproblems, use `dynamic-programming`. If the problem only needs repeated extrema or sorting mechanics, use `sorting-and-order-statistics` unless greedy correctness is central.

## Greedy Proof Checklist

Before presenting a greedy algorithm, answer these questions:

1. **What exactly is the greedy choice?** Earliest finish, highest value density, two minimum frequencies, furthest next use, shortest processing time, or another explicitly ordered choice.
2. **What is the subproblem after the choice?** It should be one residual instance, not a family of alternatives that still need comparison.
3. **Why is the choice safe?** Use an exchange argument, cut-and-paste proof, or transformation from an arbitrary optimum to an optimum that includes the greedy choice.
4. **Why does optimal substructure hold?** An optimal solution to the residual subproblem plus the greedy choice must produce an optimal solution to the original problem.
5. **What preprocessing or data structure makes choices fast?** Sorting, a min-priority queue, next-use tables, or a sweep structure often carries the running time.
6. **What tempting greedy rules fail?** Give a concrete counterexample when rejecting a rule; do not merely say it is not locally safe.

Safe proof skeleton:

1. Let an arbitrary optimal solution exist for the current subproblem.
2. If it already makes the greedy choice, continue.
3. Otherwise replace the first conflicting choice with the greedy choice.
4. Prove feasibility is preserved and objective value does not worsen.
5. Invoke the same argument recursively or inductively on the remaining subproblem.

## Greedy Versus Dynamic Programming

| Symptom | Use greedy when | Use dynamic programming when |
| --- | --- | --- |
| Choice timing | The next choice can be made before solving residual subproblems | The best first choice depends on solved subproblem values |
| Subproblem shape | The greedy choice leaves one residual problem | A choice splits into several alternatives to compare |
| Proof style | Exchange or stays-ahead transformation | Cut-and-paste recurrence plus table order |
| Knapsack signal | Fractions are allowed and value density can be consumed continuously | Items are indivisible and include/exclude alternatives must be compared |
| Implementation signal | Sort once or maintain a priority queue, then scan or merge | Store a value table and often a choice table |

Greedy and dynamic programming both need optimal substructure. The difference is whether the locally best choice is safe before residual values are known.

## Activity Selection

Use earliest finish time for maximum-cardinality compatible activities on one resource. Sort activities by nondecreasing finish time, then scan once and accept the next activity whose start is at or after the finish time of the most recently accepted activity.

Compatibility for half-open intervals means one activity can start exactly when the previous one finishes.

Proof recipe:

1. In any nonempty residual set, let the greedy activity be one with earliest finish time.
2. Take an optimal compatible set and look at the activity in it with earliest finish time.
3. If it is not the greedy activity, substitute the greedy activity for it.
4. Feasibility is preserved because the greedy finish time is no later than the replaced activity's finish time.
5. Cardinality is unchanged, so some optimum contains the greedy activity.
6. After selecting it, only activities starting after its finish remain; an optimal solution to that residual set completes the optimum.

Pseudocode pattern:

```text
sort activities by finish time increasing
selected = empty list
last_finish = -infinity
for activity in sorted order:
    if activity.start >= last_finish:
        append activity
        last_finish = activity.finish
return selected
```

If input is already sorted by finish time, the scan takes:

$$
\Theta(n)
$$

With sorting, the total time is:

$$
\Theta(n\lg n)
$$

### Activity Selection Trap Counterexamples

When disproving a proposed greedy rule, ensure the rule's first choice actually blocks a better solution.

| Bad rule | Counterexample | Why it fails |
| --- | --- | --- |
| Shortest duration first | One short middle interval surrounded by two compatible long intervals: choose intervals below. | The short activity blocks both long activities, while the long pair is compatible. |
| Fewest overlaps first | One uniquely low-overlap interval that blocks the middle of the optimal chain. | Low overlap count is static and does not measure future chain length. |
| Earliest start first | One very long early interval and many short intervals chained inside it. | Starting early can consume the whole timeline. |

Shortest-duration concrete intervals:

$$
[0,4),\ [3,5),\ [4,8)
$$

The shortest interval is the middle one, which yields one selected activity. The compatible pair is the first and third intervals, giving two activities.

Earliest-start concrete intervals:

$$
[0,10),\ [1,2),\ [2,3),\ [3,4)
$$

The earliest-start rule can choose the long interval and get one activity, while the short chain gives three.

Fewest-overlaps concrete intervals:

$$
[-1,1),\ [2,5),\ [0,3),\ [0,3),\ [0,3),\ [4,7),\ [6,9),\ [8,11),\ [8,11),\ [8,11),\ [10,12)
$$

The interval below is the unique fewest-overlaps activity; it overlaps only the two intervals shown after it.

$$
[4,7)
$$

$$
[2,5),\ [6,9)
$$

Therefore the rule selects that activity first. That choice blocks the four-activity optimum shown below. After selecting the chosen middle activity, one best completion has only three activities total.

$$
[-1,1),\ [4,7),\ [8,11)
$$

Another valid three-activity completion can use the final interval instead of the interval ending at eleven, but no completion after the greedy choice reaches four activities.

$$
[-1,1),\ [2,5),\ [6,9),\ [10,12)
$$

## Fractional and Indivisible Knapsack

For fractional knapsack, sort or select by value density and take as much as possible of the highest-density remaining item. The exchange proof shifts a small amount of weight from a lower-density item to a higher-density item and never decreases value.

For indivisible knapsack, do **not** use value density greedily without a special proof. The classic failure has a capacity of fifty and items with weights and values below.

$$
(10,60),\ (20,100),\ (30,120)
$$

The highest-density item alone with one other is worse than taking the second and third items. This is a signal for dynamic programming when weights are integral and capacity is moderate.

## Huffman Coding

Use Huffman coding for optimal binary prefix-free codes with positive character frequencies. Represent a code as a full binary tree whose leaves are characters. The objective is weighted external path length:

$$
B(T)=\sum_{c\in C} c.\mathrm{freq}\, d_T(c)
$$

Algorithm:

1. Put one leaf per character in a min-priority queue keyed by frequency.
2. Repeat until one tree remains: extract the two minimum-frequency trees, make them siblings under a new node, and insert the merged node with summed frequency.
3. Read codewords from root-to-leaf edge labels.

Correctness recipe:

1. **Greedy choice:** In some optimal full prefix-free tree, the two least frequent characters are sibling leaves at maximum depth.
2. Prove this by taking two maximum-depth sibling leaves in an optimal tree and swapping the least frequent characters into those positions. Since lower frequencies move no shallower, cost does not increase.
3. **Optimal substructure:** Merge the two least frequent characters into a pseudo-character with combined frequency. If the reduced tree is optimal, expanding that pseudo-character into the two leaves yields an optimal original tree.
4. Use the cost relation below when explaining the reduction.

$$
B(T)=B(T')+x.\mathrm{freq}+y.\mathrm{freq}
$$

With a binary min-heap, the running time is:

$$
O(n\lg n)
$$

Implementation judgment: in production, use platform compression libraries unless the task is educational, domain-specific, or needs custom static prefix codes. If implementing, define deterministic tie-breaking only for reproducibility; tie order does not affect optimal cost.

## Offline Caching

Use furthest-in-future, also called Belady's rule, when the entire request sequence is known. On a miss with a full cache, evict the cached block whose next request is farthest in the future; if a cached block is never requested again, evict such a block.

Proof recipe:

1. Consider a subproblem defined by the current cache contents and the current request index.
2. Optimal substructure holds because after processing the current request, the remaining decisions form the same problem with the resulting cache and next index.
3. For the greedy-choice property, take an optimal solution that evicts some block other than the furthest-in-future block.
4. Construct another solution that evicts the furthest-in-future block instead and shadows the original solution until the furthest-in-future block is requested.
5. Before that request, any hit made by the original solution is also a hit or is compensated by an earlier opposite hit in the modified solution.
6. At the furthest-in-future request, synchronize cache contents; after synchronization, make the same decisions as the original solution.
7. The modified solution has no more misses, so some optimum makes the greedy eviction.

Do not confuse offline optimal caching with real online cache managers. Least-recently-used uses the past as a heuristic and is not guaranteed optimal.

LRU counterexample with cache size three:

$$
1,2,3,1,2,4,1,2,3,4
$$

LRU and furthest-in-future both evict block three when block four first arrives. The difference appears later: on the miss for block three near the end, LRU evicts block four, which is requested immediately next, while furthest-in-future evicts a block with no future request and keeps block four.

## Other Greedy Patterns

| Problem | Greedy choice | Proof move | Watch for |
| --- | --- | --- | --- |
| Interval partitioning | Assign next start-time interval to a free room if possible, otherwise open a room | Depth lower bound equals maximum simultaneous intervals | Need a min-heap of room finish times |
| Unit intervals covering points | Cover the leftmost uncovered point with an interval starting there | Shift the first covering interval right or left without losing coverage | Sort points first |
| Water stops or refueling | Go as far as possible before stopping | Any earlier stop can be delayed to the greedy stop | Distances between consecutive stations must be feasible |
| Shortest processing time scheduling | Run shortest available job first in the nonpreemptive all-available case | Adjacent inversion exchange lowers total completion time | Release times and preemption change the rule |
| Coin change | Take largest coin first only for canonical systems | Prove by denomination structure or use DP | Arbitrary denominations fail |

## Answer Template

Use this structure for exercise answers:

1. **Algorithm.** State preprocessing, the greedy choice, and pseudocode.
2. **Invariant or residual problem.** Define what remains after each choice.
3. **Greedy-choice proof.** Show an arbitrary optimum can be transformed to include the greedy choice.
4. **Optimal substructure.** Show the greedy choice plus an optimal residual solution is globally optimal.
5. **Running time.** Account separately for sorting, priority queues, scanning, and output reconstruction.
6. **Counterexample if rejecting a rule.** Give intervals, weights, requests, or frequencies where the proposed first choice provably loses.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Saying earliest finish works but giving only intuition about leaving room for the future | Include the exchange that replaces the first activity in an optimum with the earliest-finishing activity |
| Giving a shortest-duration counterexample where the shortest choice still achieves optimum | Use a middle short interval that blocks two compatible outer intervals |
| Proving Huffman with "merge two smallest" folklore only | State prefix-free full-tree setting, sibling-leaf lemma, contraction subproblem, and cost relation |
| Treating offline caching as obvious because the evicted block is not needed soon | Include the shadowing or exchange argument and handle blocks never requested again |
| Applying value density to indivisible knapsack | Switch to dynamic programming or prove a special ordering condition |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Calling a greedy rule optimal because it maximizes remaining space | Prove a safe-choice exchange |
| Forgetting that half-open intervals allow equality at endpoints | Use start at or after previous finish for compatibility |
| Counting static overlaps for activity selection without considering future chains | Use overlap-count counterexamples or the earliest-finish proof |
| Omitting Huffman's prefix-free assumption | State binary prefix-free full tree before proving optimality |
| Forgetting to combine child frequencies in Huffman | Merged internal node frequency is the sum of its two children |
| Using LRU as if it were offline optimal | Furthest-in-future is optimal only with known future requests; LRU is online heuristic |
| Hiding preprocessing cost | Include sorting or heap-building costs separately from the greedy scan |

## Verification Pressure Tests

Use these to check future answers:

1. **Activity proof:** The answer should sort by finish time, accept compatible intervals, and include the exchange proof plus residual subproblem.
2. **Bad greedy traps:** The answer should disprove shortest duration, fewest overlaps, and earliest start with concrete examples where the proposed first choice loses.
3. **Huffman proof:** The answer should mention prefix-free full binary trees, the two least frequent sibling lemma, contraction into a pseudo-character, and the cost relation.
4. **Offline caching:** The answer should give furthest-in-future, handle never-used-again blocks, distinguish offline from online, and show why LRU can lose.
5. **Greedy versus DP:** The answer should choose fractional knapsack greedily but reject value-density greedy for indivisible knapsack unless extra structure is proven.
