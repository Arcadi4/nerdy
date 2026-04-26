---
name: online-algorithms
description: Use when analyzing online algorithms, competitive analysis, adversarial input, list update with move-to-front, online caching, paging, randomized marking, or ski-rental/elevator-style rent-or-buy decisions.
license: MIT
---

# Online Algorithms

## Overview

Online-algorithm answers must compare decisions made without future knowledge against an offline optimum that sees the entire input.

**Core principle:** never judge an online algorithm by its standalone worst case; judge the worst-case ratio between its cost and the cost of a future-knowing optimum under the same input model and adversary.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, direct polished answers, theorem preconditions, and formula-free headings.

## Answer Formatting Guardrail

Online-algorithm exercises often invite comparison tables. Do not put costs, thresholds, ratios, request sequences with symbolic block names, or potential-function expressions in table cells or inline code spans.

Use prose labels for cases, then put the associated expression in a display block immediately underneath. A safe pattern is:

1. Name the case in words.
2. State in prose which quantity is being computed.
3. Put the cost, ratio, bound, or sequence in a display block.
4. Return to prose for the interpretation.

If a verification answer needs a summary table, keep the table verbal only, such as "early arrival" and "ratio one," and put the exact expressions outside the table.

For elevator or ski-rental threshold answers, do not compress the case split to only the two dangerous ratios. Always name the harmless early-arrival piece first, then the just-after-give-up piece, then the late-arrival piece. The dangerous pieces determine the maximum, but the early piece confirms that the case split is complete.

## When to Use

Use this skill for:

- inputs revealed over time, including request sequences, releases, arrivals, or operation streams;
- competitive-ratio proofs for minimization problems;
- rent-or-buy or wait-then-switch strategies such as elevator, ski rental, and cow-path search;
- self-organizing lists, list update, move-to-front, and adjacent-swap cost models;
- online caching, paging, cache-eviction policies, marking algorithms, and adversarial lower bounds;
- randomized online algorithms where the adversary model determines whether randomization helps.

Do **not** use this skill merely because an algorithm processes a stream in one pass. If the task is about sublinear memory or pass complexity rather than comparing against an offline optimum, prefer a streaming-algorithms model if available.

## First Decision: What Is Being Compared?

Before computing a ratio, identify the exact quantities.

| Situation | Required framing |
| --- | --- |
| Online minimization | Compare the online cost on each input with the offline optimum cost on the same input. |
| Randomized online algorithm | Compare expected online cost against the offline optimum, and name what the adversary knows. |
| Deterministic lower bound | Construct an adversary that chooses future requests after knowing the deterministic algorithm's state. |
| Unbounded policy | Exhibit a request family where the ratio grows with request length. |
| Amortized online proof | Use a potential that measures distance from the offline configuration, then telescope. |

For minimization problems, the competitive-ratio target is the maximum ratio over all valid inputs:

$$
\max_{I \in U} \frac{A(I)}{F(I)}
$$

For randomized algorithms, the expectation is over the algorithm's random choices:

$$
\mathbf{E}[A(I)] \le c F(I)
$$

## Competitive Analysis Workflow

1. State what an input is and what the online algorithm knows when it must decide.
2. Define the offline optimum precisely; do not let it use different resources or a different cost model.
3. Write the online algorithm's cost as a piecewise function over the same input.
4. Divide the input space at the same thresholds used by the offline optimum and the online rule.
5. Maximize the ratio over the pieces; name the input that attains the maximum.
6. For lower bounds, define the adversary and the request sequence family before claiming the ratio.

## Rent-or-Buy and Wait-Then-Switch Problems

The elevator example is the prototype. If stairs cost a fixed amount and the elevator arrival time is unknown, a hedging strategy waits, then switches to the guaranteed action.

The offline optimum waits only when the elevator arrives soon enough:

$$
t(m) =
\begin{cases}
m + 1 & \text{if } m \le k - 1, \\
k & \text{if } m \ge k.
\end{cases}
$$

If the online strategy waits for a chosen amount of time before taking the stairs, the failure-prone step is remembering that switching still includes the time already spent waiting. Its cost is:

$$
h_p(m) =
\begin{cases}
m + 1 & \text{if } m \le p, \\
p + k & \text{if } m > p.
\end{cases}
$$

For integer arrival times with a useful switch before the offline stair threshold, the dangerous input is the first arrival time after the online algorithm gives up. The ratio from that piece is the expression below.

$$
\frac{p + k}{p + 2}
$$

The late-arrival piece contributes the expression below.

$$
\frac{p + k}{k}
$$

Do not relabel the just-after-give-up piece as early arrival. The early-arrival piece is the case where the elevator arrives before the online switch, and its ratio is:

$$
1
$$

For the variable-wait exercise, choose the waiting time that makes the just-after-give-up denominator match the late-arrival denominator. With integer arrival times, the optimal useful switch point is:

$$
p = k - 2
$$

The resulting maximum ratio is:

$$
2 - \frac{2}{k}
$$

The chapter's named hedge waits the stair time instead; it is the simpler ratio-two rule, not the optimizer for the variable-wait exercise.

## Search Lists and Move-to-Front

The list-maintenance model charges for both search and adjacent swaps.

- Searching for an item costs its current position in the list.
- Swapping adjacent items costs one per swap.
- `MOVE-TO-FRONT` searches for the item, then swaps it to the front.

The actual cost of a move-to-front access is:

$$
c_i^M = 2 r_{L_{i-1}^M}(x) - 1
$$

The offline algorithm `FORESEE` has its own list and may perform some number of adjacent swaps after the search:

$$
c_i^F = r_{L_{i-1}^F}(x) + t_i
$$

### Inversion Potential Proof Move

Use the inversion count between the online list and the offline list. The potential is twice the inversion count:

$$
\Phi_i = 2 I(L_i^M, L_i^F)
$$

For the searched element, split the other elements by their position relative to it before the access:

- `BB`: before the searched element in both lists;
- `BA`: before it in the move-to-front list but after it in the offline list;
- `AB`: after it in the move-to-front list but before it in the offline list.

Then the positions satisfy:

$$
r_{L_{i-1}^M}(x) = |BB| + |BA| + 1
$$

$$
r_{L_{i-1}^F}(x) = |BB| + |AB| + 1
$$

When move-to-front swaps the searched element forward, the inversion count increases for the elements in the shared-before set and decreases for the elements in the move-to-front-before/offline-after set:

$$
\Delta I = |BB| - |BA|
$$

The offline swaps can increase the potential by at most twice the number of swaps it performs. This yields the amortized bound:

$$
\hat{c}_i^M \le 4 c_i^F
$$

Because the initial potential is zero and the potential is always nonnegative, summing amortized costs bounds the total actual cost. Therefore move-to-front is four-competitive in this cost model.

### Per-Step Optimum Trap

Do not claim the offline optimum must pay no more than move-to-front on every individual request. Competitive analysis is about total cost over a sequence, and an offline optimum may pay extra early to reduce later cost.

A replayable counterexample starts with the list below.

$$
\langle 1, 2, 3, 4, 5 \rangle
$$

Use the request sequence below.

$$
5, 3, 4, 4
$$

`FORESEE` can move item four to the front after the search for item three, paying extra on that step because it knows two requests for item four are coming. On that step, `FORESEE` can pay more than move-to-front, even while its total sequence cost is lower.

## Online Caching and Paging

The caching problem has a sequence of block requests, a cache of fixed size, and a miss whenever the requested block is absent. Algorithms differ only in eviction choice on a miss when the cache is full.

### Deterministic Policies

| Policy | Competitive-analysis lesson |
| --- | --- |
| LIFO | Unbounded ratio in request length; do not use as a good online caching example. |
| LFU | Also vulnerable to unbounded behavior under adversarial sequences. |
| LRU | Epoch argument gives a ratio proportional to cache size. |
| FIFO | Also admits a ratio proportional to cache size. |
| Any deterministic online policy | A state-aware adversary forces a lower bound proportional to cache size. |

### Replayable LIFO Bad Sequence

Use blocks named by numbers. First fill the cache with the initial block range shown below.

$$
1, 2, 3, \ldots, k
$$

Then alternate between one extra block and the last loaded block.

$$
k + 1, k, k + 1, k, k + 1, k, \ldots
$$

After the cache fills, the request for the extra block evicts the last loaded block. The next request is for that just-evicted block, which evicts the extra block. This repeats, so LIFO misses on every request. The offline optimum evicts an irrelevant earlier block once and then keeps both alternating blocks.

### Epoch Proof for LRU

Define each epoch to begin when the sequence has just moved to the next block that makes the set of distinct blocks since the previous epoch exceed the cache capacity. In each epoch, LRU misses at most once per distinct block in that epoch, so at most the cache capacity times. The offline optimum must miss at least once per completed epoch because the first block of a new epoch was preceded by enough other distinct blocks to force absence from any cache of that size.

### Deterministic Lower Bound

Use a universe of one more block than cache capacity. After the cache initially fills, request the block that the deterministic online algorithm just evicted. The online algorithm misses every time. The offline furthest-in-future algorithm misses much less often because any evicted block will not be requested for many subsequent requests.

For sufficiently long sequences, the lower-bound ratio is proportional to the cache size. The proof depends on a deterministic algorithm whose state can be predicted by the adversary.

## Randomized Marking

`RANDOMIZED-MARKING` marks requested blocks. On a hit, it marks the block. On a miss, if all cached blocks are marked, it unmarks all cached blocks; then it evicts a uniformly random unmarked cached block, loads the requested block, and marks it.

Do not describe randomized marking as timestamp-based, least-recently-used, or mostly deterministic. Its analysis depends on random choice among unmarked blocks.

### Adversary Model

| Adversary | What it knows | Consequence |
| --- | --- | --- |
| Oblivious | The algorithm but not the realized random choices. | Randomized marking has logarithmic expected competitive ratio. |
| Nonoblivious | The realized random choices and cache state. | It can request the just-evicted block and erase the benefit of randomization. |
| Deterministic adversarial lower bound | The deterministic algorithm's future state. | It can force a miss on every request. |

### Old and New Requests

For randomized marking, analyze by epochs. Within an epoch, only the first request for each block matters for miss counting because the first request marks the block and later requests to that block in the same epoch hit.

- An old request asks for a block that was in the cache at the start of the epoch.
- A new request asks for a block not requested in the previous epoch.

New requests always miss. Old requests may miss only if random evictions removed them earlier in the epoch. The harmonic-number bound comes from summing the increasing miss probabilities for old requests as fewer unmarked old blocks remain.

If an epoch has the following number of new requests,

$$
r_i
$$

then randomized marking has expected misses bounded by:

$$
\mathbf{E}[X_i] \le r_i H_k
$$

Across adjacent epochs, the offline optimum must pay enough misses to cover the new blocks introduced. The standard two-epoch charging gives a logarithmic expected ratio:

$$
O(\lg k)
$$

## Online Scheduling Warning

For release-time scheduling to minimize average completion time, shortest-processing-time among currently available nonpreemptive jobs is not constant-competitive. The chapter's repair is to use the online behavior of shortest-remaining-processing-time to order jobs, then schedule nonpreemptively by completion order as jobs become known.

When answering this problem, separate three ideas:

1. Preemptive SRPT is online because a newly released shorter remaining job can interrupt the current job.
2. The preemptive completion-time sum lower-bounds the optimal nonpreemptive completion-time sum.
3. Greedily scheduling in SRPT completion order yields nonpreemptive completion times within a factor two.

## Production Translation

- Competitive ratio is a robustness certificate, not a forecast of typical performance.
- A smaller competitive ratio can still lose on common distributions; use empirical workload data when available.
- Caching policies in real systems also face concurrency, prefetching, writeback, scan resistance, and hardware constraints not modeled here.
- Randomized online guarantees must state the adversary model. Randomization that is observable to the request generator is often equivalent to determinism for worst-case analysis.
- Move-to-front teaches self-organization and potential-based comparison against an offline configuration; it is not automatically the right production list policy for every frequency-skewed workload.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Forgetting that waiting before taking stairs still costs waiting time. | Include the wait time in the switch-case cost before maximizing the ratio. |
| Optimizing a wait threshold against only one side of the input split. | Compare early-arrival, just-after-give-up, and late-arrival pieces. |
| Calling the just-after-give-up input an early-arrival case. | Reserve early arrival for elevator arrivals before the switch; call the boundary input just-after-give-up. |
| Describing move-to-front with a vague self-organization argument. | Use inversion count, the three named before-and-after sets, and amortized telescoping. |
| Claiming the offline optimum is no worse on every step. | Explain that offline may pay extra early and compare totals over the sequence. |
| Giving a LIFO bad example with all distinct requests and an incorrect offline cost. | Use the chapter sequence that alternates between the last loaded block and one extra block. |
| Describing randomized marking as timestamp or LRU-like. | State marks, unmarking all blocks, and uniform random eviction among unmarked blocks. |
| Claiming randomization helps against an adversary that sees random choices. | Distinguish oblivious and nonoblivious adversaries before stating the logarithmic bound. |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Comparing online cost to a clairvoyant algorithm with a different cache size, list operation, or resource budget. | Keep the resource model identical and change only future knowledge. |
| Treating competitive ratio as average-case performance. | It is a worst-case ratio over inputs. |
| Using a single worst-case input for the online algorithm without checking the offline cost on that input. | Compute both costs on the same sequence. |
| Omitting the input that attains the maximum ratio. | Name the adversarial arrival time or request sequence. |
| Proving randomized marking without naming the adversary. | State that the logarithmic bound is against an oblivious adversary. |
| Putting formulas inside Markdown table cells. | Keep table entries verbal and put formulas in display blocks nearby. |

## Worked Answer Pattern

For any online-algorithm exercise, use this compact structure:

1. **Model:** input sequence, online knowledge, offline knowledge, cost objective.
2. **Algorithm:** the online rule in operational terms.
3. **Offline benchmark:** what the future-knowing optimum can do on the same input.
4. **Upper bound or lower bound:** ratio calculation, potential argument, epoch argument, or adversarial sequence.
5. **Tightness or caveat:** matching lower bound, unboundedness, adversary model, or production limitation.

## Verification Pressure Tests

Use these prompts to test whether the skill changes behavior:

1. Derive the competitive ratio for waiting a chosen number of minutes before taking stairs, and identify the threshold that minimizes the maximum ratio.
2. Explain why `MOVE-TO-FRONT` is four-competitive under adjacent-swap costs, including the inversion potential and the role of `BB`, `BA`, and `AB`.
3. Refute the claim that an offline optimum must pay no more than move-to-front on every individual operation.
4. Give a LIFO cache request sequence where every request misses after the initial fill, and compute why the offline optimum does much better.
5. Prove the deterministic online caching lower bound using a request adversary that asks for the block just evicted.
6. Explain randomized marking's expected logarithmic bound and why it requires an oblivious adversary.
7. Distinguish online algorithms from streaming algorithms in a prompt about gradually arriving graph updates or memory requests.

## Static Checks

- File path is `clrs/online-algorithms/SKILL.md`.
- Frontmatter has `name: online-algorithms`, a trigger-only `description` starting with `Use when`, and `license: MIT`.
- Parent router `clrs/SKILL.md` includes an `online-algorithms` bullet.
- No formula appears in a Markdown heading, inline code span, table cell, or prose sentence.
- The skill covers elevator/rent-or-buy, move-to-front, deterministic caching, randomized marking, adversary models, and online scheduling.
- The chapter-specific facts stay here rather than in the parent CLRS router.
